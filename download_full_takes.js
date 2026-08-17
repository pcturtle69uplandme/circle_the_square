const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

async function main() {
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const page = browser.contexts()[0].pages().find(p => p.url().includes('labs.google'));
  if (!page) { console.error('No page'); process.exit(1); }

  const imgs = await page.evaluate(() => {
    return Array.from(document.querySelectorAll('img[src*="media.getMediaUrlRedirect"]')).map(i => {
      const baseId = i.src.split('name=')[1].split('&')[0];
      return { alt: i.alt, baseId, fullUrl: 'https://labs.google/fx/api/trpc/media.getMediaUrlRedirect?name=' + baseId };
    });
  });

  console.log(`Found ${imgs.length} media elements.`);
  const uniqueIds = Array.from(new Set(imgs.map(x => x.baseId)));
  console.log(`Found ${uniqueIds.length} unique base media IDs.`);

  // Download top 4 unique full-resolution images
  for (let j = 0; j < Math.min(4, uniqueIds.length); j++) {
    const id = uniqueIds[j];
    const fullUrl = `https://labs.google/fx/api/trpc/media.getMediaUrlRedirect?name=${id}`;
    console.log(`Fetching full resolution for [${j}] (${id})...`);
    
    const base64 = await page.evaluate(async (url) => {
      const resp = await fetch(url);
      const buf = await resp.arrayBuffer();
      let binary = '';
      const bytes = new Uint8Array(buf);
      for (let i = 0; i < bytes.byteLength; i++) { binary += String.fromCharCode(bytes[i]); }
      return btoa(binary);
    }, fullUrl);

    const outPath = path.resolve('character-refs', 'stencils', `flow_full_take_${j}.jpg`);
    fs.writeFileSync(outPath, Buffer.from(base64, 'base64'));
    console.log(`Saved [${j}] to ${outPath} (${fs.statSync(outPath).size} bytes)`);
  }

  process.exit(0);
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
