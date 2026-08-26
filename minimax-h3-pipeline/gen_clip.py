"""Generic MiniMax-H3 Ref2VA clip generator for the Scene 1 pipeline.
Usage: python gen_clip.py --out NAME --seed N --prompt "..." --refs a.jpg b.jpg ...
"""
import argparse
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).parent
BIN = BASE / "bin" / "sd-cuda12" / "sd-cli.exe"
MODELS = BASE / "models"
REFS_DIR = BASE / "refs"
OUT_DIR = BASE / "output"

parser = argparse.ArgumentParser()
parser.add_argument("--out", required=True)
parser.add_argument("--seed", type=int, required=True)
parser.add_argument("--prompt", required=True)
parser.add_argument("--refs", nargs="+", required=True)
parser.add_argument("--frames", type=int, default=56)
parser.add_argument("--width", type=int, default=864)
parser.add_argument("--height", type=int, default=480)
parser.add_argument("--vae-tiling", action="store_true")  # default off: ~20% slower, doesn't fix face clarity
parser.add_argument("--turbo", action="store_true",
                     help="use the turbo checkpoint (4 steps, guidance 1.0) instead of the "
                          "standard denoiser (20 steps, guidance 3.5). WARNING: verified "
                          "2026-08-26 that turbo's 4-step audio is unintelligible garbage "
                          "(Whisper transcription: empty/wrong) even though video quality is "
                          "fine — only use --turbo for shots with NO dialogue (B-roll, "
                          "establishing shots with no speech). Standard model + EasyCache is "
                          "the safe default and still ~4.1min/clip vs ~5.3-5.5min baseline.")
args = parser.parse_args()

if args.turbo:
    diffusion_model = "minimax_h3_ref2va_turbo_Q4_K_M.gguf"
    steps, guidance = "4", "1.0"
else:
    diffusion_model = "minimax_h3_ref2va_pruned-Q4_K.gguf"
    steps, guidance = "20", "3.5"

cmd = [
    str(BIN), "-M", "vid_gen",
    "--diffusion-model", str(MODELS / diffusion_model),
    "--llm", str(MODELS / "qwen3vl_32b_minimax_h3-Q4_K_M.gguf"),
    "--vae", str(MODELS / "vae" / "minimax_h3_video_vae_fp16.safetensors"),
    "--audio-vae", str(MODELS / "vae" / "minimax_h3_audio_vae_fp32.safetensors"),
    "--auto-fit",
    "--diffusion-fa",
    "--cache-mode", "easycache",
    "--cache-option", "threshold=0.25",
]
if args.vae_tiling:
    cmd.append("--vae-tiling")
for ref in args.refs:
    cmd += ["-r", str(REFS_DIR / ref)]
cmd += [
    "-p", args.prompt,
    "--cfg-scale", "1.0",
    "--guidance", guidance,
    "-W", str(args.width), "-H", str(args.height),
    "--fps", "24",
    "--video-frames", str(args.frames),
    "--steps", steps,
    "--seed", str(args.seed),
    "-v",
    "-o", str(OUT_DIR / f"{args.out}.mp4"),
]

print(f"=== Generating {args.out} (seed {args.seed}, refs {args.refs}) ===")
sys.stdout.flush()
result = subprocess.run(cmd, cwd=str(BASE))
if result.returncode != 0:
    sys.exit(result.returncode)

avi_path = OUT_DIR / f"{args.out}.mp4.avi"
mp4_path = OUT_DIR / f"{args.out}.mp4"
if avi_path.exists():
    conv = subprocess.run(
        ["ffmpeg", "-y", "-i", str(avi_path), "-c:v", "libx264", "-c:a", "aac", str(mp4_path)],
        capture_output=True,
    )
    if conv.returncode == 0 and mp4_path.exists():
        avi_path.unlink()
        print(f"Converted and removed raw AVI: {mp4_path}")
    else:
        print("ffmpeg conversion failed, keeping AVI:", conv.stderr.decode(errors="ignore")[-500:])
sys.exit(0)
