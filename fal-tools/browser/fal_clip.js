// Drive ONE MiniMax H3 Max video generation on fal.ai end to end, then save the mp4.
//
//   node fal_up.js                       # start the browser (port 9333) once
//   node fal_clip.js probe               # dump the page's controls -- run this FIRST
//   node fal_clip.js <slug> [outDir]     # generate one clip
//   node fal_clip.js --list
//
// Mirrors higgsfield-tools/browser/run_shot.js, which is battle-tested, and reuses its
// hard-won guards:
//   - overlays are dismissed before every interaction (fal shows cookie/promo modals)
//   - the result is matched against OUR submission, never "something new appeared"
//   - retries and resumability live in run_clips.js, not here
//
// Selectors were calibrated against the live sandbox on 2026-09-04. If fal changes its
// UI, re-run `probe` and fix SEL -- a wrong selector wastes a free generation.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const CLIPS = require(process.env.FAL_CLIPS || './scene2_clips.js');
const REPO = path.resolve(__dirname, '..', '..');
const CDP = 'http://127.0.0.1:9333';

// --- Calibrated against the live sandbox, 2026-09-04 -----------------------------
// URL matters: the FREE allowance lives in the sandbox, not the model playground page
// (https://fal.ai/models/... 404s for this model anyway). The sandbox exposes exactly
// two image inputs, which is what the first/last keyframe pairs need.
const SANDBOX = 'https://fal.ai/sandbox?models=&op=video.image_to_video';
const MODEL = 'minimax/h3-max/image-to-video';

const SEL = {
  prompt: 'textarea[placeholder*="Describe what you want"]',
  // ⚠️ Do NOT target input[type=file] directly. The page's SEARCH-BY-IMAGE box is also
  // an accept="image/*" file input and sorts EARLIER in the DOM, so setInputFiles on it
  // silently runs a similarity search instead of attaching a reference -- the composer
  // stays empty and Run stays disabled. Go through the composer's own "Add image"
  // button and answer the file chooser it raises.
  addImage: 'button:has-text("Add image")',
  searchByImageClear: 'input[placeholder*="Searching by image"] ~ button, button[aria-label*="clear" i]',
  // Must be an exact-text match on a VISIBLE button. A loose :has-text("Run") also
  // matches hidden ancestors and transient nodes, which then time out on waitFor.
  run: 'button:visible',
  result: 'video',
};

// fal offers ONLY these durations. Anything else must snap (see scene2_clips.js).
const DURATIONS = [5, 10, 15];

// Measured, not published: c01 charged $0.20 for 10s while the free counter did not
// move, so image-to-video is metered at $0.02/sec. fal's public page quotes $0.08/sec
// for this model, so re-check if the balance starts dropping faster than this predicts.
const RATE_PER_SEC = 0.02;
// -------------------------------------------------------------------------------

const sleep = (ms) => new Promise(r => setTimeout(r, ms));

async function dismissOverlays(page) {
  // Radix poppers (the model picker, the duration menu) stay open and swallow clicks
  // aimed at anything underneath, so close any that are showing before doing anything.
  for (let i = 0; i < 3; i++) {
    const open = await page.evaluate(() =>
      !!document.querySelector('[data-radix-popper-content-wrapper]')).catch(() => false);
    if (!open) break;
    await page.keyboard.press('Escape');
    await page.waitForTimeout(500);
  }
  for (let i = 0; i < 6; i++) {
    const acted = await page.evaluate(() => {
      const vis = (e) => e && e.getBoundingClientRect().width > 0;
      const hit = Array.from(document.querySelectorAll('button'))
        .find(b => vis(b) && /accept|agree|got it|dismiss|close|continue/i.test(b.innerText || ''));
      if (hit) { hit.click(); return true; }
      return false;
    }).catch(() => false);
    if (!acted) return;
    await page.waitForTimeout(600);
  }
}

async function getPage(browser) {
  const ctx = browser.contexts()[0];
  return ctx.pages().find(p => p.url().includes('fal.ai')) || ctx.pages()[0];
}

// Dump everything interactive so SEL can be filled in from reality, not guesswork.
async function probe(page) {
  const out = await page.evaluate(() => {
    const box = (e) => { const r = e.getBoundingClientRect(); return { x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width) }; };
    const vis = (e) => e.getBoundingClientRect().width > 0;
    return {
      url: location.href,
      signedIn: !/sign in|log in/i.test(document.body.innerText.slice(0, 3000)),
      buttons: Array.from(document.querySelectorAll('button')).filter(vis)
        .map(b => ({ text: (b.innerText || '').trim().slice(0, 40), ...box(b) })).slice(0, 40),
      fileInputs: Array.from(document.querySelectorAll('input[type=file]'))
        .map((e, i) => ({ i, accept: e.accept, multiple: e.multiple, disabled: e.disabled })),
      textareas: Array.from(document.querySelectorAll('textarea, [contenteditable="true"]')).filter(vis)
        .map(e => ({ tag: e.tagName, placeholder: e.placeholder || e.getAttribute('aria-placeholder') || '', ...box(e) })),
      selects: Array.from(document.querySelectorAll('select, [role="combobox"]')).filter(vis)
        .map(e => ({ name: e.name || e.getAttribute('aria-label') || '', text: (e.innerText || '').slice(0, 40), ...box(e) })),
      // Free-tier counters usually render as plain text somewhere on the page.
      freeTierText: (document.body.innerText.match(/[^\n]*free[^\n]*/gi) || []).slice(0, 6),
    };
  });
  console.log(JSON.stringify(out, null, 2));
}

async function main() {
  const cmd = process.argv[2];
  if (cmd === '--list') return console.log(Object.keys(CLIPS).join('\n'));

  const browser = await chromium.connectOverCDP(CDP);
  const page = await getPage(browser);

  if (cmd === 'probe') { await probe(page); await browser.close(); return; }

  const clip = CLIPS[cmd];
  if (!clip) throw new Error(`unknown clip "${cmd}" -- try --list`);
  const outDir = process.argv.slice(3).find(a => !a.startsWith('--')) || path.join(REPO, 'scene2-clips');
  const dest = path.join(outDir, `${cmd}.mp4`);

  // chainFrom seeds this clip from the previous clip's real last frame, so the join
  // survives whatever the camera actually did (see scene2_clips.js). Falls back to the
  // adopted still if the frame has not been extracted yet.
  let start = clip.startImage;
  if (clip.chainFrom) {
    const chained = path.join('scene2-clips', 'lastframes', `${clip.chainFrom}_last.png`);
    if (fs.existsSync(path.join(REPO, chained))) {
      start = chained;
      console.log(`chaining from ${clip.chainFrom}'s last frame`);
    } else {
      console.log(`WARNING: ${clip.chainFrom} last frame missing, falling back to ${clip.startImage}`);
      console.log(`  run: node last_frame.js ${clip.chainFrom}`);
    }
  }
  const frames = [start, clip.endImage].filter(Boolean).map(f => path.join(REPO, f));
  for (const f of frames) if (!fs.existsSync(f)) throw new Error(`missing frame: ${f}`);
  console.log(`${cmd}: ${clip.seconds}s, ${frames.length} keyframe(s)`);
  console.log(`  ${clip.beats}`);

  if (process.argv.includes('--dry-run')) {
    console.log('--- prompt ---\n' + clip.prompt);
    await browser.close();
    return;
  }

  if (!page.url().includes('/sandbox')) {
    await page.goto(SANDBOX, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForTimeout(6000);
  }
  await dismissOverlays(page);

  // The sandbox starts with NO model selected ("Add models"), and Run with none picked
  // would either fail or fall through to whatever default fal chooses. Selection
  // persists in the session URL (?models=...), so this only has to be done once -- but
  // verify every time rather than assume.
  const modelBtn = await page.evaluate(() =>
    Array.from(document.querySelectorAll('button'))
      .map(b => (b.innerText || '').trim())
      .find(t => /^(Add models|\d+ models?)$/.test(t)) || null);
  if (!modelBtn || /Add models/.test(modelBtn)) {
    // The composer resets after every run and drops the model with it, so select it
    // rather than failing. The picker is a Radix popover: open it, click the row, and
    // close it -- leaving it open would swallow every later click.
    console.log('no model selected, picking minimax/h3-max/image-to-video...');
    await page.getByRole('button', { name: /Add models/i }).first().click();
    await page.waitForTimeout(2500);
    const row = page.getByText(MODEL, { exact: false }).first();
    await row.waitFor({ state: 'visible', timeout: 15000 });
    const bb = await row.boundingBox();
    if (!bb) throw new Error(`could not locate ${MODEL} in the model picker`);
    await page.mouse.click(bb.x + bb.width / 2, bb.y + bb.height / 2);
    await page.waitForTimeout(2000);
    await dismissOverlays(page);
    const now = await page.evaluate(() =>
      Array.from(document.querySelectorAll('button'))
        .map(b => (b.innerText || '').trim())
        .find(t => /^(Add models|\d+ models?)$/.test(t)) || null);
    if (!now || /Add models/.test(now)) throw new Error('model selection did not take');
    console.log(`model: ${now}`);
  } else {
    console.log(`model: ${modelBtn}`);
  }

  if (!DURATIONS.includes(clip.seconds)) {
    throw new Error(`clip ${cmd} asks for ${clip.seconds}s but fal only offers ${DURATIONS.join('/')}s`);
  }

  // Clear any leftover search-by-image state from a previous mistake, so the feed is
  // not filtered and the composer is the only thing holding our frames.
  await page.evaluate(() => {
    const si = document.querySelector('input[placeholder*="Searching by image" i]');
    if (si) {
      const clear = si.parentElement && si.parentElement.querySelector('button');
      if (clear) clear.click();
    }
  }).catch(() => {});
  await page.waitForTimeout(800);

  // Attach the start frame, and the end frame when this is a keyframe pair, through the
  // composer's own control. Each click raises a native file chooser which Playwright
  // answers directly -- a real picker dialog cannot be seen or clicked.
  for (let i = 0; i < frames.length; i++) {
    const chooser = page.waitForEvent('filechooser', { timeout: 20000 });
    await page.locator(SEL.addImage).first().click();
    await (await chooser).setFiles(frames[i]);
    await page.waitForTimeout(4000);
    await dismissOverlays(page);
  }

  const attached = await page.evaluate(() =>
    Array.from(document.querySelectorAll('img'))
      .filter(im => { const r = im.getBoundingClientRect(); return r.width > 20 && r.width < 200 && r.y > 520; }).length);
  console.log(`attached ${frames.length} frame(s), composer shows ${attached} thumbnail(s)`);

  await dismissOverlays(page);
  const box = page.locator(SEL.prompt).first();
  await box.click();
  await page.keyboard.press('Control+A');
  await page.keyboard.press('Backspace');
  await page.keyboard.type(clip.prompt, { delay: 3 });

  // Duration is a dropdown of 5s/10s/15s, not a free-text field. It persists between
  // runs, so it must be set explicitly every time or a 15s clip silently renders as 5s.
  await page.getByRole('button', { name: /^\d+s$/ }).first().click();
  await page.waitForTimeout(900);
  await page.getByRole('option', { name: `${clip.seconds}s` }).first().click()
    .catch(async () => { await page.getByText(`${clip.seconds}s`, { exact: true }).last().click(); });
  await page.waitForTimeout(700);
  const shown = await page.getByRole('button', { name: /^\d+s$/ }).first().innerText().catch(() => '?');
  if (shown.trim() !== `${clip.seconds}s`) {
    throw new Error(`duration did not take: wanted ${clip.seconds}s, control shows ${shown}`);
  }
  console.log(`duration set to ${shown.trim()}`);

  await dismissOverlays(page);

  // The sandbox page also renders every PREVIOUS generation, so "a video element
  // exists" proves nothing. Snapshot what is already on the page and accept only a src
  // that was not there before -- the same stale-result bug cost two mislabelled stills
  // on the Higgsfield side before it was guarded there.
  const balBefore = await page.evaluate(() => {
    const m = document.body.innerText.match(/\$(\d+\.\d+)/);
    return m ? parseFloat(m[1]) : null;
  }).catch(() => null);
  console.log(`estimated cost: $${(clip.seconds * RATE_PER_SEC).toFixed(2)} (${clip.seconds}s @ $${RATE_PER_SEC}/sec)` +
              (balBefore !== null ? ` | balance before: $${balBefore.toFixed(2)}` : ''));

  const before = new Set(await page.evaluate((sel) =>
    Array.from(document.querySelectorAll(sel)).map(v => v.currentSrc || v.src).filter(Boolean), SEL.result));
  console.log(`${before.size} existing video(s) on page, ignoring those`);

  const runBtn = page.locator(SEL.run).filter({ hasText: /^Run/ }).last();
  await runBtn.waitFor({ state: 'visible', timeout: 15000 });
  for (let i = 0; i < 20 && await runBtn.isDisabled(); i++) await page.waitForTimeout(1000);
  if (await runBtn.isDisabled()) {
    throw new Error('Run is still disabled -- the reference image or prompt did not register');
  }
  await runBtn.click();
  console.log('submitted, waiting for render...');

  // Video takes far longer than the image pipeline did; poll patiently.
  for (let i = 0; i < 240; i++) {
    await sleep(5000);
    const src = await page.evaluate(({ sel, seen }) => {
      const all = Array.from(document.querySelectorAll(sel))
        .map(v => v.currentSrc || v.src).filter(Boolean);
      return all.find(u => !seen.includes(u)) || null;
    }, { sel: SEL.result, seen: [...before] }).catch(() => null);
    if (src && /^https?:/.test(src)) {
      const b64 = await page.evaluate(async (u) => {
        const r = await fetch(u);
        if (!r.ok) throw new Error('HTTP ' + r.status);
        const bytes = new Uint8Array(await r.arrayBuffer());
        let s = ''; const CH = 0x8000;
        for (let k = 0; k < bytes.length; k += CH) s += String.fromCharCode.apply(null, bytes.subarray(k, k + CH));
        return btoa(s);
      }, src);
      fs.mkdirSync(path.dirname(dest), { recursive: true });
      fs.writeFileSync(dest, Buffer.from(b64, 'base64'));
      console.log(`SAVED ${dest} (${fs.statSync(dest).size} bytes)`);
      const balAfter = await page.evaluate(() => {
        const m = document.body.innerText.match(/\$(\d+\.\d+)/);
        return m ? parseFloat(m[1]) : null;
      }).catch(() => null);
      if (balBefore !== null && balAfter !== null) {
        console.log(`COST: $${(balBefore - balAfter).toFixed(2)} charged | balance now $${balAfter.toFixed(2)}`);
      }
      await browser.close();

      // AUDIO GATE. A saved file is not a good clip: MiniMax H3 is a Chinese model and
      // has rendered an entire take in Mandarin from an English-only prompt, and an
      // earlier H3 take is recorded in SCENE1_MINIMAX_TRACKER as having unusable audio.
      // Transcribe every render and exit non-zero if it is not English or does not say
      // the scripted lines, so run_clips.js will not mark it done and will re-roll it.
      const { spawnSync } = require('child_process');
      console.log('verifying audio...');
      const v = spawnSync('python', [path.join(REPO, 'verify_clip_audio.py'), dest],
                          { stdio: 'inherit' });
      if (v.status !== 0) {
        console.log('AUDIO CHECK FAILED -- clip saved but NOT accepted');
        process.exit(2);
      }
      return;
    }
    const err = await page.evaluate(() =>
      (document.body.innerText.match(/[^\n]*(error|failed|quota|limit reached|out of)[^\n]*/i) || [])[0] || null
    ).catch(() => null);
    if (err) console.log(`note: page says "${err.trim().slice(0, 120)}"`);
  }
  throw new Error('timed out waiting for the video to appear');
}

main().catch(e => { console.error('ERROR:', e.message); process.exit(1); });
