const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

/**
 * Stage and fire one Frames-to-Video generation in Google Flow.
 *
 *   node gen_clip.js --prompt prompts/L5-A.txt --start FLASHBACK2047-OutRun-5.jpg \
 *                    --model "Veo 3.1 - Quality" [--end <file>] [--count x1] \
 *                    [--duration 10s] [--dry]
 *
 * --end defaults to --start, which is the whole point: start frame == end frame makes
 * the clip a closed loop the model cannot drift out of.
 * --dry stages everything but does not click Create (costs nothing).
 *
 * Every click resolves its target's box at click time by exact text. Flow's composer
 * menu re-renders and shifts on every single change, so cached pixel coordinates go
 * stale between one step and the next.
 */

const args = {};
process.argv.slice(2).forEach((a, i, arr) => {
  if (a.startsWith('--')) {
    const k = a.slice(2);
    args[k] = (arr[i + 1] && !arr[i + 1].startsWith('--')) ? arr[i + 1] : true;
  }
});

const need = (k) => { if (!args[k]) throw new Error(`missing --${k}`); return args[k]; };

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

async function click(page, target, { optional = false, wait = 1000 } = {}) {
  const b = await findBox(page, target);
  if (!b) {
    if (optional) { console.log(`  (skip "${target}" — not present)`); return false; }
    throw new Error(`element not found: "${target}"`);
  }
  await page.mouse.click(b.x, b.y);
  await page.waitForTimeout(wait);
  console.log(`  clicked "${target}"`);
  return true;
}

async function menuChip(page) {
  // The composer's settings chip, e.g. "Video\ncrop_16_9\nx2" or "🍌 Nano Banana 2\ncrop_16_9\nx2"
  return page.evaluate(() => {
    for (const el of document.querySelectorAll('button')) {
      const t = (el.innerText || '').trim();
      if (/crop_16_9|crop_9_16/.test(t) && /\bx[1-4]\b/.test(t)) {
        const r = el.getBoundingClientRect();
        if (r.width > 0) return { x: r.x + r.width / 2, y: r.y + r.height / 2, t };
      }
    }
    return null;
  });
}

async function pickFrame(page, slotLabel, filename) {
  await click(page, slotLabel, { wait: 1600 });
  const row = await findBox(page, filename);
  if (!row) throw new Error(`asset "${filename}" not in picker`);
  await page.mouse.click(row.x, row.y);
  await page.waitForTimeout(1200);
  // Some paths need the explicit confirm, others add on row click and close the modal.
  await click(page, 'Add to Prompt', { optional: true, wait: 1500 });
  console.log(`  ${slotLabel} <- ${filename}`);
}

async function main() {
  const promptFile = need('prompt');
  const startFile = need('start');
  const endFile = args.end || startFile;
  const model = need('model');
  const count = args.count || 'x1';
  const duration = args.duration;
  const dry = !!args.dry;

  const text = fs.readFileSync(path.resolve(promptFile), 'utf8').trim();
  if (text.includes('@')) throw new Error('prompt contains "@" — it hijacks the composer');

  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const ctx = browser.contexts()[0];
  const page = ctx.pages().find(p => p.url().includes(process.env.FLOW_TAB || 'labs.google')) || ctx.pages()[0];
  await page.bringToFront();

  console.log(`staging ${path.basename(promptFile)}  model=${model}  count=${count}` +
              (duration ? `  duration=${duration}` : '') + (dry ? '  [DRY]' : ''));

  // 1. open the settings menu and get into Video > Frames
  // The menu may already be open from a previous step; clicking the chip again would
  // close it. Flow also silently reverts the model between generations, so never assume.
  const menuOpen = () => page.evaluate(() => /crop_free\nFrames/.test(document.body.innerText));
  if (!await menuOpen()) {
    const chip = await menuChip(page);
    if (!chip) throw new Error('composer settings chip not found');
    await page.mouse.click(chip.x, chip.y);
    await page.waitForTimeout(1800);
  }
  if (!await menuOpen()) throw new Error('settings menu did not open');
  await click(page, 'Video');
  await click(page, 'Frames');

  // 2. model
  const cur = await page.evaluate(() => {
    const m = document.body.innerText.match(/\n(Omni Flash|Veo 3\.1 - Lite|Veo 3\.1 - Fast|Veo 3\.1 - Quality)\narrow_drop_down/);
    return m ? m[1] : null;
  });
  if (cur !== model) {
    await click(page, `${cur}\narrow_drop_down`.split('\n')[0] === cur ? cur + '\narrow_drop_down' : cur);
    await click(page, model);
  } else {
    console.log(`  model already ${model}`);
  }

  // 3. duration (only Omni Flash exposes this)
  if (duration) await click(page, duration, { optional: true });

  // 4. take count
  await click(page, count, { optional: true });

  const cost = await page.evaluate(() => {
    const m = document.body.innerText.match(/Generating will use\s*\n?\s*([0-9]+) credits/);
    return m ? m[1] : '?';
  });
  console.log(`  cost: ${cost} credits`);

  // 5. close the menu so it stops covering the composer
  await page.keyboard.press('Escape');
  await page.waitForTimeout(800);
  await click(page, 'close\nClose', { optional: true, wait: 600 });

  // 6. frames. Slots persist between generations, so clear any leftovers first —
  // otherwise the "Start"/"End" labels are absent and the picker can't be opened.
  const slotsFilled = await page.evaluate(() =>
    ![...document.querySelectorAll('*')].some(e =>
      ['Start', 'End'].includes((e.innerText || '').trim()) && e.getBoundingClientRect().width > 0));
  if (slotsFilled) {
    console.log('  clearing existing frames');
    await click(page, 'cancel', { optional: true, wait: 1200 });
    await click(page, 'cancel', { optional: true, wait: 1200 });
  }
  await pickFrame(page, 'Start', startFile);
  // --noend leaves the End slot empty: the chain architecture pins only the start, so the
  // model has no fixed target to decelerate into and no traffic layout to teleport toward.
  if (args.noend) console.log('  End left empty (--noend)');
  else await pickFrame(page, 'End', endFile);

  // 7. prompt
  const ce = await page.$('[contenteditable="true"]');
  const b = await ce.boundingBox();
  await page.mouse.click(b.x + b.width / 2, b.y + b.height / 2);
  await page.keyboard.press('Control+A');
  await page.keyboard.press('Backspace');
  for (let i = 0; i < text.length; i += 400) {
    await page.keyboard.insertText(text.slice(i, i + 400));
    await page.waitForTimeout(110);
  }
  await page.waitForTimeout(500);
  const got = await page.evaluate(() => document.querySelector('[contenteditable="true"]').innerText.trim().length);
  console.log(`  prompt: ${got}/${text.length} chars ${got === text.length ? 'OK' : 'MISMATCH'}`);
  if (got !== text.length) throw new Error('prompt did not land intact — refusing to generate');

  const tag = `${path.basename(promptFile, '.txt')}_${model.replace(/[^a-z0-9]+/gi, '')}`;
  await page.screenshot({ path: path.resolve(__dirname, `scratch/staged_${tag}.png`) });

  if (dry) {
    console.log('DRY RUN — staged but not generated');
  } else {
    await click(page, 'arrow_forward\nCreate'.split('\n')[1], { optional: true, wait: 500 })
      || await click(page, 'arrow_forward\nCreate');
    console.log(`GENERATING (${cost} credits)`);
    await page.waitForTimeout(4000);
    await page.screenshot({ path: path.resolve(__dirname, `scratch/fired_${tag}.png`) });
  }
  await browser.close();
}

main().catch(err => { console.error('ERROR:', err.message); process.exit(1); });
