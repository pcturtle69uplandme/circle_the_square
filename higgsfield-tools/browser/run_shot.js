// Drive one Higgsfield still end-to-end: clear refs -> attach refs -> prompt ->
// generate -> wait -> save full-res PNG. Reads shot definitions from scene2_shots.js.
//
//   node run_shot.js <slug> [outDir]
//   node run_shot.js --list
//
// Safety: this ALWAYS verifies the Unlimited (free) toggle is on and that the
// Generate button is not quoting a credit price before it submits. Reloading the
// page silently turns Unlimited back off while KEEPING the attached references,
// so the check has to happen per generation, not once per session.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

// Which shot definitions to drive. Defaults to Scene 2's stills; set HF_SHOTS to
// point at another module (e.g. ./location_shots.js for the Scene 3 canteen plates).
const SHOTS = require(process.env.HF_SHOTS || './scene2_shots.js');
const REPO = path.resolve(__dirname, '..', '..');
const CDN = 'd8j0ntlcm91z4.cloudfront.net';

const sleep = (ms) => new Promise(r => setTimeout(r, ms));

// Feed thumbnails are proxy URLs with the CloudFront original in a url= param.
const toFullRes = (u) => {
  const m = u.match(/[?&]url=([^&]+)/);
  if (m) u = decodeURIComponent(m[1]);
  return u.replace(/_min\.webp$/, '.png').replace(/\.webp$/, '.png');
};

const feedHead = (page) => page.evaluate((cdn) => {
  const i = Array.from(document.querySelectorAll('img'))
    .map(e => e.currentSrc || e.src || '')
    .find(u => u.includes(cdn) && /user_/.test(u));
  return i || null;
}, CDN);

// Attached references are div.size-14 tiles that CONTAIN AN <img>; the same class is
// also used by the trailing "add reference" button, which has no image and no remove
// control. Matching on the class alone made the old clear loop spin forever on that
// button and report "could not clear N attached reference(s)", which then failed every
// subsequent shot -- so match on the image, not the class.
//
// A loaded reference exposes its ~24px remove X without needing hover. A tile with no
// image that is NOT the add button is a wedged upload placeholder; those cannot be
// removed from the DOM at all and need hf_reset.js to replace the tab.
const refTiles = (page) => page.locator('div.size-14').filter({ has: page.locator('img') });

async function clearRefs(page) {
  let removed = 0;
  for (let i = 0; i < 20; i++) {
    const n = await refTiles(page).count();
    if (n === 0) return removed;
    const tile = refTiles(page).first();
    await tile.hover({ timeout: 4000 }).catch(() => {});
    const clicked = await tile.evaluate((d) => {
      const x = Array.from(d.querySelectorAll('button'))
        .find(b => b.getBoundingClientRect().width < 40);
      if (!x) return false;
      x.click();
      return true;
    }).catch(() => false);
    if (!clicked) { await page.waitForTimeout(1200); continue; }
    removed++;
    await page.waitForTimeout(500);
  }
  const left = await refTiles(page).count();
  if (left) throw new Error(`could not clear ${left} attached reference(s)`);
  return removed;
}

// Higgsfield drops full-screen interstitials over the composer without warning: a
// promo ("NEW FEATURE ... Claim Free Generation") and the media-upload consent gate.
// Their overlay is a fixed inset-0 div at z-1000, so every click lands on it instead
// of the control underneath and Playwright just retries until it times out. Clear any
// of them before touching the page. Promos get CLOSED, never clicked through.
async function dismissOverlays(page) {
  for (let i = 0; i < 8; i++) {
    const acted = await page.evaluate(() => {
      const vis = (e) => e && e.getBoundingClientRect().width > 0;
      // Our own generated reference images, so accepting the upload terms is fine.
      const agree = Array.from(document.querySelectorAll('button'))
        .find(b => /I agree, continue/i.test(b.innerText || '') && vis(b));
      if (agree) { agree.click(); return 'agree'; }
      const overlay = document.querySelector('div.fixed.inset-0[data-state="open"]');
      if (!overlay) return null;
      const dialog = document.querySelector('[role="dialog"]');
      const close = dialog && Array.from(dialog.querySelectorAll('button'))
        .find(b => /close/i.test(b.getAttribute('aria-label') || '') ||
                   (vis(b) && b.getBoundingClientRect().width < 48 && !b.innerText.trim()));
      if (close) { close.click(); return 'close'; }
      return 'stuck';
    });
    if (!acted) return i;
    if (acted === 'stuck') await page.keyboard.press('Escape');
    await page.waitForTimeout(800);
  }
  throw new Error('could not clear a blocking overlay after 8 attempts');
}

async function ensureUnlimited(page) {
  const on = await page.evaluate(() => {
    const sw = document.querySelector('[role=switch]');
    if (!sw) return null;
    if (sw.getAttribute('aria-checked') !== 'true') sw.click();
    return true;
  });
  await page.waitForTimeout(900);
  const label = await page.evaluate(() =>
    (Array.from(document.querySelectorAll('button')).find(b => /Unlimited|Generate/.test(b.innerText)) || {}).innerText || '');
  // "Generate\n2.5\n2" means it would charge credits; "Unlimited" means free.
  if (/\d/.test(label)) throw new Error(`refusing to generate: button quotes a credit cost (${JSON.stringify(label)}) -- Unlimited is off`);
  return { on, label: label.trim() };
}

// Generated assets are named hf_YYYYMMDD_HHMMSS_<uuid>.png, in UTC. That timestamp is
// the only trustworthy way to tell OUR render from someone else's: "the feed head
// changed" is not enough, because a job submitted by an earlier failed attempt can
// render late and become the head. That exact bug saved Shot 07c-2's image as Shot
// 07b-2 (byte-identical files) before this guard existed.
function assetTime(url) {
  const m = url.match(/hf_(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})(\d{2})_/);
  if (!m) return null;
  const [, y, mo, d, h, mi, sec] = m;
  return Date.UTC(+y, +mo - 1, +d, +h, +mi, +sec);
}

// Don't submit while anything is still rendering, or a foreign result could land in
// our wait window and be mistaken for ours.
async function waitForIdle(page, maxMs = 15 * 60 * 1000) {
  const deadline = Date.now() + maxMs;
  while (Date.now() < deadline) {
    const busy = await page.evaluate(() =>
      /(Processing|Generating)/.test(document.body.innerText.slice(0, 6000)));
    if (!busy) return;
    await sleep(5000);
  }
  console.log('warning: queue still busy after wait, proceeding anyway');
}

async function saveUrl(page, head, dest) {
  const url = toFullRes(head);
  const b64 = await page.evaluate(async (u) => {
    const r = await fetch(u);
    if (!r.ok) throw new Error('HTTP ' + r.status);
    const bytes = new Uint8Array(await r.arrayBuffer());
    let s = ''; const CH = 0x8000;
    for (let k = 0; k < bytes.length; k += CH) s += String.fromCharCode.apply(null, bytes.subarray(k, k + CH));
    return btoa(s);
  }, url);
  fs.mkdirSync(path.dirname(dest), { recursive: true });
  fs.writeFileSync(dest, Buffer.from(b64, 'base64'));
  console.log(`SAVED ${dest} (${fs.statSync(dest).size} bytes) from ${url}`);
}

async function main() {
  const slug = process.argv[2];
  if (slug === '--list') return console.log(Object.keys(SHOTS).join('\n'));
  const shot = SHOTS[slug];
  if (!shot) throw new Error(`unknown shot "${slug}" -- try --list`);
  // Ignore flags when looking for the optional output directory.
  const outDir = process.argv.slice(3).find(a => !a.startsWith('--')) || path.join(REPO, 'scene2-stills');
  const dest = path.join(outDir, `${slug}.png`);

  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const ctx = browser.contexts()[0];
  const page = ctx.pages().find(p => p.url().includes('higgsfield')) || ctx.pages()[0];

  let before = await feedHead(page);

  // --adopt-head: a submitted generation that finished while nothing was watching
  // (an interrupted batch, a killed browser) is already sitting at the head of the
  // feed. Save that instead of paying the render time again.
  if (process.argv.includes('--adopt-head')) {
    await saveUrl(page, before, dest);
    await browser.close();
    return;
  }

  await dismissOverlays(page);
  const cleared = await clearRefs(page);
  console.log(`cleared ${cleared} reference(s)`);

  const files = shot.refs.map(r => path.join(REPO, r));
  for (const f of files) if (!fs.existsSync(f)) throw new Error(`missing reference: ${f}`);
  if (!files.length) console.log('no references (text-to-image)');
  await dismissOverlays(page);
  if (files.length) await attachRefs(page, files);
  await runPrompt(page, shot, dest, before, browser);
}

async function attachRefs(page, files) {
  // With no references attached the composer exposes one multi-file input; as soon as
  // any reference exists it swaps to a single-file "add another" input. Handle both,
  // so a partially-cleared composer degrades to slower uploads instead of failing.
  const multi = page.locator('input[type=file][multiple]:not([disabled])');
  if (await multi.count()) {
    await multi.first().setInputFiles(files);
  } else {
    for (const f of files) {
      const one = page.locator('input[type=file]:not([disabled])').first();
      await one.waitFor({ state: 'attached', timeout: 20000 });
      await one.setInputFiles([f]);
      await page.waitForTimeout(2500);
      await dismissOverlays(page);
    }
  }
  console.log(`attached ${files.length} reference(s)`);
  // Uploads must finish before the prompt is submitted or they are dropped.
  await page.waitForTimeout(4000 + 1500 * files.length);
}

async function runPrompt(page, shot, dest, before, browser) {
  await dismissOverlays(page);
  const composer = page.locator('[contenteditable="true"], textarea').first();
  await composer.click();
  await page.keyboard.press('Control+A');
  await page.keyboard.press('Backspace');
  await page.keyboard.type(shot.prompt, { delay: 4 });
  await page.waitForTimeout(700);

  await dismissOverlays(page);
  const state = await ensureUnlimited(page);
  console.log(`generate button: ${JSON.stringify(state.label)} (free)`);

  await waitForIdle(page);
  const submittedAt = Date.now();
  await page.locator('button').filter({ hasText: /^Unlimited/ }).last().click();
  console.log('submitted, waiting for render...');

  for (let i = 0; i < 150; i++) {
    await sleep(6000);
    const head = await feedHead(page);
    if (head && head !== before) {
      const t = assetTime(toFullRes(head));
      // 120s of slack absorbs clock skew between this machine and the CDN's naming.
      if (t !== null && t < submittedAt - 120000) {
        console.log(`ignoring stale feed head from ${new Date(t).toISOString()} (predates submit)`);
        before = head;
        continue;
      }
      await saveUrl(page, head, dest);
      await browser.close();
      return;
    }
    if (await page.evaluate(() => /went wrong|failed/i.test(document.body.innerText.slice(0, 4000)))) {
      console.log('note: an error banner is visible on the feed -- still waiting');
    }
  }
  throw new Error('timed out waiting for the generation to appear');
}

main().catch(e => { console.error('ERROR:', e.message); process.exit(1); });
