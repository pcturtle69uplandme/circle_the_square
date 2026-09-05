# Trim dead air before stitching — MiniMax H3 pads clips generously

## The problem

MiniMax H3 clips routinely carry 0.5-3s of genuine silence at the head and/or tail —
a pre-roll before the line starts, a post-roll hold after it ends. Concatenated
back-to-back, a trailing hold on one clip stacks with the next clip's leading hold,
reading as an "odd pause" at almost every cut. Found 2026-08-30 across the whole
Scene 1 sequence via `ffmpeg -af silencedetect`: `07_f12_...` had a 3.05s silent tail,
`05b_f07-f08_...` had a 2.85s silent head *and* a 2.15s silent tail on a 7.3s clip
carrying just a 3-word line.

## Detection

```
ffmpeg -i <clip> -af silencedetect=noise=-40dB:d=0.25 -f null - 2>&1 | grep silence_
```

`-40dB` (not the more common `-30dB`) catches quieter room-tone tails; `-30dB` missed
a real dead-air block on `08a_f13-f14_...` in testing. Only trim a block that actually
touches the clip boundary — `silence_start: 0` for a head trim, or `silence_end`
matching the clip's total duration (within ~0.05s) for a tail trim. Mid-clip silence
(a breath, a reaction beat between two lines in the same clip) is not padding — leave
it alone.

**Threshold**: trim if the boundary-touching block is longer than ~0.5-0.6s. Shorter
holds read as a natural beat, not dead air.

## Trimming

Re-encode, don't stream-copy — a frame-accurate cut needs `-ss`/`-to` after `-i`,
which requires decoding:

```
ffmpeg -i <clip> -ss <trim_start> -to <trim_end> -c:v libx264 -preset slow -crf 17 \
  -pix_fmt yuv420p -c:a aac -b:a 192k <output>
```

Leave a **0.3s pad** at whichever boundary you're trimming (don't cut flush to the
dialogue — an abrupt start/stop reads worse than a short natural pause).

## Required before/after

1. **Archive the untrimmed original** before overwriting — `video-tests/archive/untrimmed/`.
   Never trim destructively without a copy; the trim points are read off one silencedetect
   pass and could be wrong.
2. **Re-run Whisper on the trimmed clip** and diff against the script — confirms the trim
   didn't clip actual dialogue. This is the same QA gate as generation, not optional
   just because no new content was generated.
3. **Rebuild the stitched preview with a re-encoding concat**, not `-f concat -c copy` —
   re-encoded trimmed clips can have slightly different keyframe alignment, and
   `-c copy` concat on mismatched clips has caused corrupted audio at splice points
   before (see `HANDOVER.md` §9 addendum, chain_clips.py). Use:
   `ffmpeg -f concat -safe 0 -i list.txt -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k <out>`

## When to apply

Every clip, as part of the same QA pass as the Whisper check — run silencedetect right
after generating and downloading a new beat, before it goes into the stitched preview.
Trimming after the fact (as done 2026-08-30 for beats generated 2026-08-29/30) works
too, but catching it at generation time avoids a second re-encode pass later.
