const { chromium } = require('playwright');

async function main() {
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const page = browser.contexts()[0].pages().find(p => p.url().includes('labs.google'));
  if (!page) { console.error('No page'); process.exit(1); }

  const allButtons = await page.evaluate(() => {
    return Array.from(document.querySelectorAll('button, [role="button"]')).map(b => ({
      tag: b.tagName,
      text: b.innerText.replace(/\n/g, ' ').trim(),
      aria: b.getAttribute('aria-label') || '',
      className: b.className,
      rect: b.getBoundingClientRect()
    }));
  });

  console.log('All buttons on page:', JSON.stringify(allButtons, null, 2));
  process.exit(0);
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
