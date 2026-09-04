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
// ⚠️ SELECTORS ARE NOT YET CALIBRATED. Everything in SEL below is a first guess from
// fal.ai's documented UI. Run `probe` against the live page while signed in and correct
// SEL before generating anything -- a wrong selector wastes one of only five free
// generations per day. probe prints every candidate control it can find.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const CLIPS = require(process.env.FAL_CLIPS || './scene2_clips.js');
const REPO = path.resolve(__dirname, '..', '..');
const CDP = 'http://127.0.0.1:9333';

// --- Calibrate these with `probe`. ---------------------------------------------
const SEL = {
  prompt: 'textarea, [contenteditable="true"]',
  // fal exposes separate uploads for the first and last frame in image-to-video.
  imageInputs: 'input[type=file]',
  duration: 'input[name="duration"], select[name="duration"]',
  resolution: 'select[name="resolution"], [role="combobox"]',
  run: 'button:has-text("Run"), button:has-text("Generate")',
  result: 'video source, video',
};
// -------------------------------------------------------------------------------

const sleep = (ms) => new Promise(r => setTimeout(r, ms));

async function dismissOverlays(page) {
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

  const frames = [clip.startImage, clip.endImage].filter(Boolean).map(f => path.join(REPO, f));
  for (const f of frames) if (!fs.existsSync(f)) throw new Error(`missing frame: ${f}`);
  console.log(`${cmd}: ${clip.seconds}s, ${frames.length} keyframe(s)`);
  console.log(`  ${clip.beats}`);

  if (process.argv.includes('--dry-run')) {
    console.log('--- prompt ---\n' + clip.prompt);
    await browser.close();
    return;
  }

  await dismissOverlays(page);

  // Attach the start frame, and the end frame when this is a keyframe pair.
  const inputs = page.locator(SEL.imageInputs);
  if (await inputs.count() < frames.length) {
    throw new Error(`page exposes ${await inputs.count()} file input(s) but this clip needs ${frames.length} -- run \`probe\` and fix SEL.imageInputs`);
  }
  for (let i = 0; i < frames.length; i++) await inputs.nth(i).setInputFiles(frames[i]);
  await page.waitForTimeout(3000 + 2000 * frames.length);

  await dismissOverlays(page);
  const box = page.locator(SEL.prompt).first();
  await box.click();
  await page.keyboard.press('Control+A');
  await page.keyboard.press('Backspace');
  await page.keyboard.type(clip.prompt, { delay: 3 });

  // Duration is billed per second, so never leave it at a default.
  const dur = page.locator(SEL.duration).first();
  if (await dur.count()) await dur.fill(String(clip.seconds)).catch(() => {});

  await dismissOverlays(page);
  await page.locator(SEL.run).first().click();
  console.log('submitted, waiting for render...');

  // Video takes far longer than the image pipeline did; poll patiently.
  for (let i = 0; i < 240; i++) {
    await sleep(5000);
    const src = await page.evaluate((sel) => {
      const v = document.querySelector(sel);
      return v ? (v.currentSrc || v.src || null) : null;
    }, SEL.result).catch(() => null);
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
      await browser.close();
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
