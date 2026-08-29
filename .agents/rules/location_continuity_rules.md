# Location continuity — cross-check before generating any master/anchor shot

## Video prompts: always specify camera framing explicitly

A video generation prompt that names characters and an action but never states the camera's
position defaults unpredictably — the first opening-scene test (MiniMax H3, Christina's greeting
line) came back as a POV shot from Jan's own eyes, not the intended third-person two-shot. Fixed by
explicitly stating "Third-person wide establishing shot, NOT a point-of-view shot - the camera is
positioned across the room as an observer" plus a concrete camera position/eye-line in every prompt.
**Every future video generation prompt must state the shot type and camera position explicitly** —
never assume the model infers third-person coverage from context alone.

## The gap this fixes

`location-bible.html`'s "Key features" list for a location is not exhaustive. It describes the
*real-world basis* location, not necessarily every prop the *script* requires there. Location 05
("Glass Meeting Room" / Jan's office) was rebuilt from the bible's key features alone (glass walls,
frosted dot film, triangle decal, 4-seat table, wall TV) and came out missing venetian blinds —
because the blinds requirement lives in the script's action line, not the bible's feature list:

> `CTS_Featurette_Episode.fountain`: *"Jan doesn't need to be told again. He lowers the blinds and
> locks his office door."*

The bible does separately flag this ("No real blinds exist on these particular rooms — add as a
set-dressing addition for the shoot") but under **Atmosphere**, not **Key features** — easy to skim
past if you only read the feature bullets.

## Required process before finalizing a location's master shot

1. Read the location's full entry in `location-bible.html` (Real basis, Signature, Atmosphere,
   Key features) — not just the feature bullets.
2. Grep `CTS_Featurette_Episode.fountain` for every scene set at that location (check the
   script-to-location map at the bottom of `location-bible.html` for which scene headings map
   where) and read the action lines, not just dialogue — props get introduced in action
   description (e.g. "lowers the blinds," "locks his office door") that won't appear in a location
   spec written independently of the script.
3. Cross-reference both against the room's actual generation prompt before accepting a master shot.
   Only start chaining angle variants off it once props required by *scripted action* — not just
   room aesthetics — are confirmed present.
4. If a required prop has a state that changes mid-script (blinds open → closed), decide which
   state is the *default* for the master/most shots, and note the alternate state as one of the
   angle variants (e.g. `door_closed` for Location 05) rather than baking only one state in.

## Findings log (append here as each location gets this check)

- **Location 05 (Glass Meeting Room / Jan's office)**: needs venetian blinds (raised/open by
  default, since most scenes there don't call for them closed; a `door_closed` variant shows them
  lowered for the Sharon-barges-in / affair beat). Door must visibly lock (has a lock mechanism,
  even though it's a sliding glass door) — not yet verified in a generated shot.
- Other locations (Forecourt, Reception/Atrium, Canteen, Open-plan floor, Breakout/Pitstop,
  Courtyard, Corridor) have **not yet** had this script cross-check done — do it before generating
  their master shots, not after.

## Chaining video clips: `--start-image`, not `--image-references`

`minimax_h3`'s params include both `start_image` (object) and `image_references` (array) —
these are **not interchangeable**. `image_references` is a loose style/identity reference; the
model treats it as inspiration and is free to invent its own camera setup around it.
`start_image` actually seeds the video's literal first frame.

Passing a previous clip's last-frame PNG via `--image-references` (done for
`video-tests/archive/f03_standalone_wrong_seed_minimax_h3.mp4`, 2026-08-29) produced a visible
camera jump at the join — same room, same characters, but a distinctly different camera
position, because the model wasn't told to start exactly there. Re-seeding the same beat with
`--start-image` instead (`video-tests/02_f03-f04_pitch_and_listening_minimax_h3.mp4`) reproduced
the seed frame pixel-for-pixel as frame 1 — genuinely seamless.

**Rule: when chaining a new clip off a previous clip's last frame for camera continuity,
always use `--start-image`, never `--image-references`.**

**Constraint this creates**: the API rejects mixing `start_image`/`end_image` with reference
media in the same call. If the continuation beat introduces a **new character who isn't in
the seed frame**, you cannot both seed the exact camera position AND pass that character's
identity reference sheet in one call. In that situation, treat the character's entrance as a
natural cut point instead of forcing continuity: drop `start_image`, generate that shot with
`image_references` (the new character's identity + the relevant location coverage angle), and
accept a fresh camera setup — a person walking into frame is an expected edit point, unlike a
jump mid-conversation between two characters already on screen.
