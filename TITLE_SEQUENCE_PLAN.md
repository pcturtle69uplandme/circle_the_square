# 📺 CIRCLE THE SQUARE — MAIN TITLE SEQUENCE

> **Status**: ⬜ PLANNED — nothing generated yet. This doc is the build spec.
> **Written**: 2026-08-12.
> **What it is**: the repeating main-title card for the mock TV show. The five principals walk out
> of The Triangle at dusk and pass the camera; the title lands in the air and holds.
> **Style**: 🎨 CARTOON — anchor in `CARTOON_CAST_BIBLE.md`. Cast identity from the Flow Character sheets.

---

## 1. 🔬 WHY THE LAST ATTEMPT FAILED — and the fix

The rejected take is Flow asset `1793b2a2` in project `f2f0d2c9`. It asked Veo for the cast **in prose**
("a heavy-set man in his early fifties…") **and** the title **and** the camera move, all in one
Ingredients-mode generation. It came back with the background reinvented, the style drifted off-model,
a crowd instead of five, and the title stamped at four different sizes and positions across the 8s.

That is not a prompt-wording problem. It is structural. **Flow's video composer has two modes and they
trade off against each other** (verified in-app 2026-08-12):

| Mode | Locks | Loses |
| :--- | :--- | :--- |
| **Frames** (first/last frame image) | background, architecture, colour, illustration style — perfectly | cast identity; people are generic and invented |
| **Ingredients** (Character entities) | cast identity from the model sheets | background and style — Veo composes a fresh scene |

Every one of the 25 working `T*` trailer clips used **Frames**. That is exactly why their architecture
and style never drifted. The failed title attempt used **Ingredients**, so it drifted — as designed.

### The fix: do it in two stages, in two different models

**You cannot get both from one generation. You can get both from two.**

- **Stage A — compose the frames as STILLS in Nano Banana 2** (image mode). Verified in-app: image mode
  accepts **all five Character entities *plus* the courtyard plate simultaneously** — six ingredients,
  none rejected. The still that comes out has the real building, the real cast, and the right style.
- **Stage B — animate those stills in Veo using Frames mode.** No characters attached, so nothing can
  drift. Veo only has to move the camera, which is the one thing it does reliably.

### ⚠️ The constraint that makes Stage A non-optional

Veo video mode allows **exactly one audio ingredient**, and **every saved Character carries its voice**.
Attach a second Character and Flow greys it out: *"Maximum audio ingredients reached (1 allowed)."*

**So a maximum of ONE cast member can ever be referenced in a single Veo generation.** Five leads in one
Veo take is not achievable by any prompt. Stage A is the only route to all five on model.

---

## 2. ✅ ASSET CHECK

| Need | Where | Status |
| :--- | :--- | :--- |
| 5 principal Character entities | Flow project `c1c8417d` (**08 Aug, 16:58**) | ✅ Jan, Christina, Sharon, Chris, Rick |
| Courtyard dusk plate | `L01_establishing_courtyard_dusk.jpg` — in project `f2f0d2c9` and on disk | ✅ |
| Cast model sheets (backup refs) | `character-refs/*_cartoon_sheet.jpg` | ✅ all 11 |
| Title renderer | `build_title_scroll.py` (PIL → PNG → ffmpeg overlay) | ✅ needs a "hold" mode adding |
| Assembly | ffmpeg | ✅ |

> **Characters live in a different project from the plates.** That is fine — the composer's asset picker
> has a project dropdown and picks across all three projects. Verified. Nothing needs duplicating.

---

## 3. 🎬 THE SCENE — layout

Dusk, the PRISM courtyard. Camera sits low and central on the paving, roughly where `T10` ends, looking
straight at the lit glazed entrance link. The building is warm and full of light; the courtyard is empty.

The doors open and the company comes out. They walk straight at the camera, growing as they come, and
pass either side of it and out of shot — **the camera never turns, they simply leave past it**. When the
last one is gone the courtyard is empty and lit again, and the title lands in the air over it.

**The joke**: the building is enormous and beautiful, and this is everyone who works in it. Six seconds
of grand architecture, and then the entire staff walks past you in three seconds.

**Cast order out of the doors** — Jan first, always, because he would be:

| Order | Who | Business as they pass |
| :-- | :--- | :--- |
| 1 | **Jan Peach** | Dead centre, chin up, on his phone, not looking where he is going. Passes camera left. |
| 2 | **Christina Dross** | Half a step behind him, unbothered, tablet under one arm. Passes camera right. |
| 3 | **Sharon Enfield** | Mid-conversation with Chris, not listening to him. Passes camera right. |
| 4 | **Chris** | Talking, throws bunny ears behind Rick's head as they pass. Passes camera left. |
| 5 | **Rick** | Arms crossed, entirely unaware of the bunny ears. Passes camera left. |

> Chris's bunny ears are the one gag. It already reads in `SCENE_group_photo_prism.jpg`, so it is
> established business, not a new invention.

### Shot breakdown — 12.0s core, extendable at the title

| # | Dur | Frame | Move | Title |
| :-- | :-- | :--- | :--- | :--- |
| **I1** | 3.0s | Empty courtyard, doors just opening, five small figures in the lit doorway | Very slow push in | — |
| **I2** | 3.0s | Jan and Christina at mid distance, the other three behind them | Continue push; they grow and exit frame left and right | — |
| **I3** | 3.0s | Sharon, Chris and Rick close, filling the lower frame | Continue push; all three pass the lens, bunny ears on the way | — |
| **I4** | 3.0s **+ hold** | Empty lit courtyard again, doors settling shut | Push slows and stops | **Title lands, freezes, holds** |

**I4 is the extendable one.** Its last frame is a clean, empty, symmetrical courtyard — freeze it and
hold the title over it for as long as the music bed needs. See §6.

> ### ✅ SUPERSEDED 2026-08-12 — one take does the whole thing
>
> The four-shot breakdown above was written as a risk hedge. **It is no longer needed.** The first
> Veo run (Frames mode, A1 as start frame, no end frame, Veo 3.1 Fast, x2) came back with the entire
> arc inside a single 8s take, both times:
>
> | Time | What is on screen |
> | :--- | :--- |
> | 0.0–3.5s | Five small at the lit entrance, walking out and growing |
> | ~4.2s | Full-length, mid-frame, all five clearly readable and on model |
> | ~6.1s | They pass either side of the lens and out of shot |
> | ~7.0–8.0s | **Empty lit courtyard** — the title bed, arrived at naturally |
>
> Nothing drifted: architecture, brick, glazing, dusk sky and illustration style all held for the full
> 8s, faces stayed on their model sheets, no extra people appeared, no lettering appeared.
>
> **So the build is: one Veo take + a composited title.** A1 is still needed (Stage A is what puts the
> real cast in the real courtyard), but A2/A3/A4 and shots I2/I3/I4 are not. Keep the four-shot
> breakdown only as a fallback if a future reroll refuses to clear frame in time.
>
> Validated takes: `c606c18a` (holds the group in frame longer — better cast read) and
> `44d8f370` (clears frame by ~5s — more clean tail for the title hold).

---

## 4. 🅰️ STAGE A — build the five stills (Nano Banana 2, image mode)

Five stills, because I4 needs both a start and an end frame. Work in project `f2f0d2c9`.

**Setup for every still**: attach the **five Character entities** (project dropdown → *08 Aug, 16:58* →
Characters) **and** `L01_establishing_courtyard_dusk.jpg`. Six ingredients. Model **Nano Banana 2**, 16:9.

### The Stage A template

```
Use the attached courtyard photograph as the EXACT background: same architecture, same brick,
same glazing, same dusk sky, same lighting, same illustration style, unchanged. Do not add or
invent any building, tower or structure anywhere in frame or on the skyline.

Place in it exactly <N> people and nobody else, drawn precisely from the attached character
sheets and matching them exactly in face, hair, build and wardrobe: <WHO AND WHERE>.

All wear burnt-orange PRISM lanyards. Stylised British sitcom comic art, clean bold line art,
flat muted colour palette, cel-shaded. NOT photorealistic.

Absolutely NO text, NO lettering, NO signage, NO captions anywhere in the image.
```

| Still | `<N>` | `<WHO AND WHERE>` |
| :--- | :-- | :--- |
| **A1** | 5 | all five small in the lit entrance doorway, just stepping out, Jan in front |
| **A2** | 5 | Jan and Christina at mid distance walking straight at the camera, the other three a few paces behind |
| **A3** | 3 | Sharon, Chris and Rick close to camera, chest-up, walking at the lens; Chris raising two fingers behind Rick's head |
| **A4** | 0 | *(no people — plate only, doors shut, courtyard empty and lit)* |

> **A4 needs no characters** — it is the closing frame. Generate it from the plate alone, or just use
> `L01_establishing_courtyard_dusk.jpg` unmodified. It is already exactly this image.

**Reroll rule**: if a face drifts off its model sheet, reroll the still. Do **not** proceed to Stage B
with a wrong face — Veo will faithfully animate the error.

---

## 5. 🅱️ STAGE B — animate (Veo, Frames mode)

**Frames mode, not Ingredients. Attach no characters.** With first *and* last frame set, Veo interpolates
between two images you control, which is far tighter than a first frame alone.

| Shot | First frame | Last frame | `<MOVE>` |
| :--- | :--- | :--- | :--- |
| I1 | A1 | A2 | very slow forward push across the courtyard |
| I2 | A2 | A3 | continue the forward push as they walk toward the lens |
| I3 | A3 | A4 | continue forward as the last of them pass either side of the lens |
| I4 | A4 | — | forward push slowing to a stop |

### The Stage B template

```
Animate this image with a single slow <MOVE>. Keep the exact architecture, materials, colours,
dusk lighting and illustration style of the source image completely unchanged. Do not add,
remove, redesign or move any structure, furniture or object. Do not add any people beyond
those already in the frame. Do not add text, signage or lettering of any kind. One continuous
camera move, no cuts, no speed changes. No dialogue, no speech, no singing.
```

**Non-negotiables**
- **No lettering from Veo, ever.** The title is composited in post (§6). This is settled: the rejected
  take proves Veo redraws the title every few frames and it will not hold still.
- **Discard Veo's audio track entirely** in the edit. Music goes on in post.
- **Trim from the head.** Same drift guard as the trailer — take the first ~3s of each 8s render.
- Max 8s per Veo clip; we only need 3s each.

---

## 6. 🔤 THE TITLE — fixed in the air, extendable

Rendered as real type, never generated. `build_title_scroll.py` already renders
`CIRCLE THE SQUARE` to a transparent PNG (Impact / Arial Black / Segoe UI Black, heavy white fill,
hard dark outline, drop shadow) and overlays it with ffmpeg.

**Change needed**: that script *scrolls the title off the top*. This sequence wants the opposite —
the title **arrives, stops, and stays**. Add a `--hold` mode:

1. Title rises from just below its rest position over ~0.5s and **stops dead** at ~46% frame height,
   sitting in the sky above the roofline — clear of the building, clear of the paving.
2. It **never moves again**.
3. `I4`'s final frame is held as a freeze, and the title holds over it for however long is wanted.

```
Runtime = 9.0s (I1–I3)  +  3.0s (I4 move)  +  N seconds of frozen hold
        = 12.0s core, extendable to any length without regenerating anything
```

That is the "extend it to last longer on screen" requirement — it becomes a single number in the build
script, not a new render.

**Placement check**: at 46% height the title sits against the dusk sky between the two brick wings.
That is the cleanest, flattest area of the frame and the heavy dark outline will hold against it.

---

## 7. 🛠️ ASSEMBLY

New script: **`build_title_sequence.py`**, following `build_cartoon_building_trailer.py` and reusing the
PNG renderer from `build_title_scroll.py`.

```
1. Trim I1..I4 from the head (HEAD_SKIP 0.2s), 3.0s each
2. Drop every Veo audio track
3. Scale/pad to 1920x1080, letterbox 2.39:1 to match the trailer masters
4. Concat I1..I4 as straight cuts - this is one continuous move, no fades
5. Freeze I4's last frame for N seconds
6. Overlay the title PNG: rise 0.5s, stop, hold to the end
7. Export clips/TITLE_SEQUENCE.mp4 (mute - music laid in post)
```

---

## 8. ☑️ PROGRESS TRACKER

| Stage | Item | Done |
| :--- | :--- | :-: |
| A | A1 — five in the doorway (**4 variants generated, all on model**) | ✅ |
| A | A2 — Jan and Christina mid | ➖ not needed, see §3 |
| A | A3 — Sharon, Chris, Rick close | ➖ not needed, see §3 |
| A | A4 — empty courtyard | ➖ not needed — the take arrives there itself |
| B | The single 8s take (`c606c18a`, `44d8f370`) | ✅ |
| — | Pick the keeper take | ⬜ |
| — | Download it at 1080p (*1K Original size*, not the 720p preview) | ⬜ |
| Post | `--hold` mode in `build_title_scroll.py` | ⬜ |
| Post | `build_title_sequence.py` | ⬜ |
| Post | Export | ⬜ |

---

## 9. 🔍 QC BEFORE IT GOES IN FRONT OF EVERY EPISODE

- [ ] **All five faces match their model sheets** — this repeats every episode, drift will be noticed.
- [ ] **Exactly five people.** No extras wandering in.
- [ ] **No London.** No skyline, no tower, no skyscraper behind the roofline.
- [ ] **No Veo lettering anywhere.** The only type in the piece is the composited PNG.
- [ ] **The title never moves once it stops**, and never changes shape.
- [ ] **The building is identical in all four shots** — same brick, same window grid, same sky.
- [ ] **The cut reads as one continuous forward move**, not four separate pushes.
- [ ] **Audio is silent** — no Veo dialogue, ambience or music survived into the master.
- [ ] Letterbox even; the title is not clipped by it.

---

## 10. ⚠️ GOTCHAS

Carried from `HANDOVER.md` §6 and `CARTOON_BUILDING_TRAILER_PLAN.md` §10, plus new ones from today:

- 🆕 **Veo allows 1 audio ingredient, and Characters carry voices** — so one cast member max per Veo
  generation. This is the constraint that shapes the whole plan.
- 🆕 **Frames vs Ingredients is the background/identity tradeoff.** Ingredients mode will always reinvent
  the background. Do not retry the title sequence that way.
- 🆕 **The asset picker reads across projects** via the dropdown top-left — Characters in `c1c8417d`,
  plates in `f2f0d2c9`, usable together.
- **Pressing Return in the composer attaches the previous image** instead of sending. Click Create.
- **Downloading hits a native Windows save dialog** automation cannot control — use the clipboard bypass.
- **The `<video>` src is Flow's 720p preview.** 1080p masters only come from *1K Original size* in the
  download menu. Decide before pulling these four down; a repeating title card wants the 1080p.
- **Window must be ≥1400px wide** or the composer sits under the sidebar and clicks land on Trash.

---

## 11. ❓ OPEN QUESTION

**Voice.** The brief said *"you do need voice as its a tv intro and i will fix in post with music"* —
read here as **no voice**, since music is going on in post and a title sequence has no dialogue. This
plan therefore strips Veo's audio entirely and delivers a mute master. If a voice-over *was* wanted
(an announcer over the titles), say so — it changes §5 and §7, and Jan's voice is already attached to
his Character entity and could carry it.
