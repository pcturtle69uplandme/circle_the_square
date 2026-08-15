const { chromium } = require('playwright');
const path = require('path');

async function main() {
  const outFile = process.argv[2] || 'cdp_shot.png';
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const ctx = browser.contexts()[0];
  const pages = ctx.pages();
  const page = pages.find(p => p.url().includes('labs.google')) || pages[0];
  console.log('Using page:', page.url());
  await page.screenshot({ path: path.join('C:\\AI\\Circle the Square', outFile) });
  console.log('Saved screenshot to', outFile);
  await browser.close();
}

main().catch(err => { console.error('ERROR:', err.message); process.exit(1); });
