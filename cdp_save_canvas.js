const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

// Extracts the main editor <canvas> pixel content directly (bypasses Chrome's download
// manager entirely, which has been auto-deleting Flow's blob downloads after malware scan).
// Usage: node cdp_save_canvas.js <output_path.png> [canvas_index]
async function main() {
  const outPath = process.argv[2];
  const idx = Number(process.argv[3] || 0);
  if (!outPath) { console.error('Usage: node cdp_save_canvas.js <output.png> [canvas_index]'); process.exit(1); }

  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const ctx = browser.contexts()[0];
  const page = ctx.pages().find(p => p.url().includes(process.env.FLOW_TAB || 'labs.google') && !p.url().includes('chrome://')) || ctx.pages()[0];
  console.log('Using page:', page.url());

  const dataUrl = await page.evaluate((i) => {
    const canvases = document.querySelectorAll('canvas');
    if (!canvases[i]) throw new Error(`No canvas at index ${i}, found ${canvases.length}`);
    return canvases[i].toDataURL('image/png');
  }, idx);

  const base64 = dataUrl.replace(/^data:image\/png;base64,/, '');
  const buffer = Buffer.from(base64, 'base64');
  fs.writeFileSync(outPath, buffer);
  console.log(`Saved canvas[${idx}] (${buffer.length} bytes) to ${outPath}`);
  await browser.close();
}

main().catch(err => { console.error('ERROR:', err.message); process.exit(1); });
