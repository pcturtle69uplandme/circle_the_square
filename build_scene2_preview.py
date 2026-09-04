"""Trim Scene 2's fal.ai clips to their scripted content length and stitch a preview.

fal only offers 5s / 10s / 15s durations, so every clip in fal-tools/browser/
scene2_clips.js is snapped UP to the next allowed value -- 16s of slack across ten
clips. Two things deal with that, and they are complementary:

  1. Each clip's prompt carries an explicit TIMING line telling the model what to hold
     on for the spare seconds, so it does not invent business or dialogue to fill them.
  2. This script trims the tail off afterwards, as the safety net for when it invents
     anyway.

The audio is baked into the video by MiniMax -- there is no separate stem -- so a hard
cut at the trim point would chop room tone mid-flow. Every trim therefore gets a short
audio fade-out, which is why this exists rather than a bare `ffmpeg -t`.

    python build_scene2_preview.py            # trim + stitch
    python build_scene2_preview.py --no-trim  # stitch at full generated length
"""
import json
import os
import subprocess
import sys

import imageio_ffmpeg

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CLIPS_DIR = os.path.join(BASE_DIR, "scene2-clips")
TRIM_DIR = os.path.join(CLIPS_DIR, "trimmed")
OUTPUT = os.path.join(BASE_DIR, "video-tests", "scene2_stitched_preview.mp4")

# (slug, generated clip length, scripted content length). The generated length is what
# fal was asked for; the content length is the beat estimate from VIDEO_BUDGET.md that
# the snap rounded up from. Where they match there is nothing to trim.
CLIPS = [
    ("c01_corridor_gossip",      10, 8),
    ("c02_sharon_exits",          5, 5),
    ("c03_jan_addresses",        15, 13),
    ("c04_shut_up",              15, 15),   # keep the full 3s silence -- it is the joke
    ("c05_rick_questions",       15, 15),
    ("c06_naming_inception",     15, 15),   # keep the full non-reaction beat
    ("c07_inception_exchange",   10, 10),
    ("c08_merch_gag",            15, 14),
    ("c09_groans",               15, 13),
    ("c10_get_back_to_work",     10, 10),   # keep the room emptying -- scene's last shot
]

AUDIO_FADE = 0.4   # seconds of fade before each trim point
TARGET_W, TARGET_H, FPS = 1344, 768, 24   # fal H3 Max native 768p


def run(args):
    p = subprocess.run(args, capture_output=True, text=True)
    if p.returncode != 0:
        sys.exit(f"ffmpeg failed:\n{' '.join(args[:6])}...\n{p.stderr[-1500:]}")


def main():
    do_trim = "--no-trim" not in sys.argv

    missing = [s for s, _, _ in CLIPS if not os.path.exists(os.path.join(CLIPS_DIR, s + ".mp4"))]
    if missing:
        sys.exit("Scene 2 clips not generated yet:\n  " + "\n  ".join(missing))

    os.makedirs(TRIM_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)

    parts, report = [], []
    for slug, generated, content in CLIPS:
        src = os.path.join(CLIPS_DIR, slug + ".mp4")
        keep = content if do_trim else generated

        if keep >= generated:
            parts.append(src)
            report.append((slug, generated, generated, "kept whole"))
            continue

        dst = os.path.join(TRIM_DIR, slug + ".mp4")
        # Re-encode rather than stream-copy: a copy can only cut on a keyframe, which
        # would land the trim up to a second away from where it was asked for.
        run([
            FFMPEG, "-y", "-i", src,
            "-t", str(keep),
            "-af", f"afade=t=out:st={max(0, keep - AUDIO_FADE):.2f}:d={AUDIO_FADE}",
            "-c:v", "libx264", "-preset", "medium", "-crf", "18",
            "-c:a", "aac", "-b:a", "192k",
            "-r", str(FPS), "-pix_fmt", "yuv420p",
            dst,
        ])
        parts.append(dst)
        report.append((slug, generated, keep, f"trimmed -{generated - keep}s"))

    concat_list = os.path.join(TRIM_DIR, "_concat.txt")
    with open(concat_list, "w", encoding="utf-8") as fh:
        for p in parts:
            fh.write(f"file '{p.replace(os.sep, '/')}'\n")

    run([
        FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", concat_list,
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        "-r", str(FPS), "-pix_fmt", "yuv420p",
        OUTPUT,
    ])

    print(f"{'clip':<26} {'gen':>4} {'kept':>5}  note")
    for slug, gen, keep, note in report:
        print(f"{slug:<26} {gen:>3}s {keep:>4}s  {note}")
    total = sum(k for _, _, k, _ in report)
    print(f"\n{'TOTAL':<26} {'':>4} {total:>4}s")
    print(f"written: {OUTPUT}")


if __name__ == "__main__":
    main()
