const { chromium } = require('playwright');

async function main() {
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const page = browser.contexts()[0].pages().find(p => p.url().includes('labs.google'));
  if (!page) { console.error('No page'); process.exit(1); }

  const barButtons = await page.evaluate(() => {
    const btns = Array.from(document.querySelectorAll('button, [role="button"]'));
    return btns.map((b, i) => {
      const r = b.getBoundingClientRect();
      return {
        i,
        text: b.innerText.replace(/\n/g, ' ').trim(),
        aria: b.getAttribute('aria-label') || '',
        rect: { x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height) }
      };
    }).filter(b => b.rect.y > 800);
  });

  console.log('Bar buttons at y > 800:', JSON.stringify(barButtons, null, 2));

  // If there is an arrow_forward or Create button, click it
  const target = barButtons.find(b => b.text.includes('arrow_forward') || b.text.includes('Create') || b.aria.includes('Create'));
  if (target) {
    console.log(`Clicking target button: ${target.text} at (${target.rect.x + target.rect.w/2}, ${target.rect.y + target.rect.h/2})...`);
    await page.mouse.click(target.rect.x + target.rect.w / 2, target.rect.y + target.rect.h / 2);
    await page.waitForTimeout(2000);
  }

  await page.screenshot({ path: 'character-refs/stencils/flow_after_target_click.png' });
  console.log('Saved flow_after_target_click.png');
  process.exit(0);
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
