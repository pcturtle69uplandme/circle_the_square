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

See `SCENE1_MINIMAX_TRACKER.md` §3 for the full per-beat plan and what's still pending.

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

## Adding the next beat

1. Extract the last frame of the current final numbered clip (`ffmpeg -sseof -0.3 ... -frames:v 1`)
2. Generate the next beat with `--start-image` set to that frame (never `--image-references`
   for continuity — see the gotcha in `.agents/rules/location_continuity_rules.md`)
3. Save it as the next `NN_` numbered file describing the beats it covers
4. Rebuild `scene1_stitched_preview.mp4` by concatenating all numbered files in order
5. Update `SCENE1_MINIMAX_TRACKER.md` §3
