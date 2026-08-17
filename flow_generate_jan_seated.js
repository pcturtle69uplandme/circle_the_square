const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

async function main() {
  console.log('Connecting to Chrome on port 9222...');
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const ctx = browser.contexts()[0];
  const page = ctx.pages().find(p => p.url().includes('labs.google'));
  if (!page) {
    console.error('Google Flow page not found in active contexts.');
    process.exit(1);
  }

  await page.bringToFront();
  console.log('Using Flow page:', page.url());

  // Focus composer
  const selectors = [
    'div[contenteditable="true"]',
    'textarea',
    '[role="textbox"]',
    '.tiptap',
    '.ProseMirror'
  ];

  let composer = null;
  for (const sel of selectors) {
    const el = page.locator(sel).first();
    if (await el.count() > 0 && await el.isVisible().catch(() => false)) {
      composer = el;
      console.log('Found composer:', sel);
      break;
    }
  }

  if (!composer) {
    console.error('Composer not found.');
    process.exit(1);
  }

  const promptText = "Medium shot. @Jan Peach (52-year-old heavy-set CEO with receding grey comb-over, soft build, wearing a sharp grey suit jacket buttoned over white shirt, burnt-orange PRISM lanyard) is seated comfortably in his black executive office chair behind his walnut desk in his office, looking up from his desk toward the door with a composed, slightly weary expression. Stylised British sitcom comic art, clean bold line art, flat muted colour palette, cel-shaded. Absolutely NO text, NO speech bubbles, NO captions.";

  await composer.click();
  await page.waitForTimeout(300);
  await page.keyboard.press('Control+A');
  await page.keyboard.press('Backspace');
  await page.waitForTimeout(200);

  // Type prompt
  console.log('Typing prompt into composer...');
  await page.keyboard.type(promptText, { delay: 10 });
  await page.waitForTimeout(1000);

  await page.screenshot({ path: path.join('C:\\AI\\Circle the Square', 'flow_typed_jan.png') });
  console.log('Saved flow_typed_jan.png');

  // Look for Create / Generate button
  console.log('Looking for Create button...');
  const btnSelectors = [
    'button:has-text("Create")',
    'button:has-text("Generate")',
    'button[aria-label*="Create"]',
    'button[aria-label*="Generate"]',
    'button:has(svg)'
  ];

  for (const bsel of btnSelectors) {
    const btn = page.locator(bsel).first();
    if (await btn.count() > 0 && await btn.isVisible().catch(() => false)) {
      console.log('Found button:', bsel, await btn.innerText().catch(() => ''));
    }
  }
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
