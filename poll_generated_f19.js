const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

async function main() {
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const page = browser.contexts()[0].pages().find(p => p.url().includes('labs.google'));
  if (!page) { console.error('No page'); process.exit(1); }

  console.log('Polling for new generated F19 image in Google Flow...');
  const start = Date.now();
  let foundUrl = null;

  while (Date.now() - start < 90000) {
    await page.waitForTimeout(4000);
    const media = await page.evaluate(() => {
      const imgs = Array.from(document.querySelectorAll('img[src*="media.getMediaUrlRedirect"]'));
      return imgs.map(img => ({ src: img.src, alt: img.alt, w: img.naturalWidth, h: img.naturalHeight }));
    });

    if (media.length > 0) {
      // Get the latest non-thumbnail image
      const fullImgs = media.filter(m => !m.src.includes('MEDIA_URL_TYPE_THUMBNAIL'));
      if (fullImgs.length > 0) {
        foundUrl = fullImgs[0].src;
        console.log(`[OK] Found generated take URL: ${foundUrl}`);
        break;
      }
    }
    const elapsed = Math.round((Date.now() - start)/1000);
    console.log(`Generating in Flow... (${elapsed}s elapsed)`);
  }

  if (foundUrl) {
    console.log('Downloading high-res image binary from Flow...');
    const base64 = await page.evaluate(async (url) => {
      const resp = await fetch(url);
      const buf = await resp.arrayBuffer();
      let binary = '';
      const bytes = new Uint8Array(buf);
      for (let i = 0; i < bytes.byteLength; i++) { binary += String.fromCharCode(bytes[i]); }
      return btoa(binary);
    }, foundUrl);

    const outPath = path.resolve('storyboard-frames', 'F19.jpg');
    fs.writeFileSync(outPath, Buffer.from(base64, 'base64'));
    console.log(`[OK] Saved F19 master frame to ${outPath} (${fs.statSync(outPath).size} bytes)`);
  } else {
    await page.screenshot({ path: 'character-refs/stencils/f19_poll_final_state.png' });
    console.log('Saved f19_poll_final_state.png');
  }

  process.exit(0);
}

main().catch(err => {
  console.error('Error in poll_generated_f19:', err.message);
  process.exit(1);
});
