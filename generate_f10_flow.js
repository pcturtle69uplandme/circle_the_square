const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

async function generateF10() {
  const userDataDir = path.resolve('C:\\ai\\.chrome_playwright_profile');
  console.log('Connecting to Google Flow via Playwright...');
  
  const context = await chromium.launchPersistentContext(userDataDir, {
    channel: 'chrome',
    headless: false,
    viewport: { width: 1440, height: 900 },
    args: ['--disable-blink-features=AutomationControlled']
  });

  const page = context.pages()[0] || await context.newPage();
  await page.goto('https://labs.google/fx/tools/flow/project/c1c8417d-30c8-4e76-a58c-260fec3f7a40', { waitUntil: 'networkidle', timeout: 30000 }).catch(() => {});
  
  console.log(`Page active: ${await page.title()}`);
  await page.waitForTimeout(3000);

  // Take screenshot of composer
  const composerScreen = path.resolve('C:\\ai\\Circle the Square\\flow_composer_status.png');
  await page.screenshot({ path: composerScreen });
  console.log(`Composer screenshot: ${composerScreen}`);
}

generateF10().catch(console.error);
