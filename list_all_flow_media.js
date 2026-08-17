const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

async function main() {
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const page = browser.contexts()[0].pages().find(p => p.url().includes('labs.google'));
  if (!page) { console.error('No page'); process.exit(1); }

  const imgs = await page.evaluate(() => {
    return Array.from(document.querySelectorAll('img'))
      .filter(x => x.src.includes('media.getMediaUrlRedirect'))
      .map((img, i) => ({
        index: i,
        src: img.src,
        alt: img.alt || '',
        w: img.naturalWidth,
        h: img.naturalHeight
      }));
  });

  console.log(`Found ${imgs.length} media images in Flow:`);
  imgs.forEach(m => {
    const id = m.src.split('name=')[1] || '';
    console.log(`[${m.index}] alt="${m.alt}" size=${m.w}x${m.h} id=${id}`);
  });

  // Download the last 6 images to examine them
  const lastSix = imgs.slice(-6);
  for (let j = 0; j < lastSix.length; j++) {
    const item = lastSix[j];
    const base64 = await page.evaluate(async (url) => {
      const resp = await fetch(url);
      const buf = await resp.arrayBuffer();
      let binary = '';
      const bytes = new Uint8Array(buf);
      for (let i = 0; i < bytes.byteLength; i++) { binary += String.fromCharCode(bytes[i]); }
      return btoa(binary);
    }, item.src);

    const outPath = path.resolve('character-refs', 'stencils', `flow_recent_${j}_${item.alt.replace(/[^a-zA-Z0-9]/g, '_')}.jpg`);
    fs.writeFileSync(outPath, Buffer.from(base64, 'base64'));
    console.log(`Saved recent take [${j}] (${item.alt}) to ${outPath}`);
  }

  process.exit(0);
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
