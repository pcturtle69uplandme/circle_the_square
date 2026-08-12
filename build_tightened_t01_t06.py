import os
import subprocess
import sys
import imageio_ffmpeg

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

clips_dir = os.path.join(BASE_DIR, "clips", "cartoon")
audio_bed = os.path.join(BASE_DIR, "audio-refs", "musicgen_mockumentary_score.wav")
output_master = os.path.join(BASE_DIR, "clips", "CARTOON_BUILDING_TRAILER_TIGHTENED_T01_T06.mp4")

# Director's Cut Tightened Timings for Shots T01-T06
SHOTS = [
    ("T01_railway_dusk.mp4", 4.5),   # Cold open dusk track
    ("T02_railway_day.mp4", 2.5),    # Tightened time-jump (2.5s vs 3.0s)
    ("T03_high_aerial.mp4", 6.0),    # Extended orbit (6.0s vs 5.5s) for music swell
    ("T04_curved_corner.mp4", 3.5),  # Push-in on curved corner
    ("T05_prow_crane.mp4", 3.5),    # Rising crane up prow
    ("T06_road_trees.mp4", 3.0),    # Lateral drift past trees
]

clip_paths = [os.path.join(clips_dir, name) for name, _ in SHOTS]
durations = [dur for _, dur in SHOTS]

missing = [p for p in clip_paths if not os.path.exists(p)]
if missing:
    sys.exit("Missing required clip files:\n" + "\n".join(missing))

TARGET_W, TARGET_H = 1920, 1080
LB_H = int(round(TARGET_W / 2.39))
PAD_Y = (TARGET_H - LB_H) // 2

scale_pad = (
    f"trim=0:{{dur:.2f}},setpts=PTS-STARTPTS,"
    f"scale={TARGET_W}:{LB_H}:force_original_aspect_ratio=increase,"
    f"crop={TARGET_W}:{LB_H},"
    f"pad={TARGET_W}:{TARGET_H}:0:{PAD_Y}:black,"
    f"fps=24,format=yuv420p"
)

filter_graph = ""
for i, dur in enumerate(durations):
    filter_graph += f"[{i}:v]{scale_pad.format(dur=dur)}[v{i}_scaled];"

last_v = "[v0_scaled]"
curr_offset = 0.0
t_offsets = [0.0]

for i in range(len(SHOTS) - 1):
    trans_type, trans_dur = "fade", 0.08
    offset = curr_offset + durations[i] - trans_dur
    curr_offset = offset
    t_offsets.append(offset)
    next_v = f"[v{i+1}_scaled]"
    out_v = f"[v{i+1}_xfade]" if i < len(SHOTS) - 2 else "[vout_raw]"
    filter_graph += f"{last_v}{next_v}xfade=transition={trans_type}:duration={trans_dur}:offset={offset:.2f}{out_v};"
    last_v = out_v

total_duration = t_offsets[-1] + durations[-1]
video_fade_start = max(0.0, total_duration - 1.0)
filter_graph += f"[vout_raw]fade=t=out:st={video_fade_start:.2f}:d=1.0[vout];"

# Audio bed with cold open atmosphere: fade in music at t=1.5s
vol_expr = (
    f"if(lt(t,1.5), 0.0, "
    f"if(lt(t,3.0), (t-1.5)/1.5, 1.0))"
)

audio_filter = (
    f"[{len(SHOTS)}:a]volume='{vol_expr}':eval=frame,"
    f"atrim=0:{total_duration:.2f},"
    f"afade=t=out:st={video_fade_start:.2f}:d=1.0,"
    f"aresample=48000[aout]"
)

full_filter = filter_graph + audio_filter

cmd_master = [FFMPEG, "-y"]
for p in clip_paths:
    cmd_master.extend(["-i", p])
cmd_master.extend(["-stream_loop", "-1", "-i", audio_bed])

cmd_master.extend([
    "-filter_complex", full_filter,
    "-map", "[vout]",
    "-map", "[aout]",
    "-c:v", "libx264",
    "-profile:v", "main",
    "-level", "4.1",
    "-pix_fmt", "yuv420p",
    "-preset", "medium",
    "-crf", "18",
    "-c:a", "aac",
    "-ar", "48000",
    "-ac", "2",
    "-b:a", "192k",
    "-movflags", "+faststart",
    "-t", f"{total_duration:.2f}",
    output_master
])

print(f"\n--- Rendering Director's Cut: {os.path.basename(output_master)} ({total_duration:.2f}s) ---")
res = subprocess.run(cmd_master, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

if res.returncode == 0 and os.path.exists(output_master):
    print(f"[SUCCESS] Director's Cut created!")
    print(f"Output File: {output_master} ({os.path.getsize(output_master)/1024/1024:.2f} MB)")
else:
    print(f"[ERROR] FFmpeg render error:\n{res.stderr}")
