# 🎵 PERMANENT RULE: META MUSICGEN LARGE STEREO (3.3B PARAMETERS) DEFAULT

> **USER DIRECTIVE**: ALWAYS use Meta MusicGen Large (3.3 Billion Parameters) as the MANDATORY DEFAULT MODEL for all music, score, and soundtrack generation. NEVER use synthetic/algorithmic loops. Upgraded 2026-08-09 to the **stereo** checkpoint (`facebook/musicgen-stereo-large`) for richer spatial sound — same 3.3B family, not a downgrade.

---

## 🚫 STRICT PROHIBITIONS
1. **NO Synthetic / Algorithmic Audio Loops**: Do not synthesize pitch-step loops, repeating sine/saw wave ostinatos, or mathematical audio loops.
2. **NO Downgrade to Smaller Models**: Always use a MusicGen **Large** (3.3B) checkpoint — mono or stereo — as the primary default music generator. Never fall back to `-medium`, `-small`, or other smaller checkpoints.

---

## ✅ MANDATORY MUSIC WORKFLOW
1. **Mandatory Default Model**: **`facebook/musicgen-stereo-large`** (3.3 Billion Parameters, stereo) cached at `C:\ai\models\musicgen-stereo-large\`. The prior mono checkpoint `facebook/musicgen-large` (stored at `C:\ai\models\musicgen-large\`) remains available as a fallback only, not the default.
2. **Audio Properties**: Generate 32kHz neural stereo audio directly from natural language prompts describing organic instruments (cellos, French horns, taiko drums, natural room acoustics).
3. **Outro Continuation**: Always generate full-duration neural audio blocks (`max_new_tokens`) stitched with crossfades to ensure 100% continuous soundtrack coverage through the closing title card and final fade-out.
4. **GPU Execution**: Run generation on the local RTX 4080 (`device="cuda"`, fp16) — do not fall back to CPU, which is prohibitively slow for the 3.3B model.
