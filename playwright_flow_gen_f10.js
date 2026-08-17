const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

async function main() {
  const userDataDir = path.resolve('C:\\ai\\.chrome_playwright_profile');
  console.log('Connecting with authenticated Google Flow profile...');
  
  const context = await chromium.launchPersistentContext(userDataDir, {
    channel: 'chrome',
    headless: false,
    viewport: { width: 1440, height: 900 },
    args: ['--disable-blink-features=AutomationControlled']
  });

  const page = context.pages()[0] || await context.newPage();
  console.log('Navigating to Google Flow project...');
  await page.goto('https://labs.google/fx/tools/flow/project/c1c8417d-30c8-4e76-a58c-260fec3f7a40', { waitUntil: 'networkidle', timeout: 60000 }).catch(() => {});
  await page.waitForTimeout(5000);

  console.log(`Page title: ${await page.title()}`);
  const stateScreen = path.resolve('C:\\ai\\Circle the Square\\flow_auth_canvas.png');
  await page.screenshot({ path: stateScreen });
  console.log(`Saved screenshot: ${stateScreen}`);

  // Find composer textbox / contenteditable
  console.log('Searching for composer input in project canvas...');
  const promptText = (
    "Stylised British sitcom comic art, clean bold line art, flat muted colour palette, expressive caricature, cel-shaded. " +
    "NOT photorealistic. Single still frame. 16:9 widescreen crop. NO text or lettering anywhere. " +
    "Medium close-up still frame inside executive office, matching desk framing of F04/F08. " +
    "Jan Peach (52-year-old overweight British CEO with thinning comb-over, navy suit, pale shirt, silver-grey tie, orange PRISM lanyard) " +
    "sits at his walnut executive desk. He looks mildly incredulous and bewildered, eyebrows raised with hands resting on desk, asking in disbelief. " +
    "Background matches black-and-white triangle acoustic wall and bookcase. Zero coffee cups on desk."
  );

  // Look for text input
  const inputSelectors = [
    'div[contenteditable="true"]',
    'textarea',
    '[role="textbox"]',
    '.tiptap',
    '.ProseMirror'
  ];

  let composer = null;
  for (const sel of inputSelectors) {
    composer = await page.$(sel);
    if (composer && await composer.isVisible()) {
      console.log(`Found visible composer matching: ${sel}`);
      break;
    }
  }

  if (composer) {
    await composer.click();
    await page.waitForTimeout(500);
    await composer.fill(promptText).catch(async () => {
      await page.keyboard.type(promptText);
    });
    console.log('Prompt successfully typed!');
  } else {
    console.log('Trying direct coordinate click on composer area...');
    await page.mouse.click(720, 840);
    await page.keyboard.type(promptText);
  }

  await page.waitForTimeout(1000);
  const beforeCreateScreen = path.resolve('C:\\ai\\Circle the Square\\flow_ready_create.png');
  await page.screenshot({ path: beforeCreateScreen });
  console.log(`Screenshot before Create: ${beforeCreateScreen}`);

  // Look for Create button
  console.log('Looking for Create button...');
  const createBtn = await page.$('button:has-text("Create"), button[aria-label*="Create"], button:has(span:has-text("Create"))');
  if (createBtn) {
    console.log('Clicking Create button...');
    await createBtn.click();
  } else {
    console.log('Clicking action button...');
    const btn = await page.$('button:has-text("arrow_forward"), button:has-text("add_2")');
    if (btn) await btn.click();
  }

  console.log('Generation triggered! Waiting for images to render (45s)...');
  await page.waitForTimeout(45000);

  const afterScreen = path.resolve('C:\\ai\\Circle the Square\\flow_rendered_gallery.png');
  await page.screenshot({ path: afterScreen });
  console.log(`Post-generation screenshot saved: ${afterScreen}`);

  // Extract all generated images from the page
  console.log('Extracting generated image URLs...');
  const imgUrls = await page.evaluate(() => {
    return Array.from(document.querySelectorAll('img')).map(img => ({
      src: img.src,
      alt: img.alt || '',
      width: img.naturalWidth || img.width,
      height: img.naturalHeight || img.height
    })).filter(img => img.src && (img.src.startsWith('blob:') || img.src.includes('google') || img.src.startsWith('http')));
  });

  console.log('Found Images on Canvas:', JSON.stringify(imgUrls, null, 2));

  // Find best candidate for F10
  const candidate = imgUrls.find(i => i.width >= 500 && !i.src.includes('avatar') && !i.src.includes('icon')) || imgUrls[imgUrls.length - 1];
  
  if (candidate) {
    console.log('Downloading keeper image:', candidate.src);
    const destPath = path.resolve('C:\\ai\\Circle the Square\\storyboard-frames\\F10.jpg');
    
    // Download image buffer
    const buffer = await page.evaluate(async (src) => {
      const resp = await fetch(src);
      const blob = await resp.blob();
      const reader = new FileReader();
      return new Promise((resolve) => {
        reader.onloadend = () => resolve(reader.result.split(',')[1]);
        reader.readAsDataURL(blob);
      });
    }, candidate.src);

    if (buffer) {
      fs.writeFileSync(destPath, Buffer.from(buffer, 'base64'));
      console.log(`SUCCESS: Downloaded Frame F10 to ${destPath}`);
    }
  }

  await context.close();
}

main().catch(console.error);
