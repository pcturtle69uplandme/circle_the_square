import os
import subprocess
import imageio_ffmpeg

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

title_img = r"C:\ai\Circle the Square\images\circle the square.jpeg"
clips_dir = r"C:\ai\Circle the Square\clips"
unified_theme = r"C:\ai\Circle the Square\audio-refs\constant_unified_action_theme.wav"
output_master = r"C:\ai\Circle the Square\clips\ACTION_TRAILER_MASTER_60S.mp4"

s01 = os.path.join(clips_dir, "OPENING_S01_drone_orbit.mp4")
s02 = os.path.join(clips_dir, "OPENING_S02_KEEPER.mp4")
s03 = os.path.join(clips_dir, "OPENING_S03_KEEPER.mp4")
s04 = os.path.join(clips_dir, "OPENING_S04_jan.mp4")
s05 = os.path.join(clips_dir, "OPENING_S05.mp4")
s06 = os.path.join(clips_dir, "OPENING_S06.mp4")
s07 = os.path.join(clips_dir, "OPENING_S07.mp4")
s08 = os.path.join(clips_dir, "OPENING_S08.mp4") # Untrimmed S08 with full original voice
s09 = os.path.join(clips_dir, "OPENING_S09.mp4") # S09 with confrontation voice

# 1. Generate Title Card Video with TOP OF SCREEN Text Overlay & Black Fade Out
title_video_end = os.path.join(clips_dir, "temp_action_title_end_5s.mp4")
cmd_title_end = [
    FFMPEG, "-y",
    "-loop", "1",
    "-i", title_img,
    "-t", "5.0",
    "-vf", (
        "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,format=yuv420p,"
        "drawtext=text='THIS AUTUMN - THERE IS NO ESCAPE':fontcolor=white:fontsize=36:x=(w-text_w)/2:y=60:box=1:boxcolor=black@0.6:boxborderw=10,"
        "fade=t=out:st=3.5:d=1.5"
    ),
    "-c:v", "libx264",
    "-profile:v", "main",
    "-level", "4.0",
    "-pix_fmt", "yuv420p",
    "-r", "24",
    title_video_end
]
print("Creating Action Title Card video with TOP OF SCREEN text overlay...")
subprocess.run(cmd_title_end, check=True)

clip_list = [s01, s02, s03, s04, s05, s06, s07, s08, s09, title_video_end]
wipes = ["fade", "wipeleft", "wiperight", "circlecrop", "slideleft", "slideright", "diagtl", "fade", "fade"]
trans_duration = 0.6

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

# Stream 0 (S01): Draw overlay text AT TOP OF SCREEN (y=60)
filter_graph += f"[0:v]scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,fps=24,format=yuv420p,drawtext=text='EVERY CORPORATION HAS A SECRET...':fontcolor=white:fontsize=36:x=(w-text_w)/2:y=60:box=1:boxcolor=black@0.6:boxborderw=10[v0_scaled];"

# Stream 1 (S02): Draw overlay text AT TOP OF SCREEN (y=60)
filter_graph += f"[1:v]scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,fps=24,format=yuv420p,drawtext=text='EVERY BOARDROOM HAS A PRICE.':fontcolor=white:fontsize=36:x=(w-text_w)/2:y=60:box=1:boxcolor=black@0.6:boxborderw=10[v1_scaled];"

# Remaining video streams
for i in range(2, len(clip_list)):
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
print(f"Total Action Trailer Duration: {total_duration:.2f} seconds")

# Calculate exact start timestamps for ALL dialogue soundbites:
t_offsets = [0.0]
for i in range(len(clip_list) - 1):
    t_offsets.append(t_offsets[-1] + durations[i] - trans_duration)

ms_s04 = int(t_offsets[3] * 1000)
ms_s05 = int(t_offsets[4] * 1000)
ms_s06 = int(t_offsets[5] * 1000)
ms_s07 = int(t_offsets[6] * 1000)
ms_s08 = int(t_offsets[7] * 1000)
ms_s09 = int(t_offsets[8] * 1000)

fade_out_start = max(0.0, total_duration - 1.5)
filter_graph += f"[vout_raw]fade=t=out:st={fade_out_start:.2f}:d=1.5[vout];"

# TWO-STAGE AUDIO MIX:
# Mix ALL 6 dialogue streams (S04, S05, S06, S07, S08, S09) with volume=3.0 boost -> [dialogue_mix]
# Mix 85s Constant Unified Theme [bg_theme] + [dialogue_mix] with weights=1.2 2.8
audio_filter = (
    f"[3:a]volume=3.0,adelay={ms_s04}|{ms_s04},apad=whole_dur={total_duration:.2f},aresample=48000[a_s04];"
    f"[4:a]volume=3.0,adelay={ms_s05}|{ms_s05},apad=whole_dur={total_duration:.2f},aresample=48000[a_s05];"
    f"[5:a]volume=3.0,adelay={ms_s06}|{ms_s06},apad=whole_dur={total_duration:.2f},aresample=48000[a_s06];"
    f"[6:a]volume=3.0,adelay={ms_s07}|{ms_s07},apad=whole_dur={total_duration:.2f},aresample=48000[a_s07];"
    f"[7:a]volume=3.0,adelay={ms_s08}|{ms_s08},apad=whole_dur={total_duration:.2f},aresample=48000[a_s08];"
    f"[8:a]volume=3.0,adelay={ms_s09}|{ms_s09},apad=whole_dur={total_duration:.2f},aresample=48000[a_s09];"
    f"[a_s04][a_s05][a_s06][a_s07][a_s08][a_s09]amix=inputs=6:duration=longest:dropout_transition=0[dialogue_mix];"
    f"[10:a]volume=0.95,atrim=0:{total_duration:.2f},aresample=48000[bg_theme];"
    f"[bg_theme][dialogue_mix]amix=inputs=2:weights=1.2 2.8:duration=longest:dropout_transition=0,afade=t=out:st={fade_out_start:.2f}:d=1.5,aresample=48000[aout]"
)

full_filter = filter_graph + audio_filter

cmd_master = [FFMPEG, "-y"]
for p in clip_list:
    cmd_master.extend(["-i", p])
cmd_master.extend(["-i", unified_theme])

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

print(f"\n--- Assembling Constant Unified Action Theme Master Trailer (Fade Out at {fade_out_start:.2f}s) ---")
res = subprocess.run(cmd_master, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

if res.returncode == 0 and os.path.exists(output_master):
    print(f"\n[SUCCESS] Master Action Trailer with Constant Unified Theme created successfully!")
    print(f"Output File: {output_master} ({os.path.getsize(output_master)/1024/1024:.2f} MB)")
else:
    print(f"\n[ERROR] FFmpeg master action trailer render error:\n{res.stderr}")
