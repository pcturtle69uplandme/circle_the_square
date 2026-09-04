// Ensure a CDP-controllable Chrome is running on port 9222, and DON'T die with us.
//
//   node hf_up.js [url]
//
// Why this exists instead of hf_launch.js: launchPersistentContext ties the browser's
// lifetime to the node process that started it, so the launcher has to block forever.
// That makes it a long-lived background task, and when those get cleaned up the
// browser goes with them -- which killed two Scene 2 batches mid-run. Spawning
// chrome.exe detached with its own --remote-debugging-port leaves a browser that
// outlives this script, so run_shot.js can just connectOverCDP to it whenever.
//
// Exits as soon as the endpoint answers, so it is safe to call before every batch.
const { spawn } = require('child_process');
const http = require('http');
const path = require('path');

const PORT = 9222;
const PROFILE = path.resolve(__dirname, '..', '..', 'ai.chrome_playwright_profile');
const URL = process.argv[2] || 'https://higgsfield.ai/ai/image?model=nano-banana-2';
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
