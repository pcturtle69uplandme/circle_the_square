const { chromium } = require('playwright');

async function main() {
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const page = browser.contexts()[0].pages().find(p => p.url().includes('labs.google'));
  if (!page) { console.error('No page'); process.exit(1); }

  console.log('Clicking mode dropdown at (1011, 943)...');
  await page.mouse.click(1011, 943);
  await page.waitForTimeout(1000);

  // Take screenshot of the open dropdown menu
  await page.screenshot({ path: 'character-refs/stencils/flow_dropdown_open.png' });
  console.log('Saved flow_dropdown_open.png');

  // Find and click Image menuitem
  const imageItem = page.locator('text="Image", [role="menuitem"]:has-text("Image"), [role="option"]:has-text("Image")').first();
  if (await imageItem.isVisible()) {
    console.log('Clicking Image option...');
    await imageItem.click();
    await page.waitForTimeout(1000);
  }

  await page.screenshot({ path: 'character-refs/stencils/flow_after_image_select.png' });
  console.log('Saved flow_after_image_select.png');
  process.exit(0);
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
