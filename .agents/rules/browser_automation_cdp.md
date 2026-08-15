# Browser automation for Google Flow — persistent Playwright + CDP

## The problem this solves
Claude Code's `claude-in-chrome` MCP extension (its `computer`/`screenshot`, `get_page_text`, `find`
tools) **hangs indefinitely on the Flow project canvas** — `Page.captureScreenshot` times out after
30s, `get_page_text`/`find` time out after 45s waiting for `document_idle` that never fires. This is
consistent across tab reloads, new tabs, and even a full Chrome process restart (2026-08-15). Root
cause: Flow's canvas is a continuous WebGL/animation-loop SPA that appears to never yield a stable
compositor frame or hit network-idle, which the extension's CDP bridge waits on. **Do not keep retrying
the extension tools on this page — it is not transient.**

## The working method
Launch a **separate, real Playwright-controlled Chrome** (not the extension's browser) with a remote
debugging port open, then drive it via short-lived `connectOverCDP` scripts. This works because
Playwright's own `page.screenshot()` / `page.evaluate()` don't share the extension's stuck code path.

### 1. Launch once (background, stays open)
```powershell
cd "C:\AI\Circle the Square"
node persistent_launch.js
```
Run this **in the background** (it blocks forever on purpose — `await new Promise(() => {})` — to keep
the CDP port alive for follow-up scripts). It:
- Opens a **persistent** Chrome profile at `C:\ai\.chrome_playwright_profile` (`channel: 'chrome'`,
  `headless: false`, `--remote-debugging-port=9222`)
- Navigates to the Flow project/edit URL (edit the `FLOW_URL` const at the top of the file for a
  different project)

### 2. Drive it with small scripts, one action at a time
Each of these connects fresh via `chromium.connectOverCDP('http://127.0.0.1:9222')`, does one thing,
screenshots the result, and exits (~1–3s round trip — much faster and more reliable than the extension
bridge). Screenshot after every action before deciding the next one; don't chain blind multi-step
scripts — Flow's UI selectors drift and you need to see state to recover.

| Script | Purpose |
|---|---|
| `cdp_shot.js [out.png]` | Screenshot current canvas state |
| `cdp_click.js "<text>" [out.png]` | Click the first visible element containing that text |
| `cdp_click_coord.js <x> <y> [out.png]` | Click at pixel coords — use for icon-only buttons (download, trash, asset thumbnails) that have no matchable text |
| `cdp_type.js "<text>" [out.png]` | Clear and type into the composer box (tries contenteditable/.ProseMirror/textarea selectors) |
| `cdp_eval.js "<js expr>"` | Run arbitrary JS in the page, prints JSON — use to list `<img>` srcs, check for error banners, etc. |
| `cdp_zoom.js x y w h [out.png]` | Screenshot a cropped region (CSS-pixel coords, not the raw PNG's device-scaled pixels — divide your on-image estimate by the page's device scale factor, e.g. 1.25 for a 1600-wide viewport rendering at 2000px) — use to inspect small details (badges, papers) for stray lettering |
| `cdp_save_canvas.js <out.png> [idx]` | Extract the editor's `<canvas>` pixel buffer directly, bypassing Chrome's download manager (see below) |
| `cdp_downloads_check2.js` | List Chrome's download-manager entries (name/state) via `chrome://downloads` shadow DOM |
| `cdp_downloads_retry.js` | Click Retry on any deleted download entries (not reliable — see below) |

All scripts pick `ctx.pages().find(p => p.url().includes('labs.google'))`, so it's safe to have other
tabs open in the same profile.

### 3. Auth is manual, always
The persistent profile may not be logged into Google. **No agent may enter a Google password** —
if a script lands on `accounts.google.com`, stop and ask the human to sign in in the visible
(`headless: false`) window, then resume. Once signed in, the profile stays authenticated across future
launches (cookies persist in `C:\ai\.chrome_playwright_profile`).

### 4. Full workflow for one frame
1. `node persistent_launch.js` (background) → wait ~5s → `node cdp_shot.js` to confirm canvas loaded.
2. If on the marketing landing page, `node cdp_click.js "No thanks"` (decline cookies) then
   `node cdp_click.js "Create with Google Flow"` if needed to enter the app.
3. Attach references (Character entities + master frame) via the asset picker — this needs
   `cdp_shot.js` to locate icons, then `cdp_click_coord.js`. No dedicated script for this yet; it's
   click-by-coordinate against a fresh screenshot each time.
4. `cdp_type.js "<style anchor> <frame prompt>"` — never press Return, always click **Create** via
   `cdp_click.js "Create"`.
5. Poll with `cdp_shot.js` every ~10–15s until both takes render.
6. Score takes against the QA checklist in `featurette_storyboard_image_prompts.md` (HARD checks
   then SOFT checks) — this judgment call is the agent's, not scriptable.
7. Trash the loser (`cdp_click_coord.js` on its trash icon), rename keeper to the frame ID, download
   at 1K Original size (`cdp_click_coord.js` on the download icon → "1K Original size").
8. Move/rename the downloaded file into `storyboard-frames/<ID>.jpg`, tick the tracker in
   `featurette_storyboard_image_prompts.md`.

## Download-manager auto-deletion (found 2026-08-15, F18)
Clicking Flow's download-size menu (`cdp_click_coord.js` on the "1K Original size" / "2K Upscaled" row)
can silently fail: Chrome's download manager scans the blob download for malware and **deletes it**
before it reaches `Downloads\`, with no error surfaced to the page. Check `chrome://downloads` after any
download click, not just the Downloads folder — a "Deleted" state there confirms this happened.
`cdp_downloads_check2.js` reads the shadow-DOM download list (name/state); `cdp_downloads_retry.js`
clicks Retry on any deleted entries, but retry does not reliably work either.

**Don't fight the scanner** (it's a legitimate Chrome security feature, not a bug to bypass) — instead
avoid the download manager path entirely:
- If a download **did** land in `Downloads\` (check `chrome://downloads` for a non-"Deleted" state, or
  just look for a new file), just use it — no need to re-derive resolution: F01–F17 in this project are
  all **2752×1536**, and both "1K Original size" and "2K Upscaled" have produced exactly that resolution
  in practice, so don't assume a "2K" filename means a mismatched/wrong-tier asset — verify by comparing
  pixel dimensions (`python -c "from PIL import Image; print(Image.open('x.jpg').size)"`) against an
  already-approved frame instead of trusting the label.
- If nothing survives the scan, fall back to `cdp_save_canvas.js <out.png> [canvas_index]` — the Flow
  editor renders the main image on a `<canvas>` element (this is also *why* the claude-in-chrome
  extension hangs on this page, see top of this file), so `canvas.toDataURL()` extracts it directly with
  no Chrome download path involved at all. Caveat: this grabs the on-screen **display buffer**, which
  came out at 1325×739 in one test — lower-res than the real asset — so prefer a real download and only
  use this as a last resort, then upscale/regenerate rather than shipping a soft frame.

## Cross-agent handoff
This complements [`cli_image_quota_rules.md`](cli_image_quota_rules.md) §0b: `agy` runs the CLI
`generate_image` route until its quota is spent, then hands off to whichever assistant is driving the
browser (Claude Code or another agent, e.g. Kimi) for the Google Flow fallback — using this CDP method,
not the claude-in-chrome extension. Any assistant with shell + Node access can pick this up: the scripts
have no Claude-specific dependency, just `playwright` (already in `package.json`/`node_modules`).

**If `cdp_*.js` connection fails** (`ECONNREFUSED 127.0.0.1:9222`): `persistent_launch.js` isn't running
— relaunch it in the background first.
