# Scene 1 — Higgsfield 2K Video Tracker

> ⚠️ **SUPERSEDED DOCUMENT (rewrite in progress).** This file used to track Scene 1
> video through the **local MiniMax-H3 Ref2VA pipeline** (`minimax-h3-pipeline/`).
> That route is **paused, not deleted** — see `HANDOVER.md` §9 for full history.
> The **adopted Scene 1 video route is now Higgsfield 2K only** (Higgsfield `MiniMax H3`
> for dialogue close-ups, Higgsfield `Kling v3.0` for bridging/continuation shots) —
> see `HANDOVER.md` §10 and `video-tests/` for ground truth.
>
> **Do NOT route any Scene 1 video through the local MiniMax-H3, local Wan 2.2,
> Qwen3-TTS, or MuseTalk pipelines.** Those are fallbacks only, and per the user's
> 2026-08-29 directive they are not in the active path.
>
> This file is being rewritten to track the **Higgsfield 2K cut** instead. The legacy
> rows below the horizontal rule are kept for archaeology only; ignore them when
> planning new work.

---

## 1. Engine routing (Higgsfield 2K only)

| Shot type | Engine | Resolution | Typical cost | Notes |
|---|---|---|---|---|
| 2K stills / reference plates | `Nano Banana 2` (Higgsfield) | 2560×1440 | 1.5 credits/shot | Master-edit chaining for multi-angle coverage (see `generate-location-coverage.js`) |
| Dialogue close-ups | `MiniMax H3` (Higgsfield cloud) | **2560×1440** | 10 credits/short clip, 30 credits/15s | Primary video path for Scene 1. ⚠️ **Combine consecutive beats to fill up to 15s per clip, don't generate one beat per call** — see `.agents/rules/clip_duration_rules.md` |
| Bridging / continuation shots | ~~`Kling v3.0`~~ **use `MiniMax H3` instead** | 2560×1440 | same as dialogue row | **Superseded 2026-08-29 evening.** Kling was only picked because MiniMax's `--image-references` couldn't seed an exact continuation frame — `--start-image` fixes that at full 2K (see `.agents/rules/location_continuity_rules.md`), so there's no longer a reason to drop to Kling's 720p for a bridging shot. Keep Kling only as a fallback if `--start-image` continuity genuinely fails on a specific shot. |

**Budget (last known, 2026-08-29 21:32 BST):** 562.79 credits (includes a 22cr loss to a failed 503 job, retried successfully, plus 62cr across three F07/F08 fix regens — see §3 notes) remaining of an original
1208.5 + plan allotment. ~372 credits spent in ~4.5 hours on this session. Per-beat
costs noted in §3.

**Local pipelines — DO NOT USE for Scene 1 video:**
- `minimax-h3-pipeline/` (local MiniMax-H3, Q4_K + EasyCache) — paused
- `wan22-pipeline/` (local Wan 2.2 TI2V-5B) — paused, `output/` empty
- Qwen3-TTS voice cloning — paused
- MuseTalk lip-sync — paused

Available as fallbacks if the Higgsfield credit budget runs low, but **not** the
adopted path.

---

## 2. Reference asset state (as of 2026-08-29)

### Characters — 12-shot photoreal reference set per character
Path: `character-refs/higgsfield/<slug>/` (12 shots: front, 3/4, profile, slight up/down,
neutral + in-character expression, harsh + soft lighting, neutral + characteristic full body)

| Character | Status | Manifest |
|---|---|---|
| Jan | ✅ done | `higgsfield-tools/cast-refs-manifest.json` |
| Christina | ✅ done | same |
| Sharon | ✅ done | same |
| Chris | ✅ done | same |
| Rick | ✅ done | same |
| Gemma | ✅ done | same |
| Maureen | ✅ done | same |
| Trevor | ✅ done | same |

4 script characters without Higgsfield refs yet: **Priya, Barbara, Dev, Tomasz**
(supporting cast, may or may not appear in Scene 1 — confirm against
`featurette_storyboard_image_prompts.md` script before generating).

### Locations — multi-angle coverage
Path: `location-refs/higgsfield/coverage/<slug>/`

| Location | Angles | Status |
|---|---|---|
| `jan_office` | 15 (master_wide + 7 chained + 7 bonus) | ✅ all done |
| `goldfish_meeting_room` | 8 (master_wide + 7 chained) | ✅ all done |
| `jan_office_corridor` | 1 (master_wide only) | 🔶 master done, chained angles pending |

`jan_office_corridor` chained angles to fill (defined in `location-coverage-manifest.json`):
`corridor_view`, `door_closed`, `table_head`, `table_reverse`, `table_side`,
`decal_closeup`, `openplan_context_wide`. Retry face-bearing angles with `--image`
chaining off the master + tighter identity-locking prompts (initial attempts were
policy-blocked on identity-protected faces — see HANDOVER §10 addendum).

---

## 3. Per-beat plan (Scene 1, F01–F26b)

Storyboard stills F01–F21 are **approved as cartoon keyframes** in
`storyboard-frames/F01.jpg` … `F21.jpg` from the pre-pivot Google Flow track
(verified, committed). F22–F26b are the only stills not yet approved.

The **video** is a separate track and is being generated from scratch on Higgsfield.
Video planning below: per beat, pick the engine based on the shot type, list estimated
cost, and reference the existing approved still + matching location coverage angle.

> **Re-plan pending.** This table is the proposed re-plan based on the HANDOVER §10
> routing. Confirm beat-by-beat before generating — some beats (e.g. wide establishing
> shots) will need re-cuts that don't match the approved cartoon stills.

| # | Frame | Beat | Engine | Est. cost | Refs (char + loc angle) | Still approved? | Video status |
|---|-------|------|--------|-----------|-------------------------|-----------------|--------------|
| 1 | F01 | Wide establishing — Christina enters, greets Jan | `MiniMax H3` 2K (30 cr, 15s) | 30 | Jan + Christina, `jan_office_master_wide` | ✅ (cartoon, F01.jpg) | ✅ covered by `video-tests/01_f01-f02_opening_greeting_minimax_h3.mp4` (F01+F02 combined, 2026-08-29) |
| 2 | F02 | Jan sighs — "Barely..." | (combined into row 1's 15s clip) | — | Jan, `jan_office_desk_front` or `_master_wide` | ✅ (cartoon, F02.jpg) | ✅ covered by row 1's clip |
| 3 | F03 | Christina pitches — "I have an idea..." | `MiniMax H3` 2K (22 cr actual, 11.5s, combined with F04) | 22 | Christina + Jan, `--start-image` seeded off beat-1's exact last frame (see gotcha below — NOT `--image-references`) | ✅ (cartoon, F03.jpg) | ✅ `video-tests/02_f03-f04_pitch_and_listening_minimax_h3.mp4` (2026-08-29) — combined with F04 |
| 3b | — | (superseded attempt, kept for reference) | — | — | — | — | ⚠️ `video-tests/archive/f03_standalone_wrong_seed_minimax_h3.mp4` — seeded via `--image-references` instead of `--start-image`; caused a visible camera jump at the join. Not used in the cut. |
| 4 | F04 | Jan — "I'm listening." | (combined into row 3's clip) | — | Jan, `jan_office_desk_front` | ✅ (cartoon, F04.jpg) | ✅ covered by row 3's clip |
| 5 | F05 | Christina explains breakfast-meeting concept | `MiniMax H3` 2K (24+18 cr actual, split across 2 clips — full line ~47 words, too long for one 15s clip) | 42 | Christina, `--start-image` chained off beat-2's exact last frame, then off part1's last frame | ✅ (cartoon, F05.jpg) | ✅ `video-tests/03a_f05_breakfast_pitch_part1_minimax_h3.mp4` (12.25s) + `video-tests/03b_f05_breakfast_pitch_part2_minimax_h3.mp4` (9.42s) (2026-08-29) |
| 6 | F06a | Jan enthused, steepled fingers | `MiniMax H3` 2K (30 cr actual, 14.4s — one long Jan speech split across F06a/F06b) | 30 | Jan + Christina, `--start-image` chained off beat-03b's exact last frame | ✅ (cartoon, F06a.jpg) | ✅ `video-tests/04a_f06a_jan_enthused_part1_minimax_h3.mp4` (2026-08-29), Whisper-verified verbatim |
| 7 | F06b | Jan gesturing, MBA name-drop | `MiniMax H3` 2K (14 cr actual, 7.3s) | 14 | Jan + Christina, `--start-image` chained off F06a's exact last frame | ✅ (cartoon, F06b.jpg) | ✅ `video-tests/04b_f06b_jan_mba_punchline_minimax_h3.mp4` (2026-08-29), Whisper-verified verbatim |
| 8 | F07 | Christina deadpan — "Diminishing returns..." | `MiniMax H3` 2K (28 cr actual, 14.4s — regenerated a second time 2026-08-29 evening to add a walk-in preamble, see continuity note below) | 28 | Christina + Jan, `--image-references` (jan_office_desk_reverse + identity sheets, NOT `--start-image` — intentional cut, resets drift depth to 0) | ✅ (cartoon, F07.jpg) | ✅ `video-tests/05a_f07_reverse_angle_part1_minimax_h3.mp4` (regenerated 2026-08-29), Whisper-verified verbatim |
| 9 | F08 | Jan — "Great. Make it so." | (combined into F07's part2 clip, 3rd regen 14 cr actual, 7.3s) | 14 | Jan + Christina, `--start-image` chained off the regenerated F07 part1's exact last frame | ✅ (cartoon, F08.jpg) | ✅ `video-tests/05b_f07-f08_reverse_angle_part2_minimax_h3.mp4` (regenerated again 2026-08-29), Whisper-verified verbatim |

> ⚠️ **Continuity fix 2026-08-29 evening — F07/F08 regenerated a 2nd time.** The first `05a` take
> (drift-reset cut described above) placed Christina already standing across the desk with no
> on-screen motion connecting it to `04b`'s last frame, where she'd been standing beside Jan at
> the desk's near corner — read as an instant teleport, and the shift to a colder-lit wall behind
> her landed as a tone jump too. Fixed by re-running F07 with the same `image_references` (no new
> asset) but a prompt that adds a walk-in preamble: she visibly steps back from Jan, crosses to the
> visitor chair, and settles before her line. `05b` was then also regenerated (`--start-image` off
> the new `05a`'s last frame) since it had been chained off the *old* `05a`'s last frame and would
> otherwise pop at that internal join. Old takes kept as
> `video-tests/archive/05a_f07_reverse_angle_part1_teleport_minimax_h3.mp4` and
> `.../05b_f07-f08_reverse_angle_part2_teleport_minimax_h3.mp4`.
>
> **2nd fix, same evening — `05b` regenerated again.** That 2nd take of `05b` reopened with
> Christina restating her whole "diminishing returns" line before Jan's response — a straight
> repeat of what `05a` had just delivered a moment earlier, audible/visible as a duplicate once
> the two clips play back to back. Also, per a user note: "Great. Make it so." is Picard's line
> from *Star Trek: TNG* — and the script's very next beats (F09-F11) are Jan asking Christina if
> she's seen it and her not getting the reference, so the line is a deliberate setup, not a throwaway.
> Fixed both at once (required new footage anyway, so a plain trim of the old take wasn't enough):
> regenerated `05b` a 3rd time, same `--start-image` off `05a`'s last frame, this time with no
> restated dialogue (a silent beat, then straight to Jan's line) and a prompt directing Jan to
> deliver it with a self-satisfied point-and-smile, playing up the reference, while Christina's
> expression doesn't flicker. Old (repeat-line) take archived as
> `video-tests/archive/05b_f07-f08_reverse_angle_part2_repeatline_minimax_h3.mp4`.
> `scene1_stitched_preview.mp4` rebuilt (91.66s). Balance after all three regens: 562.79 credits.
| 10 | F09 | Christina confused — "I am sorry, what?" | `MiniMax H3` 2K, combined with F10+F11 | TBD | Christina + Jan, `--start-image` chained forward from the reset point (depth 2 from reset) | ✅ (cartoon, F09.jpg) | ⬜ not started (regen) |
| 11 | F10 | Jan — Star Trek reference | (combined into F09's clip) | — | Jan, `jan_office_desk_front` | ✅ (cartoon, F10.jpg) | ⬜ not started (regen) |
| 12 | F11 | Christina — "Shockingly no." | (combined into F09's clip) | — | Christina, `jan_office_desk_front` | ✅ (cartoon, F11.jpg) | ⬜ not started (regen) |

> ⚠️ **Generational drift discovered 2026-08-29, ~20:35 BST — F07/F08/F09-11 regenerating.**
> Chaining `--start-image` off an ever-more-derivative frame compounds: measured brightness
> dropping and shadow-crushing roughly doubling every ~4 generations deep (depth 1 → 17.8%
> near-black pixels, depth 4 → 27.8%, depth 8 → 36.8% — see the conversation for the
> full analysis). The original `05a`/`05b`/`06` clips (depths 6-8) are archived in
> `video-tests/archive/` as `*_drifted_minimax_h3.mp4`, not deleted, but not used in the cut.
> **Fix**: reset the chain periodically by cutting to a fresh angle seeded from an
> undegraded location reference plate (`--image-references`, not `--start-image`) instead of
> always continuing from the previous clip's last frame — doubles as legitimate
> shot/reverse-shot cinematography instead of one 100+ second static two-shot. F07 is being
> regenerated from `jan_office_desk_reverse.png` (an over-the-shoulder angle favoring
> Christina) as this reset point. Plan to reset again periodically (e.g. every ~6-8 beats)
> rather than chaining all the way to F20's already-planned reset.
| 13 | F12 | Jan dismisses — "Fine, just make it happen..." | `MiniMax H3` 2K (10 cr) | 10 | Jan, `jan_office_desk_front` | ✅ (cartoon, F12.jpg) | ⬜ not started |
| 14 | F13 | Christina — "poorly rehearsed presentations?" | `MiniMax H3` 2K (10 cr) | 10 | Christina, `jan_office_desk_front` | ✅ (cartoon, F13.jpg) | ⬜ not started |
| 15 | F14 | Jan offended — "MBA from the University of --" | `MiniMax H3` 2K (10 cr) | 10 | Jan, `jan_office_desk_front` | ✅ (cartoon, F14.jpg) | ⬜ not started |
| 16 | F15 | Christina cuts in — "Made Up Place?" | `MiniMax H3` 2K (10 cr) | 10 | Christina, `jan_office_desk_front` | ✅ (cartoon, F15.jpg) | ⬜ not started |
| 17 | F16 | Jan screams — "GET OUT NOW YOU STUPID COW!" | `MiniMax H3` 2K (10 cr) | 10 | Jan, `jan_office_desk_front` | ✅ (cartoon, F16.jpg) | ⬜ not started |
| 18 | F17 | Christina exits calmly, door shuts | `MiniMax H3` 2K (~10-15 cr est.) — **routing corrected**, was `Kling v3.0` 720p; that was only needed before `--start-image` was discovered (see below) | ~12 | Christina, `--start-image` chained off F16's exact last frame | ✅ (cartoon, F17.jpg) | ⬜ not started |
| 19 | F18 | Jan unbuttons shirt, flustered/sweating | `MiniMax H3` 2K (10 cr) | 10 | Jan, `jan_office_master_wide` | ✅ (cartoon, F18.jpg) | ⬜ not started |
| 20 | F19 | Jan removes shirt, arrow revealed | `MiniMax H3` 2K (10 cr) | 10 | Jan, `jan_office_seating_area` | ✅ (cartoon, F19.jpg) | ⬜ not started |
| 21 | F20 | Sharon enters unannounced — Jan reacts | `MiniMax H3` 2K (10 cr) | 10 | Jan + Sharon, `jan_office_door_entrance` | ✅ (cartoon, F20.jpg) | ⬜ not started |
| 22 | F21 | Sharon glances at the arrow | `MiniMax H3` 2K (10 cr) | 10 | Sharon, `jan_office_seating_area` | ✅ (cartoon, F21.jpg) | ⬜ not started |
| 23 | F22 | Jan frozen, mortified | `MiniMax H3` 2K (10 cr) | 10 | Jan, `jan_office_seating_area` | ⬜ still pending | ⬜ not started |
| 24 | F23 | Sharon — "breakfast meetings now." | `MiniMax H3` 2K (10 cr) | 10 | Sharon, `jan_office_seating_area` | ⬜ still pending | ⬜ not started |
| 25 | F24 | Jan brushes her off | `MiniMax H3` 2K (10 cr) | 10 | Jan, `jan_office_master_wide` | ⬜ still pending | ⬜ not started |
| 26 | F25 | Sharon — "I have needs too Jan..." | `MiniMax H3` 2K (10 cr) | 10 | Sharon, `jan_office_seating_area` | ⬜ still pending | ⬜ not started |
| 27 | F26a | Jan yanks blinds shut | `MiniMax H3` 2K (10 cr) | 10 | Jan, `jan_office_window_side` | ⬜ still pending | ⬜ not started |
| 28 | F26b | Jan locks the door | `MiniMax H3` 2K (~10-15 cr est.) — **routing corrected**, was `Kling v3.0` 720p, same reason as F17 | ~12 | Jan, `--start-image` chained off F26a's exact last frame | ⬜ still pending | ⬜ not started |

**Estimated total: ~290 credits** (27 × 10 + 1 × 15 for F05) for `MiniMax H3`,
plus ~40 credits for the 2 `Kling v3.0` bridging shots. **~330 credits for full Scene 1.**

This is **well within** the remaining 898.9-credit budget. ⚠️ **Recalc before
running** — F05 may need 15s+ for the breakfast-meeting explanation dialogue and
the bridging shots' exact engine choice may change. Confirm with the user before
spending.

---

## 4. Output workspace

- **Video files:** `video-tests/`
- **Reference stills:** `character-refs/higgsfield/<slug>/` and `location-refs/higgsfield/coverage/<slug>/`
- **Manifests:** `higgsfield-tools/cast-refs-manifest.json` and `higgsfield-tools/location-coverage-manifest.json`
- **Usage log:** `higgsfield-tools/usage-log.jsonl` (append-only, polled by `usage-tracker.js`)
- **Last-frame bridging stills:** `video-tests/<scene>_<frame>_lastframe.png` (used to seed next shot)

Existing test outputs in `video-tests/` (proof-of-concept only — not the final Scene 1 cut):
- `archive/christina_greeting_v1_pov_rejected_minimax_h3.mp4` (2K, 5.17s, 10 cr) — first-person framing
- `archive/christina_greeting_v2_thirdperson_minimax_h3.mp4` (2K, 5.17s, 10 cr) — re-cut third-person
- `archive/frame_for_kling_start.png` — last-frame extract, seed for Kling
- `archive/jan_response_kling_continuation_720p.mp4` (⚠️ 720p, 10.04s, 20 cr) — Kling continuation test
- `01_f01-f02_opening_greeting_minimax_h3.mp4` (2K, 15.08s, 30 cr) — single 15s opening
- `archive/opening_lastframe.png` — last-frame extract of the 15s

---

## 5. QA Rules (Higgsfield-specific)

1. **Default to `MiniMax H3` (2K) for any dialogue close-up.** Kling v3.0 is 720p
   and should only be used for bridging/continuation shots where its specific
   motion characteristics are needed. ⚠️ Always check `ffprobe` output resolution
   before declaring a shot done — the credit log alone won't tell you the resolution.
2. **Bridging shots: use a clean 1–2s segment of the previous clip as seed, not
   the literal final frame.** Final-frame seeds inherit that exact frame's
   artifacts (e.g. mid-blur on a hand transition). Re-extract from a clean segment
   if budget allows. See HANDOVER §10 "Gotchas" for the full finding.
3. **Verify on a single frame before committing to a full generation.** Higgsfield
   `Nano Banana 2` policy-blocks / face-blocks auto-refund, but `MiniMax H3` and
   `Kling v3.0` video credits are charged regardless. The `usage-tracker.js watch`
   feed is the early-warning signal — long stretches of `(refund)` rows on the
   ref generator usually mean a face is hitting identity protection and you
   need to swap reference or relax the prompt.
4. **Credit balance: stop and re-plan at <200 credits remaining.** The
   `usage-tracker.js watch` terminal shows the live balance; do not assume the
   last logged tick is current. Refresh before each batch.
5. **Reference continuity: every clip in §3 should pick a location coverage
   angle that matches the storyboard beat, not the closest one available.**
   Example: a "Jan yanks the blinds" beat (F26a) should use
   `jan_office_window_side`, not the generic `master_wide`. If the right angle
   doesn't exist in `location-refs/higgsfield/coverage/jan_office/`, generate it
   first (Nano Banana 2, 1.5 cr) before attempting the video.
6. **720p shots must be flagged in any editor/cut list.** `Kling v3.0` outputs
   `1280×720`, not 2K. If 2K continuity is mandatory for the final cut,
   regenerate the bridging shot as `MiniMax H3` and pay 10–30 credits/shot
   instead of 20–30.

---

## 6. Next steps (priority order)

1. **Fill `jan_office_corridor` chained coverage angles** — only `master_wide`
   exists. Need `corridor_view`, `door_closed`, `table_head`, `table_reverse`,
   `table_side`, `decal_closeup`, `openplan_context_wide` (7 angles × 1.5 cr = 10.5 cr).
   Retry face-bearing angles with `--image` chaining off the master + tighter
   identity-locking prompts.
2. **Resolve F22–F26b storyboard stills** (5 keyframes, no Higgsfield video can
   be cut without a reference still to anchor the beat — even though the
   adopted route is Higgsfield video, not Flow stills, the storyboard still
   drives the per-beat reference choice). 5 × 1.5 cr = 7.5 cr.
3. **Pilot the F01 Higgsfield cut as the working test case** — uses
   `jan_office_master_wide` + Jan + Christina refs, 10 cr. This validates the
   §3 plan against a real shot before committing to all 28 beats.
4. **Run the Scene 1 budget through `usage-tracker.js watch`** during the
   F01 test to confirm per-shot costs match the §3 estimates. Re-budget §3
   if the test comes in materially different.
5. **Re-cut the test outputs in `video-tests/` into a coherent Scene 1 opening
   once F01 is validated** (3 × 2K H3 + 1 × 720p Kling → ~15s of the S01–S03
   beats, then continue forward through §3).

---

## 7. What this file used to be (archaeology — do not action)

> Everything below the next horizontal rule is the **legacy local-pipeline tracker**
> from before the 2026-08-29 Higgsfield pivot. Kept so the git history of
> attempts is not lost. **Do not generate anything from these rows** — they
> describe a paused route. See §1 for the active engine routing.

---

# [LEGACY — DO NOT USE] Scene 1 — MiniMax-H3 Generation Tracker

Photoreal Ref2VA pipeline (turbo Q4_K denoiser + EasyCache as of 2026-08-26, auto-fit backend,
24fps / 864x480, frame count now sized per clip to fit its dialogue at natural pace — see
`minimax-h3-pipeline/README.md` and QA Rules 1-2 below — not fixed at 56).
References used per clip noted; QA checked against: (1) face/identity match to character
sheet, (2) wardrobe match, (3) location/set match, (4) no artifacts/garbling, (5) action
matches script beat, (6) dialogue pace sounds natural, not rushed (needs a human listen).

| # | Frame | Clip | Refs | Status | Notes |
|---|-------|------|------|--------|-------|
| 1 | F01 | — | Jan, Christina, Office | ✅ **resolved: Wan + TTS + lip-sync route validated** | Two MiniMax-H3 attempts both had real problems: v2 (turbo) had unusable audio, v3 (standard+EasyCache, `F01_v3.mp4`, seed 201002) had correct audio and beat but the whole wide shot read blurry/low-res (864x480 doesn't carry enough detail across a full wide environment). H3-FaceRefine was tried as a same-pipeline fix (see `minimax-h3-pipeline/README.md`) but did not actually sharpen the face at default settings. **The working answer**: `wan22-pipeline/` (sharp silent wide shot) + Qwen3-TTS voice clone (correct dialogue audio, cloned from a verified MiniMax-H3 sample) + MuseTalk lip-sync — validated end-to-end 2026-08-26 on a generic test clip (Whisper-verified exact transcription, real varying mouth shapes, no visible seams). Full setup/usage in `wan22-pipeline/comfyui-tools/README.md`. **Not yet applied to F01 itself** — that's the next step: generate F01's Wan wide shot with Jan+Christina, clone Christina's voice from her already-verified F03 line, generate her "Morning Jan. Survive the weekend?" line, lip-sync it in. |
| 2 | F02 | 1/3 (v3) | Jan, Office | 🔶 pending user review | **replanned as 3 clips, not 2** — original 22-word line was split 7/15 words, the 15-word half was rushed (6.4 wps); replit at natural clause breaks: "Barely. Another day dealing with these morons," / "who cannot understand the discipline and brilliance" / "it takes to run a place like this." — each ~7-8 words at 90 frames (3.75s), natural pace. Chained via `chain_clips.py`. **v2 (turbo) had unusable audio — Whisper transcription came back empty/wrong on all 3 turbo chunks despite fine-looking video; standard model transcribed the dialogue exactly right.** Regenerated as v3 with the standard model (seed 202101) → `F02_v3_c1/c2/c3.mp4` + `F02_v3_full.mp4`. Also fixed: concat previously used raw stream-copy, which corrupted audio at every splice ("hard cuts" on playback) — now re-encodes on concat. **Still needs a human listen** to confirm pacing/splice audio now sounds right. |
| 3 | F02 | 2/3 (v3) | Jan, Office | 🔶 pending user review | see row above — this is clip 2 of the replanned 3-clip F02 |
| 3b | F02 | 3/3 (v3) | Jan, Office | 🔶 pending user review | see row above — this is clip 3 of the replanned 3-clip F02 |
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

## [LEGACY] Restart plan — do this before generating F01 again

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

## [LEGACY] QA Rules (added 2026-08-25)

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

## [LEGACY] Addendum — 2026-08-27: cartoon-track F01 test on MiniMax-H3 (separate from the row above)

Everything above this line is the **photoreal** track. A separate **cartoon** track exists
(`storyboard-frames/F01.jpg` etc., style anchor in `MASTER_STORYBOARD_SESSION_PROMPTS.md`) and
had never been tried through MiniMax-H3 — only Google Flow. Ran one test:
`F01_cartoon_v1.mp4` (seed 401001), refs `jan_f01_cartoon_stencil.png` +
`christina_f01_cartoon_stencil.png` (cutout stencils from `character-refs/stencils/`) +
`office_cartoon_L10.jpg` (`location-refs/cartoon-plates/L10_jans_office.jpg`), standard
denoiser + EasyCache, 56 frames/864x480, dialogue embedded directly in the prompt text.

- **Audio correct** — Whisper transcription: "morning, Jan. Survive the weekend." exact
  match to the scripted line. No separate TTS/lip-sync pass needed for this track.
- **The photoreal wide-shot blur problem (row 1 above) did not reproduce** — Jan and
  Christina's faces stayed legible at 864x480 in the same full-room wide framing. Flat
  cel-shaded cartoon faces appear to carry much better than photoreal texture at this
  resolution, though this is one data point, not yet a settled finding.
- **New problem, not seen on the photoreal track**: every flat surface (ceiling, floor,
  glass, walls) picked up an unwanted sketchy cross-hatch texture not present in the
  reference stencils/plate or the original `F01.jpg` (which is clean flat cel-shaded art,
  no hatching). Likely the model interpreting "cartoon line art" loosely. Untried fix: add
  `cross-hatch, sketch texture, pencil shading` to the negative prompt on the next attempt.

Not yet decided whether this becomes the adopted cartoon-track route — one clip, one
character pair, no chained/multi-clip test yet.
