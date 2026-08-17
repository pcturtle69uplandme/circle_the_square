const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

async function main() {
  console.log('Connecting to persistent Chrome over CDP on port 9222...');
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const page = browser.contexts()[0].pages().find(p => p.url().includes('labs.google'));
  if (!page) { console.error('No page'); process.exit(1); }

  await page.bringToFront();

  // 1. Close any open dialogs first
  const doneBtn = page.locator('button:has-text("Done"), button:has-text("Back"), button:has-text("Close")').first();
  if (await doneBtn.isVisible()) {
    console.log('Closing open modal...');
    await doneBtn.click();
    await page.waitForTimeout(1000);
  }

  // 2. Clear composer
  const composer = page.locator('div[contenteditable="true"], textarea').first();
  await composer.click();
  await page.keyboard.press('Control+A');
  await page.keyboard.press('Backspace');
  await page.waitForTimeout(500);

  // 3. Attach @Jan Peach via Add Media or character button
  console.log('Attaching @Jan Peach character reference...');
  // Look for Add Media button or type @
  const addMediaBtn = page.locator('button[aria-label="Add Media"], button:has-text("Add Media"), button:has-text("Add")').first();
  if (await addMediaBtn.isVisible()) {
    await addMediaBtn.click();
    await page.waitForTimeout(1000);
    // Click Characters tab inside modal
    const charTab = page.locator('[role="tab"]:has-text("Characters"), button:has-text("Characters")').first();
    if (await charTab.isVisible()) {
      await charTab.click();
      await page.waitForTimeout(1000);
    }
    // Select Jan Peach
    const janTile = page.locator('text="Jan Peach", img[alt*="Jan"]').first();
    if (await janTile.isVisible()) {
      await janTile.click();
      await page.waitForTimeout(500);
    }
    // Click Add to Prompt / Done
    const addPromptBtn = page.locator('button:has-text("Add to Prompt"), button:has-text("Select")').first();
    if (await addPromptBtn.isVisible()) {
      await addPromptBtn.click();
      await page.waitForTimeout(1000);
    }
  }

  // 4. Fill the prompt text
  const promptText = `Stylised British sitcom comic art, clean bold line art, flat muted colour palette, expressive caricature, cel-shaded. NOT photorealistic. Single still frame. 16:9 widescreen crop. No visible real-world branding or crests. Character appearance must exactly match the attached references — do not invent or alter appearance, age, or wardrobe colour. The desk, shelving, wall pattern and every piece of furniture must exactly match the attached location reference in design, colour and position. Absolutely NO text, NO speech bubbles, NO captions, NO labels, NO sound effects, NO lettering of any kind anywhere in the image.

Wide still frame inside executive office. Jan Peach (52-year-old overweight cartoon executive with thinning comb-over, round face, gold watch on wrist, orange PRISM lanyard around his neck) has pulled his pale blue collared shirt fully off, chest bared with manicured chest hair arrow pointing downward, mid-motion dropping the crumpled shirt onto his chair. Flustered, sweating brow, flushed face, breathing heavily. Background is strictly the office with black-and-white geometric triangle acoustic wall, dark wooden bookcase on the right, and walnut desk.`;

  await composer.click();
  await composer.fill(promptText);
  await page.waitForTimeout(1000);

  // 5. Count existing media IDs
  const initialMedia = await page.evaluate(() => {
    return Array.from(document.querySelectorAll('img[src*="media.getMediaUrlRedirect"]')).map(img => img.src);
  });
  console.log(`Initial media count: ${initialMedia.length}`);

  // 6. Click Create
  console.log('Clicking Create button...');
  const createBtn = page.locator('button:has-text("Create")').first();
  await createBtn.click();
  console.log('Create clicked! Waiting for generation...');

  // 7. Poll for new image
  const start = Date.now();
  let newSrc = null;
  while (Date.now() - start < 180000) {
    await page.waitForTimeout(5000);
    const current = await page.evaluate(() => {
      return Array.from(document.querySelectorAll('img[src*="media.getMediaUrlRedirect"]')).map(img => img.src);
    });
    const diff = current.filter(s => !initialMedia.includes(s));
    if (diff.length > 0) {
      newSrc = diff[0];
      console.log(`[OK] Generated new media: ${newSrc}`);
      break;
    }
    console.log(`Generating... (${Math.round((Date.now() - start)/1000)}s)`);
  }

  if (newSrc) {
    console.log('Downloading generated take...');
    const base64 = await page.evaluate(async (url) => {
      const resp = await fetch(url);
      const buf = await resp.arrayBuffer();
      let binary = '';
      const bytes = new Uint8Array(buf);
      for (let i = 0; i < bytes.byteLength; i++) { binary += String.fromCharCode(bytes[i]); }
      return btoa(binary);
    }, newSrc);

    const outPath = path.resolve('storyboard-frames', 'F19.jpg');
    fs.writeFileSync(outPath, Buffer.from(base64, 'base64'));
    console.log(`[OK] Saved F19 keeper take to ${outPath} (${fs.statSync(outPath).size} bytes)`);
  } else {
    await page.screenshot({ path: 'character-refs/stencils/f19_poll_timeout.png' });
    console.log('Saved f19_poll_timeout.png for debugging.');
  }

  process.exit(0);
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
