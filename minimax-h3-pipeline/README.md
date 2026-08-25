# MiniMax-H3 video pipeline

> **Read alongside**: `SCENE1_MINIMAX_TRACKER.md` (repo root) — the active shot-by-shot
> progress tracker and QA rules for the Scene 1 generation pass this pipeline is being used
> for. `HANDOVER.md` §9 has the session summary and decision context.

## What this is

A local, from-scratch video generation route piloted 2026-08-25 as a possible replacement
for (or supplement to) Google Flow/Veo for animating Scene 1. Uses **MiniMax-H3**
(open-weight, omni-modal, generates video + native synced audio) run via
[stable-diffusion.cpp](https://github.com/leejet/stable-diffusion.cpp)'s `sd-cli`, entirely
on the local RTX 4080 (16GB VRAM).

**This is a genuine finding, not a rejected experiment** (unlike the earlier WAN 2.2 local
video test — see `HANDOVER.md` §6) — both cartoon and photoreal generations produced
usable, identity-consistent results in ~4-5 minutes per clip.

## Where everything lives (machine-specific, not in this repo)

The actual install is **outside this git repo**, at `C:\AI\minimax-h3\` (capital `AI` —
different folder from `C:\ai\Circle the Square`):

- `C:\AI\minimax-h3\bin\sd-cuda12\sd-cli.exe` — prebuilt Windows/CUDA12 binary from
  stable-diffusion.cpp releases, plus its `cudart64_12.dll` etc. copied alongside it.
- `C:\AI\minimax-h3\models\` — `minimax_h3_{ref2va,fl2va}_pruned-Q4_K.gguf` (denoisers),
  `qwen3vl_32b_minimax_h3-Q4_K_M.gguf` (shared text encoder), `vae/minimax_h3_video_vae_fp16.safetensors`,
  `vae/minimax_h3_audio_vae_fp32.safetensors`. ~50GB total, downloaded from
  `huggingface.co/unsloth/MiniMax-H3-GGUF`. **Not committed anywhere** — re-download if this
  machine changes.
- `C:\AI\minimax-h3\refs\` — character/location reference images staged for generation
  (crops from `character-refs/_photoreal-archive/*.jpg` and `location-refs/*.png`, copied
  in, not symlinked).
- `C:\AI\minimax-h3\output\` — generated clips (`.mp4`, auto-converted from the raw
  `.mp4.avi` `sd-cli` actually writes — see gotcha below).

`gen_clip.py` in this folder is the one script that survives in version control — copy it
back to `C:\AI\minimax-h3\` (or point `--refs`/model paths at wherever the install lives) to
resume on a fresh machine, after redownloading the models above.

## Two denoiser variants — do not mix up

- **Ref2VA** (`minimax_h3_ref2va_pruned-*.gguf`): takes a reference image (`-r`/`--ref-image`,
  used via `gen_clip.py --refs`) + a text prompt describing how to animate it. Use this for
  every character/location-locked shot — it's what identity and location consistency depend on.
- **FL2VA** (`minimax_h3_fl2va_pruned-*.gguf`): text-only, zero reference images. Only used
  once this session, for an early "can it do photoreal at all" test. Not the active route —
  `gen_clip.py` is hardcoded to Ref2VA.

These are separate weight partitions. Loading the wrong one for the mode you're using
produces garbage output with no error.

## Usage

```
python gen_clip.py --out F01_c1 --seed 101001 \
  --refs jan_photoreal_front_panel.jpg christina_front_panel.jpg jan_office_location_fixed.png \
  --prompt "Reference 1 shows Jan. Reference 2 shows Christina. Reference 3 shows the office ..."
```

- `--refs` are filenames inside `C:\AI\minimax-h3\refs\` (relative, not full paths).
- Reference multiple images by number in the prompt text ("Reference 1 shows...", "Reference
  2 shows...") — MiniMax-H3 uses natural language, not positional/tagged references.
- Output auto-converts to `.mp4` and deletes the raw `.avi` (see gotcha below) — a 56-frame
  clip is ~300-400KB as `.mp4` vs ~3-6MB raw.
- Defaults: 864×480, 56 frames, 24fps, 20 steps, `--auto-fit` backend placement,
  `--diffusion-fa`. These are the proven-safe settings — see constraints below before
  changing any of them.

## Hardware constraints — read before changing settings

**16GB VRAM is the hard ceiling and it is already nearly maxed at the proven-safe settings.**

- **56 frames (2.33s @ 24fps) is the longest clip length confirmed safe.** 96 frames pushed
  VRAM to ~15.8/16.4GB and caused thrashing (user-observed slowdown, killed mid-run). Do not
  increase `--frames` past 56 without re-testing carefully, watching `nvidia-smi` live.
- **864×480 is the proven-safe resolution.** A 960×544 (MiniMax-H3's native training res)
  test with `--vae-tiling` also stayed under budget (~14.9GB peak) but ran ~20% slower
  overall due to VAE tiling's repeated per-tile reload overhead, for no actual gain — it does
  not fix small/blurry faces in wide shots, which is a *framing* problem, not a resolution
  one. Not adopted as default.
- `--auto-fit` reliably places the denoiser (~10.9GB) + VAE (~5.0GB) on GPU and the 32B
  text-encoder (~17.7GB) on CPU RAM. The one-time text-encoding forward pass on CPU is slow
  (~2 min for a 3-reference prompt) but this is *not* the same failure mode as offloading the
  per-step diffusion transformer (which is what made WAN 2.2 and FLUX.2 klein CPU-offload
  unusably slow) — the heavy iterative compute (sampling) still runs entirely on GPU.
- If VRAM looks like it's climbing toward ~15.8GB+ mid-run, kill it
  (`taskkill //IM sd-cli.exe //F`) rather than letting it thrash.
- **ComfyUI and `sd-cli` cannot run at the same time** — always check `nvidia-smi` and kill
  any leftover ComfyUI python.exe process before starting a MiniMax-H3 generation, and vice
  versa. Both have been left running accidentally this session and caused OOM/RAM failures.

## Known gotchas

- `sd-cli` only writes `.avi`/`.webm`/animated `.webp` containers — passing a `.mp4` output
  path silently gets `.avi` appended (`name.mp4.avi`). `gen_clip.py` handles the ffmpeg
  re-encode + cleanup automatically; don't reinvent this per-script.
- Confirm exact node/flag names via `sd-cli --help` (or `GET /object_info` for ComfyUI)
  before assuming a flag exists — this codebase moves fast and flag names shift between
  builds.
- MiniMax-H3 needs at least one image reference for Ref2VA to lock identity; a raw 4-pose
  turnaround sheet is a *worse* reference than a single cropped clean pose (confuses which
  pose to animate) — always crop to one clean pose before using a `character-refs/*_sheet.*`
  file as a `-r` reference.
