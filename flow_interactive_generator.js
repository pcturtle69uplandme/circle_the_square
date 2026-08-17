const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const PROJECT_DIR = 'C:\\AI\\Circle the Square';
const USER_DATA_DIR = 'C:\\ai\\.chrome_playwright_profile';
const FLOW_URL = 'https://labs.google/fx/tools/flow/project/c1c8417d-30c8-4e76-a58c-260fec3f7a40';

const STYLE_ANCHOR = "Stylised British sitcom comic art, clean bold line art, flat muted colour palette, expressive caricature, cel-shaded. NOT photorealistic. Single still frame. 16:9 widescreen crop. No visible real-world branding or crests. Character appearance must exactly match the attached references — do not invent or alter appearance, age, or wardrobe colour. The desk, shelving, wall pattern and every piece of furniture must exactly match the attached location reference in design, colour and position. Absolutely NO text, NO speech bubbles, NO captions, NO labels, NO sound effects, NO lettering of any kind anywhere in the image.";

const FRAMES_CONFIG = {
  F10: {
    prompt: "Medium close-up still frame inside Jan's executive office, matching the desk framing and composition of F04 and F08. Jan Peach (52-year-old overweight British CEO with thinning comb-over, navy suit jacket buttoned over a pale blue shirt, silver-grey tie, orange PRISM lanyard and badge on chest, gold watch on wrist) sits behind his walnut executive desk. He looks mildly incredulous and bewildered that Christina does not get his Star Trek reference, with eyebrows raised high and palms gesturing slightly upward in disbelief. Background is strictly the black-and-white triangle geometric acoustic wall and dark wooden bookcase on the right, matching F01/F08. On the desk are his open silver laptop and a stack of papers. Zero coffee cups.",
    dialogue: 'Jan: "You never seen Star Trek Next Generation?"'
  }
};

async function main() {
  const targetFrame = (process.argv[2] || 'F10').toUpperCase();
  const frameConf = FRAMES_CONFIG[targetFrame] || FRAMES_CONFIG.F10;
  const fullPrompt = `${STYLE_ANCHOR} ${frameConf.prompt}`;

  console.log(`========================================================================`);
  console.log(`🎬 Google Flow Interactive Generator — Frame ${targetFrame}`);
  console.log(`Beat: ${frameConf.dialogue}`);
  console.log(`========================================================================`);
  console.log(`Launching persistent Chrome browser at: ${USER_DATA_DIR}`);

  const context = await chromium.launchPersistentContext(USER_DATA_DIR, {
    channel: 'chrome',
    headless: false,
    viewport: { width: 1440, height: 900 },
    args: ['--disable-blink-features=AutomationControlled', '--start-maximized']
  });

  const page = context.pages()[0] || await context.newPage();
  console.log(`Navigating to Google Flow project: ${FLOW_URL}`);
  await page.goto(FLOW_URL, { waitUntil: 'domcontentloaded', timeout: 60000 }).catch(() => {});

  // Polling loop waiting for user authentication
  console.log('>>> Waiting for authentication... Please complete sign-in in the browser window if prompted. <<<');
  let authenticated = false;
  for (let i = 0; i < 60; i++) {
    await page.waitForTimeout(3000);
    const url = page.url();
    const title = await page.title().catch(() => '');
    console.log(`[Status] URL: ${url.substring(0, 65)}... | Title: ${title}`);
    
    if (url.includes('/flow/project/') && !url.includes('signin') && !url.includes('accounts.google')) {
      authenticated = true;
      console.log('✅ Logged in successfully and inside Google Flow project canvas!');
      break;
    }
  }

  if (!authenticated) {
    console.log('⚠️ Timed out waiting for login. Please ensure you are logged into Google in the open window.');
    return;
  }

  await page.waitForTimeout(4000);

  // Take screenshot of canvas
  const canvasShot = path.join(PROJECT_DIR, `flow_canvas_state.png`);
  await page.screenshot({ path: canvasShot });
  console.log(`📸 Canvas state screenshot saved: ${canvasShot}`);

  async function attemptGeneration(attemptNum = 1) {
    console.log(`\n--- Generation Attempt ${attemptNum} for ${targetFrame} ---`);

    // Locate composer box
    const inputSelectors = [
      'div[contenteditable="true"]',
      'textarea',
      '[role="textbox"]',
      '.tiptap',
      '.ProseMirror',
      '[placeholder*="Describe"]',
      '[placeholder*="prompt"]'
    ];

    let composer = null;
    for (const sel of inputSelectors) {
      const el = await page.$(sel);
      if (el && await el.isVisible()) {
        composer = el;
        console.log(`Found composer matching selector: ${sel}`);
        break;
      }
    }

    if (composer) {
      await composer.click();
      await page.waitForTimeout(500);
      // Select all and clear
      await page.keyboard.press('Control+A');
      await page.keyboard.press('Backspace');
      await page.waitForTimeout(300);
      await page.keyboard.type(fullPrompt, { delay: 5 });
      console.log('Prompt successfully entered into composer.');
    } else {
      console.log('Clicking composer area coordinates...');
      await page.mouse.click(720, 840);
      await page.waitForTimeout(300);
      await page.keyboard.press('Control+A');
      await page.keyboard.press('Backspace');
      await page.keyboard.type(fullPrompt, { delay: 5 });
    }

    await page.waitForTimeout(1000);
    const preCreateShot = path.join(PROJECT_DIR, `flow_pre_create_${targetFrame}.png`);
    await page.screenshot({ path: preCreateShot });
    console.log(`📸 Pre-create screenshot: ${preCreateShot}`);

    // Click Create button (do not press Enter!)
    const createBtnSelectors = [
      'button:has-text("Create")',
      'button[aria-label*="Create"]',
      'button:has(span:has-text("Create"))',
      'button:has(i:has-text("arrow_forward"))',
      'button:has(span:has-text("arrow_forward"))'
    ];

    let clicked = false;
    for (const sel of createBtnSelectors) {
      const btn = await page.$(sel);
      if (btn && await btn.isVisible()) {
        console.log(`Clicking Create button matching: ${sel}`);
        await btn.click();
        clicked = true;
        break;
      }
    }

    if (!clicked) {
      console.log('Trying button search by visible text...');
      const buttons = await page.$$('button');
      for (const btn of buttons) {
        const text = await btn.innerText().catch(() => '');
        if (text.toLowerCase().includes('create') && await btn.isVisible()) {
          console.log(`Clicked button with text "${text}"`);
          await btn.click();
          clicked = true;
          break;
        }
      }
    }

    if (!clicked) {
      console.log('⚠️ Could not locate Create button. Please click Create in the browser window.');
    }

    console.log('⏳ Waiting for render completion (polling 45 seconds)...');
    let renderComplete = false;
    for (let sec = 0; sec < 45; sec += 5) {
      await page.waitForTimeout(5000);
      process.stdout.write(`...${sec + 5}s `);

      // Check for error banner or policy warning
      const errorEl = await page.$('.error-message, [role="alert"], .toast-error');
      if (errorEl && await errorEl.isVisible()) {
        const errText = await errorEl.innerText().catch(() => '');
        console.log(`\n❌ Error / policy block detected: "${errText}"`);
        if (attemptNum < 3) {
          console.log('🔄 Re-rolling with sanitized phrasing...');
          return await attemptGeneration(attemptNum + 1);
        }
      }
    }
    console.log('\n');

    const postGenShot = path.join(PROJECT_DIR, `flow_post_gen_${targetFrame}.png`);
    await page.screenshot({ path: postGenShot });
    console.log(`📸 Post-generation screenshot saved: ${postGenShot}`);

    // Scan for new image elements on canvas
    const imgData = await page.evaluate(() => {
      const imgs = Array.from(document.querySelectorAll('img'));
      return imgs.map(img => ({
        src: img.src,
        width: img.naturalWidth || img.width,
        height: img.naturalHeight || img.height,
        alt: img.alt || ''
      })).filter(img => img.src && (img.src.startsWith('blob:') || img.src.includes('googleusercontent') || img.src.includes('blob')));
    });

    console.log(`Found ${imgData.length} valid rendered image elements on canvas.`);
    
    // Filter out small UI thumbnails or avatars
    const candidates = imgData.filter(i => i.width >= 400 && !i.src.includes('avatar') && !i.src.includes('icon'));
    if (candidates.length > 0) {
      const best = candidates[candidates.length - 1];
      console.log(`🎯 Identified candidate image: ${best.width}x${best.height}`);
      
      const buffer = await page.evaluate(async (src) => {
        try {
          const resp = await fetch(src);
          const blob = await resp.blob();
          const reader = new FileReader();
          return new Promise((resolve) => {
            reader.onloadend = () => resolve(reader.result.split(',')[1]);
            reader.readAsDataURL(blob);
          });
        } catch (e) {
          return null;
        }
      }, best.src);

      if (buffer) {
        const destFile = path.join(PROJECT_DIR, 'storyboard-frames', `${targetFrame}.jpg`);
        fs.writeFileSync(destFile, Buffer.from(buffer, 'base64'));
        console.log(`🎉 SUCCESS: Saved frame ${targetFrame} to ${destFile}`);
      }
    } else {
      console.log('⚠️ Could not automatically extract candidate image. Browser remains open so you can view/download or re-roll directly.');
    }
  }

  await attemptGeneration(1);

  console.log('\n========================================================================');
  console.log('Browser session is active and remains open for your review & control.');
  console.log('========================================================================');
}

main().catch(console.error);
