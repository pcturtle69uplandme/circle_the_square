const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

async function run() {
  const userDataDir = path.resolve('C:\\ai\\.chrome_playwright_profile');
  console.log('Launching Chrome persistent context for Google Flow...');
  
  const context = await chromium.launchPersistentContext(userDataDir, {
    channel: 'chrome',
    headless: false,
    viewport: { width: 1440, height: 900 },
    args: ['--disable-blink-features=AutomationControlled']
  });

  const page = context.pages()[0] || await context.newPage();
  console.log('Navigating to project page...');
  await page.goto('https://labs.google/fx/tools/flow/project/c1c8417d-30c8-4e76-a58c-260fec3f7a40', { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(6000);

  // Take screenshot of current view
  const currentScreen = path.resolve('C:\\ai\\Circle the Square\\flow_current_view.png');
  await page.screenshot({ path: currentScreen });
  console.log(`Saved screenshot: ${currentScreen}`);

  // Query all buttons and inputs on the page
  const elements = await page.evaluate(() => {
    const inputs = Array.from(document.querySelectorAll('input, textarea, [contenteditable="true"], [role="textbox"]')).map(el => ({
      tag: el.tagName,
      role: el.getAttribute('role'),
      placeholder: el.getAttribute('placeholder'),
      ariaLabel: el.getAttribute('aria-label'),
      className: el.className,
      innerText: el.innerText.substring(0, 50)
    }));
    
    const buttons = Array.from(document.querySelectorAll('button')).map(b => ({
      text: b.innerText.trim(),
      ariaLabel: b.getAttribute('aria-label'),
      disabled: b.disabled
    })).filter(b => b.text.length > 0 || b.ariaLabel);

    return { inputs, buttons: buttons.slice(0, 30) };
  });

  console.log('Found Inputs:', JSON.stringify(elements.inputs, null, 2));
  console.log('Found Buttons (first 30):', JSON.stringify(elements.buttons, null, 2));
  
  await context.close();
}

run().catch(console.error);
