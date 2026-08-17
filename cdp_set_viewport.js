const { chromium } = require('playwright');
async function main() {
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const ctx = browser.contexts()[0];
  const page = ctx.pages().find(p => p.url().includes(process.env.FLOW_TAB || 'rive.app')) || ctx.pages()[0];
  await page.setViewportSize({ width: 1600, height: 1000 });
  await page.waitForTimeout(500);
  const dims = await page.evaluate(() => ({ vw: window.innerWidth, vh: window.innerHeight, dpr: window.devicePixelRatio }));
  console.log(JSON.stringify(dims));
  await browser.close();
}
main().catch(e => { console.error(e.message); process.exit(1); });
