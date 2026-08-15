const { chromium } = require('playwright');
const path = require('path');

// Clicks at pixel coordinates (from a screenshot taken via cdp_shot.js) — use for icon-only
// buttons (download icon, trash icon, asset thumbnails) where text-based click.js won't match.
// Usage: node cdp_click_coord.js <x> <y> [screenshot_out.png]
async function main() {
  const x = Number(process.argv[2]);
  const y = Number(process.argv[3]);
  const outFile = process.argv[4] || 'cdp_after_click_coord.png';
  if (Number.isNaN(x) || Number.isNaN(y)) { console.error('Usage: node cdp_click_coord.js <x> <y> [out.png]'); process.exit(1); }

  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const ctx = browser.contexts()[0];
  const page = ctx.pages().find(p => p.url().includes('labs.google')) || ctx.pages()[0];

  await page.mouse.click(x, y);
  console.log(`Clicked at (${x}, ${y})`);
  await page.waitForTimeout(1000);
  await page.screenshot({ path: path.join('C:\\AI\\Circle the Square', outFile) });
  console.log('Saved screenshot to', outFile);
  await browser.close();
}

main().catch(err => { console.error('ERROR:', err.message); process.exit(1); });
