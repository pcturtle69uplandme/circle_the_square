# Scene 1 — MiniMax-H3 Generation Tracker

Photoreal Ref2VA pipeline (Q4_K denoiser, auto-fit backend, 56 frames / 24fps / 864x480).
References used per clip noted; QA checked against: (1) face/identity match to character
sheet, (2) wardrobe match, (3) location/set match, (4) no artifacts/garbling, (5) action
matches script beat.

| # | Frame | Clip | Refs | Status | Notes |
|---|-------|------|------|--------|-------|
| 1 | F01 | 1/1 | Jan, Christina, Office | ✅ pass (wide) | office skyline fixed (Shard removed); faces small — normal for a wide establishing shot |
| 2 | F02 | 1/2 | Jan, Office | ⚠️ revisit | identity/location/face all good, but see QA Rule 1 — likely also rushed once compared to c2 |
| 3 | F02 | 2/2 | Jan, Office | ⚠️ revisit | dialogue sounds rushed (14 words in 2.33s) — QA Rule 1; also background drift vs c1 — QA Rule 4 |
| 4 | F03 | 1/2 | Christina, Office | ⬜ pending | |
| 5 | F03 | 2/2 | Christina, Office | ⬜ pending | |
| 6 | F04 | 1/1 | Jan, Office | ⬜ pending | |
| 7 | F05 | 1/3 | Christina, Office | ⬜ pending | |
| 8 | F05 | 2/3 | Christina, Office | ⬜ pending | |
| 9 | F05 | 3/3 | Christina, Office | ⬜ pending | |
| 10 | F06a | 1/2 | Jan, Office | ⬜ pending | |
| 11 | F06a | 2/2 | Jan, Office | ⬜ pending | |
| 12 | F06b | 1/2 | Jan, Office | ⬜ pending | |
| 13 | F06b | 2/2 | Jan, Office | ⬜ pending | |
| 14 | F07 | 1/2 | Christina, Office | ⬜ pending | |
| 15 | F07 | 2/2 | Christina, Office | ⬜ pending | |
| 16 | F08 | 1/1 | Jan, Office | ⬜ pending | |
| 17 | F09 | 1/1 | Christina, Office | ⬜ pending | |
| 18 | F10 | 1/1 | Jan, Office | ⬜ pending | |
| 19 | F11 | 1/1 | Christina, Office | ⬜ pending | |
| 20 | F12 | 1/2 | Jan, Office | ⬜ pending | |
| 21 | F12 | 2/2 | Jan, Office | ⬜ pending | |
| 22 | F13 | 1/1 | Christina, Office | ⬜ pending | |
| 23 | F14 | 1/2 | Jan, Office | ⬜ pending | |
| 24 | F14 | 2/2 | Jan, Office | ⬜ pending | |
| 25 | F15 | 1/1 | Christina, Office | ⬜ pending | |
| 26 | F16 | 1/2 | Jan, Office | ⬜ pending | |
| 27 | F16 | 2/2 | Jan, Office | ⬜ pending | |
| 28 | F17 | 1/1 | Christina, Office | ⬜ pending | |
| 29 | F18 | 1/1 | Jan, Office | ⬜ pending | |
| 30 | F19 | 1/1 | Jan, Office | ✅ done (earlier test) | see character-refs/stencils + minimax-h3/output |
| 31 | F20 | 1/1 | Jan, Sharon, Office | ⬜ pending | need Sharon front-panel ref |
| 32 | F21 | 1/1 | Sharon, Jan, Office | ⬜ pending | |
| 33 | F22 | 1/1 | Jan, Office | ⬜ pending | |
| 34 | F23 | 1/1 | Sharon, Office | ⬜ pending | |
| 35 | F24 | 1/2 | Jan, Sharon, Office | ⬜ pending | |
| 36 | F24 | 2/2 | Jan, Sharon, Office | ⬜ pending | |
| 37 | F25 | 1/1 | Sharon, Office | ⬜ pending | |
| 38 | F26a | 1/1 | Jan, Office | ⬜ pending | |
| 39 | F26b | 1/1 | Jan, Office | ⬜ pending | |

**Total: 39 clips.** Started 2026-08-25. **Paused after F02 clip 2** (user instruction) —
F01 and both F02 clips are provisional and will be regenerated from scratch on restart, per
the restart plan below. Nothing after F02 has been attempted yet.

## Restart plan — do this before generating F01 again

1. Fix `refs/jan_office_location_fixed.png`: add venetian blinds to the windows (raised/open
   position, since Scene 1 opens with them up and F26a is the payoff of lowering them). Draft
   edit prompt already prepared (Kontext-dev, office reference as input) — not yet run.
2. Re-check `MASTER_PRODUCTION_MANUAL.md` §8 prop table against the *full* script (not just
   Scene 1) for any other fixtures introduced late in a location that are missing from that
   location's reference image. Add venetian blinds to that table as a documented fix once
   confirmed, so this doesn't get missed again on other locations (canteen chair/window,
   corridor, etc.).
3. Re-plan clip lengths against QA Rule 1 below (natural dialogue pace, not rushed) — the
   original 39-clip estimate under-counted how many clips long lines actually need at 56
   frames/2.33s per clip. Expect the real count to be higher.
4. Only then regenerate F01 clip 1, then F02 clips, then continue forward — do not resume
   mid-list without redoing these two.

## QA Rules (added 2026-08-25)

1. **Dialogue pacing must not be rushed.** Original per-clip word budgets assumed too much
   speech fits in 56 frames (2.33s) — F02 clip 2 (14 words) already sounds rushed. Natural
   conversational pace is ~2.2-2.5 words/sec, so a 2.33s clip comfortably holds only ~5-6
   words. Every clip's line length must be checked against this before generating, and split
   further if needed rather than accepting sped-up delivery.
2. **Extending clip length beyond 56 frames in a single pass is VRAM-limited and not worth
   fighting directly** — 96 frames pushed VRAM to ~15.8/16.4GB and thrashed. Tested
   2026-08-26: `--max-vram`/`--stream-layers` to force the text encoder onto GPU does NOT
   help reach longer single-pass clips (it's slower and still OOMs later — see
   `minimax-h3-pipeline/README.md` hardware constraints section for the full finding). For
   the current pass, prefer more (shorter, correctly-paced) 56-frame clips over fewer rushed
   ones. **User's acceptance boundary (2026-08-26): a 10-second clip taking up to 30 minutes
   is fine** — so the real path to longer output is chunked generation: multiple 56-frame
   Ref2VA segments, each seeded from the last frame of the previous segment as a reference
   image for continuity, concatenated afterward. Built and validated 2026-08-26 as
   `minimax-h3-pipeline/chain_clips.py` — 5-chunk pipeline test (generic scene, not a real
   shot) produced 280 frames / 11.7s in ~19-20min, well inside the 30min budget. Cut points
   are seamless, but there's a real compounding framing/zoom-in drift within each chunk's own
   generation — see the README's "Chained/chunked generation" section for the full finding
   and mitigation ideas before using this on a real shot with more than 2-3 chunks.
   Also added: EasyCache + a turbo checkpoint (both in the README's hardware-constraints
   section) cut per-clip time from ~5.3-5.5min to ~3.4min — both now the default in
   `gen_clip.py`/`chain_clips.py`, so re-estimate clip counts/timing against the new ~3.4min
   figure, not the original ~5min one.
3. **Location references must be scanned against the FULL script, not just the current
   scene's earliest beat**, before locking them in. The office reference was missing venetian
   blinds needed for F26a ("Jan yanks the blinds shut") because nothing scanned forward for
   props/fixtures introduced later in the same location. Cross-check `MASTER_PRODUCTION_MANUAL.md`
   §8 (Costume & Prop Master Inventory) against every location reference before the first clip
   of a scene, and add anything missing to that table.
4. **Clips sharing one reference image must still be checked against each other**, not just
   against the reference — F02 clip 1 and clip 2 (same shot, same ref) already drifted on
   shelving contents and a background glass element. Flag any such drift during QA even when
   the reference match is individually fine.
