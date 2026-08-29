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

When one beat's dialogue is too long for a single 15s clip, split it at a natural
pause and give both parts the same leading number with an `a`/`b` suffix (as with
`03a`/`03b`) rather than advancing the sequence number — they're one beat, not two.

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
4. **Whisper-transcribe the new clip and diff it against the script line(s) before
   ticking the beat off** (`whisper <clip> --model small --language English`) — cheap
   check, and it has already caught one real script typo
5. Rebuild `scene1_stitched_preview.mp4` by concatenating all numbered files in order
6. Update `SCENE1_MINIMAX_TRACKER.md` §3
