const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

async function main() {
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const page = browser.contexts()[0].pages().find(p => p.url().includes('labs.google'));
  if (!page) { console.error('No page'); process.exit(1); }

  // Check the Create button coordinates and state
  const btnInfo = await page.evaluate(() => {
    const btns = Array.from(document.querySelectorAll('button'));
    const createBtn = btns.find(b => b.innerText && b.innerText.trim().toLowerCase() === 'create');
    if (!createBtn) return null;
    const r = createBtn.getBoundingClientRect();
    return {
      text: createBtn.innerText,
      disabled: createBtn.disabled,
      rect: { x: r.x, y: r.y, w: r.width, h: r.height }
    };
  });

  console.log('Create button info:', JSON.stringify(btnInfo, null, 2));
  if (btnInfo && !btnInfo.disabled) {
    console.log('Clicking Create button at exact coordinates...');
    await page.mouse.click(btnInfo.rect.x + btnInfo.rect.w / 2, btnInfo.rect.y + btnInfo.rect.h / 2);
    await page.waitForTimeout(2000);
  }

  await page.screenshot({ path: 'character-refs/stencils/flow_after_create_click.png' });
  console.log('Saved flow_after_create_click.png');
  process.exit(0);
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
