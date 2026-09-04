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

const SHOTS = require('./scene2_shots.js');
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

// Each attached reference sits in a div.size-14 whose small (~24px) button is the
// remove X. It is opacity:0 until hover, but a direct .click() still fires it.
async function clearRefs(page) {
  for (let i = 0; i < 12; i++) {
    const left = await page.evaluate(() => {
      const box = Array.from(document.querySelectorAll('div.size-14'))
        .find(d => Array.from(d.querySelectorAll('button')).some(b => b.getBoundingClientRect().width < 32));
      if (!box) return 0;
      const x = Array.from(box.querySelectorAll('button')).find(b => b.getBoundingClientRect().width < 32);
      x.click();
      return 1;
    });
    if (!left) return i;
    await page.waitForTimeout(400);
  }
  return -1;
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

async function main() {
  const slug = process.argv[2];
  if (slug === '--list') return console.log(Object.keys(SHOTS).join('\n'));
  const shot = SHOTS[slug];
  if (!shot) throw new Error(`unknown shot "${slug}" -- try --list`);
  const outDir = process.argv[3] || path.join(REPO, 'scene2-stills');
  const dest = path.join(outDir, `${slug}.png`);

  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const ctx = browser.contexts()[0];
  const page = ctx.pages().find(p => p.url().includes('higgsfield')) || ctx.pages()[0];

  const before = await feedHead(page);

  const cleared = await clearRefs(page);
  console.log(`cleared ${cleared} reference(s)`);

  const files = shot.refs.map(r => path.join(REPO, r));
  for (const f of files) if (!fs.existsSync(f)) throw new Error(`missing reference: ${f}`);
  await page.locator('input[type=file]').first().setInputFiles(files);
  console.log(`attached ${files.length} reference(s)`);
  // Uploads must finish before the prompt is submitted or they are dropped.
  await page.waitForTimeout(4000 + 1500 * files.length);

  const composer = page.locator('[contenteditable="true"], textarea').first();
  await composer.click();
  await page.keyboard.press('Control+A');
  await page.keyboard.press('Backspace');
  await page.keyboard.type(shot.prompt, { delay: 4 });
  await page.waitForTimeout(700);

  const state = await ensureUnlimited(page);
  console.log(`generate button: ${JSON.stringify(state.label)} (free)`);

  await page.locator('button').filter({ hasText: /^Unlimited/ }).last().click();
  console.log('submitted, waiting for render...');

  for (let i = 0; i < 150; i++) {
    await sleep(6000);
    const head = await feedHead(page);
    if (head && head !== before) {
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
      console.log(`SAVED ${dest} (${fs.statSync(dest).size} bytes)`);
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
