const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

async function main() {
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const page = browser.contexts()[0].pages().find(p => p.url().includes('labs.google'));
  if (!page) { console.error('No page'); process.exit(1); }

  // Inspect all media images in Flow project
  const media = await page.evaluate(() => {
    return Array.from(document.querySelectorAll('img'))
      .map((img, i) => ({
        index: i,
        alt: img.alt || '',
        src: img.src,
        w: img.naturalWidth,
        h: img.naturalHeight
      }))
      .filter(x => x.src.includes('media.getMediaUrlRedirect'));
  });

  console.log(`Found ${media.length} media items.`);
  const validImages = media.filter(m => !m.src.includes('MEDIA_URL_TYPE_THUMBNAIL'));
  console.log(`Found ${validImages.length} full images.`);

  if (validImages.length > 0) {
    const latest = validImages[0];
    console.log('Latest full image:', JSON.stringify(latest, null, 2));

    const base64 = await page.evaluate(async (url) => {
      const resp = await fetch(url);
      const buf = await resp.arrayBuffer();
      let binary = '';
      const bytes = new Uint8Array(buf);
      for (let i = 0; i < bytes.byteLength; i++) { binary += String.fromCharCode(bytes[i]); }
      return btoa(binary);
    }, latest.src);

    const outPath = path.resolve('storyboard-frames', 'F19.jpg');
    fs.writeFileSync(outPath, Buffer.from(base64, 'base64'));
    console.log(`Saved latest take to ${outPath} (${fs.statSync(outPath).size} bytes)`);
  }

  process.exit(0);
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
