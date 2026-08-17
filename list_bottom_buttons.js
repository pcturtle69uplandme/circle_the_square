const { chromium } = require('playwright');

async function main() {
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const page = browser.contexts()[0].pages().find(p => p.url().includes('labs.google'));
  if (!page) { console.error('No page'); process.exit(1); }

  const bottomButtons = await page.evaluate(() => {
    const btns = Array.from(document.querySelectorAll('button, [role="button"]'));
    return btns.map((b, i) => {
      const r = b.getBoundingClientRect();
      return {
        i,
        tag: b.tagName,
        text: b.innerText.replace(/\n/g, ' ').trim(),
        aria: b.getAttribute('aria-label') || '',
        rect: { x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height) }
      };
    }).filter(b => b.rect.y > 600 && b.rect.w > 0);
  });

  console.log('Bottom buttons found:', JSON.stringify(bottomButtons, null, 2));
  process.exit(0);
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
