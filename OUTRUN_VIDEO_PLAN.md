# OUTRUN — FLASHBACK2047 music video: production plan

Flow project: **outrun** — `https://labs.google/fx/tools/flow/project/2f37a1bd-506c-4e95-8f94-ae1ca5e3b755`
Status: 6 source plates uploaded (2026-08-15). No video generated yet — awaiting sign-off on tier.

---

## 1. The assets

### Plates (`C:\kontitemp\ArtWorks`) — all 2752×1536 (1.792:1)

| ID | File | Look |
|---|---|---|
| **L1** | `FLASHBACK2047-OutRun-1.jpg` | **Riviera noon.** Monaco/Cap-Martin. Stone retaining wall + arch right, hillside town, sailboats and a white motor yacht on a deep-blue sea. Traffic: yellow coupé centre, dark sedan, black convertible right lane on a yellow French plate (`862 LW 06`). Big cumulus, hard midday light. |
| **L2** | `FLASHBACK2047-OutRun-2.jpg` | **Big Sur afternoon.** Tan cliffs right, white surf smashing rocks left, road S-bending right into the haze. Traffic: red coupé, silver sedan, dark sedan overtaking right. Exhaust flame. |
| **L3** | `FLASHBACK2047-OutRun-3.jpg` | **Golden hour.** Low sun on the water left, ochre villa + stone arch right, palm silhouettes, long shadow bars striping the tarmac. Warm amber grade. Traffic: red coupé, black sedan right. |
| **L4** | `FLASHBACK2047-OutRun-4.jpg` | **Night.** Full moon top-left with a glitter path on the sea, lit city towers centre-right, streetlamps, wet reflective asphalt with light streaks. Deep blue. Traffic: two cars ahead showing red tails. |
| **L5** | `FLASHBACK2047-OutRun-5.jpg` | **Ocean Ave noon.** Santa Monica. Tall palm colonnade both sides, white apartment towers right, green sign `OCEAN AVE 300 FT`. Traffic: red coupé, grey sedan, white coupé right. Exhaust flame. |
| **L6** | `FLASHBACK2047-OutRun-6.jpg` | **Sunset.** Full orange sky, sun on the horizon left, palm avenue converging to a dead-centre vanishing point, condo towers right. Near-monochrome orange. Traffic: three sedans right. |

### Music (`C:\kontitemp\Music`) — FLASHBACK2047 TURBO REMIX

| Track | Duration | Seconds |
|---|---|---|
| Magical Sound Shower | 3:16.5 | 196.52 |
| Passing Breeze | 2:43.6 | 163.56 |
| Splash Wave | 2:49.8 | 169.76 |
| Last Wave | 2:47.9 | 167.88 |
| **TOTAL** | **11:37.7** | **697.72** |

---

## 2. OutRun research → what it buys us

Sega, 1986, designed by **Yu Suzuki**; highest-grossing arcade game in the world by 1987. Facts that
change how we shoot this:

- **The car is a Ferrari Testarossa Spider** (an unlicensed open-top conversion) seen from a **fixed
  low rear third-person camera** — the plates already nail this. The camera in OutRun *never* cuts,
  orbits or changes height. That's not a stylistic choice we're making, it's the game's signature, and
  it happens to be exactly what kills drift. Lock the camera in every prompt.
- **Super Scaler sprite scaling**: the 3D is faked by scaling 2D sprites rushing toward the viewer at
  60fps. The visual read is *roadside objects exploding past the lens while the hero car stays pinned
  and razor-sharp*. Prompt for that contrast explicitly — blur the world, not the car.
- **15 stages over a branching 5-stage run** (Coconut Beach → … → Seaside Town / Lakeside /
  Autobahn), with **seamless stage-to-stage transitions** and no loading. Our six looks are effectively
  six stages, so cross-dissolving one look into the next *is* the authentic OutRun move.
- **Traffic is the core mechanic** — you dodge it against a timer, and "the road curves, crests and
  dips… obscuring upcoming traffic". An empty road is the one thing that would read as not-OutRun.
  This is why "always cars on the road" goes in every single prompt as a hard requirement.
- **The soundtrack is diegetic** — three tracks selectable on the in-car radio (*Passing Breeze*,
  *Magical Sound Shower*, *Splash Wave*). **"Last Wave" is not a driving track** — it plays on the
  final score / name-entry screen. So Last Wave belongs at the *end* of our film, over the night
  section. That ordering is canon, not taste.

Sources: [Wikipedia](https://en.wikipedia.org/wiki/Out_Run) ·
[Sega Wiki](https://sega.fandom.com/wiki/Out_Run) ·
[Hardcore Gaming 101](https://www.hardcoregaming101.net/outrun/) ·
[StrategyWiki route map](https://strategywiki.org/wiki/Out_Run) ·
[Hagerty on Yu Suzuki's road trip](https://www.hagerty.co.uk/articles/automotive-history/a-gearhead-programmer-an-epic-european-road-trip-and-the-creation-of-outrun/)

---

## 3. The anti-drift architecture

This is the part that matters most. Five rules:

1. **Every hero clip is a closed loop: first frame = last frame = the same uploaded plate.** In Flow,
   use *Frames to Video* and set **both** the start frame and the end frame to the identical plate.
   The model can only interpolate between two pinned images, so it is structurally incapable of
   drifting away from the look — it must return home by second 8. This also means **any clip of a given
   look can hard-cut to any other clip of that look invisibly**, because they all start and end on the
   same frame.
2. **Transitions are also pinned at both ends** — start frame = plate A, end frame = plate B. The whole
   film is therefore a chain of bounded segments; there is no point at which the model is free-running.
3. **Never use Extend, and never feed clip N's last frame into clip N+1.** That is exactly how drift
   compounds — each generation inherits the previous one's errors. Every clip goes back to the original
   uploaded JPG.
4. **One Style Bible preamble, byte-identical on every prompt** (§5). Variation lives only in the
   short beat line at the end.
5. **Explicit negatives on every prompt**, including "no empty road" and "no change to the car".

Bonus: because every clip returns to its master frame, the *entire film* can be made to loop —
add one `L4 → L5` transition (night back to noon) and it runs forever.

---

## 4. Duration maths and the three tiers

At **8s per clip with hard cuts**, filling 697.72s needs **89 clip-slots**:

| Section | Track | Duration | Looks | 8s slots | 10s slots |
|---|---|---|---|---|---|
| I | Magical Sound Shower | 196.52 | L5 → L1 | 25 | 20 |
| II | Passing Breeze | 163.56 | L2 | 21 | 17 |
| III | Splash Wave | 169.76 | L3 → L6 | 22 | 17 |
| IV | Last Wave | 167.88 | L4 | 21 | 17 |
| | | **697.72** | | **89** | **71** |

Two things that move that number:
- **If Flow gives you 10s clips, the slot count drops from 89 to 71** — worth checking on the first
  generation before batching.
- **1s crossfades cost ~11 extra clips** (each clip only contributes 7s of timeline). Hard cuts on the
  beat are both cheaper and more arcade-authentic; I'd crossfade only at the six look-changes.

Filling 89 slots does **not** mean generating 89 clips, because every clip is a seamless loop:

| Tier | Unique clips | Unique footage | Repeats per clip | Verdict |
|---|---|---|---|---|
| **A — Lean** | 12 (6 loops + 6 transitions) | 1:36 | ~14× | Too repetitive for 11½ min. Only if credits are tight. |
| **B — Balanced** ⭐ | **30** (24 hero + 6 transitions) | **4:00** | ~3.4× | **Recommended.** With 4+ variants per look and repeats spaced minutes apart, it reads as continuous driving. |
| **C — Full unique** | 89 | 11:38 | 0 | ~3× the cost of B for a difference most viewers won't clock. |

**Tier B hero allocation** — looks that carry a whole track alone get more variants:

| Look | Variants | Section | Slots | Uses per clip |
|---|---|---|---|---|
| L5 Ocean Ave noon | 3 | I | 12 | 4× |
| L1 Riviera noon | 3 | I | 12 | 4× |
| L2 Big Sur | **6** | II | 20 | 3.3× |
| L3 Golden hour | 3 | III | 10 | 3.3× |
| L6 Sunset | 3 | III | 10 | 3.3× |
| L4 Night | **6** | IV | 20 | 3.3× |
| **Transitions** | 6 | boundaries | 6 | 1× |

Transitions: `L5→L1` (inside I), `L1→L2` (I→II), `L2→L3` (II→III), `L3→L6` (inside III),
`L6→L4` (III→IV), `L4→L5` (end wrap, makes the film loop).

⚠️ **Mirroring and reverse playback are off the table** as cheap variety tricks — flipping puts the
traffic on the wrong side and mirrors the `OCEAN AVE` sign and the number plates; reversing makes the
cars drive backwards. Repeats have to be honest repeats. A ±4% speed offset on alternate uses is the
only safe disguise (and it's authentic — the arcade game recycled roadside sprites constantly).

---

## 5. The prompt engine

### 5.1 STYLE BIBLE — prepend verbatim to every single prompt

> 1980s Sega OutRun–inspired anime illustration, cel-shaded painterly key art, thick clean linework,
> saturated poster colours, 1986 arcade attract-mode energy. LOCKED CHASE CAMERA: a fixed low
> third-person view directly behind the car, camera height at boot level, the car centred in the lower
> third of frame and the horizon across the upper third. The camera never cuts, never orbits, never
> changes lens or height, and stays rigidly behind the car for the entire shot. Continuous forward
> travel at high speed, with strong horizontal motion blur on the tarmac and the roadside while the
> hero car itself stays razor sharp and perfectly still relative to the camera.

### 5.2 CAR LOCK — verbatim on every prompt

> Hero car: a red Ferrari Testarossa Spider convertible with the roof down, seen square-on from
> behind — two round tail lights each side (four in total) set into a black slatted rear grille panel,
> black lower valance, quad chrome exhaust tips, prancing-horse badge centred on the tail, black side
> strakes, five-spoke alloy wheels. The car's colour, shape, badges, wheels and proportions never
> change for a single frame. Two occupants seen from behind: a male driver in the left seat with short
> dark brown wavy hair, and a blonde female passenger in the right seat with long hair streaming in the
> slipstream. Neither turns toward camera and neither leaves the car.

### 5.3 ROAD & TRAFFIC LOCK — verbatim on every prompt

> The hero car stays on the tarmac inside its own lane at all times — all four wheels on the road
> surface, never on the verge, never airborne, never crossing the guardrail. AT LEAST THREE other
> vehicles are visible on the road at all times: period late-1980s sedans and coupés in the adjacent
> lanes and receding into the distance ahead, entering and leaving frame naturally as they are
> overtaken or as they pass. The road is a multi-lane coastal highway with crisp white dashed lane
> markings and a metal guardrail along the seaward side. The `FLASHBACK2047` wordmark stays fixed,
> static and legible in the bottom-left corner.

### 5.4 NEGATIVES — verbatim on every prompt

> No camera cuts, no scene changes, no change of time of day, no change of weather. No text, captions,
> subtitles, UI, HUD, logos or watermarks other than the existing bottom-left wordmark. No change to the
> car's colour or model. No empty road. No pedestrians or characters outside vehicles. No crashes, no
> spin-outs. No car exiting frame. No zoom or reframe. No morphing of the hero car or its occupants.
> No spoken dialogue and no music.

### 5.5 LOOP CLAUSE — on all 24 hero clips (omit on transitions)

> The shot begins and ends on the identical framing and identical vehicle positions so that it loops
> seamlessly and undetectably.

### 5.6 Per-look anchors

| Look | Anchor line |
|---|---|
| L1 | Mediterranean Riviera at midday under towering white cumulus; a pale stone retaining wall and an arched tunnel mouth on the right, a hillside town of white villas above, deep blue sea to the left with white sailboats and a motor yacht. |
| L2 | Big Sur / Pacific Coast Highway in the afternoon; raw tan cliffs on the right, white surf exploding over black rocks on the left, the highway S-bending away to the right into coastal haze. |
| L3 | Golden hour, the low sun sitting on the water to the left throwing a molten path across the sea; an ochre Riviera villa and stone arch on the right, palm silhouettes, long shadow bars striping the tarmac; warm amber grade. |
| L4 | Night; a full moon high on the left laying a glitter path on a dark sea, a skyline of lit city towers ahead on the right, sodium streetlamps, wet reflective asphalt streaked with light; deep blue palette, red tail lights ahead. |
| L5 | Santa Monica Ocean Avenue at midday; a colonnade of tall palms on both sides, white apartment towers on the right, a green highway sign reading OCEAN AVE 300 FT, brilliant cumulus over a turquoise Pacific. |
| L6 | Full sunset, the sun resting on the horizon to the left over the sea; an avenue of black palm silhouettes converging on a dead-centre vanishing point, condo towers on the right; near-monochrome burnt-orange grade. |

### 5.7 Beat lines — the only thing that varies

| Beat | Line |
|---|---|
| **A Cruise** | Steady high-speed cruise holding the centre lane; the roadside streaks past, two cars are overtaken on the right, the passenger's hair whips in the wind. |
| **B Overtake** | The hero car drifts one lane to the right, sweeps past a slower sedan, then settles back into its original lane and exact original position by the end of the shot. |
| **C Curve** | The highway sweeps into a long bend; the car leans into it and straightens back to dead centre, the guardrail and roadside rushing past on the outside of the turn. |
| **D Surge** | A burst of throttle — the exhausts flare, the motion blur intensifies and the traffic ahead is reeled in, then the speed settles back exactly where it started. |
| **E Crest** | The road crests a rise and dips, briefly hiding then revealing the traffic ahead, before levelling back to the opening framing. |
| **F Pack** | Traffic thickens — four or five cars in the lanes ahead and alongside — and the hero car threads between them, returning to clear centre lane by the end. |

**Worked example (clip `L5-A`), the whole thing assembled:**

> *[5.1 Style Bible]* *[5.2 Car Lock]* Santa Monica Ocean Avenue at midday; a colonnade of tall palms on
> both sides, white apartment towers on the right, a green highway sign reading OCEAN AVE 300 FT,
> brilliant cumulus over a turquoise Pacific. Steady high-speed cruise holding the centre lane; the
> roadside streaks past, two cars are overtaken on the right, the passenger's hair whips in the wind.
> *[5.3 Road & Traffic Lock]* *[5.5 Loop Clause]* *[5.4 Negatives]*

Transitions swap the loop clause for, e.g.:

> The shot begins on the golden-hour coast road and the light deepens continuously into full sunset
> across the eight seconds, the sun dropping to the horizon and the palms going to silhouette — one
> unbroken take with no cut, the camera and the car never changing position in frame.

---

## 5.8 Clip manifest — the 30 generations (Tier B)

Every hero clip is `first frame = last frame = its plate`. Generate in this order; tick as approved.

| # | Clip ID | Plate | Beat | Approved | Downloaded |
|---|---|---|---|---|---|
| 1 | `L5-A` | OutRun-5 | A Cruise | ☐ | ☐ |
| 2 | `L5-C` | OutRun-5 | C Curve | ☐ | ☐ |
| 3 | `L5-F` | OutRun-5 | F Pack | ☐ | ☐ |
| 4 | `L1-A` | OutRun-1 | A Cruise | ☐ | ☐ |
| 5 | `L1-B` | OutRun-1 | B Overtake | ☐ | ☐ |
| 6 | `L1-D` | OutRun-1 | D Surge | ☐ | ☐ |
| 7 | `L2-A` | OutRun-2 | A Cruise | ☐ | ☐ |
| 8 | `L2-B` | OutRun-2 | B Overtake | ☐ | ☐ |
| 9 | `L2-C` | OutRun-2 | C Curve | ☐ | ☐ |
| 10 | `L2-D` | OutRun-2 | D Surge | ☐ | ☐ |
| 11 | `L2-E` | OutRun-2 | E Crest | ☐ | ☐ |
| 12 | `L2-F` | OutRun-2 | F Pack | ☐ | ☐ |
| 13 | `L3-A` | OutRun-3 | A Cruise | ☐ | ☐ |
| 14 | `L3-C` | OutRun-3 | C Curve | ☐ | ☐ |
| 15 | `L3-D` | OutRun-3 | D Surge | ☐ | ☐ |
| 16 | `L6-A` | OutRun-6 | A Cruise | ☐ | ☐ |
| 17 | `L6-B` | OutRun-6 | B Overtake | ☐ | ☐ |
| 18 | `L6-E` | OutRun-6 | E Crest | ☐ | ☐ |
| 19 | `L4-A` | OutRun-4 | A Cruise | ☐ | ☐ |
| 20 | `L4-B` | OutRun-4 | B Overtake | ☐ | ☐ |
| 21 | `L4-C` | OutRun-4 | C Curve | ☐ | ☐ |
| 22 | `L4-D` | OutRun-4 | D Surge | ☐ | ☐ |
| 23 | `L4-E` | OutRun-4 | E Crest | ☐ | ☐ |
| 24 | `L4-F` | OutRun-4 | F Pack | ☐ | ☐ |
| 25 | `T5-1` | 5 → 1 | noon Santa Monica dissolving into noon Riviera | ☐ | ☐ |
| 26 | `T1-2` | 1 → 2 | Riviera cliffs opening out into Big Sur surf | ☐ | ☐ |
| 27 | `T2-3` | 2 → 3 | afternoon warming down into golden hour | ☐ | ☐ |
| 28 | `T3-6` | 3 → 6 | golden hour deepening into full sunset | ☐ | ☐ |
| 29 | `T6-4` | 6 → 4 | sunset burning out into moonlit night | ☐ | ☐ |
| 30 | `T4-5` | 4 → 5 | night lifting to dawn-bright noon *(end wrap — optional)* | ☐ | ☐ |

## 5.9 Storyboard / EDL — 89 slots across 11:37.7

Hard cuts within a section; 1s crossfade only on the `T` transitions. Times are cumulative.

### Section I — *Magical Sound Shower* · 196.52s · 25 slots · noon
| Slots | In → Out | Content |
|---|---|---|
| 1–12 | 0:00 → 1:36 | **L5** Ocean Ave. `A C F A C F A C F A C F` — palms, OCEAN AVE sign, opening statement |
| 13 | 1:36 → 1:44 | **`T5-1`** ⤫ Santa Monica → Riviera |
| 14–25 | 1:44 → 3:16.5 | **L1** Riviera. `A B D A B D A B D A B D` — yachts, stone arch, French plates. Last slot trimmed 3.5s |

### Section II — *Passing Breeze* · 163.56s · 21 slots · afternoon
| Slots | In → Out | Content |
|---|---|---|
| 26 | 3:16.5 → 3:24.5 | **`T1-2`** ⤫ Riviera → Big Sur |
| 27–46 | 3:24.5 → 6:00 | **L2** Big Sur. `A B C D E F` ×3 + `A B` — the S-bend track, surf, cliffs. Last slot trimmed 4.4s |

### Section III — *Splash Wave* · 169.76s · 22 slots · golden hour → sunset
| Slots | In → Out | Content |
|---|---|---|
| 47 | 6:00 → 6:08 | **`T2-3`** ⤫ Big Sur → golden hour |
| 48–57 | 6:08 → 7:28 | **L3** Golden hour. `A C D A C D A C D A` — shadow bars, molten sea |
| 58 | 7:28 → 7:36 | **`T3-6`** ⤫ golden hour → sunset |
| 59–68 | 7:36 → 8:50 | **L6** Sunset. `A B E A B E A B E A` — palm avenue, vanishing point. Last slot trimmed 6.2s |

### Section IV — *Last Wave* · 167.88s · 21 slots · night
| Slots | In → Out | Content |
|---|---|---|
| 69 | 8:50 → 8:58 | **`T6-4`** ⤫ sunset → night |
| 70–89 | 8:58 → 11:37.7 | **L4** Night. `A B C D E F` ×3 + `A B` — moon path, city towers, wet asphalt. Ends on the game's score-screen theme |
| *(wrap)* | — | **`T4-5`** if the film is to loop back to the top |

**Repeat spacing check:** within a section, the same clip never recurs closer than 3 slots (24s) and
usually 6 (48s); across the film no clip appears in two different sections. That's the margin that makes
3–4 reuses read as continuous driving rather than as a looping GIF.

---

## 6. Stitching on the laptop

`ffmpeg 9.0` and `python 3.12` are already on this machine, so I can build the assembly rather than
hand you 30 loose files.

- **Strip Veo's generated audio** on every clip (`-an`) — Veo 3 adds engine/ambience that will fight the
  remixes.
- **Cut on the beat.** All four tracks are steady-tempo remixes; I'll detect BPM and snap every cut to a
  bar line so the loop points land musically instead of at an arbitrary 8.000s.
- **Hard cuts within a section, 1s crossfade at the six look-changes** (`xfade`).
- **Overlay a clean static `FLASHBACK2047` wordmark** bottom-left over the whole film. Veo will very
  likely smear or wobble the baked-in one; a crisp overlay hides that. If it comes out clean, we drop
  the overlay.
- Output: **one continuous 11:37 film**, or four standalone videos (one per track), or both.
- Aspect note: the plates are 1.792:1 and Veo outputs 16:9 (1.778:1) — about a 1% side crop. Invisible.

---

## 7. Decisions — SIGNED OFF 2026-08-15

1. **Tier B — 30 clips.** 24 hero loops + 6 transitions, ~3.4× reuse. ✅
2. **Both deliverables**: one continuous 11:37 film *and* four standalone per-track videos, built from
   the same 30 clips. ✅
3. **Track order**: day-cycle, *Last Wave* last. ✅

## 9. Vehicle identification and reference assets (2026-08-16)

### What the hero car actually is
Zoomed to native resolution, the tail panel carries a garbled `TESTAROSSA` on the left and `FERRARI`
on the right with a prancing horse centred — but **the geometry is not a real Testarossa**. A real
Testarossa hides its tail lights *behind* the full-width black slat grille; here four round lights sit
exposed and outboard of it, over a louvred engine cover. That's Mondial t Cabriolet / 348 territory.
It's an OutRun-flavoured composite — which is period-correct, since the arcade car was itself an
unlicensed "Spider" conversion.

**This changed the prompt.** The car block used to say *"red Ferrari Testarossa Spider"*. Naming a real
model invites the video model to *correct* the car toward the real thing — i.e. to cause exactly the
drift we're trying to prevent. The block now describes **geometry only** and names no model. It also
keeps brand words out of the prompt, which the content filters prefer.

### Other vehicles
| Plate | Vehicle | Identification |
|---|---|---|
| L1 | black convertible, right lane | 1990s roadster, tan leather, yellow French plate `862 LH 06` (06 = Alpes-Maritimes) |
| L5 | white coupé, right lane | late-1980s Japanese wedge coupé — RX-7 FC / Supra A70 lineage |
| L1 | yellow coupé | too small to identify |
| L2/L3/L6 | dark sedans | generic late-80s/90s three-box sedans, too motion-blurred to identify |

**Recommendation: do not build assets for the traffic.** They are small, distant, heavily motion-blurred
and *deliberately* vary from clip to clip. Locking them would burn ingredient slots and QA time for no
visible gain. A one-line prompt description covers them.

### Reference assets built — from the plates themselves
Style-match is guaranteed **by construction**: these are the artist's own pixels, not a photo and not a
fresh generation. A photoreal Ferrari reference would drag the whole look toward photorealism.

| File | What it is |
|---|---|
| `refs/HERO_CAR_SHEET.png` | 2748×1156 — six rear views of the hero car, one per plate, across all six lighting conditions. No lettering (a reference with text invites the model to render text). |
| `refs/HERO_CAR_REAR.png` | 1928×1116 — the single cleanest isolated rear view (from L1: largest, sharpest, most evenly lit). |

Built by `scratch/build_car_sheet.py`. Rear is the only angle the film ever shows, so rear-only
coverage is complete coverage.

### ⚠️ The six plates do not depict an identical car
Laying the six crops side by side makes this obvious, and it caps what "no drift" can mean:

- **Exhaust tips** differ — L1 and L4 show four distinct chrome tips; L2/L5/L6 read as two fatter pairs.
- **Tail light colour** differs — L1's outer lights are amber, elsewhere they're all red.
- **Proportions** differ — L3 and L6 are noticeably wider and lower than L1.
- **Tail lettering** is garbled differently on every single plate.

Consequence: **within** a clip we are fine, because each clip is anchored to one plate and never mixes.
The shift only shows **across the six transitions**, where plate A's car becomes plate B's car — and
that is masked by the light changing at the same moment. Fixing it properly would mean repainting the
plates to a single car design; not worth it for a 1% side-crop-level artefact.

### Should the hero car be a Flow Character?
**Worth testing on `L5-A`, but it is a supplement, not a redesign.** Two unknowns to resolve empirically:

1. Flow's Character entities are people-oriented — unverified whether they accept a vehicle at all.
2. Unverified whether *Frames to Video* mode accepts an extra Character ingredient alongside its start
   and end frames.

And the honest framing: Frames-to-Video already pins both endpoints to the plate, which is a **stronger**
constraint than a Character reference. A Character could only help the middle ~7 seconds. So: try it on
the first clip, measure with `qa_clip.py` against a no-Character control, keep it only if the car
stability score actually improves.

## 10. QA harness

`qa_clip.py <clip.mp4> <plate.jpg>` scores each clip and exits 0=PASS / 1=REVIEW / 2=FAIL.

| Check | Catches | Fail threshold |
|---|---|---|
| Endpoint fidelity | did the frame pinning hold | SSIM < 0.80 vs plate |
| Loop closure | will it cut clean | SSIM < 0.85 first vs last |
| Car stability | morph / colour shift, with worst timestamp | SSIM < 0.70, or colour drift > 0.10 |
| Pop detection | **new cars, new roads** appearing from nowhere | delta spike z > 6 AND > 0.004 absolute |
| Speed | car looks parked; or eases out and "brakes" at every loop point | energy < 0.010, or ease-out ratio < 0.70 |

Validated both ways: a clean clip scores 0.998 endpoints / 0.9999 loop → PASS; a deliberately drifting
one → FAIL naming "last frame does not match plate", "loop closure poor", "hero car morphs at t=5.0s".

## 11. Execution order once approved

1. Generate **one** clip (`L5-A`) → review it → confirm the real credit cost per clip before batching.
2. Batch the remaining hero loops, look by look, QA'ing each against the plate for drift.
3. Generate the 6 transitions.
4. Download all at max resolution (watch for the Chrome download-manager deletion issue — see
   `.agents/rules/browser_automation_cdp.md`).
5. Build the ffmpeg assembly, mux the music, review, iterate.
