const { chromium } = require('playwright');
const path = require('path');

// Rename the currently-open asset via the edit page title input.
// Usage: node cdp_rename.js "F19" [out.png]
async function main() {
  const newName = process.argv[2];
  const outFile = process.argv[3] || 'cdp_after_rename.png';
  if (!newName) { console.error('Usage: node cdp_rename.js "<name>" [out.png]'); process.exit(1); }

  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const ctx = browser.contexts()[0];
  const page = ctx.pages().find(p => p.url().includes(process.env.FLOW_TAB || 'labs.google')) || ctx.pages()[0];

  // The title lives in a plain <input type=text> at the top-left of the edit page.
  const input = page.locator('input[type="text"]').first();
  await input.waitFor({ state: 'visible', timeout: 10000 });
  await input.click();
  await page.keyboard.press('Control+A');
  await page.keyboard.type(newName, { delay: 20 });
  await page.keyboard.press('Enter');
  await page.waitForTimeout(1500);

  console.log('Title now:', await input.inputValue());
  await page.screenshot({ path: path.resolve(__dirname, outFile) });
  console.log('Saved screenshot to', outFile);
  await browser.close();
}

main().catch(err => { console.error('ERROR:', err.message); process.exit(1); });
