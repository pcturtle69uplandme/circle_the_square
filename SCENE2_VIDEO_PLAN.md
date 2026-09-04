# 🎬 SCENE 2 — VIDEO GENERATION PLAN

> Pre-production pass, done **before** any video generation, so we don't re-roll paid
> MiniMax H3 clips. Method mirrors Scene 1's (`.agents/rules/clip_duration_rules.md`):
> measure actual spoken word count at ~2.75 words/sec, cap each clip at ~14s (15s
> ceiling), combine consecutive beats where they fit, split/trim where they don't.
> Camera framing rules from `.agents/rules/location_continuity_rules.md` apply
> throughout (state shot type explicitly, `--start-image` for continuity within a
> take, reset the chain every 6-8 generations or at a natural cut point).

---

## ⚠️ Crowd/extras consistency — confirmed broken, needs a decision

Checked side-by-side across the 7 adopted Scene 2 stills (Shots 06, 07, 07b, 07c, 08,
08b, 09): **the named cast (Jan, Chris, Rick, Sharon) stay consistent** because their
reference photos are fed into every generation. **The generic background office
workers do not** — different hair colours, faces, and clothing in the crowd from shot
to shot, because we never gave "the crowd" any reference images; Nano Banana 2 invents
a fresh set of extras every time it's asked for "generic unnamed office workers."

This will read as a different set of colleagues in every cut unless fixed. Options:

1. **Generate 3-4 recurring "background extra" reference photos** (same process as
   the named cast — quick, free on Nano Banana 2) and include 2-3 of them by name in
   every Scene 2 crowd prompt going forward. Most correct, most setup work.
2. **Rely on video chaining for continuity within a continuous take, accept resets at
   cuts.** If consecutive beats are generated as one chained `--start-image` video
   sequence (not separate stills), the crowd is pixel-continuous within that chain by
   construction. It only resets where the scene legitimately cuts to a new camera
   angle anyway (matching real filmmaking — background extras aren't always the same
   people shot-to-shot in a wide scene). Cheapest, but leaves visible resets at chain
   boundaries (see clip breakdown below for where those fall).
3. **Both** — recurring extras for insurance, chained video for the connecting motion.

**Decided 2026-09-03**: option 1 — generate recurring extra reference photos. Plan:
4 generic background-extra portraits (2 female, 2 male), same single-portrait style as
the named cast, saved to `character-refs/higgsfield/extra_01/` through `extra_04/`.
Include 2-3 of them by name in every future Scene 2 crowd prompt. Checked
`CTS_Featurette_Episode.fountain` for the other script-known-but-unreferenced minor
characters (Priya, Barbara, Dev, Tomasz, per `SCENE1_MINIMAX_TRACKER.md` §2) first —
none of those names appear anywhere in this script, so they're not applicable here;
the extras are freshly invented generic names.

**DONE (2026-09-03 late)**: all four recurring background extras exist as
`character-refs/higgsfield/extra_0N/extra_0N_fullbody_neutral.png` (2752x1536, Nano
Banana 2, 16:9, 2K, free/Unlimited tier on `groovingmushroom1467`):

| Ref | Who |
|---|---|
| `extra_01` | woman, 30s, long light brown wavy hair, white floral-print blouse, navy trousers |
| `extra_02` | man, 30s, dark hair, glasses, blue checked shirt |
| `extra_03` | Black British woman, 45, short natural curly black hair, mustard knit top, grey trousers |
| `extra_04` | British South Asian man, 55, greying hair and short grey beard, charcoal jumper over pale blue collar, navy chinos |

Both new refs were generated with the same prompt shape as `extra_01`/`extra_02`
(full body head-to-shoe, front-facing, arms relaxed, plain light-grey studio
backdrop, even lighting, no lanyard) so the four read as one consistent set.

**And the retrofit question is settled**: rather than leave the seven first-pass
stills predating the extras, the user's call (2026-09-03) was to **regenerate every
Scene 2 beat from Shot 06 onward** with the extras wired into each crowd prompt.
That work is tracked in `higgsfield-tools/browser/scene2_shots.js`, which is now the
single source of truth for Scene 2 prompts -- see `SCENE2_CONTINUITY_NOTES.md`.

---

## Dialogue timing audit (word counts from `CTS_Featurette_Episode.fountain`, ~2.75 wps)

| Beat | Spoken words | Est. duration | Fits ≤15s? |
|---|---|---|---|
| Shot 06 (Chris/Rick gossip) | 20 | ~8s | ✅ |
| Shot 07 (Sharon exits, silent) | 0 (action only) | ~3-4s | ✅ |
| Shot 07b-1 (Jan opens / Sharon-pass Q&A / sniggering) | 30 | ~12-13s | ✅ |
| Shot 07b-2 (Jan's "SHUT UP!" outburst) | 33 | ~12s | ✅ |
| Shot 07c (Rick questions old project / Jan names "Inception") | **82** | **~30s** | ❌ **overflow** |
| Shot 08 (Chris heckle exchange) | 25 | ~10s | ✅ |
| Shot 08b (merch reveal + "will there be a lead" + self-appointment) | 37 | ~14s | ⚠️ tight, at the ceiling |
| Shot 09 (£50k reveal + groans + "GET BACK TO WORK") | 50 | ~18s | ❌ **overflow** |

**Two beats overflow the 15s ceiling as scripted verbatim**: Shot 07c (Jan's
justification monologue is 65 words alone) and Shot 09 (Jan's closing speech, 50
words). This is expected — the full fountain script is written for a full episode;
`scene_dialogue_audio_guide.md` only named 3 of these 7 beats in the first place,
suggesting the featurette cut was never meant to voice every word verbatim.

**Decided 2026-09-03**: split, don't trim — keep every scripted word, break each into
2 clips at a natural pause:

- **Shot 07c splits into 07c-1 / 07c-2**: 07c-1 = Rick's question + Jan's opening
  justification ("There's no need for the previous project... within budget.") ≈ 43
  words / ~16s (still slightly over — pacing/delivery speed can absorb this, or trim
  a few words of filler if the actual generation runs long). 07c-2 = the rest of Jan's
  justification through "...call the project Inception." ≈ 35 words / ~13s. The
  already-adopted Shot 07c still (Jan mid-announcement, arm raised, Rick skeptical)
  fits **07c-2** best (it's the triumphant naming beat) — 07c-1 doesn't have its own
  still yet.
- **Shot 09 splits into 09-1 / 09-2**: 09-1 = crowd groans + Jan's calmer opening
  ("Yes groan all you like... into my duties.") ≈ 35 words / ~13s. 09-2 = "I will let
  you know... GET BACK TO WORK!" ≈ 15 words / ~5.5s. The already-adopted Shot 09 still
  (Jan mid-shout, fist raised, flushed) fits **09-2** best (it's the shouted climax)
  — 09-1 doesn't have its own still yet.

So both already-adopted "07c" and "09" stills are really the **second half** of a
two-clip beat — each needs one more still generated for its calmer opening half before
video generation.

---

## Clip breakdown & camera plan

Numbering: one row = one planned video generation call (pending the trim/split
decision above for 07c and 09, which may become 2 rows each).

| # | Beat(s) | Anchor still | Camera | Chain method |
|---|---|---|---|---|
| 1 | Shot 06 | adopted ✅ | Medium two-shot on Chris/Rick, corridor location, static or slow push-in | Fresh `image_references` (scene opener) |
| 2 | Shot 07 | adopted ✅ | Wide, door opening, Sharon walking toward camera | `--start-image` off clip 1's last frame — **but Sharon is a new character entering frame**, so per the continuity rules this can't combine `start_image` with her identity reference in one call. Treat her entrance as the natural cut: generate with `image_references` (Sharon + Chris + Rick + Jan refs, location plate), accept a fresh camera setup. |
| 3 | Shot 07b-1 | not yet generated as a separate still — see note below | Jan turns to address the gathering crowd, medium-wide | `--start-image` off clip 2's last frame (Jan/Chris/Rick already in frame, no new character) |
| 4 | Shot 07b-2 | adopted ✅ (this still IS the outburst peak) | Push in slightly on Jan as he flares up | `--start-image` off clip 3's last frame |
| 5 | Shot 07c | adopted ✅ | Jan mid-announcement, Rick skeptical in frame | `--start-image` off clip 4's last frame |
| 6 | Shot 08 | adopted ✅ | Chris heckles across the crowd — reset point (see below) | **Reset the chain here** (6-8 generation guidance) — fresh `image_references` off an undegraded location plate + Jan/Chris refs |
| 7 | Shot 08b | adopted ✅ | Jan presents the box, medium two-shot with Chris | `--start-image` off clip 6's last frame |
| 8 | Shot 09 | adopted ✅ | Jan's final outburst, push in tighter than 07b's flare-up for escalation | `--start-image` off clip 7's last frame |

**Note on clip 3 (Shot 07b-1)**: we only generated one still for the 07b beat, and it
captures the *peak* of the "SHUT UP!" outburst (now assigned to clip 4). The calmer
opening exchange (Jan's "Right guys—", the Sharon-pass question, his evasive answer,
the sniggering) doesn't have its own still yet. For video purposes this may not
matter — clip 3 could start from clip 2's last frame (calm) and animate directly into
clip 4's still (the outburst) as its end-frame — but flagging it since it means clip 3
has no independent still to sanity-check before spending video credits on it.

**Total estimated clips**: 8 (before any 07c/09 splitting decision — could rise to 10
if both are split rather than trimmed).

---

## Open decisions before generating any Scene 2 video

1. Crowd/extras consistency approach (see top of file).
2. Trim vs. split for Shot 07c and Shot 09's overflow dialogue.
3. Confirm clip 3 (07b-1) doesn't need its own still first, or generate one.
4. Video costs real credits (not free like the Nano Banana 2 stills) — confirm
   per-clip generation approval process before burning through the balance on 8+
   clips, several of which may need retakes given how often stills needed 2-3
   attempts to get continuity right.
