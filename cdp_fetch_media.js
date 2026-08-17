const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

// Pull a Flow media asset at full resolution straight out of the page's
// authenticated session, bypassing Chrome's download manager entirely
// (its malware scan silently deletes Flow's blob downloads — see
// .agents/rules/browser_automation_cdp.md). Unlike cdp_save_canvas.js this
// gets the real asset, not the on-screen display buffer.
//
// Usage: node cdp_fetch_media.js <mediaId> <out.jpg>
async function main() {
  const mediaId = process.argv[2];
  const outFile = process.argv[3];
  if (!mediaId || !outFile) {
    console.error('Usage: node cdp_fetch_media.js <mediaId> <out.jpg>');
    process.exit(1);
  }

  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const ctx = browser.contexts()[0];
  const page = ctx.pages().find(p => p.url().includes(process.env.FLOW_TAB || 'labs.google')) || ctx.pages()[0];

  const b64 = await page.evaluate(async (id) => {
    const res = await fetch(`https://labs.google/fx/api/trpc/media.getMediaUrlRedirect?name=${id}`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const buf = new Uint8Array(await res.arrayBuffer());
    let s = '';
    for (let i = 0; i < buf.length; i += 0x8000) {
      s += String.fromCharCode.apply(null, buf.subarray(i, i + 0x8000));
    }
    return btoa(s);
  }, mediaId);

  const out = path.resolve(__dirname, outFile);
  fs.mkdirSync(path.dirname(out), { recursive: true });
  fs.writeFileSync(out, Buffer.from(b64, 'base64'));
  console.log(`Wrote ${out} (${fs.statSync(out).size} bytes)`);
  await browser.close();
}

main().catch(err => { console.error('ERROR:', err.message); process.exit(1); });
