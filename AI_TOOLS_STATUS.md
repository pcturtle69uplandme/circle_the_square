# ⚡ AI TOOLS — CAPABILITY & STATUS REFERENCE
> **Plan**: Google AI Pro ($19.99/month)  
> **Last Updated**: 2026-08-08 16:29

---

## 🖼️ TOOL 1 — Gemini Flash Image (Still Generation)
**Model**: `gemini-3.1-flash-image`  
**Access via**: Antigravity CLI (ask me directly) or [aistudio.google.com](https://aistudio.google.com)

| Capability | Detail |
| :--- | :--- |
| **What it generates** | Photorealistic still images, concept art, storyboard frames, character sheets, location sheets |
| **Resolution** | 0.5K / **1K default** / 2K / 4K |
| **Aspect ratios** | 1:1 · 16:9 · 9:16 · 3:2 · 2:3 · 3:4 · 4:3 · and wide extremes (1:4, 4:1) |
| **Multi-turn editing** | ✅ Yes — can edit specific elements of a generated image in follow-up prompts |
| **Image conditioning** | ✅ Yes — attach up to 3 reference images to guide the output |
| **What it can't do** | ❌ No audio · ❌ No video · ❌ No function calling |
| **Included in AI Pro?** | ✅ Yes — daily quota included |
| **Quota reset** | Daily — **resets ~17:21 today** |
| **Current state** | 🔴 **QUOTA HIT** |

### Best used for:
- Location identity sheets (glass meeting room, open-plan, canteen)
- Character style frame approvals before committing to video
- Storyboard gate-check panels per shot (S01–S19)
- Poster / thumbnail assets

---

## 🎬 TOOL 2 — Veo Video Generation
**Current model**: `veo-3.1` (Veo 2 was deprecated June 2026 — use Veo 3.1 now)  
**Access via**: [aistudio.google.com](https://aistudio.google.com) → model dropdown → select Veo 3.1

> ⚠️ **Important**: Veo 2 (`veo-2.0-generate-001`) was shut down June 30, 2026. Use **Veo 3.1** instead — it's better and is what your subscription now gives you.

| Capability | Detail |
| :--- | :--- |
| **What it generates** | Short cinematic video clips from text prompts or image references |
| **Resolution** | 720p |
| **Clip duration** | **5–8 seconds** per clip (sweet spot — generates best at 8s) |
| **Input modalities** | Text-to-video · Image-to-video (image conditioning up to 20MB) |
| **Aspect ratios** | 16:9 · 9:16 |
| **Native audio** | ✅ Yes on Veo 3.1 — can generate ambient sound, SFX, and dialogue audio natively |
| **Outputs per prompt** | Up to 4 video variants per generation |
| **Included in AI Pro?** | ✅ Yes — monthly usage cap, Google notifies when approaching limit |
| **Quota reset** | Monthly cap — also resets **daily** for daily allowance |
| **Current state** | 🔴 **QUOTA HIT** (daily) |

### Best used for:
- Each of the 19 featurette micro-clips (S01–S19) — one at a time, gate-checked
- Opening title sequence clips (SHOT 01–05)
- 8 seconds is the target duration per clip for best quality

### ⚡ Veo 3.1 vs Veo 2 for this project:
| Feature | Veo 2 (dead) | Veo 3.1 (use this) |
| :--- | :--- | :--- |
| Native audio | ❌ | ✅ |
| Duration | 5–8s | 5–8s |
| Resolution | 720p | 720p |
| Image conditioning | ✅ | ✅ |
| Available | ❌ Shut down June 2026 | ✅ Active |

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
| 🔴 Gemini Flash Image | QUOTA HIT | **~17:21 today** |
| 🔴 Veo 3.1 Video | QUOTA HIT | Daily + monthly cap |
| 🟢 Qwen3-TTS (Local) | AVAILABLE | No quota |
| 🟢 Gemini Text / CLI | AVAILABLE | No quota |
| 🟢 Git / GitHub | AVAILABLE | No limit |

---

## 📋 Generation Queue (Auto-starts at ~17:21)

**Do these IN ORDER — each feeds the next:**

| # | Task | Tool | Output |
|---|------|------|--------|
| 1 | Glass Meeting Room location sheet | Gemini Flash Image | `location-refs/glass_meeting_room_location_sheet.jpg` |
| 2 | Open-Plan Office location sheet | Gemini Flash Image | `location-refs/open_plan_office_location_sheet.jpg` |
| 3 | Canteen location sheet | Gemini Flash Image | `location-refs/canteen_location_sheet.jpg` |
| 4 | S01 still — gate check | Gemini Flash Image | `clips/S01_office_establishing_still.jpg` |
| 5–22 | S02–S19 stills — gate check each | Gemini Flash Image | `clips/S##_[name]_still.jpg` |
| 23 | All stills approved → start video | **Veo 3.1** via AI Studio | `clips/S01_office_establishing.mp4` … |
