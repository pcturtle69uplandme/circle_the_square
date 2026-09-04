# 🎬 SCENE 2 — EXPANDED VIDEO SCRIPT & COVERAGE AUDIT

> `INT. CORRIDOR / OPEN-PLAN FLOOR - CONTINUOUS` — `CTS_Featurette_Episode.fountain`
> L88–151.
>
> **Purpose**: same pass as `SCENE3_VIDEO_SCRIPT.md`. Per beat: (a) script verbatim,
> (b) what the adopted still shows, (c) **what the still cannot show and the video must
> supply**, (d) anything the script calls for that exists nowhere in the assets.
> Read before writing MiniMax H3 prompts — video costs credits, stills did not.
>
> Companions: `SCENE2_CONTINUITY_NOTES.md` (per-shot reasoning),
> `SCENE2_VIDEO_PLAN.md` (chaining/timing method).

---

## 🔴 Section 1 — The dialogue guide is materially wrong for this scene

`scene_dialogue_audio_guide.md` covers Scene 2 in **three** shots (06, 08, 09). The
scene actually has **ten** beats. Worse, where it does quote dialogue it has silently
rewritten it, and in one case that destroys the biggest joke in the episode.

### 1.1 The Inception gag is broken in the guide 🔴

**Fountain script — the actual exchange, four turns:**

> `JAN:` *"…So I have decided to call the project Inception."*
> `CHRIS (shouting to laughter):` ***"You're dreaming Jan!"***
> `JAN:` ***"What?!"***
> `CHRIS:` *"Inception is the name of a film about dreams Jan."*
> `JAN (flustered):` *"Oh, well it is also the name of this project."*

**Guide's version (L17–21) — three turns:**

> `@Jan:` *"I have decided to call the project Inception."*
> `@Chris:` *"Inception is the name of a film about dreams Jan!"*
> `@Jan:` *"Oh, well it is also the name of this project."*

The guide **deletes "You're dreaming Jan!" and "What?!"**. Those two lines *are* the
joke: the heckle is a double meaning, Jan misses it, and only then does Chris explain.
Cut them and Chris merely states a film fact — there is no gag left, just trivia.

**Use the fountain. All four turns.**

### 1.2 Jan's closing speech is paraphrased away 🔴

**Fountain:**

> *"Yes groan all you like, but I am the one with the most talent and skills to deliver
> this. It will add £50k to my salary as I simply add this role into my duties. I will
> let you know when more information is available, now GET BACK TO WORK!"*

**Guide:** *"The position has been filled... by me! It will add £50k to my salary! NOW
GET BACK TO WORK!"*

The guide loses *"I am the one with the most talent and skills"* (the character note),
*"as I simply add this role into my duties"* (the actual joke — he is doing two jobs
for one), and *"I will let you know when more information is available"* (corporate
non-answer). It also relocates the self-appointment, which belongs in the previous beat.

### 1.3 Also missing from the guide entirely

Seven of ten beats are unmentioned: Sharon's exit, Jan's clap and opening line, the
Sharon-pass evasion, the sniggering, the "SHUT UP!" flare-up, Rick's challenge about
the failing project, Jan's justification monologue, and the merch gag.

> **Standing rule, already learned once on this project**: work from
> `CTS_Featurette_Episode.fountain`, never from a summary guide. The guide is a rough
> audio sketch, not a source of truth.

---

## ⚠️ Section 2 — Script beats with no still anchor

### 2.1 Who opens the blinds? 🟡

Shot 06 ends with the blinds **lowered and shut opaque** and the door closed. Shot 07
opens with the door **open** and the blinds **raised**. Nothing shows the change.

Flagged as an open question in `SCENE2_CONTINUITY_NOTES.md` and still unresolved. The
plan there was to bridge 06→07 as a **single start/end keyframe generation** with
Sharon raising the blinds and opening the door as the connecting action, rather than a
jump cut. Confirm that before generating.

### 2.2 "Minutes later" 🟡

Script: *"**Minutes later**, Jan emerges (shirt re-buttoned askew) and claps his hands."*
There is a genuine time jump between clip 07 and clip 07b-1. Nothing marks it. Options:
a hard cut (fine, standard), or a brief hold on the corridor. Decide deliberately —
right now the two clips will chain as if continuous, which contradicts the script.

### 2.3 Jan's "What?!" reaction has no anchor 🔴

The Shot 08 still shows Chris **mid-heckle** only. The exchange needs Jan
uncomprehending ("What?!") and then flustered ("Oh, well it is also the name of this
project"). Neither state is anchored anywhere.

26 words ≈ 9.5s fits one clip, but that is **four speaker turns and two Jan reaction
beats** in under ten seconds. **Recommend splitting**:

| New clip | Content | Words | Est. |
|---|---|---|---|
| `08a` | Chris: "You're dreaming Jan!" → Jan: "What?!" | 6 | ~2.5s |
| `08b` | Chris explains → Jan flustered | 20 | ~7s |

The existing `shot08` still anchors `08a`. **`08b` would need one new still** (Jan
flustered, Chris mid-explanation) — free to generate. This renames the merch gag to
`08c`.

### 2.4 The Sharon-pass evasion is folded into one still 🟢

Jan's *"Err... yes she does. I have given her the rest of the day off for personal
reasons"* shares the `07b-1` still with his clap and opening line. Acceptable — it is
one continuous address — but the video prompt must cover Jan's shiftiness on "Err…",
which the still (chin up, self-important) does not show.

---

## 🎞️ Section 3 — Beat-by-beat expansion

Audio note: the video model generates its own audio, so every line and SFX below must
appear in the clip prompt. No separate TTS or foley pass exists.

---

### Clip 1 — `shot06_corridor_gossip`

- **SCRIPT**: `CHRIS: "Christ! They don't even try to hide it any more do they."` /
  `RICK (flat): "Never have. Give it another five minutes."`
- **STILL HAS**: Chris and Rick by the desk run, blinds shut opaque, door closed, nobody
  else in frame.
- **VIDEO MUST ADD**: Chris's nod toward the shut door; Rick's total non-reaction — the
  comedy is his flatness. Slow push-in or static.
- **AUDIO**: both lines. Chris smirking; Rick monotone. Low open-plan ambience.
- **NOTE**: Rick's **grey polo** is script-pinned and was wrong in the first pass. Keep.

---

### Clip 2 — `shot07_sharon_exits`

- **SCRIPT**: *"They watch Sharon leave Jan's room dripping in sweat, with dishevelled
  hair and makeup."*
- **STILL HAS**: Sharon mid-exit, dishevelled; Jan visible seated inside; Chris and Rick
  watching.
- **VIDEO MUST ADD**: 🔴 **the blinds being raised and the door opening** (§2.1) —
  otherwise the fixture state contradicts clip 1. Sharon walking toward camera,
  smoothing her blouse, not making eye contact.
- **AUDIO**: no dialogue. Door handle, footsteps, a snigger from Chris.

---

### Clip 3 — `shot07b1_jan_addresses`

- **SCRIPT**: *"Minutes later, Jan emerges (shirt re-buttoned askew) and claps his hands
  to gather everyone around."* → `JAN: "Right guys, as you know --"` →
  `CHRIS: "Does Sharon get a pass on attending this?"` → `JAN: "Err... yes she does. I
  have given her the rest of the day off for personal reasons."`
- **STILL HAS**: Jan mid-clap addressing the gathered crowd, shirt askew; Chris with hand
  half-raised; crowd calm and attentive.
- **VIDEO MUST ADD**: the **time jump** (§2.2); Jan emerging from the office; the
  **clap** as a sound and a gesture; the crowd gathering; and Jan's **shiftiness** on
  "Err…" (§2.4) — eyes away, a tug at the collar.
- **AUDIO**: the clap, Jan's line cut off mid-sentence, Chris's question, Jan's evasion.

---

### Clip 4 — `shot07b2_shut_up_flareup`

- **SCRIPT**: *"Quiet sniggering ripples through the assembled crowd of worker drones."*
  → `JAN (flushed): "SHUT UP! I am truly appalled by the lack of discipline in this
  place and that changes now! I have decided a new project is required to manage all the
  change around here."`
- **STILL HAS**: Jan mid-outburst, hands raised, flushed; crowd sniggering behind hands.
- **VIDEO MUST ADD**: the **ripple** — sniggering spreading person to person before Jan
  snaps. That progression is the beat and a still cannot carry it.
- **AUDIO**: 🔴 quiet sniggering building, then the shouted line cutting it dead.

---

### Clip 5 — `shot07c1_rick_questions`

- **SCRIPT**: `RICK: "What happened to the last project for this, isn't it ongoing? By
  that I mean completely failing."` → Jan begins his justification.
- **STILL HAS**: Rick arms folded and skeptical; Jan palm-up, patronising.
- **VIDEO MUST ADD**: Rick's deadpan delivery and the beat before "completely failing";
  Jan's smile curdling.
- **AUDIO**: Rick's line; Jan's opening justification.

---

### Clip 6 — `shot07c2_naming_inception`

- **SCRIPT**: *"…So I have decided to call the project Inception."*
- **STILL HAS**: Jan arm raised, triumphant; Rick unimpressed beside him.
- **VIDEO MUST ADD**: the presenting gesture landing; the crowd's flat non-reaction.
- **AUDIO**: the line, delivered as if announcing a moon landing.

---

### Clips 7–8 — the Inception exchange *(currently one clip; recommend two — §2.3)*

- **SCRIPT**: `CHRIS: "You're dreaming Jan!"` → `JAN: "What?!"` → `CHRIS: "Inception is
  the name of a film about dreams Jan."` → `JAN (flustered): "Oh, well it is also the
  name of this project."`
- **STILL HAS**: `shot08` — Chris heckling from across the room, crowd laughing, Jan
  turning, startled.
- **VIDEO MUST ADD**: 🔴 **Jan's two reaction beats, neither of which is anchored** —
  blank incomprehension on "What?!", then flustered climb-down. Also the laughter
  swelling on the heckle.
- **AUDIO**: all four lines plus crowd laughter. **Do not use the guide's three-line
  version (§1.1).**
- **NEEDS**: one new still for the flustered half if split.

---

### Clip 9 — `shot08b_merch_gag`

- **SCRIPT**: *"Jan realizes it is too late to change the name, as he has already ordered
  1,000 stress balls, pens, and t-shirts with 'PROJECT INCEPTION' printed on them."* →
  `CHRIS: "Will there be a lead for this?"` → `JAN: "At last something sensible is
  asked. Yes there will. However, it is with regret that I have to inform you all that
  the position has already been filled... by me."`
- **STILL HAS**: Jan with the open box, "PROJECT INCEPTION" legible on box, stress balls
  and t-shirts; Chris questioning.
- **VIDEO MUST ADD**: Jan's **realisation** — the dawning "oh no" as he looks at the box;
  the pause before "…by me"; the crowd's intake of breath.
- **AUDIO**: full line including *"At last something sensible is asked"* — the guide cuts
  it (§1.2).
- **NOTE**: script says **1,000** items. The still shows one box. Either accept it as
  the tip of the order, or have the camera find stacked boxes behind.

---

### Clip 10 — `shot09_1_groans`

- **SCRIPT**: *"GROANS echo from the crowd."* → `JAN: "Yes groan all you like, but I am
  the one with the most talent and skills to deliver this. It will add £50k to my salary
  as I simply add this role into my duties."`
- **STILL HAS**: crowd groaning and exasperated; Jan calm, smug, palm-down.
- **VIDEO MUST ADD**: the groan **starting** — it is a reaction to clip 9's reveal, so
  the clip should open on it.
- **AUDIO**: 🔴 collective groan; then Jan's full line — including *"as I simply add this
  role into my duties"*, which the guide drops and which is the actual joke.

---

### Clip 11 — `shot09_2_50k_outburst`

- **SCRIPT**: `JAN: "I will let you know when more information is available, now GET BACK
  TO WORK!"`
- **STILL HAS**: Jan mid-bellow, fist raised, flushed; crowd recoiling and turning away.
- **VIDEO MUST ADD**: the escalation from clip 10's calm smugness into the shout — the
  two clips are one continuous emotional move and should chain tightly.
- **AUDIO**: the line; chairs scraping as people disperse.

---

## 🧾 Section 4 — In the images but not in the script

| Invention | Why |
|---|---|
| `extra_01`–`extra_04` recurring crowd | Script says only "worker drones"; without fixed refs the crowd changes every cut |
| "JAN'S OFFICE" signage on the glass | Appeared in `07c-2`; kept per user decision 2026-09-04 |
| Rick's grey polo / Chris's light blue shirt | Actually **is** in the script's parentheticals — restated because the cast refs don't lock colour |
| One box of merch rather than 1,000 items | Practical framing choice |

---

## ✅ Section 5 — Decisions needed before generating video

1. **Use the fountain dialogue, not the guide** (§1.1, §1.2) — affects clips 7–11.
   *Recommend: fountain, all four Inception turns and Jan's full closing speech.*
2. **Split the Inception exchange into two clips** (§2.3)? Needs one new free still.
   *Recommend: yes.*
3. **Bridge 06→07 with Sharon opening the blinds** (§2.1)? *Recommend: yes — otherwise
   the fixture state contradicts itself.*
4. **How to mark "Minutes later"** (§2.2) — hard cut or held beat?
5. **Merch quantity** (clip 9) — one box, or find stacked boxes?

If 2 is taken, Scene 2 becomes **11 clips**, not 10.
