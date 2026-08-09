import numpy as np
from scipy.io import wavfile
import os

sample_rate = 44100
duration = 85.0 # Guaranteed 85s duration for 100% full coverage
t = np.linspace(0, duration, int(sample_rate * duration), False)

left = np.zeros_like(t)
right = np.zeros_like(t)

# --- CONSTANT UNIFIED THEME SYNTHESIZERS ---

def synth_bass_pulse(freq, dur, sr=44100):
    t_n = np.linspace(0, dur, int(sr * dur), False)
    env = np.exp(-6.0 * t_n)
    sig = np.sin(2 * np.pi * freq * t_n) + 0.5 * np.sin(4 * np.pi * freq * t_n)
    return sig * env

def acoustic_rhythm_guitar(freq, dur, sr=44100):
    buf_len = int(sr / freq)
    buf = np.random.uniform(-1, 1, buf_len)
    samples = np.zeros(int(sr * dur))
    idx = 0
    for i in range(len(samples)):
        val = buf[idx]
        buf[idx] = 0.5 * (buf[idx] + buf[(idx + 1) % buf_len]) * 0.993
        samples[i] = val
        idx = (idx + 1) % buf_len
    return samples

def unified_lead_theme(freq, dur, sr=44100):
    t_n = np.linspace(0, dur, int(sr * dur), False)
    env = np.sin(np.pi * t_n / dur) ** 0.6
    sig = (
        np.sin(2 * np.pi * freq * t_n) +
        0.4 * np.sin(2 * np.pi * freq * 2.0 * t_n) +
        0.2 * np.sin(2 * np.pi * freq * 3.0 * t_n)
    )
    return sig * env

def continuous_drone_pad(freq, dur, sr=44100):
    t_n = np.linspace(0, dur, int(sr * dur), False)
    mod = 1.0 + 0.01 * np.sin(2 * np.pi * 0.2 * t_n)
    sig = np.sin(2 * np.pi * freq * mod * t_n) + 0.3 * np.sin(2 * np.pi * freq * 2.0 * mod * t_n)
    return sig

print("Synthesizing 85-Second Constant Unified Corporate Action Theme...")

# 1. CONTINUOUS AMBIENT PAD & SUB-BASS DRONE (Uninterrupted 0.0s -> 85.0s)
pad_sig = continuous_drone_pad(110.0, duration) * 0.20 # A2 Pad
left += pad_sig
right += pad_sig

# 2. CONSTANT 128 BPM RHYTHMIC DRIVING PULSE & THEME
bpm = 128
beat_sec = 60.0 / bpm
step_sec = beat_sec / 2 # 8th note steps

# Unified Musical Chords: A Minor -> F Major -> C Major -> G Major
chords = [
    [110.00, 164.81, 220.00, 261.63], # Am
    [87.31,  130.81, 174.61, 220.00], # F
    [130.81, 196.00, 261.63, 329.63], # C
    [98.00,  146.83, 196.00, 246.94]  # G
]

# Catchy Unified Theme Melody (A Minor Scale)
melody_notes = [
    440.00, 523.25, 659.25, 587.33, 523.25, 440.00, 392.00, 440.00,
    523.25, 659.25, 783.99, 659.25, 587.33, 523.25, 440.00, 392.00
]

total_steps = int(duration / step_sec)

for step in range(total_steps):
    t_step = step * step_sec
    idx = int(t_step * sample_rate)
    
    # A) Driving Synth Bass Pulse (Every beat)
    chord = chords[(step // 8) % len(chords)]
    bass_f = chord[0]
    bass_sig = synth_bass_pulse(bass_f, 0.4) * 0.35
    
    # B) Acoustic Rhythm Guitar (Every step)
    guitar_f = chord[step % len(chord)]
    guitar_sig = acoustic_rhythm_guitar(guitar_f, 0.35) * 0.22
    
    # C) Unified Melodic Lead Theme (Every 2 steps)
    lead_sig = np.zeros(0)
    if step % 2 == 0:
        lead_f = melody_notes[(step // 2) % len(melody_notes)]
        lead_sig = unified_lead_theme(lead_f, 0.45) * 0.30

    # Mix into main stereo tracks
    max_len = max(len(bass_sig), len(guitar_sig), len(lead_sig))
    idx_e = min(len(t), idx + max_len)
    actual_len = idx_e - idx
    
    def safe_slice(arr, l):
        return arr[:l] if len(arr) >= l else np.pad(arr, (0, l - len(arr)))

    b_part = safe_slice(bass_sig, actual_len)
    g_part = safe_slice(guitar_sig, actual_len)
    l_part = safe_slice(lead_sig, actual_len)
    
    pan = 0.5 + 0.15 * np.sin(step * 0.5)
    
    left[idx:idx_e] += (b_part * 0.5) + (g_part * (1 - pan)) + (l_part * 0.5)
    right[idx:idx_e] += (b_part * 0.5) + (g_part * pan) + (l_part * 0.5)

# Reverb Room Simulation
delay_samples = int(sample_rate * 0.04)
decay = 0.35
left_reverb = left.copy()
right_reverb = right.copy()
left_reverb[delay_samples:] += left[:-delay_samples] * decay
right_reverb[delay_samples:] += right[:-delay_samples] * decay

# Master volume fade out over last 2.5 seconds (82.5s - 85.0s)
fade_start = int(82.5 * sample_rate)
left_reverb[fade_start:] *= np.linspace(1, 0, len(t) - fade_start)
right_reverb[fade_start:] *= np.linspace(1, 0, len(t) - fade_start)

master_stereo = np.vstack((left_reverb, right_reverb)).T
master_stereo /= np.max(np.abs(master_stereo)) + 1e-6
master_int16 = (master_stereo * 32767).astype(np.int16)

out_dir = r"C:\ai\Circle the Square\audio-refs"
os.makedirs(out_dir, exist_ok=True)
out_wav = os.path.join(out_dir, "constant_unified_action_theme.wav")
wavfile.write(out_wav, sample_rate, master_int16)
print(f"[SUCCESS] Created Constant 85s Unified Corporate Action Theme: {out_wav} ({duration}s)")
