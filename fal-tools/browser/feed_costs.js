// Report the real duration and charge for recent generations, straight off the feed.
//
//   node feed_costs.js [n]
//
// Exists because the per-second rate could not be inferred reliably from balance deltas:
// an early 5s clip showed $0.100 while a later run showed $1.300, so the effective rate
// is not the flat $0.02/sec that a single observation suggested. fal prints the actual
// charge against each generation; read that rather than guessing.
const { chromium } = require('playwright');

(async () => {
  const n = Number(process.argv[2] || 6);
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9333');
  const page = browser.contexts()[0].pages().find(p => p.url().includes('fal.ai'));

  const out = await page.evaluate((count) => {
    const text = document.body.innerText;
    const balance = (text.match(/Credits:\s*\$([0-9.]+)/) || [])[1] || null;
    const blocks = text.split('Image To Video').slice(1, count + 1);
    const rows = blocks.map((s) => ({
      age: (s.match(/([0-9]+ (?:second|minute|hour|day)s? ago)/) || [])[1] || null,
      duration: (s.match(/Duration:\s*([0-9]+)/) || [])[1] || null,
      cost: (s.match(/Total Cost:\s*\$([0-9.]+)/) || [])[1] || null,
      prompt: (s.match(/Prompt\s*\n([^\n]{0,70})/) || [])[1] || '',
    }));
    return { balance, rows };
  }, n);

  console.log(`balance: $${out.balance}`);
  console.log('age'.padEnd(18) + 'dur'.padEnd(6) + 'cost'.padEnd(10) + '$/sec');
  let total = 0;
  for (const r of out.rows) {
    const d = Number(r.duration), c = Number(r.cost);
    if (r.cost) total += c;
    const rate = d && c ? (c / d).toFixed(3) : '-';
    console.log(
      String(r.age || '?').padEnd(18) +
      String(r.duration ? r.duration + 's' : '?').padEnd(6) +
      String(r.cost ? '$' + r.cost : '?').padEnd(10) +
      rate
    );
  }
  console.log(`\nlisted total: $${total.toFixed(3)}`);
  await browser.close();
})().catch(e => { console.error('ERROR:', e.message); process.exit(1); });
