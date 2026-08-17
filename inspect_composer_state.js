const { chromium } = require('playwright');

async function main() {
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const page = browser.contexts()[0].pages().find(p => p.url().includes('labs.google'));
  if (!page) { console.error('No page'); process.exit(1); }

  const status = await page.evaluate(() => {
    const composer = document.querySelector('div[contenteditable="true"]');
    const composerText = composer ? composer.innerText : 'NO COMPOSER';

    const btns = Array.from(document.querySelectorAll('button')).map(b => ({
      text: b.innerText.replace(/\n/g, ' ').trim(),
      disabled: b.disabled,
      className: b.className
    }));

    const alerts = Array.from(document.querySelectorAll('[role="alert"], [class*="error"], [class*="toast"]'))
      .map(el => el.innerText);

    const images = Array.from(document.querySelectorAll('img')).map(img => ({
      alt: img.alt,
      src: img.src
    }));

    return { composerText: composerText.substring(0, 100), btns: btns.slice(0, 15), alerts, imgCount: images.length };
  });

  console.log('DOM status:', JSON.stringify(status, null, 2));
  process.exit(0);
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
