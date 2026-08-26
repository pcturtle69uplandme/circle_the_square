# Wan 2.2 TI2V-5B pipeline — wide/establishing/silent shots

Added 2026-08-26 as the local route for shots MiniMax-H3 can't handle well and Google Flow
can't handle at all. See `minimax-h3-pipeline/README.md` for the MiniMax-H3 side (close-up,
dialogue-bearing shots — that pipeline is unaffected by this one).

## Why this exists

Two dead ends led here:
1. **MiniMax-H3 fails on wide shots.** At 864x480 in a full-room wide framing, faces resolve
   to a genuinely featureless blob (checked at native pixel crop, not just "soft") — a
   pixel-count problem, not fixable by quantization or upscaling (an upscaler can't recover
   detail that was never resolved, and risks inventing a wrong-looking face for an
   identity-locked character).
2. **Google Flow can't replace it either** — Flow's likeness/content filters block or
   complain about generating photoreal humans doing certain actions, making it unreliable
   for this project's identity-locked character shots.

Wan 2.2 TI2V-5B (the dense 5B model, not the 14B MoE variant — see below) turned out to be
small enough to run entirely within 16GB VRAM without the RAM-offload trap that made WAN
2.2's 14B variant and FLUX.2 klein "unusably slow" on this same machine, while producing
sharper output than MiniMax-H3 even at wider framings.

## Where everything lives (machine-specific, not in this repo)

- `C:\AI\wan22-ti2v\models\` — `diffusion_models/wan2.2_ti2v_5B_fp16.safetensors` (10.0GB),
  `vae/wan2.2_vae.safetensors` (1.4GB), `text_encoders/umt5-xxl-encoder-Q8_0.gguf` (6.0GB).
  ~17.4GB total, downloaded from `Comfy-Org/Wan_2.2_ComfyUI_Repackaged` and
  `city96/umt5-xxl-encoder-gguf` on HuggingFace. **Not committed anywhere** — re-download if
  this machine changes.
- `C:\AI\wan22-ti2v\refs\` — reference images (see below — usually bootstrapped from a
  MiniMax-H3 output frame, not a fresh photo).
- `C:\AI\wan22-ti2v\output\` — generated clips.
- Uses the **same `sd-cli.exe` binary** as the MiniMax-H3 pipeline
  (`C:\AI\minimax-h3\bin\sd-cuda12\sd-cli.exe`) — stable-diffusion.cpp supports both models.
  **Still can't run both pipelines' generations at the same time** — same GPU-contention risk
  as running two MiniMax jobs at once; check `tasklist | grep sd-cli` first.

## This is NOT MiniMax-H3's Ref2VA — single reference image only

sd-cli's Wan 2.2 support is single-image I2V (`-i`), not a multi-reference mode. Checked the
official `stable-diffusion.cpp` docs directly to confirm there's no `-r`/multi-ref flag for
Wan — same story as LTX-2.3, whose multi-reference IC-LoRA support is ComfyUI-only plumbing
not present in this CLI.

**The reference image's framing carries over almost literally.** Tested 2026-08-26:
- A standing full-body turnaround photo (`jan_photoreal_front_panel.jpg`) as `-i` produced a
  clip that stayed cropped to the torso for its entire length — the text prompt ("sits at
  his desk... looks up at the camera") did not pull the framing into anything resembling
  that description. I2V here preserves composition far more than it reinterprets it.
  Sharp texture detail (suit, tie weave) even at this crop, though — the underlying
  resolution/decode quality is genuinely better than MiniMax-H3's.
- Using a **MiniMax-H3-generated frame already showing Jan seated at his desk**
  (`jan_seated_desk_ref.png`, extracted from `F02_v3_c1.mp4`'s first frame) as `-i` instead
  produced a clean, sharp, fully-visible face in the correct pose immediately.

**Practical rule: always bootstrap the `-i` reference from an actual frame in roughly the
target pose/framing**, not a turnaround/portrait sheet. For a shot with no existing frame to
pull from, composite one yourself (paste the character crop into the location plate,
roughly matching the intended camera framing) before using it here — untested but should
work on the same principle, since the model is clearly following the reference's
composition closely.

## No audio — this pipeline is for silent shots only

Wan 2.2 TI2V-5B is video-only (checked via `ffprobe` — no audio stream in output). This is
fine because this pipeline exists specifically for shots that don't need dialogue
(wide/establishing/reaction/b-roll) — add room-tone/ambience downstream in the edit.
**Do not use this for dialogue-bearing shots** — those stay on `minimax-h3-pipeline/`, which
has verified-correct synced audio (see that README's turbo-audio-failure section for why
audio correctness needs active verification, not just "sounds probably fine").

If a shot using this pipeline later turns out to need actual speech, that requires a
separate TTS + lip-sync pipeline — real added complexity, not something built here. Don't
attempt to bolt audio onto a Wan clip casually.

**This is not just a hypothetical** — F01 is exactly this case: it's a wide establishing
shot (the reason it was routed here in the first place) but it also carries Christina's line
("Morning Jan. Survive the weekend?"). Not resolved as of 2026-08-26 — see
`SCENE1_MINIMAX_TRACKER.md` row 1 for the options being weighed (accept MiniMax's blur,
split into wide-then-cut coverage, or add a TTS/lip-sync layer). Check whether a shot
actually has dialogue before assuming it belongs in this pipeline just because it's wide.

## Usage

```
python gen_wide_clip.py --out NAME --seed N --ref some_frame.png --prompt "..."
```

- `--ref` is a single filename inside `C:\AI\wan22-ti2v\refs\` (see framing rule above).
- Defaults: 832x480, 24fps, cfg-scale 6.0, flow-shift 3.0, euler sampler, `--vae-tiling`
  hardcoded on (see below — do not remove).
- `--frames` defaults to **240 (~10s)** — validated single-pass, no chaining, in ~9 minutes.
  This is the headline win over MiniMax-H3, which needed risky chained 56-frame segments to
  reach anywhere near 10s. Actual output frame count rounds to the model's latent
  compression grid — 240 requested produced 237 real frames (9.875s), close enough.

## Critical flag: `--vae-tiling` is not optional

Without it, the VAE decode step requests a compute buffer around 21GB against this 16GB
card — the sampling step itself is fast (29s for 33 frames!) but the decode alone then took
**794 seconds** (13+ minutes) for just 33 frames, functionally unusable. With `--vae-tiling`,
the same clip decoded in ~20s and the compute buffer request drops to ~1-14GB depending on
frame count (scales with frame count, checked up to 240 frames without issue). This is the
single most important setting for this model on this hardware. If you ever see this pipeline
running unexpectedly slowly, check this flag is actually present before anything else.

## Validated results (2026-08-26)

- 33 frames (1.4s): 54s total generation, sharp face when ref framing was right.
- 240 frames (~10s): 530s (~8.8min) total, VRAM peaked ~13.9GB (no thrashing). Checked frames
  at 0%, 50%, 100% of the clip — identity, framing, wardrobe, location all held with zero
  drift (this is a single continuous generation, not a chained/stitched one — no splice
  points to drift at).
- Not yet tested: two-character shots, camera motion/panning prompts, a from-scratch
  composited reference (only tested bootstrapping from an existing MiniMax-H3 frame so far).
