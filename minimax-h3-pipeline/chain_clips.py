"""Chunked MiniMax-H3 Ref2VA generation: chains N clips into one longer continuous shot.

Each chunk after the first is conditioned on a single reference image extracted from the
last frame of the previous chunk, instead of the original character/location refs. This is
the workaround for MiniMax-H3's single-pass VRAM ceiling (~56-96 frames on a 16GB card,
see minimax-h3-pipeline/README.md) when a longer continuous shot is needed and the
generation-time budget allows multiple chunks (each ~4min with EasyCache).

Usage:
  python chain_clips.py --out NAME --seed 500001 \
    --refs jan_photoreal_front_panel.jpg jan_office_location_fixed.png \
    --prompts "chunk 1 prompt..." "chunk 2 prompt..." "chunk 3 prompt..."

--refs are used for chunk 1 only (filenames inside refs/, same convention as gen_clip.py).
Every later chunk uses only the extracted last frame of the previous chunk as its reference.
Produces NAME_c1.mp4 .. NAME_cN.mp4 plus a concatenated NAME_full.mp4.
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


def run_clip(out_name, seed, prompt, ref_filenames, frames, width, height, standard=False):
    if standard:
        diffusion_model, steps, guidance = "minimax_h3_ref2va_pruned-Q4_K.gguf", "20", "3.5"
    else:
        diffusion_model, steps, guidance = "minimax_h3_ref2va_turbo_Q4_K_M.gguf", "4", "1.0"
    cmd = [
        str(BIN), "-M", "vid_gen",
        "--diffusion-model", str(MODELS / diffusion_model),
        "--llm", str(MODELS / "qwen3vl_32b_minimax_h3-Q4_K_M.gguf"),
        "--vae", str(MODELS / "vae" / "minimax_h3_video_vae_fp16.safetensors"),
        "--audio-vae", str(MODELS / "vae" / "minimax_h3_audio_vae_fp32.safetensors"),
        "--auto-fit", "--diffusion-fa",
        "--cache-mode", "easycache", "--cache-option", "threshold=0.25",
    ]
    for ref in ref_filenames:
        cmd += ["-r", str(REFS_DIR / ref)]
    cmd += [
        "-p", prompt,
        "--cfg-scale", "1.0",
        "--guidance", guidance,
        "-W", str(width), "-H", str(height),
        "--fps", "24",
        "--video-frames", str(frames),
        "--steps", steps,
        "--seed", str(seed),
        "-v",
        "-o", str(OUT_DIR / f"{out_name}.mp4"),
    ]
    print(f"=== Generating {out_name} (seed {seed}, refs {ref_filenames}) ===", flush=True)
    result = subprocess.run(cmd, cwd=str(BASE))
    if result.returncode != 0:
        sys.exit(result.returncode)

    avi_path = OUT_DIR / f"{out_name}.mp4.avi"
    mp4_path = OUT_DIR / f"{out_name}.mp4"
    if avi_path.exists():
        conv = subprocess.run(
            ["ffmpeg", "-y", "-i", str(avi_path), "-c:v", "libx264", "-c:a", "aac", str(mp4_path)],
            capture_output=True,
        )
        if conv.returncode == 0 and mp4_path.exists():
            avi_path.unlink()
            print(f"Converted and removed raw AVI: {mp4_path}", flush=True)
        else:
            print("ffmpeg conversion failed, keeping AVI:", conv.stderr.decode(errors="ignore")[-500:], flush=True)
    return mp4_path


def extract_last_frame(mp4_path, out_ref_filename):
    out_path = REFS_DIR / out_ref_filename
    subprocess.run(
        ["ffmpeg", "-y", "-sseof", "-0.2", "-i", str(mp4_path), "-update", "1", "-vframes", "1", str(out_path)],
        capture_output=True,
    )
    return out_ref_filename


def concat_clips(mp4_paths, final_out):
    list_file = OUT_DIR / "_chain_concat_list.txt"
    with open(list_file, "w") as f:
        for p in mp4_paths:
            f.write(f"file '{p.resolve().as_posix()}'\n")
    subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(list_file), "-c", "copy", str(final_out)],
        capture_output=True,
    )
    list_file.unlink()


parser = argparse.ArgumentParser()
parser.add_argument("--out", required=True)
parser.add_argument("--seed", type=int, required=True)
parser.add_argument("--refs", nargs="+", required=True, help="chunk 1 refs, filenames inside refs/")
parser.add_argument("--prompts", nargs="+", required=True, help="one prompt per chunk, in order")
parser.add_argument("--frames", type=int, default=56)
parser.add_argument("--width", type=int, default=864)
parser.add_argument("--height", type=int, default=480)
parser.add_argument("--standard", action="store_true", help="see gen_clip.py --standard")
args = parser.parse_args()

chunk_mp4s = []
current_refs = args.refs
for i, prompt in enumerate(args.prompts):
    name = f"{args.out}_c{i + 1}"
    mp4 = run_clip(name, args.seed + i, prompt, current_refs, args.frames, args.width, args.height, args.standard)
    chunk_mp4s.append(mp4)
    last_frame_ref = extract_last_frame(mp4, f"_{name}_lastframe.png")
    current_refs = [last_frame_ref]

final_out = OUT_DIR / f"{args.out}_full.mp4"
concat_clips(chunk_mp4s, final_out)
total_frames = len(args.prompts) * args.frames
print(f"=== Done: {final_out} ({total_frames} frames / {total_frames / 24:.1f}s @ 24fps) ===", flush=True)
