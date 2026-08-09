import numpy as np
from scipy.io import wavfile
import os

sample_rate = 44100
duration = 38.0  # 38 seconds total video soundtrack
t = np.linspace(0, duration, int(sample_rate * duration), False)

# Initialize stereo audio track
left = np.zeros_like(t)
right = np.zeros_like(t)

# Corporate Mockumentary Theme (Acoustic Guitar Strum + Marimba + Pizzicato Bass)
# Key of A Major (A, C#, E, F#)
notes = {
    'A2': 110.0, 'E3': 164.81, 'A3': 220.0, 'C#4': 277.18, 
    'E4': 329.63, 'F#4': 369.99, 'A4': 440.0, 'C#5': 554.37
}

# Arpeggio pattern over 38 seconds
arpeggio_notes = ['A3', 'C#4', 'E4', 'A4', 'E4', 'C#4', 'F#4', 'C#5']
beat_duration = 0.4  # 150 BPM upbeat corporate rhythm

for beat in range(int(duration / beat_duration)):
    t_start = beat * beat_duration
    idx_start = int(t_start * sample_rate)
    idx_end = min(len(t), int((t_start + beat_duration * 1.5) * sample_rate))
    dur_note = (idx_end - idx_start) / sample_rate
    t_note = np.linspace(0, dur_note, idx_end - idx_start, False)

    # 1. Acoustic Guitar Note
    freq = notes[arpeggio_notes[beat % len(arpeggio_notes)]]
    guitar_env = np.exp(-4.0 * t_note)
    guitar_tone = np.sin(2 * np.pi * freq * t_note) + 0.3 * np.sin(4 * np.pi * freq * t_note)
    guitar_sig = guitar_tone * guitar_env * 0.25

    # 2. Marimba Tick (percussive high ping)
    marimba_env = np.exp(-15.0 * t_note)
    marimba_sig = np.sin(2 * np.pi * (freq * 2) * t_note) * marimba_env * 0.15

    # 3. Low Pizzicato Bass Note (on every 4th beat)
    bass_sig = 0
    if beat % 4 == 0:
        bass_freq = notes['A2']
        bass_env = np.exp(-2.5 * t_note)
        bass_sig = np.sin(2 * np.pi * bass_freq * t_note) * bass_env * 0.35

    # Combine with panning
    pan = 0.5 + 0.2 * np.sin(beat * 0.5)  # Soft stereo motion
    left[idx_start:idx_end] += (guitar_sig + marimba_sig + bass_sig) * (1 - pan)
    right[idx_start:idx_end] += (guitar_sig + marimba_sig + bass_sig) * pan

# Fade in and Fade out
fade_len = int(sample_rate * 2.0)
fade_in = np.linspace(0, 1, fade_len)
fade_out = np.linspace(1, 0, fade_len)

left[:fade_len] *= fade_in
right[:fade_len] *= fade_in
left[-fade_len:] *= fade_out
right[-fade_len:] *= fade_out

# Normalize & export 16-bit WAV
audio_stereo = np.vstack((left, right)).T
audio_stereo /= np.max(np.abs(audio_stereo)) + 1e-6
audio_int16 = (audio_stereo * 32767).astype(np.int16)

out_dir = r"C:\ai\Circle the Square\audio-refs"
os.makedirs(out_dir, exist_ok=True)
out_wav = os.path.join(out_dir, "opening_theme_music.wav")
wavfile.write(out_wav, sample_rate, audio_int16)
print(f"Successfully generated corporate acoustic theme music track: {out_wav} (38s)")
