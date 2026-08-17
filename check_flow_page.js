const { chromium } = require('playwright');
const path = require('path');

async function checkState() {
  const userDataDir = path.resolve('C:\\ai\\.chrome_playwright_profile');
  const context = await chromium.launchPersistentContext(userDataDir, {
    channel: 'chrome',
    headless: false,
    viewport: { width: 1440, height: 900 },
    args: ['--disable-blink-features=AutomationControlled']
  });

  const page = context.pages()[0] || await context.newPage();
  await page.goto('https://labs.google/fx/tools/flow/project/c1c8417d-30c8-4e76-a58c-260fec3f7a40', { waitUntil: 'networkidle', timeout: 30000 }).catch(() => {});
  
  const title = await page.title();
  const url = page.url();
  console.log(`Current URL: ${url}`);
  console.log(`Current Title: ${title}`);
  
  // Take screenshot for visual status
  const screenshotPath = path.resolve('C:\\ai\\Circle the Square\\flow_state_check.png');
  await page.screenshot({ path: screenshotPath });
  console.log(`Screenshot saved to: ${screenshotPath}`);
  
  // Check if sign-in button is present
  const signinBtn = await page.$('text="Sign in"');
  if (signinBtn) {
    console.log('STATUS: Google Sign-In is required in this Chrome profile window.');
  } else {
    console.log('STATUS: Logged in / Project canvas active.');
  }
}

checkState().catch(console.error);
