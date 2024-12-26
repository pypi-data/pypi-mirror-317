# Fast Whisper Diarizer

Fast Whisper Diarizer is a Python package for audio transcription and speaker diarization using the Whisper model and NeMo toolkit.

## Installation

To install the package, run:

```sh
pip install fast-whisper-diarizer
```

## Usage

To use the `process_audio` function, you can follow the example below. This function allows you to process audio data for transcription and speaker diarization, accepting both file paths and in-memory bytes data as input.

### Example

```python
from fast_whisper_diarizer import process_audio

# Example usage with a file path
process_audio(
    audio_data="path/to/audio/file.wav",
    output_directory="path/to/output/directory",
    whisper_model_name="tiny.en",
    separate_vocals=True,
    processing_batch_size=8,
    language_code="en",
    suppress_numeric_tokens=True,
    computation_device="cuda"
)

# Example usage with in-memory bytes data
with open("path/to/audio/file.wav", "rb") as f:
    audio_bytes = f.read()

process_audio(
    audio_data=audio_bytes,
    output_directory="path/to/output/directory",
    whisper_model_name="tiny.en",
    separate_vocals=True,
    processing_batch_size=8,
    language_code="en",
    suppress_numeric_tokens=True,
    computation_device="cuda"
)
```

### Parameters
- **audio_data (str or bytes)**: The input audio, either as a file path (str) or in-memory bytes data (bytes).
- **output_directory (str, optional)**: The directory where output files will be saved. Defaults to the directory of the input file if not specified.
- **whisper_model_name (str)**: The name of the Whisper model to use for transcription. Defaults to "tiny.en".
- **separate_vocals (bool)**: Whether to perform vocal separation from the background music. Defaults to True.
- **processing_batch_size (int)**: The batch size for processing the audio. Defaults to 8.
- **language_code (str)**: The language code for transcription. Defaults to "en".
- **suppress_numeric_tokens (bool)**: Whether to suppress numeric tokens during transcription. Defaults to True.
- **computation_device (str)**: The device to use for computation, either "cuda" or "cpu". Defaults to "cuda" if available.

This function does not return a value but saves output files to the specified directory.
