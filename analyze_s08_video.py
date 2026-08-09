import os
import subprocess
import sys
import imageio_ffmpeg

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
video_path = r"C:\ai\Circle the Square\clips\OPENING_S08.mp4"
frames_dir = r"C:\ai\Circle the Square\frames\s08_analysis"
os.makedirs(frames_dir, exist_ok=True)

print(f"--- Analyzing {video_path} ---")

# 1. Get Duration & Stream Info
cmd_info = [FFMPEG, "-i", video_path]
res_info = subprocess.run(cmd_info, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)

duration = 0.0
fps = 24.0

for line in res_info.stderr.splitlines():
    if "Duration:" in line:
        parts = line.split("Duration:")[1].split(",")[0].strip().split(":")
        duration = float(parts[0])*3600 + float(parts[1])*60 + float(parts[2])
    if "fps" in line:
        for item in line.split(","):
            if "fps" in item:
                try:
                    fps = float(item.strip().split()[0])
                except Exception:
                    pass

print(f"Video Duration: {duration:.2f} seconds | FPS: {fps}")

# 2. Extract frames every 0.25 seconds in the last 3 seconds of the clip
print(f"Extracting tail frames from t = {max(0, duration - 3.0):.2f}s to {duration:.2f}s...")
cmd_frames = [
    FFMPEG, "-y",
    "-ss", str(max(0, duration - 3.5)),
    "-i", video_path,
    "-vf", "fps=5,scale=640:-1",
    os.path.join(frames_dir, "frame_%03d.jpg")
]
subprocess.run(cmd_frames, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

extracted = os.listdir(frames_dir)
print(f"Extracted {len(extracted)} diagnostic tail frames to: {frames_dir}")

# 3. Audio Volume / Speech Analysis via silencedetect / astats
cmd_audio = [
    FFMPEG, "-i", video_path,
    "-af", "astats=metadata=1:reset=1,ametadata=print:key=lavfi.astats.Overall.RMS_level",
    "-f", "null", "-"
]
res_audio = subprocess.run(cmd_audio, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)

rms_levels = []
for line in res_audio.stderr.splitlines():
    if "RMS_level" in line:
        rms_levels.append(line.strip())

print(f"Audio RMS Level samples found: {len(rms_levels)}")
if rms_levels:
    print("Tail end audio RMS levels:")
    for l in rms_levels[-10:]:
        print(" ", l)
