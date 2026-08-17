const { chromium } = require('playwright');

async function main() {
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const page = browser.contexts()[0].pages().find(p => p.url().includes('labs.google'));
  if (!page) { console.error('No page'); process.exit(1); }

  const textboxes = await page.evaluate(() => {
    const els = Array.from(document.querySelectorAll('[contenteditable="true"], textarea, input, [role="textbox"], [role="combobox"]'));
    return els.map((el, i) => {
      const rect = el.getBoundingClientRect();
      return {
        index: i,
        tag: el.tagName,
        role: el.getAttribute('role'),
        contenteditable: el.getAttribute('contenteditable'),
        placeholder: el.getAttribute('placeholder') || el.innerText.substring(0, 30),
        className: el.className,
        id: el.id,
        rect: { x: rect.x, y: rect.y, w: rect.width, h: rect.height },
        visible: rect.width > 0 && rect.height > 0
      };
    });
  });

  console.log('Visible inputs/textboxes:', JSON.stringify(textboxes.filter(t => t.visible), null, 2));
  process.exit(0);
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
