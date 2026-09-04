# 🎬 SCENE 3 — EXPANDED VIDEO SCRIPT & COVERAGE AUDIT

> `INT. STAFF RESTAURANT / CANTEEN - NEXT MORNING` — `CTS_Featurette_Episode.fountain`
> L152–196, the final scene.
>
> **Purpose**: this is the pre-video pass. For each beat it sets out (a) the script
> verbatim, (b) what the adopted still already shows, (c) **what the still cannot
> show and the video clip must therefore supply**, and (d) anything the script calls
> for that is **not anywhere in the assets**. Read this before writing a single
> MiniMax H3 prompt — video is the first thing in this scene that costs credits.
>
> Companion to `SCENE3_SHOT_LIST.md` (which plans the stills) and
> `SCENE2_VIDEO_PLAN.md` (which established the chaining method).

---

## ⚠️ Section 1 — Things the script calls for that DO NOT EXIST in any asset

These are the real gaps. Nothing below is covered by a still, and most are not
covered by the dialogue guide either.

### 1.1 Christina's sabotage — an entire story beat with no coverage 🔴

Script L154, the scene's opening action line, verbatim:

> *"Lots of pain au chocolat have been prepared by the canteen team to a specific
> high-sugar recipe given by Christina. Even the canteen staff thought the sugar
> content was far too high, but Christina assured them it was fine."*

**This is currently invisible in the film.** It is pure prose with no dialogue, no
shot, and no mention in `scene_dialogue_audio_guide.md`. It is also not decoration —
it is the scene's *causal* setup. Christina spends all of Scene 1 manoeuvring against
Jan; this line implies she deliberately engineered the sugar crash that triggers his
meltdown. Without it, Jan simply explodes about a pastry and the scene loses its
spine.

Christina has a full reference set (`character-refs/higgsfield/christina/`), so she is
generatable at no cost. **This needs a decision** — three options:

| Option | What it costs | What it buys |
|---|---|---|
| **A. Drop it** | nothing | Scene plays as a pure tantrum. Loses the Christina throughline. |
| **B. Add a cold-open still + clip** — Christina at the servery the previous day, instructing a doubtful Maureen, pointing at a recipe card | 1 free still + 1 paid clip | Restores the setup and pays off Scene 1. Recommended. |
| **C. Voiceover only** over clip 1 | 1 paid clip's audio | Cheapest way to keep the plot point; no new visuals. |

My recommendation is **B**, as a new clip `s3_00_christina_recipe` placed before
clip 1. It is the only option that makes the joke land visually, and the still is free.

### 1.2 Rick's best line has been silently cut 🔴

The fountain script gives Rick:

> *"No relax, he will be out for a while. **I knew this Taser would come in useful one
> day in this place.** I think we need the police here..."*

`scene_dialogue_audio_guide.md` L143 drops the middle sentence entirely. That sentence
is the punchline — it retroactively characterises Rick as a man who has been waiting
years for this. **Use the full fountain line, not the guide's version.**

This is exactly the failure the Scene 2 standing rule warns about: *always check the
full `.fountain` script for every gag, never just a summary guide's named beats.* The
guide also compresses nine beats into four, so treat it as a rough audio reference
only.

Timing impact: full line ≈ 30 words ≈ 11s (fits the 15s ceiling). Trimmed ≈ 19 words
≈ 7s.

### 1.3 Jan's entrance is never shown 🟡

Script: *"The last pastry has just been claimed **before Jan enters**."* No still shows
Jan entering the canteen — clip 2 opens with him already at the counter. Either fold
the entrance into clip 2's opening motion (walking in, crossing to the counter), or
accept a cut. Low risk, but decide deliberately.

### 1.4 Chris materialises from nowhere 🟡

Chris first appears in clip 8, crouching. He is in **none** of clips 1–7. Rick's
absence is deliberate — it protects the Taser reveal — but Chris has no such excuse,
and appearing only to deliver a line reads as a continuity jump. **Fix in the video
prompts**: put Chris in the crowd from clip 1 onward (he is in the queue, then among
the frozen onlookers). No new stills needed; the video prompts can place him.

### 1.5 The canteen team, plural 🟢

Script says *"the canteen **team**"* and *"the canteen **staff** thought…"*. Only
Maureen is ever visible. Minor; add a second server behind the counter in clip 1's
video prompt if it is cheap to do so.

---

## 🎞️ Section 2 — Beat-by-beat expansion

Format per beat: **SCRIPT** (verbatim) → **STILL HAS** → **VIDEO MUST ADD** → **AUDIO**.

Audio matters more than usual here: per project rule the video model generates its own
audio, so every SFX and line below has to be in the clip prompt. There is no separate
TTS or foley pass.

---

### Clip 0 — Christina's recipe *(proposed, see §1.1 — does not yet exist)*

- **SCRIPT**: L154, the high-sugar recipe given by Christina over the canteen staff's
  objections.
- **STILL HAS**: nothing. Not generated.
- **VIDEO MUST ADD**: Christina at the servery handing Maureen a recipe card or tablet,
  Maureen frowning at it and gesturing at the sugar quantity, Christina waving the
  objection away with a small cold smile and walking off. Previous day, so dress the
  counter differently (full trays, no crowd).
- **AUDIO**: no scripted dialogue. Either mime it, or invent a line pair consistent with
  Christina's register. Ambient canteen tone.

---

### Clip 1 — `s3_01_canteen_busy`

- **SCRIPT**: *"Due to the free food, there is high demand. The last pastry has just
  been claimed before Jan enters."*
- **STILL HAS**: busy canteen, queue at the servery, diners at tables, full pastry
  trays, a worker lifting one with tongs. All four recurring extras present.
- **VIDEO MUST ADD**:
  - The **motion of the last pastry being taken** — tongs close, pastry lifts, tray is
    left empty. This is the story point and it only exists as motion.
  - General canteen life: chatter, people moving through the queue.
  - **Chris placed in the crowd** (see §1.4).
- **AUDIO**: busy canteen ambience — cutlery, overlapping conversation, coffee machine.
  No dialogue.

---

### Clip 2 — `s3_02_jan_asks_maureen`

- **SCRIPT**: `JAN: "Is there any more pain au chocolat?"` / `CANTEEN WORKER: "Sorry,
  all gone."`
- **STILL HAS**: Jan at the counter looking down at emptied trays; Maureen mid-shrug;
  crumbs and paper cases; intact china stacks.
- **VIDEO MUST ADD**:
  - Optionally Jan's **entrance and approach** (see §1.3).
  - Maureen's shrug as a *movement*, and Jan's face falling.
  - Lip-sync on both lines.
- **AUDIO**: both lines. Ambience continues **normally** here — the room has not yet
  noticed anything.
- **NOTE**: the script credits `CANTEEN WORKER`; we cast **Maureen**, who is in the
  cast bible as a canteen worker. Deliberate, recorded in `SCENE3_SHOT_LIST.md`.

---

### Clip 3 — `s3_03_that_is_it`

- **SCRIPT**: `JAN (veins bulging): "OH THAT IS IT!"`
- **STILL HAS**: Jan flushed, fists clenched, bellowing; Maureen recoiling; room still
  occupied and normal; china stacks still intact.
- **VIDEO MUST ADD**: the **snap** — Jan going from deflated to incandescent in about a
  second. Veins/colour rising. Heads in the background starting to turn.
- **AUDIO**: the line, shouted. Ambience should start to drop away.

---

### Clip 4 — `s3_04_plates_swept`

- **SCRIPT**: *"Jan grabs the plates from the counter and sweeps them onto the floor.
  CRASH! China shatters. Everyone in the canteen stops talking and stares."*
- **STILL HAS**: **the aftermath only** — china already smashed across the floor,
  counter bare, Jan's arms still flung out at the end of the sweep, room frozen.
- **VIDEO MUST ADD**: 🔴 **the entire action.** No still shows Jan grabbing or holding
  the plates. This clip runs from clip 3's end frame (stacks intact) to clip 4's still
  (stacks destroyed), and the sweep happens between them. That is exactly why clip 4
  was anchored on aftermath — use **start-frame/end-frame keyframing**, not a single
  reference.
- **AUDIO**: 🔴 **CRASH of shattering china**, then **sudden total silence** — the
  script's "everyone stops talking" is an *audio* beat as much as a visual one. The
  cut from busy ambience to dead silence is the joke's timing.

---

### Clip 5 — `s3_05_mba_scream`

- **SCRIPT**: `JAN (screaming): "I HAVE HAD IT WITH THIS PLACE! I HAVE AN MBA, NOBODY
  APPRECIATES MY IMMENSE TALENT!"`
- **STILL HAS**: Jan mid-scream, arms wide; broken china persisting on the floor; crowd
  frozen; window still intact.
- **VIDEO MUST ADD**: the delivery — spittle, heaving chest, the crowd flinching back a
  half-step.
- **AUDIO**: the full line, screamed. Room silent behind it apart from a scraped chair
  or a gasp.
- **NOTE**: the fountain has *"I HAVE AN MBA, NOBODY…"*; the dialogue guide writes
  *"I HAVE AN MBA! NOBODY…"*. Trivial, but use the fountain punctuation for the beat.

---

### Clip 6 — `s3_06_chair_through_window`

- **SCRIPT**: *"Jan grabs a heavy meeting chair and hurls it into the nearest window.
  GLASS SHATTERS."*
- **STILL HAS**: **the aftermath only** — pane shattered with jagged edges, the chair
  lying on the courtyard paving beyond, glass spray across the floor, chair stack one
  short, Jan at the end of his follow-through.
- **VIDEO MUST ADD**: 🔴 **the grab and the throw.** No still shows Jan holding a chair.
  Again a start/end keyframe pair: clip 5's end (window intact) → clip 6's still
  (window gone).
- **AUDIO**: 🔴 **glass explosion**, chair clattering onto paving outside, screams from
  the crowd.
- **NOTE**: the chair stack was invented for the plate so that "a heavy meeting chair"
  is plausibly to hand in a canteen. Not in the script; keep it consistent now it
  exists.

---

### Clip 7 — `s3_07_taser_collapse`

- **SCRIPT**: *"Jan turns to grab a second chair. Suddenly — POP-CRACKLE! A loud
  electric discharge sound behind Jan. Jan freezes, drops the chair, and slumps
  face-first onto the floor unconscious. Behind him stands RICK, holding a prop
  TASER."*
- **STILL HAS**: **the aftermath only** — Jan face-down and limp, a chair on the floor
  beside him, Rick standing behind with the yellow stun device lowered, onlookers
  frozen.
- **VIDEO MUST ADD**: 🔴 **the most action-dense clip in the scene, and the only one
  where the still covers the least.** Four distinct actions have no anchor at all:
  1. Jan **turning back** toward the chair stack
  2. Jan **grabbing a second chair**
  3. Jan **freezing** at the discharge
  4. Jan **dropping the chair and falling face-first**
  — and only then does the still's state apply. Rick must also **enter or be revealed**.
  **Consider splitting this clip in two** (`07a` turn-and-grab, `07b` freeze-and-drop);
  at ~6s for four beats plus a reveal it is the most likely clip in the scene to need
  retakes.
- **AUDIO**: 🔴 **POP-CRACKLE-ZZZZT electric discharge**, the chair hitting the floor, a
  **heavy body thud**, gasps.
- **NOTE**: Rick is deliberately absent from clips 1–6 to protect this reveal. Do not
  "fix" that.

---

### Clip 8 — `s3_08_have_you_killed_him`

- **SCRIPT**: `CHRIS (crouching down): "Have you killed him?"`
- **STILL HAS**: Chris crouched beside Jan looking up at Rick; Rick standing calm above;
  Jan on his back; broken window behind.
- **VIDEO MUST ADD**: Chris **crossing and crouching** (the script says "crouching
  down" — it is a movement), and **rolling Jan onto his back** if you want the 7→8
  position change explained on camera rather than implied.
- **AUDIO**: the line, and the room's shocked murmur starting to return.
- **NOTE**: Jan is face-down in clip 7 and on his back here. Deliberate — Chris turning
  him over to check is what the line implies. See `SCENE3_SHOT_LIST.md`.

---

### Clip 9 — `s3_09_rick_reply`

- **SCRIPT**: `RICK (calmly stowing Taser): "No relax, he will be out for a while. I
  knew this Taser would come in useful one day in this place. I think we need the
  police here..."` → `FADE OUT.`
- **STILL HAS**: Rick mid-stow of the yellow taser, talking; Chris crouched looking up;
  Jan out cold; crowd watching.
- **VIDEO MUST ADD**: the stow completing; Rick's total lack of urgency; possibly him
  reaching for a phone on the last line. **`FADE OUT` is the end of the episode** — the
  clip needs to hold a beat and fade, not cut hard.
- **AUDIO**: the **full three-sentence line** (see §1.2), deadpan. Murmuring crowd.
  Then silence into the fade.

---

## 🧾 Section 3 — Things in the IMAGES that the script does NOT specify

Recorded so a later pass does not "correct" them back out. All are deliberate.

| Invention | Where | Why |
|---|---|---|
| **Maureen** as the canteen worker | all counter shots | Script says generic `CANTEEN WORKER`; she is in the cast bible as one |
| **`extra_01`–`extra_04`** recurring crowd | every crowd shot | Otherwise the model invents a different set of colleagues per cut |
| **Jan's changed shirt and tie** (pale blue / dark red) | all | Scene 3 is `NEXT MORNING`, the only non-continuous scene |
| **Stack of meeting chairs by the window** | clips 6–7 | Motivates "a heavy meeting chair" existing in a canteen |
| **One pane broken, others intact** | clips 6–9 | Script says "the nearest window"; the plate is a glazed wall |
| **Jan on his back from clip 8** | clips 8–9 | Makes Chris's "have you killed him" check readable |

---

## ✅ Section 4 — Decisions needed before generating video

1. **Christina's sabotage (§1.1)** — add clip 0, voiceover, or drop? *Recommend: add.*
2. **Rick's full line (§1.2)** — confirm we use the fountain version, not the guide's
   trimmed one. *Recommend: fountain.*
3. **Split clip 7 (§ clip 7)** — four actions plus a reveal in ~6s is the highest-risk
   clip in the scene. *Recommend: split into 07a / 07b.*
4. **Jan's entrance (§1.3)** — fold into clip 2, or cut to him already at the counter?
5. **Chris placed in the crowd from clip 1 (§1.4)** — confirm, since it changes the
   clip 1 and clip 4 video prompts.

If 1 and 3 are both taken, Scene 3 becomes **11 clips**, not 9.

---

## 📐 Section 5 — Method reminders carried from Scene 2

- Clips 4, 6 and 7 are **start-frame/end-frame** generations, not single-reference
  ones. That is the whole reason their stills were anchored on aftermath.
- Reset the chain every 6–8 generations or at a natural cut.
- ~2.75 words/sec, 15s hard ceiling.
- Free image re-rolls are unlimited on `groovingmushroom1467`; **video is not free** —
  every clip below costs credits, so confirm the decisions in §4 first.
