import os
import subprocess
import imageio_ffmpeg
import numpy as np
from moviepy import VideoFileClip

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
clips_dir = r"C:\ai\Circle the Square\clips"

clips = [
    "OPENING_S01_drone_orbit.mp4",
    "OPENING_S02_KEEPER.mp4",
    "OPENING_S03_KEEPER.mp4",
    "OPENING_S04_jan.mp4",
    "OPENING_S05.mp4",
    "OPENING_S06.mp4",
    "OPENING_S07.mp4",
    "OPENING_S08_trimmed.mp4",
    "OPENING_S09.mp4"
]

print("=== INSPECTING AUDIO OF ALL SOURCE CLIPS ===")
t_acc = 0.0
for i, c in enumerate(clips):
    p = os.path.join(clips_dir, c)
    v_clip = VideoFileClip(p)
    dur = v_clip.duration
    t_start = t_acc
    t_end = t_acc + dur - (0.6 if i < len(clips)-1 else 0.0)
    t_acc = t_end

    has_audio = v_clip.audio is not None
    db = -100
    if has_audio:
        arr = v_clip.audio.to_soundarray(fps=22050)
        rms = np.sqrt(np.mean(arr**2)) if len(arr) > 0 else 0
        db = 20 * np.log10(rms) if rms > 0 else -100
    
    print(f"Shot {i+1:02d} ({c}): Timeline {t_start:5.1f}s -> {t_end:5.1f}s | Duration: {dur:5.2f}s | Audio: {db:5.1f} dB")
    v_clip.close()

print("\nChecking exact audio at t = 55.0s to 70.0s (around 1 minute mark) in OPENING_S08_trimmed & OPENING_S09...")
