const { chromium } = require('playwright');
const { execFileSync } = require('child_process');
const fs = require('fs');
const path = require('path');

/**
 * Run one hop of the chain: upload a seed frame, generate from it, download the result,
 * and extract the next seed frame.
 *
 *   node chain_hop.js --seed chain/L5/hop01_end.png --prompt prompts/chain/L5-A.txt \
 *                     --out clips/outrun/L5_hop02.mp4 [--model "Veo 3.1 - Fast"]
 *
 * Only the START frame is ever pinned. Pinning the end made the model stop the world and
 * teleport traffic into position over the last two seconds (measured: last second at 7%
 * of peak speed); with start-only it holds 70% and the whole 8s is usable.
 */
const args = {};
process.argv.slice(2).forEach((a, i, arr) => {
  if (a.startsWith('--')) args[a.slice(2)] = (arr[i + 1] && !arr[i + 1].startsWith('--')) ? arr[i + 1] : true;
});
const need = k => { if (!args[k]) throw new Error(`missing --${k}`); return args[k]; };

const CDP = 'http://127.0.0.1:9222';
const sleep = ms => new Promise(r => setTimeout(r, ms));

async function getPage(browser) {
  const ctx = browser.contexts()[0];
  return ctx.pages().find(p => p.url().includes(process.env.FLOW_TAB || 'labs.google')) || ctx.pages()[0];
}

async function findBox(page, target) {
  return page.evaluate((t) => {
    const hits = [];
    for (const el of document.querySelectorAll('*')) {
      const txt = (el.innerText || '').trim();
      if (txt !== t && txt.split('\n').slice(1).join('\n') !== t) continue;
      const r = el.getBoundingClientRect();
      if (r.width > 0 && r.height > 0) hits.push({ x: r.x + r.width / 2, y: r.y + r.height / 2, a: r.width * r.height });
    }
    hits.sort((p, q) => p.a - q.a);
    return hits[0] || null;
  }, target);
}

async function click(page, target, { optional = false, wait = 1100 } = {}) {
  const b = await findBox(page, target);
  if (!b) { if (optional) return false; throw new Error(`not found: "${target}"`); }
  await page.mouse.click(b.x, b.y);
  await page.waitForTimeout(wait);
  return true;
}

async function main() {
  const seed = path.resolve(need('seed'));
  const promptFile = need('prompt');
  const out = path.resolve(need('out'));
  const model = args.model || 'Veo 3.1 - Fast';
  const text = fs.readFileSync(path.resolve(promptFile), 'utf8').trim();
  if (text.includes('@')) throw new Error('prompt contains "@"');
  if (!fs.existsSync(seed)) throw new Error(`seed not found: ${seed}`);

  const browser = await chromium.connectOverCDP(CDP);
  const page = await getPage(browser);
  await page.bringToFront();
  const seedName = path.basename(seed);
  console.log(`hop: seed=${seedName} model=${model}`);

  // 1. upload the seed frame
  const before = await page.$$('input[type="file"]');
  if (!before.length) throw new Error('no file input on page');
  await before[0].setInputFiles(seed);
  console.log('  uploaded seed, waiting for it to register...');
  await sleep(12000);

  // 2. settings: Video > Frames, model, x1
  const menuOpen = () => page.evaluate(() => /crop_free\nFrames/.test(document.body.innerText));
  if (!await menuOpen()) {
    const chip = await page.evaluate(() => {
      for (const el of document.querySelectorAll('button')) {
        const t = (el.innerText || '').trim();
        if (/crop_16_9|crop_9_16/.test(t) && /\bx[1-4]\b/.test(t)) {
          const r = el.getBoundingClientRect();
          if (r.width > 0) return { x: r.x + r.width / 2, y: r.y + r.height / 2 };
        }
      }
      return null;
    });
    if (!chip) throw new Error('settings chip not found');
    await page.mouse.click(chip.x, chip.y);
    await sleep(1800);
  }
  await click(page, 'Video');
  await click(page, 'Frames');
  const cur = await page.evaluate(() => {
    const m = document.body.innerText.match(/\n(Omni Flash|Veo 3\.1 - Lite|Veo 3\.1 - Fast|Veo 3\.1 - Quality)\narrow_drop_down/);
    return m ? m[1] : null;
  });
  if (cur !== model) { await click(page, `${cur}\narrow_drop_down`); await click(page, model); }
  await click(page, args.count || 'x1', { optional: true });
  const cost = await page.evaluate(() => {
    const m = document.body.innerText.match(/Generating will use\s*\n?\s*([0-9]+) credits/);
    return m ? m[1] : '?';
  });
  console.log(`  cost: ${cost} credits`);
  await page.keyboard.press('Escape');
  await sleep(800);

  // 3. clear any leftover frames, then set Start only
  const filled = await page.evaluate(() =>
    ![...document.querySelectorAll('*')].some(e =>
      ['Start', 'End'].includes((e.innerText || '').trim()) && e.getBoundingClientRect().width > 0));
  if (filled) { await click(page, 'cancel', { optional: true, wait: 1200 }); await click(page, 'cancel', { optional: true, wait: 1200 }); }

  await click(page, 'Start', { wait: 1600 });
  const row = await findBox(page, seedName);
  if (!row) throw new Error(`seed "${seedName}" not visible in picker — upload may still be processing`);
  await page.mouse.click(row.x, row.y);
  await sleep(1300);
  await click(page, 'Add to Prompt', { optional: true, wait: 1500 });
  console.log(`  Start <- ${seedName}  (End left empty)`);

  // 4. prompt
  const ce = await page.$('[contenteditable="true"]');
  const bb = await ce.boundingBox();
  await page.mouse.click(bb.x + bb.width / 2, bb.y + bb.height / 2);
  await page.keyboard.press('Control+A');
  await page.keyboard.press('Backspace');
  for (let i = 0; i < text.length; i += 400) { await page.keyboard.insertText(text.slice(i, i + 400)); await sleep(110); }
  await sleep(500);
  const got = await page.evaluate(() => document.querySelector('[contenteditable="true"]').innerText.trim().length);
  if (got !== text.length) throw new Error(`prompt ${got}/${text.length} — refusing to generate`);

  if (args.dry) { console.log('DRY — staged only'); await browser.close(); return; }

  // 5. fire and wait
  const known = await page.evaluate(() => [...document.querySelectorAll('video')].map(v => v.src || v.currentSrc));
  await click(page, 'arrow_forward\nCreate'.split('\n')[1]);
  console.log(`  GENERATING (${cost} credits)`);
  let src = null;
  for (let i = 0; i < 60; i++) {
    await sleep(15000);
    const st = await page.evaluate((k) => {
      const pct = (document.body.innerText.match(/\b(\d{1,3})%/) || [])[1] || null;
      const fresh = [...document.querySelectorAll('video')].map(v => v.src || v.currentSrc).filter(s => s && !k.includes(s));
      return { pct, fresh };
    }, known);
    if (st.pct) { console.log(`    ${st.pct}%`); continue; }
    if (st.fresh.length) { src = st.fresh[0]; break; }
  }
  if (!src) throw new Error('generation did not produce a new video in time');

  // 6. download + next seed
  const ctx = browser.contexts()[0];
  const resp = await ctx.request.get(src, { headers: { referer: page.url() } });
  if (!resp.ok()) throw new Error(`download failed ${resp.status()}`);
  fs.mkdirSync(path.dirname(out), { recursive: true });
  fs.writeFileSync(out, await resp.body());
  console.log(`  wrote ${out}  ${(fs.statSync(out).size / 1048576).toFixed(2)} MB`);

  const nextSeed = out.replace(/\.mp4$/i, '_end.png');
  execFileSync('ffmpeg', ['-v', 'error', '-y', '-sseof', '-0.05', '-i', out, '-vframes', '1', '-q:v', '1', nextSeed]);
  console.log(`  next seed: ${nextSeed}`);
  await browser.close();
}

main().catch(err => { console.error('ERROR:', err.message); process.exit(1); });
