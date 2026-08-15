const { chromium } = require('playwright');

// Evaluates an arbitrary JS expression string in the page context and prints the JSON result.
// Usage: node cdp_eval.js "document.title"
// Usage: node cdp_eval.js "Array.from(document.querySelectorAll('img')).map(i=>({src:i.src,w:i.naturalWidth}))"
async function main() {
  const expr = process.argv[2];
  if (!expr) { console.error('Usage: node cdp_eval.js "<js expression>"'); process.exit(1); }

  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const ctx = browser.contexts()[0];
  const page = ctx.pages().find(p => p.url().includes('labs.google')) || ctx.pages()[0];

  const result = await page.evaluate(new Function(`return (${expr})`));
  console.log(JSON.stringify(result, null, 2));
  await browser.close();
}

main().catch(err => { console.error('ERROR:', err.message); process.exit(1); });
