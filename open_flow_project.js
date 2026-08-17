const { chromium } = require('playwright');

async function main() {
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const page = browser.contexts()[0].pages().find(p => p.url().includes('labs.google'));
  if (!page) { console.error('No page'); process.exit(1); }

  console.log('Navigating into Circle the Square animation project...');
  const projectLink = page.locator('text="Circle the Square animation"').first();
  if (await projectLink.isVisible()) {
    await projectLink.click();
    await page.waitForTimeout(3000);
  } else {
    // Navigate directly to the project URL
    await page.goto('https://labs.google/fx/tools/flow/project/f2f0d2c9-ec16-420d-98af-b495197dad08');
    await page.waitForTimeout(4000);
  }

  console.log('Current URL:', page.url());
  await page.screenshot({ path: 'character-refs/stencils/flow_inside_project.png' });
  console.log('Saved flow_inside_project.png');
  process.exit(0);
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
