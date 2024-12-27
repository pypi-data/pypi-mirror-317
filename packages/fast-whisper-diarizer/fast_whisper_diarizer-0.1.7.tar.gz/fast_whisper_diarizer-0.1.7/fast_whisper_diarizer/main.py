import os
import torch
import logging
import argparse
import numpy as np
from typing import Dict, Any
import torchaudio
from deepmultilingualpunctuation import PunctuationModel
from transformers.pipelines import json
from .transcriber import transcribe_audio, initialize_transcriber_model
from .diarizer import assign_speaker_to_transcripts, perform_diarization
from .utils import cleanup, format_timestamp, setup_diarizer_config
import io


def initialize_models(whisper_model_name, computation_device="cuda" if torch.cuda.is_available() else "cpu"):
    """
    Initialize the transcription and diarization models.

    :param whisper_model_name: The name of the Whisper model to use for transcription.
    :param computation_device: Device to use for computation ('cpu' or 'cuda').
    """
    initialize_transcriber_model(whisper_model_name, computation_device)


def diarize_audio(
    audio_data: Any,
    whisper_model_name: str = "tiny.en",
    separate_vocals: bool = True,
    processing_batch_size: int = 8,
    language_code: str = "en",
    suppress_numeric_tokens: bool = True,
    computation_device: str = "cuda" if torch.cuda.is_available() else "cpu"
) -> None:
    """
    Process an audio file for transcription and speaker diarization.

    This function handles audio input from either a file path or in-memory bytes data.
    It performs optional vocal separation, transcribes the audio using the specified
    Whisper model, and applies speaker diarization to identify different speakers
    within the audio.

    Args:
        audio_data (str or bytes): The input audio, either as a file path (str) or
            in-memory bytes data (bytes).
        whisper_model_name (str): The name of the Whisper model to use for
            transcription. Defaults to "tiny.en".
        separate_vocals (bool): Whether to perform vocal separation from the
            background music. Defaults to True.
        processing_batch_size (int): The batch size for processing the audio.
            Defaults to 8.
        language_code (str): The language code for transcription. Defaults to "en".
        suppress_numeric_tokens (bool): Whether to suppress numeric tokens during
            transcription. Defaults to True.
        computation_device (str): The device to use for computation, either "cuda"
            or "cpu". Defaults to "cuda" if available.

    Raises:
        FileNotFoundError: If the audio file path does not exist.
        ValueError: If the audio_data is neither a file path nor bytes.
        Exception: For any other errors encountered during processing.

    Returns:
        None: This function does not return a value but saves output files to the
        specified directory.
    """
    # Check if audio_data is a file path or bytes
    if isinstance(audio_data, str):
        audio_path = audio_data
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
    elif isinstance(audio_data, bytes):
        audio_path = io.BytesIO(audio_data)
    else:
        raise ValueError("audio_data must be a file path or bytes data")

    # Create temporary directory
    temp_dir = os.path.join(os.getcwd(), "temp_outputs")
    os.makedirs(temp_dir, exist_ok=True)

    try:
        # Step 1: Stem audio if enabled
        if separate_vocals and isinstance(audio_path, str):
            return_code = os.system(
                f'python -m demucs.separate -n htdemucs --two-stems=vocals "{audio_path}" -o "{temp_dir}" --device "{computation_device}"'
            )
            if return_code != 0:
                logging.warning(
                    "Source splitting failed, using original audio file.")
                vocal_target = audio_path
            else:
                vocal_target = os.path.join(
                    temp_dir,
                    "htdemucs",
                    os.path.splitext(os.path.basename(audio_path))[0],
                    "vocals.wav",
                )
        else:
            vocal_target = audio_path

        # Ensure a valid language is set
        language_code = language_code or "en"

        # Step 2: Transcribe audio
        segments, info, audio_waveform = transcribe_audio(
            vocal_target,
            model_name=whisper_model_name,
            language=language_code,
            device=computation_device,
            batch_size=processing_batch_size,
            suppress_numerals=suppress_numeric_tokens
        )
        segments = [segment._asdict() for segment in segments]

        # Expand dimensions of audio_waveform
        audio_waveform = np.expand_dims(audio_waveform, axis=0)

        # Step 3: Save mono audio for diarization
        torchaudio.save(
            os.path.join(temp_dir, "mono_file.wav"),
            torch.from_numpy(audio_waveform),
            16000,
            channels_first=True,
        )
        # Step 4: Perform diarization
        speaker_timestamps = perform_diarization(
            os.path.join(temp_dir, "mono_file.wav"), temp_dir)

        final_transcript = assign_speaker_to_transcripts(
            segments, speaker_timestamps)
        # print(speaker_timestamps)
        print(json.dumps(final_transcript))
        return final_transcript
    except Exception as e:
        logging.error(f"Error processing audio: {str(e)}")
        raise
    finally:
        # Clean up temporary files
        cleanup(temp_dir)


def main():
    parser = argparse.ArgumentParser(
        description="Audio Transcription and Diarization")
    parser.add_argument("audio_path", help="Path to the input audio file")
    parser.add_argument(
        "--model", default="tiny.en",
        help="Whisper model name")
    parser.add_argument("--no-stem", action="store_false", dest="enable_stemming",
                        help="Disable vocal separation")
    parser.add_argument("--batch-size", type=int, default=8, help="Batch size")
    parser.add_argument(
        "--language", help="Language code (auto-detect if not specified)")
    parser.add_argument("--no-suppress-numerals", action="store_false",
                        dest="suppress_numerals", help="Don't suppress numerical tokens")

    try:
        args = parser.parse_args()

        diarize_audio(
            audio_data=args.audio_path,
            whisper_model_name=args.model,
            separate_vocals=args.enable_stemming,
            processing_batch_size=args.batch_size,
            language_code=args.language,
            suppress_numeric_tokens=args.suppress_numerals
        )
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
