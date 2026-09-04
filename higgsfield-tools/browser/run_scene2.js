// Generate every Scene 2 still that is not already on disk, one at a time.
//
//   node run_scene2.js [--force] [--only <slug>,<slug>]
//
// Resumable on purpose: free-tier renders take minutes each, so a ten-shot batch is a
// long-running job that will sometimes be interrupted (a killed background task, a
// closed browser, a dropped session). Re-running picks up where it left off instead of
// re-rendering what already succeeded. Pass --force to regenerate everything.
//
// Output is written per line and unbuffered so progress is visible while it runs --
// piping the child through `tail` hides everything until each shot finishes.
const { spawnSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const SHOTS = require('./scene2_shots.js');
const OUT = path.resolve(__dirname, '..', '..', 'scene2-stills');

const args = process.argv.slice(2);
const force = args.includes('--force');
const onlyIdx = args.indexOf('--only');
const only = onlyIdx >= 0 ? (args[onlyIdx + 1] || '').split(',').filter(Boolean) : null;

// "Already on disk" is not enough: first-pass stills from the previous session share
// filenames with some of the new slugs, and editing one shot's prompt must not
// invalidate every other shot. So each PNG gets a sidecar recording the hash of the
// prompt+refs that produced it. A shot counts as done when its sidecar matches the
// current definition, which makes re-rolling exactly one beat a one-line edit.
const crypto = require('crypto');
const fingerprint = (slug) =>
  crypto.createHash('sha256')
    .update(JSON.stringify({ prompt: SHOTS[slug].prompt, refs: SHOTS[slug].refs }))
    .digest('hex').slice(0, 16);
const sidecar = (slug) => path.join(OUT, `.${slug}.gen.json`);

const isDone = (slug) => {
  if (!fs.existsSync(path.join(OUT, `${slug}.png`))) return false;
  try {
    return JSON.parse(fs.readFileSync(sidecar(slug), 'utf8')).fingerprint === fingerprint(slug);
  } catch { return false; }
};
const markDone = (slug) => fs.writeFileSync(sidecar(slug), JSON.stringify({
  slug, fingerprint: fingerprint(slug), generated: new Date().toISOString(), beat: SHOTS[slug].beat,
}, null, 2));

const slugs = Object.keys(SHOTS).filter(s => !only || only.includes(s));
const todo = slugs.filter(s => force || !isDone(s));

console.log(`${slugs.length} shot(s) in scope, ${slugs.length - todo.length} already done, ${todo.length} to generate`);

// Make sure a detached browser is up before the queue starts, and again on retry --
// a batch that outlives its browser otherwise fails every remaining shot.
const ensureBrowser = () => spawnSync(process.execPath, [path.join(__dirname, 'hf_up.js')], { stdio: 'inherit' });
ensureBrowser();

const failed = [];
for (const [n, slug] of todo.entries()) {
  console.log(`\n[${n + 1}/${todo.length}] ${slug} -- ${SHOTS[slug].beat}`);
  // Chrome intermittently drops its CDP endpoint under a long run (every remaining
  // shot in one batch died on "connectOverCDP: Timeout" after one such drop, then the
  // last one succeeded once it recovered). Retry a couple of times rather than
  // abandoning the rest of the queue for a transient browser hiccup.
  let ok = false;
  for (let attempt = 1; attempt <= 3 && !ok; attempt++) {
    if (attempt > 1) console.log(`  retry ${attempt}/3 for ${slug}`);
    const r = spawnSync(process.execPath, [path.join(__dirname, 'run_shot.js'), slug], {
      stdio: 'inherit',
      timeout: 20 * 60 * 1000,
    });
    ok = r.status === 0;
    if (!ok && attempt < 3) { spawnSync(process.execPath, ['-e', 'setTimeout(()=>{},15000)']); ensureBrowser(); }
  }
  if (ok) markDone(slug);
  else {
    console.log(`FAILED ${slug}`);
    failed.push(slug);
  }
}

console.log(`\ndone: ${todo.length - failed.length}/${todo.length} generated`);
if (failed.length) {
  console.log(`failed: ${failed.join(', ')}`);
  process.exit(1);
}
