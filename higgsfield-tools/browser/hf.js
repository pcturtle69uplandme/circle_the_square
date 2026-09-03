// One-shot CDP driver for Higgsfield's web UI. Connects to the Chrome started by
// hf_launch.js, does ONE thing, screenshots, exits. Consolidates the cdp_*.js zoo
// (see .agents/rules/browser_automation_cdp.md) into subcommands.
//
// IMPORTANT: every coordinate is a CSS pixel (getBoundingClientRect space), NOT a
// screenshot pixel. Screenshots are devicePixelRatio times bigger. Use `viewport`
// to get the dpr, or `eval` to pull real coords off the DOM.
//
//   node hf.js shot [out.png]
//   node hf.js goto <url> [out.png]
//   node hf.js text [maxChars]              page innerText
//   node hf.js click "<text>" [out.png]     first visible element containing text
//   node hf.js coord <x> <y> [out.png]      click CSS-pixel coord
//   node hf.js type "<text>" [out.png]      focus composer, select-all, type
//   node hf.js key <Key> [out.png]          e.g. Escape
//   node hf.js eval "<js expr>"             run JS, print JSON
//   node hf.js viewport                     {vw, vh, dpr}
//   node hf.js upload <x> <y> <fileA;fileB>  click a control, feed its file chooser
//   node hf.js grab <x> <y> <outPath>       click, capture the download via CDP
const { chromium } = require('playwright');
const path = require('path');

const SHOTS = path.join(__dirname, 'shots');
const MATCH = process.env.HF_URL_MATCH || 'higgsfield';

const out = (f) => (path.isAbsolute(f) ? f : path.join(SHOTS, f));

async function main() {
  const [cmd, ...args] = process.argv.slice(2);
  if (!cmd) throw new Error('no subcommand — see header of this file');

  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const ctx = browser.contexts()[0];
  const pages = ctx.pages();
  const page = pages.find(p => p.url().includes(MATCH)) || pages[0];
  console.log('page:', page.url());

  let shot = null;

  switch (cmd) {
    case 'shot':
      shot = args[0] || 'hf_shot.png';
      break;

    case 'goto':
      await page.goto(args[0], { waitUntil: 'domcontentloaded', timeout: 60000 });
      await page.waitForTimeout(2500);
      shot = args[1] || 'hf_shot.png';
      break;

    case 'text': {
      const max = parseInt(args[0] || '6000', 10);
      const t = await page.evaluate(() => document.body.innerText);
      console.log(t.replace(/\n{3,}/g, '\n\n').slice(0, max));
      break;
    }

    case 'click': {
      const target = args[0];
      const loc = page.locator(`text=${JSON.stringify(target)}`).first();
      await loc.scrollIntoViewIfNeeded({ timeout: 10000 }).catch(() => {});
      await loc.click({ timeout: 15000 });
      await page.waitForTimeout(1500);
      shot = args[1] || 'hf_shot.png';
      break;
    }

    case 'coord':
      await page.mouse.click(Number(args[0]), Number(args[1]));
      await page.waitForTimeout(1500);
      shot = args[2] || 'hf_shot.png';
      break;

    case 'type': {
      const text = args[0];
      // Composer selectors drift; try the usual suspects in order.
      const sels = ['textarea', '[contenteditable="true"]', '.ProseMirror', 'input[type="text"]'];
      let done = false;
      for (const s of sels) {
        const el = page.locator(s).first();
        if (await el.count() && await el.isVisible().catch(() => false)) {
          await el.click();
          await page.keyboard.press('Control+A');
          await page.keyboard.press('Backspace');
          await page.keyboard.type(text, { delay: 12 });
          console.log('typed into:', s);
          done = true;
          break;
        }
      }
      if (!done) throw new Error('no visible composer found — screenshot and use `coord` instead');
      await page.waitForTimeout(800);
      shot = args[1] || 'hf_shot.png';
      break;
    }

    case 'key':
      await page.keyboard.press(args[0]);
      await page.waitForTimeout(1200);
      shot = args[1] || 'hf_shot.png';
      break;

    case 'eval': {
      const r = await page.evaluate(`(() => (${args[0]}))()`);
      console.log(JSON.stringify(r, null, 2));
      break;
    }

    case 'viewport': {
      const r = await page.evaluate(() => ({
        vw: window.innerWidth, vh: window.innerHeight, dpr: window.devicePixelRatio
      }));
      console.log(JSON.stringify(r));
      break;
    }

    case 'upload': {
      // Click a coord that opens a native file chooser and feed it the file directly --
      // a real picker dialog can't be seen or clicked. Same trick as ../../cdp_upload.js.
      const fc = page.waitForEvent('filechooser', { timeout: 30000 });
      await page.mouse.click(Number(args[0]), Number(args[1]));
      const chooser = await fc;
      // Semicolon-separated for controls that take several files (character training).
      const files = args[2].split(';').map(f => f.trim()).filter(Boolean);
      await chooser.setFiles(files);
      await page.waitForTimeout(2500);
      console.log('uploaded ' + files.length + ' file(s)');
      shot = args[3] || 'hf_shot.png';
      break;
    }

    case 'setfiles': {
      // Feed an <input type=file> directly by index. More reliable than clicking a
      // drop-zone that may not raise a filechooser event.
      const idx = Number(args[0]);
      const files = args[1].split(';').map(f => f.trim()).filter(Boolean);
      const input = page.locator('input[type=file]').nth(idx);
      await input.setInputFiles(files);
      await page.waitForTimeout(3500);
      console.log('set ' + files.length + ' file(s) on input#' + idx);
      shot = args[2] || 'hf_shot.png';
      break;
    }

    case 'grab': {
      // Capture at the CDP level so Chrome's download manager (and its
      // scanner-triggered auto-deletion) never touches the file.
      const dest = args[2];
      const p = page.waitForEvent('download', { timeout: 60000 });
      await page.mouse.click(Number(args[0]), Number(args[1]));
      const dl = await p;
      await dl.saveAs(dest);
      console.log('saved:', dest);
      break;
    }

    default:
      throw new Error(`unknown subcommand: ${cmd}`);
  }

  if (shot) {
    await page.screenshot({ path: out(shot) });
    console.log('shot:', out(shot));
  }
  await browser.close();
}

main().catch(err => { console.error('ERROR:', err.message); process.exit(1); });
