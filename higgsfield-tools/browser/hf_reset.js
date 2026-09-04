// Reset the Higgsfield composer by replacing the tab.
//
//   node hf_reset.js [url]
//
// Repeated failed uploads leave the composer wedged with empty placeholder reference
// tiles: no <img> inside them and no remove X, so the hover-and-click clear in
// run_shot.js can never drain them and every later shot fails at "could not clear N
// attached reference(s)". Reloading is not enough -- attached references survive a
// reload (and the Unlimited toggle silently flips off). Opening a fresh tab and
// closing the old one gives a genuinely clean composer.
const { chromium } = require('playwright');

const URL = process.argv[2] || 'https://higgsfield.ai/ai/image?model=nano-banana-2';

(async () => {
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const ctx = browser.contexts()[0];
  const old = ctx.pages().filter(p => p.url().includes('higgsfield'));

  const page = await ctx.newPage();
  await page.goto(URL, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await page.waitForTimeout(6000);

  for (const p of old) await p.close().catch(() => {});

  const tiles = await page.evaluate(() => document.querySelectorAll('div.size-14').length);
  console.log(`composer reset -- ${tiles} reference tile(s) remaining`);
  await browser.close();
  if (tiles > 0) process.exit(1);
})().catch(e => { console.error('ERROR:', e.message); process.exit(1); });
