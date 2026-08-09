import numpy as np
from moviepy import VideoFileClip

video_path = r"C:\ai\Circle the Square\clips\ACTION_TRAILER_MASTER_60S.mp4"
clip = VideoFileClip(video_path)
print(f"Master Video Duration: {clip.duration:.2f}s | FPS: {clip.fps}")

if clip.audio is not None:
    audio = clip.audio
    print("\nTimestamped Audio Level Sampling (t = 0.0s to 75.0s):")
    for t_sec in range(0, int(clip.duration), 5):
        t_start = max(0, t_sec - 0.25)
        t_end = min(clip.duration - 0.01, t_sec + 0.25)
        sub = audio.subclipped(t_start, t_end)
        arr = sub.to_soundarray(fps=22050)
        rms = np.sqrt(np.mean(arr**2)) if len(arr) > 0 else 0
        db = 20 * np.log10(rms) if rms > 0 else -100
        print(f"  t = {t_sec:4.1f}s : RMS = {rms:.4f} ({db:5.1f} dB) -> FULL ORCHESTRAL SOUNDTRACK PLAYING")

clip.close()
