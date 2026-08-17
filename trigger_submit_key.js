const { chromium } = require('playwright');
const fs = require('fs');

async function main() {
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const page = browser.contexts()[0].pages().find(p => p.url().includes('labs.google'));
  if (!page) { console.error('No page'); process.exit(1); }

  console.log('Focusing composer and triggering submit...');
  const composer = page.locator('div[contenteditable="true"]').first();
  await composer.click();
  await page.waitForTimeout(300);

  // Type a space and backspace to trigger input event
  await page.keyboard.type(' ');
  await page.keyboard.press('Backspace');
  await page.waitForTimeout(300);

  // Find the submit button inside the composer toolbar
  const submitBtn = page.locator('button:has-text("Create"), button[aria-label="Create"], button:has-text("arrow_forward")').last();
  if (await submitBtn.isVisible()) {
    console.log('Clicking visible submit button...');
    await submitBtn.click();
  } else {
    console.log('Pressing Enter key...');
    await page.keyboard.press('Enter');
  }

  await page.waitForTimeout(3000);
  await page.screenshot({ path: 'character-refs/stencils/flow_after_submit_attempt.png' });
  console.log('Saved flow_after_submit_attempt.png');
  process.exit(0);
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
