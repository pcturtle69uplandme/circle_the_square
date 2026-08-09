import numpy as np
from scipy.io import wavfile
import os

sample_rate = 44100
duration = 65.0
t = np.linspace(0, duration, int(sample_rate * duration), False)

left = np.zeros_like(t)
right = np.zeros_like(t)

# 1. METALLIC TICKING CLOCK (Act I: 0s - 15s)
for tick in range(30):
    t_tick = tick * 0.5
    idx_t = int(t_tick * sample_rate)
    if idx_t < len(t):
        dur_tick = int(sample_rate * 0.05)
        t_sub = np.linspace(0, 0.05, dur_tick, False)
        tick_sig = (np.sin(2 * np.pi * 3500.0 * t_sub) * np.exp(-40.0 * t_sub)) + (np.sin(2 * np.pi * 80.0 * t_sub) * np.exp(-20.0 * t_sub))
        left[idx_t:idx_t+dur_tick] += tick_sig * 0.25
        right[idx_t:idx_t+dur_tick] += tick_sig * 0.25

# 2. HOLLYWOOD BRASS BRAAM DROP FUNCTION (At key hit points: t=0s, 15s, 23s, 28s, 34s, 40s, 52s)
def add_braam(t_start, volume=0.7):
    idx_s = int(t_start * sample_rate)
    dur_b = int(sample_rate * 2.5)
    idx_e = min(len(t), idx_s + dur_b)
    actual_len = idx_e - idx_s
    t_b = np.linspace(0, actual_len / sample_rate, actual_len, False)
    
    # 40Hz Sawtooth/Brass Sub-Bass + Low Pitch Pitch-Bend
    f0 = 55.0 * np.exp(-0.8 * t_b) # Pitch drops from 55Hz to 40Hz
    env = np.exp(-1.2 * t_b)
    braam_sig = (np.sin(2 * np.pi * f0 * t_b) + 0.6 * np.sin(4 * np.pi * f0 * t_b) + 0.3 * np.sin(6 * np.pi * f0 * t_b)) * env * volume
    
    left[idx_s:idx_e] += braam_sig
    right[idx_s:idx_e] += braam_sig

braam_hits = [0.0, 15.0, 23.0, 28.0, 34.0, 40.0, 52.0]
for hit in braam_hits:
    add_braam(hit, volume=0.65)

# 3. HIGH-INTENSITY ACTION ORCHESTRAL PERCUSSION (23s - 52s)
bpm = 138
beat_sec = 60.0 / bpm
t_action_start = 23.0
t_action_end = 52.0

for beat in range(int((t_action_end - t_action_start) / beat_sec)):
    t_b = t_action_start + beat * beat_sec
    idx_s = int(t_b * sample_rate)
    dur_p = int(sample_rate * 0.3)
    idx_e = min(len(t), idx_s + dur_p)
    actual_len = idx_e - idx_s
    t_p = np.linspace(0, actual_len / sample_rate, actual_len, False)

    # Heavy Taiko Drum Slam
    taiko_env = np.exp(-10.0 * t_p)
    taiko_sig = np.sin(2 * np.pi * 70.0 * t_p) * taiko_env * 0.40
    
    # Fast Snare Rimshot (on alternating beats)
    rim_sig = 0
    if beat % 2 == 1:
        rim_env = np.exp(-25.0 * t_p)
        rim_sig = np.random.normal(0, 0.2, actual_len) * rim_env * 0.30

    left[idx_s:idx_e] += (taiko_sig + rim_sig)
    right[idx_s:idx_e] += (taiko_sig + rim_sig)

# Normalize & export 16-bit WAV
audio_stereo = np.vstack((left, right)).T
audio_stereo /= np.max(np.abs(audio_stereo)) + 1e-6
audio_int16 = (audio_stereo * 32767).astype(np.int16)

out_dir = r"C:\ai\Circle the Square\audio-refs"
os.makedirs(out_dir, exist_ok=True)
out_wav = os.path.join(out_dir, "action_trailer_soundtrack.wav")
wavfile.write(out_wav, sample_rate, audio_int16)
print(f"[SUCCESS] Generated Action Movie Trailer Audio Bed: {out_wav} (65s)")
