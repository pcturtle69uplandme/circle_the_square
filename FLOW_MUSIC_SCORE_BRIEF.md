# 🎵 FLOW MUSIC SCORE BRIEF v2 — "ALL UNDER ONE ROOF" CARTOON BUILDING TRAILER

> **For**: Google Flow Music (https://www.flowmusic.app/) — paste the two prompts in §3.
> **Picture**: `clips/CARTOON_BUILDING_TRAILER_2X_FLOW_MUSIC.mp4` — **98.5s**, 25 shots, no dialogue.
> **v2 change (2026-08-12)**: the track join moved from 0:51.5 to **0:40.0 — the exact moment
> the camera comes through the revolving doors**. The outside→inside mood flip is now
> guaranteed by two genuinely different tracks, not by asking one track to change mood
> at a timestamp (Flow did not honour that in v1).
> Track 1 = **0:00–0:40.0 (exterior journey)**, Track 2 = **0:40.0–1:38.5 (interior)**.
> **Drop finished files into** `audio-refs/` as `track1.mp3` / `track2.mp3`.

---

## 1. 🎭 THE CORE IDEA — two moods, one door

| | TRACK 1 — OUTSIDE | TRACK 2 — INSIDE |
| :--- | :--- | :--- |
| World | Sky, railway, grounds, approach | Lobby, lifts, desks, offices |
| Mood | Open, airy, curious, a little grand | Bright, busy, self-important corporate bounce |
| Texture | Clarinet + piano lead, strings, light kit | Pizzicato + marimba drive, muted trumpet, fuller kit |
| Feels like | A nature documentary about a building | The sitcom actually starting |

The listener must **hear the door**. Track 1 ends hanging (unresolved, mid-anticipation);
Track 2 enters immediately brighter and busier. The build script crossfades them over
2s centred on 0:40.0 — the exact frame the atrium appears.

Shared DNA so it still reads as one score: same key (F major), same ~106 BPM, same
instrument family. The difference is energy and density, not a new universe.

---

## 2. ⏱️ TIME INDEX

### TRACK 1 — 0:00 to 0:40.0 (generate ≥40s; script trims at 40.0s)

| Time | Shots | Picture | Music |
| :--- | :--- | :--- | :--- |
| 0:00–0:02.5 | T01 railway dusk | Cold open, almost still | **Silence → fade in**: lone clarinet over soft piano |
| 0:02.5–0:13.5 | T02–T03 railway day, high aerial | The whole complex revealed | Theme statement: strings + clarinet melody, upright bass enters |
| 0:13.5–0:28.5 | T05–T08 prow, road, garden, picnic | Drone explores the grounds | Settle into an easy groove: brushed kit joins, curious and open |
| 0:28.5–0:32.5 | **T09 swoop into courtyard** | The one fast move | **Accent swell at 0:28.5** — one bar of excitement, then back |
| 0:32.5–0:40.0 | T10 approach, T11 revolving doors | Committing to the entrance | Rising anticipation, then **stop on an unresolved hanging chord at 0:40.0 — do NOT resolve**. The next track resolves it. |

### TRACK 2 — 0:40.0 to 1:38.5 (generate ≥58.5s; script trims at 58.5s)

Times below are **track-relative** (0:00 in Flow = 0:40.0 in the trailer).

| Track time | Trailer time | Shots | Picture | Music |
| :--- | :--- | :--- | :--- | :--- |
| 0:00–0:11.0 | 0:40.0–0:51.0 | T12–T14 atrium fly-ins, orange pod | Three energetic lobby looks | **Enter bright and busy from bar 1** — the mood flip. Fullest texture: pizzicato drive, marimba, muted trumpet, corporate bounce |
| 0:11.0–0:21.5 | 0:51.0–1:01.5 | T15–T17 speedgates, balustrade, walkway | Ascent to upper floor | Lighten slightly, keep the forward motion |
| 0:21.5–0:40.5 | 1:01.5–1:20.5 | T18–T23 desks, corridor, meeting room, canteen, breakout | The actual workplace | **Comic monotony**: repetitive typing-like marimba/pizzicato ostinato, the daily grind as a groove |
| 0:40.5–0:45.0 | 1:20.5–1:25.0 | T24 Jan's office orbit | The throne room, empty | **Pull almost everything out** — soft strings/piano, lots of air; the emptiness is the joke |
| 0:45.0–0:53.0 | 1:25.0–1:33.0 | T25 group photo (8s hold) | Cast chaos, near-static | Warm re-entry: full theme, affectionate |
| 0:53.0–0:58.5 | 1:33.0–1:38.5 | T26 title card | Pull-back, dusk, **CIRCLE THE SQUARE** | Final cadence, resolve fully, **fade to silence over the last 3s** |

---

## 3. 📋 FLOW MUSIC PROMPTS — paste these

### Track 1 (exterior, 40s) → save as `audio-refs/track1.mp3`

```
British mockumentary sitcom score, cartoon comedy — EXTERIOR mood. Open, airy and
curious, like a nature documentary about an office building. Solo clarinet lead over
soft piano, warm strings, upright bass, light brushed kit. ~106 BPM, F major.
Starts almost bare and grows in small steps. One short accent swell at 0:28 (two
seconds of excitement, then back to wry). From 0:32 build gentle rising anticipation
and END ON AN UNRESOLVED HANGING CHORD at 0:40 — do not resolve the final cadence,
leave it suspended mid-air. Acoustic instruments only, nimble and understated,
never epic, never sad, no synths, no vocals. Instrumental, 40 seconds, one
continuous cue.
```

### Track 2 (interior, 58.5s) → save as `audio-refs/track2.mp3`

```
British mockumentary sitcom score, cartoon comedy — INTERIOR mood, the show actually
starting. Enter BRIGHT AND BUSY from the very first bar: pizzicato string drive,
marimba, muted trumpet, brushed kit, self-important corporate bounce. Same world as
before (~106 BPM, F major) but noticeably more energetic and dense. Hold that energy
to 0:11, ease slightly with forward motion to 0:21. Then a busier repetitive
section: typing-like marimba and pizzicato ostinato, the comic monotony of office
work, until 0:40. At 0:40 strip almost everything away — soft strings and piano
only, lots of air, for 5 seconds. At 0:45 the full theme returns warmly. Final
cadence resolves at 0:53, then fade to silence over the last 3 seconds. Acoustic,
wry, never epic, no synths, no vocals. Instrumental, 58 seconds, one continuous cue.
```

> ⚠️ Generate slightly long if unsure (45s / 60s+) — the script trims each track at
> the join with a 2s crossfade. Never loop a short track.
> ⚠️ The mood flip is carried by the **two files being different**, so keep both
> prompts' mood words intact even if you tweak instrumentation.

---

## 4. 🔌 AFTER GENERATION

1. Save both files into `C:\AI\Circle the Square\audio-refs\` as `track1.mp3` and
   `track2.mp3` (overwrite the v1 files).
2. `build_cartoon_building_trailer.py` already points at those names and now joins
   at **40.0s** — nothing to edit unless the filenames differ.
3. Re-run: `python build_cartoon_building_trailer.py`
4. The script re-times both beds, crossfades them at the door moment, keeps the
   swoop/door ducking and the SFX layer (T18 stays muted) — nothing else to change.
