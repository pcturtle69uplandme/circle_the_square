// Price fal's image-to-video models WITHOUT generating anything.
//
//   node price_models.js [durationSeconds]
//
// The sandbox shows an "Est." figure once a model and duration are set, so every
// candidate can be priced for free. This exists because inferring a rate from a balance
// delta got it wrong by 6.5x once already -- read what the platform states.
//
// Never clicks Run.
const { chromium } = require('playwright');

const CANDIDATES = [
  'minimax/h3-max/image-to-video',
  'minimax/h3/image-to-video',
  'bytedance/seedance-2.5/image-to-video',
  'lightricks/ltx-2.5/image-to-video/pro',
  'lightricks/ltx-2.5/image-to-video/fast',
  'minimax/hailuo-2.3/pro/image-to-video',
  'minimax/hailuo-2.3-fast/standard/image-to-video',
  'minimax/hailuo-02/standard/image-to-video',
  'minimax/hailuo-02-fast/image-to-video',
  'alibaba/wan-3.0-prime/image-to-video',
  'alibaba/wan-3.0/image-to-video',
];

const sleep = ms => new Promise(r => setTimeout(r, ms));

async function clearModels(page) {
  // Remove every currently-selected model so estimates are per-model, not cumulative.
  for (let i = 0; i < 8; i++) {
    const removed = await page.evaluate(() => {
      const chips = Array.from(document.querySelectorAll('button'))
        .filter(b => /image-to-video|text-to-video/i.test(b.innerText || ''));
      for (const c of chips) {
        const x = Array.from(c.parentElement ? c.parentElement.querySelectorAll('button') : [])
          .find(b => b.getBoundingClientRect().width < 32);
        if (x) { x.click(); return true; }
      }
      return false;
    }).catch(() => false);
    if (!removed) return;
    await sleep(400);
  }
}

(async () => {
  const secs = Number(process.argv[2] || 10);
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9333');
  const page = browser.contexts()[0].pages().find(p => p.url().includes('fal.ai'));

  console.log(`pricing image-to-video models at ${secs}s (no generations run)\n`);
  console.log('model'.padEnd(48) + 'est'.padEnd(12) + '$/sec');

  const results = [];
  for (const model of CANDIDATES) {
    await page.keyboard.press('Escape').catch(() => {});
    await sleep(300);
    await clearModels(page);

    let est = null;
    try {
      await page.getByRole('button', { name: /Add models|models$/i }).first().click();
      await sleep(1800);
      const row = page.getByText(model, { exact: false }).first();
      if (await row.count()) {
        const bb = await row.boundingBox();
        if (bb) {
          await page.mouse.click(bb.x + bb.width / 2, bb.y + bb.height / 2);
          await sleep(1500);
        }
      }
      await page.keyboard.press('Escape');
      await sleep(800);
      est = await page.evaluate(() => {
        const m = document.body.innerText.match(/Est\.?\s*\$?([0-9]+\.[0-9]+)/);
        return m ? m[1] : null;
      });
    } catch { /* model may not be listed */ }

    const rate = est ? (Number(est) / secs).toFixed(4) : '-';
    console.log(model.padEnd(48) + String(est ? '$' + est : 'n/a').padEnd(12) + rate);
    results.push({ model, est, rate });
  }

  const priced = results.filter(r => r.est).sort((a, b) => Number(a.rate) - Number(b.rate));
  if (priced.length) {
    console.log('\ncheapest first:');
    for (const r of priced) console.log(`  $${r.rate}/sec  ${r.model}`);
  }
  await browser.close();
})().catch(e => { console.error('ERROR:', e.message); process.exit(1); });
