import os
import subprocess
import sys
import imageio_ffmpeg

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

clips_dir = os.path.join(BASE_DIR, "clips", "cartoon")
audio_bed = os.path.join(BASE_DIR, "audio-refs", "musicgen_mockumentary_score.wav")
output_master = os.path.join(BASE_DIR, "clips", "CARTOON_BUILDING_TRAILER_FULL.mp4")

if not os.path.exists(audio_bed):
    sys.exit(f"Error: Could not find audio file at {audio_bed}")

# Full 26-shot cut per CARTOON_BUILDING_TRAILER_PLAN.md section 3 / 8.
# (filename, trimmed duration in seconds)
SHOTS = [
    ("T01_railway_dusk.mp4", 4.5),
    ("T02_railway_day.mp4", 3.0),
    ("T03_high_aerial.mp4", 5.5),
    ("T04_curved_corner.mp4", 3.5),
    ("T05_prow_crane.mp4", 3.5),
    ("T06_road_trees.mp4", 3.0),
    ("T07_garden_glide.mp4", 3.5),
    ("T08_picnic_arc.mp4", 3.0),
    ("T09_swoop_courtyard.mp4", 3.5),
    ("T10_entrance_approach.mp4", 3.5),
    ("T11_through_doors.mp4", 3.0),
    ("T12_atrium_pan_a.mp4", 3.5),
    ("T13_atrium_pan_b.mp4", 3.5),
    ("T14_orange_pod.mp4", 3.0),
    ("T15_speedgates.mp4", 3.0),
    ("T16_over_balustrade.mp4", 3.5),
    ("T17_gallery_walkway.mp4", 3.0),
    ("T18_desk_run.mp4", 3.5),
    ("T19_work_tables.mp4", 2.5),
    ("T20_corridor.mp4", 2.0),
    ("T21_meeting_room.mp4", 2.5),
    ("T22_canteen.mp4", 2.5),
    ("T23_breakout.mp4", 2.5),
    ("T24_jans_office_orbit.mp4", 4.0),
    ("T25_group_photo.mp4", 3.5),
    ("T26_title_card.mp4", 5.5),
]

# Transition INTO each shot (index 1..25); shot 0 has no incoming transition.
# Straight cuts everywhere except the S11 door whip and the S24->S25 slow fade.
S11_INDEX = 10  # T11_through_doors.mp4
S24_INDEX = 23  # T24_jans_office_orbit.mp4

clip_paths = [os.path.join(clips_dir, name) for name, _ in SHOTS]
durations = [d for _, d in SHOTS]

missing = [p for p in clip_paths if not os.path.exists(p)]
if missing:
    sys.exit(
        "Error: missing clip files, download them from Flow into clips/cartoon/ first:\n"
        + "\n".join(f"  {p}" for p in missing)
    )

TARGET_W, TARGET_H = 1920, 1080
# 2.39:1 letterbox within a 1920x1080 frame
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
    if i + 1 == S11_INDEX:
        trans_type, trans_dur = "hblur", 0.3
    elif i + 1 == S24_INDEX + 1:
        # S24 -> S25 is the plan's "slow fade" beat
        trans_type, trans_dur = "fade", 0.8
    else:
        trans_type, trans_dur = "fade", 0.08

    offset = curr_offset + durations[i] - trans_dur
    curr_offset = offset
    t_offsets.append(offset)
    next_v = f"[v{i+1}_scaled]"
    out_v = f"[v{i+1}_xfade]" if i < len(SHOTS) - 2 else "[vout_raw]"
    filter_graph += f"{last_v}{next_v}xfade=transition={trans_type}:duration={trans_dur}:offset={offset:.2f}{out_v};"
    last_v = out_v

total_duration = t_offsets[-1] + durations[-1]

print(f"Total trailer duration: {total_duration:.2f}s ({len(SHOTS)} shots)")

video_fade_start = max(0.0, total_duration - 1.5)
filter_graph += f"[vout_raw]fade=t=out:st={video_fade_start:.2f}:d=1.5[vout];"

# Music bed: fade in over S01 (reach full by ~2.5s), duck ~3dB under the S11 whip,
# begin the final fade at the head of S26, silent by the end of black.
s11_start = t_offsets[S11_INDEX]
s11_end = s11_start + durations[S11_INDEX]
duck_gain = 0.708  # ~3dB down

vol_expr = (
    f"if(lt(t,2.5), t/2.5, "
    f"if(lt(t,{s11_start:.2f}), 1.0, "
    f"if(lt(t,{s11_end:.2f}), {duck_gain}, 1.0)))"
)

audio_filter = (
    f"[{len(SHOTS)}:a]volume='{vol_expr}':eval=frame,"
    f"atrim=0:{total_duration:.2f},"
    f"afade=t=out:st={video_fade_start:.2f}:d=1.5,"
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

print("\n--- Assembling CARTOON_BUILDING_TRAILER_FULL.mp4 ---")
res = subprocess.run(cmd_master, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

if res.returncode == 0 and os.path.exists(output_master):
    print(f"\n[SUCCESS] Trailer created!")
    print(f"Output File: {output_master} ({os.path.getsize(output_master)/1024/1024:.2f} MB)")
else:
    print(f"\n[ERROR] FFmpeg render error:\n{res.stderr}")
