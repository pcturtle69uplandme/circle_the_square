const { chromium } = require('playwright');
const path = require('path');

// Types text into the Flow composer box (contenteditable/textarea), clearing it first.
// Usage: node cdp_type.js "the prompt text" [screenshot_out.png]
async function main() {
  const text = process.argv[2];
  const outFile = process.argv[3] || 'cdp_after_type.png';
  if (!text) { console.error('Usage: node cdp_type.js "<text>" [out.png]'); process.exit(1); }

  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const ctx = browser.contexts()[0];
  const page = ctx.pages().find(p => p.url().includes(process.env.FLOW_TAB || 'labs.google')) || ctx.pages()[0];
  console.log('Using page:', page.url());

  const selectors = [
    'div[contenteditable="true"]',
    'textarea',
    '[role="textbox"]',
    '.tiptap',
    '.ProseMirror',
    '[placeholder*="Describe"]',
    '[placeholder*="prompt"]'
  ];

  let composer = null;
  for (const sel of selectors) {
    const el = page.locator(sel).first();
    if (await el.count() > 0 && await el.isVisible().catch(() => false)) {
      composer = el;
      console.log('Found composer via selector:', sel);
      break;
    }
  }
  if (!composer) { console.error('Composer not found.'); process.exit(1); }

  await composer.click();
  await page.waitForTimeout(300);
  await page.keyboard.press('Control+A');
  await page.keyboard.press('Backspace');
  await page.waitForTimeout(200);
  await page.keyboard.type(text, { delay: 5 });
  console.log('Typed text into composer.');

  await page.waitForTimeout(500);
  await page.screenshot({ path: path.resolve(__dirname, outFile) });
  console.log('Saved screenshot to', outFile);
  await browser.close();
}

main().catch(err => { console.error('ERROR:', err.message); process.exit(1); });
