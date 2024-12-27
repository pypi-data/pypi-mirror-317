# Modified version of https://github.com/ZFTurbo/Music-Source-Separation-Training/blob/main/inference.py by Roman Solovyev (ZFTurbo)

import argparse
import time
import librosa
from tqdm.auto import tqdm
import os
import glob
import torch
import numpy as np
import soundfile as sf
import torch.nn as nn

from bs_roformer.utils import PACKAGE_DIR, prefer_target_instrument, demix, get_model_from_config, ensure_model_exists

import warnings
warnings.filterwarnings("ignore")

def run_folder(model, args, config, device, verbose=False):
    start_time = time.time()
    model.eval()
    all_mixtures_path = glob.glob(args.input_folder + '/*.*')
    all_mixtures_path.sort()
    sample_rate = 44100
    if 'sample_rate' in config.audio:
        sample_rate = config.audio['sample_rate']
    print('Total files found: {} Use sample rate: {}'.format(len(all_mixtures_path), sample_rate))

    instruments = prefer_target_instrument(config)[:]

    os.makedirs(args.output_folder, exist_ok=True)

    if not verbose:
        all_mixtures_path = tqdm(all_mixtures_path, desc="Total progress")

    if args.disable_detailed_pbar:
        detailed_pbar = False
    else:
        detailed_pbar = True

    for path in all_mixtures_path:
        print("Starting processing track: ", path)
        if not verbose:
            all_mixtures_path.set_postfix({'track': os.path.basename(path)})
        try:
            mix, sr = librosa.load(path, sr=sample_rate, mono=False)
        except Exception as e:
            print('Cannot read track: {}'.format(path))
            print('Error message: {}'.format(str(e)))
            continue

        # Convert mono to stereo if needed
        if len(mix.shape) == 1:
            mix = np.stack([mix, mix], axis=0)

        mix_orig = mix.copy()
        if 'normalize' in config.inference:
            if config.inference['normalize'] is True:
                mono = mix.mean(0)
                mean = mono.mean()
                std = mono.std()
                mix = (mix - mean) / std

        if args.use_tta:
            # orig, channel inverse, polarity inverse
            track_proc_list = [mix.copy(), mix[::-1].copy(), -1. * mix.copy()]
        else:
            track_proc_list = [mix.copy()]

        full_result = []
        for mix in track_proc_list:
            waveforms = demix(config, model, mix, device, pbar=detailed_pbar, model_type=args.model_type)
            full_result.append(waveforms)

        # Average all values in single dict
        waveforms = full_result[0]
        for i in range(1, len(full_result)):
            d = full_result[i]
            for el in d:
                if i == 2:
                    waveforms[el] += -1.0 * d[el]
                elif i == 1:
                    waveforms[el] += d[el][::-1].copy()
                else:
                    waveforms[el] += d[el]
        for el in waveforms:
            waveforms[el] = waveforms[el] / len(full_result)

        # Calculate residual if lossless mode is enabled
        if args.lossless:
            # Step 1: Convert everything to tensors on the right device
            mix_orig_tensor = torch.tensor(mix_orig, device=device)
            waveform_tensors = {instr: torch.tensor(waveforms[instr], device=device) for instr in instruments}
            
            # Step 2: Calculate what's missing (the residual)
            sum_stems = sum(waveform_tensors[instr] for instr in instruments)
            residual = mix_orig_tensor - sum_stems
            
            # Step 3: Run the model again on just the residual
            residual_stems = demix(config, model, residual, device, pbar=detailed_pbar, model_type=args.model_type)
            residual_stems = {k: torch.tensor(v, device=device) for k, v in residual_stems.items()}
            
            # Distribute residual based on model's classification
            if 'drums' in instruments and 'other' in instruments:
                # Get drums confidence from model's output
                drums_ratio = torch.sum(torch.abs(residual_stems['drums'])) / (
                    torch.sum(torch.abs(residual_stems['drums'])) + torch.sum(torch.abs(residual_stems['other']))
                )
                
                # Hybrid approach:
                # 1. Use model's separated stems for the clear drum/other content
                # 2. Use ratio-based distribution for the ambiguous content
                drums_residual = residual_stems['drums']
                other_residual = residual_stems['other']
                
                # Calculate remaining ambiguous content
                ambiguous_residual = residual - (drums_residual + other_residual)
                
                # Add clear content plus ratio-weighted ambiguous content
                waveforms['drums'] = (waveform_tensors['drums'] + 
                                    drums_residual + 
                                    ambiguous_residual * drums_ratio).cpu().numpy()
                waveforms['other'] = (waveform_tensors['other'] + 
                                    other_residual + 
                                    ambiguous_residual * (1 - drums_ratio)).cpu().numpy()
            elif instruments:
                # Fallback: add to first stem if neither drums nor other exists
                first_stem = instruments[0]
                waveforms[first_stem] = (waveform_tensors[first_stem] + residual).cpu().numpy()

        # Create a new `instr` in instruments list, 'instrumental'
        if args.extract_instrumental:
            instr = 'vocals' if 'vocals' in instruments else instruments[0]
            if 'instrumental' not in instruments:
                instruments.append('instrumental')
            # Output "instrumental", which is an inverse of 'vocals' or the first stem in list if 'vocals' absent
            waveforms['instrumental'] = mix_orig - waveforms[instr]

        for instr in instruments:
            estimates = waveforms[instr].T
            if 'normalize' in config.inference:
                if config.inference['normalize'] is True:
                    estimates = estimates * std + mean
            file_name, _ = os.path.splitext(os.path.basename(path))
            if args.flac_file:
                output_file = os.path.join(args.output_folder, f"{file_name}_{instr}.flac")
                subtype = 'PCM_16' if args.pcm_type == 'PCM_16' else 'PCM_24'
                sf.write(output_file, estimates, sr, subtype=subtype)
            else:
                output_file = os.path.join(args.output_folder, f"{file_name}_{instr}.wav")
                subtype = 'PCM_16' if args.pcm_type == 'PCM_16' else 'PCM_24' if args.pcm_type == 'PCM_24' else 'FLOAT'
                sf.write(output_file, estimates, sr, subtype=subtype)

    time.sleep(1)
    print("Elapsed time: {:.2f} sec".format(time.time() - start_time))


def proc_folder(args):
    parser = argparse.ArgumentParser(description='BS-RoFormer Music Source Separation')
    parser.add_argument("input_path", nargs='?', type=str, help="path to a single audio file to process (optional)")
    parser.add_argument("--input_folder", type=str, help="folder with mixtures to process (ignored if input_path is provided)")
    parser.add_argument("--output_folder", default="output", type=str, help="path to store results as wav file")
    parser.add_argument("--model_type", type=str, default='bs_roformer', help="bs_roformer or mel_band_roformer")
    parser.add_argument("--config_path", type=str, 
                       default=os.path.join(PACKAGE_DIR, 'config_bs_roformer_384_8_2_485100.yaml'), 
                       help="path to config file")
    parser.add_argument("--start_check_point", type=str, 
                       default=os.path.join(PACKAGE_DIR, 'model_bs_roformer_ep_17_sdr_9.6568.ckpt'), 
                       help="Initial checkpoint to valid weights")
    parser.add_argument("--device_ids", nargs='+', type=int, default=0, help='list of gpu ids')
    parser.add_argument("--extract_instrumental", action='store_true', help="invert vocals to get instrumental if provided")
    parser.add_argument("--disable_detailed_pbar", action='store_true', help="disable detailed progress bar")
    parser.add_argument("--force_cpu", action = 'store_true', help="Force the use of CPU even if CUDA is available")
    parser.add_argument("--flac_file", action = 'store_true', help="Output flac file instead of wav")
    parser.add_argument("--pcm_type", type=str, choices=['PCM_16', 'PCM_24', 'FLOAT'], default='PCM_16', help="PCM type for WAVE OR FLAC files (PCM_16 or PCM_24)")
    parser.add_argument("--use_tta", action='store_true', help="Flag adds test time augmentation during inference (polarity and channel inverse). While this triples the runtime, it reduces noise and slightly improves prediction quality.")
    parser.add_argument("--lossless", action='store_true', default=True, help="Enable lossless mode - adds residual difference back to drums/other stems to preserve all audio content")
    parser.add_argument('--disable-lossless', dest='lossless', action='store_false')
    if args is None:
        args = parser.parse_args()
    else:
        args = parser.parse_args(args)

    # If single file is provided, create a temporary input folder with just that file
    if args.input_path and os.path.isfile(args.input_path):
        temp_input_folder = os.path.join(os.path.dirname(args.input_path), '.temp_input')
        os.makedirs(temp_input_folder, exist_ok=True)
        import shutil
        shutil.copy2(args.input_path, temp_input_folder)
        args.input_folder = temp_input_folder
    elif not args.input_folder:
        args.input_folder = 'input'  # default value if neither input_path nor input_folder is provided

    if args.lossless:
        print("Lossless mode enabled")

    device = "cpu"
    if args.force_cpu:
        device = "cpu"
    elif torch.cuda.is_available():
        print('CUDA is available, use --force_cpu to disable it.')
        device = "cuda"
        device = f'cuda:{args.device_ids[0]}' if type(args.device_ids) == list else f'cuda:{args.device_ids}'
    elif torch.backends.mps.is_available():
        device = "mps"

    print("Using device: ", device)

    model_load_start_time = time.time()
    torch.backends.cudnn.benchmark = True

    model, config = get_model_from_config(args.model_type, args.config_path)
    
    # Ensure model exists and get path
    model_path = ensure_model_exists(args.start_check_point)
    
    if model_path:
        print('Start from checkpoint: {}'.format(model_path))
        state_dict = torch.load(model_path, map_location=device, weights_only=True)
        model.load_state_dict(state_dict)
    print("Instruments: {}".format(config.training.instruments))

    # in case multiple CUDA GPUs are used and --device_ids arg is passed
    if type(args.device_ids) == list and len(args.device_ids) > 1 and not args.force_cpu:
        model = nn.DataParallel(model, device_ids = args.device_ids)

    model = model.to(device)

    print("Model load time: {:.2f} sec".format(time.time() - model_load_start_time))

    try:
        run_folder(model, args, config, device, verbose=True)
    finally:
        # Clean up temporary folder if it was created
        if args.input_path and os.path.exists(temp_input_folder):
            shutil.rmtree(temp_input_folder)


if __name__ == "__main__":
    proc_folder(None)