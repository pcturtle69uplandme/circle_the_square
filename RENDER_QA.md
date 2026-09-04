# ✅ PRE-RENDER QA GATE — Scenes 2 and 3

> Written after the first real clip (`c01_corridor_gossip`) came back, because rendering
> one clip taught things no amount of planning would have. Everything below is either
> **already fixed**, or a **decision still open**. Read before spending on clips 2–10.
>
> Companions: `SCENE2_VIDEO_SCRIPT.md` / `SCENE3_VIDEO_SCRIPT.md` (coverage audit),
> `VIDEO_BUDGET.md` (cost), `fal-tools/README.md` (how to run it).

---

## 1. Asset status — both scenes are complete

| | Stills | Status |
|---|---|---|
| **Scene 2** | 11 / 11 | ✅ all adopted and QA'd |
| **Scene 3** | 11 / 11 | ✅ all adopted and QA'd |
| **Canteen plates** | 3 / 3 | ✅ adopted |
| **Scene 2 clips** | 1 / 10 | `c01` adopted; 9 outstanding |

Four stills were generated late and QA'd only at this gate — worth recording because
they nearly went to render unchecked:

- `shot08b_inception_explained` — Jan's flustered climb-down. ✅ Correct navy tie for
  Scene 2 (not Scene 3's dark red).
- `s3_01_canteen_busy` / `s3_04_plates_swept` — regenerated with **Chris now in frame**
  (tray at the counter; staring from the right). Fixes him materialising at clip 8. ✅
- `s3_07a_second_chair` — Jan lifting a chair, **Rick absent**, so the Taser reveal
  survives. ✅

---

## 2. What `c01` taught us — FIXED

### 2.1 The camera overshot its direction 🔧 fixed

`c01` was written as a wide two-shot with *"push in very slowly"*. It came back a
**medium two-shot** — a far bigger move than asked.

Harmless inside the clip. **Not harmless at the join**: `c02` was going to seed from the
original wide still, which would jump the camera back out to a framing it had already
left — and `c02` is continuous action (Chris and Rick watching Sharon leave), not a cut.

Two fixes, both applied:

- **A `FRAMING` lock** now appears in all 8 non-keyframe clips: *"hold the reference
  frame shot size… the framing at the END must still match the framing at the START. Do
  not push in, do not zoom, do not reframe."* Giving the model a **framing target**
  rather than a movement *speed* is the point — "slowly" was interpreted as licence.
- **`chainFrom`** seeds a clip from the previous clip's **real last frame**
  (`last_frame.js`) rather than an adopted still. Applied to `c02` only.

**Chaining is deliberately limited to c02.** Scene 1 measured generational drift
compounding down a chain — brightness falling and shadows crushing roughly twice every
~4 links. Every other Scene 2 clip is a genuine cut and keeps its own adopted still,
which resets the chain for free.

### 2.2 Rick's deadpan didn't land 🔧 fixed

Rick read *animated* — mouth open, brow raised, mid-conversation. **His non-reaction is
the joke**; Scene 2 runs on the absence of a response three separate times (Rick here,
the crowd's silence after "SHUT UP!", the blank on "Inception").

`(flat monotone, no expression change)` as a parenthetical was too weak. Replaced with
explicit negative direction: *"a DEAD, MOTIONLESS face. His eyebrows do not move, he
does not smile, he does not turn to look at Chris… Only his mouth moves."*

### 2.3 What went right — keep doing it

- **Identity held.** Chris and Rick carried over from the still with wardrobe intact —
  the grey polo and light blue shirt both survived into motion.
- **The blinds held.** The closed opaque blinds that took four attempts as a still
  stayed shut and opaque through the clip.
- **Audio arrived in-pass** — AAC stereo, no separate foley stage needed.
- **Duration was exact** — 10.14s for a 10s request, 1344×768, 24fps.

---

## 3. Decisions still open 🔶

### 3.1 Resolution mismatch across the film

Scene 1 is **2560×1440** (Higgsfield). Scene 2 will be **1344×768** (fal). Scene 3 is
planned for Higgsfield 2K.

That means the finished episode would run 2K → 768p → 2K. The 768p middle will be
visibly softer on a large screen. This was accepted knowingly in `HANDOVER.md` §12 when
the alternative was not building Scene 2 at all — but that was before Scene 3 was
costed and found to fit comfortably in the Higgsfield balance.

**Worth re-deciding now.** Options: accept it; upscale Scene 2 in post; or move Scene 2
to Higgsfield too (~218 credits, which no longer fits alongside Scene 3 without a
top-up).

### 3.2 Background extras appear where the still had none

`c01`'s still specified *"exactly two men and nobody else"*. The clip added people
walking in the background. Arguably an improvement — a real office has traffic — but it
is the model overriding an explicit instruction, so flag it rather than assume it
generalises safely.

### 3.3 Scene 3's content filter risk is untested on fal

Scene 3 has a rage sequence, property destruction and a taser. Higgsfield NSFW-flagged a
Scene 2 still for nothing worse than a red-faced shouting man. **fal's filter behaviour
is completely unknown to us** — no Scene 3 clip has been attempted anywhere. If Scene 3
does go to fal rather than Higgsfield, test `s3_07b_taser_collapse` early rather than
last.

### 3.4 Aspect ratio is never set explicitly

The sandbox has an **Aspect Ratio** control the driver does not touch. `c01` came back
16:9 matching the stills, so the default appears correct — but it is a default, not a
guarantee. Consider pinning it the way duration now is.

---

## 4. Cost position

Confirmed by generating `c01`: the balance moved **$0.74 → $0.54**, while the free
counter stayed at 50. **Image-to-video is metered at $0.02/sec** — the free 5/day is
text-to-video only, exactly as the breakdown said.

| | |
|---|---|
| Spent so far | $0.20 (`c01`, 10s) |
| Remaining 9 clips | 115s ≈ **$2.30** |
| Balance | $0.54 |
| **Top-up needed** | **~$2** |

For comparison the same scene on Higgsfield 2K is ~218 credits ≈ $10.64.

---

## 5. Go / no-go

**Ready to render clips 2–10** once the top-up lands. Before the batch:

1. `node last_frame.js c01_corridor_gossip` — already done, `c02` will chain from it.
2. Run **`c02` alone first** and check the join against `c01`'s tail. It is the only
   chained clip and the only 2-frame keyframe pair, so it is the highest-risk clip in
   the scene.
3. If `c02`'s framing holds, run the rest — but **QA each clip's last frame against the
   next clip's start still** and add `chainFrom` wherever the camera has drifted.

Do not batch all nine blind. The camera-overshoot problem is exactly the kind that only
shows up at the joins, and at $0.02/sec a re-render is cheap — an unusable scene is not.
