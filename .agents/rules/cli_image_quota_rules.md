# 🖼️ CLI IMAGE GENERATION QUOTA & WORKFLOW RULES

## 0. MANDATORY: CLI ONLY — NEVER THE BROWSER
- **All image generation runs through the CLI `generate_image` tool. No exceptions.**
- **Do NOT propose, open, or route work to a browser** — not Google AI Studio, not `aistudio.google.com`, not any web UI. The user does not do any work in the browser.
- **Do NOT suggest browser-based workarounds** when CLI quota is exhausted. The correct response to exhaustion is to **wait for the window to clear**, not to switch tools.
- **Rationale:** the CLI holds character consistency across frames within a session. That consistency is the whole point of the storyboard, and it is worth waiting out a quota window for.
- **This rule overrides every other workflow suggestion in this repo**, including any older AI Studio guidance in `MASTER_STORYBOARD_SESSION_PROMPTS.md` or `TOOLS_AND_SCRIPTS_GUIDE.html`.

## 1. CLI Tool Limits (`generate_image`)
- **Capacity Ceiling:** Maximum **12 image generations** per rolling **4-hour window**.
- **Enforcement:** If a `429 RESOURCE_EXHAUSTED` error is received from `cloudcode-pa.googleapis.com`, stop CLI generations immediately and notify the user of the exact reset timestamp.
- **Tracking:** Maintain a count of generated images per session so the user is warned when approaching 10/12 images.
- **On exhaustion:** report the reset time and pause. Resume on the CLI once capacity returns. Never fall back to another tool.

## 2. Session Consistency & Batch Pacing
- **Single-Session Consistency:** For multi-frame storyboards (e.g. 64 frames), generate through one continuous CLI session so character memory carries between frames.
- **Pacing:** at 12 images per rolling 4-hour window, a full 64-frame board takes roughly **6 windows (~20+ hours)**. Plan in batches of 12, in frame order, and record where each batch stopped so the next one resumes cleanly.
- **Character Tags:** All prompts must include explicit `@tag` character names (`@jan`, `@christina`, `@sharon`, `@chris`, `@rick`) and physical anchors.
- **Output Storage:** Save all generated frames into `circle_the_square/storyboard-frames/Fxx.jpg` to feed `storyboard_slideshow.html`.

## 3. Prohibited generation routes
- ❌ Google AI Studio / any browser UI
- ❌ `generate_all_fal_storyboard_frames.py` and the fal.ai batch route — text-only conditioning, produced a board scrapped for character drift (`becdfc8`)
- ✅ CLI `generate_image` only
