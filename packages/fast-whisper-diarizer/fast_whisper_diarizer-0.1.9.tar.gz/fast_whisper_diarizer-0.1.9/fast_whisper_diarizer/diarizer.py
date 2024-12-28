import os
import torch
import torchaudio
import logging
from typing import Counter, List, Dict, Any, Optional
from omegaconf import OmegaConf
import wget
import json
from nemo.collections.asr.models.msdd_models import NeuralDiarizer
from .utils import setup_diarizer_config


def perform_diarization(audio_path: str, temp_dir: str) -> List[List[float]]:
    """Perform speaker diarization on the audio file."""
    # Determine the device to use
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # Initialize NeMo MSDD diarization model with the correct device
    msdd_model = NeuralDiarizer(cfg=setup_diarizer_config(temp_dir)).to(device)
    msdd_model.diarize()

    # Clean up CUDA memory if used
    if device == "cuda":
        torch.cuda.empty_cache()

    # Read and parse RTTM file
    speaker_ts = []
    rttm_file = os.path.join(temp_dir, "pred_rttms", "mono_file.rttm")

    with open(rttm_file, "r") as f:
        for line in f:
            line_list = line.split(" ")
            start = int(float(line_list[5]) * 1000)
            duration = int(float(line_list[8]) * 1000)
            speaker_id = int(line_list[11].split("_")[-1])
            speaker_ts.append([start, start + duration, speaker_id])

    return speaker_ts


MILLISECONDS = 1000


def assign_speaker_to_transcripts(transcripts, diarization_timestamps):
    """
    Assign speakers to transcript segments based on diarization timestamps.

    Args:
        transcripts (list): List of transcript segments, each containing 'start', 'end', and 'text'.
        diarization_timestamps (list): List of diarization timestamps, each containing start time, end time, and speaker ID.

    Returns:
        list: List of transcript segments with assigned speakers.
    """
    result = []

    # Loop through each transcript segment
    for segment in transcripts:
        segment_start = segment["start"] * MILLISECONDS
        segment_end = segment["end"] * MILLISECONDS
        assigned_speakers = []  # List to store all speakers if multiple overlaps

        # Loop through each diarization period
        for timestamp in diarization_timestamps:
            diarization_start, diarization_end, speaker = timestamp
            if (
                segment_start <= diarization_end and
                segment_end >= diarization_start
            ):
                # Check if there's any overlap between the segment and the diarization period
                assigned_speakers.append(speaker)
            # Determine the most frequent speaker (or first in case of a tie)
            if assigned_speakers:
                speaker_counts = Counter(assigned_speakers)
                # Get the most common speaker, in case of a tie, the first is selected
                most_common_speaker = speaker_counts.most_common(1)[0][0]
            else:
                most_common_speaker = None  # No speaker assigned if there's no overlap

        # Add the assigned speakers (if more than one overlap, we capture all speakers)
        result.append({
            "text": segment["text"],
            "start": segment_start,
            "end": segment_end,
            "speaker": most_common_speaker+1 if most_common_speaker is not None else None
        })

    return result
