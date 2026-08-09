import os
import subprocess
import imageio_ffmpeg
import numpy as np
from moviepy import VideoFileClip

video_path = r"C:\ai\Circle the Square\clips\OPENING_S08.mp4"

clip = VideoFileClip(video_path)
print(f"Clip Duration: {clip.duration:.2f}s | FPS: {clip.fps} | Size: {clip.size}")

if clip.audio is not None:
    audio = clip.audio
    print("\nDetailed 0.5s Step Audio & Speech Analysis:")
    for t_ms in range(0, int(clip.duration * 1000), 500):
        t = t_ms / 1000.0
        t_start = max(0, t - 0.25)
        t_end = min(clip.duration - 0.01, t + 0.25)
        sub = audio.subclipped(t_start, t_end)
        arr = sub.to_soundarray(fps=22050)
        rms = np.sqrt(np.mean(arr**2)) if len(arr) > 0 else 0
        db = 20 * np.log10(rms) if rms > 0 else -100
        speech_flag = "[SPEECH/TALKING]" if db > -22.0 else "[AMBIENT/QUIET]"
        print(f"  t = {t:4.1f}s : RMS = {rms:.4f} ({db:5.1f} dB) -> {speech_flag}")

clip.close()
