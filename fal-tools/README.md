# fal.ai tooling — Scene 2 video on MiniMax H3 Max

Closes the open item recorded in `HANDOVER.md` §12: *"No fal.ai tooling exists in this
repo."*

## Why fal.ai for Scene 2

Verified 2026-09-04 against fal's own model page (see `VIDEO_BUDGET.md`):

| | |
|---|---|
| Free tier | **5 generations / rolling 24h**, up to **15s each**. Account required, no subscription. |
| Resolution | 768p (1344×768 @ 24fps) |
| Metered | $0.08/sec at 768p beyond the free allowance |
| Keyframing | ✅ first-to-last frame image-to-video |
| Audio | ✅ synchronised, generated in the same pass |

Same model family as Scene 1's Higgsfield footage, so it still intercuts. The trade is
768p instead of 2K, in exchange for £0 — a resolution drop the user accepted knowingly
back in September (`HANDOVER.md` §12; do not "fix" it back onto paid Higgsfield without
asking).

Google Flow was considered and rejected: it runs Veo 3.1, a different model family, and
caps clips at 4–8s when six of Scene 2's run 12–15s. See `VIDEO_BUDGET.md`.

## Layout

| File | Role |
|---|---|
| `browser/scene2_clips.js` | The ten clip definitions — prompt, dialogue, SFX, keyframes, duration |
| `browser/fal_up.js` | Starts a **detached** Chrome on **port 9333** with its own profile |
| `browser/fal_clip.js` | Drives one generation; `probe` dumps the page for calibration |
| `browser/run_clips.js` | Resumable batch driver, capped at the free-tier allowance |

Port 9333 and a separate profile are deliberate: the Higgsfield pipeline owns 9222, and
the two must be able to run at once under different logins.

## Usage

```bash
cd fal-tools/browser

node fal_up.js                    # start the browser once (detached, survives task cleanup)
                                  # -> sign in to fal.ai by hand in that window

node fal_clip.js probe            # REQUIRED FIRST -- dump the live page's controls
node run_clips.js --dry-run --max 99   # print every prompt, generate nothing

node run_clips.js                 # generate up to 5 clips (one free-tier day)
node run_clips.js --only c07_inception_exchange   # re-render one clip
```

## Calibrated 2026-09-04 — what the live sandbox actually does

Probed while signed in. Four things differed from the documentation:

1. **The model playground URL 404s.** `fal.ai/models/fal-ai/minimax/h3-max/...` does not
   exist. The working surface is the **sandbox**:
   `https://fal.ai/sandbox?models=&op=video.image_to_video`.
2. **The free allowance showed "50 free generations today"**, not the documented 5/day.
   Treat 5 as the guaranteed floor and 50 as a bonus that may be promotional — the
   driver still caps at `--max 5` by default.
3. **Duration is a dropdown of 5s / 10s / 15s only** — not free-form seconds. See
   "Handling the fixed durations" below.
4. **Two image inputs** (`accept="image/*"`), which is exactly what the first/last
   keyframe pairs need.

Re-run `node fal_clip.js probe` if fal changes its UI.

## Handling the fixed durations

fal offers only 5s / 10s / 15s, but the beats are 8s, 12s, 13s, 14s and so on. Every
clip is snapped **up**, never down, so a line can never be cut mid-delivery. That takes
Scene 2 from 109s of content to 125s of clip — **16s of slack across 10 clips**, with 3
landing exactly.

**The danger of snapping up is not dead air — it is that the model fills time it was
given and told nothing about**, with invented business, a repeated gesture, or worst of
all invented dialogue over a finished line. So every clip with slack carries an explicit
`TIMING:` line stating where the dialogue ends, exactly what to hold on for the
remainder, and always closing with *"No further dialogue."*

| Clip | Content | Clip | Held beat |
|---|---|---|---|
| `c01` | 8s | 10s | Rick's blank deadpan while Chris waits for a reaction |
| `c03` | 13s | 15s | Jan pleased with his own answer, crowd flat |
| `c04` | 12s | 15s | **Frozen silence after "SHUT UP!"** |
| `c06` | 13s | 15s | **Nobody reacting at all to the name "Inception"** |
| `c08` | 14s | 15s | The crowd's stunned faces after "…by me" |
| `c09` | 13s | 15s | Jan's smug face over resentful muttering |
| `c10` | 6s | 10s | **The room emptying around Jan, alone** — the scene's last shot |

In practice the slack is an asset. The silence after the outburst, the blank
non-reaction to the project name, and the floor clearing around Jan at the end are
comedy beats the scene wants anyway — the fixed durations just force us to direct them
deliberately instead of hoping they emerge.

If a generation still overruns, the fallback is to re-chunk which beats share a clip
rather than to trim in the edit, since trimming cuts the audio tail mid-flow.

## A trap worth knowing

The sandbox renders **every previous generation** on the same page, so "a `<video>`
element exists" proves nothing about your own run. `fal_clip.js` snapshots the video
sources before submitting and accepts only one that was not already there. This is the
same stale-result bug that mislabelled two Higgsfield stills before it was guarded —
without it, a clip will happily save a video from two days ago.

Duration also **persists between runs**, so it is set and then read back and verified
every time; otherwise a 15s clip silently renders as 5s.

## How this differs from the Higgsfield toolkit

It reuses the patterns that were expensive to learn there — detached browser so the
process outliving its launcher cannot kill it mid-run, overlay dismissal before every
interaction, fingerprint sidecars so editing one prompt re-renders exactly one clip, and
per-clip retries so a transient failure does not abandon the queue.

Two things are deliberately different:

- **`--max` defaults to 5**, matching the free allowance. Scene 2 is ten clips, so a
  clean run is two days. Without the cap a batch would roll straight past the free tier
  and start billing at $0.08/sec.
- **Polling is much longer** (up to 20 minutes per clip). Video generation is far slower
  than the image pipeline.

## Clip plan

Ten clips, ~109s total. `endImage` marks a first-to-last keyframe pair.

| Clip | s | Keyframes | Beat |
|---|---|---|---|
| `c01_corridor_gossip` | 8 | 1 | Chris and Rick gossip |
| `c02_sharon_exits` | 5 | **2** | Blinds raised, Sharon exits — fixes the continuity hole where nothing showed the blinds opening |
| `c03_jan_addresses` | 13 | 1 | Jan claps, is asked about Sharon, deflects |
| `c04_shut_up` | 12 | 1 | Sniggering ripples, Jan erupts |
| `c05_rick_questions` | 15 | 1 | Rick's challenge, Jan justifies |
| `c06_naming_inception` | 13 | 1 | Jan names the project |
| `c07_inception_exchange` | 10 | **2** | All **four** turns of the gag |
| `c08_merch_gag` | 14 | 1 | The merch, and Jan appoints himself |
| `c09_groans` | 13 | 1 | Groans, Jan justifies the £50k |
| `c10_get_back_to_work` | 6 | 1 | The final bellow |

Dialogue is verbatim from `CTS_Featurette_Episode.fountain`. It is **not** taken from
`scene_dialogue_audio_guide.md`, which deletes *"You're dreaming Jan!"* and *"What?!"*
from the Inception exchange and paraphrases Jan's closing speech — see
`SCENE2_VIDEO_SCRIPT.md` §1.
