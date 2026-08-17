#!/usr/bin/env python3
"""
Track how far a chained sequence has drifted from its original plate.

    python drift_track.py <plate.jpg> <seed1.png> <seed2.png> ...
    python drift_track.py <plate.jpg> --glob "chain/L5/*_end.png"

Every hop reseeds from a generated frame, so error accumulates. This measures the hero
car's IDENTITY - its bodywork shape and its colour - against the ORIGINAL plate, and
reports where the chain has wandered far enough that it is time to move to the next plate.
The scene change then lands exactly where the look starts to go, so drift motivates the
edit instead of spoiling it.

Crucially the comparison is position- and scale-invariant. A fixed crop conflates "the car
changed" with "the car sits four pixels left of where it did", and the second is not drift
- the car legitimately shifts in frame as it drives. So the car is segmented out by its red
bodywork, cropped to its own bounding box and normalised to a fixed size before comparison.
"""
import argparse
import glob as globlib
import os
import sys

import numpy as np
from PIL import Image

NORM = (240, 144)   # normalised car crop
SWITCH_AT = 0.62
WARN_AT = 0.75


def _box(img, r):
    pad = np.pad(img, r + 1, mode="edge")
    integ = pad.cumsum(0).cumsum(1)
    k = 2 * r + 1
    h, w = img.shape
    y = np.arange(h) + r + 1
    x = np.arange(w) + r + 1
    tot = (integ[np.ix_(y + r, x + r)] - integ[np.ix_(y - r - 1, x + r)]
           - integ[np.ix_(y + r, x - r - 1)] + integ[np.ix_(y - r - 1, x - r - 1)])
    return tot / (k * k)


def ssim(a, b, r=4):
    c1, c2 = 0.01 ** 2, 0.03 ** 2
    ma, mb = _box(a, r), _box(b, r)
    saa = _box(a * a, r) - ma * ma
    sbb = _box(b * b, r) - mb * mb
    sab = _box(a * b, r) - ma * mb
    return float(np.mean(((2 * ma * mb + c1) * (2 * sab + c2)) /
                         ((ma ** 2 + mb ** 2 + c1) * (saa + sbb + c2))))


def find_car(path):
    """Segment the red hero car and return a normalised crop of it, plus its mean colour."""
    im = Image.open(path).convert("RGB")
    W, H = im.size
    rgb = np.asarray(im, dtype=np.float64) / 255.0
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]

    # The hero car is the large red mass low in frame. Other red vehicles exist but are
    # small and sit higher up, so restrict to the bottom 55% and trim outliers.
    red = (r > 0.28) & (r > g * 1.45) & (r > b * 1.45)
    red[:int(H * 0.45), :] = False
    if red.sum() < 500:
        return None, None, 0

    # Take the largest CONNECTED red mass, not every red pixel. Distant red cars and tail
    # lights are also red, and including them stretched the bounding box differently in
    # every frame — which read as drift when nothing had actually changed.
    SC = 200
    sy, sx = max(1, H // SC), max(1, W // SC)
    small = red[::sy, ::sx]
    h2, w2 = small.shape
    seen = np.zeros_like(small, dtype=bool)
    best, best_n = None, 0
    for j in range(h2):
        for i in range(w2):
            if not small[j, i] or seen[j, i]:
                continue
            stack, comp = [(j, i)], []
            seen[j, i] = True
            while stack:
                cj, ci = stack.pop()
                comp.append((cj, ci))
                for dj, di in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nj, ni = cj + dj, ci + di
                    if 0 <= nj < h2 and 0 <= ni < w2 and small[nj, ni] and not seen[nj, ni]:
                        seen[nj, ni] = True
                        stack.append((nj, ni))
            if len(comp) > best_n:
                best_n, best = len(comp), comp
    if not best or best_n < 12:
        return None, None, 0

    cj = np.array([p[0] for p in best])
    ci = np.array([p[1] for p in best])
    y0, y1 = int(cj.min() * sy), int((cj.max() + 1) * sy)
    x0, x1 = int(ci.min() * sx), int((ci.max() + 1) * sx)
    pad_x = int((x1 - x0) * 0.06)
    pad_y = int((y1 - y0) * 0.10)
    x0, x1 = max(0, x0 - pad_x), min(W, x1 + pad_x)
    y0, y1 = max(0, y0 - pad_y), min(H, y1 + pad_y)
    if x1 - x0 < 40 or y1 - y0 < 25:
        return None, None, 0

    crop = im.crop((x0, y0, x1, y1)).resize(NORM, Image.LANCZOS)
    c = np.asarray(crop, dtype=np.float64) / 255.0
    gray = c @ np.array([0.299, 0.587, 0.114])
    # mean colour of the actual red pixels only, so background road doesn't dilute it
    cr = c[..., 0], c[..., 1], c[..., 2]
    m = (cr[0] > 0.28) & (cr[0] > cr[1] * 1.45) & (cr[0] > cr[2] * 1.45)
    body = c[m].mean(0) if m.sum() > 100 else c.reshape(-1, 3).mean(0)
    return gray, body, len(xs)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("plate")
    ap.add_argument("seeds", nargs="*")
    ap.add_argument("--glob")
    a = ap.parse_args()

    seeds = sorted(globlib.glob(a.glob)) if a.glob else a.seeds
    if not seeds:
        print("no seed frames given")
        return 1

    bg, bc, bn = find_car(a.plate)
    if bg is None:
        print(f"could not segment the car in {a.plate}")
        return 2
    print(f"plate: {os.path.basename(a.plate)}  (car = {bn} px)")
    print(f"{'hop':>4}  {'shape':>7}  {'colour Δ':>8}  status   frame")

    switch = None
    for i, s in enumerate(seeds, 1):
        g, c, n = find_car(s)
        if g is None:
            print(f"{i:>4}  {'--':>7}  {'--':>8}  NO CAR  {os.path.basename(s)}")
            switch = switch or i
            continue
        sc = ssim(g, bg)
        dc = float(np.abs(c - bc).max())
        # colour drift matters as much as shape: a car turning orange is a fail even if
        # its silhouette is perfect.
        if sc < SWITCH_AT or dc > 0.12:
            status, switch = "SWITCH", (switch or i)
        elif sc < WARN_AT or dc > 0.08:
            status = "warn  "
        else:
            status = "ok    "
        print(f"{i:>4}  {sc:>7.4f}  {dc:>8.4f}  {status}  {os.path.basename(s)}  "
              f"{'#' * int(max(0.0, sc) * 30)}")

    print()
    if switch:
        print(f"=> crossed the threshold at hop {switch}. Transition to the next plate on or "
              f"before that hop.")
    else:
        print(f"=> still healthy after {len(seeds)} hops — the plate is holding; keep going.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
