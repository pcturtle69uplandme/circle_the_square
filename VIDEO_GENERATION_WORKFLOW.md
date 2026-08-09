# 🎬 CIRCLE THE SQUARE — VIDEO GENERATION WORKFLOW
> **How to Generate the 19 Shot Clips Using Your Subscription**  
> **No API keys. No billing. Subscription only.**

---

## 🚦 WHEN QUOTA HAS RESET — Your Workflow

> Veo 2 quotas on Google One AI Premium / AI Studio typically reset **daily**.  
> If you hit the limit, wait until the next day and continue from where you left off.

---

## 🛠️ METHOD 1 — AI Studio Web UI (Recommended)

This is the correct subscription-based route. No API key required.

### Steps for Each Shot

1. **Open**: [aistudio.google.com](https://aistudio.google.com) — sign in with your Google account
2. **Select**: `Veo 2` or `Veo 3` from the model dropdown
3. **Open**: [`featurette_prompt_engine.md`](file:///C:/kontitemp/ai/circle_the_square/featurette_prompt_engine.md) — navigate to the shot you're on (e.g. S01)
4. **Paste**: The `VIDEO PROMPT` block for that shot into AI Studio's prompt field
5. **Upload**: The 2–3 reference images listed for that shot as image conditioning inputs
6. **Set duration**: 5–10 seconds as specified per shot
7. **Generate** — wait ~2–5 minutes
8. **Download** the `.mp4` — save to:  
   📁 `C:\kontitemp\ai\circle_the_square\clips\S01_office_establishing.mp4` (adjust number per shot)
9. **Watch** the clip — run through the **GATE CHECK** in the prompt engine
10. ✅ Approved → move to next shot | ❌ Rejected → tweak prompt → regenerate

---

## 🛠️ METHOD 2 — Antigravity CLI Image Generation (For Stills / Style Frames)

When quota for video is exhausted, I can generate **photorealistic still frames** directly here in the CLI using your subscription — these work as:
- **Style reference frames** to check character + location looks before committing to video
- **Storyboard panels** for director approval
- **Thumbnail / poster assets**

Just say: *"generate S01 as a still frame"* and I'll use the `generate_image` tool directly.

---

## 📋 SHOT QUEUE — Pick Up Where You Left Off

Mark each shot below as you go:

| Shot | Name | Duration | Clip Filename | Status |
|------|------|----------|--------------|--------|
| S01 | Jan's Office — Establishing Wide | 6s | `S01_office_establishing.mp4` | ⬜ |
| S02 | Jan's Office — MCU Jan Pompous | 8s | `S02_jan_pompous_mcu.mp4` | ⬜ |
| S03 | Jan's Office — OTS Christina Deadpan | 6s | `S03_christina_deadpan_ots.mp4` | ⬜ |
| S04 | Jan's Office — CU Jan Stress Build | 5s | `S04_jan_stress_build_cu.mp4` | ⬜ |
| S05 | Jan's Office — Shirtless Arrow + Sharon | 8s | `S05_shirtless_arrow_sharon.mp4` | ⬜ |
| S06 | Jan's Office — Sharon Unbothered MCU | 4s | `S06_sharon_unbothered_mcu.mp4` | ⬜ |
| S07 | Jan's Office — Jan Locks Blinds | 5s | `S07_jan_locks_blinds.mp4` | ⬜ |
| S08 | Corridor — Sharon Exits Dishevelled | 8s | `S08_sharon_exits_dishevelled.mp4` | ⬜ |
| S09 | Corridor — Chris & Rick 2-Shot | 6s | `S09_chris_rick_2shot.mp4` | ⬜ |
| S10 | Open-Plan — Jan Announces Inception | 8s | `S10_jan_inception_wide.mp4` | ⬜ |
| S11 | Open-Plan — Jan £50k MCU | 8s | `S11_jan_50k_mcu.mp4` | ⬜ |
| S12 | Open-Plan — Crowd Reaction Cuts | 6s | `S12_crowd_reaction.mp4` | ⬜ |
| S13 | Canteen — Establishing Wide | 6s | `S13_canteen_establishing.mp4` | ⬜ |
| S14 | Canteen — Jan Discovers Empty Tray | 8s | `S14_jan_discovers_no_pastries.mp4` | ⬜ |
| S15 | Canteen — Plates Crash & Chair Smash | 10s | `S15_canteen_meltdown_plates_chair.mp4` | ⬜ |
| S16 | Canteen — Rick Draws Taser | 5s | `S16_rick_draws_taser.mp4` | ⬜ |
| S17 | Canteen — INSERT Taser Flash | 3s | `S17_taser_insert_flash.mp4` | ⬜ |
| S18 | Canteen — Jan Slumps | 5s | `S18_jan_slumps.mp4` | ⬜ |
| S19 | Canteen — Have You Killed Him? | 8s | `S19_have_you_killed_him.mp4` | ⬜ |

> Status: ⬜ PENDING · ✅ APPROVED · ❌ REJECTED · 🔄 REGENERATING

---

## 📁 All Clips Save To

**Filename**: `clips\` folder  
**Full Path**: [`C:\kontitemp\ai\circle_the_square\clips\`](file:///C:/kontitemp/ai/circle_the_square/clips/)

---

## ⏱️ QUOTA RESET INFO

| Platform | Quota Reset |
|----------|------------|
| Google AI Studio (subscription) | Daily — resets at midnight Pacific |
| Veo 2 free tier | 2 videos/day |
| Google One AI Premium | Higher limits — check [aistudio.google.com](https://aistudio.google.com) usage tab |

---

## 📎 Key Files

| File | Path |
|------|------|
| Shot Prompt Engine | [`C:\kontitemp\ai\circle_the_square\featurette_prompt_engine.md`](file:///C:/kontitemp/ai/circle_the_square/featurette_prompt_engine.md) |
| Shot List | [`C:\kontitemp\ai\circle_the_square\featurette_shot_list.md`](file:///C:/kontitemp/ai/circle_the_square/featurette_shot_list.md) |
| Clips Output Folder | [`C:\kontitemp\ai\circle_the_square\clips\`](file:///C:/kontitemp/ai/circle_the_square/clips/) |
