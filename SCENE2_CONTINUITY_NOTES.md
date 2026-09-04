# 🎬 SCENE 2 — CONTINUITY NOTES (open-plan floor / Jan's office corridor)

> **Purpose**: `scene_dialogue_audio_guide.md` and `CTS_Featurette_Episode.fountain`
> give the dialogue and stage directions, but a human reading them fills in a lot of
> blocking, timing, and state (who's in frame, what a door/blind is doing, who's
> exhausted vs. composed) without noticing they're doing it. An image-generation
> pipeline doesn't fill any of that in — it only has what's typed into the prompt.
> This file makes those implicit facts explicit, shot by shot, so the next session
> (or the next regeneration) doesn't have to re-derive them from scratch, and doesn't
> repeat mistakes already made once in this project (see "Mistakes already made" at
> the bottom of each shot where relevant).
>
> **Do not edit `CTS_Featurette_Episode.fountain` to add this detail** — the script
> stays clean as the actual screenplay. This file is the companion continuity layer,
> same relationship as `LOCATION_PLATE_SHOT_LIST.md` is to the location plates.

## Adopted stills — local files (regenerated 2026-09-03 late)

All adopted Scene 2 stills live in `scene2-stills/` (2752×1536 PNGs, Nano Banana 2 at
16:9/2K on the free Unlimited tier, downloaded straight from the Higgsfield CDN — the
in-app Download button raises no download event in the Playwright-automated profile).

> **The whole scene was regenerated from Shot 06 onward on 2026-09-03**, replacing the
> first pass. Two reasons: the first-pass stills predated `extra_01`–`extra_04`, so the
> background crowd was a different set of people in every frame; and the first pass had
> drifted off the script in wardrobe (see the Rick note below). The old filenames
> (`shot07b_*`, `shot07c_*`, `shot09_50k_*`) are superseded by the split-aware slugs
> below — one file per **planned video clip**, matching `SCENE2_VIDEO_PLAN.md`.

| Clip | File | Beat |
|---|---|---|
| 06 | `scene2-stills/shot06_corridor_gossip.png` | Chris & Rick gossip, blinds shut |
| 07 | `scene2-stills/shot07_sharon_exits.png` | Sharon exits dishevelled, Jan still inside |
| 07b-1 | `scene2-stills/shot07b1_jan_addresses.png` | Jan emerges, claps, "Right guys" |
| 07b-2 | `scene2-stills/shot07b2_shut_up_flareup.png` | Sniggering → "SHUT UP!" |
| 07c-1 | `scene2-stills/shot07c1_rick_questions.png` | Rick questions the old project |
| 07c-2 | `scene2-stills/shot07c2_naming_inception.png` | Jan names "Inception" |
| 08 | `scene2-stills/shot08_project_inception_heckle.png` | Chris heckles across the crowd |
| 08b | `scene2-stills/shot08b_merch_gag.png` | Branded merch gag + self-appointment |
| 09-1 | `scene2-stills/shot09_1_groans.png` | Crowd groans, Jan calm and smug |
| 09-2 | `scene2-stills/shot09_2_50k_outburst.png` | "GET BACK TO WORK!" |

**Prompts are no longer ad-hoc.** Every prompt above is defined in
`higgsfield-tools/browser/scene2_shots.js` and generated with
`node higgsfield-tools/browser/run_shot.js <slug>`, which clears the previous
references, attaches the right ones, types the prompt, verifies the free tier and
saves the full-res PNG. Re-roll any shot by editing that file and re-running the slug —
do not hand-type prompts into the web UI, or this file goes stale again.

Recurring background extras are complete: `character-refs/higgsfield/extra_01` through
`extra_04` (2F/2M). Every crowd prompt names all four and attaches their reference
photos. Rejected variants stay in `scene2-stills/rejected/`, for reference only.

### Two pipeline bugs that silently produced WRONG stills

Both produced plausible-looking Scene 2 frames, so neither showed up as a failure —
only side-by-side QA caught them. Guards are now in `run_shot.js`; don't remove them.

1. **Shots saved each other's images.** The runner accepted "the feed head changed" as
   proof its own render had arrived. But a job submitted by an *earlier failed attempt*
   renders minutes later and becomes the head, so `shot07b2` saved `shot07c2`'s image
   (byte-identical files) and `shot09_1` saved the flare-up. Fixed by parsing the UTC
   timestamp embedded in the CDN filename (`hf_YYYYMMDD_HHMMSS_<uuid>.png`) and
   rejecting any asset that predates our own submit, plus waiting for the queue to go
   idle before submitting.

2. **The composer wedged and locked out uploads.** `clearRefs` matched `div.size-14`,
   which is also the class of the trailing "add reference" button — a tile with no
   image and no remove control. The loop span on it forever, left references attached,
   and an attached reference flips the uploader from multi-file to single-file mode,
   so every later shot failed with the uploader "never appearing". Match on tiles that
   *contain an `<img>`*, not on the class. `hf_reset.js` replaces the tab when
   placeholders wedge beyond recovery.

Also: Chrome must be started **detached** (`hf_up.js`), not by a script that blocks
forever. A blocking launcher is a long-lived background task, and when those get
cleaned up the browser dies mid-batch — that killed two runs.

### QA is per-shot and manual; "generated" is not "good"

`.<slug>.gen.json` sidecars record a fingerprint of the prompt+refs that produced each
adopted PNG, so editing one shot's prompt re-rolls only that shot. Two beats kept an
earlier take over a later one, both recorded in their sidecar:

- **07b-2** — the re-render drifted `extra_03` to braided hair (her ref is short
  natural curls) and framed tighter than 09-2 needs, since 09-2 is meant to be the
  tighter escalation.
- **08** — the re-render drifted Jan to a patterned tie (plain blue everywhere else)
  and lost the red/black triangle feature wall.

Losing takes live in `scene2-stills/candidates/`; the pre-split first pass is in
`scene2-stills/superseded/`.

### Wardrobe is pinned by the script, not by the character refs

The cast reference photos deliberately leave shirt colour loose ("casual-smart office
wear", "plain button-down or polo"), but the **script's own parentheticals pin it**:
`CHRIS (32, lean, light blue shirt)` and `RICK (40, broad, grey polo)`. The first-pass
Shot 06 put Rick in a **navy button-down** — the ref photo didn't say otherwise and the
prompt didn't either. Every prompt in `scene2_shots.js` now restates both wardrobes
verbatim. Restate wardrobe in *every* prompt; it does not carry over from a reference
photo.

### Getting the closed blinds to actually read as closed (Shot 06)

This took four attempts and the fix generalises to any "fixture is in a non-default
state" prompt:

1. "blinds lowered" → rendered lowered but with the slats open; the desk, chair and red
   triangle wall showed straight through.
2. "lowered AND slats tilted completely shut, opaque" → the *door* pane went opaque but
   the narrow side panel and the corner return still leaked the interior.
3. Naming **every pane** ("the wide glazed door, the tall narrow side panel beside it,
   and the glazed panel on the corner return, ALL of them") plus describing the
   **result** rather than the mechanism ("must read as a SOLID OPAQUE PALE PANEL like a
   blank white wall; no furniture, no colour, no silhouettes through any pane") finally
   held — but it overcorrected into **frosted glass** and the camera crept in tight.
4. Adding "the closed slats must still read as a VENETIAN BLIND, fine horizontal slat
   lines visible, not frosted glass" plus an explicit FRAMING line ("stand well back,
   take in the whole door, both men from the knees up, corridor receding behind") gave
   the adopted frame.

Lesson: describe the **visible result** you want, enumerate **every instance** of the
fixture, and state framing explicitly — a negative constraint alone ("blinds shut")
gets interpreted as a mechanism, not an outcome, and fixing an outcome tends to drag
the framing with it.

---

## Scene-level facts (apply to every shot below)

- **Setting**: `INT. CORRIDOR / OPEN-PLAN FLOOR - CONTINUOUS` — i.e. this scene picks
  up in the same continuous moment Scene 1 ends on, just outside Jan's office door,
  not a time-skip.
- **Jan's office has a glazed (glass) wall/door with venetian blinds**, per the
  approved location spec `LOCATION_PLATE_SHOT_LIST.md` L10 ("black-and-white triangle
  acoustic feature wall, walnut desk... glazed partition"). The blinds are a real,
  operable fixture in the reference photos — not something to invent in the prompt.
- **Location plate in use**: `location-refs/higgsfield/coverage/jan_office_corridor/jan_office_corridor_master_wide.png`
  — this is the *outside-looking-in* reverse angle (correct camera position for
  Chris/Rick, who are standing in the open-plan floor, not inside the office).
  `jan_office/jan_office_master_wide.png` is the companion *inside-looking-out* angle
  of the same room (used for establishing Jan's desk, not for Scene 2's corridor shots).
- ⚠️ **Data-quality gotcha, confirmed 2026-09-03**: both `location-refs/higgsfield/coverage/jan_office/`
  and `location-refs/higgsfield/coverage/jan_office_corridor/` contain a `door_closed`,
  `table_head`, `table_reverse`, `corridor_view`, `openplan_context_wide` set of images
  that are a **different, unrelated glass meeting-pod room** (hexagonal pendant lights
  in the `jan_office` set; brick pillars + red triangle branding in the
  `jan_office_corridor` set) — neither of which is Jan's actual office. Only
  `desk_front`, `desk_reverse`, `door_entrance`, `high_corner_wide`, `master_wide`,
  `seating_area`, `wall_feature_closeup`, `window_side` in the `jan_office` folder are
  the real, approved office (walnut desk, black-and-white triangle wall). Don't reach
  for the other angles in either folder for anything involving Jan's actual office.
  There's also a `location-refs/higgsfield/_archive-walnut-office-wrong/` folder —
  despite the name, it holds earlier **rejected generation attempts** of the *correct*
  walnut office (iterating toward the clean version now in the active `jan_office/`
  folder), not a different, wrong office design. Don't be misled by the folder name.
- **Characters in this scene, in order of appearance**: Sharon (exiting), Jan (stays
  behind, emerges later), Chris, Rick, then a wider unnamed staff crowd from Shot 08
  onward.

---

## Shot 06 — "Corridor Gossip" (6s)

- **Who's visible**: Chris, Rick. **Nobody else** — Sharon and Jan are both still
  inside the office at this point, door and blinds fully shut. Don't add them to the
  frame.
- **Blinds/door state**: **Fully closed and opaque** — both lowered *and* the slats
  tilted flat shut, zero gap. This is not the default state of the reference photo
  (which shows the blinds raised) — it must be stated explicitly in the prompt every
  time, including "completely opaque, nothing inside visible."
  - **Mistake already made**: an early generation described the blinds as "lowered"
    only, without "slats tilted shut" — the model rendered lowered-but-open slats,
    letting the desk and bookshelf show through. Always specify both lowered AND
    tilted shut.
- **Why the blinds are closed here specifically**: this is the moment right after
  Scene 1 ends ("Jan lowers the blinds and locks his office door"), before Sharon has
  come out. Chris's line ("they don't even try to hide it") is commentary on the
  *pattern* of behaviour (the blinds always go down, everyone knows what that means),
  not on anything visible through the glass.
- **Adopted asset**: generated 2026-09-03, Nano Banana 2, 2752×1536, free/Unlimited
  tier on the `groovingmushroom1467` account.

## Shot 07 — Sharon exits (unnumbered in the dialogue guide; sits between 06 and 08)

- Not present in `scene_dialogue_audio_guide.md`'s Scene 2 list (which jumps 06→08)
  because it has no dialogue — but it's a real beat in the fountain script action
  lines: *"They watch Sharon leave Jan's room dripping in sweat, with dishevelled
  hair and makeup."*
- **Who's visible**: Sharon (foreground, walking out, the focus of the shot), Chris
  and Rick (background, watching, same positions as Shot 06), **and Jan** — seated at
  his desk, visible through the now-open door, back of composure not yet regained.
  - **Mistake already made**: the first version of this shot left the office visibly
    empty behind Sharon. That's a continuity break — the script has Jan emerging
    "minutes later," meaning he's still inside at this exact moment. He doesn't need
    to be a focal point (seated, back to camera / partially obscured is enough) but
    the room must read as occupied, or his later emergence makes no sense.
- **Blinds/door state**: door open, blinds raised — this is the one moment in the
  scene where the interior is meant to be visible, since Sharon is mid-exit.
- **Sharon's physical state, explicit**: hair visibly mussed/dishevelled (strands out
  of place), makeup smudged, light sheen of sweat, blouse slightly untucked/creased,
  expression dazed but trying to compose herself. None of this is in her character
  reference photo (plain neutral studio shot) — it all has to be described in the
  prompt from the script's "dripping in sweat, dishevelled hair and makeup" line.
- **Open question, not yet resolved**: *who* physically opens the blinds/door between
  Shot 06 and Shot 07 is not shown as its own beat — current plan (2026-09-03) is to
  bridge 06→07 as one video generation (MiniMax H3, start-frame/end-frame mode) with
  Sharon opening the blinds and walking out as the connecting action described in the
  prompt, rather than an unexplained jump cut. Not yet generated as of this writing.
- **Adopted asset**: generated 2026-09-03, Nano Banana 2, 2752×1536, free/Unlimited
  tier, `groovingmushroom1467` — second version (with Jan visible) is the adopted one,
  not the first (empty-office) version.

## Shot 07b — Sharon-pass deflection → "SHUT UP!" flare-up (new, added 2026-09-03)

> ⚠️ **Rule going forward: always check the full script for every gag/joke line, not
> just the shots named in `scene_dialogue_audio_guide.md`.** That file only names the
> beats someone picked as key; the fountain script has more dialogue and sight gags in
> between that are easy to miss if you only work from the abbreviated guide. This shot
> and the two below exist because a first pass at Scene 2 skipped them.

- **Script lines**: Jan claps his hands, "Right guys, as you know—" → Chris: "Does
  Sharon get a pass on attending this?" → Jan (evasive): "Err... yes she does. I have
  given her the rest of the day off for personal reasons." → "Quiet sniggering ripples
  through the assembled crowd" → Jan (flushed): "SHUT UP! I am truly appalled by the
  lack of discipline in this place and that changes now! I have decided a new project
  is required to manage all the change around here."
- **Who's visible**: Jan (peak moment = the "SHUT UP!" outburst — flushed, defensive,
  having just been caught out over Sharon), crowd reacting with poorly-suppressed
  sniggering (hands over mouths, smirks, not full laughter — they're trying not to
  laugh at him).
- **Adopted asset**: generated 2026-09-03, Nano Banana 2, 2752×1536, free/Unlimited
  tier, `groovingmushroom1467`. Jan with both hands raised in an exasperated shout,
  flushed; crowd behind him genuinely sniggering with hands over mouths.

## Shot 07c — Rick questions the old project → Jan names "Inception" (new, added 2026-09-03)

- **Script lines**: Rick: "What happened to the last project for this, isn't it
  ongoing? By that I mean completely failing." → Jan justifies it at length → "...I
  have decided to call the project Inception."
- **Who's visible**: Jan (mid-explanation, pompous gesture as he announces the name),
  Rick (same deadpan/arms-crossed characterization as Shot 06 — skeptical, unimpressed
  by the deflection).
- **Continuity**: sets up Shot 08's heckle immediately after — Jan should be
  mid-triumphant-announcement here, right before Chris cuts him down.
- **Adopted asset**: generated 2026-09-03, Nano Banana 2, 2752×1536, free/Unlimited
  tier, `groovingmushroom1467`. Jan with one arm raised presenting/announcing, Rick
  beside him arms crossed and visibly unimpressed, crowd flanking both sides.

## Shot 08 — "Project Inception" heckle (8s)

- **Who's visible**: Jan (now out of the office, addressing the crowd — this is his
  "minutes later" emergence, "shirt re-buttoned askew" per the script), Chris
  (heckling — "Inception is the name of a film about dreams Jan!"), plus a wider
  unnamed crowd of office workers gathered round per the script ("claps his hands to
  gather everyone around").
- **Jan's physical state**: shirt re-buttoned but askew (not perfectly composed) —
  visible sign he's just come from an intimate/flustered moment, without being explicit
  about what that moment was.
- **Blocking note**: Chris heckles from within/across the crowd, not standing right
  next to Jan — matches the dialogue guide's "(shouting over crowd)" direction better
  than a close-up heckle.
- **Adopted asset**: generated 2026-09-03, Nano Banana 2, 2752×1536, free/Unlimited
  tier, `groovingmushroom1467`. Two variants generated; the one with Chris positioned
  across the crowd (not directly beside Jan) is the adopted one.

## Shot 08b — Branded merch sight gag → "will there be a lead?" reveal (new, added 2026-09-03)

- **Script lines**: "Jan realizes it is too late to change the name, as he has already
  ordered 1,000 stress balls, pens, and t-shirts with 'PROJECT INCEPTION' printed on
  them." → Chris: "Will there be a lead for this?" → Jan: "At last something sensible
  is asked. Yes there will. However, it is with regret that I have to inform you all
  that the position has already been filled... by me."
- **Who's visible**: Jan, holding or gesturing at a box/stack of the branded merch
  (stress balls, pens, t-shirts, all printed "PROJECT INCEPTION") — sheepish about
  having jumped the gun, then pivoting to smug as he reveals he's given himself the
  role. Chris nearby, asking the question, not yet reacting to the reveal (that's
  Shot 09's job).
- ⚠️ **Exception to the usual "no text" prompt rule**: the whole joke is the tacky
  branded merch with "PROJECT INCEPTION" printed on it — the prompt for this shot
  should deliberately ask for that text to be visible on the props, unlike every other
  shot in this project.
- **Adopted asset**: generated 2026-09-03, Nano Banana 2, 2752×1536, free/Unlimited
  tier, `groovingmushroom1467`. "PROJECT INCEPTION" clearly legible on the box and on
  the stress balls/pens inside; Jan sheepishly shrugging with the open box, Chris
  facing him with a curious/questioning expression, crowd visible behind.

## Shot 09 — £50k raise outburst (7s)

- **Who's visible**: Jan (shouting), same crowd as Shot 08 reacting with groans.
- **Adopted asset**: generated 2026-09-03, Nano Banana 2, 2752×1536, free/Unlimited
  tier, `groovingmushroom1467`. Jan only (no Chris reference needed for this one) —
  fist raised, flushed red, mouth open mid-shout; crowd reacting with exasperation
  (heads in hands, arms crossed, wincing). One duplicate generation attempt was
  auto-flagged NSFW and refunded (false positive, likely from the aggressive
  expression/red-faced description) — harmless since it's the free tier, just retry
  if it happens again.

---

## General lesson for future shots (any scene)

Before writing a generation prompt, explicitly answer these, even when they feel
obvious from reading the script:
1. **Who is physically in frame** — not just who's speaking. Absence needs to be a
   deliberate choice (character truly not there) vs. an accident (character should be
   there but the prompt didn't say so).
2. **What state is every practical fixture in** — doors, blinds, lights — if the
   script or previous shot implies a specific state (closed, locked, open), say so
   explicitly; don't rely on the reference photo's default state.
3. **What physical/emotional state are characters in** — reference photos are neutral
   studio shots. Dishevelled, exhausted, sweating, smug, furious — none of that
   carries over unless it's in the prompt.
4. **Does this shot's location plate actually match** what a previous or next shot
   implies is the same physical space — verify by comparing the visible set dressing
   (wall features, furniture), not just the filename.
