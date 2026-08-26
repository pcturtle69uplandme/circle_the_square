"""Wan 2.2 TI2V-5B single-image I2V clip generator — for wide/establishing/silent shots.

Added 2026-08-26 as the local replacement for wide shots that were failing on MiniMax-H3
(faces reading as a blurry, featureless blob at 864x480 in a full-room wide framing — a
resolution/pixel-count problem, not fixable by better quantization) and that couldn't go to
Google Flow either (Flow's likeness/content filters kept blocking photoreal human generation).

Usage: python gen_wide_clip.py --out NAME --seed N --ref some_frame.png --prompt "..."

Key differences from minimax-h3-pipeline/gen_clip.py:
- Single reference image only (--ref, one file) — Wan's sd-cli support is single-image I2V,
  not MiniMax-H3's true multi-reference Ref2VA. The reference should already be framed and
  posed close to what you want the output to look like: I2V strongly preserves the
  reference's framing/composition rather than reinterpreting it from a text prompt (tested
  2026-08-26 — a standing full-body turnaround photo produced a clip that never showed the
  face; a MiniMax-H3-generated seated-at-desk frame produced a clean, well-framed result).
  For a brand-new scene with no existing frame to bootstrap from, composite a reference
  image yourself (paste the character crop into the location plate) before using it here.
- No audio. Wan 2.2 TI2V-5B is video-only. This pipeline is for shots that don't need
  dialogue (wide/establishing/reaction/b-roll) — add room-tone/ambience downstream in the
  edit, don't try to bolt speech onto this. Dialogue-bearing shots stay on MiniMax-H3
  (minimax-h3-pipeline/), which has verified-correct synced audio.
- --frames defaults to 240 (~10s @ 24fps) — validated single-pass, no chaining needed, in
  ~9 minutes. This is the headline win over MiniMax-H3, which needed chained 56-frame
  segments (with real framing-drift risk) to reach anywhere near 10s.
- `--vae-tiling` is NOT optional here — it's hardcoded on. Without it, the VAE decode step
  requested a ~21GB compute buffer against our 16GB card and took 794s (13+ minutes) for
  just 33 frames, functionally unusable. With it, the same clip decoded in ~20s. This is the
  single most important flag for this model on this hardware — do not remove it "to try
  without" without re-testing carefully.
"""
import argparse
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).parent
BIN = Path("C:/AI/minimax-h3/bin/sd-cuda12/sd-cli.exe")  # shared binary, same stable-diffusion.cpp build
MODELS = Path("C:/AI/wan22-ti2v/models")
REFS_DIR = Path("C:/AI/wan22-ti2v/refs")
OUT_DIR = Path("C:/AI/wan22-ti2v/output")

parser = argparse.ArgumentParser()
parser.add_argument("--out", required=True)
parser.add_argument("--seed", type=int, required=True)
parser.add_argument("--prompt", required=True)
parser.add_argument("--ref", required=True, help="single reference image filename, inside refs/")
parser.add_argument("--frames", type=int, default=240)
parser.add_argument("--width", type=int, default=832)
parser.add_argument("--height", type=int, default=480)
parser.add_argument("--negative-prompt", default="worst quality, low quality, blurry, distorted, artifacts")
args = parser.parse_args()

cmd = [
    str(BIN), "-M", "vid_gen",
    "--diffusion-model", str(MODELS / "diffusion_models" / "wan2.2_ti2v_5B_fp16.safetensors"),
    "--vae", str(MODELS / "vae" / "wan2.2_vae.safetensors"),
    "--t5xxl", str(MODELS / "text_encoders" / "umt5-xxl-encoder-Q8_0.gguf"),
    "--auto-fit", "--diffusion-fa", "--vae-tiling",
    "-i", str(REFS_DIR / args.ref),
    "-p", args.prompt,
    "-n", args.negative_prompt,
    "--cfg-scale", "6.0",
    "--sampling-method", "euler",
    "--flow-shift", "3.0",
    "-W", str(args.width), "-H", str(args.height),
    "--video-frames", str(args.frames),
    "--fps", "24",
    "--seed", str(args.seed),
    "-v",
    "-o", str(OUT_DIR / f"{args.out}.mp4"),
]

print(f"=== Generating {args.out} (seed {args.seed}, ref {args.ref}, {args.frames} frames) ===")
sys.stdout.flush()
result = subprocess.run(cmd, cwd=str(MODELS.parent))
if result.returncode != 0:
    sys.exit(result.returncode)

avi_path = OUT_DIR / f"{args.out}.mp4.avi"
mp4_path = OUT_DIR / f"{args.out}.mp4"
if avi_path.exists():
    conv = subprocess.run(
        ["ffmpeg", "-y", "-i", str(avi_path), "-c:v", "libx264", str(mp4_path)],
        capture_output=True,
    )
    if conv.returncode == 0 and mp4_path.exists():
        avi_path.unlink()
        print(f"Converted and removed raw AVI: {mp4_path}")
    else:
        print("ffmpeg conversion failed, keeping AVI:", conv.stderr.decode(errors="ignore")[-500:])
sys.exit(0)
