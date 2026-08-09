import os
import subprocess
import imageio_ffmpeg
import numpy as np
from moviepy import VideoFileClip

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
video_path = r"C:\ai\Circle the Square\clips\OPENING_TRAILER_MASTER.mp4"

clip = VideoFileClip(video_path)
print(f"Master Video Duration: {clip.duration:.2f}s | FPS: {clip.fps}")

if clip.audio is not None:
    audio = clip.audio
    print("\nOutro Audio Level Sampling (t = 28.0s to 35.0s):")
    for t_ms in range(28000, int(clip.duration * 1000), 500):
        t = t_ms / 1000.0
        t_start = max(0, t - 0.25)
        t_end = min(clip.duration - 0.01, t + 0.25)
        sub = audio.subclipped(t_start, t_end)
        arr = sub.to_soundarray(fps=22050)
        rms = np.sqrt(np.mean(arr**2)) if len(arr) > 0 else 0
        db = 20 * np.log10(rms) if rms > 0 else -100
        status = "SILENT / CUT OFF!" if db < -45.0 else f"AUDIO PLAYING ({db:5.1f} dB)"
        print(f"  t = {t:4.1f}s : RMS = {rms:.4f} ({db:5.1f} dB) -> {status}")

clip.close()
