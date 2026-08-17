const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

async function main() {
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const page = browser.contexts()[0].pages().find(p => p.url().includes('labs.google'));
  if (!page) { console.error('No page'); process.exit(1); }

  // Inspect all media URLs and elements in the DOM
  const mediaUrls = await page.evaluate(async () => {
    const images = Array.from(document.querySelectorAll('img[src*="media.getMediaUrlRedirect"]'));
    return images.map(img => ({
      src: img.src,
      alt: img.alt,
      width: img.naturalWidth,
      height: img.naturalHeight
    }));
  });

  console.log(`Total media images found: ${mediaUrls.length}`);
  if (mediaUrls.length > 0) {
    const newest = mediaUrls[0]; // Most recent in Flow UI is typically at the top/first in DOM or last
    console.log('Top media element:', JSON.stringify(newest, null, 2));

    // Fetch binary of the first and last to verify
    for (let i of [0, mediaUrls.length - 1]) {
      const item = mediaUrls[i];
      const base64 = await page.evaluate(async (url) => {
        const resp = await fetch(url);
        const buf = await resp.arrayBuffer();
        let binary = '';
        const bytes = new Uint8Array(buf);
        for (let j = 0; j < bytes.byteLength; j++) { binary += String.fromCharCode(bytes[j]); }
        return btoa(binary);
      }, item.src);

      const outPath = path.resolve('storyboard-frames', `F19_take_${i}.jpg`);
      fs.writeFileSync(outPath, Buffer.from(base64, 'base64'));
      console.log(`Saved take [${i}] to ${outPath} (${fs.statSync(outPath).size} bytes)`);
    }
  }

  process.exit(0);
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
