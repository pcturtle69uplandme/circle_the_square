# 🤝 HANDOVER — Circle the Square

> **For**: the next Claude Code session, likely on a different machine.
> **Written**: 2026-08-10, end of the session that switched the project to cartoon.
> **Repo**: https://github.com/pcturtle69uplandme/circle_the_square (private)
> **Read next**: `CARTOON_CAST_BIBLE.md`, `LOCATION_PLATE_SHOT_LIST.md`, `.agents/rules/cli_image_quota_rules.md`

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
| 7 of 11 characters saved in Google Flow | Flow project (see §4) |
| 5 principals have voices attached in Flow | Flow project |
| 3 cartoon location plates generated | Flow project only, not downloaded |
| 12-plate shot list for drone moves | `LOCATION_PLATE_SHOT_LIST.md` |

### ⬜ Next steps, in priority order

1. **Style-transfer the rest of the building photos to cartoon.** This is the live task and the method
   is proven — see §5. The user wants a library of cartoon plates to animate into video.
2. **Add the last 4 Flow characters**: Priya Raghavan, Barbara Whitlock, Dev Osei, Tomasz Wojcik.
   Background roles, no voices exist for them.
3. **Download the cartoon plates** into the repo — needs the user's say-so, it is a file download.
4. **Then**: the 64 frames, generated against the locked Flow characters, as video keyframes.

### 📭 Deliberately empty

`storyboard-frames/` holds only `README.txt`. The user cleared it to start from F00. The 25 old
photoreal frames are **recoverable**: `git checkout 1380f97 -- storyboard-frames/`

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
  text-to-image generation succeeds. Regenerate rather than edit.
- The asset picker labels everything `Character model sheet…` with thumbnails too small to tell apart.
  **Always click an asset and check the preview before adding it** — a sheet was attached to the wrong
  character this way. Renaming assets in Flow would fix this permanently.
- **Download is two steps**: the download icon, then "1K Original size" in the dropdown.
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
