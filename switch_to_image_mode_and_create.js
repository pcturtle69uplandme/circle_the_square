const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

async function main() {
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const page = browser.contexts()[0].pages().find(p => p.url().includes('labs.google'));
  if (!page) { console.error('No page'); process.exit(1); }

  console.log('Checking current mode toggle...');
  const modeBtn = page.locator('button:has-text("Video")').first();
  if (await modeBtn.isVisible()) {
    console.log('Switching from Video mode to Image mode...');
    await modeBtn.click();
    await page.waitForTimeout(500);

    const imageOption = page.locator('text="Image", [role="menuitem"]:has-text("Image"), button:has-text("Image")').first();
    if (await imageOption.isVisible()) {
      await imageOption.click();
      console.log('Selected Image mode!');
      await page.waitForTimeout(500);
    }
  }

  // Focus composer
  const composer = page.locator('div[contenteditable="true"]').first();
  await composer.waitFor({ state: 'visible', timeout: 10000 });
  await composer.click();

  // Find submit / Create button
  console.log('Looking for Create / arrow_forward button...');
  const createBtn = page.locator('button:has-text("Create"), button[aria-label="Create"], button:has-text("arrow_forward")').last();
  if (await createBtn.isVisible()) {
    console.log('Clicking Create button in Image mode...');
    await createBtn.click();
  } else {
    console.log('Pressing Enter...');
    await page.keyboard.press('Enter');
  }

  await page.waitForTimeout(2000);
  await page.screenshot({ path: 'character-refs/stencils/flow_image_mode_triggered.png' });
  console.log('Saved flow_image_mode_triggered.png');
  process.exit(0);
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
