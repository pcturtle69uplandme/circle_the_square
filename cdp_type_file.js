const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

// Type the contents of a file into Flow's composer.
//   node cdp_type_file.js prompts/L5-A.txt [out.png]
//
// Uses fill-then-verify rather than keystroke simulation: the prompts run to ~2000
// characters and Flow's composer is a contenteditable that intermittently drops or
// reorders fast synthetic keystrokes. Also refuses to type a literal "@", which opens
// the mention picker and silently swallows the rest of the prompt.
async function main() {
  const file = process.argv[2];
  const outFile = process.argv[3];
  if (!file) throw new Error('usage: cdp_type_file.js <file> [out.png]');
  const text = fs.readFileSync(path.resolve(file), 'utf8').trim();
  if (text.includes('@')) throw new Error('prompt contains "@" — it will hijack the composer');

  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const ctx = browser.contexts()[0];
  const page = ctx.pages().find(p => p.url().includes(process.env.FLOW_TAB || 'labs.google'))
    || ctx.pages()[0];

  const sel = ['textarea', '[contenteditable="true"]', '.ProseMirror'];
  let box = null, used = null;
  for (const s of sel) {
    const el = await page.$(s);
    if (el) {
      const b = await el.boundingBox();
      if (b && b.width > 200) { box = b; used = s; break; }
    }
  }
  if (!box) throw new Error('composer input not found');

  await page.mouse.click(box.x + box.width / 2, box.y + box.height / 2);
  await page.waitForTimeout(300);
  await page.keyboard.press('Control+A');
  await page.keyboard.press('Backspace');
  await page.waitForTimeout(200);

  // Type in chunks so a stall is visible rather than silently truncating.
  const CHUNK = 400;
  for (let i = 0; i < text.length; i += CHUNK) {
    await page.keyboard.insertText(text.slice(i, i + CHUNK));
    await page.waitForTimeout(120);
  }
  await page.waitForTimeout(600);

  const got = await page.evaluate((s) => {
    const el = document.querySelector(s);
    return (el.value !== undefined ? el.value : el.innerText) || '';
  }, used);

  console.log(`selector: ${used}`);
  console.log(`wanted ${text.length} chars, composer has ${got.trim().length}`);
  console.log(got.trim().length === text.length ? 'OK — exact match' : 'MISMATCH — check before generating');

  if (outFile) {
    await page.screenshot({ path: path.resolve(__dirname, outFile) });
    console.log('saved', outFile);
  }
  await browser.close();
}

main().catch(err => { console.error('ERROR:', err.message); process.exit(1); });
