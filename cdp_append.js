const { chromium } = require('playwright');
const path = require('path');
async function main() {
  const text = process.argv[2];
  const outFile = process.argv[3] || 'cdp_append.png';
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const ctx = browser.contexts()[0];
  const page = ctx.pages().find(p => p.url().includes('labs.google')) || ctx.pages()[0];
  const rect = await page.evaluate(() => {
    const el = document.querySelector('[contenteditable="true"]');
    const r = el.getBoundingClientRect();
    return {x: r.x + r.width/2, y: r.y + r.height - 5};
  });
  await page.mouse.click(rect.x, rect.y);
  await page.keyboard.press('Control+End');
  await page.waitForTimeout(200);
  await page.keyboard.type(text, { delay: 25 });
  await page.waitForTimeout(300);
  await page.screenshot({ path: path.join('C:/AI/Circle the Square', outFile) });
  console.log('Appended, saved to', outFile);
  await browser.close();
}
main().catch(e => { console.error(e.message); process.exit(1); });
