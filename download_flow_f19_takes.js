const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

async function main() {
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const page = browser.contexts()[0].pages().find(p => p.url().includes('labs.google'));
  if (!page) { console.error('No page'); process.exit(1); }

  // Extract all media items from the project
  const mediaList = await page.evaluate(async () => {
    const images = Array.from(document.querySelectorAll('img[src*="media.getMediaUrlRedirect"]'));
    const items = [];
    for (const img of images) {
      const parent = img.closest('[role="button"], div, button');
      const label = parent ? parent.innerText : img.alt || '';
      items.push({ src: img.src, label: label.replace(/\n/g, ' ').trim() });
    }
    return items;
  });

  console.log(`Found ${mediaList.length} media items in project.`);
  const f19Matches = mediaList.filter(m => m.label.toLowerCase().includes('f19') || m.label.toLowerCase().includes('shirt') || m.label.toLowerCase().includes('dropping'));
  console.log('F19 candidates:', JSON.stringify(f19Matches, null, 2));

  // Download candidate takes
  let idx = 0;
  for (const item of f19Matches) {
    console.log(`Downloading candidate ${idx}: ${item.label}...`);
    const base64 = await page.evaluate(async (url) => {
      const resp = await fetch(url);
      const buf = await resp.arrayBuffer();
      let binary = '';
      const bytes = new Uint8Array(buf);
      for (let i = 0; i < bytes.byteLength; i++) { binary += String.fromCharCode(bytes[i]); }
      return btoa(binary);
    }, item.src);

    const outPath = path.resolve('storyboard-frames', `F19_flow_candidate_${idx}.jpg`);
    fs.writeFileSync(outPath, Buffer.from(base64, 'base64'));
    console.log(`Saved candidate ${idx} to ${outPath} (${fs.statSync(outPath).size} bytes)`);
    idx++;
  }

  process.exit(0);
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
