// Drive one Google Flow still generation end-to-end via CDP: upload a fresh reference
// image (the "Recent" panel is not stable -- items drop out as new ones are added, so
// searching it by name is unreliable), type the prompt, submit, poll for the newest
// generated image, download it. Mirrors higgsfield-tools/browser/run_shot.js's role but
// for Flow's Nano Banana Pro (free tier) instead of Higgsfield.
//
//   node flow_generate.js <local-reference-image-path> <prompt-json-file> <output-png-path>
//
// prompt-json-file: a JSON file containing { "prompt": "..." } -- passed as a file to
// avoid shell-escaping a long prompt with quotes/dashes.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const PORT = 9223;
const sleep = (ms) => new Promise(r => setTimeout(r, ms));

async function main() {
  const [refImage, promptFile, outPath] = process.argv.slice(2);
  if (!refImage || !promptFile || !outPath) {
    console.error('Usage: node flow_generate.js <local-reference-image-path> <prompt-json-file> <output-png-path>');
    process.exit(1);
  }
  const { prompt } = JSON.parse(fs.readFileSync(promptFile, 'utf8'));

  const browser = await chromium.connectOverCDP(`http://127.0.0.1:${PORT}`);
  const ctx = browser.contexts()[0];
  const page = ctx.pages().find(p => p.url().includes('flow.google.com')) || ctx.pages()[0];

  // Record every large generated-image URL currently on the page, so we can tell which
  // one is new after submitting.
  const before = new Set(await page.evaluate(() =>
    Array.from(document.querySelectorAll('img')).map(i => i.currentSrc || i.src).filter(Boolean)));

  await page.keyboard.press('Escape').catch(() => {});
  await page.waitForTimeout(400);

  // Open the reference picker and upload the reference image fresh.
  const addBtns = page.locator('button:has-text("add")');
  await addBtns.last().click();
  await page.waitForTimeout(800);
  const uploadBtn = page.locator('.cdk-overlay-container button.sidebar-upload-btn');
  const [chooser] = await Promise.all([
    page.waitForEvent('filechooser', { timeout: 10000 }),
    uploadBtn.first().click(),
  ]);
  await chooser.setFiles([path.resolve(refImage)]);
  // Wait for the upload to finish (its asset-item stops saying "Uploading").
  for (let i = 0; i < 15; i++) {
    const items = await page.evaluate(() => Array.from(document.querySelectorAll('.asset-item')).map(e => (e.innerText || '').trim()));
    if (!items.some((t) => t.startsWith('Uploading'))) break;
    await sleep(1500);
  }
  // The freshly uploaded asset is always item 0 (most recent).
  await page.locator('.asset-item').nth(0).click();
  await page.waitForTimeout(400);
  await page.locator('.detail-add-to-prompt-btn').first().click();
  await page.waitForTimeout(600);

  // Type the prompt.
  const composer = page.locator('[contenteditable="true"], textarea').first();
  await composer.click({ position: { x: 10, y: 10 }, force: true });
  await page.keyboard.press('Control+A');
  await page.keyboard.press('Backspace');
  await page.keyboard.type(prompt, { delay: 2 });
  await page.waitForTimeout(500);

  // Submit.
  await page.locator('button', { hasText: 'arrow_forward' }).last().click();
  console.log('submitted, waiting for render...');

  // Poll for a new large image.
  let found = null;
  for (let i = 0; i < 24; i++) {
    await sleep(5000);
    const imgs = await page.evaluate(() =>
      Array.from(document.querySelectorAll('img')).map(i => ({ src: i.currentSrc || i.src, w: i.naturalWidth }))
        .filter(i => i.w > 500));
    const fresh = imgs.find(i => !before.has(i.src));
    if (fresh) { found = fresh.src; break; }
    console.log(`  waiting... (${i + 1})`);
  }
  if (!found) throw new Error('timed out waiting for a new generated image');

  const b64 = await page.evaluate(async (u) => {
    const r = await fetch(u);
    if (!r.ok) throw new Error('HTTP ' + r.status);
    const bytes = new Uint8Array(await r.arrayBuffer());
    let s = ''; const CH = 0x8000;
    for (let k = 0; k < bytes.length; k += CH) s += String.fromCharCode.apply(null, bytes.subarray(k, k + CH));
    return btoa(s);
  }, found);
  fs.mkdirSync(path.dirname(outPath), { recursive: true });
  fs.writeFileSync(outPath, Buffer.from(b64, 'base64'));
  console.log(`SAVED ${outPath} (${fs.statSync(outPath).size} bytes) from ${found}`);

  await browser.close();
}

main().catch((e) => { console.error('ERROR:', e.message); process.exit(1); });
