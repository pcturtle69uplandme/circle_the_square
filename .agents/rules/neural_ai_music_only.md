# 🎵 PERMANENT RULE: EXTERNAL MUSIC SERVICES ONLY — NO LOCAL MUSIC LLM

> **USER DIRECTIVE** (updated 2026-08-12): NEVER run any local music generation model (e.g. MusicGen, AudioCraft, Jukebox, or any GPU-local music inference). All music and soundtrack audio MUST come from external cloud music generation services such as **Google Flow Music** (https://www.flowmusic.app/) or equivalent. Drop pre-generated external audio files into `audio-refs/` and reference them in the build script.

---

## 🚫 STRICT PROHIBITIONS
1. **NO Local Music LLM**: Do NOT run `facebook/musicgen-stereo-large`, `facebook/musicgen-large`, `facebook/musicgen-medium`, or any other local AudioCraft / MusicGen model checkpoint on the user's machine.
2. **NO GPU Music Inference**: Do NOT use `torch`, `transformers`, `MusicgenForConditionalGeneration`, or any local model inference pipeline for music generation.
3. **NO Synthetic / Algorithmic Audio Loops**: Do not synthesize pitch-step loops, repeating sine/saw wave ostinatos, or mathematical audio patterns using `-stream_loop` in FFmpeg or any code-generated audio.

---

## ✅ MANDATORY MUSIC WORKFLOW
1. **External Service Only**: Instruct the user to generate music tracks via **Google Flow Music** (https://www.flowmusic.app/) or another cloud music generation service.
2. **Drop Files to `audio-refs/`**: Place the externally generated audio files (MP3 or WAV) into `C:\kontitemp\ai\circle_the_square\audio-refs\`.
3. **Reference in Build Script**: Update `build_cartoon_building_trailer.py` to point `audio_bed_1` and `audio_bed_2` to the external audio files — no local generation code.
4. **2 Assembly Integrations**: Always assemble exactly 2 distinct external tracks sequentially with smooth crossfades (no loops, no repeats) for the full trailer duration.
