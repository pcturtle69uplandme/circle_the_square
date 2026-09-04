# 🎬 SCENE 3 — STAFF RESTAURANT / CANTEEN

> `INT. STAFF RESTAURANT / CANTEEN - NEXT MORNING` — `CTS_Featurette_Episode.fountain`
> L152–196, the final scene. Companion to `SCENE2_CONTINUITY_NOTES.md`; same method,
> same pipeline.

## Location — new, built 2026-09-04

Scene 3 is the third distinct location in the script and the first that had **no
photoreal plate**. What existed (`location-refs/cartoon-plates/L11_canteen_counter.jpg`,
`canteen_location_sheet.jpg`, `clips/cartoon/T22_canteen.mp4`) is all from the archived
cartoon pivot, not the live route.

Three plates in `location-refs/higgsfield/coverage/staff_canteen/`, defined in
`higgsfield-tools/browser/location_shots.js`:

| Plate | Role |
|---|---|
| `staff_canteen_master_wide` | The anchor. Text-to-image, **no references** — nothing can contaminate it. Every Scene 3 prompt attaches this. |
| `staff_canteen_servery_counter` | Jan's exchange with Maureen. Establishes the empty pastry trays and the china stacks he later sweeps. |
| `staff_canteen_window_wall` | Establishes the intact glazing Jan hurls a chair through, and the stack of heavy meeting chairs he takes it from. |

**All three adopted 2026-09-04.** One lesson worth keeping: the window wall needed a
re-roll because asking for a new camera angle while also saying "reproduce the
reference exactly" simply returns the reference — the first attempt handed back the
master's composition with a chair stack added. Stating the camera *move* ("turned 90
degrees right… the servery counter is now BEHIND the camera and must NOT be visible")
fixed it. Describe what leaves the frame, not just what enters it.

The master wide is text-to-image and the other two chain off it, deliberately: the
`jan_office_corridor` set was ruined by deriving angles from layout text alone (see
`location-refs/higgsfield/_archive-corridor-meetingroom-wrong/WHY_ARCHIVED.txt`), and
only the text-to-image master survived that.

**Design decision**: the canteen sits in the double-height atrium with a full-height
glazed wall, consistent with `LOCATION_PLATE_SHOT_LIST.md` L07 ("canteen tables below")
and L11 ("stainless servery, timber-fronted counter"). The glazing matters dramatically
— the chair-through-the-window beat needs a real glass wall, not a punched window.

## Cast — no new references needed

The script's `CANTEEN WORKER` is **Maureen**, already in the cast bible as *"a 58-year-old
British woman, Maureen, a canteen worker… beige apron over a white polo shirt"*, with a
full ref set in `character-refs/higgsfield/maureen/`. Jan, Chris, Rick and
`extra_01`–`extra_04` all carry over from Scene 2 unchanged.

**Wardrobe is NEXT MORNING** — this is the one scene that is not continuous with the
others. Jan should be in a *different* shirt/tie from Scenes 1–2 (still badly worn), and
the crowd may vary. Chris's light blue shirt and Rick's grey polo are script-pinned
identifiers, so keep those; per `SCENE2_CONTINUITY_NOTES.md` wardrobe must be restated
in every prompt or it drifts.

## Beat breakdown — 9 clips, nothing overflows

Word counts at Scene 1's measured ~2.75 words/sec, 15s ceiling per
`.agents/rules/clip_duration_rules.md`. Unlike Scene 2's 07c and 09, **no beat needs
splitting** — the longest is Rick's closing speech at ~11s.

| # | Slug | Beat | Words | Est. |
|---|---|---|---|---|
| 1 | `s3_01_canteen_busy` | Canteen busy, free pastries, last one claimed | 0 | ~4s |
| 2 | `s3_02_jan_asks_maureen` | "Is there any more pain au chocolat?" / "Sorry, all gone." | 10 | ~4s |
| 3 | `s3_03_that_is_it` | Jan, veins bulging: "OH THAT IS IT!" | 4 | ~2s |
| 4 | `s3_04_plates_swept` | Plates swept off the counter, china shatters, room stares | 0 | ~4s |
| 5 | `s3_05_mba_scream` | "I HAVE HAD IT WITH THIS PLACE!… NOBODY APPRECIATES MY IMMENSE TALENT!" | 16 | ~6s |
| 6 | `s3_06_chair_through_window` | Chair hurled into the window, glass shatters | 0 | ~4s |
| 7 | `s3_07_taser_collapse` | Turns for a second chair, POP-CRACKLE, slumps; Rick revealed | 0 | ~6s |
| 8 | `s3_08_have_you_killed_him` | Chris crouching: "Have you killed him?" | 4 | ~2s |
| 9 | `s3_09_rick_reply` | Rick stows the Taser, "…we need the police here…" | 30 | ~11s |

### Continuity state to carry through the scene

Answering the four questions `SCENE2_CONTINUITY_NOTES.md` says to answer before writing
any prompt:

- **Pastry trays**: full and busy in clip 1 → **empty with crumbs from clip 2 onward**.
  The gag only works if the audience saw them full first.
- **The china**: stacked on the counter in clips 1–3 → **smashed across the floor from
  clip 4 onward**. It must stay on the floor in every later clip; it never gets tidied.
- **The window**: intact in clips 1–5 → **shattered from clip 6 onward**. The stack of
  heavy meeting chairs loses one chair from clip 6.
- **Jan**: composed-ish in clip 2 → flushed and shouting 3–6 → **on the floor,
  unconscious, from clip 7**. He is never upright again. He goes down **face-first**
  in clip 7 (the script's word) but lies **on his back** in clips 8–9. That is
  deliberate, not drift: Chris crouches to check him between those clips and asks
  "Have you killed him?", and rolling someone over to see if they are breathing is
  exactly what that line implies. Do not "fix" clips 8–9 to face-down — it would
  make Chris's check unreadable.
- **Rick**: must be **absent or unremarkable in the background** for clips 1–6, then
  revealed behind Jan in clip 7. Showing him early kills the reveal.
- **The crowd**: eating and talking in clip 1, **frozen and staring from clip 4**
  (the script says so explicitly), then crowding closer at 8–9.
- **Room occupancy is itself continuity.** A prompt that names only the speaking
  characters comes back with an EMPTY canteen — that is what happened to the first
  clip 3, which rendered a deserted room between a busy clip 1 and a frozen-crowd
  clip 4, reading as a cut to a different time of day. Every clip from 1 to 9 must
  say the room is occupied and roughly what the occupants are doing. Same lesson as
  Scene 2's Shot 07 (Jan had to be visible inside the office): **absence has to be a
  deliberate choice, never an omission.**

## Known risks

1. **Content filtering.** A Scene 2 generation was auto-flagged NSFW and refunded for
   nothing worse than a red-faced shouting man. Scene 3 is a rage sequence with property
   destruction and a Taser, so expect more false positives. Describe it as a **prop**
   taser, lead on aftermath rather than the weapon, and re-roll — the free tier refunds
   automatically.
2. **The CLI cannot generate these.** `generate-location-coverage.js` shells out to
   `higgsfield.cmd`, which is stuck on the paid `cheungtai37` account and cannot produce
   free generations. Everything here goes through the browser toolkit
   (`run_shot.js` with `HF_SHOTS=./location_shots.js`).
3. **Glass and shattering china are hard**. If the shatter reads badly as a still, the
   video pass may serve it better as motion — consider generating the *before* and
   *after* states and letting MiniMax H3 do the break between keyframes.
