const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

async function main() {
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const ctx = browser.contexts()[0];
  const page = ctx.pages().find(p => p.url().includes('labs.google'));
  if (!page) {
    console.error('Flow page not found');
    process.exit(1);
  }

  console.log('Inspecting Flow project URL:', page.url());

  // Click on the Characters tab if visible, or inspect all assets in DOM
  const textMatches = await page.evaluate(() => {
    const all = Array.from(document.querySelectorAll('*'));
    const matches = [];
    all.forEach(el => {
      if (el.children.length === 0 && el.innerText) {
        const t = el.innerText.trim();
        if (t.includes('Jan') || t.includes('Christina') || t.includes('Sharon') || t.includes('Rick') || t.includes('Chris') || t.includes('Characters') || t.includes('Uploads') || t.includes('Ingredients')) {
          matches.push({ tag: el.tagName, text: t, parent: el.parentElement ? el.parentElement.tagName : '' });
        }
      }
    });
    return matches;
  });

  console.log(`Found ${textMatches.length} text matches in Flow DOM:`);
  textMatches.slice(0, 20).forEach((m, i) => console.log(` [${i}] <${m.tag}> ${m.text}`));
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
