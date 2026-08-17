# 🎬 RIVE CUTOUT-RIGGING PIVOT — read this before touching character animation

> **Branch**: `rive-cutout-rigging-pivot` (created 2026-08-17, off `main`).
> **Status**: proof-of-concept only. One character (Jan Peach), one pose (front view), no bones yet.
> **Read alongside**: `HANDOVER.md` (overall project state), `.agents/rules/browser_automation_cdp.md`
> (the browser-automation method used to build this — now updated with Rive-specific gotchas).

---

## 1. Why this exists

The animation step (Google Flow / Veo, per `HANDOVER.md` §6) generates a fixed clip from a text/image
prompt each time. Getting a specific character pose or expression exactly right means re-rolling
generations and hoping — there's no way to reach in and adjust a hand, an eyebrow, a stance. The user
flagged this as the main time-sink: **"lots of re-generation even after QA."**

The fix being tested here is not a replacement for Flow — it's a narrower tool for the piece Flow is
worst at. **Backgrounds, plates, and static keyframes stay exactly as they are** (Google Flow /
Nano Banana 2, per `HANDOVER.md` §4-5, `LOCATION_PLATE_SHOT_LIST.md`). What's being piloted is
swapping **character performance** — the part that needs fine, repeatable, art-directable control —
onto a cutout/bone-rig tool, where a character is posed directly instead of re-prompted.

This is only viable *because* of an earlier pivot: the project moved from photoreal to **cartoon /
cel-shaded** art on 2026-08-10 (`HANDOVER.md` §2). The character sheets in `character-refs/*_cartoon_sheet.jpg`
are clean flat-color turnaround sheets (front/¾/side/back on solid grey) — exactly the reference format
a cutout rig needs. This pivot would not have been feasible against the old photoreal style.

## 2. What was actually tried, in order

1. **Synfig Studio** (free, open-source, desktop) was installed via `winget install Synfig.SynfigStudio`
   and validated first. Jan's front-view pose was cut out of `character-refs/jan_peach_cartoon_sheet.jpg`
   (script-based background removal, see `character-refs/rigging-test/`) and a minimal `.sif` project
   importing it was hand-written and confirmed to render correctly via Synfig's own CLI renderer
   (`synfig.exe file.sif -o out.png`). **This works and is still available as a fallback** — but Synfig
   is a native desktop app, and this session has no way to drive its GUI (only browser automation is
   available; raw Windows `SendInput`/`mouse_event` calls were tried and **do not reach the real
   interactive desktop session** — clicks land nowhere, confirmed by two failed attempts at
   pixel-verified coordinates). Building an actual bone rig in Synfig would require the human doing it
   by hand in the GUI, using `character-refs/rigging-test/jan_rig_test.sif` as the starting point.
2. **Rive** (rive.app, browser-based) was chosen instead specifically because it's inside Chrome, where
   the existing CDP browser-automation toolkit (see `.agents/rules/browser_automation_cdp.md`) gives
   **real, verified control** — clicking, typing, drag-and-drop, and file upload all confirmed working.
   This is the live path being built out.

## 3. Current state of the Rive file

- Live at **https://editor.rive.app/file/untitled/2513750** — under the user's own Rive account
  (`pcturle69 uplandme`, project "Pcturtle"). Still titled "Untitled" (renaming via the tab wasn't
  worth the extra coordinate-guessing risk — the numeric file ID in the URL is what's permanent).
- Artboard sized **678×1385px**, matching the cutout exactly.
- `jan_front_cutout.png` (background-removed front-view pose, also saved locally at
  `character-refs/rigging-test/jan_front_cutout.png`) is uploaded as an Asset and placed centered
  (Position 339, 692.5 — i.e. exactly the artboard midpoint) filling the frame edge-to-edge.
- **No skeleton/bones yet.** This is the actual next step, not done in this session — see §5.

## 4. Files this pivot added

| File | What it is |
|---|---|
| `character-refs/rigging-test/jan_front_cutout.png` | Jan's front pose, isolated from the 4-pose turnaround sheet, background removed (alpha channel), used as the Rive/Synfig source image |
| `character-refs/rigging-test/jan_rig_test.sif` | Synfig project importing the cutout — confirmed valid via CLI render, no bones |
| `character-refs/rigging-test/jan_rig_test_render.png` | CLI-rendered proof the `.sif` file is valid (transparent background correct) |
| `cdp_click_type.js`, `cdp_click_slow.js`, `cdp_drag.js`, `cdp_upload.js`, `cdp_set_viewport.js` | New additions to the CDP browser-automation toolkit (repo root, alongside the existing `cdp_*.js` scripts) — needed because Rive's editor is canvas-rendered like Flow's, so no DOM selectors work, and it needed drag-and-drop plus native file-upload handling that the older scripts didn't cover |
| `.agents/rules/browser_automation_cdp.md` | Updated: new script table rows, a note that this method now also drives non-Flow sites, and a new gotcha about the browser viewport silently drifting out of sync with screenshot coordinates (see below) |

## 5. Next steps, in priority order

1. **Build the actual bone rig for Jan** in the live Rive file above: Bone tool (toolbar) to lay a
   chain over the cutout (spine, two arms, optionally legs), then select the image layer and use its
   **Deform** section (visible in the right-hand inspector once the layer is selected) to bind it to
   the bones. Rive can deform a single flat bitmap with bones directly — it does **not** require
   pre-cutting the character into separate limb layers first, which is what makes this fast.
2. **Test posing** — move a bone, confirm the cutout bends convincingly at the joint, iterate on bone
   placement/weighting until a shoulder or elbow move looks right.
3. **Decide the export/composite path** before scaling to more characters: Rive exports to its own
   `.riv` runtime format, or can be rendered out as a PNG sequence / video. Whichever is chosen has to
   composite over the Flow-generated background plates (`location-refs/cartoon-plates/`) in whatever
   the final assembly pipeline is — this hasn't been figured out yet and is a real open question, not
   a detail.
4. **Only after Jan's rig is proven** — repeat for the other 10 characters in `CARTOON_CAST_BIBLE.md`.
   Don't build 11 rigs before validating the one.
5. Update `HANDOVER.md` §6 ("Video generation route") once this is far enough along to be a real
   decision, not a experiment — right now Flow/Veo is still the settled route for actual animation;
   this pivot has not been adopted project-wide, it's a branch-scoped test.

## 6. Gotcha carried over from this session (full detail in browser_automation_cdp.md)

Rive's editor is **entirely canvas-rendered** — no real DOM buttons/inputs, so `cdp_click.js`
(text-matching) never works there; go straight to coordinate clicks. Also, the browser window's
viewport can silently drift (observed 1600×1000 → 1535×1538 mid-session, source: an unrelated
Windows-desktop-automation attempt sending real input to the same screen region) which invalidates
previously-measured coordinates with no error. Run `cdp_set_viewport.js` to re-lock it and re-measure
from a fresh screenshot if clicks that used to land stop doing anything.
