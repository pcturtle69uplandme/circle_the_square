const { chromium } = require('playwright');
const path = require('path');

// Click at (x,y) CSS coords, select-all, type text, press Tab. Generic for canvas-rendered inputs.
// Usage: node cdp_click_type.js <x> <y> "<text>" [out.png]
async function main() {
  const x = Number(process.argv[2]);
  const y = Number(process.argv[3]);
  const text = process.argv[4];
  const outFile = process.argv[5] || 'scratch/cdp_click_type_out.png';

  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const ctx = browser.contexts()[0];
  const page = ctx.pages().find(p => p.url().includes(process.env.FLOW_TAB || 'rive.app')) || ctx.pages()[0];

  await page.mouse.click(x, y);
  await page.waitForTimeout(300);
  await page.keyboard.press('Control+A');
  await page.waitForTimeout(100);
  await page.keyboard.type(text, { delay: 20 });
  await page.keyboard.press('Tab');
  console.log(`Clicked (${x},${y}) and typed "${text}"`);
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join('C:\\AI\\Circle the Square', outFile) });
  console.log('Saved screenshot to', outFile);
  await browser.close();
}

main().catch(err => { console.error('ERROR:', err.message); process.exit(1); });
