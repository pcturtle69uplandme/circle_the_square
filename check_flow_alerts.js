const { chromium } = require('playwright');

async function main() {
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const page = browser.contexts()[0].pages().find(p => p.url().includes('labs.google'));
  if (!page) { console.error('No page'); process.exit(1); }

  const info = await page.evaluate(() => {
    const alerts = Array.from(document.querySelectorAll('[role="alert"], [class*="toast"], [class*="error"], [class*="policy"], [class*="snackbar"]'))
      .map(el => el.innerText.trim())
      .filter(Boolean);

    const media = Array.from(document.querySelectorAll('img[src*="media.getMediaUrlRedirect"]'))
      .map(i => ({ alt: i.alt, src: i.src, w: i.naturalWidth, h: i.naturalHeight }));

    const composer = document.querySelector('div[contenteditable="true"]');

    return {
      alerts,
      composerText: composer ? composer.innerText.substring(0, 80) : '',
      mediaCount: media.length,
      topMedia: media.slice(0, 4)
    };
  });

  console.log('Flow Alert State:', JSON.stringify(info, null, 2));
  process.exit(0);
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
