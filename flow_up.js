// Ensure a CDP-controllable Chrome is running on port 9223 for Google Flow, detached
// from this node process (same pattern as higgsfield-tools/browser/hf_up.js, so a
// killed background task doesn't take the browser down with it -- that bug cost two
// Scene 2 batches earlier in this project when launchPersistentContext was used
// instead). Separate port (9223) from the Higgsfield Chrome (9222) so both can run
// side by side. Reuses the existing Flow profile at C:\ai\.chrome_playwright_profile.
//
//   node flow_up.js [url]
//
// Exits as soon as the endpoint answers and the window is visible -- log in manually
// with the pcturtle69uplandme@gmail.com Google account in the opened window, then
// hand back to automation.
const { spawn } = require('child_process');
const http = require('http');

const PORT = 9223;
const PROFILE = 'C:\\ai\\.chrome_playwright_profile';
const URL = process.argv[2] || 'https://labs.google/fx/tools/flow';
const CHROME = process.env.CHROME_PATH ||
  'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';

const alive = () => new Promise((resolve) => {
  const req = http.get({ host: '127.0.0.1', port: PORT, path: '/json/version', timeout: 2500 },
    (res) => { res.resume(); resolve(res.statusCode === 200); });
  req.on('error', () => resolve(false));
  req.on('timeout', () => { req.destroy(); resolve(false); });
});

const sleep = (ms) => new Promise(r => setTimeout(r, ms));

(async () => {
  if (await alive()) return console.log(`chrome already up on ${PORT}`);

  const child = spawn(CHROME, [
    `--remote-debugging-port=${PORT}`,
    `--user-data-dir=${PROFILE}`,
    '--disable-blink-features=AutomationControlled',
    '--no-first-run',
    '--no-default-browser-check',
    '--window-size=1600,1000',
    URL,
  ], { detached: true, stdio: 'ignore' });
  child.unref();

  for (let i = 0; i < 40; i++) {
    await sleep(1000);
    if (await alive()) return console.log(`chrome up on ${PORT} (detached pid ${child.pid})`);
  }
  console.error(`chrome did not expose CDP on ${PORT} within 40s`);
  process.exit(1);
})();
