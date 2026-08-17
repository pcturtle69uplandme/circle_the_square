const { chromium } = require('playwright');
const path = require('path');

// Click the SMALLEST visible element whose trimmed innerText equals the given string
// (or equals "<icon>\n<label>"). Flow's composer menu re-renders and moves on every
// change, so cached pixel coordinates go stale constantly — matching on exact text and
// resolving the box at click time avoids that whole class of bug.
//
//   node cdp_click_exact.js "Veo 3.1 - Quality" [out.png]
//   node cdp_click_exact.js "10s" [out.png]
async function main() {
  const want = process.argv[2];
  const outFile = process.argv[3];
  if (!want) throw new Error('usage: cdp_click_exact.js "<exact text>" [out.png]');

  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const ctx = browser.contexts()[0];
  const page = ctx.pages().find(p => p.url().includes(process.env.FLOW_TAB || 'labs.google'))
    || ctx.pages()[0];

  const box = await page.evaluate((target) => {
    const hits = [];
    for (const el of document.querySelectorAll('*')) {
      const t = (el.innerText || '').trim();
      if (t !== target && t.split('\n').slice(1).join('\n') !== target) continue;
      const r = el.getBoundingClientRect();
      if (r.width > 0 && r.height > 0) {
        hits.push({ x: r.x + r.width / 2, y: r.y + r.height / 2, area: r.width * r.height });
      }
    }
    if (!hits.length) return null;
    hits.sort((a, b) => a.area - b.area);
    return hits[0];
  }, want);

  if (!box) throw new Error(`no visible element with exact text "${want}"`);
  await page.mouse.click(box.x, box.y);
  console.log(`clicked "${want}" at (${Math.round(box.x)}, ${Math.round(box.y)})`);
  await page.waitForTimeout(1200);
  if (outFile) {
    await page.screenshot({ path: path.resolve(__dirname, outFile) });
    console.log('saved', outFile);
  }
  await browser.close();
}

main().catch(err => { console.error('ERROR:', err.message); process.exit(1); });
