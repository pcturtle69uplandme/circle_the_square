const { chromium } = require('playwright');
async function main() {
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const ctx = browser.contexts()[0];
  const page = ctx.pages().find(p => p.url().includes('chrome://downloads')) || await ctx.newPage();
  if (!page.url().includes('chrome://downloads')) await page.goto('chrome://downloads/');
  await page.waitForTimeout(500);
  const clicked = await page.evaluate(() => {
    const mgr = document.querySelector('downloads-manager');
    const list = mgr.shadowRoot.querySelector('#downloadsList');
    const items = Array.from(list.querySelectorAll('downloads-item'));
    let n = 0;
    for (const item of items) {
      const sr = item.shadowRoot;
      const retryBtn = Array.from(sr.querySelectorAll('cr-button, button')).find(b => b.textContent.trim() === 'Retry');
      if (retryBtn) { retryBtn.click(); n++; }
    }
    return n;
  });
  console.log('Clicked retry on', clicked, 'items');
  await page.waitForTimeout(2000);
  await page.close();
  await browser.close();
}
main().catch(e => { console.error(e.message); process.exit(1); });
