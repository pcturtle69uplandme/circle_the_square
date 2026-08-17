const { chromium } = require('playwright');
const fs = require('fs');

async function main() {
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const page = browser.contexts()[0].pages().find(p => p.url().includes('labs.google'));
  if (!page) { console.error('No page'); process.exit(1); }

  const imgs = await page.evaluate(() => {
    return Array.from(document.querySelectorAll('img'))
      .map(i => ({ src: i.src, alt: i.alt, w: i.naturalWidth, h: i.naturalHeight }))
      .filter(x => x.src.includes('media.getMediaUrlRedirect'));
  });

  console.log(`Found ${imgs.length} media images in Flow:`);
  imgs.slice(0, 10).forEach((m, i) => console.log(`[${i}] ${m.alt} (${m.w}x${m.h}) ${m.src}`));
  process.exit(0);
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
