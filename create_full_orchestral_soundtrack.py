import numpy as np
from scipy.io import wavfile
import os

sample_rate = 44100
duration = 80.0 # Full 80s coverage
t = np.linspace(0, duration, int(sample_rate * duration), False)

left = np.zeros_like(t)
right = np.zeros_like(t)

# --- 1. FULL ORCHESTRAL INSTRUMENT SYNTHESIZERS ---

def staccato_strings(freq, dur, sr=44100):
    # Rapid 16th-note violin string bow attack (Sawtooth + High-pass resonance filter)
    t_n = np.linspace(0, dur, int(sr * dur), False)
    env = np.exp(-12.0 * t_n)
    # Harmonics: Fundamental + 2nd, 3rd, 4th, 5th harmonics
    sig = (
        np.sin(2 * np.pi * freq * t_n) +
        0.5 * np.sin(4 * np.pi * freq * t_n) +
        0.3 * np.sin(6 * np.pi * freq * t_n) +
        0.2 * np.sin(8 * np.pi * freq * t_n)
    )
    return sig * env

def brass_section_braam(freq, dur, sr=44100):
    # Heavy French Horn & Trombone Brass ensemble (Sawtooth + Low Pitch Drop)
    t_n = np.linspace(0, dur, int(sr * dur), False)
    f_drop = freq * np.exp(-0.3 * t_n)
    env = np.exp(-1.5 * t_n)
    sig = (
        np.sin(2 * np.pi * f_drop * t_n) +
        0.8 * np.sin(4 * np.pi * f_drop * t_n) +
        0.6 * np.sin(6 * np.pi * f_drop * t_n) +
        0.4 * np.sin(8 * np.pi * f_drop * t_n) +
        0.25 * np.sin(10 * np.pi * f_drop * t_n)
    )
    return sig * env

def timpani_roll(freq, dur, sr=44100):
    # Low Orchestral Timpani Drum Slam
    t_n = np.linspace(0, dur, int(sr * dur), False)
    env = np.exp(-4.0 * t_n)
    sig = np.sin(2 * np.pi * freq * (1 - 0.2 * t_n) * t_n) * env
    return sig

def tubular_bell(freq, dur, sr=44100):
    # Orchestral Chime / Tubular Bell
    t_n = np.linspace(0, dur, int(sr * dur), False)
    env = np.exp(-3.0 * t_n)
    sig = (np.sin(2 * np.pi * freq * t_n) + 0.5 * np.sin(2 * np.pi * freq * 2.76 * t_n)) * env
    return sig

# --- 2. ORCHESTRAL COMPOSITION & HARMONY ---

bpm = 135
beat_sec = 60.0 / bpm
step_sec = beat_sec / 4 # 16th note steps

# Orchestral Chord Progression: D minor - Bb Major - F Major - C Major
chord_roots = [146.83, 116.54, 174.61, 130.81] # D3, Bb2, F3, C3
violin_melody = [
    587.33, 698.46, 880.00, 698.46, 587.33, 523.25, 698.46, 523.25,
    440.00, 587.33, 698.46, 587.33, 523.25, 440.00, 392.00, 440.00
]

print("Synthesizing Full Orchestral Action Score with Strings, Brass, Timpani, and Chimes...")

total_steps = int(duration / step_sec)

for step in range(total_steps):
    t_sec = step * step_sec
    idx_s = int(t_sec * sample_rate)
    
    # Root Chord Index
    root_f = chord_roots[(step // 16) % len(chord_roots)]
    
    # A) Staccato Violin 16th-note Ostinato (Plays continuously throughout)
    v_freq = violin_melody[step % len(violin_melody)]
    str_sig = staccato_strings(v_freq, 0.2)
    
    # B) Low Cello & Contrabass Bassline Pulse (Quarter notes)
    bass_sig = np.zeros(0)
    if step % 4 == 0:
        bass_sig = staccato_strings(root_f / 2, 0.45)
        
    # C) Full Orchestral Brass Ensemble Braam (Downbeats every 2 bars / 32 steps)
    brass_sig = np.zeros(0)
    if step % 32 == 0 or step % 32 == 16:
        brass_sig = brass_section_braam(root_f, 1.8)
        
    # D) Timpani Drum Slams (On beat 1 and beat 3)
    timp_sig = np.zeros(0)
    if step % 8 == 0 or step % 8 == 6:
        timp_sig = timpani_roll(root_f / 2, 0.8)
        
    # E) Tubular Chime Bells (On major chord shifts)
    bell_sig = np.zeros(0)
    if step % 16 == 0:
        bell_sig = tubular_bell(v_freq * 2, 1.5)

    # Mix into Stereo Track
    max_len = max(len(str_sig), len(bass_sig), len(brass_sig), len(timp_sig), len(bell_sig))
    idx_e = min(len(t), idx_s + max_len)
    actual_len = idx_e - idx_s

    def safe_slice(arr, l):
        return arr[:l] if len(arr) >= l else np.pad(arr, (0, l - len(arr)))

    str_part = safe_slice(str_sig, actual_len) * 0.22
    bass_part = safe_slice(bass_sig, actual_len) * 0.35
    brass_part = safe_slice(brass_sig, actual_len) * 0.45
    timp_part = safe_slice(timp_sig, actual_len) * 0.40
    bell_part = safe_slice(bell_sig, actual_len) * 0.18

    # Stereo Panning (Strings left, Brass right, Timpani center)
    pan_str = 0.35
    pan_brass = 0.65
    
    left[idx_s:idx_e] += str_part * (1 - pan_str) + brass_part * (1 - pan_brass) + bass_part * 0.5 + timp_part * 0.5 + bell_part * 0.5
    right[idx_s:idx_e] += str_part * pan_str + brass_part * pan_brass + bass_part * 0.5 + timp_part * 0.5 + bell_part * 0.5

# Hall Reverb (Convolution delay)
delay_samples = int(sample_rate * 0.05) # 50ms orchestral hall reflection
decay = 0.40
left_reverb = left.copy()
right_reverb = right.copy()
left_reverb[delay_samples:] += left[:-delay_samples] * decay
right_reverb[delay_samples:] += right[:-delay_samples] * decay

# Master volume fade out over last 2 seconds
fade_start = int((duration - 2.0) * sample_rate)
left_reverb[fade_start:] *= np.linspace(1, 0, len(t) - fade_start)
right_reverb[fade_start:] *= np.linspace(1, 0, len(t) - fade_start)

master_stereo = np.vstack((left_reverb, right_reverb)).T
master_stereo /= np.max(np.abs(master_stereo)) + 1e-6
master_int16 = (master_stereo * 32767).astype(np.int16)

out_dir = r"C:\ai\Circle the Square\audio-refs"
os.makedirs(out_dir, exist_ok=True)
out_wav = os.path.join(out_dir, "full_orchestral_action_soundtrack.wav")
wavfile.write(out_wav, sample_rate, master_int16)
print(f"[SUCCESS] Created Full Orchestral Action Soundtrack: {out_wav} ({duration}s)")
