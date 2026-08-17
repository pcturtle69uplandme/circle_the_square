const { chromium } = require('playwright');
const path = require('path');

async function main() {
  const textToClick = process.argv[2];
  const outFile = process.argv[3] || 'cdp_after_click.png';
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const ctx = browser.contexts()[0];
  const pages = ctx.pages();
  const page = pages.find(p => p.url().includes(process.env.FLOW_TAB || 'labs.google')) || pages[0];
  console.log('Using page:', page.url());

  const el = page.getByText(textToClick, { exact: false }).first();
  await el.waitFor({ state: 'visible', timeout: 10000 });
  await el.click();
  console.log(`Clicked element with text: "${textToClick}"`);

  await page.waitForTimeout(3000);
  await page.screenshot({ path: path.resolve(__dirname, outFile) });
  console.log('Saved screenshot to', outFile, '| URL now:', page.url());
  await browser.close();
}

main().catch(err => { console.error('ERROR:', err.message); process.exit(1); });
