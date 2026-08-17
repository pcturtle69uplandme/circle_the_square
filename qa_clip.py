#!/usr/bin/env python3
"""
Drift QA for a generated OutRun clip.

    python qa_clip.py <clip.mp4> <plate.jpg> [--fps 6] [--json out.json] [--sheet out.png]

Answers four questions numerically, so clips get accepted or rejected on evidence
rather than on a vibe check:

  1. ENDPOINT FIDELITY  does frame 0 / the last frame actually match the plate?
                        (this is the bit Frames-to-Video is supposed to guarantee)
  2. LOOP CLOSURE       does the last frame match the first, i.e. will it loop clean?
  3. CAR STABILITY      does the hero car morph, change colour or change shape mid-clip?
                        Measured on a fixed bottom-centre ROI where the car always sits.
  4. POP DETECTION      does anything materialise out of nowhere — a new car, a new road,
                        a new building? Measured as spikes in frame-to-frame delta that
                        are not explained by the steady forward-travel baseline.

Exit code 0 = PASS, 1 = REVIEW, 2 = FAIL.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image

# Fixed ROI where the hero car body sits in every plate (fractions of w/h).
# Kept tight to the bodywork: a looser box includes roadside and sky, which legitimately
# change as the world travels past, and that false-flagged "hero car morphs" on a clip
# where the car was in fact perfectly stable.
CAR_ROI = (0.36, 0.62, 0.64, 0.96)
# Upper band: sky/horizon/roadside — where new roads and buildings would appear.
WORLD_ROI = (0.0, 0.0, 1.0, 0.55)
# Bottom band: tarmac rushing past. Its frame-to-frame energy IS the sense of speed.
ROAD_ROI = (0.0, 0.78, 1.0, 1.0)

# Tarmac motion energy below this reads as a parked car with a wobbling background.
SPEED_FLOOR = 0.010

WORK_W, WORK_H = 640, 360


# ---------------------------------------------------------------- image utils

def _box_blur(img, r):
    """Mean filter over a (2r+1) square, via integral image. img is 2-D float."""
    pad = np.pad(img, r + 1, mode="edge")
    integral = pad.cumsum(0).cumsum(1)
    k = 2 * r + 1
    h, w = img.shape
    y, x = np.arange(h) + r + 1, np.arange(w) + r + 1
    y0, y1 = y - r - 1, y + r
    x0, x1 = x - r - 1, x + r
    total = (integral[np.ix_(y1, x1)] - integral[np.ix_(y0, x1)]
             - integral[np.ix_(y1, x0)] + integral[np.ix_(y0, x0)])
    return total / (k * k)


def ssim(a, b, r=4):
    """Windowed SSIM on grayscale float arrays in [0,1]. Returns mean SSIM."""
    c1, c2 = 0.01 ** 2, 0.03 ** 2
    mu_a, mu_b = _box_blur(a, r), _box_blur(b, r)
    saa = _box_blur(a * a, r) - mu_a * mu_a
    sbb = _box_blur(b * b, r) - mu_b * mu_b
    sab = _box_blur(a * b, r) - mu_a * mu_b
    num = (2 * mu_a * mu_b + c1) * (2 * sab + c2)
    den = (mu_a ** 2 + mu_b ** 2 + c1) * (saa + sbb + c2)
    return float(np.mean(num / den))


def crop(arr, roi):
    h, w = arr.shape[:2]
    x0, y0, x1, y1 = roi
    return arr[int(y0 * h):int(y1 * h), int(x0 * w):int(x1 * w)]


def load(path):
    im = Image.open(path).convert("RGB").resize((WORK_W, WORK_H), Image.LANCZOS)
    rgb = np.asarray(im, dtype=np.float64) / 255.0
    gray = rgb @ np.array([0.299, 0.587, 0.114])
    return rgb, gray


def mean_rgb(rgb, roi):
    return crop(rgb, roi).reshape(-1, 3).mean(0)


# ---------------------------------------------------------------- extraction

def extract(clip, fps, outdir):
    cmd = ["ffmpeg", "-v", "error", "-i", clip, "-vf", f"fps={fps}",
           os.path.join(outdir, "f_%04d.png")]
    subprocess.run(cmd, check=True)
    return sorted(os.path.join(outdir, f) for f in os.listdir(outdir)
                  if f.startswith("f_"))


def contact_sheet(paths, idxs, labels, out, cols=4):
    thumbs = []
    for i, lab in zip(idxs, labels):
        im = Image.open(paths[i]).convert("RGB").resize((480, 270))
        thumbs.append((im, lab))
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 480, rows * 270), (12, 12, 12))
    for n, (im, _) in enumerate(thumbs):
        sheet.paste(im, ((n % cols) * 480, (n // cols) * 270))
    sheet.save(out)


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("clip")
    ap.add_argument("plate")
    ap.add_argument("--fps", type=float, default=6.0)
    ap.add_argument("--json", dest="json_out")
    ap.add_argument("--sheet", dest="sheet_out")
    a = ap.parse_args()

    tmp = tempfile.mkdtemp(prefix="qaclip_")
    try:
        frames = extract(a.clip, a.fps, tmp)
        if len(frames) < 4:
            print("FAIL: extracted only %d frames" % len(frames))
            return 2

        plate_rgb, plate_gray = load(a.plate)
        data = [load(f) for f in frames]
        grays = [g for _, g in data]
        rgbs = [c for c, _ in data]

        # 1. endpoint fidelity ------------------------------------------------
        first_v_plate = ssim(crop(grays[0], WORLD_ROI), crop(plate_gray, WORLD_ROI))
        last_v_plate = ssim(crop(grays[-1], WORLD_ROI), crop(plate_gray, WORLD_ROI))

        # 2. loop closure -----------------------------------------------------
        loop = ssim(grays[0], grays[-1])

        # 3. car stability ----------------------------------------------------
        plate_car = crop(plate_gray, CAR_ROI)
        car_ssim = [ssim(crop(g, CAR_ROI), plate_car) for g in grays]
        plate_car_rgb = mean_rgb(plate_rgb, CAR_ROI)
        car_hue_drift = [float(np.abs(mean_rgb(c, CAR_ROI) - plate_car_rgb).max())
                         for c in rgbs]

        # 4. pop detection ----------------------------------------------------
        # Frame-to-frame delta in the world band. Forward travel gives a steady
        # baseline; a car or road appearing from nowhere is a spike above it.
        deltas = [float(np.abs(crop(grays[i + 1], WORLD_ROI)
                               - crop(grays[i], WORLD_ROI)).mean())
                  for i in range(len(grays) - 1)]
        # A z-score alone false-fires on near-static footage, where the MAD collapses
        # to quantisation noise — so a spike must also clear an absolute floor.
        ABS_FLOOR = 0.004
        med = float(np.median(deltas))
        mad = float(np.median([abs(d - med) for d in deltas])) or 1e-6
        spikes = [{"frame": i + 1, "t": round((i + 1) / a.fps, 2),
                   "delta": round(d, 5), "z": round((d - med) / (1.4826 * mad), 2)}
                  for i, d in enumerate(deltas)
                  if (d - med) / (1.4826 * mad) > 6.0
                  and d > max(ABS_FLOOR, med * 1.5)]

        # 5. speed ------------------------------------------------------------
        # Tarmac motion energy. Two failure modes matter: the whole clip being too
        # slow (car looks parked), and the clip easing out at the end to hit its
        # pinned last frame — which makes the car visibly brake at every loop point.
        road_energy = [float(np.abs(crop(grays[i + 1], ROAD_ROI)
                                    - crop(grays[i], ROAD_ROI)).mean())
                       for i in range(len(grays) - 1)]
        span = max(1, int(round(a.fps)))  # one second of samples
        head = float(np.mean(road_energy[:span]))
        tail = float(np.mean(road_energy[-span:]))
        ease_ratio = tail / head if head > 1e-9 else 0.0

        worst_car = int(np.argmin(car_ssim))

        res = {
            "clip": a.clip, "plate": a.plate, "frames": len(frames), "fps": a.fps,
            "endpoint_fidelity": {"first_vs_plate": round(first_v_plate, 4),
                                  "last_vs_plate": round(last_v_plate, 4)},
            "loop_closure": round(loop, 4),
            "car_stability": {"min_ssim": round(float(min(car_ssim)), 4),
                              "mean_ssim": round(float(np.mean(car_ssim)), 4),
                              "worst_frame": worst_car,
                              "worst_t": round(worst_car / a.fps, 2),
                              "max_colour_drift": round(float(max(car_hue_drift)), 4)},
            "pops": {"baseline_delta": round(med, 5), "spikes": spikes},
            "speed": {"mean_road_energy": round(float(np.mean(road_energy)), 5),
                      "first_second": round(head, 5),
                      "last_second": round(tail, 5),
                      "ease_out_ratio": round(ease_ratio, 3)},
        }

        # verdict --------------------------------------------------------------
        fails, reviews = [], []
        if first_v_plate < 0.80:
            fails.append(f"first frame does not match plate (SSIM {first_v_plate:.3f})")
        if last_v_plate < 0.80:
            fails.append(f"last frame does not match plate (SSIM {last_v_plate:.3f}) — will not loop")
        if loop < 0.85:
            fails.append(f"loop closure poor (SSIM {loop:.3f})")
        if min(car_ssim) < 0.70:
            fails.append(f"hero car morphs at t={worst_car / a.fps:.1f}s (SSIM {min(car_ssim):.3f})")
        elif min(car_ssim) < 0.82:
            reviews.append(f"hero car wobbles at t={worst_car / a.fps:.1f}s (SSIM {min(car_ssim):.3f})")
        if max(car_hue_drift) > 0.10:
            fails.append(f"hero car colour shifts ({max(car_hue_drift):.3f})")
        if spikes:
            reviews.append(f"{len(spikes)} pop-in candidate(s) at "
                           + ", ".join(f"{s['t']}s" for s in spikes))
        if np.mean(road_energy) < SPEED_FLOOR:
            fails.append(f"car is not travelling at speed — tarmac motion energy "
                         f"{np.mean(road_energy):.4f} < {SPEED_FLOOR}")
        if ease_ratio < 0.70:
            fails.append(f"clip decelerates into its end frame (ease-out ratio "
                         f"{ease_ratio:.2f}) — the car will visibly brake at every loop point")
        elif ease_ratio < 0.85 or ease_ratio > 1.30:
            reviews.append(f"speed is uneven head-to-tail (ratio {ease_ratio:.2f})")

        res["verdict"] = "FAIL" if fails else ("REVIEW" if reviews else "PASS")
        res["notes"] = fails + reviews

        if a.sheet_out:
            idxs = [0, worst_car, len(frames) - 1] + [s["frame"] for s in spikes[:5]]
            labels = ["first", "worst car", "last"] + [f"pop {s['t']}s" for s in spikes[:5]]
            contact_sheet(frames, idxs, labels, a.sheet_out)
            res["sheet"] = a.sheet_out

        out = json.dumps(res, indent=2)
        print(out)
        if a.json_out:
            with open(a.json_out, "w", encoding="utf-8") as fh:
                fh.write(out)

        return {"PASS": 0, "REVIEW": 1, "FAIL": 2}[res["verdict"]]
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
