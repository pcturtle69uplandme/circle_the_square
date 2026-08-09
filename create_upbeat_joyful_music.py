import numpy as np
from scipy.io import wavfile
import os

sample_rate = 44100
duration = 45.0  # 45 seconds track
t = np.linspace(0, duration, int(sample_rate * duration), False)

left = np.zeros_like(t)
right = np.zeros_like(t)

# Upbeat, joyful, bright corporate theme in C Major / G Major
# Bright plucks, marimba, cheerful acoustic ukulele feel (128 BPM)
notes = {
    'C4': 261.63, 'D4': 293.66, 'E4': 329.63, 'G4': 392.00,
    'A4': 440.00, 'C5': 523.25, 'D5': 587.33, 'E5': 659.25, 'G5': 783.99
}

# Upbeat chord progression: C - G - Am - F (4 bars loop)
bpm = 128
beat_sec = 60.0 / bpm
step_sec = beat_sec / 2  # 8th note bouncing rhythm

pattern = ['C4', 'E4', 'G4', 'C5', 'G4', 'E4', 'C5', 'E5',
           'B3', 'D4', 'G4', 'D5', 'G4', 'D4', 'B4', 'D5',
           'A3', 'C4', 'E4', 'A4', 'E4', 'C4', 'A4', 'C5',
           'F3', 'A3', 'C4', 'F4', 'C4', 'A3', 'F4', 'A4']

for step in range(int(duration / step_sec)):
    t_start = step * step_sec
    idx_start = int(t_start * sample_rate)
    idx_end = min(len(t), int((t_start + step_sec * 1.8) * sample_rate))
    dur_note = (idx_end - idx_start) / sample_rate
    t_note = np.linspace(0, dur_note, idx_end - idx_start, False)

    note_name = pattern[step % len(pattern)]
    freq = notes.get(note_name, 392.0)

    # 1. Joyful Ukulele / Marimba Pluck
    pluck_env = np.exp(-12.0 * t_note)
    pluck_tone = np.sin(2 * np.pi * freq * t_note) + 0.4 * np.sin(4 * np.pi * freq * t_note) + 0.2 * np.sin(6 * np.pi * freq * t_note)
    pluck_sig = pluck_tone * pluck_env * 0.22

    # 2. Bouncy Bass Note (every 2 steps)
    bass_sig = 0
    if step % 2 == 0:
        bass_freq = freq / 2.0
        bass_env = np.exp(-5.0 * t_note)
        bass_sig = np.sin(2 * np.pi * bass_freq * t_note) * bass_env * 0.30

    # 3. High Shimmer Bell / Chime (every 4 steps)
    shimmer_sig = 0
    if step % 4 == 0:
        shimmer_env = np.exp(-18.0 * t_note)
        shimmer_sig = np.sin(2 * np.pi * (freq * 2) * t_note) * shimmer_env * 0.12

    # Stereo panning
    pan = 0.5 + 0.25 * np.sin(step * 0.8)
    left[idx_start:idx_end] += (pluck_sig + bass_sig + shimmer_sig) * (1 - pan)
    right[idx_start:idx_end] += (pluck_sig + bass_sig + shimmer_sig) * pan

# Fade in and Fade out
fade_in_len = int(sample_rate * 1.0)
fade_out_len = int(sample_rate * 2.5)
left[:fade_in_len] *= np.linspace(0, 1, fade_in_len)
right[:fade_in_len] *= np.linspace(0, 1, fade_in_len)
left[-fade_out_len:] *= np.linspace(1, 0, fade_out_len)
right[-fade_out_len:] *= np.linspace(1, 0, fade_out_len)

# Normalize & export 16-bit WAV
audio_stereo = np.vstack((left, right)).T
audio_stereo /= np.max(np.abs(audio_stereo)) + 1e-6
audio_int16 = (audio_stereo * 32767).astype(np.int16)

out_dir = r"C:\ai\Circle the Square\audio-refs"
os.makedirs(out_dir, exist_ok=True)
out_wav = os.path.join(out_dir, "upbeat_joyful_theme.wav")
wavfile.write(out_wav, sample_rate, audio_int16)
print(f"Successfully generated upbeat joyful music track: {out_wav} (45s)")
