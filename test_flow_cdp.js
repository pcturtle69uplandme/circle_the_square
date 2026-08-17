const { chromium } = require('playwright');

async function testConnection() {
  try {
    console.log('Attempting to connect to Chrome over CDP on port 9222...');
    const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
    console.log('Connected to Chrome via CDP successfully!');
    const contexts = browser.contexts();
    console.log(`Found ${contexts.length} browser contexts.`);
    for (const ctx of contexts) {
      const pages = ctx.pages();
      console.log(`Context has ${pages.length} open pages:`);
      for (const p of pages) {
        console.log(` - ${p.url()} (${await p.title()})`);
      }
    }
  } catch (err) {
    console.log('CDP connection failed:', err.message);
  }
}

testConnection();
