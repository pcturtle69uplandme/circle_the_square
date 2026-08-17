const { chromium } = require('playwright');
const path = require('path');

async function main() {
  const userDataDir = 'C:\\Users\\konti\\AppData\\Local\\Google\\Chrome\\User Data';
  console.log('Launching Playwright with main user profile...');
  
  try {
    const context = await chromium.launchPersistentContext(userDataDir, {
      channel: 'chrome',
      headless: false,
      viewport: null,
      args: [
        '--disable-blink-features=AutomationControlled',
        '--start-maximized'
      ]
    });
    
    console.log('SUCCESS: Browser opened with primary user session!');
    const page = context.pages()[0] || await context.newPage();
    console.log('Navigating to Google Flow project...');
    await page.goto('https://labs.google/fx/tools/flow/project/c1c8417d-30c8-4e76-a58c-260fec3f7a40', { waitUntil: 'domcontentloaded' });
    console.log(`Page Title: ${await page.title()}`);
    console.log(`Current URL: ${page.url()}`);
    
    // Wait so the user can see it on screen
    await page.waitForTimeout(10000);
    await context.close();
  } catch (err) {
    console.error('Launch Error:', err.message);
  }
}

main().catch(console.error);
