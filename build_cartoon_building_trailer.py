import os
import subprocess
import sys
import imageio_ffmpeg

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

clips_dir = os.path.join(BASE_DIR, "clips", "cartoon")
# Music: 2 external tracks from Flow Music (no local LLM)
# Integration 1: Small Stakes.mp3  (0.0s -> mid)
# Integration 2: The Paper Trail.mp3 (mid -> end)
output_master = os.path.join(BASE_DIR, "clips", "CARTOON_BUILDING_TRAILER_2X_FLOW_MUSIC.mp4")

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
# 25-shot cut (~1:40 min total runtime / 100.0s).
# T25 (Group Photo) is kept 100% full length (8.0s).
# All clip sound effects/audio REMOVED per user request.
# Driven 100% by regenerated theme tune score.
SHOTS = [
    ("T01_railway_dusk.mp4", 4.5),
    ("T02_railway_day.mp4", 3.5),
    ("T03_high_aerial.mp4", 5.5),
    ("T05_prow_crane.mp4", 4.0),
    ("T06_road_trees.mp4", 3.5),
    ("T07_garden_glide.mp4", 4.0),
    ("T08_picnic_arc.mp4", 3.5),
    ("T09_swoop_courtyard.mp4", 4.0),
    ("T10_entrance_approach.mp4", 4.0),
    ("T11_through_doors.mp4", 3.5),
    ("T12_atrium_pan_a.mp4", 4.0),
    ("T13_atrium_pan_b.mp4", 3.5),
    ("T14_orange_pod.mp4", 3.5),
    ("T15_speedgates.mp4", 3.5),
    ("T16_over_balustrade.mp4", 3.5),
    ("T17_gallery_walkway.mp4", 3.5),
    ("T18_desk_run.mp4", 4.0),
    ("T19_work_tables.mp4", 3.0),
    ("T20_corridor.mp4", 3.0),
    ("T21_meeting_room.mp4", 3.0),
    ("T22_canteen.mp4", 3.0),
    ("T23_breakout.mp4", 3.0),
    ("T24_jans_office_orbit.mp4", 4.5),
    ("T25_group_photo.mp4", 8.0),  # 100% FULL UNTRIMMED — Group photo shoot
    ("T26_title_card.mp4", 5.5),
]

# External Flow Music tracks — no local model inference
audio_bed_1 = os.path.join(BASE_DIR, "audio-refs", "Small Stakes.mp3")       # Integration 1
audio_bed_2 = os.path.join(BASE_DIR, "audio-refs", "The Paper Trail.mp3")    # Integration 2

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
    print(f"--- Full ~1:40 Master Render (2 Assembly Integrations, Zero Loops) ---")

clip_paths = [p for _, _, p in available_shots]

TARGET_W, TARGET_H = 1920, 1080
# Full 16:9 scale/pad without widescreen 2.39:1 crop
scale_pad = (
    f"scale={TARGET_W}:{TARGET_H}:force_original_aspect_ratio=decrease,"
    f"pad={TARGET_W}:{TARGET_H}:(ow-iw)/2:(oh-ih)/2:black,"
    f"fps=24,format=yuv420p"
)

filter_graph = ""
total_duration = 0.0
concat_v_inputs = []

for i, (name, dur, path) in enumerate(available_shots):
    clip_len = probe_duration(path)
    # T25 (Group Photo) is kept 100% full length; other clips trim drift off the end
    if name == "T25_group_photo.mp4":
        start_t = 0.0
        dur_clean = clip_len
    else:
        start_t = 0.20 if clip_len > 1.0 else 0.0
        dur_clean = min(dur, max(0.5, clip_len - start_t))
    
    end_t = start_t + dur_clean
    total_duration += dur_clean
    
    # Video processing with hard cuts
    filter_graph += f"[{i}:v]trim=start={start_t:.2f}:end={end_t:.2f},setpts=PTS-STARTPTS,{scale_pad}[v{i}_scaled];"
    concat_v_inputs.append(f"[v{i}_scaled]")

concat_inputs = "".join(concat_v_inputs)
filter_graph += f"{concat_inputs}concat=n={len(available_shots)}:v=1:a=0[vout_raw];"

print(f"Total trailer duration (~1:40 min target): {total_duration:.2f}s ({len(available_shots)} shots)")

video_fade_start = max(0.0, total_duration - 1.5)
filter_graph += f"[vout_raw]fade=t=out:st={video_fade_start:.2f}:d=1.5[vout];"

# 2 Assembly Integrations setup (ZERO loops):
# Integration 1: constant_unified_action_theme.wav (Part 1, 0.0s -> 51.5s)
# Integration 2: musicgen_large_neural_score.wav (Part 2, 51.5s -> 98.5s)
m1_idx = len(available_shots)
m2_idx = len(available_shots) + 1
dur_part1 = 51.5
dur_part2 = max(1.0, total_duration - dur_part1)

filter_graph += (
    f"[{m1_idx}:a]atrim=0:{dur_part1:.2f},asetpts=PTS-STARTPTS,volume='if(lt(t,2.5), t/2.5, 1.0)':eval=frame,afade=t=out:st={(dur_part1-2.0):.2f}:d=2.0,aresample=48000,aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo[m1_norm];"
    f"[{m2_idx}:a]atrim=0:{dur_part2:.2f},asetpts=PTS-STARTPTS,afade=t=in:st=0:d=2.0,afade=t=out:st={(dur_part2-1.5):.2f}:d=1.5,aresample=48000,aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo[m2_norm];"
    f"[m1_norm][m2_norm]concat=n=2:v=0:a=1[aout]"
)

full_filter = filter_graph

cmd_master = [FFMPEG, "-y"]
for _, _, p in available_shots:
    cmd_master.extend(["-i", p])
cmd_master.extend(["-i", audio_bed_1, "-i", audio_bed_2])

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

