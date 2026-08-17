const { chromium } = require('playwright');
const path = require('path');

// Drag from (x1,y1) to (x2,y2) with intermediate steps, then screenshot.
// Usage: node cdp_drag.js x1 y1 x2 y2 [out.png]
async function main() {
  const [x1, y1, x2, y2] = process.argv.slice(2, 6).map(Number);
  const outFile = process.argv[6] || 'scratch/cdp_drag_out.png';

  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const ctx = browser.contexts()[0];
  const page = ctx.pages().find(p => p.url().includes(process.env.FLOW_TAB || 'rive.app')) || ctx.pages()[0];

  await page.mouse.move(x1, y1);
  await page.waitForTimeout(200);
  await page.mouse.down();
  await page.waitForTimeout(150);
  const steps = 12;
  for (let i = 1; i <= steps; i++) {
    const x = x1 + (x2 - x1) * (i / steps);
    const y = y1 + (y2 - y1) * (i / steps);
    await page.mouse.move(x, y);
    await page.waitForTimeout(60);
  }
  await page.waitForTimeout(150);
  await page.mouse.up();
  console.log(`Dragged (${x1},${y1}) -> (${x2},${y2})`);
  await page.waitForTimeout(1500);
  await page.screenshot({ path: path.join('C:\\AI\\Circle the Square', outFile) });
  console.log('Saved screenshot to', outFile);
  await browser.close();
}

main().catch(err => { console.error('ERROR:', err.message); process.exit(1); });
