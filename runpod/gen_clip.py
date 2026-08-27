"""Generic MiniMax-H3 Ref2VA clip generator — cross-platform.

Usage: python gen_clip.py --out NAME --seed N --prompt "..." --refs a.jpg b.jpg ...

Derived from `minimax-h3-pipeline/gen_clip.py`. The ONLY substantive change is
binary resolution: the original hardcoded `bin/sd-cuda12/sd-cli.exe`, which is
Windows-only. stable-diffusion.cpp publishes no prebuilt Linux CUDA binary, so
on a pod `sd-cli` is compiled from source and lands at `bin/sd-cli` instead.
This version finds either, so the same file works on the main PC and the pod.
Fold it back over the original when the branches merge.
"""
import argparse
import os
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).parent
MODELS = BASE / "models"
REFS_DIR = BASE / "refs"
OUT_DIR = BASE / "output"


def find_binary():
    """$SD_CLI wins; then the Linux build layout; then the Windows one."""
    env = os.environ.get("SD_CLI")
    if env:
        return Path(env)
    for candidate in (BASE / "bin" / "sd-cli",
                      BASE / "bin" / "sd-cuda12" / "sd-cli.exe",
                      BASE / "bin" / "sd-cuda12" / "sd-cli"):
        if candidate.exists():
            return candidate
    sys.exit(
        f"error: no sd-cli binary found under {BASE / 'bin'}.\n"
        "  Set SD_CLI=/path/to/sd-cli, or run runpod/setup_pod_minimax.sh to build it."
    )


BIN = find_binary()

parser = argparse.ArgumentParser()
parser.add_argument("--out", required=True)
parser.add_argument("--seed", type=int, required=True)
parser.add_argument("--prompt", required=True)
parser.add_argument("--refs", nargs="+", required=True)
parser.add_argument("--frames", type=int, default=56)
parser.add_argument("--width", type=int, default=864)
parser.add_argument("--height", type=int, default=480)
parser.add_argument("--vae-tiling", action="store_true")  # default off: ~20% slower, doesn't fix face clarity
parser.add_argument("--quant", default="Q4_K", choices=["Q3_K", "Q4_K", "Q5_0", "Q6_K", "Q8_0"],
                    help="ref2va denoiser quantisation. Q4_K (11.4GB) is what the 16GB card "
                         "was limited to; Q5_0/Q6_K/Q8_0 (up to ~21.4GB) only became reachable "
                         "on a 48GB card. NOTE: HANDOVER.md is explicit that the wide-shot "
                         "blob face is a pixel-count problem, NOT a quantisation one - raise "
                         "--width/--height for that. A bigger quant is for general fidelity, "
                         "and costs speed via memory bandwidth. Ignored with --turbo.")
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
    diffusion_model = f"minimax_h3_ref2va_pruned-{args.quant}.gguf"
    steps, guidance = "20", "3.5"

if not (MODELS / diffusion_model).exists():
    sys.exit(f"error: {diffusion_model} is not on this machine.\n"
             f"  present: {', '.join(sorted(p.name for p in MODELS.glob('*ref2va*.gguf'))) or 'none'}\n"
             f"  fetch it:  hf download unsloth/MiniMax-H3-GGUF {diffusion_model} --local-dir {MODELS}")

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
print(f"    {args.width}x{args.height}, {args.frames} frames, binary {BIN}")
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
