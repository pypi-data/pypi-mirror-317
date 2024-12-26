# Fast Whisper Diarizer

Fast Whisper Diarizer is a Python package for audio transcription and speaker diarization using the Whisper model and NeMo toolkit.

## Installation

To install the package, run:

```sh
pip install fast-whisper-diarizer
```

## Initialization

Before using the `diarize_audio` function, you need to initialize the models using the `initialize_models` function. This ensures that the necessary models are loaded and ready for processing.

Example:

```python
from fast_whisper_diarizer import initialize_models

whisper_model_name = "tiny.en"

# Initialize models
initialize_models(whisper_model_name)
```

## Usage

To use the `diarize_audio` function, you can follow the example below. This function allows you to process audio data for transcription and speaker diarization, accepting both file paths and in-memory bytes data as input.

### Example

```python
from fast_whisper_diarizer import diarize_audio

# Example usage with a file path
final_transcript = diarize_audio(
    audio_data="path/to/audio/file.wav",
    whisper_model_name="tiny.en"
)
print(final_transcript)

# Example usage with in-memory bytes data
with open("path/to/audio/file.wav", "rb") as f:
    audio_bytes = f.read()

final_transcript = diarize_audio(
    audio_data=audio_bytes,
    whisper_model_name="tiny.en"
)
print(final_transcript)
```

### Parameters

- **audio_data (str or bytes)**: The input audio, either as a file path (str) or in-memory bytes data (bytes).
- **whisper_model_name (str)**: The name of the Whisper model to use for transcription.

### Optional Parameters

| Parameter                 | Type   | Default | Description                                          |
| ------------------------- | ------ | ------- | ---------------------------------------------------- |
| `separate_vocals`         | `bool` | `True`  | Whether to separate vocals from the audio.           |
| `processing_batch_size`   | `int`  | `8`     | Batch size for processing audio.                     |
| `language_code`           | `str`  | `None`  | Language code for transcription.                     |
| `suppress_numeric_tokens` | `bool` | `True`  | Whether to suppress numeric tokens in transcription. |
| `computation_device`      | `str`  | `'cpu'` | Device to use for computation ('cpu' or 'cuda').     |
