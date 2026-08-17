const { chromium } = require('playwright');
const path = require('path');
async function main() {
  const outFile = process.argv[2] || 'cdp_clear.png';
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const ctx = browser.contexts()[0];
  const page = ctx.pages().find(p => p.url().includes(process.env.FLOW_TAB || 'labs.google')) || ctx.pages()[0];
  const rect = await page.evaluate(() => {
    const el = document.querySelector('[contenteditable="true"]');
    if (!el) return null;
    const r = el.getBoundingClientRect();
    return {x: r.x + r.width/2, y: r.y + r.height/2};
  });
  if (!rect) { console.error('composer not found'); process.exit(1); }
  await page.mouse.click(rect.x, rect.y);
  await page.keyboard.press('Control+A');
  await page.keyboard.press('Backspace');
  await page.waitForTimeout(300);
  await page.screenshot({ path: path.resolve(__dirname, outFile) });
  console.log('Cleared, saved to', outFile);
  await browser.close();
}
main().catch(e => { console.error(e.message); process.exit(1); });
