const { chromium } = require('playwright');

async function main() {
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const page = browser.contexts()[0].pages().find(p => p.url().includes('labs.google'));
  if (!page) { console.error('No page'); process.exit(1); }

  const dialogText = await page.evaluate(() => {
    const modals = Array.from(document.querySelectorAll('[role="dialog"], [role="modal"], div[class*="modal"], div[class*="dialog"]'))
      .map(m => m.innerText);
    return modals;
  });

  console.log('Dialogs found:', dialogText);

  // Click Agree button if present
  const agreeBtn = page.locator('button:has-text("Agree"), button:has-text("I agree"), button:has-text("Got it")').first();
  if (await agreeBtn.isVisible()) {
    console.log('Clicking Agree button...');
    await agreeBtn.click();
    await page.waitForTimeout(1000);
  }

  // Also close any media viewer modal by clicking Back / Done
  const doneBtn = page.locator('button:has-text("Done"), button:has-text("Back")').first();
  if (await doneBtn.isVisible()) {
    console.log('Clicking Done/Back...');
    await doneBtn.click();
    await page.waitForTimeout(1000);
  }

  await page.screenshot({ path: 'character-refs/stencils/flow_ready.png' });
  console.log('Saved flow_ready.png');
  process.exit(0);
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
