from pydub import AudioSegment
from pydub.effects import speedup
import subprocess
import librosa
import numpy as np

# ==== SETTINGS ====
input_mp3 = "1 Hour Full Relax with top Bollywood Hindi Lofi Songs to Chill Relax Arijit Singh Lofi.mp3"

# Tempo settings
auto_detect_tempo = True
target_bpm = 0        # e.g., 85 if you want fixed, else keep 0
manual_tempo_percent = +3  # additional manual tempo change in %

# Key settings
auto_detect_key = True
change_to_key = None  # e.g., "C", "G#m", or None to keep original

# Reverb settings: choose "light", "medium", "deep"
reverb_type = "medium"

# ==== STEP 1: Load audio ====
audio = AudioSegment.from_file(input_mp3)
audio.export("debug_original.wav", format="wav")  # save for librosa

# ==== STEP 2: Auto detect tempo ====
y, sr = librosa.load("debug_original.wav")

tempo_detected, _ = librosa.beat.beat_track(y=y, sr=sr)

# Fix if tempo_detected is an array (take first element as float)
if isinstance(tempo_detected, np.ndarray):
    tempo_detected = float(tempo_detected[0])

print(f"DEBUG: tempo_detected type: {type(tempo_detected)}")
print(f"🎵 Detected BPM: {tempo_detected:.1f}")

# Decide final tempo change
if target_bpm > 0:
    tempo_change_ratio = target_bpm / tempo_detected
else:
    tempo_change_ratio = 1.0

# Apply manual adjustment too
tempo_change_ratio *= (1 + manual_tempo_percent / 100.0)

print(f"⚡ Applying tempo change ratio: {tempo_change_ratio:.3f}")

audio_tempo = speedup(audio, playback_speed=tempo_change_ratio)

# ==== STEP 3: Auto detect key ====
if auto_detect_key:
    chroma = librosa.feature.chroma_cens(y=y, sr=sr)
    chroma_mean = np.mean(chroma, axis=1)
    key_index = np.argmax(chroma_mean)
    keys_major = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    detected_key = keys_major[key_index]
    print(f"🎼 Detected key (approx): {detected_key}")

    if change_to_key:
        print(f"⚠️ Key change not yet implemented, keeping original key.")
else:
    detected_key = "Unknown"

# ==== STEP 4: Export temp WAV for reverb ====
temp_input = "temp_input.wav"
audio_tempo.export(temp_input, format="wav")

# ==== STEP 5: Apply reverb ====
if reverb_type == "light":
    reverb_filter = "aecho=0.8:0.88:40|60:0.3|0.2"
elif reverb_type == "deep":
    reverb_filter = "aecho=0.8:0.9:100|180:0.6|0.5"
else:  # medium
    reverb_filter = "aecho=0.8:0.88:60|100:0.4|0.3"

temp_output = "final_output_with_reverb.wav"
cmd = [
    "ffmpeg",
    "-y",
    "-i", temp_input,
    "-af", reverb_filter,
    temp_output
]
print(f"🌌 Applying reverb: {reverb_type}")
subprocess.run(cmd, check=True)

# ==== STEP 6: Export final MP3 ====
final_audio = AudioSegment.from_wav(temp_output)
final_mp3 = "Processed_Lofi_TempoReverb_Advanced.mp3"
final_audio.export(final_mp3, format="mp3")

print("✅ Done! Final processed file:", final_mp3)
print(f"✨ Detected BPM: {tempo_detected:.1f}, Detected Key: {detected_key}")
