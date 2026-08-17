const { chromium } = require('playwright');
const path = require('path');
async function main() {
  const text = process.argv[2];
  const outFile = process.argv[3] || 'cdp_typeraw.png';
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const ctx = browser.contexts()[0];
  const page = ctx.pages().find(p => p.url().includes(process.env.FLOW_TAB || 'labs.google')) || ctx.pages()[0];
  await page.keyboard.type(text, { delay: 30 });
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.resolve(__dirname, outFile) });
  console.log('Saved to', outFile);
  await browser.close();
}
main().catch(e => { console.error(e.message); process.exit(1); });
