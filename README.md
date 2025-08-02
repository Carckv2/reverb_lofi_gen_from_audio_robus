# Lofi Audio Processor

This Python script processes a long audio file (e.g., a 1-hour lofi mix) by automatically detecting and optionally adjusting the tempo, detecting the musical key, applying a reverb effect, and exporting the final result as an MP3.

---

## Features

- **Automatic tempo detection** using `librosa`.
- Optional **tempo adjustment** by a fixed BPM or percentage.
- **Key detection** (approximate) using chroma features.
- Apply **reverb effect** with configurable intensity (light, medium, deep) using `ffmpeg`.
- Works on long audio files (e.g., 1 hour) and exports final processed MP3.

---

## Requirements

- Python 3.7+
- [pydub](https://github.com/jiaaro/pydub)
- [librosa](https://librosa.org/)
- `ffmpeg` installed and available in system PATH.

---

## Installation

1. Install Python packages:

```bash
pip install pydub librosa numpy
Install ffmpeg:

Windows: Download from https://ffmpeg.org/download.html and add to PATH.

Linux/macOS: Use package manager, e.g., sudo apt install ffmpeg.

Usage
Place your input audio file (e.g., MP3) in the same folder as the script or adjust the input_mp3 path in the script.

Configure settings inside the script:

target_bpm: Set to desired BPM or 0 to keep detected tempo.

manual_tempo_percent: Percentage to speed up (>0) or slow down (<0) tempo.

change_to_key: Set to a key string to change key (currently not implemented).

reverb_type: Choose from "light", "medium", or "deep".

Run the script:

python process_lofi.py
Output MP3 file will be saved as Processed_Lofi_TempoReverb_Advanced.mp3.

Notes
Key change is not implemented yet, only detection.

Tempo change adjusts playback speed uniformly.

Reverb is applied via ffmpeg audio filters.

Script exports intermediate WAV files for processing.

Long audio files may take several minutes to process depending on system specs.

License
This script is provided as-is under the MIT License. Use at your own risk.