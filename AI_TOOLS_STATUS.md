# ⚡ AI TOOLS — QUICK STATUS REFERENCE

> **Last Updated**: 2026-08-08 16:27  
> Update the status column whenever a quota hits or resets.

---

| Tool | What It Does | How to Access | Quota / Limit | Current State |
| :--- | :--- | :--- | :--- | :--- |
| **Gemini Flash Image** | Photorealistic still frames, style frames, storyboard panels, location sheets, character sheets | Antigravity CLI — just ask me directly | Daily quota. **Resets ~17:21 today** | 🔴 QUOTA HIT |
| **Veo 2 Video** | 5–10 second cinematic video clips per shot | AI Studio web UI → [aistudio.google.com](https://aistudio.google.com) — subscription, no API key | Daily quota. Resets **midnight Pacific** | 🔴 QUOTA HIT |
| **Qwen3-TTS (Local GPU)** | Character dialogue voice audio `.wav` files | ComfyUI locally — `C:\ai\ComfyUI\` | No quota — runs on your GPU | 🟢 AVAILABLE |
| **Gemini Text / Code** | Planning, scripting, prompts, documents, git | Antigravity CLI — this conversation | Very high daily limit | 🟢 AVAILABLE |
| **Git / GitHub** | Version control, push to `main` | CLI — runs locally | No limit | 🟢 AVAILABLE |

---

## 🔄 Status Key
| Icon | Meaning |
| :--- | :--- |
| 🟢 AVAILABLE | Ready to use right now |
| 🟡 LIMITED | Working but approaching quota |
| 🔴 QUOTA HIT | Exhausted — wait for reset |
| ⏸️ PAUSED | Deliberately not in use |

---

## 📋 Generation Queue (When Quota Resets at ~17:21)

**Do these IN ORDER — each feeds the next:**

| # | Task | Tool | Output File |
|---|------|------|------------|
| 1 | Generate Glass Meeting Room location sheet | Gemini Flash Image | `location-refs/glass_meeting_room_location_sheet.jpg` |
| 2 | Generate Open-Plan Office location sheet | Gemini Flash Image | `location-refs/open_plan_office_location_sheet.jpg` |
| 3 | Generate Canteen location sheet | Gemini Flash Image | `location-refs/canteen_location_sheet.jpg` |
| 4 | Generate S01 still frame | Gemini Flash Image | `clips/S01_office_establishing_still.jpg` |
| 5 | Gate check S01 → Generate S02 | Gemini Flash Image | `clips/S02_jan_pompous_mcu_still.jpg` |
| … | Continue S03–S19 | Gemini Flash Image | `clips/S##_[name]_still.jpg` |

> Once stills for all 19 shots are approved → move to **Veo 2 video generation** via AI Studio.
