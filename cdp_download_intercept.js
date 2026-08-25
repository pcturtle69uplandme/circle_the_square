const { chromium } = require('playwright');

async function main() {
  const dlIconX = parseFloat(process.argv[2]);
  const dlIconY = parseFloat(process.argv[3]);
  const optX = parseFloat(process.argv[4]);
  const optY = parseFloat(process.argv[5]);
  const outPath = process.argv[6];

  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const ctx = browser.contexts()[0];
  const pages = ctx.pages();
  const page = pages.find(p => p.url().includes('labs.google')) || pages[0];
  console.log('Using page:', page.url());

  await page.mouse.click(dlIconX, dlIconY);
  await page.waitForTimeout(600);

  const downloadPromise = page.waitForEvent('download', { timeout: 15000 });
  await page.mouse.click(optX, optY);
  const download = await downloadPromise;
  console.log('Download event fired. Suggested filename:', download.suggestedFilename());
  console.log('URL:', download.url());
  await download.saveAs(outPath);
  console.log('Saved to', outPath);
  await browser.close();
}

main().catch(err => { console.error('ERROR:', err.message); process.exit(1); });
