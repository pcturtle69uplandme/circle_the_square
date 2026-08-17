const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

async function main() {
  console.log('Connecting to persistent Chrome over CDP on port 9222...');
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const ctx = browser.contexts()[0];
  const page = ctx.pages().find(p => p.url().includes('labs.google'));
  if (!page) {
    console.error('Google Flow page not found in active browser tabs.');
    process.exit(1);
  }

  await page.bringToFront();
  console.log('Active Flow URL:', page.url());

  const promptText = `Stylised British sitcom comic art, clean bold line art, flat muted colour palette, expressive caricature, cel-shaded. NOT photorealistic. Single still frame. 16:9 widescreen crop. No visible real-world branding or crests. Character appearance must exactly match the attached references — do not invent or alter appearance, age, or wardrobe colour. The desk, shelving, wall pattern and every piece of furniture must exactly match the attached location reference in design, colour and position. Absolutely NO text, NO speech bubbles, NO captions, NO labels, NO sound effects, NO lettering of any kind anywhere in the image.

Wide still frame inside executive office. Jan Peach (52-year-old overweight cartoon executive with thinning comb-over, round face, gold watch on wrist, orange PRISM lanyard around his neck) has pulled his pale blue collared shirt fully off, chest bared with manscaped hair, mid-motion dropping the crumpled shirt onto his chair. Flustered, sweating brow, flushed face, breathing heavily. Background is strictly the office with black-and-white geometric triangle acoustic wall, dark wooden bookcase on the right, and walnut desk.`;

  // 1. Locate composer contenteditable or textarea
  const composerSelector = 'div[contenteditable="true"], textarea';
  await page.waitForSelector(composerSelector, { timeout: 10000 });
  const composer = page.locator(composerSelector).first();
  await composer.click();
  await page.keyboard.press('Control+A');
  await page.keyboard.press('Backspace');
  await page.waitForTimeout(500);

  console.log('Filling F19 prompt into composer...');
  await composer.fill(promptText);
  await page.waitForTimeout(1000);

  // 2. Count existing generated media items before triggering Create
  const initialMediaIds = await page.evaluate(() => {
    const images = Array.from(document.querySelectorAll('img[src*=\"media.getMediaUrlRedirect\"], img[src*=\"lh3.googleusercontent.com\"]'));
    return images.map(img => img.src);
  });
  console.log(`Initial media elements on page: ${initialMediaIds.length}`);

  // 3. Find and click Create button
  console.log('Locating Create button...');
  const createBtn = page.locator('button:has-text("Create"), button[aria-label="Create"]').first();
  if (await createBtn.isVisible()) {
    await createBtn.click();
    console.log('Clicked Create button successfully!');
  } else {
    // Fallback search
    const clicked = await page.evaluate(() => {
      const btns = Array.from(document.querySelectorAll('button'));
      const btn = btns.find(b => b.innerText && b.innerText.trim().toLowerCase() === 'create');
      if (btn) { btn.click(); return true; }
      return false;
    });
    console.log('Create clicked via evaluate:', clicked);
  }

  // 4. Poll for new media generation
  console.log('Waiting for generation to complete (polling media elements)...');
  let newMediaUrl = null;
  const startTime = Date.now();
  const timeoutMs = 180000; // 3 min max

  while (Date.now() - startTime < timeoutMs) {
    await page.waitForTimeout(5000);
    const currentMedia = await page.evaluate(() => {
      const imgs = Array.from(document.querySelectorAll('img'));
      return imgs.map(img => img.src).filter(src => src && (src.includes('media.getMediaUrlRedirect') || src.includes('labs.google')));
    });

    const diff = currentMedia.filter(src => !initialMediaIds.includes(src));
    if (diff.length > 0) {
      newMediaUrl = diff[0];
      console.log(`[OK] Detected new generated media URL: ${newMediaUrl}`);
      break;
    }
    const elapsed = Math.round((Date.now() - startTime) / 1000);
    console.log(`Still generating... (${elapsed}s elapsed)`);
  }

  if (!newMediaUrl) {
    // Take screenshot of Flow page for diagnosis
    await page.screenshot({ path: 'character-refs/stencils/flow_f19_status.png' });
    console.log('Saved flow_f19_status.png for inspection.');
  } else {
    // 5. Download the high-res image via page.evaluate fetch
    console.log('Fetching high-res image binary from Flow context...');
    const base64Data = await page.evaluate(async (url) => {
      const resp = await fetch(url);
      const buffer = await resp.arrayBuffer();
      let binary = '';
      const bytes = new Uint8Array(buffer);
      for (let i = 0; i < bytes.byteLength; i++) {
        binary += String.fromCharCode(bytes[i]);
      }
      return btoa(binary);
    }, newMediaUrl);

    const outPath = path.resolve('storyboard-frames', 'F19.jpg');
    fs.writeFileSync(outPath, Buffer.from(base64Data, 'base64'));
    console.log(`[OK] Saved F19 Take 0 to ${outPath} (${fs.statSync(outPath).size} bytes)`);
  }

  await browser.disconnect();
}

main().catch(err => {
  console.error('Error in flow_generate_f19:', err.message);
  process.exit(1);
});
