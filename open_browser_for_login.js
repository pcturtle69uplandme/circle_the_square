const { chromium } = require('playwright');
const path = require('path');

async function main() {
  const userDataDir = path.resolve('C:\\ai\\.chrome_playwright_profile');
  console.log('Opening Chrome for one-time Google Flow login...');
  
  const context = await chromium.launchPersistentContext(userDataDir, {
    channel: 'chrome',
    headless: false,
    viewport: { width: 1440, height: 900 },
    args: ['--disable-blink-features=AutomationControlled']
  });

  const page = context.pages()[0] || await context.newPage();
  await page.goto('https://labs.google/fx/tools/flow/project/c1c8417d-30c8-4e76-a58c-260fec3f7a40');
  console.log('Google Flow window opened! Log in with your Google Pro account to save the session permanently.');
}

main().catch(console.error);
