const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

async function main() {
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const page = browser.contexts()[0].pages().find(p => p.url().includes('labs.google'));
  if (!page) { console.error('No page'); process.exit(1); }

  // 1. Get exact submit button and click via evaluate
  const result = await page.evaluate(() => {
    const btns = Array.from(document.querySelectorAll('button'));
    const createBtn = btns.find(b => b.innerText && (b.innerText.includes('arrow_forward') || b.innerText.trim().toLowerCase() === 'create'));
    if (createBtn) {
      createBtn.click();
      return { clicked: true, text: createBtn.innerText, disabled: createBtn.disabled };
    }
    return { clicked: false };
  });

  console.log('DOM click result:', JSON.stringify(result, null, 2));
  await page.waitForTimeout(3000);
  await page.screenshot({ path: 'character-refs/stencils/flow_after_dom_click.png' });
  console.log('Saved flow_after_dom_click.png');
  process.exit(0);
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
