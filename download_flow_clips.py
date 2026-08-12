"""Download Google Flow video clips to clips/cartoon/ for build_cartoon_building_trailer.py.

Usage:
  1. In Chrome DevTools (F12) on Google Flow, run:
       copy(Array.from(document.querySelectorAll('video')).map(v => v.src || v.querySelector('source')?.src).filter(Boolean))
  2. Run:
       python download_flow_clips.py --from-clipboard
"""

import argparse
import base64
import json
import os
import sys
import urllib.request
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).parent
CLIPS_DIR = BASE_DIR / "clips" / "cartoon"

# The 25 shot target filenames from build_cartoon_building_trailer.py (T04 removed)
SHOT_FILENAMES = [
    "T01_railway_dusk.mp4",
    "T02_railway_day.mp4",
    "T03_high_aerial.mp4",
    "T05_prow_crane.mp4",
    "T06_road_trees.mp4",
    "T07_garden_glide.mp4",

    "T08_picnic_arc.mp4",
    "T09_swoop_courtyard.mp4",
    "T10_entrance_approach.mp4",
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
    "T26_title_card.mp4",
]


def download_url(url, dest_path):
    print(f"Downloading -> {dest_path.name}...")
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        dest_path.write_bytes(resp.read())
    print(f"  Saved ({dest_path.stat().st_size / 1024 / 1024:.2f} MB)")


def get_clipboard_text():
    try:
        res = subprocess.run(
            ["powershell", "-NoProfile", "-Command", "Get-Clipboard"],
            capture_output=True,
            text=True,
            timeout=10,
            check=True,
        )
        return res.stdout.strip()
    except Exception as e:
        sys.exit(f"Error reading clipboard: {e}")


def main():
    parser = argparse.ArgumentParser(description="Download Flow video clips.")
    parser.add_argument(
        "--from-clipboard", action="store_true", help="Read URL array or links from clipboard"
    )
    parser.add_argument(
        "--urls-file", help="Path to text/json file containing list of URLs"
    )

    args = parser.parse_args()
    CLIPS_DIR.mkdir(parents=True, exist_ok=True)

    urls = []
    base64_map = {}
    if args.from_clipboard:
        raw = get_clipboard_text()
        try:
            parsed = json.loads(raw)
            if isinstance(parsed, dict):
                base64_map = parsed
            elif isinstance(parsed, list):
                urls = parsed
        except Exception:
            urls = [line.strip() for line in raw.splitlines() if line.strip().startswith("http")]
    elif args.urls_file:
        p = Path(args.urls_file)
        if not p.is_file():
            sys.exit(f"File not found: {p}")
        text = p.read_text(encoding="utf-8")
        try:
            parsed = json.loads(text)
            if isinstance(parsed, dict):
                base64_map = parsed
            elif isinstance(parsed, list):
                urls = parsed
        except Exception:
            urls = [line.strip() for line in text.splitlines() if line.strip().startswith("http")]

    if not urls and not base64_map:
        sys.exit("No valid HTTP URLs or base64 data found on clipboard.")

    # Find existing clips to know where to start naming
    existing = set(p.name for p in CLIPS_DIR.glob("*.mp4"))
    target_idx = 0
    while target_idx < len(SHOT_FILENAMES) and SHOT_FILENAMES[target_idx] in existing:
        target_idx += 1

    if base64_map:
        print(f"Found {len(base64_map)} base64 encoded clips.")
        for i, (key, b64_data) in enumerate(base64_map.items()):
            idx = target_idx + i
            out_name = SHOT_FILENAMES[idx] if idx < len(SHOT_FILENAMES) else f"extra_clip_{idx + 1}.mp4"
            dest = CLIPS_DIR / out_name
            print(f"Writing {dest.name}...")
            dest.write_bytes(base64.b64decode(b64_data))
            print(f"  Saved ({dest.stat().st_size / 1024 / 1024:.2f} MB)")
    else:
        print(f"Found {len(urls)} clip URLs.")
        for i, url in enumerate(urls):
            idx = target_idx + i
            out_name = SHOT_FILENAMES[idx] if idx < len(SHOT_FILENAMES) else f"extra_clip_{idx + 1}.mp4"
            dest = CLIPS_DIR / out_name
            download_url(url, dest)

    print(f"\nDone! Clips saved to {CLIPS_DIR.resolve()}")



if __name__ == "__main__":
    main()
