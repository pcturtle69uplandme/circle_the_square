const { chromium } = require('playwright');

async function main() {
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const page = browser.contexts()[0].pages().find(p => p.url().includes('labs.google'));
  if (!page) { console.error('No page'); process.exit(1); }

  const state = await page.evaluate(() => {
    const alerts = Array.from(document.querySelectorAll('[role="alert"], [class*="toast"], [class*="error"], [class*="policy"], [class*="banner"]'))
      .map(el => el.innerText.trim())
      .filter(Boolean);

    const media = Array.from(document.querySelectorAll('img[src*="media.getMediaUrlRedirect"]'))
      .map(img => ({ alt: img.alt, src: img.src, w: img.naturalWidth, h: img.naturalHeight }));

    const buttons = Array.from(document.querySelectorAll('button'))
      .map(b => b.innerText.replace(/\n/g, ' ').trim())
      .filter(Boolean);

    return { alerts, mediaCount: media.length, media: media.slice(0, 5), buttons: buttons.slice(0, 10) };
  });

  console.log('Flow Live State:', JSON.stringify(state, null, 2));
  await page.screenshot({ path: 'character-refs/stencils/flow_live_state.png' });
  console.log('Saved character-refs/stencils/flow_live_state.png');
  process.exit(0);
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
