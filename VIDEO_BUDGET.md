# 💷 VIDEO BUDGET — Scenes 2 and 3 on MiniMax H3

> Costed from **actual observed spend**, not list prices. Source:
> `higgsfield-tools/usage-log.jsonl` (Scene 1's real generations) and
> `.agents/rules/clip_duration_rules.md`.

## The rate, measured

Scene 1's 19 MiniMax H3 clips at 2560×1440 cost **374 credits**, distributed:

| Credits | 10 | 14 | 16 | 18 | 20 | 22 | 24 | 28 | 30 |
|---|---|---|---|---|---|---|---|---|---|
| Clips | 2 | 2 | 1 | 4 | 2 | 4 | 1 | 2 | 1 |

Mean **19.7 credits/clip**, range 10–30. That maps exactly onto the rule in
`clip_duration_rules.md` (8s = 16cr, 15s = 30cr):

> **2 credits per second at 2K. Minimum billed 5s (10 credits). Maximum 15s (30
> credits).**

The floor matters: **a 2-second beat still costs 10 credits.** Billing is per second of
clip, not per beat — so short beats are the expensive ones, proportionally.

---

## Dialogue load

Measured from `CTS_Featurette_Episode.fountain` at the project's established ~2.75
words/sec, plus reaction/action time.

| | Spoken words | Notes |
|---|---|---|
| **Scene 2** | **275** | Dialogue-heavy. Six clips run 12–15s. |
| **Scene 3** | **64** | Action-heavy. Eight of eleven beats fall under the 5s floor. |

This asymmetry drives everything below: Scene 2 is expensive because it is *long*,
Scene 3 is inefficient because it is *choppy*.

---

## Scene 2 — 11 clips, beat-by-beat

| Clip | Words | Est. | Billed | Cr |
|---|---|---|---|---|
| 06 corridor gossip | 19 | 8s | 8 | 16 |
| 07 sharon exits | 0 | 4s | 5 ⚠️ | 10 |
| 07b-1 jan addresses | 31 | 13s | 13 | 26 |
| 07b-2 shut up | 33 | 12s | 12 | 24 |
| 07c-1 rick questions | 43 | 16s | 15 ✂️ | 30 |
| 07c-2 naming inception | 35 | 13s | 13 | 26 |
| 08a dreaming heckle | 4 | 2s | 5 ⚠️ | 10 |
| 08b inception explained | 20 | 7s | 7 | 14 |
| 08c merch gag | 38 | 14s | 14 | 28 |
| 09-1 groans | 37 | 13s | 13 | 26 |
| 09-2 get back to work | 15 | 6s | 6 | 12 |
| **Total** | **275** | | **111s** | **222** |

⚠️ = padded up to the 5s floor · ✂️ = capped at the 15s ceiling

## Scene 3 — 11 clips, beat-by-beat

| Clip | Words | Est. | Billed | Cr |
|---|---|---|---|---|
| 00 christina recipe | 0 | 6s | 6 | 12 |
| 01 canteen busy | 0 | 4s | 5 ⚠️ | 10 |
| 02 jan asks maureen | 10 | 4s | 5 ⚠️ | 10 |
| 03 that is it | 4 | 2s | 5 ⚠️ | 10 |
| 04 plates swept | 0 | 4s | 5 ⚠️ | 10 |
| 05 mba scream | 16 | 6s | 6 | 12 |
| 06 chair through window | 0 | 4s | 5 ⚠️ | 10 |
| 07a second chair | 0 | 3s | 5 ⚠️ | 10 |
| 07b taser collapse | 0 | 4s | 5 ⚠️ | 10 |
| 08 have you killed him | 4 | 2s | 5 ⚠️ | 10 |
| 09 rick reply | 30 | 11s | 11 | 22 |
| **Total** | **64** | | **63s** | **126** |

**Eight of eleven clips hit the floor.** Real content is ~51s but 63s is billed — 24%
of Scene 3's cost is padding.

---

## 💡 Combining beats saves real money on Scene 3

`clip_duration_rules.md` is explicit: bill is per length, not per beat, so consecutive
beats should be chained into one call up to 15s. Applied:

### Scene 3 combined — 6 clips instead of 11

| Clip | Beats | Billed | Cr |
|---|---|---|---|
| A | 00 christina *(separate — different day)* | 6 | 12 |
| B | 01 busy + 02 jan asks | 8 | 16 |
| C | 03 that is it + 04 plates swept | 6 | 12 |
| D | 05 mba scream + 06 chair through window | 10 | 20 |
| E | 07a second chair + 07b taser collapse | 7 | 14 |
| F | 08 killed him + 09 rick reply | 13 | 26 |
| **Total** | | **50s** | **100** |

**Saves 26 credits (21%) and halves the number of calls.** C, D and E are exactly the
destruction/keyframe pairs — combining them is *better* filmmaking too, since the break
happens as continuous motion inside one clip rather than across a cut.

### Scene 2 combined — 10 clips instead of 11

Only `08a`+`08b` merge cleanly (9.5s). Everything else is already 12–15s. **218
credits** — a saving of just 4. Scene 2's beats are long enough that there is nothing
to reclaim.

---

## Retake allowance — do not skip this

Scene 1's log is the honest guide. Of its 374 credits, the tracker identifies **84 as
waste**: 62 across three regenerations (generational drift) plus a 22-credit failed 503
job that had to be retried. That is **22% overhead on a scene where we were still
learning the tool**.

Scenes 2 and 3 start from QA'd stills and a hardened pipeline, so they should do better
— but glass, shattering china and a body falling are harder motion than Scene 1's
talking heads. **Budget 30%.**

| | Clips | Base | +30% retakes | **Realistic** |
|---|---|---|---|---|
| **Scene 2** (combined) | 10 | 218 | +65 | **~283** |
| **Scene 3** (combined) | 6 | 100 | +30 | **~130** |
| **Both** | 16 | 318 | +95 | **~413** |

Beat-by-beat instead of combined: ~452 credits.

---

## 🔴 The balance problem

Last observed balance on `groovingmushroom1467` (Plus plan, 2026-09-04): **287
credits**. *Re-check before committing — this needs confirming at the point of spend.*

| Plan | Cost | Fits in 287? |
|---|---|---|
| Scene 3 only | ~130 | ✅ comfortably, ~157 left |
| Scene 2 only | ~283 | ⚠️ only just — no retake margin at all |
| **Both scenes** | **~413** | ❌ **short by ~126** |

At the historic rate of **~$0.0488/credit** (`HANDOVER.md` §10), the shortfall is about
**$6**, and the whole 413-credit programme is about **$20**. Topping up is likely
cheaper than any workaround.

### Options

1. **Top up ~150 credits (~$7)** and do both scenes. Simplest, and cheap in absolute
   terms.
2. **Scene 3 first (~130).** It is the finale, it is the cheaper half, and it leaves
   ~157 credits as a buffer. Scene 2 follows after a top-up.
3. **Scene 2 first (~283).** Fits only if nothing needs a retake, which the Scene 1
   evidence says will not happen. Not recommended.
4. **Drop to a lower resolution.** Scene 1 was shot at 2560×1440 and Scene 2/3 must
   intercut with it, so this trades continuity for money. Only worth it if the budget
   is hard-capped.

**Recommendation: option 2 if not topping up, option 1 if you are.** Scene 3 is the
better first spend either way — it is cheaper, it is the ending, and its combined-clip
structure means fewer calls and therefore fewer chances to burn credits on a retake.


---

## 🆕 Platform comparison — verified 2026-09-04

`HANDOVER.md` §12 recorded fal.ai's free tier from a web search in September and noted
it was never hands-on verified. Re-checked against fal's own model page today.

### fal.ai `minimax/h3-max` — confirmed

| | |
|---|---|
| **Free tier** | **5 generations/day**, up to **15s each**, rolling 24h reset. Account required, no subscription. |
| **Resolution** | 768p (1344×768 @ 24fps), or 480p |
| **Metered beyond free** | **$0.08/sec** at 768p (a launch promo of $0.04/sec was advertised — verify it still applies before relying on it) |
| **Keyframing** | ✅ image-to-video with **first-to-last frame** support |
| **Audio** | ✅ synchronised audio generated in the same pass — room tone, foley, ambience |

Two things matter here beyond price:

- **First-to-last frame keyframing is supported.** That is exactly what clips 4, 6 and
  7 need — they were deliberately anchored on aftermath so the break happens as motion
  between two frames. Without keyframing that plan would not port.
- **Audio is in the same pass**, which satisfies the project rule that the video model
  must generate its own audio (no separate TTS or lip-sync chain).

### Google Flow — not viable for Scenes 2 or 3

Flow runs **Veo 3.1**, not MiniMax H3. Three blockers, in order of severity:

1. **Different model family.** §12 already rejected Grok Imagine on exactly this
   reasoning: mixing another family into a scene anchored on MiniMax H3's look reads as
   a visible style break.
2. **Clips cap at 4–8s.** Six of Scene 2's clips run 12–15s, so every one would split —
   10 clips becomes ~15, with more cuts and more drift.
3. **Resolution** below Scene 1's 2560×1440.

Credits are not the constraint (AI Pro = 1,000/month; Scene 2 ≈ 300 at Veo 3.1 Fast).
The look is. **Keep Flow for work that does not need to match MiniMax** — the title
sequence and the building/drone establishing plates it was already used for.

### Scene 2 costed three ways

Scene 2 is 10 combined clips totalling ~111s.

| Route | Resolution | Cost | Elapsed |
|---|---|---|---|
| **fal.ai free** | 768p | **£0** | ~2 days (5/day), ~3 with retakes |
| **fal.ai metered** | 768p | ~**$8.88** (~$4.44 if the promo holds) | same day |
| **Higgsfield** | 2K | ~218 cr ≈ **$10.64** | same day |

fal.ai metered at 768p is cheaper per second than Higgsfield at 2K, but the real choice
is £0-and-slow versus 2K-and-now.

### Recommended split

- **Scene 2 → fal.ai free tier.** 768p, £0, two to three days. Same model family, so it
  still cuts against Scene 1 and Scene 3.
- **Scene 3 → Higgsfield 2K** (~130 credits of the ~287 balance). The finale at full
  quality, leaving ~157 credits as retake buffer.
- **Google Flow → neither.** Reserve for title/drone work.

**Blocker before starting**: there is still **no fal.ai tooling in this repo** —
`higgsfield-tools/` is Higgsfield-specific. Scene 2 on fal.ai needs a small driver
equivalent to `run_shot.js`, plus the account. That is the first task if this route is
taken.
