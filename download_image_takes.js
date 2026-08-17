const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

async function main() {
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const page = browser.contexts()[0].pages().find(p => p.url().includes('labs.google'));
  if (!page) { console.error('No page'); process.exit(1); }

  const imageIds = [
    '259de7d9-2936-4b80-8c33-f3568f21e005',
    '4c483c2f-7fb6-4d1f-9cb1-195cdbf12282',
    '5beb66dd-45c7-426c-beda-348dae44dc6f',
    '8c36ec68-ebeb-43c6-8db5-a37f32d5cf58',
    'e8cf8c3e-b395-45ad-ad22-8ddd0e154a3e',
    '7c42bdae-3220-48a6-8869-9f2dfe159b2a',
    '0ae8eea6-ccc0-4fa4-b359-76565db275da',
    '9b627de2-a387-430e-a238-c4c8b1e4ad21',
    'ac19ec93-0db0-4093-9ca8-bcf760a87a9d',
    '3633c86a-d5d0-4acb-abfe-1b8684a05132',
    'bf1cc175-8d6e-4e0f-ac7a-70e7f890c4e7',
    '2a8b83fe-cdfc-41b0-9620-a81fd6d14559',
    '71e181a4-9329-4520-ada7-0f6175ae9969',
    '70e2d9cd-3b16-4b5c-86cb-ea73bfdca78e',
    '27b6105c-3fdf-458f-9942-162b53945976',
    '5193de96-98b8-48d8-8b2f-617c682d294d',
    '517bbbe6-73bb-4657-9061-6f29c602f265',
    'acf36e9f-da8a-4941-9106-a2a013c3effd',
    'f0c839e8-fd43-4593-a329-9825d934bf7f',
    'aac70885-32d1-4d4e-a0ad-6a5b0f6a0a62',
    'd7c8b023-3f05-4734-81d1-cc12f3b08d4a'
  ];

  console.log(`Downloading ${imageIds.length} candidate image takes...`);
  for (let i = 0; i < imageIds.length; i++) {
    const id = imageIds[i];
    const url = `https://labs.google/fx/api/trpc/media.getMediaUrlRedirect?name=${id}`;
    try {
      const base64 = await page.evaluate(async (u) => {
        const resp = await fetch(u);
        const buf = await resp.arrayBuffer();
        let binary = '';
        const bytes = new Uint8Array(buf);
        for (let j = 0; j < bytes.byteLength; j++) { binary += String.fromCharCode(bytes[j]); }
        return btoa(binary);
      }, url);

      const outPath = path.resolve('character-refs', 'stencils', `flow_cand_${i}_${id.substring(0, 8)}.jpg`);
      fs.writeFileSync(outPath, Buffer.from(base64, 'base64'));
      console.log(`[${i}] Saved ${id.substring(0, 8)} (${fs.statSync(outPath).size} bytes)`);
    } catch (e) {
      console.error(`Error downloading ${id}:`, e.message);
    }
  }

  process.exit(0);
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
