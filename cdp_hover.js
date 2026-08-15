const { chromium } = require('playwright');
const path = require('path');
async function main() {
  const [x, y] = process.argv.slice(2, 4).map(Number);
  const outFile = process.argv[4] || 'cdp_hover.png';
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const ctx = browser.contexts()[0];
  const page = ctx.pages().find(p => p.url().includes('labs.google')) || ctx.pages()[0];
  await page.mouse.move(x, y);
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join('C:/AI/Circle the Square', outFile) });
  console.log('Saved hover screenshot to', outFile);
  await browser.close();
}
main().catch(e => { console.error(e.message); process.exit(1); });
