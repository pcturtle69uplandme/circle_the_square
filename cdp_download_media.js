const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

/**
 * Download a Flow media asset straight to disk.
 *
 *   node cdp_download_media.js <out.mp4> [videoIndex]
 *   node cdp_download_media.js <out.mp4> --url <mediaUrl>
 *
 * Fetches inside the page so the session cookies apply, then transfers the bytes as
 * base64 and writes them here. This bypasses Chrome's download manager entirely, which
 * scans Flow's blob downloads for malware and deletes them before they reach Downloads\
 * (see .agents/rules/browser_automation_cdp.md).
 */
async function main() {
  const outFile = process.argv[2];
  if (!outFile) throw new Error('usage: cdp_download_media.js <out.mp4> [index|--url <u>]');
  const urlFlag = process.argv.indexOf('--url');
  const idx = urlFlag === -1 ? Number(process.argv[3] || 0) : null;

  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const ctx = browser.contexts()[0];
  const page = ctx.pages().find(p => p.url().includes(process.env.FLOW_TAB || 'labs.google')) || ctx.pages()[0];

  let url = urlFlag !== -1 ? process.argv[urlFlag + 1] : await page.evaluate((i) => {
    const v = document.querySelectorAll('video')[i];
    return v ? (v.src || v.currentSrc) : null;
  }, idx);
  if (!url) throw new Error('no video element / url found');
  console.log('source:', url.slice(0, 90));

  // Playwright's request context shares the page's cookies but is not subject to CORS,
  // which an in-page fetch() is — the media URL 302s to a different origin and the
  // browser blocks reading that response.
  const resp = await ctx.request.get(url, { headers: { referer: page.url() } });
  if (!resp.ok()) throw new Error(`request failed ${resp.status()}`);
  const body = await resp.body();

  const out = path.resolve(outFile);
  fs.mkdirSync(path.dirname(out), { recursive: true });
  fs.writeFileSync(out, body);
  console.log(`wrote ${out}  ${(fs.statSync(out).size / 1048576).toFixed(2)} MB`);
  await browser.close();
}

main().catch(err => { console.error('ERROR:', err.message); process.exit(1); });
