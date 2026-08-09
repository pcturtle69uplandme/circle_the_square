import os
import subprocess
import imageio_ffmpeg
import numpy as np
from moviepy import VideoFileClip

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
s09_path = r"C:\ai\Circle the Square\clips\OPENING_S09.mp4"
v9 = VideoFileClip(s09_path)

print(f"OPENING_S09 Duration: {v9.duration}s")

# Extract audio to wav file
out_wav = r"C:\ai\Circle the Square\audio-refs\s09_voice_extracted.wav"
cmd = [FFMPEG, "-y", "-i", s09_path, "-vn", "-acodec", "pcm_s16le", "-ar", "44100", "-ac", "2", out_wav]
subprocess.run(cmd, check=True)

# Sample audio volume at every 0.5s inside S09
arr = v9.audio.to_soundarray(fps=44100)
for t_ms in range(0, int(v9.duration * 1000), 500):
    t_sec = t_ms / 1000.0
    idx_s = int(t_sec * 44100)
    idx_e = int(min(len(arr), idx_s + 44100 * 0.5))
    chunk = arr[idx_s:idx_e]
    rms = np.sqrt(np.mean(chunk**2)) if len(chunk) > 0 else 0
    db = 20 * np.log10(rms) if rms > 0 else -100
    print(f"  S09 t = {t_sec:4.1f}s : RMS = {rms:.4f} ({db:5.1f} dB)")

v9.close()
