const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

async function main() {
  console.log('Connecting to Chrome on port 9222...');
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const ctx = browser.contexts()[0];
  const page = ctx.pages().find(p => p.url().includes('labs.google'));
  if (!page) {
    console.error('Google Flow page not found.');
    process.exit(1);
  }

  await page.bringToFront();

  // Click Create button
  const createBtn = page.locator('button:has-text("Create")').first();
  if (await createBtn.count() > 0 && await createBtn.isVisible()) {
    console.log('Clicking Create button...');
    await createBtn.click();
  } else {
    console.log('Create button not found, trying Enter in composer...');
  }

  // Wait for generation to start and complete
  console.log('Waiting for generation in Flow...');
  await page.waitForTimeout(5000);

  // Poll for 45 seconds to let generation finish
  for (let i = 0; i < 9; i++) {
    await page.waitForTimeout(5000);
    console.log(`Polling generation... ${(i + 1) * 5}s`);
    await page.screenshot({ path: path.join('C:\\AI\\Circle the Square', `flow_gen_progress_${i}.png`) });
  }

  console.log('Generation polling complete. Screenshot captured.');
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
