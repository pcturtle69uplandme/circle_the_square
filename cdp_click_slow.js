const { chromium } = require('playwright');
const path = require('path');

// Slower, more deliberate click: move -> pause -> down -> pause -> up -> pause -> screenshot.
// Some canvas-rendered UIs (Rive editor) don't register Playwright's instantaneous click().
async function main() {
  const x = Number(process.argv[2]);
  const y = Number(process.argv[3]);
  const outFile = process.argv[4] || 'scratch/cdp_click_slow_out.png';

  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const ctx = browser.contexts()[0];
  const page = ctx.pages().find(p => p.url().includes(process.env.FLOW_TAB || 'rive.app')) || ctx.pages()[0];

  await page.mouse.move(x, y);
  await page.waitForTimeout(400);
  await page.mouse.down();
  await page.waitForTimeout(150);
  await page.mouse.up();
  console.log(`Slow-clicked at (${x}, ${y})`);
  await page.waitForTimeout(2000);
  await page.screenshot({ path: path.join('C:\\AI\\Circle the Square', outFile) });
  console.log('Saved screenshot to', outFile);
  await browser.close();
}

main().catch(err => { console.error('ERROR:', err.message); process.exit(1); });
