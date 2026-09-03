# 🤝 HANDOVER — Scene 2 session, 2026-09-03

> Read this first if picking up Scene 2 work on a different machine (e.g. laptop).
> Everything referenced here is committed and pushed — see the commit this file
> shipped in for the exact snapshot.

## What happened this session

1. **Pivoted Scene 2 stills to Higgsfield's free tier.** The account `groovingmushroom1467`
   (a separate Google identity from the main paid `cheungtai37` account used for Scene 1)
   has **Nano Banana 2** on an **Unlimited/free** tier — confirmed hands-on, not the
   $23 "7-day Unlimited" upsell (that's a different, paid thing — see
   `SCENE2_VIDEO_PLAN.md` if that upsell reappears, don't buy it without asking the user).
   Nano Banana Pro (a different model) is **not** free — 2 credits/image on the shared
   balance. Only Nano Banana 2 has the free badge.

2. **Generated all 7 Scene 2 stills**, covering every beat and gag in the script (not
   just the 3 named in `scene_dialogue_audio_guide.md` — that guide undersells the
   scene, see `SCENE2_CONTINUITY_NOTES.md`'s "check script for gags" note):
   `06 → 07 → 07b → 07c → 08 → 08b → 09`. All saved locally in `scene2-stills/`
   (2752×1536 PNGs), all logged with the continuity reasoning behind each choice in
   `SCENE2_CONTINUITY_NOTES.md`.

3. **Found and fixed a real location bug**: the `jan_office` and `jan_office_corridor`
   location-ref folders each secretly contain images of a *different, unrelated* glass
   meeting-pod room mixed in alongside the real approved office (walnut desk,
   black-and-white triangle wall, per `LOCATION_PLATE_SHOT_LIST.md` L10). Full
   breakdown of which files are legit vs. mismatched is in `SCENE2_CONTINUITY_NOTES.md`'s
   "Data-quality gotcha" callout — read it before touching either folder again.

4. **Started building recurring background-extra references** (`character-refs/higgsfield/extra_01/`,
   `extra_02/`) because the crowd of generic office workers was a different set of
   people in nearly every generated still — confirmed by comparing them side by side.
   **`extra_03` and `extra_04` are not done yet.**

5. **Wrote a full pre-production video plan** (`SCENE2_VIDEO_PLAN.md`) before spending
   any credits on actual video: dialogue-length audit (Scene 1's ~2.75 words/sec, 15s
   ceiling method), which beats need splitting (07c and 09 both overflow — decided to
   split into 2 clips each rather than trim dialogue), and the `--start-image` chaining
   plan per beat. **No video has been generated yet** — this is all still planning.

## What's NOT done — pick up here

1. **Generate `extra_03` and `extra_04`** (recurring background extras) — same style
   as `extra_01`/`extra_02` (plain gray studio backdrop, fullbody, neutral pose). See
   `SCENE2_VIDEO_PLAN.md`'s crowd-consistency section for the plan these feed into.
2. **Retrofit `extra_01`-`04` into the 7 already-adopted stills' prompts** — right now
   the 7 stills predate the extras, so the crowd still isn't locked across them. Either
   accept that (video chaining will lock it going forward from here) or regenerate.
   Not decided — ask the user.
3. **Generate the missing "calmer half" stills** for 07c and 09's now-split clips
   (07c-1: Rick's question + Jan's opening justification; 09-1: crowd groans + Jan's
   calmer opening line) — the existing 07c/09 stills are the second/climactic half of
   each two-clip beat, not the first. See `SCENE2_VIDEO_PLAN.md`'s clip breakdown table.
4. **Actual video generation** hasn't started. MiniMax H3 on Higgsfield supports
   start-frame/end-frame keyframing (the "Frames" tab, not "References") — confirmed
   working in this session. **This costs real credits, not free** — get the user's
   go-ahead before generating, unlike the free stills (which per the user's explicit
   instruction this session should be auto-generated + QA'd, no per-shot confirmation
   needed).

## Account/login gotchas (don't re-discover these)

- The Higgsfield **CLI**'s `higgsfield auth login` cannot be switched off `cheungtai37`
  on this machine — tried three ways, all failed (see `project_higgsfield_account_switch_gotcha`
  memory). Don't retry it. Use the **web app** instead, in an isolated Playwright
  profile, with the user logging in manually.
- Browser automation in this project uses **local Playwright scripts** (`hf_*.js` in
  the repo root — not committed, scratch tooling, same as the pre-existing `fal_*.js`
  scripts), not the `claude-in-chrome` extension — that extension needs a claude.ai
  login this Google account doesn't have. `hf_launch.js <url>` opens a dedicated
  profile at `C:\ai\.chrome_playwright_profile_higgsfield_alt` with CDP on port 9223;
  `hf_screenshot.js`, `hf_click.js`, `hf_click_and_type.js`, `hf_upload_seq.js`, etc.
  drive it. **Recalibrate coordinates if the browser window gets resized** — this
  happened mid-session (1603×986 → 1412×906 viewport) and broke every hardcoded
  coordinate until caught; always sanity-check with `hf_viewport.js` if clicks start
  missing.
- The in-app **Download button didn't trigger a file** in this automated profile.
  Worked around it by reading image URLs off the page (`hf_get_img_url.js`) and
  fetching the direct CDN PNG URL with `curl` instead (strip `_min.webp` from the
  filename, use the `https://d8j0ntlcm91z4.cloudfront.net/user_.../hf_TIMESTAMP_UUID.png`
  pattern, not the `images.higgs.ai` proxy URL).

## Standing rules from this session (already saved to memory, listed here for visibility)

- Always check the full `.fountain` script for every gag/line when planning a shot
  list, not just a summary guide's named beats.
- Auto-generate (don't ask first) for **free** image generations; QA the result
  yourself to decide accept vs. re-roll. Paid generations (video) still need explicit
  confirmation before spending credits.
- Prefer local Playwright automation over the `claude-in-chrome` extension for this
  project specifically.
