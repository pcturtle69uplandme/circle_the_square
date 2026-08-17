const { chromium } = require('playwright');
const path = require('path');

async function main() {
  const userDataDir = path.resolve('C:\\ai\\.chrome_playwright_profile');
  console.log(`Launching persistent Chrome context at ${userDataDir}...`);
  
  const context = await chromium.launchPersistentContext(userDataDir, {
    channel: 'chrome',
    headless: false,
    viewport: { width: 1440, height: 900 },
    args: ['--disable-blink-features=AutomationControlled']
  });

  const page = context.pages().length > 0 ? context.pages()[0] : await context.newPage();
  console.log('Navigating to Google Flow project...');
  await page.goto('https://labs.google/fx/tools/flow/project/c1c8417d-30c8-4e76-a58c-260fec3f7a40', { waitUntil: 'domcontentloaded' });
  console.log(`Page loaded: ${await page.title()}`);
}

main().catch(console.error);
