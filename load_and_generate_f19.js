const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

async function main() {
  console.log('Connecting to persistent Chrome over CDP on port 9222...');
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const page = browser.contexts()[0].pages().find(p => p.url().includes('labs.google'));
  if (!page) { console.error('No page'); process.exit(1); }

  console.log('Navigating directly to Circle the Square Flow project...');
  await page.goto('https://labs.google/fx/tools/flow/project/f2f0d2c9-ec16-420d-98af-b495197dad08');
  await page.waitForTimeout(6000);
  console.log('Current URL:', page.url());

  // 1. Wait for composer textbox to be visible
  const composer = page.locator('div[contenteditable="true"], textarea, div[role="textbox"]').first();
  await composer.waitFor({ state: 'visible', timeout: 15000 });
  console.log('Composer found and visible.');

  // 2. Click composer to focus and clear
  await composer.click();
  await page.keyboard.press('Control+A');
  await page.keyboard.press('Backspace');
  await page.waitForTimeout(500);

  // 3. Attach Jan Peach character entity via Add Media / picker
  console.log('Checking for Add Media / Character buttons...');
  const addBtn = page.locator('button[aria-label="Add Media"], button:has-text("Add Media")').first();
  if (await addBtn.isVisible()) {
    await addBtn.click();
    await page.waitForTimeout(1000);

    const charTab = page.locator('button:has-text("Characters"), [role="tab"]:has-text("Characters")').first();
    if (await charTab.isVisible()) {
      await charTab.click();
      await page.waitForTimeout(1000);
    }

    const janItem = page.locator('text="Jan Peach"').first();
    if (await janItem.isVisible()) {
      console.log('Found Jan Peach character tile. Clicking...');
      await janItem.click();
      await page.waitForTimeout(500);
    }

    const addPromptBtn = page.locator('button:has-text("Add to Prompt")').first();
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

  // 5. Count existing media
  const initialMedia = await page.evaluate(() => {
    return Array.from(document.querySelectorAll('img[src*="media.getMediaUrlRedirect"]')).map(img => img.src);
  });
  console.log(`Initial media count: ${initialMedia.length}`);

  // 6. Click Create button
  console.log('Clicking Create button...');
  const createBtn = page.locator('button:has-text("Create")').first();
  await createBtn.click();
  console.log('Create clicked! Polling for new generation...');

  // 7. Poll for completion
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
    const elapsed = Math.round((Date.now() - start)/1000);
    console.log(`Still generating... (${elapsed}s elapsed)`);
  }

  if (newSrc) {
    console.log('Downloading generated high-res frame...');
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
    console.log(`[OK] Saved F19 master frame to ${outPath} (${fs.statSync(outPath).size} bytes)`);
  } else {
    await page.screenshot({ path: 'character-refs/stencils/f19_timeout.png' });
    console.log('Saved f19_timeout.png for review.');
  }

  process.exit(0);
}

main().catch(err => {
  console.error('Error in load_and_generate_f19:', err.message);
  process.exit(1);
});
