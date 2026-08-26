# 🤝 HANDOVER — Circle the Square

> **For**: the next Claude Code session, likely on a different machine.
> **Written**: 2026-08-10, end of the session that switched the project to cartoon.
> **Repo**: https://github.com/pcturtle69uplandme/circle_the_square (private)
> **Read next**: **`featurette_storyboard_image_prompts.md`** ← 64 episode keyframes ·
> `CARTOON_BUILDING_TRAILER_PLAN.md` (✅ completed master trailer cut), `CARTOON_CAST_BIBLE.md`

> 🎬 **MASTER WORKFLOW (Adopted 2026-08-17)**: Google Flow generates isolated character stencils (clean background),
> composited with locked cartoon plates (`location-refs/cartoon-plates/`) and foreground furniture occlusion layers
> in Rive / layered canvas (`render_multiplane_frame.py`). Eliminates background drift, furniture amnesia, and scale hallucinations.
> All frames follow the strict HARD/SOFT Take QA checklist.

> 🧪 **PILOT IN PROGRESS (2026-08-25)**: Local video generation via **MiniMax-H3** is being
> trialled as a possible route for Scene 1, in parallel with the master workflow above — not
> yet adopted project-wide. **Read `minimax-h3-pipeline/README.md` and
> `SCENE1_MINIMAX_TRACKER.md` before touching this** — full details in §9 below.

---

## 1. What this project is

A British mockumentary comedy, *Circle the Square*, about **Jan Peach**, the pompous CEO of a company
called **PRISM**, and the meltdown he has over a missing pain au chocolat. 64 storyboard frames across
3 scenes are scripted, with dialogue, in `featurette_storyboard_image_prompts.md`.

**The building is real**: The Triangle, Cambridge (Eric Parry Architects) — photos in `building-reference/`.
It is in **low-rise Cambridge, not London**. Generations repeatedly defaulted to a London skyline; one
came back with Tower Bridge. Exclude it explicitly in every prompt.

---

## 2. The big pivot — read this before doing anything

The project **switched from photoreal to cartoon on 2026-08-10**, and the reason matters:

**Google Flow refused to generate photoreal Jan Peach.** Three attempts, all blocked, including on wording
as innocuous as *"sitting back in his chair, looking thoughtfully toward the camera, in quiet repose"*.
The same frame in comic style generated first try. Flow's own words: *"Bypassing the photorealistic
character entity did the trick."*

It reads as **likeness protection on a photoreal human face, not content policy** — he passed fine
small-in-frame in a wide two-shot and failed every solo close-up. The photoreal character sheets were
likely built from a real person's photograph.

**Do not try to go back to photoreal for characters.** It has been tested and it does not work.

The user also decided the deliverable is now a **cartoon animated video**, not a comic-strip storyboard.
So the 64 frames become keyframes for video rather than panels in a slideshow.

---

## 3. Current state

### ✅ Done

| Thing | Where |
| :--- | :--- |
| 11 cartoon character model sheets | `character-refs/*_cartoon_sheet.jpg`, committed |
| Full cast specs, style anchor, prompt template | `CARTOON_CAST_BIBLE.md` |
| Character bible rebuilt around cartoon | `character-bible.html` |
| Photoreal sheets retired but kept as spec | `character-refs/_photoreal-archive/` |
| 7 of 11 characters saved in Google Flow | Flow project (see §4) — ✅ **verified in Flow 2026-08-11** |
| 5 principals have voices attached in Flow | Flow project |
| **26 cartoon plates downloaded** (11 of 12 L-numbers + 6 bonus) | `location-refs/cartoon-plates/` + `PLATES_MANIFEST.md` |
| 12-plate shot list for drone moves | `LOCATION_PLATE_SHOT_LIST.md` |
| 64 keyframe prompts, cartoon style anchor | `featurette_storyboard_image_prompts.md` |
| **Scene 1 Storyboard Frames Approved (F01–F17)** | `storyboard-frames/F01.jpg` through `F17.jpg` (all verified & committed) |
| **Building Trailer Master Complete** (25 shots, 1080p) | `clips/CARTOON_BUILDING_TRAILER_FULL.mp4` |

### ⬜ Next steps, in priority order (Session 2026-08-15 Handover)

1. **Continue generating Scene 1 frames in Google Flow starting at Frame F18**:
   - **F18**: Jan alone, sweating profusely, panting, unbuttoning shirt to cool down.
   - **F19**: Jan removes shirt, baring chest, visual gag with manscaped arrow pattern.
   - **F20**: Sharon walks in unannounced, Jan reacts in alarm.
   - **F21–F26b**: The arrow reveal, Sharon conversation, Jan shutting venetian blinds and locking the door.
   - Prompts, continuity flags, and attach legends are in `featurette_storyboard_image_prompts.md`.
2. **Engines / Directives**:
   - **Google Flow ONLY** (User directive: do not use local FLUX.2 or CLI for this run; use Google Flow via browser).
   - Character entities: `@jan`, `@christina`, `@sharon` saved in Flow.
   - Attach the previous approved frame (e.g. `F14.jpg`/`F16.jpg` for F18) to preserve desk/furniture/geometry.
   - Output destination: save/download keepers at 1K Original Size to `storyboard-frames/<FRAME_ID>.jpg` and tick the tracker.
   Background roles, no voices exist for them. All four already have cartoon sheets on disk.
4. **L04 tower detail** is the one missing plate — brick tower and glazed timber lantern box against
   a dusk sky. Everything else on the 12-plate list is done. Not needed for the building trailer.
5. **Then**: animate the 64 keyframes as Veo moves for the episode proper, and recut the character
   trailers over the `Small Stakes` / `Paper Trail` beds.

### ✅ Flow inventory — verified 2026-08-11

Checked directly in the live project, settling the earlier disagreement. **7 characters saved**:
Jan Peach, Christina Dross, Sharon Enfield, Chris, Rick, Maureen, Gemma Ashcroft. The project memory
note claiming "all six leads" was wrong, and `CARTOON_CAST_BIBLE.md`'s "none saved" was badly stale.
**37 generated images total**: 11 character sheets (all already on disk) + 26 plates (now downloaded).

### 🎞️ The existing clips are photoreal — all 17 of them

Everything in `clips/`, including `ACTION_TRAILER_MASTER_60S.mp4`, `SMALL_STAKES_TRAILER_MASTER_60S.mp4`
and `PAPER_TRAIL_TRAILER_MASTER_78S.mp4`, was rendered before the pivot. Worse, S01/S02 show a **glass
skyscraper** — wrong for The Triangle regardless of style. **Every picture needs re-rendering.**
What survives: the edit structures in `ACTION_TRAILER_DIRECTORS_PLAN.md`, and the scored beds in
`audio-refs/` (style-agnostic).

### 📭 Deliberately empty

`storyboard-frames/` holds only `README.txt`. The user cleared it to start from F00. The 25 old
photoreal frames are **recoverable**: `git checkout 1380f97 -- storyboard-frames/` — but they are
photoreal, so leave them buried.

---

## 4. Google Flow — the working environment

**Project**: "Circle The Square TV C…" at
`https://labs.google/fx/tools/flow/project/c1c8417d-30c8-4e76-a58c-260fec3f7a40`
Account is PRO. Model in use: **Nano Banana 2**.

**Characters saved** (portrait + profile; voice where noted):

| Character | Voice attached | Accent |
| :--- | :--- | :--- |
| Jan Peach | ✅ | British RP, "boardroom" kind |
| Christina Dross | ✅ | Clear British London RP |
| Sharon Enfield | ✅ | Welsh, subtle lilt |
| Chris | ✅ | Dry South London Estuary |
| Rick | ✅ | Flat Midlands / East Anglian |
| Maureen | — | canteen worker, has one line |
| Gemma Ashcroft | — | receptionist |

**The five voices already existed in Flow** before this session, matching the bible exactly. Do not
create new ones — select the existing ones.

---

## 5. Style transfer — the method that works

The user's idea, and it is better than describing a location from scratch. Attach a **real photo** of
the building and restyle it. Geometry, camera angle and materials are preserved; only the rendering
changes. Verified working on the courtyard exterior.

```
Redraw this photograph as a stylised comic illustration. Keep the exact architecture,
camera angle, composition and proportions of the original photo - do not redesign the
building, do not move the camera, do not add or remove any structures. Only change the
rendering style. Keep the pale buff brick and precast concrete banding, the grid of tall
narrow windows, the glazed timber lantern box on the tower, and the low-rise setting.
Style: stylised British sitcom comic art, clean bold line art, flat muted colour palette,
cel-shaded, simplified detail. Absolutely NO text, NO signage lettering, NO captions
anywhere in the image.
```

**"Only change the rendering style" is doing the heavy lifting.** Without it the model treats the photo
as loose inspiration and reinvents the building.

The real photos are already uploaded to Flow — see the **Uploads** tab in the left sidebar.

---

## 6. Gotchas learned the hard way

**Google Flow UI**
- **Pressing Return in the composer attaches the previous image** instead of sending, silently turning a
  fresh generation into an edit. Click the **Create** button instead.
- **Image-to-image edits that insert a person get policy-blocked** even when the equivalent fresh
  text-to-image generation succeeds. Regenerate rather than edit — **for people only.**
- **Edits that change scenery work fine, and are better than regenerating.** Proven 2026-08-11:
  `L10_jans_office` came back with The Shard in the window and an edit removed it while preserving
  every piece of set dressing. Regenerating would have rerolled the whole room. Prompt in
  `LOCATION_PLATE_SHOT_LIST.md` §⚠️.
- The asset picker labels everything `Character model sheet…` with thumbnails too small to tell apart.
  **Always click an asset and check the preview before adding it** — a sheet was attached to the wrong
  character this way. Renaming assets in Flow would fix this permanently.
- **Download is two steps**: the download icon, then "1K Original size" in the dropdown.
- **⚠️ Chrome is set to "Ask where to save each file", which opens a native Windows save dialog.
  Claude cannot control native dialogs** — it blocks the tab and the download never completes.
  Either the user turns that setting off, or use the bypass below.
- **Bulk download bypass that works** (used for all 26 plates on 2026-08-11, no dialogs):
  1. In-page JS: `fetch('https://labs.google/fx/api/trpc/media.getMediaUrlRedirect?name=<mediaId>')`
     → `arrayBuffer` → base64 → `navigator.clipboard.writeText(...)`. Batch ~5 per clipboard write.
  2. PowerShell: `Get-Clipboard -Raw` → `[Convert]::FromBase64String` → `[IO.File]::WriteAllBytes`.
  - **The page must have focus** or `clipboard.writeText` throws "Document is not focused" — click an
    empty area of the page first.
  - **Generated images are 1376×768**; uploaded reference photos are every other size. That is a
    reliable way to separate Flow's own output from the source photography.
  - The Images grid is **virtualised** — off-screen thumbnails unmount, so scroll in steps and
    accumulate media IDs as they pass through rather than reading the DOM once.
- Downloads land in **`C:\kontitemp\ai\circle_the_square\images\`** on the original machine, not `~/Downloads`.
- Flow ignores multi-character composition instructions unless you say **"both must appear together in
  this one wide frame"** explicitly.
- Flow renders **16:9**, not the 2.39:1 in the style anchor. Crop after, or accept it.
- Beware stale coordinates after the window resizes — it caused mis-clicks including an accidental Share
  dialog and two items sent to trash. Prefer the `find` tool over fixed coordinates.

**Image generation routes** — full detail in `.agents/rules/cli_image_quota_rules.md`
- **CLI first, browser only when CLI quota is spent.** That is the user's settled rule.
- **`agy` (Antigravity CLI) has the `generate_image` tool but cannot drive a browser. Claude Code drives
  Chrome but has no `generate_image`.** So CLI batches run in `agy`, then hand over to Claude for Flow.
  Run `agy -i` — `agy -p` headless auto-denies tool permissions.
- **Two different 429s.** `cloudcode-pa` is a 12-per-rolling-4-hours subscription window — wait it out or
  switch to Flow. `interactions.create()` reporting *"prepayment credits are depleted"* is **billing**
  exhaustion that waiting never clears.
- **`gen_image.py` on Gemini is blocked** — prepay credits depleted. Do not waste time on it.
- Do not suggest buying another hosted engine to escape content filters. Most carry comparable policy.

**Video generation route — settled 2026-08-13**
- **Local video generation (WAN 2.2, run through ComfyUI) was tried and abandoned — too slow to be
  usable.** Test case: `T25_group_photo` regenerated locally as `T25_group_photo_wan22_seed20260813_49f.mp4`
  plus QC frames in `preview_frames/wan22/`; deleted 2026-08-14 once the user confirmed the render time
  wasn't worth it. **Do not suggest local WAN 2.2 (or another local video model) as a route — it's been
  tested and rejected on speed, not quality.** Video generation stays on **Google Flow / Veo 3.1** (cloud,
  subscription-based, no API key) — see `FLOW_CONSISTENCY_PROMPTING_GUIDE.md` and §0 above for credits/limits.
  Local generation is still fine for **images** (CLI `generate_image`, per the quota rules below) and for
  audio (MusicGen, Qwen3-TTS) — the rejection is video-specific.

**Machine-specific — will differ on a new machine**
- `gen_image.py` and `fal_key.py` live at **`C:\kontitemp\ai\`**, one level *above* the repo, and are
  **not in version control**. They will not exist after a fresh clone.
- Three scripts hardcode `AI_DIR = Path(r"C:\ai\AI")`, a path that does not exist. One-line fix each.
- The **local GPU stack is absent** — no torch, no CUDA, no ComfyUI. All the IP-Adapter and MusicGen
  scripts will fail.
- **`.git` is ~581 MB** because of the image history. A fresh clone will be slow.

---

## 7. Working with this user

- They move fast and change direction mid-task. Check current intent rather than assuming the last
  instruction still holds — the CLI-only rule was reversed within the hour, and the deliverable changed
  from comic storyboard to animated video.
- They will interrupt with "stop" mid-operation. Stop immediately and do not tidy up afterwards.
- They ask for corrections directly and expect them applied, not debated.
- Continuity accuracy matters to them: the building is Cambridge not London, the company is PRISM not
  Peach Corp, and panels carry no lettering because the viewer draws its own speech bubbles.

---

## 8. Doc status after the cartoon repoint (2026-08-11)

Every `.md` was swept for photoreal-era assumptions. Where a doc's *structure* was still sound but its
*style block* was not, the structure was kept and the style swapped — the shot lists and edit plans
represent real work and did not need throwing away.

### 🎨 Live — cartoon, use these

| Doc | Role |
| :--- | :--- |
| `CARTOON_CAST_BIBLE.md` | **Cast + style source of truth.** 11 characters, style anchor, prompt template |
| `featurette_storyboard_image_prompts.md` | **The working doc.** All 64 keyframes, cartoon anchor, `@tag` legend |
| `MASTER_STORYBOARD_SESSION_PROMPTS.md` | Ready-to-paste cartoon prompts, Scene 1 from F01 |
| `LOCATION_PLATE_SHOT_LIST.md` | 12 cartoon plates + the camera move each feeds |
| `MASTER_PRODUCTION_MANUAL.md` | Umbrella manual, cartoon banner + corrected rosters |
| `OPENING_TITLE_SEQUENCE_PLAN.md` | Title sequence, structure locked, awaiting cartoon re-render |

### ⛔ Superseded — reference only

`featurette_prompt_engine.md` and `storyboard_prompt_engine.md` (photoreal Veo prompts; workflow and
20-shot structure still useful), `featurette_shot_list.md`, `location-bible.html` (photoreal locations),
`ACTION_TRAILER_DIRECTORS_PLAN.md` (edit structure survives, footage does not).

### Things fixed along the way

- **`MASTER_PRODUCTION_MANUAL.md` §3 listed 9 locations, 7 of which named files that never existed.**
  Replaced with the true 7-file on-disk inventory, each mapped to its pending cartoon plate.
- **Maureen was being invented per-frame.** F47/F48/F51 told you to let the model make up a canteen
  worker; she has had a sheet since 2026-08-10. Now `@maureen` in all three.
- **Rick was described as security** in the session prompts, contradicting the bible. He is
  rank-and-file staff.
- **Frame count confirmed at 64.** Easy to miscount as 58: there is no plain F06, F26 or F37 because
  those beats are split into `F06a/F06b`, `F26a/F26b`, `F37a/F37b`. Highest ID is F61, true count is 64.
  Verified: 64 tracker rows, 64 prompt blocks.
- `storyboard_slideshow.html` is now framed as a **continuity-checking tool**, not the deliverable.

---

## 9. Session 2026-08-25 — photoreal stills route, MiniMax-H3 pilot, Scene 1 QA gap

### What changed

1. **Full 11-character photoreal cast completed.** 5 principals (Jan, Christina, Sharon,
   Chris, Rick) already had photoreal turnaround sheets in `character-refs/_photoreal-archive/`
   from before the cartoon pivot. The 6 supporting cast (Maureen, Gemma Ashcroft, Priya
   Raghavan, Barbara Whitlock, Dev Osei, Tomasz Wojcik) were generated this session, locally,
   via **FLUX krea-dev through ComfyUI** — no cloud calls. This is a separate, photoreal track
   alongside the cartoon assets, not a replacement for them.
2. **`gen_image.py` (Google Gemini cloud stills) is confirmed dead** — hit "prepayment
   credits depleted" on the very first supporting-cast attempt. Matches the prior finding in
   `.agents/rules/cli_image_quota_rules.md`. Local FLUX (krea-dev for fresh generations,
   Kontext-dev for reference-conditioned edits) is now the only working stills route.
3. **Location references confirmed already complete and photoreal** — all 5 script locations
   (`location-refs/*_location_sheet.jpg`) predate the cartoon pivot and didn't need
   regenerating. One bug found and fixed: `jan_office_location_sheet.jpg` had The Shard /
   London skyline through the window (the exact bug `HANDOVER.md` §6 already flagged for the
   cartoon plates, but this photoreal sheet had its own uncorrected instance). Fixed via
   FLUX Kontext-dev edit → `location-refs/jan_office_location_sheet_fixed.png`. **Use the
   `_fixed` version, not the original, for anything referencing Jan's office going forward.**
4. **MiniMax-H3 piloted as a local video route** — see `minimax-h3-pipeline/README.md` for
   full technical detail (hardware constraints, gotchas, exact CLI usage). Short version: it
   works, produces identity-consistent photoreal *and* cartoon video with synced audio in
   ~4-5 min/clip on the RTX 4080, and is a genuinely different finding from the WAN 2.2
   rejection in §6 — not being proposed as a full replacement for Flow/Veo yet, but validated
   enough to attempt a real scene with.
5. **Scene 1 (28 keyframes, F01-F26b) shot-planned for MiniMax-H3 generation** — see
   `SCENE1_MINIMAX_TRACKER.md`. Only F01 and F02 (2 clips) were actually generated before
   pausing; **both are provisional and will be redone**, not carried forward. Two real
   problems surfaced during that first attempt, now written up as standing QA rules in that
   tracker:
   - The office reference was missing venetian blinds needed later in the same scene (F26a,
     "Jan yanks the blinds shut") — nothing had scanned the *full* script for fixtures
     introduced late in a location that still need to exist in its reference image from frame
     one. `MASTER_PRODUCTION_MANUAL.md` §8 (prop/continuity table) exists and is the right
     place to track this, but doesn't mention blinds — needs updating once the reference fix
     lands.
   - Dialogue was rushed — a 14-word line doesn't fit naturally in a 2.33s clip at
     conversational pace (~2.2-2.5 words/sec ⇒ ~5-6 words/clip, not the ~11 assumed). The
     original 39-clip estimate for Scene 1 under-counts how many clips long lines actually
     need; expect the real count to be meaningfully higher once re-planned.

### Next steps, in priority order

1. Before regenerating anything: fix the blinds gap (edit prompt drafted, not yet run — see
   `SCENE1_MINIMAX_TRACKER.md` restart plan), re-audit `MASTER_PRODUCTION_MANUAL.md` §8
   against the whole script (not just Scene 1) for similar late-introduced-fixture gaps in
   the other 4 locations, and re-plan Scene 1's clip count against the corrected dialogue-pace
   assumption.
2. Regenerate F01, then F02 (both clips), then continue forward through the shot list —
   `SCENE1_MINIMAX_TRACKER.md` has the full 28-keyframe breakdown and per-clip status.
3. Once Scene 1 is validated end-to-end (identity, location, pacing, no drift between clips
   sharing a reference), decide whether MiniMax-H3 becomes the adopted route for Scenes 2-3
   too, or whether Flow/Veo stays primary with MiniMax-H3 as a supplementary tool. Not yet
   decided — this session only validated the pipeline works, not that it should replace the
   master workflow.

### Addendum — Session 2026-08-26: MiniMax-H3 speed work

Not a Scene 1 shot session — pure pipeline speed/duration work, prompted by per-clip time
(~5.3min for 2.3s) feeling slow. Full detail in `minimax-h3-pipeline/README.md` and
`SCENE1_MINIMAX_TRACKER.md` QA Rule 2; summary:

- Ruled out forcing the 32B text encoder onto GPU (`--stream-layers`) — tested, it's 13x
  *slower* (20.7min vs 96s) and still OOMs afterward. Don't retry this.
- Added EasyCache + a turbo denoiser checkpoint (`minimax_h3_ref2va_turbo_Q4_K_M.gguf`,
  downloaded this session) — both now default in `gen_clip.py`/`chain_clips.py`. Per-clip
  time down from ~5.3-5.5min to ~3.4min, quality checked and holding up (must use
  `--steps 4 --guidance 1.0` with this specific turbo file, not 8 — see README).
- Added `chain_clips.py` for chunked/chained generation past the ~56-frame single-pass VRAM
  ceiling (last frame of chunk N seeds chunk N+1). Validated on a generic test scene: 11.7s
  in ~19-20min. Cut points are seamless; there's a real compounding framing/zoom-in drift
  within each chunk's own generation, not yet mitigated — read the README section before
  using this on a real shot with more than 2-3 chunks.
- Re-estimate any Scene 1 clip-count/timing plan against the new ~3.4min figure.
- **Follow-up same day: regenerated F01/F02 for real, found two more problems, pivoted to a
  second local model.** Full detail in `minimax-h3-pipeline/README.md` and
  `wan22-pipeline/README.md`; summary:
  - Turbo's audio is broken (not just a risk — verified with Whisper transcription: standard
    model transcribes dialogue exactly right, turbo transcribes as empty/wrong on every
    chunk tested despite fine-looking video). Defaults flipped back to standard+EasyCache;
    `--turbo` is now opt-in for no-dialogue shots only.
  - The chain-concat "hard cuts" turned out to be a real bug (naive `-c copy` stream-copy
    concat corrupts audio at AAC splice boundaries) — fixed by re-encoding on concat.
  - **F01-type wide shots are a dead end on MiniMax-H3**: faces resolve to a genuinely
    featureless blob at 864x480 in a full-room wide framing (checked at native pixel crop) —
    a pixel-count problem, not a quantization one. Checked the next-tier quantizations
    (Q5_0/Q6_K/Q8_0 — 13.9-21.4GB) and none fit this 16GB card without offloading the
    diffusion model itself, which is exactly the failure mode that made WAN 2.2 (14B) and
    FLUX.2 klein "unusably slow" in earlier sessions (see §6) — did not pursue.
  - Google Flow was considered as the wide-shot replacement but is blocked by Flow's
    likeness/content filters on photoreal human generation/action prompts.
  - **Pivoted to Wan 2.2 TI2V-5B** (the dense 5B model, not the 14B MoE variant already
    rejected) as a second local pipeline specifically for wide/establishing/silent shots —
    see `wan22-pipeline/README.md`. Validated: single-pass 10-second clips (no chaining, no
    drift) in ~9 minutes, sharper output than MiniMax-H3, fits in 16GB VRAM without the
    RAM-offload trap (critical: needs `--vae-tiling`, or VAE decode alone takes 13+ minutes).
    Trade-offs: single-reference-image only (no true multi-ref like Ref2VA — needs
    bootstrapping the reference from an existing well-framed frame, e.g. a MiniMax-H3
    output), and no audio at all (fine, since this pipeline is only for shots that don't
    need dialogue — those stay on MiniMax-H3).
  - **Net result**: two local pipelines now, split by shot type — MiniMax-H3
    (`minimax-h3-pipeline/`) for close-up dialogue shots, Wan 2.2 TI2V-5B
    (`wan22-pipeline/`) for wide/establishing/silent shots. Neither Flow nor a single unified
    pipeline covers both needs on this hardware.

### Addendum — Session 2026-08-26, continued: F01's wide-shot-with-dialogue conflict solved

F01 needed both a wide shot (Wan's strength) and a real dialogue line (only MiniMax had
working audio) — this was left unresolved above. Explored two ComfyUI-based fixes in the
same session, in parallel, for comparison:

- **H3-FaceRefine** (crop the face, re-render through MiniMax-H3 itself at high
  magnification, keep native audio): got the whole thing running after a genuinely large
  environment-fixing effort (see `wan22-pipeline/comfyui-tools/README.md` for the full,
  ugly chain — VS Build Tools, a full CUDA Toolkit install, a source-patched `mmcv`, a real
  dtype bug fixed in ComfyUI's own core MiniMax code). Even working correctly (~11x face
  magnification, confirmed via the tool's own diagnostic logging), **it did not actually
  sharpen Jan's face** on the real F01 test case — still an unresolved blob at default
  tuning. Not adopted; not worth further parameter-hunting given the alternative below
  already works.
- **Wan (silent) + Qwen3-TTS (voice clone) + MuseTalk (lip-sync)**: also required a large
  environment-fixing chain (same doc), but **this one actually works** — validated
  end-to-end with a real test: cloned Jan's voice from an already-verified-correct
  MiniMax-H3 audio sample, generated new dialogue with Qwen3-TTS, lip-synced it onto a
  silent Wan clip with MuseTalk. Whisper transcription of the final muxed video exactly
  matched the target text; frame-by-frame inspection showed real, varying mouth shapes in
  sync with speech, no visible seam.

**This is now the answer for any wide/establishing shot that needs dialogue.** Full setup
and usage documented in `wan22-pipeline/comfyui-tools/README.md` (a `graph_to_prompt.py`
tool is included there too, for driving ComfyUI headlessly via its `/prompt` API when the
Chrome browser extension isn't available). Not yet applied to F01 itself — see
`SCENE1_MINIMAX_TRACKER.md` row 1 for the concrete next step.
