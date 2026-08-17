const { chromium } = require('playwright');

async function main() {
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const page = browser.contexts()[0].pages().find(p => p.url().includes('labs.google'));
  if (!page) { console.error('No page'); process.exit(1); }

  const info = await page.evaluate(() => {
    const allButtons = Array.from(document.querySelectorAll('button')).map(b => ({
      text: b.innerText.replace(/\n/g, ' ').trim(),
      aria: b.getAttribute('aria-label') || '',
      rect: b.getBoundingClientRect()
    })).filter(b => b.rect.width > 0);

    const spans = Array.from(document.querySelectorAll('h1, h2, h3, p, span'))
      .map(s => ({ text: s.innerText.trim(), tag: s.tagName }))
      .filter(s => s.text.length > 0 && s.text.length < 50);

    return { allButtons: allButtons.slice(0, 25), spans: spans.slice(0, 20) };
  });

  console.log('Visible Buttons:', JSON.stringify(info.allButtons, null, 2));
  console.log('Visible Texts:', JSON.stringify(info.spans, null, 2));
  process.exit(0);
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
