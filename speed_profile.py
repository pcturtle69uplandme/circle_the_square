#!/usr/bin/env python3
"""
Per-second tarmac motion energy for one or more clips.

    python speed_profile.py clip1.mp4 [clip2.mp4 ...]

The single most important measurement for this project: it shows whether the car holds
speed for the whole take or decelerates into the final frame. A clip that eases out will
visibly brake at every cut, so the tail figure decides whether a clip is usable and where
it has to be trimmed.
"""
import glob
import os
import subprocess
import sys
import tempfile
import shutil

import numpy as np
from PIL import Image

FPS = 8
ROAD_TOP = 0.78  # fraction of height; below this is tarmac rushing past


def profile(path):
    d = tempfile.mkdtemp(prefix="spd_")
    try:
        subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vf", f"fps={FPS},scale=640:360",
                        os.path.join(d, "f_%03d.png")], check=True)
        fs = sorted(glob.glob(os.path.join(d, "f_*.png")))
        if len(fs) < FPS:
            return None
        g = [np.asarray(Image.open(f).convert("L"), dtype=float) / 255 for f in fs]
        y0 = int(360 * ROAD_TOP)
        e = [float(np.abs(g[i + 1][y0:, :] - g[i][y0:, :]).mean()) for i in range(len(g) - 1)]
        secs = []
        for s in range(len(e) // FPS + (1 if len(e) % FPS else 0)):
            seg = e[s * FPS:(s + 1) * FPS]
            if seg:
                secs.append(float(np.mean(seg)))
        return secs
    finally:
        shutil.rmtree(d, ignore_errors=True)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    for path in sys.argv[1:]:
        secs = profile(path)
        if not secs:
            print(f"{path}: too short to profile")
            continue
        peak = max(secs)
        print(f"\n{os.path.basename(path)}")
        for i, v in enumerate(secs):
            bar = "#" * int(v / peak * 44)
            print(f"  {i}-{i+1}s  {v:.4f}  {bar}")
        tail_pct = secs[-1] / peak * 100
        # A healthy chain clip holds speed to the final frame; anything under ~55% of peak
        # in the last second is a visible brake.
        verdict = "HOLDS SPEED" if tail_pct >= 55 else ("SOFT TAIL" if tail_pct >= 30 else "BRAKES HARD")
        print(f"  last second = {tail_pct:.0f}% of peak  ->  {verdict}")
        # Where does it stop being usable?
        cut = len(secs)
        for i, v in enumerate(secs):
            if v / peak < 0.45:
                cut = i
                break
        print(f"  usable footage: 0-{cut}s of {len(secs)}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
