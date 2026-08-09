import numpy as np
from scipy.io import wavfile
import os

sample_rate = 44100
out_dir = r"C:\ai\Circle the Square\audio-refs"

# ==========================================
# CLEAN ZONE SFX TRACK (NO NOISE / NO HISS)
# ==========================================
# 14.4 seconds for Shots 01 & 02
t_sfx = np.linspace(0, 14.4, int(sample_rate * 14.4), False)

# Pure smooth warm sub hum (60Hz & 120Hz pure sine waves - zero noise/hiss)
sub_hum = np.sin(2 * np.pi * 60.0 * t_sfx) * 0.08 + np.sin(2 * np.pi * 120.0 * t_sfx) * 0.05

# Smooth chime pings at start of Shot 01 (t=0.0s) and Shot 02 (t=7.2s)
chime1 = np.sin(2 * np.pi * 880.0 * t_sfx) * np.exp(-3.5 * t_sfx) * 0.20
chime2_t = np.maximum(0, t_sfx - 7.2)
chime2 = np.sin(2 * np.pi * 1046.5 * chime2_t) * np.exp(-3.5 * chime2_t) * 0.20

zone_sfx = sub_hum + chime1 + chime2
zone_sfx /= np.max(np.abs(zone_sfx)) + 1e-6

# Smooth 0.5s fade in and out to prevent click pops
fade_len = int(sample_rate * 0.5)
zone_sfx[:fade_len] *= np.linspace(0, 1, fade_len)
zone_sfx[-fade_len:] *= np.linspace(1, 0, fade_len)

zone_sfx_stereo = np.vstack((zone_sfx * 0.5, zone_sfx * 0.5)).T
zone_int16 = (zone_sfx_stereo * 32767).astype(np.int16)

sfx_wav = os.path.join(out_dir, "zone_ambient_sfx.wav")
wavfile.write(sfx_wav, sample_rate, zone_int16)
print(f"[SUCCESS] Regenerated clean Zone SFX Track (Hissing/Noise removed): {sfx_wav}")
