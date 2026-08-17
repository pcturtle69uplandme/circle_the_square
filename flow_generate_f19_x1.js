const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

async function main() {
  console.log('Connecting to persistent Chrome over CDP on port 9222...');
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const page = browser.contexts()[0].pages().find(p => p.url().includes('labs.google'));
  if (!page) { console.error('No page'); process.exit(1); }

  // 1. Get initial image IDs on page before click
  const initialMedia = await page.evaluate(() => {
    return Array.from(document.querySelectorAll('img[src*="media.getMediaUrlRedirect"]')).map(img => img.src);
  });
  console.log(`Initial media count: ${initialMedia.length}`);

  // 2. Click the Create button (arrow_forward at x=1276, y=951)
  console.log('Clicking the Create button (arrow_forward at x=1276, y=951)...');
  await page.mouse.click(1276, 951);
  console.log('Create clicked successfully!');

  // 3. Poll for new image generation
  const start = Date.now();
  let newMediaUrl = null;
  while (Date.now() - start < 180000) {
    await page.waitForTimeout(4000);
    const currentMedia = await page.evaluate(() => {
      return Array.from(document.querySelectorAll('img[src*="media.getMediaUrlRedirect"]')).map(img => img.src);
    });

    const diff = currentMedia.filter(s => !initialMedia.includes(s));
    if (diff.length > 0) {
      newMediaUrl = diff[0];
      console.log(`[OK] Detected new generated image: ${newMediaUrl}`);
      break;
    }
    const elapsed = Math.round((Date.now() - start) / 1000);
    console.log(`Generating F19 in Google Flow... (${elapsed}s elapsed)`);
  }

  if (newMediaUrl) {
    console.log('Fetching high-res image binary from Google Flow context...');
    const base64 = await page.evaluate(async (url) => {
      const resp = await fetch(url);
      const buf = await resp.arrayBuffer();
      let binary = '';
      const bytes = new Uint8Array(buf);
      for (let i = 0; i < bytes.byteLength; i++) { binary += String.fromCharCode(bytes[i]); }
      return btoa(binary);
    }, newMediaUrl);

    const outPath = path.resolve('storyboard-frames', 'F19.jpg');
    fs.writeFileSync(outPath, Buffer.from(base64, 'base64'));
    console.log(`[OK] Saved F19 master frame to ${outPath} (${fs.statSync(outPath).size} bytes)`);
  } else {
    await page.screenshot({ path: 'character-refs/stencils/f19_generation_state.png' });
    console.log('Saved f19_generation_state.png for inspection.');
  }

  process.exit(0);
}

main().catch(err => {
  console.error('Error in flow_generate_f19_x1:', err.message);
  process.exit(1);
});
