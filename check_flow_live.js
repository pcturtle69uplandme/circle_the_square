const { chromium } = require('playwright');
const fs = require('fs');

async function main() {
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const page = browser.contexts()[0].pages().find(p => p.url().includes('labs.google'));
  if (!page) {
    console.error('Flow page not found');
    process.exit(1);
  }

  const domInfo = await page.evaluate(() => {
    const alerts = Array.from(document.querySelectorAll('[role="alert"], [class*="toast"], [class*="error"], [class*="policy"]'))
      .map(el => el.innerText.trim())
      .filter(Boolean);

    const media = Array.from(document.querySelectorAll('img[src*="media.getMediaUrlRedirect"], img[src*="labs.google"], img[src*="googleusercontent"]'))
      .map(img => ({ src: img.src, alt: img.alt, width: img.naturalWidth, height: img.naturalHeight }));

    const buttons = Array.from(document.querySelectorAll('button'))
      .map(b => b.innerText.trim())
      .filter(Boolean);

    return { alerts, mediaCount: media.length, media: media.slice(-4), buttons: buttons.slice(0, 15) };
  });

  console.log('DOM Info:', JSON.stringify(domInfo, null, 2));
  await page.screenshot({ path: 'character-refs/stencils/flow_f19_live.png' });
  console.log('Saved character-refs/stencils/flow_f19_live.png');
  process.exit(0);
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
