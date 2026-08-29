# Clip duration — always plan to fill up to 15 seconds

## The rule

`MiniMax H3` (Higgsfield) accepts an arbitrary `--duration` up to 15s, billed per length
(observed: 8s cost 16 credits, 15s cost 30 credits — see `higgsfield-tools/usage-log.jsonl`),
not per beat. **One generation call should cover as many consecutive script beats as fit
naturally in 15 seconds, not one beat per clip.** Generating beat-by-beat wastes calls and
credits on padding/reaction time that a combined clip gets for free.

**Before submitting a `minimax_h3` job**: read the next unfinished beats in
`SCENE1_MINIMAX_TRACKER.md` §3 in script order, sum their spoken-line lengths at a natural
pace (~2.5-3 words/sec) plus a beat of reaction/reaction-shot time between lines, and chain
as many as fit under 15s into a single prompt describing the full exchange in sequence
(who speaks when, what each does while listening). Stop adding beats once the estimate
would exceed ~14s — leave a little headroom rather than cutting a line short.

## Precedent

- `video-tests/01_f01-f02_opening_greeting_minimax_h3.mp4` — F01 (Christina's greeting) + F02
  (Jan's "Barely...") combined into one 15s clip.
- `video-tests/archive/f03_standalone_wrong_seed_minimax_h3.mp4` — F03 alone, 8s. Done as a
  single beat *before* this rule was written; not to be treated as the pattern going forward.
  Superseded by `video-tests/02_f03-f04_pitch_and_listening_minimax_h3.mp4`, which also fixed
  the `--start-image` seeding bug (see `.agents/rules/location_continuity_rules.md`).

## Applying it

Continue the chain (F04 onward) by combining consecutive beats up to the 15s ceiling —
e.g. F04 (Jan, "I'm listening.") + F05 (Christina, breakfast-meeting pitch) is a natural
one-clip pairing; extend to F06a if the estimate still leaves headroom. Reference
`CTS_Featurette_Episode.fountain` for the exact combined dialogue.
