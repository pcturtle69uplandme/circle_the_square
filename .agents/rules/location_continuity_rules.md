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

## Generational drift: don't chain `--start-image` indefinitely

Each `--start-image` continuation re-feeds the model's own prior output back into itself.
Diffusion models compound their own stylistic bias with each pass — measured on
2026-08-29 across a chain of 8 consecutive `--start-image` generations (all seeded from the
same original `01_...` clip, no resets): brightness dropped and shadow-crushing roughly
doubled every ~4 generations (depth 1 → 17.8% near-black pixels, depth 4 → 27.8%, depth 8 →
36.8%), and the image visibly shifted from photoreal toward a more "painted/illustrated"
look with harder local contrast. Saturation drifted early then plateaued, but the
brightness/shadow trend was linear and ongoing — left unchecked it would have made later
beats in a long scene look markedly worse than the opening ones.

**Rule: don't chain `--start-image` for an entire scene.** Every ~6-8 generations (sooner if
a natural cut point exists anyway, e.g. a new character entering per the constraint above),
reset the chain by cutting to a different camera angle seeded from an undegraded source —
a fresh location coverage plate via `image_references`, not a frame extracted from any
previous video generation. This doubles as legitimate shot/reverse-shot cinematography
(don't hold one static two-shot for 100+ seconds) rather than reading as a workaround.
`video-tests/archive/*_drifted_minimax_h3.mp4` holds the clips that prompted this finding,
kept for reference, not used in the cut.

**How to tell if a clip has drifted**: extract a comparable frame and compare against an
early clip's frame — `python3` + PIL, check `(arr.min(axis=2)<5).mean()` (fraction of
near-black pixels) and overall brightness. Rising shadow-crush and falling brightness across
a chain is the tell; eyeballing alone can miss it until it's severe.

## Never let a still-speaking character warp to a different shot mid-line

When a single scripted speech is split across two clips only because of fal's 15s duration
cap — not because the fountain has an actual beat break — the second clip MUST chain from
the first clip's real extracted last frame, never from an independently pre-designed
"adopted still," even when that still shows a plausible alternate camera angle for the
same beat.

**Case that cost a render**: `c05_rick_questions` → `c06_naming_inception` (Scene 2). The
fountain writes Jan's justification and the "Inception" naming as one unbroken speech
(`CTS_Featurette_Episode.fountain` L122); it's split into two clips purely for the duration
cap. c06 was first generated from an independently adopted still
(`shot07c2_naming_inception.png`) showing a different, wider angle near Jan's office door —
reasoned at the time as an intentional cut for the reveal beat, since the two stills were
designed with different framings. It rendered fine and passed the audio-transcription gate,
but on review it reads as Jan warping to a new position mid-sentence, because there is no
cut in the underlying scene to justify it. The render was wasted; redone chained from
`c05`'s actual last frame instead.

**Rule: if the character is still speaking the same continuous line (no scene/beat break in
the fountain at that point), chain the next clip from the previous clip's real last frame —
per "Chaining video clips" above. Only cut to a different adopted still when the fountain
itself has an actual beat change there (new speaker taking over, a described entrance/exit,
a genuine scene cut). The existence of a differently-framed production still for the next
beat is NOT by itself evidence of an intentional cut — check the script, not the art.**

This sharpens the "genuine cut vs continuation" test above: the test is whether the SCRIPT
has a break there, not whether a separately-designed still happens to exist for the next beat.

## A shot-list number is production planning, not the script — and a cut can't drop someone

Two further corrections from the same c06→c07 handoff (Scene 2), both from watching the
actual render rather than reasoning about it in advance:

1. **A shot-list renumbering (07c → 08a/08b) is not evidence of a script break either.**
   I initially treated the new shot number as proof this was a genuine cut. It isn't — the
   fountain has no scene heading or action break between Jan's line and Chris's heckle,
   same as the 07c-1/07c-2 case above. Shot numbers are a downstream production-planning
   artifact (breaking a long scene into coverage), not the screenplay itself. **Check the
   fountain text directly; don't infer a break from any shot-list document.**

2. **Even a legitimate cut can't make an already-on-screen character vanish.** c07's stills
   (`shot08a`/`shot08b`) never included RICK, who was clearly on screen a moment earlier in
   c06 (arms folded, beside Jan). Cutting to them was defensible for *introducing* Chris
   (a new character entering is a legitimate edit point, per "Chaining video clips" above)
   but it silently dropped Rick too — which reads as a continuity error, not an edit,
   because nothing in the script or the cut motivates his absence. **Before using any still
   for a clip that follows one where multiple characters are already established, check
   that still contains every character who was just on screen** — not only the ones with
   lines in the upcoming clip. If it doesn't, composite a corrected still (base it on the
   *previous clip's real last frame*, so the already-established characters are
   pixel-accurate, and add only the new character via their reference sheet) rather than
   using the incomplete one or forcing a chain that has to invent the new character from
   text alone.

   **Follow-up, same clip — the fix above still cost a wasted render.** The composited
   still (`fal-tools/api/compose_shot08_heckle.js`, via `fal-ai/nano-banana-pro/edit`) came
   back **1024×1024** because no aspect ratio was requested, while every other Scene 2 still
   is **2752×1536**. Nothing checked this before submitting it to `image-to-video`, which
   just inherits whatever aspect ratio its seed image has — no independent aspect parameter
   overrides it. The render came back **768×768**, a visibly square clip spliced into an
   otherwise-widescreen scene, on top of a separate voice-assignment glitch (Jan's voice came
   out of Chris) that surfaced once a third named speaker (Rick) was added to the same
   dialogue prompt. Both were only caught on manual review after paying for the render, and
   the fix was reverted — the original two-speaker keyframe pair (missing Rick, but correct
   aspect and voices) was kept as the accepted take instead.

   **Rule: `ffprobe -v error -show_entries stream=width,height -of csv=p=0 <image>` EVERY
   image straight out of a generation/composite step, before it ever gets passed to
   `image_url` for a video render — not just when something already looks wrong.** Compare
   against the scene's standing resolution (Scene 2 = 2752×1536). If it doesn't match, pass
   an explicit aspect-ratio/size parameter on the image-generation call, or crop/pad the
   result to match. Never submit a mismatched-aspect still to the video model and catch it
   after the fact — that's a paid render spent to discover something a one-line `ffprobe`
   check catches for free.

   **Related, unresolved**: adding a third named speaker (Rick) to a dialogue prompt that
   previously had only two (Jan, Chris) coincided with the model assigning Jan's line to
   Chris's voice. Not yet root-caused or proven as the mechanism — noted here so the next
   multi-speaker prompt watches for it and reports back what's found.
