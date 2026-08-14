# 🤝 HANDOVER — Circle the Square

> **For**: the next Claude Code session, likely on a different machine.
> **Written**: 2026-08-10, end of the session that switched the project to cartoon.
> **Repo**: https://github.com/pcturtle69uplandme/circle_the_square (private)
> **Read next**: **`featurette_storyboard_image_prompts.md`** ← 64 episode keyframes ·
> `CARTOON_BUILDING_TRAILER_PLAN.md` (✅ completed master trailer cut), `CARTOON_CAST_BIBLE.md`

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
| **All docs repointed to the cartoon path** (2026-08-11) | see §8 |
| **Building Trailer Master Complete** (25 shots, 1080p) | `clips/CARTOON_BUILDING_TRAILER_FULL.mp4` |

### ⬜ Next steps, in priority order

1. **Generate the 64 keyframes** against the saved Flow characters and the downloaded cartoon plates.
   The plates that used to block this are done. See `featurette_storyboard_image_prompts.md`.
2. **Add the last 4 Flow characters**: Priya Raghavan, Barbara Whitlock, Dev Osei, Tomasz Wojcik.
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
