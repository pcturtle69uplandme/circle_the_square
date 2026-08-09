import os
import subprocess
import imageio_ffmpeg

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

title_img = r"C:\ai\Circle the Square\images\circle the square.jpeg"
clips_dir = r"C:\ai\Circle the Square\clips"
ai_music_audio = r"C:\ai\Circle the Square\audio-refs\ai_musicgen_soundtrack.wav"
zone_sfx_audio = r"C:\ai\Circle the Square\audio-refs\zone_ambient_sfx.wav"
output_master = r"C:\ai\Circle the Square\clips\OPENING_TRAILER_MASTER.mp4"

opening_s01 = os.path.join(clips_dir, "OPENING_S01_drone_orbit.mp4")
opening_s02 = os.path.join(clips_dir, "OPENING_S02_KEEPER.mp4")
opening_s03 = os.path.join(clips_dir, "OPENING_S03_KEEPER.mp4")
opening_s04 = os.path.join(clips_dir, "OPENING_S04_jan.mp4")

# 1. Generate 5s Closing Title Card Video with black fade out
title_video_end = os.path.join(clips_dir, "temp_title_end_5s.mp4")
cmd_title_end = [
    FFMPEG, "-y",
    "-loop", "1",
    "-i", title_img,
    "-t", "5.0",
    "-vf", "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,format=yuv420p",
    "-c:v", "libx264",
    "-profile:v", "main",
    "-level", "4.0",
    "-pix_fmt", "yuv420p",
    "-r", "24",
    title_video_end
]
print("Creating 5s Closing Title Card video...")
subprocess.run(cmd_title_end, check=True)

clip_list = [
    opening_s01,
    opening_s02,
    opening_s03,
    opening_s04,
    title_video_end
]

wipes = ["wipeleft", "wiperight", "circlecrop", "fade"]
trans_duration = 0.8

def get_duration(p):
    cmd = [FFMPEG, "-i", p]
    res = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    for line in res.stderr.splitlines():
        if "Duration:" in line:
            parts = line.split("Duration:")[1].split(",")[0].strip().split(":")
            return float(parts[0])*3600 + float(parts[1])*60 + float(parts[2])
    return 5.0

durations = [get_duration(p) for p in clip_list]
print(f"Clip durations: {[round(d, 2) for d in durations]}")

filter_graph = ""

for i in range(len(clip_list)):
    filter_graph += f"[{i}:v]scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,fps=24,format=yuv420p[v{i}_scaled];"

last_v = "[v0_scaled]"
curr_offset = 0.0

for i in range(len(clip_list) - 1):
    offset = curr_offset + durations[i] - trans_duration
    curr_offset = offset
    next_v = f"[v{i+1}_scaled]"
    out_v = f"[v{i+1}_xfade]" if i < len(clip_list) - 2 else "[vout_raw]"
    w_type = wipes[i % len(wipes)]
    filter_graph += f"{last_v}{next_v}xfade=transition={w_type}:duration={trans_duration}:offset={offset:.2f}{out_v};"
    last_v = out_v

total_duration = curr_offset + durations[-1] - trans_duration

jan_start_sec = (durations[0] - trans_duration) + (durations[1] - trans_duration) + (durations[2] - trans_duration)
jan_delay_ms = int(jan_start_sec * 1000)

fade_out_start = max(0.0, total_duration - 1.5)

# Video fade to black at the end
filter_graph += f"[vout_raw]fade=t=out:st={fade_out_start:.2f}:d=1.5[vout];"

# FIX FOR ABRUPT AUDIO OUTRO:
# Put bg_music as input 0 in amix with duration=longest, and pad jan_voice to total_duration
# Input 3: S04_jan.mp4 -> Jan's voice (delayed to t=21.6s)
# Input 5: ai_musicgen_soundtrack.wav -> Meta MusicGen AI Track
# Input 6: zone_ambient_sfx.wav -> Hiss-free Zone SFX

audio_filter = (
    f"[3:a]volume=1.8,adelay={jan_delay_ms}|{jan_delay_ms},apad=whole_dur={total_duration:.2f},aresample=48000[jan_voice];"
    f"[5:a]volume=0.45,atrim=0:{total_duration:.2f},aresample=48000[bg_music];"
    f"[6:a]volume=0.35,apad=whole_dur={total_duration:.2f},aresample=48000[zone_sfx];"
    f"[bg_music][jan_voice][zone_sfx]amix=inputs=3:duration=longest:dropout_transition=0,afade=t=out:st={fade_out_start:.2f}:d=1.5,aresample=48000[aout]"
)

full_filter = filter_graph + audio_filter

cmd_master = [FFMPEG, "-y"]
for p in clip_list:
    cmd_master.extend(["-i", p])
cmd_master.extend(["-i", ai_music_audio])
cmd_master.extend(["-i", zone_sfx_audio])

cmd_master.extend([
    "-filter_complex", full_filter,
    "-map", "[vout]",
    "-map", "[aout]",
    "-c:v", "libx264",
    "-profile:v", "main",
    "-level", "4.0",
    "-pix_fmt", "yuv420p",
    "-preset", "medium",
    "-crf", "20",
    "-c:a", "aac",
    "-ar", "48000",
    "-ac", "2",
    "-b:a", "192k",
    "-movflags", "+faststart",
    "-t", f"{total_duration:.2f}",
    output_master
])

print(f"\n--- Assembling Perfect Outro Audio Sync Master Trailer (Audio Fade Out at {fade_out_start:.2f}s) ---")
res = subprocess.run(cmd_master, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

if res.returncode == 0 and os.path.exists(output_master):
    print(f"\n[SUCCESS] Master Video Trailer with seamless audio outro created successfully!")
    print(f"Output File: {output_master} ({os.path.getsize(output_master)/1024/1024:.2f} MB)")
else:
    print(f"\n[ERROR] FFmpeg master render error:\n{res.stderr}")
