# video-tests — Scene 1 Higgsfield cut

## Rebuild order

Files at the top level, prefixed `01_`, `02_`, etc., are the **adopted sequence** — the
current beats of the Scene 1 cut, in order. To rebuild the full cut, concatenate them in
numeric-prefix order (same codec/resolution throughout, so `ffmpeg -f concat -c copy` works
without re-encoding). `scene1_stitched_preview.mp4` is that concatenation, already built —
rebuild it after adding a new numbered clip.

Each numbered clip's beat coverage:

| File | Beats covered |
|---|---|
| `01_f01-f02_opening_greeting_minimax_h3.mp4` | F01 (Christina enters, greets Jan) + F02 (Jan — "Barely...") |
| `02_f03-f04_pitch_and_listening_minimax_h3.mp4` | F03 (Christina pitches the idea) + F04 (Jan — "I'm listening.") |
| `03a_f05_breakfast_pitch_part1_minimax_h3.mp4` + `03b_..._part2_minimax_h3.mp4` | F05 (Christina explains the breakfast-meeting concept) — one beat, split into two clips because its full script line (~47 words) exceeds the 15s ceiling on its own |
| `04a_f06a_jan_enthused_part1_minimax_h3.mp4` + `04b_f06b_jan_mba_punchline_minimax_h3.mp4` | F06a+F06b (Jan's enthused reaction through the MBA punchline) — one script speech (~74 words), split the same way |
| `05a_f07_reverse_angle_part1_minimax_h3.mp4` + `05b_f07-f08_reverse_angle_part2_minimax_h3.mp4` | F07 (Christina's dry "diminishing returns" line) + F08 (Jan — "Great. Make it so.") — regenerated 2026-08-29 from a fresh reverse angle (`jan_office_desk_reverse.png`) as a drift-reset point, then regenerated again the same evening to fix a continuity jump, see below |

When one beat's dialogue is too long for a single 15s clip, split it at a natural
pause and give both parts the same leading number with an `a`/`b` suffix (as with
`03a`/`03b`) rather than advancing the sequence number — they're one beat, not two.

See `SCENE1_MINIMAX_TRACKER.md` §3 for the full per-beat plan and what's still pending.

## Generational drift — reset the `--start-image` chain periodically

Chaining `--start-image` for 8 straight generations (the original F09-F11 attempt) visibly
degraded image quality — brightness dropping, shadows crushing, a shift from photoreal
toward a "painted" look. Measured and documented in
`.agents/rules/location_continuity_rules.md`. **Every ~6-8 generations, reset by cutting to
a different camera angle** seeded from a fresh location coverage plate via
`--image-references` (not `--start-image`) instead of always continuing from the previous
clip's last frame. This doubles as legitimate shot/reverse-shot cinematography rather than
holding one static two-shot for the whole scene. F07 (`05a_...`) is the first reset point,
cut to an over-the-shoulder angle off `jan_office_desk_reverse.png`.

## Reverse-angle cut: motivate the position change on-screen

A drift-reset cut (see above) changes camera angle *and* can put a character somewhere new in
frame — that repositioning needs to actually happen on screen, not just be implied by the cut.
`05a`'s first take (2026-08-29 evening) placed Christina already standing across the desk near
the visitor chair, with no motion connecting it to `04b`'s last frame where she'd been standing
right beside Jan at the desk's near corner — it read as an instant teleport, and the shift to a
colder-lit feature wall behind her landed as a tone jump on top of that. Fixed by regenerating F07
with the same reference images (no new asset needed) but a prompt that adds a walk-in preamble:
Christina visibly steps back from Jan, crosses to the visitor chair, and settles there before her
line. **Whenever a drift-reset (or any `image_references`-seeded) cut relocates a character
relative to their position in the previous clip, write that relocation into the new clip's action
description as on-screen motion** — don't rely on the cut alone to sell it.

This has a knock-on effect worth checking every time: if a later clip was chained off the *old*
take's exact last frame via `--start-image`, it will no longer match once the earlier clip is
regenerated. `05b` was chained off the original `05a`'s last frame, so it had to be regenerated
too (`--start-image` off the new `05a`'s last frame) to avoid a fresh pop at that internal join.
Old takes are archived as `archive/05a_f07_reverse_angle_part1_teleport_minimax_h3.mp4` and
`archive/05b_f07-f08_reverse_angle_part2_teleport_minimax_h3.mp4`.

## Don't restate dialogue across a split clip, and mine the script for reference jokes

The 2nd take of `05b` above (the walk-in fix) reopened by having Christina restate her whole
"diminishing returns" line before Jan's response — a straight repeat of what `05a` had just
delivered a moment earlier. Harmless in isolation, but a duplicate once the two clips play back
to back. **When a beat is split across two clip files (`05a`/`05b`, `03a`/`03b`, etc.), don't
have the later clip re-deliver the earlier clip's dialogue "for continuity" — a silent beat is
enough; the `--start-image` seed already carries the visual continuity.**

Separately, worth catching earlier next time: "Great. Make it so." (F08) is Jan quoting Picard's
line from *Star Trek: TNG* — and the script's very next beats (F09-F11) are Jan asking if
Christina's seen the show and her not getting the reference. That makes it a deliberate setup,
not a throwaway line, and the performance should sell it as Jan being pleased with his own
cleverness. `05b` was regenerated a 3rd time to drop the repeated line and add that
self-satisfied delivery in one pass (both needed new footage, so a local `ffmpeg` trim of the
old take wasn't enough on its own — trimming stays the right call whenever a fix needs no new
content, just cutting what's already there). Old take archived as
`archive/05b_f07-f08_reverse_angle_part2_repeatline_minimax_h3.mp4`. **Read scripted lines for
reference/callback jokes before locking a beat's performance direction** — check whether a later
beat pays it off before treating a line as generic dialogue.

## `archive/`

Superseded or exploratory takes, kept for reference only — **not** part of the rebuild:

- `christina_greeting_v1_pov_rejected_minimax_h3.mp4` — first F01 attempt, came back as a
  POV shot from Jan's eyes instead of third-person (see `.agents/rules/location_continuity_rules.md`)
- `christina_greeting_v2_thirdperson_minimax_h3.mp4` — corrected framing, but superseded once
  the combined `01_...` clip was generated
- `jan_response_kling_continuation_720p.mp4` — an early Kling v3.0 continuation test; 720p,
  not part of the 2K cut
- `f03_standalone_wrong_seed_minimax_h3.mp4` — F03 seeded via `--image-references` instead of
  `--start-image`; caused a visible camera jump. Superseded by `02_f03-f04_...`
- `frame_for_kling_start.png`, `opening_lastframe.png` — frame extracts from the above,
  kept only as a record of the seeding technique
- `05a_f07-f08_part1_drifted_minimax_h3.mp4`, `05b_f07-f08_part2_drifted_minimax_h3.mp4`,
  `06_f09-f11_drifted_minimax_h3.mp4` — F07/F08/F09-11 as originally generated, 6-8
  `--start-image` generations deep from the original F01 clip with no reset. Visibly
  degraded (see "Generational drift" below). Superseded by the `05a`/`05b` reverse-angle
  regeneration; F09-11 not yet redone.
- `05a_f07_reverse_angle_part1_teleport_minimax_h3.mp4`,
  `05b_f07-f08_reverse_angle_part2_teleport_minimax_h3.mp4` — the drift-reset take of F07/F08
  described just above: correct drift depth and location, but Christina's position jumps across
  the desk with no on-screen motion to connect it to `04b`. Superseded by the walk-in-preamble
  take.
- `05b_f07-f08_reverse_angle_part2_repeatline_minimax_h3.mp4` — the walk-in-preamble take of
  `05b`: fixed the teleport, but reopened by having Christina repeat her whole line from `05a`
  before Jan's response, and didn't play up the Star Trek reference in his delivery. Superseded
  by the current `05b`.

## Adding the next beat

1. Extract the last frame of the current final numbered clip (`ffmpeg -sseof -0.3 ... -frames:v 1`)
2. Generate the next beat with `--start-image` set to that frame (never `--image-references`
   for continuity — see the gotcha in `.agents/rules/location_continuity_rules.md`)
3. Save it as the next `NN_` numbered file describing the beats it covers
4. **Whisper-transcribe the new clip and diff it against the script line(s) before
   ticking the beat off** (`whisper <clip> --model small --language English`) — cheap
   check, and it has already caught one real script typo
5. Rebuild `scene1_stitched_preview.mp4` by concatenating all numbered files in order
6. Update `SCENE1_MINIMAX_TRACKER.md` §3
