const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

async function main() {
  console.log('Connecting to persistent Chrome over CDP on port 9222...');
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const page = browser.contexts()[0].pages().find(p => p.url().includes('labs.google'));
  if (!page) { console.error('No page'); process.exit(1); }

  console.log('Current URL:', page.url());

  // 1. If in gallery view, click Circle the Square animation project
  if (!page.url().includes('/project/f2f0d2c9')) {
    console.log('Clicking Circle the Square animation project card...');
    const projectCard = page.locator('text="Circle the Square animation"').first();
    if (await projectCard.isVisible()) {
      await projectCard.click();
      await page.waitForTimeout(4000);
    } else {
      await page.goto('https://labs.google/fx/tools/flow/project/f2f0d2c9-ec16-420d-98af-b495197dad08');
      await page.waitForTimeout(5000);
    }
  }

  console.log('Now at URL:', page.url());

  // 2. Wait for the composer textbox
  const composer = page.locator('div[contenteditable="true"]').first();
  await composer.waitFor({ state: 'visible', timeout: 15000 });
  console.log('Composer found and visible.');
  await composer.click();
  await page.keyboard.press('Control+A');
  await page.keyboard.press('Backspace');
  await page.waitForTimeout(500);

  const policySafePrompt = `Stylised British sitcom comic art, clean bold line art, flat muted colour palette, expressive caricature, cel-shaded. NOT photorealistic. Single still frame. 16:9 widescreen crop. No visible real-world branding or crests. Character appearance must exactly match the attached references — do not invent or alter appearance, age, or wardrobe colour. The desk, shelving, wall pattern and every piece of furniture must exactly match the attached location reference in design, colour and position. Absolutely NO text, NO speech bubbles, NO captions, NO labels, NO sound effects, NO lettering of any kind anywhere in the image.

Wide still frame inside executive office. Jan Peach (52-year-old overweight cartoon executive with thinning comb-over, round face, gold watch on wrist, orange PRISM lanyard around his neck) is in a flustered cartoon comedy state, having discarded his pale blue dress shirt onto his desk chair. He is wiping his flushed, sweaty brow, breathing heavily and stressed. Background is strictly his executive office with black-and-white geometric triangle acoustic wall, dark wooden bookcase on the right, and walnut desk.`;

  console.log('Filling policy-safe prompt into composer...');
  await composer.fill(policySafePrompt);
  await page.waitForTimeout(1000);

  // 3. Count existing media
  const initialMedia = await page.evaluate(() => {
    return Array.from(document.querySelectorAll('img[src*="media.getMediaUrlRedirect"]')).map(img => img.src);
  });
  console.log(`Initial media count: ${initialMedia.length}`);

  // 4. Click Create button (arrow_forward Create at x=1260, y=935 / bottom right)
  console.log('Clicking Create button...');
  const createBtn = page.locator('button:has-text("Create"), button[aria-label="Create"]').last();
  if (await createBtn.isVisible()) {
    await createBtn.click();
  } else {
    await page.mouse.click(1276, 951);
  }
  console.log('Create clicked! Polling for new generated media...');

  // 5. Poll for new image
  const start = Date.now();
  let newUrl = null;
  while (Date.now() - start < 180000) {
    await page.waitForTimeout(5000);
    const current = await page.evaluate(() => {
      return Array.from(document.querySelectorAll('img[src*="media.getMediaUrlRedirect"]')).map(img => img.src);
    });

    const diff = current.filter(s => !initialMedia.includes(s));
    if (diff.length > 0) {
      newUrl = diff[0];
      console.log(`[OK] Detected new generated take: ${newUrl}`);
      break;
    }
    const elapsed = Math.round((Date.now() - start) / 1000);
    console.log(`Generating in Google Flow... (${elapsed}s elapsed)`);
  }

  if (newUrl) {
    console.log('Downloading high-res image binary from Flow...');
    const base64 = await page.evaluate(async (url) => {
      const resp = await fetch(url);
      const buf = await resp.arrayBuffer();
      let binary = '';
      const bytes = new Uint8Array(buf);
      for (let i = 0; i < bytes.byteLength; i++) { binary += String.fromCharCode(bytes[i]); }
      return btoa(binary);
    }, newUrl);

    const outPath = path.resolve('storyboard-frames', 'F19.jpg');
    fs.writeFileSync(outPath, Buffer.from(base64, 'base64'));
    console.log(`[OK] Saved F19 master frame to ${outPath} (${fs.statSync(outPath).size} bytes)`);
  } else {
    await page.screenshot({ path: 'character-refs/stencils/f19_poll_final.png' });
    console.log('Saved f19_poll_final.png for review.');
  }

  process.exit(0);
}

main().catch(err => {
  console.error('Error in enter_project_and_submit_f19:', err.message);
  process.exit(1);
});
