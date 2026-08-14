# 🎯 FLOW PROMPTING FOR CONSISTENCY — research synthesis + ready prompts

> **Written**: 2026-08-12. **Purpose**: how to prompt Google Flow so the cast, building and
> cartoon style stay locked — and the exact prompts for the final title-sequence video.
> Sources: web research (cited at bottom) + our own verified in-app findings in
> `TITLE_SEQUENCE_PLAN.md` and `HANDOVER.md`. Where they conflict, **our in-app findings win.**

---

## 1. The mental model — why consistency breaks

- **The model has no memory.** Every generation is a fresh task. Consistency comes only from
  what you attach and what you repeat — never from what you generated before.
- **Text alone is imprecise.** "A heavy-set man in his fifties" renders differently every time.
  Attachments (Character entities, plates, frames) are the real anchors; text steers.
- **Flow's composer trades off two locks** (verified in-app 2026-08-12):

| Mode | Locks | Loses | Use for |
| :--- | :--- | :--- | :--- |
| **Frames** (first/last frame) | background, architecture, colour, illustration style | cast identity (people invented) | animating a still you already composed |
| **Ingredients** (Character entities) | cast identity from model sheets | background & style (scene reinvented) | composing stills with the real cast |

- **Veo allows exactly ONE audio ingredient, and every Character carries a voice** — so at most
  ONE Character entity per Veo video generation. All five leads in one Veo take is impossible
  in Ingredients mode. This is why the title sequence is two-stage. *(Our finding; the public
  guides describe 1–3 reference images for Veo 3.1 Standard — Flow's Character-audio rule is
  stricter and is what the app actually enforces.)*

## 2. The rules that actually move the needle

1. **Compose in image mode, animate in Frames mode.** Nano Banana 2 image mode accepts all five
   Character entities + the courtyard plate at once (six ingredients, verified). The still has
   the real cast in the real building. Then Veo only has to move the camera — the one thing it
   does reliably.
2. **Verbatim rule.** Reuse character/location/style wording word-for-word across every prompt.
   Tests show full-vs-simplified descriptions swing consistency by ~40%. Our
   `featurette_prompt_engine_cartoon.md` character blocks and the cast-bible style anchor exist
   for exactly this reason — paste, never paraphrase.
3. **Name each attachment's role in the prompt.** "Use reference 1 as the character, reference 2
   as the environment…" measurably improves identity lock.
4. **One camera move per clip, in film terms** — "slow dolly in", "tracking shot", not prose.
   Add 2–3 specific motion cues max; competing instructions make output wander.
5. **Negative constraints matter.** "No text, no signage, no extra people, no skyline towers"
   prevents the model freelancing. (Veo once added sunglasses to a previously bare face
   mid-sequence in a documented test.)
6. **Never let Veo render lettering.** It redraws it every few frames. Titles are composited in
   post (`build_title_scroll.py`). Settled by the rejected take `1793b2a2`.
7. **Reroll at the STILL stage, not the video stage.** A wrong face in a start frame will be
   faithfully animated. Cheap to fix in Nano Banana, expensive in Veo.
8. **Trim from the head, keep clips short.** Use the first ~3s of each 8s render; drift grows
   with clip length.
9. **Keep lighting/angle consistent across shots** — big lighting jumps and extreme angles are
   the top causes of face drift between shots.
10. **Draft cheap, iterate one variable at a time.** Change one thing per reroll or you won't
    know what fixed it.
11. **Anchor scale to measurable objects in the scene — and verify by pixel measurement, never
    by eye** (learned the hard way 2026-08-12: two "scale looks OK" eyeball calls passed people
    drawn ~5× too tall). When placing people in a locked plate, the prompt must size them
    against a named reference: *"each person no taller than the door leaves directly behind
    them"* (door leaf ≈ 2.1–2.2m, person ≈ 1.7m ≈ 0.8× door at the same depth; courtyard trees
    ≈ 3× person height). Then **measure the result**: person pixel height ÷ door pixel height,
    corrected for depth (feet lower in frame = closer to camera = legitimately larger, ~ground
    plane: apparent size ∝ 1/depth, depth ∝ 1/(y_feet − y_horizon)). If the depth-corrected
    ratio isn't ≈0.8, re-roll — do not proceed to video, because Frames mode will faithfully
    animate the wrong scale.

## 3. The exact prompts for the final sequence

### Stage A — the start-frame still (Nano Banana 2, image mode, 16:9)

Setup: attach **5 Character entities** (project dropdown → *08 Aug, 16:58* → Characters) **+
`L01_establishing_courtyard_dusk.jpg`**. Six ingredients. If a face drifts, reroll the still.

```
Use the attached courtyard photograph as the EXACT background: same architecture, same brick,
same glazing, same dusk sky, same lighting, same illustration style, unchanged. Do not add or
invent any building, tower or structure anywhere in frame or on the skyline.

Place in it exactly five people and nobody else, drawn precisely from the attached character
sheets and matching them exactly in face, hair, build and wardrobe: all five small in the lit
entrance doorway, just stepping out, Jan Peach in front.

All wear burnt-orange PRISM lanyards. Stylised British sitcom comic art, clean bold line art,
flat muted colour palette, cel-shaded. NOT photorealistic.

Absolutely NO text, NO lettering, NO signage, NO captions anywhere in the image.
```

✅ Done — A1 has 4 on-model variants (in project `f2f0d2c9`; downloaded copies in
`character-refs/flow_downloads/grid_12/13/14/16`).

### Stage A variant — the S26 posed lineup with reference title (final shot)

Same six ingredients (L01 + @Jan Peach, @Christina Dross, @Sharon Enfield, @Chris, @Rick as
**@mention tokens**, rule: one @mention per character, plain-text names are weaker). Adds the
posed lineup, the **scale anchor** (rule 11), and the baked title that serves as a position
reference only — the real title is composited in post.

```
Use the attached courtyard image as the EXACT background: same architecture, same brick, same
glazing, same dusk sky, same lighting, same illustration style, unchanged. Do not add or invent
any building, tower or structure anywhere in frame or on the skyline. Place in it exactly five
people and nobody else: @Jan Peach, @Christina Dross, @Sharon Enfield, @Chris and @Rick,
matching their character sheets exactly in face, hair, build and wardrobe, standing in a posed
lineup facing the camera, full length, right at the lit entrance doors in the middle distance,
small in the frame - each person no taller than the door leaves directly behind them, the full
building facade and sky towering above them. All wear burnt-orange PRISM lanyards. Stylised
British sitcom comic art, clean bold line art, flat muted colour palette, cel-shaded. NOT
photorealistic. Render the words "CIRCLE THE SQUARE" in large bold white capital letters with a
thick black outline, centred in the upper middle of the frame against the sky. No other text,
signage or lettering anywhere else in the image.
```

### Stage B — the final video (Veo 3.1 Fast, Frames mode, A1 as FIRST frame, NO characters, x2)

```
Animate this image with a single very slow forward dolly push across the courtyard toward the
lit entrance, then hold. The five people walk straight toward the camera, growing as they come,
and pass either side of the lens and out of shot; the camera never turns. When the last one is
gone, the courtyard is empty and lit again and the push slows to a stop.

Keep the exact architecture, materials, colours, dusk lighting and illustration style of the
source image completely unchanged. Do not add, remove, redesign or move any structure, furniture
or object. Do not add any people beyond those already in the frame. Do not add text, signage or
lettering of any kind. One continuous camera move, no cuts, no speed changes. No dialogue, no
speech, no singing.
```

✅ Validated — takes `c606c18a` (better cast read) and `44d8f370` (earlier frame-clear, cleaner
title tail) both held style + faces for the full 8s. **Remaining: pick keeper, download at
"1K Original size" (1080p), then composite the title in post.**

### Fallback only — if a reroll won't clear frame in time

Chain Frames-mode clips with first AND last frame set (A1→A2→A3→A4 stills per
`TITLE_SEQUENCE_PLAN.md` §4). Endpoints that are close in perspective/scale/lighting avoid the
crossfade failure mode; describe the physical motion between them, don't just ask for a
"seamless transition".

## 4. Flow UI gotchas (verified in-app)

- **🆕 Video is always x1, and always the 20-credit Veo 3.1 Fast** (user rule 2026-08-12) —
  never x2+, never the 100-credit Quality tier. Images are free, so re-roll *stills* freely and
  spend video credits only on a locked start frame.
- **🆕 Use `@` mentions to bind Character entities in the prompt text** (verified 2026-08-12):
  typing `@Jan` opens the asset picker pre-filtered; click the Character row (not the image of the
  same name — `@Jan` also matches `L10_jans_office.jpg`) and confirm. The mention becomes an inline
  token AND attaches the entity chip. Use one @mention per character — plain-text names are weaker.
  Careful with substring collisions: `@Chris` also matches `Christina Dross`; pick the exact row.
- **🆕 Automation: never `keyboard.type` a multi-line prompt** — each `\n` is a Return, and Return
  SUBMITS. A 3-paragraph prompt fired as 3 separate generations (2026-08-12, six wasted images).
  Use `keyboard.insert_text` (no key events, cannot submit) for prose, `keyboard.type` only for the
  `@Name` trigger, and click **Create** deliberately at the end.
- **🆕 Automation: clicking the composer puts the caret where you click** — inserting text after a
  click can land mid-prompt. Always `Control+End` after focusing the textbox before inserting.
- **Click Create — don't press Return.** Return attaches the previous image instead of sending.
- **Window ≥1400px wide** or the composer hides under the sidebar and clicks land on Trash.
- **The asset picker reads across projects** (dropdown top-left): Characters live in `c1c8417d`,
  plates in `f2f0d2c9` — usable together, nothing needs duplicating.
- **The `<video>` preview is 720p.** 1080p masters only via *1K Original size* in the download menu.
- **Download hits a native Windows save dialog** automation can't drive — use the clipboard bypass
  or grab the media URL directly (see `flow_download_images.py` for the URL pattern).

## 5. Reference-image & credit limits (web research, verified 2026-08-14)

- **Ingredients panel = 3 upload slots** (Subject / Scene / Style) — this is the real ceiling for
  Flow's consumer Ingredients-to-Video feature. Third-party claims of "4 reference images" refer
  to Vertex AI's separate API-only reference-image feature, not Flow's UI — don't confuse them.
- **The Character/audio rule holds up against fresh research.** A saved Flow Character bundles
  visuals *and* an assigned voice profile (Google's own Character-creation docs confirm the
  pairing). Veo supports exactly one audio ingredient per generation, so **only one saved
  Character entity can go into a single Veo Ingredients-mode take** if you want it to speak —
  matches our 2026-08-12 in-app finding above. The other 1–2 ingredient slots can still hold
  non-Character images (a location plate, a style ref, a plain uncast photo) without triggering
  the audio conflict — Google's own prompting guide shows a two-person dialogue take built this
  way (raw reference images, not saved Characters).
- **Credits are monthly, not daily** — supersedes the "daily reset" note in
  `VIDEO_GENERATION_WORKFLOW.md`, which was written for the older Veo 2 free tier.
  **Google AI Pro** (this project's subscription, no API key/billing) = **1,000 Flow
  credits/month**. AI Ultra ($100/mo) = 10,000/month at roughly half the per-video cost below.
- **Per-generation cost, 4–8s clip:**

  | Tier | Credits (AI Pro) | Credits (AI Ultra) |
  | :--- | :--- | :--- |
  | Veo 3.1 Lite | ~10 | ~5 |
  | Veo 3.1 Fast (project default) | ~20 | ~10 |
  | Veo 3.1 Quality | ~100 | — |

  At Fast/x1 (this project's locked setting — see §4), 1,000 credits/month ≈ **~50 Veo 3.1 Fast
  8-second clips**. The 19-shot queue in `VIDEO_GENERATION_WORKFLOW.md` costs ~380 credits at one
  take per shot, leaving headroom for rerolls without exhausting the monthly allowance.

## 6. Sources

- [Veo 3.1 Prompting Guide — Pixel Dojo](https://pixeldojo.ai/guides/veo-3-1-prompting-guide)
  (mode playbook: i2v, references, first/last frame; name each reference's role)
- [Veo 3 Character Consistency with Scenebuilder — Easton Dev](https://eastondev.com/blog/en/posts/ai/20251207-veo3-character-consistency-guide/)
  (verbatim rule ~40% consistency swing; Scenebuilder Extend/Jump-to; negative prompts; lighting/angle continuity)
- [Veo 3.1 First and Last Frame Guide — FlowVeo3](https://flowveo3.com/posts/veo-3-1-first-last-frame-guide)
  (endpoint compatibility, describe physical motion not "seamless transition")
- [Veo 3.1 First→Last Frame workflow — VEO3 Gen](https://www.veo3gen.app/blog/veo-31-firstlast-frame-transitions-a-creator-workflow-for-smooth-beforeafter-rev)
  (3-part prompt: restate anchors, define transition path, constrain style/timing/audio)
- Our own: `TITLE_SEQUENCE_PLAN.md` §1 (Frames vs Ingredients tradeoff, 1-audio-ingredient rule),
  `HANDOVER.md` §6, `CARTOON_BUILDING_TRAILER_PLAN.md` §10.
- [Manage your Google Flow credits — Google Flow Help](https://support.google.com/flow/answer/16526234?hl=en)
  (monthly credit allowance by plan, per-generation costs by Veo 3.1 tier)
- [Bringing new Veo 3.1 updates into Flow — Google Blog](https://blog.google/innovation-and-ai/products/veo-updates-flow/)
- [Ultimate prompting guide for Veo 3.1 — Google Cloud Blog](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1)
  (multi-character dialogue via raw reference images, not saved Characters)
- [Veo 3.1 Ingredients to Video guide 2026 — veo3ai.io](https://www.veo3ai.io/blog/veo-3-1-ingredients-to-video-guide-2026)
  (3-slot Subject/Scene/Style panel)
- [Mastering Google Flow: Character & Avatar Creation — Kartaca](https://kartaca.com/en/mastering-google-flow-the-ultimate-guide-to-character-avatar-creation/)
  (Character entities bundle visuals + an assigned voice profile)
- [Google Veo 3.1 Ingredients to Video Update — CineD](https://www.cined.com/google-veo-3-1-ingredients-to-video-update-adds-native-vertical-format-4k-upscaling-and-enhanced-character-consistency/)
