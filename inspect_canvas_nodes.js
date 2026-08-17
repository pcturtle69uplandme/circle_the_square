const { chromium } = require('playwright');
const fs = require('fs');

async function main() {
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const page = browser.contexts()[0].pages().find(p => p.url().includes('labs.google'));
  if (!page) { console.error('No page'); process.exit(1); }

  // Inspect the canvas nodes and cards
  const canvasInfo = await page.evaluate(() => {
    const cards = Array.from(document.querySelectorAll('[data-node-id], .react-flow__node, [class*="node"], [class*="card"], [class*="item"]'))
      .map(el => ({
        tag: el.tagName,
        className: el.className,
        text: el.innerText ? el.innerText.substring(0, 80).replace(/\n/g, ' ') : ''
      }));

    const generatingSpinners = Array.from(document.querySelectorAll('[class*="spinner"], [class*="loading"], [role="progressbar"]'))
      .map(el => el.className);

    return { cardCount: cards.length, cards: cards.slice(0, 15), generatingSpinners };
  });

  console.log('Canvas Info:', JSON.stringify(canvasInfo, null, 2));
  await page.screenshot({ path: 'character-refs/stencils/flow_canvas_state.png' });
  console.log('Saved flow_canvas_state.png');
  process.exit(0);
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
