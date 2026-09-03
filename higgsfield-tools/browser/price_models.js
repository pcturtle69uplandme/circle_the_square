// Prices each image model by selecting it and reading the Generate button's credit
// figure. Selecting a model spends nothing -- only Generate does. Reopens the model
// picker between each pick because choosing one closes it.
const { chromium } = require('playwright');

const MODEL_CHIP = { x: 345, y: 939 };
const TARGETS = [
  'Higgsfield Soul 2.0',
  'Higgsfield Soul Cinema',
  'Seedream 5.0 lite',
  'Nano Banana Pro',
  'Nano Banana 2',
  'Higgsfield Soul',
  'Recraft V4 Styles',
  'Z-Image',
];

async function main() {
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const ctx = browser.contexts()[0];
  const page = ctx.pages().find(p => p.url().includes('higgsfield')) || ctx.pages()[0];

  const results = [];
  for (const name of TARGETS) {
    try {
      await page.mouse.click(MODEL_CHIP.x, MODEL_CHIP.y);
      await page.waitForTimeout(1200);

      const pt = await page.evaluate((n) => {
        const els = [...document.querySelectorAll('*')].filter(
          e => e.children.length === 0 && (e.innerText || '').trim() === n
        );
        for (const e of els) {
          const r = e.getBoundingClientRect();
          if (r.width > 0 && r.height > 0) {
            return { x: Math.round(r.x + r.width / 2), y: Math.round(r.y + r.height / 2) };
          }
        }
        return null;
      }, name);

      if (!pt) { results.push({ model: name, cost: 'not found in picker' }); continue; }

      await page.mouse.click(pt.x, pt.y);
      await page.waitForTimeout(1800);

      const info = await page.evaluate(() => {
        const btn = [...document.querySelectorAll('button')]
          .find(b => /generate/i.test((b.innerText || '')));
        const t = document.body.innerText;
        const i = t.indexOf('Describe the scene');
        return {
          gen: btn ? btn.innerText.replace(/\s+/g, ' ').trim() : '(no generate button)',
          bar: i < 0 ? '' : t.slice(i, i + 110).replace(/\n/g, ' | '),
          url: location.href,
        };
      });
      results.push({ model: name, cost: info.gen, bar: info.bar, url: info.url });
      console.log(`${name.padEnd(24)} -> ${info.gen}`);
    } catch (e) {
      results.push({ model: name, cost: 'ERROR ' + e.message });
      console.log(`${name.padEnd(24)} -> ERROR ${e.message}`);
    }
  }

  console.log('\nJSON:\n' + JSON.stringify(results, null, 1));
  await browser.close();
}

main().catch(e => { console.error('ERROR:', e.message); process.exit(1); });
