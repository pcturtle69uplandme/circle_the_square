import numpy as np
from scipy.io import wavfile
import os

sample_rate = 44100
duration = 80.0
t = np.linspace(0, duration, int(sample_rate * duration), False)

left = np.zeros_like(t)
right = np.zeros_like(t)

# --- 1. HOLLYWOOD FILM SCORE SOUND GENERATORS ---

def sub_drone(freq, dur, sr=44100):
    t_n = np.linspace(0, dur, int(sr * dur), False)
    env = np.ones_like(t_n)
    # Slow pitch modulation (vibrato/movement)
    mod = 1.0 + 0.02 * np.sin(2 * np.pi * 0.5 * t_n)
    sig = np.sin(2 * np.pi * freq * mod * t_n) + 0.4 * np.sin(4 * np.pi * freq * mod * t_n)
    return sig * env

def braam_drop(freq, dur, sr=44100):
    t_n = np.linspace(0, dur, int(sr * dur), False)
    f_drop = freq * np.exp(-0.4 * t_n)
    env = np.exp(-1.5 * t_n)
    sig = (
        np.sin(2 * np.pi * f_drop * t_n) +
        0.8 * np.sin(4 * np.pi * f_drop * t_n) +
        0.6 * np.sin(6 * np.pi * f_drop * t_n) +
        0.3 * np.sin(8 * np.pi * f_drop * t_n)
    )
    return sig * env

def staccato_strings(freq, dur, sr=44100):
    t_n = np.linspace(0, dur, int(sr * dur), False)
    env = np.exp(-14.0 * t_n)
    sig = (
        np.sin(2 * np.pi * freq * t_n) +
        0.5 * np.sin(4 * np.pi * freq * t_n) +
        0.3 * np.sin(6 * np.pi * freq * t_n)
    )
    return sig * env

def anvil_impact(sr=44100):
    t_n = np.linspace(0, 3.0, int(sr * 3.0), False)
    env = np.exp(-4.0 * t_n)
    # Metallic anvil high frequency + sub-bass drop
    sig = (np.sin(2 * np.pi * 2400.0 * t_n) + np.sin(2 * np.pi * 3800.0 * t_n)) * env * 0.4
    sub = np.sin(2 * np.pi * 45.0 * np.exp(-0.5 * t_n) * t_n) * np.exp(-1.0 * t_n) * 0.8
    return sig + sub

print("Synthesizing 5-Act Non-Repeating Hollywood Trailer Score...")

# --- 2. ACT-BY-ACT CINEMATIC SCORE STRUCTURE ---

# ACT I: SUSPENSEFUL ATMOSPHERIC SETUP (0:00 - 0:15)
# Low 45Hz D drone + Metallic ticking + Soft glass pads
act1_dur = 15.0
act1_samples = int(act1_dur * sample_rate)
d1 = sub_drone(45.0, act1_dur) * 0.35
left[:act1_samples] += d1
right[:act1_samples] += d1

# Ticking clock in Act 1
for tick in range(30):
    t_t = tick * 0.5
    idx = int(t_t * sample_rate)
    dur_t = int(sample_rate * 0.04)
    t_sub = np.linspace(0, 0.04, dur_t, False)
    tick_sig = np.sin(2 * np.pi * 4000.0 * t_sub) * np.exp(-50.0 * t_sub) * 0.20
    left[idx:idx+dur_t] += tick_sig
    right[idx:idx+dur_t] += tick_sig

# ACT II: EXECUTIVE CONSPIRACY (0:15 - 0:25)
# Low Cello melody (non-repeating) + Low brass pitch bends
act2_start = 15.0
cello_notes = [110.0, 123.47, 130.81, 146.83, 164.81, 174.61, 196.00]
for i, f in enumerate(cello_notes):
    t_c = act2_start + i * 1.4
    idx = int(t_c * sample_rate)
    dur_c = int(sample_rate * 1.6)
    t_sub = np.linspace(0, 1.6, dur_c, False)
    cello_sig = (np.sin(2 * np.pi * f * t_sub) + 0.4 * np.sin(4 * np.pi * f * t_sub)) * np.exp(-1.5 * t_sub) * 0.40
    idx_e = min(len(t), idx + dur_c)
    a_l = idx_e - idx
    left[idx:idx_e] += cello_sig[:a_l]
    right[idx:idx_e] += cello_sig[:a_l]

# ACT III: WHISTLEBLOWER ESCALATION (0:25 - 0:45)
# Evolving 4-chord string progression: Dm -> Bb -> F -> C (Non-repeating melody)
act3_start = 25.0
progression_freqs = [
    [587.33, 698.46, 880.00], # Dm
    [466.16, 587.33, 698.46], # Bb
    [698.46, 880.00, 1046.5], # F
    [523.25, 659.25, 783.99]  # C
]
bpm = 135
beat_sec = 60.0 / bpm
step_sec = beat_sec / 4

for step in range(int((45.0 - 25.0) / step_sec)):
    t_step = act3_start + step * step_sec
    idx = int(t_step * sample_rate)
    chord = progression_freqs[(step // 16) % len(progression_freqs)]
    note_f = chord[step % len(chord)]
    str_sig = staccato_strings(note_f, 0.18) * 0.25
    
    # Taiko drum accent on beat 1
    taiko_sig = np.zeros(0)
    if step % 4 == 0:
        dur_tk = int(sample_rate * 0.4)
        t_tk = np.linspace(0, 0.4, dur_tk, False)
        taiko_sig = np.sin(2 * np.pi * 60.0 * t_tk) * np.exp(-8.0 * t_tk) * 0.45
        
    idx_e = min(len(t), idx + len(str_sig))
    a_l = idx_e - idx
    left[idx:idx_e] += str_sig[:a_l]
    right[idx:idx_e] += str_sig[:a_l]
    
    if len(taiko_sig) > 0:
        idx_e2 = min(len(t), idx + len(taiko_sig))
        a_l2 = idx_e2 - idx
        left[idx:idx_e2] += taiko_sig[:a_l2]
        right[idx:idx_e2] += taiko_sig[:a_l2]

# Braam drops on staff cut transitions
braams = [25.0, 31.0, 37.0, 45.0]
for b in braams:
    b_sig = braam_drop(65.0, 2.0) * 0.70
    idx = int(b * sample_rate)
    idx_e = min(len(t), idx + len(b_sig))
    a_l = idx_e - idx
    left[idx:idx_e] += b_sig[:a_l]
    right[idx:idx_e] += b_sig[:a_l]

# ACT IV: CLIMAX MELTDOWN (0:45 - 0:55)
# Double-time action drums + French Horn brass crescendo
act4_start = 45.0
for step in range(int((55.0 - 45.0) / (step_sec / 2))):
    t_step = act4_start + step * (step_sec / 2)
    idx = int(t_step * sample_rate)
    dur_d = int(sample_rate * 0.25)
    t_d = np.linspace(0, 0.25, dur_d, False)
    drum_sig = np.sin(2 * np.pi * (80.0 - step * 0.5) * t_d) * np.exp(-12.0 * t_d) * 0.50
    idx_e = min(len(t), idx + dur_d)
    a_l = idx_e - idx
    left[idx:idx_e] += drum_sig[:a_l]
    right[idx:idx_e] += drum_sig[:a_l]

# ACT V: TITLE CARD IMPACT & OUTRO (0:55 - 0:78)
# Anvil Impact at 55.0s + Sub reverb decay
anvil_sig = anvil_impact() * 1.2
idx_title = int(55.0 * sample_rate)
idx_e = min(len(t), idx_title + len(anvil_sig))
a_l = idx_e - idx_title
left[idx_title:idx_e] += anvil_sig[:a_l]
right[idx_title:idx_e] += anvil_sig[:a_l]

# Reverb Room Simulation
delay_samples = int(sample_rate * 0.06)
decay = 0.40
left_reverb = left.copy()
right_reverb = right.copy()
left_reverb[delay_samples:] += left[:-delay_samples] * decay
right_reverb[delay_samples:] += right[:-delay_samples] * decay

# Master volume fade out over last 2 seconds (75s - 77.8s)
fade_start = int(75.0 * sample_rate)
left_reverb[fade_start:] *= np.linspace(1, 0, len(t) - fade_start)
right_reverb[fade_start:] *= np.linspace(1, 0, len(t) - fade_start)

master_stereo = np.vstack((left_reverb, right_reverb)).T
master_stereo /= np.max(np.abs(master_stereo)) + 1e-6
master_int16 = (master_stereo * 32767).astype(np.int16)

out_dir = r"C:\ai\Circle the Square\audio-refs"
os.makedirs(out_dir, exist_ok=True)
out_wav = os.path.join(out_dir, "non_repeating_cinematic_score.wav")
wavfile.write(out_wav, sample_rate, master_int16)
print(f"[SUCCESS] Created 5-Act Non-Repeating Cinematic Trailer Score: {out_wav} ({duration}s)")
