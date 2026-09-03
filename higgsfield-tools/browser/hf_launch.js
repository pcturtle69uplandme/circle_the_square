// Persistent Chrome for Higgsfield, CDP on 9222 — same pattern as ../../persistent_launch.js
// (see .agents/rules/browser_automation_cdp.md). Blocks forever on purpose so the
// port stays open for follow-up `hf.js` calls. Run it in the background.
const { chromium } = require('playwright');

// Anchored to the repo root, not cwd. The old literal was a broken escape -- JS
// collapses backslash-a to a and backslash-dot to dot -- so it silently resolved to a
// RELATIVE 'ai.chrome_playwright_profile' and the profile landed in the repo root.
// That directory holds the logged-in free-tier Higgsfield account, so keep using it.
const path = require('path');
const USER_DATA_DIR = path.resolve(__dirname, '..', '..', 'ai.chrome_playwright_profile');
const HF_URL = process.argv[2] || 'https://higgsfield.ai/';

async function main() {
  console.log(`Launching persistent Chrome at ${USER_DATA_DIR} with CDP on 9222...`);
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
  await page.goto(HF_URL, { waitUntil: 'domcontentloaded', timeout: 60000 })
    .catch(e => console.log('goto error (continuing):', e.message));
  console.log('READY. Title:', await page.title());
  console.log('URL:', page.url());

  await new Promise(() => {});
}

main().catch(err => { console.error('FATAL:', err); process.exit(1); });
