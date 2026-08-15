# Working rules (user directives, 2026-08-15)

1. **Wait for instructions.** Do not start work, chain steps, or continue to a
   next step without the user's explicit direction. State what you would do
   next and stop, unless the user tells you to proceed autonomously.
2. **VRAM-resident models only.** The GPU is an RTX 4080 16 GB. Local
   image/video pipelines must fit entirely in VRAM — no CPU-offloaded
   pipelines (bf16 klein measured ~10 min/frame that way and the path was
   removed on purpose). For FLUX.2 klein use `--model 4b` (distilled drafts,
   default) or `--model 9b` (base, keepers only).
3. **10-minute frame budget.** No single image/frame render may exceed
   10 minutes. If a configuration would, step down the quality ladder
   (fewer steps, smaller refs, distilled model) instead of waiting.
