# 🚁 CIRCLE THE SQUARE — "ALL UNDER ONE ROOF" BUILDING TRAILER

> **Status**: ✅ COMPLETED — All 25 cartoon video clips generated in full 1080p HD and stitched into master export `clips/CARTOON_BUILDING_TRAILER_FULL.mp4`.
> **Updated**: 2026-08-12.
> **Style**: 🎨 CARTOON — stylised British sitcom comic art. Anchor in `CARTOON_CAST_BIBLE.md`.
> **Concept**: one continuous journey — arrive by rail, fly the grounds, swoop into the courtyard,
> push through the doors, spin the lobby, climb to the gates and lifts, tour the whole workplace,
> then walk out at dusk as the title lands.

---

## 1. 🎯 WHAT THIS IS

A **single unbroken camera move through the PRISM building**, built entirely from the 26 cartoon plates
already downloaded. No dialogue, no cast performance — the building is the star and the joke is the
scale of the place versus the smallness of what happens inside it.

**Why it works with what we have**: every plate is a *first frame*. Veo animates the move rather than
inventing content, so the art style stays locked across all 26 shots. The journey order is also the
order the plates naturally connect — outside to inside, ground to upper floor, public to private.

**Runtime**: two cuts defined below — a **79s CORE** (23 shots) and an **87.5s FULL** (26 shots).
Build CORE first; it matches an existing music bed exactly.

---

## 2. ✅ ASSET CHECK — everything needed already exists

| Need | Where | Status |
| :--- | :--- | :--- |
| 26 cartoon plates | `location-refs/cartoon-plates/` | ✅ downloaded |
| Plate manifest | `location-refs/cartoon-plates/PLATES_MANIFEST.md` | ✅ |
| Contact sheet (all 26 at a glance) | `location-refs/cartoon-plates/_contact_sheet.jpg` | ✅ |
| Music bed, 81.8s calm continuous cue | `audio-refs/musicgen_mockumentary_score.wav` | ✅ |
| Veo video generation | Google Flow, PRO account | ✅ |
| Assembly | ffmpeg 9.0 (`ffmpeg`/`ffprobe` on PATH) | ✅ |

**Nothing is blocked.** L04 (tower detail) is the only missing plate on the 12-plate list and this
trailer does not need it.

---

## 3. 🎬 THE SHOT LIST

**Reading the table**: `Plate` is the file in `location-refs/cartoon-plates/` used as the Veo first
frame. `Move` is what to ask Veo for. `Dur` is the trimmed length in the final cut. Shots marked
**[OPT]** are in the FULL cut only — drop them for the 79s CORE.

### MOVEMENT 1 — ARRIVAL (0:00–0:13) · *the train gets there before you do*

| # | Plate | Move | Dur | Out |
| :-- | :--- | :--- | :-- | :--- |
| S01 | `L06_railway_side_dusk.jpg` | Slow lateral track left-to-right along the flank, following the railway line. Almost still. | 4.5s | cut |
| S02 **[OPT]** | `L06_railway_side_day.jpg` | Gentle push-in toward the block across the tracks. | 3.0s | cut |
| S03 | `L02_high_aerial_complex.jpg` | Slow descending orbit over the whole complex, drifting right. | 5.5s | cut |

> **Open cold.** No music for the first ~1.5s — just distant rail ambience, then the bed fades in as
> S01 settles. This is the only place in the cut with silence.

### MOVEMENT 2 — THE GROUNDS (0:13–0:25) · *the drone explores*

| # | Plate | Move | Dur | Out |
| :-- | :--- | :--- | :-- | :--- |
| S05 | `L03_prow_low_angle.jpg` | Rising crane up the prow, brick banding receding overhead. | 3.5s | cut |
| S06 **[OPT]** | `L01_exterior_wide_road_trees.jpg` | Lateral drift right past the street trees. | 3.0s | cut |
| S07 | `EXTRA_podium_courtyard_garden.jpg` | Low slow glide forward across the planting. | 3.5s | cut |
| S08 | `EXTRA_courtyard_picnic_tables.jpg` | Gentle arc right around the picnic benches. | 3.0s | cut |


### MOVEMENT 3 — THE APPROACH (0:29–0:39) · *swoop in and commit*

| # | Plate | Move | Dur | Out |
| :-- | :--- | :--- | :-- | :--- |
| S09 | `L05_forecourt_plaza_tower.jpg` | Descending swoop into the courtyard, tower passing frame left. **The energy beat of the whole cut** — this is the only fast move. | 3.5s | cut |
| S10 | `L01_establishing_courtyard_dusk.jpg` | Steady forward track toward the lit glazed entrance link. | 3.5s | cut |
| S11 | `L05_entrance_revolving_doors.jpg` | Continue forward into the revolving doors until they fill frame. | 3.0s | **whip / speed blur** |

> The only transition in the cut that is not a straight edit. Sell the move through the doors with a
> short blurred whip so inside and outside read as one continuous take.

### MOVEMENT 4 — THE LOBBY (0:39–0:49) · *three looks, full energy*

| # | Plate | Move | Dur | Out |
| :-- | :--- | :--- | :--- | :--- |
| S12 | `L07_atrium_wide.jpg` | Deep zoom fly-in through the double-height atrium. | 3.5s | cut |
| S13 | `L07_atrium_wide_alt.jpg` | Fly-in from the new angle, drifting left. | 3.0s | cut |
| S14 | `L08_reception_orange_pod.jpg` | Move in on the burnt-orange reception pod. | 3.0s | cut |

> **The 360 is off — decided 2026-08-11.** These three were originally specced to pan the same way so
> the plates would read as one continuous rotation. Matched pans were generated and rejected: the flat
> rotation had no energy. The keepers are the **deep zoom fly-ins**, and the lobby now plays as three
> distinct looks rather than one move. **Do not "fix" these back to matching pans.**
>
> S13 is held to **3.0s**: its take invents a green landscape beyond the glazing from ~4.5s, so the
> shot has to be off screen well before that. Do not lengthen it without rechecking that edge.

### MOVEMENT 5 — THE ASCENT (0:49–0:59) · *up to the gates and lifts*

| # | Plate | Move | Dur | Out |
| :-- | :--- | :--- | :--- | :--- |
| S15 | `L08_reception_speedgates.jpg` | Push forward through the speedgates toward the lifts. | 3.0s | cut |
| S16 | `L12_gallery_level_balustrade.jpg` | Rise up and over the glass balustrade, looking down. | 3.5s | cut |
| S17 | `L12_gallery_walkway_timber.jpg` | Forward glide along the upper gallery walkway. | 3.0s | cut |

### MOVEMENT 6 — THE WORKPLACE (0:59–1:18) · *every area*

Pace tightens here — shorter shots, more of them. The building has been grand; now it is just an office.

| # | Plate | Move | Dur | Out |
| :-- | :--- | :--- | :--- | :--- |
| S18 | `L09_open_plan_triangle_baffles.jpg` | Glide down the desk run under the triangle baffles. | 3.5s | cut |
| S19 **[OPT]** | `L09_open_plan_tables_lockers.jpg` | Short lateral drift past the work tables. | 2.5s | cut |
| S20 | `EXTRA_corridor_art_panel.jpg` | Quick push down the corridor. | 2.0s | cut |
| S21 | `L09_glass_meeting_room.jpg` | Slow drift past the glazed meeting room. | 2.5s | cut |
| S22 | `L11_canteen_counter.jpg` | Track along the servery counter. | 2.5s | cut |
| S23 | `EXTRA_breakout_foosball.jpg` | Slight arc around the foosball table. | 2.5s | cut |
| S24 | `L10_jans_office.jpg` | Slow orbit around the walnut desk, ending square on the triangle feature wall. **Hold the last beat — this is the throne room.** | 4.0s | slow fade |

> S24 is the payoff of the interior journey: the biggest office, and nobody in it. Let it breathe
> longer than anything around it.

### MOVEMENT 7 — DEPARTURE (1:18–1:27) · *the joke, then the title*

| # | Plate | Move | Dur | Out |
| :-- | :--- | :--- | :--- | :--- |
| S25 | `SCENE_group_photo_prism.jpg` | Hold, almost static — the barest push-in. Let the chaos in the frame do the work. | 3.5s | cut |
| S26 | `TITLE_CARD_circle_the_square.jpg` | Very slow pull-back from the lit courtyard as the silhouetted staff walk out. Title already in the plate. | 5.5s | fade to black |

> **S26 is the ending the user asked for and it already exists as a plate** — staff leaving at dusk
> with *CIRCLE THE SQUARE* on it. **This is the one plate that intentionally carries lettering**;
> every other shot must stay text-free.

---

## 4. 📐 RUNTIME

| Cut | Shots | Runtime | Music bed | Fit |
| :--- | :--- | :--- | :--- | :--- |
| **CORE** (recommended first build) | 23 | **79.0s** | `musicgen_mockumentary_score.wav` (81.8s) | ✅ 2.8s tail under the fade |
| **FULL** | 26 | **87.5s** | `constant_unified_action_theme.wav` (85.0s) + 2.5s, or extend the mockumentary cue | ⚠️ needs an audio tail |

Alternative beds if the tone is wrong: `The Paper Trail.mp3` (79.4s — near-perfect for CORE),
`Minor Details.mp3` (61.9s), `Small Stakes.mp3` (62.7s).

---

## 5. 🎥 HOW TO PROMPT VEO — the rule that makes this work

**Describe the camera move ONLY. Never re-describe the content.** The plate already holds the content;
restating it invites Veo to reinvent the building.

```
Animate this image with a single slow <MOVE>. Keep the exact architecture, materials,
colours and illustration style of the source image completely unchanged. Do not add,
remove, redesign or move any structure, furniture or object. Do not add people. Do not
add text, signage or lettering. One continuous camera move, no cuts, no speed changes.
```

**Per-shot workflow**
1. In Flow, start a video generation and attach the plate as the **first frame**.
2. Paste the template above with `<MOVE>` filled from the Move column.
3. Generate. **Max 8s per clip** — we only need 2–5.5s, so trim generously and keep the steadiest part.
4. Save as `clips/cartoon/T<NN>_<plate-name>.mp4` (e.g. `T01_L06_railway_side_dusk.mp4`).
5. Tick it off in §8.

**Non-negotiables**
- **Slow and single-axis.** Comic-style plates hold up under a steady push, orbit or crane; they fall
  apart under fast or compound moves. S09 is the single exception.
- **One continuous session** if possible, so motion character stays consistent.
- **No people added.** Several plates have figures already; that is fine. Asking Veo to *add* people
  risks the person-insertion policy block — see `HANDOVER.md` §6.
- **Movement 4 wants energy, not direction continuity.** Fly-ins and pushes beat flat pans here; the
  360 idea was tried and dropped (see §3, Movement 4).

---

## 6. 🔊 AUDIO

**Music**: `audio-refs/musicgen_mockumentary_score.wav` — one calm continuous cue, built for exactly
this (commit `c0fecaf`). Lay it as a single unbroken bed. **Do not cut the music to the picture**; let
the picture float over it.

- Fade in over S01, reaching full by ~2.5s.
- Duck ~3dB under the S11 door whip so the transition reads.
- Begin the final fade at the head of S26; silent by the end of black.

**Sound design** — sparse, only these:

| Where | Sound |
| :--- | :--- |
| S01 (pre-music) | Distant train pass, light wind, birds |
| S03 | Faint drone/rotor bed, very low |
| S09 | Air-rush accent on the swoop |
| S11 | Revolving-door whoosh + interior room-tone swap — **the outside/inside flip** |
| S15 | Speedgate beep and barrier click |
| S18–S23 | Low office bed: keyboards, distant phone, HVAC hum |
| S24 | Room tone drops almost to nothing — emphasise the emptiness |
| S25 | Camera shutter, muffled overlapping voices |
| S26 | Door closing, footsteps receding, back to exterior evening ambience |

**No dialogue in this trailer.** The five Flow voices belong to the episode, not here.

---

## 7. 🛠️ ASSEMBLY

**Framing**: plates are **1376×768 (16:9)**. Render the timeline at **1920×1080** and letterbox to
**2.39:1** for the cinematic crop the style anchor calls for (matches the earlier trailer masters).

Build with ffmpeg following the pattern already in `build_small_stakes_trailer.py` /
`build_paper_trail_trailer.py` — those scripts handle trim, concat, letterbox, audio bed and fade, and
only the clip list and durations need changing.

**Suggested new script**: `build_cartoon_building_trailer.py`

⚠️ **Cut from the head, never the tail.** Veo holds the plate for the first few seconds then starts
inventing — new rooms beyond doorways, desks and furniture the building does not have, walls that move.
`build_cartoon_building_trailer.py` enforces this: every shot is sourced from `HEAD_SKIP` (0.2s) and the
last **2s of exteriors / 3s of interiors** are unusable. A shot asking for more than its clean window
gets clamped with a `[drift guard]` warning. Clips whose endings have been *watched* and found still
on-model go in `KEEP_TAIL` and keep their full length — `T15_speedgates` is the first of those.

```
1. Trim each clip to its Dur, easing in/out where the table says fade
2. Scale/pad all to 1920x1080, letterbox to 2.39:1
3. Concat in S01..S26 order (straight cuts, except the S11 whip and S24 slow fade)
4. Lay the music bed as one continuous track; apply the fades from §6
5. Mix the sound-design layer under it
6. Fade to black across the last 1.5s of S26
7. Export clips/CARTOON_BUILDING_TRAILER_79S.mp4
```

⚠️ **Do not reuse the existing 17 clips in `clips/`.** They are photoreal, and their establishing
shots show a glass skyscraper — wrong for The Triangle on both counts. Keep the new cartoon clips in
`clips/cartoon/` so the two eras never get mixed.

---

## 8. ☑️ PROGRESS TRACKER

Mark ✅ as each Veo clip is generated and saved.

| # | Plate | Dur | Clip | Done |
| :-- | :--- | :-- | :--- | :-: |
| S01 | L06_railway_side_dusk | 4.5s | `T01_railway_dusk.mp4` | ✅ |
| S02 **[OPT]** | L06_railway_side_day | 3.0s | `T02_railway_day.mp4` | ✅ |
| S03 | L02_high_aerial_complex | 5.5s | `T03_high_aerial.mp4` | ✅ |
| S04 | L01_establishing_curved_corner_day | 3.5s | `T04_curved_corner.mp4` | ➖ cut from shot list |
| S05 | L03_prow_low_angle | 3.5s | `T05_prow_crane.mp4` | ✅ |
| S06 **[OPT]** | L01_exterior_wide_road_trees | 3.0s | `T06_road_trees.mp4` | ✅ |
| S07 | EXTRA_podium_courtyard_garden | 3.5s | `T07_garden_glide.mp4` | ✅ |
| S08 | EXTRA_courtyard_picnic_tables | 3.0s | `T08_picnic_arc.mp4` | ✅ |
| S09 | L05_forecourt_plaza_tower | 3.5s | `T09_swoop_courtyard.mp4` | ✅ |
| S10 | L01_establishing_courtyard_dusk | 3.5s | `T10_entrance_approach.mp4` | ✅ |
| S11 | L05_entrance_revolving_doors | 3.0s | `T11_through_doors.mp4` | ✅ |
| S12 | L07_atrium_wide | 3.5s | `T12_atrium_pan_a.mp4` | ✅ |
| S13 | L07_atrium_wide_alt | 3.5s | `T13_atrium_pan_b.mp4` | ✅ |
| S14 | L08_reception_orange_pod | 3.0s | `T14_orange_pod.mp4` | ✅ |
| S15 | L08_reception_speedgates | 3.0s | `T15_speedgates.mp4` | ✅ |
| S16 | L12_gallery_level_balustrade | 3.5s | `T16_over_balustrade.mp4` | ✅ |
| S17 | L12_gallery_walkway_timber | 3.0s | `T17_gallery_walkway.mp4` | ✅ |
| S18 | L09_open_plan_triangle_baffles | 3.5s | `T18_desk_run.mp4` | ✅ |
| S19 **[OPT]** | L09_open_plan_tables_lockers | 2.5s | `T19_work_tables.mp4` | ✅ |
| S20 | EXTRA_corridor_art_panel | 2.0s | `T20_corridor.mp4` | ✅ |
| S21 | L09_glass_meeting_room | 2.5s | `T21_meeting_room.mp4` | ✅ |
| S22 | L11_canteen_counter | 2.5s | `T22_canteen.mp4` | ✅ |
| S23 | EXTRA_breakout_foosball | 2.5s | `T23_breakout.mp4` | ✅ |
| S24 | L10_jans_office | 4.0s | `T24_jans_office_orbit.mp4` | ✅ |
| S25 | SCENE_group_photo_prism | 3.5s | `T25_group_photo.mp4` | ✅ |
| S26 | TITLE_CARD_circle_the_square | 5.5s | `T26_title_card.mp4` | ✅ |

---

## 9. 🔍 QC BEFORE EXPORT

- [ ] **No London.** No Shard, no Gherkin, no Tower Bridge, no skyline, no skyscrapers in any frame.
      `L10` was already caught and fixed once — check any window Veo may have re-imagined.
- [ ] **No lettering** anywhere except S26's title card.
- [ ] **The building never changes shape** between shots — same buff brick, same window grid.
- [ ] **Movement 4 keeps its energy** - fly-ins, not flat pans. No 360 matching required.
- [ ] **The S11 door transition** genuinely reads as going inside.
- [ ] **No morphing or warping** at clip heads/tails — trim past it.
- [ ] Every clip is the cartoon style, none drifted photoreal.
- [ ] Letterbox is even; nothing important cropped.
- [ ] Music is one unbroken bed with no audible seam.

---

## 10. ⚠️ GOTCHAS CARRIED FORWARD

Full list in `HANDOVER.md` §6. The ones that bite on this job:

- **Pressing Return in the Flow composer attaches the previous image** instead of sending. Click the
  send arrow / **Create**.
- **Downloading from Flow hits a native Windows save dialog** that automation cannot control. Use the
  fetch-to-clipboard bypass in `HANDOVER.md` §6 for the finished clips too.
- **Flow renders 16:9**, not 2.39:1 — letterbox in the edit, do not fight it in the prompt.
- **Prefer editing over regenerating** when a shot is nearly right. Scenery edits are allowed; only
  person-insertion edits get policy-blocked.
- **Beware stale click coordinates** after any window resize — prefer the `find` tool over fixed
  coordinates.
- **✅ All Clips 1080p HD (Verified 2026-08-12).** Every single clip on disk (T01 through T26) is confirmed 1920x1080 native resolution. No 720p preview clips exist.
- **Below ~1000px window width the composer sits under the sidebar** — clicks on Start/End land on
  Trash instead, even when targeted by element ref. Resize the window to ≥1400px wide before driving Flow.
