const { chromium } = require('playwright');
const path = require('path');

async function run() {
  const userDataDir = path.resolve('C:\\ai\\.chrome_playwright_profile');
  console.log('Launching browser to enter project canvas...');
  
  const context = await chromium.launchPersistentContext(userDataDir, {
    channel: 'chrome',
    headless: false,
    viewport: { width: 1440, height: 900 },
    args: ['--disable-blink-features=AutomationControlled']
  });

  const page = context.pages()[0] || await context.newPage();
  console.log('Navigating to Google Flow project...');
  await page.goto('https://labs.google/fx/tools/flow/project/c1c8417d-30c8-4e76-a58c-260fec3f7a40', { waitUntil: 'domcontentloaded', timeout: 30000 }).catch(() => {});
  await page.waitForTimeout(5000);

  // Look for entry button if on landing page
  const entryBtn = await page.$('button:has-text("Create with Google Flow"), button:has-text("Try in Google Flow"), a:has-text("Try in Google Flow")');
  if (entryBtn) {
    console.log('Found entry CTA button, clicking...');
    await entryBtn.click();
    await page.waitForTimeout(6000);
  }

  console.log(`Live Canvas URL: ${page.url()}`);
  console.log(`Live Canvas Title: ${await page.title()}`);
  
  const shot = path.resolve('C:\\ai\\Circle the Square\\project_canvas_live.png');
  await page.screenshot({ path: shot });
  console.log(`Screenshot saved to: ${shot}`);
  
  await context.close();
}

run().catch(console.error);
