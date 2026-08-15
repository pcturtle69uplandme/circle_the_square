const { chromium } = require('playwright');
async function main() {
  const key = process.argv[2] || 'Escape';
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const ctx = browser.contexts()[0];
  const page = ctx.pages().find(p => p.url().includes('labs.google')) || ctx.pages()[0];
  await page.keyboard.press(key);
  console.log('Pressed', key);
  await browser.close();
}
main().catch(e => { console.error(e.message); process.exit(1); });
