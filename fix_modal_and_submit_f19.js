const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

async function main() {
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const page = browser.contexts()[0].pages().find(p => p.url().includes('labs.google'));
  if (!page) { console.error('No page'); process.exit(1); }

  // 1. Close the open character modal
  console.log('Closing character detail modal...');
  const doneBtn = page.locator('button:has-text("Done"), button:has-text("Back")').first();
  if (await doneBtn.isVisible()) {
    await doneBtn.click();
    await page.waitForTimeout(1000);
  }

  // Also press Escape if still overlaying
  await page.keyboard.press('Escape');
  await page.waitForTimeout(500);

  // 2. Check composer on the canvas
  const composer = page.locator('div[contenteditable="true"], textarea, div[role="textbox"]').first();
  await composer.waitFor({ state: 'visible', timeout: 5000 });
  await composer.click();
  console.log('Composer focused.');

  const promptText = `Stylised British sitcom comic art, clean bold line art, flat muted colour palette, expressive caricature, cel-shaded. NOT photorealistic. Single still frame. 16:9 widescreen crop. No visible real-world branding or crests. Character appearance must exactly match the attached references — do not invent or alter appearance, age, or wardrobe colour. The desk, shelving, wall pattern and every piece of furniture must exactly match the attached location reference in design, colour and position. Absolutely NO text, NO speech bubbles, NO captions, NO labels, NO sound effects, NO lettering of any kind anywhere in the image.

Wide still frame inside executive office. Jan Peach (52-year-old overweight cartoon executive with thinning comb-over, round face, gold watch on wrist, orange PRISM lanyard around his neck) has pulled his pale blue collared shirt fully off, chest bared with manicured chest hair arrow pointing downward, mid-motion dropping the crumpled shirt onto his chair. Flustered, sweating brow, flushed face, breathing heavily. Background is strictly the office with black-and-white geometric triangle acoustic wall, dark wooden bookcase on the right, and walnut desk.`;

  await composer.fill(promptText);
  await page.waitForTimeout(500);

  // 3. Find and click Create button
  console.log('Locating Create button on canvas...');
  const createBtn = page.locator('button:has-text("arrow_forward"), button:has-text("Create"), button[aria-label="Create"]').last();
  await createBtn.click();
  console.log('Create clicked on canvas! Generation initiated.');

  await page.screenshot({ path: 'character-refs/stencils/flow_generating_f19.png' });
  console.log('Saved flow_generating_f19.png');
  process.exit(0);
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
