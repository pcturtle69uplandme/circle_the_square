const { chromium } = require('playwright');
async function main() {
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const ctx = browser.contexts()[0];
  const page = await ctx.newPage();
  await page.goto('chrome://downloads/');
  await page.waitForTimeout(1000);
  const items = await page.evaluate(() => {
    const mgr = document.querySelector('downloads-manager');
    const list = mgr.shadowRoot.querySelector('#downloadsList');
    return Array.from(list.querySelectorAll('downloads-item')).map(item => {
      const sr = item.shadowRoot;
      const q = (sel) => sr.querySelector(sel)?.textContent?.trim();
      return {
        fileLink: q('#file-link'),
        fileName: q('#file-name'),
        url: q('#url'),
        state: q('#state'),
        pauseOrResume: q('#pause-or-resume'),
        showInFolder: !!sr.querySelector('#show'),
        allText: sr.textContent.replace(/\s+/g,' ').trim().slice(0,300)
      };
    });
  });
  console.log(JSON.stringify(items, null, 2));
  await page.close();
  await browser.close();
}
main().catch(e => { console.error(e.message); process.exit(1); });
