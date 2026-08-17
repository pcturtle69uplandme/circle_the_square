const { chromium } = require('playwright');
const path = require('path');

// Screenshot a cropped region for close inspection. Usage: node cdp_zoom.js x y width height [out.png]
async function main() {
  const [x, y, w, h] = process.argv.slice(2, 6).map(Number);
  const outFile = process.argv[6] || 'cdp_zoom.png';
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const ctx = browser.contexts()[0];
  const page = ctx.pages().find(p => p.url().includes(process.env.FLOW_TAB || 'labs.google')) || ctx.pages()[0];
  await page.screenshot({ path: path.resolve(__dirname, outFile), clip: { x, y, width: w, height: h } });
  console.log('Saved zoomed screenshot to', outFile);
  await browser.close();
}

main().catch(err => { console.error('ERROR:', err.message); process.exit(1); });
