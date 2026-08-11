# ⚡ AI TOOLS — CAPABILITY & STATUS REFERENCE
> **Plan**: Google AI Pro ($19.99/month)  
> **Last Updated**: 2026-08-09 22:35

---

## 🎵 TOOL 5 — Meta MusicGen Large (3.3B Parameters — MANDATORY DEFAULT)
**Model**: `facebook/musicgen-large` (3.3 Billion Parameters)  
**Location**: `C:\ai\models\musicgen-large\`  
**Access via**: Local PyTorch / Transformers on machine

| Capability | Detail |
| :--- | :--- |
| **What it generates** | Master studio-quality 32kHz cinematic film scores, soundtrack stems, sound effects |
| **Model Size** | **3.3 Billion Parameters** (Meta AI Flagship Music Transformer) |
| **Quota** | None — runs locally on machine |
| **Default Model** | ✅ **YES — Permanent Mandatory Default AI Music Generator** |
| **Current state** | 🟢 **ACTIVE / DEFAULT** |

---

## 🖼️ TOOL 1 — Gemini Flash Image (Still Generation)
**Model**: `gemini-3.1-flash-image`  
**Access via**: Antigravity CLI (ask me directly) or [aistudio.google.com](https://aistudio.google.com)

| Capability | Detail |
| :--- | :--- |
| **What it generates** | Still images, concept art, storyboard frames, character sheets, location sheets. 🎨 **This project renders cartoon** — paste the style anchor from `CARTOON_CAST_BIBLE.md`. Photoreal characters are blocked (likeness protection); cartoon is not. |
| **Resolution** | 0.5K / **1K default** / 2K / 4K |
| **Aspect ratios** | 1:1 · 16:9 · 9:16 · 3:2 · 2:3 · 3:4 · 4:3 · and wide extremes (1:4, 4:1) |
| **Multi-turn editing** | ✅ Yes — can edit specific elements of a generated image in follow-up prompts |
| **Image conditioning** | ✅ Yes — attach up to 3 reference images to guide the output |
| **What it can't do** | ❌ No audio · ❌ No video · ❌ No function calling |
| **Included in AI Pro?** | ✅ Yes — daily quota included |
| **Quota reset** | Daily — resets tonight |
| **Current state** | 🟢 **ACTIVE** |

---

## 🎬 TOOL 2 — Veo Video Generation
**Current model**: `veo-3.1` (Veo 2 was deprecated June 2026 — use Veo 3.1 now)  
**Access via**: [aistudio.google.com](https://aistudio.google.com) → model dropdown → select Veo 3.1

| Capability | Detail |
| :--- | :--- |
| **What it generates** | Short cinematic video clips from text prompts or image references |
| **Resolution** | 720p |
| **Clip duration** | **5–8 seconds** per clip (sweet spot — generates best at 8s) |
| **Input modalities** | Text-to-video · Image-to-video (image conditioning up to 20MB) |
| **Aspect ratios** | 16:9 · 9:16 |
| **Native audio** | ✅ Yes on Veo 3.1 — can generate ambient sound, SFX, and dialogue audio natively |
| **Outputs per prompt** | Up to 4 video variants per generation |
| **Included in AI Pro?** | ✅ Yes — monthly usage cap |
| **Current state** | 🟢 **ACTIVE** |

---

## 🎙️ TOOL 3 — Qwen3-TTS (Local GPU — Always Available)
**Access via**: ComfyUI at `C:\ai\ComfyUI\`

| Capability | Detail |
| :--- | :--- |
| **What it generates** | Hyper-realistic character dialogue `.wav` voice files |
| **Characters locked** | Jan · Christina · Sharon · Chris · Rick |
| **Quota** | None — runs on your local GPU |
| **Current state** | 🟢 **AVAILABLE** |

---

## 💬 TOOL 4 — Gemini Text / Code (This CLI)
**Access via**: Antigravity CLI — this conversation

| Capability | Detail |
| :--- | :--- |
| **What it does** | Planning · Scripting · Prompt writing · Documentation · Git · File management |
| **Quota** | Very high daily limit |
| **Current state** | 🟢 **AVAILABLE** |

---

## 🔄 Status Summary

| Tool | State | Resets |
| :--- | :--- | :--- |
| 🟢 **Meta MusicGen Large (3.3B)** | **PERMANENT DEFAULT** | No quota |
| 🟢 Gemini Flash Image | AVAILABLE | Daily reset |
| 🟢 Veo 3.1 Video | AVAILABLE | Daily reset |
| 🟢 Qwen3-TTS (Local) | AVAILABLE | No quota |
| 🟢 Gemini Text / CLI | AVAILABLE | No quota |
| 🟢 Git / GitHub | AVAILABLE | No limit |
