// Pull finished generations off the Higgsfield feed and save them as full-res PNGs.
//
// The in-app Download button does not raise a download event in this Playwright
// profile (confirmed on the laptop session too), so instead we read the <img> src
// off the feed and fetch the CDN original directly. Feed thumbnails are served as
// "<name>_min.webp"; stripping that suffix back to ".png" yields the full-res
// original on the same CloudFront host. The images.higgs.ai proxy URL does NOT
// work for this -- it only serves the resized derivative.
//
//   node hf_grab.js list [n]              print the newest n feed image URLs
//   node hf_grab.js save <index> <out>    save feed image #index (0 = newest)
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const CDN = 'd8j0ntlcm91z4.cloudfront.net';

// Feed order is newest-first. Keep only real generation assets on the CDN host --
// avatars, preset thumbnails and marketing art live elsewhere and would shift the
// index out from under the caller.
async function feedUrls(page) {
  return page.evaluate((cdn) => {
    const seen = new Set();
    return Array.from(document.querySelectorAll('img'))
      .map(i => i.currentSrc || i.src || '')
      .filter(u => u.includes(cdn) && /user_/.test(u))
      .filter(u => (seen.has(u) ? false : (seen.add(u), true)));
  }, CDN);
}

// Feed <img> srcs come wrapped in the resizing proxy:
//   https://images.higgs.ai/?...&url=<url-encoded CDN url>&w=640&q=85
// Unwrap to the embedded CloudFront URL, then turn the "_min.webp" derivative back
// into the full-res ".png" original. Bare CDN URLs pass through unchanged.
function toFullRes(u) {
  const m = u.match(/[?&]url=([^&]+)/);
  if (m) u = decodeURIComponent(m[1]);
  return u.replace(/_min\.webp$/, '.png').replace(/\.webp$/, '.png');
}

async function main() {
  const [cmd, ...args] = process.argv.slice(2);
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const ctx = browser.contexts()[0];
  const page = ctx.pages().find(p => p.url().includes('higgsfield')) || ctx.pages()[0];

  const urls = (await feedUrls(page)).map(toFullRes);

  if (cmd === 'list') {
    urls.slice(0, Number(args[0] || 8)).forEach((u, i) => console.log(i + '  ' + u));
  } else if (cmd === 'save') {
    const idx = Number(args[0]);
    const dest = args[1];
    const url = urls[idx];
    if (!url) throw new Error(`no feed image at index ${idx} (found ${urls.length})`);
    // Fetch from inside the page so the request carries the session cookies the
    // CDN checks; a bare curl from the shell gets a 403 on some assets.
    const b64 = await page.evaluate(async (u) => {
      const r = await fetch(u);
      if (!r.ok) throw new Error('HTTP ' + r.status);
      const buf = await r.arrayBuffer();
      let s = '';
      const bytes = new Uint8Array(buf);
      const CH = 0x8000;
      for (let i = 0; i < bytes.length; i += CH) {
        s += String.fromCharCode.apply(null, bytes.subarray(i, i + CH));
      }
      return btoa(s);
    }, url);
    fs.mkdirSync(path.dirname(dest), { recursive: true });
    fs.writeFileSync(dest, Buffer.from(b64, 'base64'));
    console.log(`saved ${dest} (${fs.statSync(dest).size} bytes) from ${url}`);
  } else {
    throw new Error('usage: hf_grab.js list [n] | save <index> <out>');
  }
  await browser.close();
}

main().catch(e => { console.error('ERROR:', e.message); process.exit(1); });
