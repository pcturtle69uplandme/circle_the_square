const { chromium } = require('playwright');

const USER_DATA_DIR = 'C:\\ai\\.chrome_playwright_profile';
const FLOW_URL = 'https://labs.google/fx/tools/flow/project/f2f0d2c9-ec16-420d-98af-b495197dad08/edit/581aaf73-456f-4089-bf86-51e7b9368d44';

async function main() {
  console.log(`Launching persistent Chrome context at ${USER_DATA_DIR} with CDP on 9222...`);
  const context = await chromium.launchPersistentContext(USER_DATA_DIR, {
    channel: 'chrome',
    headless: false,
    viewport: { width: 1600, height: 1000 },
    args: [
      '--disable-blink-features=AutomationControlled',
      '--start-maximized',
      '--remote-debugging-port=9222'
    ]
  });

  const page = context.pages()[0] || await context.newPage();
  console.log('Navigating to Flow project...');
  await page.goto(FLOW_URL, { waitUntil: 'domcontentloaded', timeout: 60000 }).catch(e => console.log('goto error (continuing):', e.message));
  console.log('READY. Title:', await page.title());
  console.log('URL:', page.url());

  // Keep process alive indefinitely so CDP stays open for follow-up scripts.
  await new Promise(() => {});
}

main().catch(err => {
  console.error('FATAL:', err);
  process.exit(1);
});
