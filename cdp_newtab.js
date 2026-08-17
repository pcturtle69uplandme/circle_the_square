const { chromium } = require('playwright');
const path = require('path');

// Open an extra tab in the already-running persistent Chrome (port 9222) without
// disturbing whatever the existing labs.google tab is doing.
//   node cdp_newtab.js [url] [out.png]
async function main() {
  const url = process.argv[2] || 'https://labs.google/fx/tools/flow';
  const outFile = process.argv[3] || 'cdp_newtab.png';
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const ctx = browser.contexts()[0];
  const page = await ctx.newPage();
  await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 })
    .catch(e => console.log('goto error (continuing):', e.message));
  await page.waitForTimeout(4000);
  await page.screenshot({ path: path.resolve(__dirname, outFile) });
  console.log('Opened tab:', page.url());
  console.log('Tabs now:', ctx.pages().map(p => p.url()).join('\n           '));
  console.log('Saved screenshot to', outFile);
  await browser.close();
}

main().catch(err => { console.error('ERROR:', err.message); process.exit(1); });
