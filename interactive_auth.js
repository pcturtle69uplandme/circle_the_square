const { chromium } = require('playwright');
const path = require('path');

async function main() {
  const userDataDir = path.resolve('C:\\ai\\.chrome_playwright_profile');
  console.log('Opening persistent Chrome window on your screen for Google authentication...');
  
  const context = await chromium.launchPersistentContext(userDataDir, {
    channel: 'chrome',
    headless: false,
    viewport: { width: 1440, height: 900 },
    args: ['--disable-blink-features=AutomationControlled', '--start-maximized']
  });

  const page = context.pages()[0] || await context.newPage();
  console.log('Navigating to Google Flow project...');
  await page.goto('https://labs.google/fx/tools/flow/project/c1c8417d-30c8-4e76-a58c-260fec3f7a40');

  console.log('========================================================================');
  console.log('BROWSER WINDOW OPEN: Please log in with your Google account on screen.');
  console.log('Once you are inside the Flow project canvas, let me know in the chat!');
  console.log('========================================================================');

  // Keep checking URL every 5 seconds and logging status
  while (true) {
    await page.waitForTimeout(5000);
    const url = page.url();
    const title = await page.title().catch(() => '');
    console.log(`[Heartbeat] URL: ${url.substring(0, 80)}... | Title: ${title}`);
    if (url.includes('/flow/project/') && !url.includes('signin') && !url.includes('accounts.google')) {
      console.log('>>> AUTHENTICATION DETECTED! You are now inside the project canvas. <<<');
    }
  }
}

main().catch(console.error);
