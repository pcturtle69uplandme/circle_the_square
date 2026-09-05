// The fal REST API (submit/status/result) never returns a cost field -- confirmed by
// inspecting all three response shapes. The only place the actual billed amount shows up
// is this dashboard request-detail page. This is read-only: it does not submit or drive
// any generation, just reads back what a completed request cost.
//
//   node get_request_cost.js <endpoint-id> <request-id>
//   e.g. node get_request_cost.js fal-ai/minimax-h3-turbo/image-to-video 01a070b1-dad1-7623-ab7f-05e6174b6002
//
// Requires the port-9333 fal.ai Chrome profile to already be up and logged in (fal_up.js).

const { chromium } = require('playwright');

async function main() {
  const [endpoint, requestId] = process.argv.slice(2);
  if (!endpoint || !requestId) {
    console.error('Usage: node get_request_cost.js <endpoint-id> <request-id>');
    process.exit(1);
  }

  const browser = await chromium.connectOverCDP('http://127.0.0.1:9333');
  const page = browser.contexts()[0].pages().find(p => p.url().includes('fal.ai')) || browser.contexts()[0].pages()[0];

  await page.goto(`https://fal.ai/models/${endpoint}/requests/${requestId}`, { waitUntil: 'domcontentloaded', timeout: 45000 });
  await page.waitForTimeout(2500);

  if (page.url().includes('/login')) {
    console.error('Not logged in to fal.ai in the port-9333 Chrome profile. Sign in by hand in that window and re-run.');
    await browser.close();
    process.exit(1);
  }

  const text = await page.evaluate(() => document.body.innerText);
  const cost = (text.match(/Cost\s*\n?\$([0-9.]+)/) || [])[1];
  const duration = (text.match(/Duration\s*\n?([0-9.]+)s/) || [])[1];
  const status = (text.match(/Status\s*\n?(\d+)/) || [])[1];

  if (!cost) {
    console.error('Could not find a Cost field on the request page -- it may still be processing, or fal changed the page layout.');
    await browser.close();
    process.exit(1);
  }

  console.log(JSON.stringify({ requestId, status, executionSeconds: duration, cost: `$${cost}` }, null, 2));
  await browser.close();
}

main().catch((e) => { console.error('ERROR:', e.message); process.exit(1); });
