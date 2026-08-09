import numpy as np
from scipy.io import wavfile
import os

sample_rate = 44100
duration = 45.0
t = np.linspace(0, duration, int(sample_rate * duration), False)

def karplus_strong(freq, dur, sr=44100):
    buf_len = int(sr / freq)
    buf = np.random.uniform(-1, 1, buf_len)
    samples = np.zeros(int(sr * dur))
    idx = 0
    for i in range(len(samples)):
        val = buf[idx]
        buf[idx] = 0.5 * (buf[idx] + buf[(idx + 1) % buf_len]) * 0.992
        samples[i] = val
        idx = (idx + 1) % buf_len
    return samples

def marimba_tone(freq, dur, sr=44100):
    t_n = np.linspace(0, dur, int(sr * dur), False)
    env = np.exp(-14.0 * t_n)
    sig = np.sin(2 * np.pi * freq * t_n) + 0.4 * np.sin(2 * np.pi * freq * 3.9 * t_n) + 0.15 * np.sin(2 * np.pi * freq * 9.2 * t_n)
    return sig * env

left_track = np.zeros_like(t)
right_track = np.zeros_like(t)

chords = [
    [130.81, 196.00, 261.63, 329.63, 392.00],  # C major
    [123.47, 196.00, 246.94, 293.66, 392.00],  # G/B
    [110.00, 164.81, 220.00, 261.63, 329.63],  # Am
    [87.31,  174.61, 220.00, 261.63, 349.23]   # F
]

melody_freqs = [
    523.25, 659.25, 783.99, 659.25, 587.33, 659.25, 587.33, 392.00,
    523.25, 659.25, 587.33, 523.25, 440.00, 523.25, 392.00, 329.63
]

bpm = 122
beat_len = 60.0 / bpm
step_len = beat_len / 2

for step in range(int(duration / step_len)):
    t_sec = step * step_len
    idx_s = int(t_sec * sample_rate)
    
    chord = chords[(step // 8) % len(chords)]
    note_f = chord[step % len(chord)]
    strum_dur = min(1.5, duration - t_sec)
    guitar_note = karplus_strong(note_f, strum_dur)
    
    marimba_f = note_f * 2
    marimba_note = marimba_tone(marimba_f, min(0.4, duration - t_sec))
    
    lead_sig = np.zeros(0)
    if step % 2 == 0:
        lead_f = melody_freqs[(step // 2) % len(melody_freqs)]
        t_l = np.linspace(0, 0.4, int(sample_rate * 0.4), False)
        lead_env = np.exp(-5.0 * t_l)
        lead_sig = (np.sin(2 * np.pi * lead_f * t_l) + 0.3 * np.sin(2 * np.pi * lead_f * 1.5 * t_l)) * lead_env * 0.25

    n_samples = min(len(guitar_note), len(marimba_note))
    idx_e = min(len(t), idx_s + n_samples)
    actual_len = idx_e - idx_s
    
    pan = 0.5 + 0.2 * np.sin(step * 0.6)
    sig_comb = (guitar_note[:actual_len] * 0.22) + (marimba_note[:actual_len] * 0.15)
    
    left_track[idx_s:idx_e] += sig_comb * (1 - pan)
    right_track[idx_s:idx_e] += sig_comb * pan
    
    if len(lead_sig) > 0:
        l_e = min(len(t), idx_s + len(lead_sig))
        a_l = l_e - idx_s
        left_track[idx_s:l_e] += lead_sig[:a_l] * 0.5
        right_track[idx_s:l_e] += lead_sig[:a_l] * 0.5

delay_samples = int(sample_rate * 0.04)
decay = 0.35
left_reverb = left_track.copy()
right_reverb = right_track.copy()
left_reverb[delay_samples:] += left_track[:-delay_samples] * decay
right_reverb[delay_samples:] += right_track[:-delay_samples] * decay

fade_start = int((duration - 3.0) * sample_rate)
left_reverb[fade_start:] *= np.linspace(1, 0, len(t) - fade_start)
right_reverb[fade_start:] *= np.linspace(1, 0, len(t) - fade_start)

master_stereo = np.vstack((left_reverb, right_reverb)).T
master_stereo /= np.max(np.abs(master_stereo)) + 1e-6
master_int16 = (master_stereo * 32767).astype(np.int16)

out_dir = r"C:\ai\Circle the Square\audio-refs"
os.makedirs(out_dir, exist_ok=True)
out_wav = os.path.join(out_dir, "acoustic_studio_soundtrack.wav")
wavfile.write(out_wav, sample_rate, master_int16)
print(f"[SUCCESS] Created physical-modelled Acoustic Studio Soundtrack: {out_wav} (45s)")
