const { chromium } = require('playwright');
const path = require('path');

// Click at (x,y), catching a native file chooser dialog if one opens, and feed it filePath.
// Usage: node cdp_upload.js <x> <y> <filePath> [out.png]
async function main() {
  const x = Number(process.argv[2]);
  const y = Number(process.argv[3]);
  const filePath = process.argv[4];
  const outFile = process.argv[5] || 'scratch/cdp_upload_out.png';

  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const ctx = browser.contexts()[0];
  const page = ctx.pages().find(p => p.url().includes(process.env.FLOW_TAB || 'rive.app')) || ctx.pages()[0];

  const [chooser] = await Promise.all([
    page.waitForEvent('filechooser', { timeout: 5000 }).catch(() => null),
    page.mouse.click(x, y),
  ]);

  if (chooser) {
    await chooser.setFiles(filePath);
    console.log('File chooser handled, set file:', filePath);
  } else {
    console.log('No file chooser appeared within timeout.');
  }

  await page.waitForTimeout(2000);
  await page.screenshot({ path: path.join('C:\\AI\\Circle the Square', outFile) });
  console.log('Saved screenshot to', outFile);
  await browser.close();
}

main().catch(err => { console.error('ERROR:', err.message); process.exit(1); });
