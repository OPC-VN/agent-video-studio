# Adapted from TMElyralab/MuseTalk at 2536eaf06b85f775d8e04b7fd81bf6699155a58d.
import math
import os

import soundfile
import numpy as np
import torch
from transformers import AutoFeatureExtractor


class AudioProcessor:
    def __init__(self, feature_extractor_path="openai/whisper-tiny/"):
        self.feature_extractor = AutoFeatureExtractor.from_pretrained(feature_extractor_path, local_files_only=True)

    def get_audio_feature(self, wav_path, start_index=0, weight_dtype=None):
        if not os.path.exists(wav_path):
            raise FileNotFoundError(wav_path)
        samples, sampling_rate = soundfile.read(wav_path, dtype="float32")
        if sampling_rate != 16000 or samples.ndim != 1:
            raise ValueError("audio must be a mono 16 kHz WAV")
        # Split audio into 30s segments
        segment_length = 30 * sampling_rate
        segments = [samples[i:i + segment_length] for i in range(0, len(samples), segment_length)]

        features = []
        for segment in segments:
            audio_feature = self.feature_extractor(
                segment,
                return_tensors="pt",
                sampling_rate=sampling_rate
            ).input_features
            if weight_dtype is not None:
                audio_feature = audio_feature.to(dtype=weight_dtype)
            features.append(audio_feature)

        return features, len(samples)

    def get_whisper_chunk(
        self,
        whisper_input_features,
        device,
        weight_dtype,
        whisper,
        sample_count,
        fps=25,
        audio_padding_length_left=2,
        audio_padding_length_right=2,
    ):
        audio_feature_length_per_frame = 2 * (audio_padding_length_left + audio_padding_length_right + 1)
        whisper_feature = []
        # Process multiple 30s mel input features
        for input_feature in whisper_input_features:
            input_feature = input_feature.to(device).to(weight_dtype)
            audio_feats = whisper.encoder(input_feature, output_hidden_states=True).hidden_states
            audio_feats = torch.stack(audio_feats, dim=2)
            whisper_feature.append(audio_feats)

        whisper_feature = torch.cat(whisper_feature, dim=1)
        # Trim the last segment to remove padding
        sr = 16000
        audio_fps = 50
        fps = int(fps)
        whisper_idx_multiplier = audio_fps / fps
        num_frames = math.floor((sample_count / sr) * fps)
        actual_length = math.floor((sample_count / sr) * audio_fps)
        whisper_feature = whisper_feature[:,:actual_length,...]

        # Calculate padding amount
        padding_nums = math.ceil(whisper_idx_multiplier)
        # Add padding at start and end
        batch, _, layers, width = whisper_feature.shape
        left = whisper_feature.new_zeros((batch, padding_nums * audio_padding_length_left, layers, width))
        right = whisper_feature.new_zeros((batch, padding_nums * 3 * audio_padding_length_right, layers, width))
        whisper_feature = torch.cat((left, whisper_feature, right), dim=1)

        audio_prompts = []
        for frame_index in range(num_frames):
            try:
                audio_index = math.floor(frame_index * whisper_idx_multiplier)
                audio_clip = whisper_feature[:, audio_index: audio_index + audio_feature_length_per_frame]
                if audio_clip.shape[1] != audio_feature_length_per_frame:
                    raise ValueError("unexpected audio chunk length")
                audio_prompts.append(audio_clip)
            except Exception as e:
                raise RuntimeError("invalid Whisper audio chunk") from e

        audio_prompts = torch.cat(audio_prompts, dim=0)  # T, 10, 5, 384
        audio_prompts = audio_prompts.flatten(1, 2)
        return audio_prompts
