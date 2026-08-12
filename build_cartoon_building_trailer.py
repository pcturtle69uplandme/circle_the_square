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

# --- Veo drift guard ---------------------------------------------------------
# Veo holds the source plate for the first few seconds, then starts inventing:
# new rooms appear beyond doorways, desks and furniture that were never in the
# building fill the far end of the frame, walls move. The further a clip gets
# from its first frame, the less it looks like The Triangle. So the tail of
# every 8s render is the least trustworthy part of it and we never cut from it.
#
# Usable window for each clip = [HEAD_SKIP, clip_length - drift_drop].
# Interiors drift fastest — a corridor or an office invents a whole new room in
# the time an aerial only drifts a little — so they give up more of their tail.
HEAD_SKIP = 0.2           # skip the first-frame settle / any morph on frame 1
DRIFT_DROP_DEFAULT = 2.0  # exteriors: never use the last 2.0s
DRIFT_DROP_TIGHT = 3.0    # interiors and tight shots: never use the last 3.0s
DRIFT_DROP_NONE = 0.2     # eye-checked clips: only the final settle comes off

# Clips whose endings were watched and found still on-model - the move arrives
# somewhere the building really goes, nothing invented. These keep their tails
# and ignore the drop above. Only add a shot here after actually watching it.
KEEP_TAIL = {
    "T15_speedgates.mp4",  # ends in the lift lobby, which is where it was heading
}

# Shots that sit inside the building or push in close. These get the 3s drop.
TIGHT_SHOTS = {
    "T11_through_doors.mp4",
    "T12_atrium_pan_a.mp4",
    "T13_atrium_pan_b.mp4",
    "T14_orange_pod.mp4",
    "T15_speedgates.mp4",
    "T16_over_balustrade.mp4",
    "T17_gallery_walkway.mp4",
    "T18_desk_run.mp4",
    "T19_work_tables.mp4",
    "T20_corridor.mp4",
    "T21_meeting_room.mp4",
    "T22_canteen.mp4",
    "T23_breakout.mp4",
    "T24_jans_office_orbit.mp4",
    "T25_group_photo.mp4",
}


def probe_duration(path, default=8.0):
    """Length of a clip in seconds; falls back to the Veo default of 8s."""
    try:
        res = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", path],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=20,
        )
        return float(res.stdout.strip())
    except Exception:
        return default


def usable_window(path, name):
    """(start, max_usable_duration) inside a clip, with the drift tail cut off."""
    if name in KEEP_TAIL:
        drop = DRIFT_DROP_NONE
    else:
        drop = DRIFT_DROP_TIGHT if name in TIGHT_SHOTS else DRIFT_DROP_DEFAULT
    length = probe_duration(path)
    end = max(HEAD_SKIP + 0.5, length - drop)
    return HEAD_SKIP, end - HEAD_SKIP


# 25-shot cut (T04 removed per user request).
# (filename, trimmed duration in seconds)
SHOTS = [
    ("T01_railway_dusk.mp4", 4.5),
    ("T02_railway_day.mp4", 2.5),
    ("T03_high_aerial.mp4", 6.0),
    ("T05_prow_crane.mp4", 3.5),
    ("T06_road_trees.mp4", 3.0),
    ("T07_garden_glide.mp4", 3.5),
    ("T08_picnic_arc.mp4", 3.0),
    ("T09_swoop_courtyard.mp4", 3.5),
    ("T10_entrance_approach.mp4", 3.5),
    ("T11_through_doors.mp4", 3.0),
    ("T12_atrium_pan_a.mp4", 3.5),
    # 3.0s not 3.5s: an invented green landscape appears through the glazing from
    # ~4.5s, so this shot stops well clear of it. Do not lengthen without rechecking.
    ("T13_atrium_pan_b.mp4", 3.0),
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

# Find available contiguous clips
available_shots = []
for name, dur in SHOTS:
    p = os.path.join(clips_dir, name)
    if os.path.exists(p):
        available_shots.append((name, dur, p))
    else:
        break

if not available_shots:
    sys.exit(
        f"Error: no clip files found in {clips_dir}.\n"
        "Download clips from Google Flow first (e.g. T01_railway_dusk.mp4)."
    )

is_full_cut = len(available_shots) == len(SHOTS)
out_target = output_master if is_full_cut else os.path.join(BASE_DIR, "clips", f"CARTOON_BUILDING_TRAILER_PREVIEW_{len(available_shots)}SHOTS.mp4")

if not is_full_cut:
    print(f"--- Partial Build Mode: Rendering {len(available_shots)} of {len(SHOTS)} clips ---")
    missing_name = SHOTS[len(available_shots)][0]
    print(f"    (Stopped at missing clip #{len(available_shots)+1}: {missing_name})\n")
else:
    print(f"--- Full 26-Shot Master Render ---")

clip_paths = [p for _, _, p in available_shots]

# Apply the drift guard: source every shot from the head of its clip and clamp
# any shot that asks for more than its trustworthy window can give.
src_starts = []
durations = []
for name, dur, path in available_shots:
    start, max_dur = usable_window(path, name)
    src_starts.append(start)
    if dur > max_dur:
        print(
            f"    [drift guard] {name}: {dur:.2f}s requested, only {max_dur:.2f}s "
            f"is clean - trimming to {max_dur:.2f}s."
        )
        dur = max_dur
    durations.append(dur)

active_shots = [(name, dur) for (name, _, _), dur in zip(available_shots, durations)]


TARGET_W, TARGET_H = 1920, 1080
# 2.39:1 letterbox within a 1920x1080 frame
LB_H = int(round(TARGET_W / 2.39))
PAD_Y = (TARGET_H - LB_H) // 2

scale_pad = (
    f"trim={{start:.2f}}:{{end:.2f}},setpts=PTS-STARTPTS,"
    f"scale={TARGET_W}:{LB_H}:force_original_aspect_ratio=increase,"
    f"crop={TARGET_W}:{LB_H},"
    f"pad={TARGET_W}:{TARGET_H}:0:{PAD_Y}:black,"
    f"fps=24,format=yuv420p"
)

filter_graph = ""
for i, dur in enumerate(durations):
    start = src_starts[i]
    filter_graph += f"[{i}:v]{scale_pad.format(start=start, end=start + dur)}[v{i}_scaled];"

last_v = "[v0_scaled]"
curr_offset = 0.0
t_offsets = [0.0]

for i in range(len(active_shots) - 1):
    if i + 1 == S11_INDEX and len(active_shots) > S11_INDEX:
        trans_type, trans_dur = "hblur", 0.3
    elif i + 1 == S24_INDEX + 1 and len(active_shots) > S24_INDEX:
        # S24 -> S25 is the plan's "slow fade" beat
        trans_type, trans_dur = "fade", 0.8
    else:
        trans_type, trans_dur = "fade", 0.08

    offset = curr_offset + durations[i] - trans_dur
    curr_offset = offset
    t_offsets.append(offset)
    next_v = f"[v{i+1}_scaled]"
    out_v = f"[v{i+1}_xfade]" if i < len(active_shots) - 2 else "[vout_raw]"
    filter_graph += f"{last_v}{next_v}xfade=transition={trans_type}:duration={trans_dur}:offset={offset:.2f}{out_v};"
    last_v = out_v

total_duration = t_offsets[-1] + durations[-1]

print(f"Total trailer duration: {total_duration:.2f}s ({len(active_shots)} shots)")

video_fade_start = max(0.0, total_duration - 1.5)
filter_graph += f"[vout_raw]fade=t=out:st={video_fade_start:.2f}:d=1.5[vout];"

# Music bed: fade in over S01 (reach full by ~2.5s), duck ~3dB under the S11 whip,
# begin the final fade at the head of S26, silent by the end of black.
s11_start = t_offsets[min(S11_INDEX, len(active_shots) - 1)]
s11_end = s11_start + durations[min(S11_INDEX, len(active_shots) - 1)]
duck_gain = 0.708  # ~3dB down

vol_expr = (
    f"if(lt(t,2.5), t/2.5, "
    f"if(lt(t,{s11_start:.2f}), 1.0, "
    f"if(lt(t,{s11_end:.2f}), {duck_gain}, 1.0)))"
)

audio_filter = (
    f"[{len(active_shots)}:a]volume='{vol_expr}':eval=frame,"
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
    out_target
])

print(f"\n--- Assembling {os.path.basename(out_target)} ---")
res = subprocess.run(cmd_master, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

if res.returncode == 0 and os.path.exists(out_target):
    print(f"\n[SUCCESS] Trailer created!")
    print(f"Output File: {out_target} ({os.path.getsize(out_target)/1024/1024:.2f} MB)")
else:
    print(f"\n[ERROR] FFmpeg render error:\n{res.stderr}")

