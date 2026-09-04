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
2. **The "50 free generations today" banner is split PER MODEL, and is misleading.**
   The breakdown (user-supplied, 2026-09-04) reads:

   | Model | Free/day |
   |---|---|
   | Z Image Turbo | 10 |
   | Birefnet Background Removal V2 | 10 |
   | FLUX.2 [klein] 9B | 10 |
   | Wan Text to Video | 5 |
   | Flux 3 Text To Video Draft | 5 |
   | **MiniMax H3 Max — Text to Video** | **5** |
   | Grok Imagine Video 1.5 | 5 |

   🔴 **The MiniMax entry is TEXT-to-video. There is no image-to-video line.** Every
   clip in this project is image-to-video, anchored on a QA'd still — that is the whole
   point of the 19 stills. So the free allowance may not cover our route at all. See
   "Is image-to-video free?" below; this is unresolved and must be settled before
   planning around £0.
3. **Duration is a dropdown of 5s / 10s / 15s only** — not free-form seconds. See
   "Handling the fixed durations" below.
4. **Two image inputs** (`accept="image/*"`), which is exactly what the first/last
   keyframe pairs need.

Re-run `node fal_clip.js probe` if fal changes its UI.

## 🔴 Is image-to-video free? — UNRESOLVED

The free breakdown names **"MiniMax H3 Max Text to Video"** only. Our route is
image-to-video. Three possibilities, in decreasing order of optimism:

1. The 5/day covers the model regardless of mode, and the label is just loose.
2. Image-to-video is metered while text-to-video is free.
3. Image-to-video is metered at a different rate again.

**Evidence to hand**: an earlier session's `minimax/h3-max/image-to-video` run, 5s, is
logged in the sandbox feed as **Total Cost $0.100** — i.e. ~$0.02/sec, well under the
$0.08/sec on the public model page. The account balance stands at **$0.74**.

**How to settle it cheaply**: generate exactly one short image-to-video clip and watch
which counter moves — the free tally, or the $0.74. That costs at most ten cents and
answers it definitively. Do this before committing to a route.

**What it means if image-to-video is metered:**

| Rate | Scene 2 (125s) | Covered by $0.74? |
|---|---|---|
| $0.02/sec (observed) | ~$2.50 | ❌ short ~$1.76 |
| $0.08/sec (published) | ~$10.00 | ❌ short ~$9.26 |

Either way a small top-up covers it, and both figures are still at or below Higgsfield's
~$10.64 for the same scene at 2K.

**Do NOT fall back to text-to-video to stay free.** It would discard the still anchors,
and with them every bit of character and location continuity the 19 QA'd stills exist to
provide. Paying a few dollars is far cheaper than regenerating that consistency.

## 🔑 The start frame must contain every character — fal is not Higgsfield

**This is the biggest architectural difference between the two platforms, and it
dictates how the clips are cut.**

Higgsfield takes a gallery of character reference images alongside the prompt, so a
character can be introduced mid-shot and still hold their identity. **fal's
image-to-video takes only a first frame and an optional last frame.** There is no
reference slot. Anything not in the start frame is invented from the text description —
which will not match a cast reference, and therefore will not match Scene 1's footage.

**Rule: every character who needs identity-locking must already be IN the clip's start
frame.** Dropping a character sheet into the second slot does not help — that slot is
the LAST frame, so the clip would end on a studio portrait.

Audited across Scene 2: ten of eleven clips already satisfy this, because each start
still contains everyone who appears. Only the Sharon beat did not, and it failed exactly
as predicted — starting from `shot06` (Chris and Rick only) left Sharon *and* Jan to be
invented, and the render put Sharon in the corridor having never come out of the office.

The fix drove the cut structure:

| Clip | Start frame | Why |
|---|---|---|
| `c02a_blinds_raised` | `shot06` | Fixture change only — **nobody in shot needs anchoring** |
| `c02b_sharon_exits` | `shot07` | Contains **all four** — Sharon, Jan, Chris, Rick |

So a beat that needs a character who is not in the available still gets **split**, so that
one half needs no anchoring and the other starts from a frame that has everybody. That is
a structural consequence of the platform, not a stylistic choice.

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
