import os
import subprocess
import sys
import imageio_ffmpeg

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

clips_dir = os.path.join(BASE_DIR, "clips", "cartoon")
# Music: 2 external tracks from Flow Music (no local LLM)
# Integration 1: track1.mp3  (0.0s -> mid)
# Integration 2: track2.mp3  (mid -> end)
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

# Clips whose native Veo audio fights the score - strip them from the SFX layer
# entirely (picture unaffected). Per user 2026-08-12: T18's audio clashes with
# the music.
MUTE_NATIVE = {
    "T18_desk_run.mp4",
}

# Clips whose native audio should sit further FORWARD in the mix (multiplier on
# top of the base SFX level). Per user 2026-08-12: the birds in T08 were
# inaudible under the score.
NAT_BOOST = {
    "T08_picnic_arc.mp4": 2.5,
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
# Audio: 2 external Flow Music beds (track1 + track2) as the score,
# with each clip's native Veo audio mixed UNDER the music as the SFX/ambience
# layer (air rush on the swoop, door whoosh, gate beeps, office room tone,
# crowd murmur on the group photo). Music ducks ~4dB under the S09 swoop and
# the S11 door transition so those moments read.
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
audio_bed_1 = os.path.join(BASE_DIR, "audio-refs", "track1.mp3")   # Integration 1: 0:00-0:51.5
audio_bed_2 = os.path.join(BASE_DIR, "audio-refs", "track2.mp3")   # Integration 2: 0:51.5-end

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
    f"format=yuv420p"
)

filter_graph = ""
total_duration = 0.0
concat_v_inputs = []
concat_a_inputs = []
shot_starts = {}  # name -> start time in the final cut (for music ducking)

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
    shot_starts[name] = total_duration
    total_duration += dur_clean

    # Video processing with hard cuts.
    # trim/fps rounding drops ~1 frame per segment; over 25 segments that left the
    # picture ~1s ahead of the audio by the end of the cut (broke T25 lip sync).
    # Fix: pad with cloned tail frames then cut to an exact frame count, so every
    # segment is precisely dur_clean long and video/audio boundaries stay locked.
    n_frames = max(1, round(dur_clean * 24))
    filter_graph += (
        f"[{i}:v]trim=start={start_t:.2f}:end={end_t:.2f},setpts=PTS-STARTPTS,"
        f"fps=24,tpad=stop_mode=clone:stop=0.25,trim=end_frame={n_frames},setpts=PTS-STARTPTS,"
        f"{scale_pad}[v{i}_scaled];"
    )
    concat_v_inputs.append(f"[v{i}_scaled]")
    # Native Veo audio: same window as the picture, trimmed and levelled later.
    # Clips in MUTE_NATIVE are silenced here - their audio clashes with the score.
    # Clips in NAT_BOOST get a per-shot gain so quiet ambience reads (T08 birds).
    if name in MUTE_NATIVE:
        nat_vol = 0.0
    else:
        nat_vol = NAT_BOOST.get(name, 1.0)
    filter_graph += f"[{i}:a]atrim=start={start_t:.2f}:end={end_t:.2f},asetpts=PTS-STARTPTS,volume={nat_vol},aresample=48000,aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo[a{i}_nat];"
    concat_a_inputs.append(f"[a{i}_nat]")

concat_inputs = "".join(concat_v_inputs)
filter_graph += f"{concat_inputs}concat=n={len(available_shots)}:v=1:a=0[vout_raw];"
concat_a = "".join(concat_a_inputs)
# SFX/ambience layer: native audio bed, mixed up close under the score.
# Base level 0.55, boosted a further ~1.5x during T25 (group photo) so the crowd
# murmur and shutter sounds carry that shot; gentle fades at head and tail.
nat_fade_out_start = max(0.0, total_duration - 2.0)
t25_start = shot_starts.get("T25_group_photo.mp4", 85.0)
t25_end = t25_start + 8.0
nat_vol_expr = f"0.55*if(between(t,{t25_start:.2f},{t25_end:.2f}),1.5,1)"
filter_graph += (
    f"{concat_a}concat=n={len(available_shots)}:v=0:a=1[nat_raw];"
    f"[nat_raw]volume='{nat_vol_expr}':eval=frame,lowpass=f=6000,afade=t=in:st=0:d=0.5,afade=t=out:st={nat_fade_out_start:.2f}:d=2.0[nat];"
)

print(f"Total trailer duration (~1:40 min target): {total_duration:.2f}s ({len(available_shots)} shots)")

video_fade_start = max(0.0, total_duration - 1.5)
filter_graph += f"[vout_raw]fade=t=out:st={video_fade_start:.2f}:d=1.5[vout];"

# 2 Assembly Integrations setup (ZERO loops):
# Integration 1: track1.mp3  (0.0s -> door transition)
# Integration 2: track2.mp3  (door transition -> end)
# The join sits exactly on the outside->inside flip: the first frame of T12
# (atrium), the moment the camera is through the revolving doors. Two different
# moods, one door - the listener must hear the transition.
m1_idx = len(available_shots)
m2_idx = len(available_shots) + 1
dur_part1 = shot_starts.get("T12_atrium_pan_a.mp4", 40.0)
dur_part2 = max(1.0, total_duration - dur_part1)

# Duck the score ~4dB under the two moments whose native audio must read:
# the S09 courtyard swoop and the S11 revolving-door transition. Plus a gentle
# ~2.5dB dip across the whole T25 group-photo hold so the crowd sits on top.
duck_c1 = shot_starts.get("T09_swoop_courtyard.mp4", 0.0) + 2.0
duck_c2 = shot_starts.get("T11_through_doors.mp4", 0.0) + 1.5
duck_c3 = t25_start + 4.0
duck_expr = (
    f"1 - 0.4*pow(max(0,1-abs(t-{duck_c1:.2f})/1.2),2)"
    f" - 0.4*pow(max(0,1-abs(t-{duck_c2:.2f})/1.2),2)"
    f" - 0.25*pow(max(0,1-abs(t-{duck_c3:.2f})/4.0),2)"
)

filter_graph += (
    f"[{m1_idx}:a]atrim=0:{dur_part1:.2f},asetpts=PTS-STARTPTS,volume='if(lt(t,2.5), t/2.5, 1.0)':eval=frame,afade=t=out:st={(dur_part1-2.0):.2f}:d=2.0,aresample=48000,aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo[m1_norm];"
    f"[{m2_idx}:a]atrim=0:{dur_part2:.2f},asetpts=PTS-STARTPTS,afade=t=in:st=0:d=2.0,afade=t=out:st={(dur_part2-1.5):.2f}:d=1.5,aresample=48000,aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo[m2_norm];"
    f"[m1_norm][m2_norm]concat=n=2:v=0:a=1[mus_raw];"
    f"[mus_raw]volume='{duck_expr}':eval=frame[mus];"
    f"[mus][nat]amix=inputs=2:duration=first:normalize=0:weights='0.6 1',alimiter=limit=0.95:level=disabled,aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo[aout]"
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

