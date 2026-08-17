const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

async function main() {
  const userDataDir = path.resolve('C:\\ai\\.chrome_playwright_profile');
  console.log('Connecting to Google Flow via Playwright persistent context...');
  
  const context = await chromium.launchPersistentContext(userDataDir, {
    channel: 'chrome',
    headless: false,
    viewport: { width: 1440, height: 900 },
    args: ['--disable-blink-features=AutomationControlled']
  });

  const page = context.pages()[0] || await context.newPage();
  console.log('Navigating to Google Flow project...');
  await page.goto('https://labs.google/fx/tools/flow/project/c1c8417d-30c8-4e76-a58c-260fec3f7a40', { waitUntil: 'networkidle', timeout: 45000 }).catch(() => {});

  await page.waitForTimeout(4000);
  
  // Find composer textbox
  console.log('Locating composer input...');
  const promptText = (
    "Medium close-up still frame inside Jan's executive office, matching the desk framing of F04/F08. " +
    "Jan Peach (52-year-old overweight British CEO with thinning comb-over hair, navy suit, pale shirt, silver-grey tie, orange PRISM lanyard) " +
    "sits at his walnut executive desk. He looks mildly incredulous and bewildered, eyebrows raised and head cocked slightly with hands resting on desk, " +
    "asking in disbelief. On the desk are a laptop and papers (no coffee cups). Background behind Jan is strictly the black-and-white geometric triangle " +
    "acoustic feature wall and side bookcase, matching F01/F08. Stylised British sitcom comic art, clean bold line art, flat muted colour palette, " +
    "expressive caricature, cel-shaded, 16:9 widescreen crop. Absolutely NO text, NO speech bubbles, NO captions, NO labels, NO sound effects, " +
    "NO lettering of any kind anywhere in the image."
  );

  // Try finding textbox / contenteditable
  let inputElement = await page.$('textarea, [contenteditable="true"], textbox');
  if (!inputElement) {
    // Try by placeholder or role
    inputElement = await page.$('div[role="textbox"], [placeholder*="prompt"], [placeholder*="Describe"]');
  }

  if (inputElement) {
    console.log('Found composer input element! Typing prompt...');
    await inputElement.click();
    await page.waitForTimeout(500);
    // Clear and fill
    await inputElement.fill(promptText).catch(async () => {
      await page.keyboard.type(promptText);
    });
    console.log('Prompt typed successfully.');
  } else {
    console.log('Looking for text area by clicking on composer area...');
    await page.mouse.click(720, 850);
    await page.keyboard.type(promptText);
  }

  await page.waitForTimeout(1000);
  const beforeCreateScreen = path.resolve('C:\\ai\\Circle the Square\\flow_before_create.png');
  await page.screenshot({ path: beforeCreateScreen });
  console.log(`Saved screenshot before Create: ${beforeCreateScreen}`);

  // Find and click Create button (avoiding Return in composer per handover rules)
  console.log('Looking for Create button...');
  const createButton = await page.$('button:has-text("Create"), button[aria-label*="Create"], button:has(span:has-text("Create"))');
  if (createButton) {
    console.log('Clicking Create button...');
    await createButton.click();
  } else {
    console.log('Attempting selector for Create icon button...');
    const btn = await page.$('button:has-text("arrow_forward"), button:has-text("add_2")');
    if (btn) await btn.click();
  }

  console.log('Generation triggered! Waiting for images to render (30s)...');
  await page.waitForTimeout(30000);

  const afterGenScreen = path.resolve('C:\\ai\\Circle the Square\\flow_after_generation.png');
  await page.screenshot({ path: afterGenScreen });
  console.log(`Saved post-generation screenshot: ${afterGenScreen}`);

  // Try extracting the latest generated image
  console.log('Attempting to download latest generated media...');
  const images = await page.$$('img');
  console.log(`Found ${images.length} images on page.`);
  
  for (const img of images) {
    const src = await img.getAttribute('src');
    if (src && (src.startsWith('blob:') || src.startsWith('http') || src.startsWith('data:'))) {
      const alt = (await img.getAttribute('alt')) || '';
      console.log(`Image candidate: alt="${alt}", src="${src.substring(0, 60)}..."`);
    }
  }
  
  console.log('F10 generation workflow run complete.');
}

main().catch(console.error);
