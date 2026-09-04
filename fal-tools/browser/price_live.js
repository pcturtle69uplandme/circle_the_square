// Price models against a REAL loaded composer, without generating anything.
//
//   node price_live.js [durationSeconds] [model,model,...]
//
// The sandbox only computes its "Est." figure once an image, a prompt, a duration and a
// model are all set, which is why an empty-composer probe returned nothing. This loads a
// genuine start frame and prompt once, then swaps the model and reads the estimate.
//
// NEVER clicks Run. Reading the platform's own figure is the point: inferring fal's rate
// from a balance delta got it wrong by 6.5x once already.
const { chromium } = require('playwright');
const path = require('path');

const REPO = path.resolve(__dirname, '..', '..');
const FRAME = path.join(REPO, 'scene2-stills', 'shot06_corridor_gossip.png');
const PROMPT = 'Two office workers talk quietly in a corridor. Natural daylight, photoreal, static camera.';

const DEFAULT_MODELS = [
  'minimax/h3-max/image-to-video',
  'minimax/h3/image-to-video',
  'wan/v2.6/image-to-video',
  'alibaba/wan-3.0/image-to-video',
  'fal-ai/ovi/image-to-video',
  'bytedance/seedance-2.0/fast/image-to-video',
  'google/gemini-omni-flash/image-to-video',
];

const sleep = ms => new Promise(r => setTimeout(r, ms));

async function escape(page) { await page.keyboard.press('Escape').catch(() => {}); await sleep(400); }

// Remove every selected model so each estimate is for one model alone.
async function clearModels(page) {
  for (let i = 0; i < 10; i++) {
    const gone = await page.evaluate(() => {
      const chip = Array.from(document.querySelectorAll('div,span'))
        .find(e => /image-to-video/i.test(e.textContent || '') &&
                   e.getBoundingClientRect().width > 0 && e.getBoundingClientRect().y > 600);
      if (!chip) return false;
      const x = Array.from((chip.closest('div') || chip).querySelectorAll('button'))
        .find(b => b.getBoundingClientRect().width < 32);
      if (!x) return false;
      x.click();
      return true;
    }).catch(() => false);
    if (!gone) return;
    await sleep(400);
  }
}

async function readEst(page) {
  return page.evaluate(() => {
    const m = document.body.innerText.match(/Est\.?\s*\$?\s*([0-9]+\.[0-9]+)/);
    return m ? m[1] : null;
  });
}

(async () => {
  const secs = Number(process.argv[2] || 10);
  const models = (process.argv[3] || '').split(',').filter(Boolean);
  const list = models.length ? models : DEFAULT_MODELS;

  const browser = await chromium.connectOverCDP('http://127.0.0.1:9333');
  const page = browser.contexts()[0].pages().find(p => p.url().includes('fal.ai'));
  await escape(page);

  // Load a real frame and prompt once, so the estimate can be computed at all.
  const already = await page.evaluate(() => Array.from(document.querySelectorAll('img'))
    .filter(i => { const r = i.getBoundingClientRect(); return r.width > 20 && r.width < 200 && r.y > 500 && r.y < 780; }).length);
  if (!already) {
    const chooser = page.waitForEvent('filechooser', { timeout: 20000 });
    await page.getByRole('button', { name: /Add image/i }).first().click();
    await (await chooser).setFiles(FRAME);
    await sleep(4000);
  }
  const box = page.locator('textarea[placeholder*="Describe what you want"]').first();
  if (!(await box.inputValue()).trim()) {
    await box.click();
    await page.keyboard.type(PROMPT, { delay: 2 });
    await sleep(600);
  }
  // Duration.
  await page.getByRole('button', { name: /^\d+s$/ }).first().click();
  await sleep(900);
  await page.getByText(`${secs}s`, { exact: true }).last().click().catch(() => {});
  await escape(page);

  console.log(`estimates at ${secs}s, real frame + prompt loaded, nothing generated\n`);
  console.log('model'.padEnd(46) + 'est'.padEnd(12) + '$/sec');

  const rows = [];
  for (const model of list) {
    await escape(page);
    await clearModels(page);
    await sleep(500);
    let est = null;
    try {
      await page.getByRole('button', { name: /Add models|models$/i }).first().click();
      await sleep(2000);
      const row = page.getByText(model, { exact: false }).first();
      if (await row.count()) {
        const bb = await row.boundingBox();
        if (bb) { await page.mouse.click(bb.x + bb.width / 2, bb.y + bb.height / 2); await sleep(1800); }
      }
      await escape(page);
      est = await readEst(page);
    } catch { /* not listed */ }
    const rate = est ? (Number(est) / secs).toFixed(4) : '-';
    console.log(model.padEnd(46) + String(est ? '$' + est : 'n/a').padEnd(12) + rate);
    rows.push({ model, est, rate });
  }

  const priced = rows.filter(r => r.est).sort((a, b) => Number(a.rate) - Number(b.rate));
  if (priced.length) {
    console.log('\ncheapest first  (Scene 2 = 135s):');
    for (const r of priced) {
      console.log(`  $${r.rate}/sec  ->  $${(Number(r.rate) * 135).toFixed(2)}  ${r.model}`);
    }
  }
  await browser.close();
})().catch(e => { console.error('ERROR:', e.message); process.exit(1); });
