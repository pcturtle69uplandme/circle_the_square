import os
import subprocess
import imageio_ffmpeg

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
src_file = r"C:\ai\Circle the Square\clips\OPENING_S08.mp4"
backup_file = r"C:\ai\Circle the Square\clips\OPENING_S08_original_backup.mp4"
trimmed_file = r"C:\ai\Circle the Square\clips\OPENING_S08_trimmed.mp4"
output_overwritten = r"C:\ai\Circle the Square\clips\OPENING_S08.mp4"

# Cut duration: 6.8 seconds (removes tail bit from t=6.8s to t=10.0s where man talks)
TRIM_END_SEC = 6.8

print(f"--- Trimming OPENING_S08.mp4 to 0.0s - {TRIM_END_SEC}s ---")

# Backup original if not already backed up
if not os.path.exists(backup_file):
    import shutil
    shutil.copy(src_file, backup_file)
    print(f"Backed up original file to: {backup_file}")

# FFmpeg lossless stream cut up to 6.8s
cmd = [
    FFMPEG, "-y",
    "-i", backup_file,
    "-t", str(TRIM_END_SEC),
    "-c:v", "libx264",
    "-preset", "fast",
    "-crf", "18",
    "-c:a", "aac",
    trimmed_file
]

res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
if res.returncode == 0 and os.path.exists(trimmed_file):
    print(f"[SUCCESS] Trimmed clip created: {trimmed_file} ({os.path.getsize(trimmed_file)/1024/1024:.2f} MB)")
    import shutil
    shutil.copy(trimmed_file, output_overwritten)
    print(f"[SUCCESS] Updated {output_overwritten} with trimmed version!")
else:
    print(f"[ERROR] FFmpeg trimming failed:\n{res.stderr}")
