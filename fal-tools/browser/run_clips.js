// Generate every Scene 2 clip not already on disk, one at a time, and STOP when the
// free-tier allowance runs out rather than silently spending money.
//
//   node run_clips.js [--force] [--only <slug>,<slug>] [--max N] [--dry-run]
//
// Resumable in the same way as higgsfield-tools/browser/run_batch.js: each saved mp4
// gets a sidecar holding a fingerprint of the prompt + frames + duration that produced
// it, so editing one clip's prompt re-renders exactly that clip and leaves the rest.
//
// ⚠️ THE FREE TIER IS 5 GENERATIONS PER ROLLING 24 HOURS. This driver defaults to
// --max 5 for that reason: Scene 2 is ten clips, so a clean run is two days, and a
// run that quietly continued past the allowance would start billing at $0.08/sec.
// Raise --max deliberately, never by habit.
const { spawnSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const CLIPS = require(process.env.FAL_CLIPS || './scene2_clips.js');
const OUT = process.env.FAL_OUT || path.resolve(__dirname, '..', '..', 'scene2-clips');

const args = process.argv.slice(2);
const force = args.includes('--force');
const dryRun = args.includes('--dry-run');
const onlyIdx = args.indexOf('--only');
const only = onlyIdx >= 0 ? (args[onlyIdx + 1] || '').split(',').filter(Boolean) : null;
const maxIdx = args.indexOf('--max');
const max = maxIdx >= 0 ? Number(args[maxIdx + 1]) : 5;

const fingerprint = (slug) => {
  const c = CLIPS[slug];
  return crypto.createHash('sha256')
    .update(JSON.stringify({ p: c.prompt, s: c.startImage, e: c.endImage || null, d: c.seconds }))
    .digest('hex').slice(0, 16);
};
const sidecar = (slug) => path.join(OUT, `.${slug}.gen.json`);

const isDone = (slug) => {
  if (!fs.existsSync(path.join(OUT, `${slug}.mp4`))) return false;
  try { return JSON.parse(fs.readFileSync(sidecar(slug), 'utf8')).fingerprint === fingerprint(slug); }
  catch { return false; }
};
const markDone = (slug) => fs.writeFileSync(sidecar(slug), JSON.stringify({
  slug, fingerprint: fingerprint(slug), seconds: CLIPS[slug].seconds,
  beats: CLIPS[slug].beats, generated: new Date().toISOString(),
}, null, 2));

const ensureBrowser = () => spawnSync(process.execPath, [path.join(__dirname, 'fal_up.js')], { stdio: 'inherit' });

const slugs = Object.keys(CLIPS).filter(s => !only || only.includes(s));
const todo = slugs.filter(s => force || !isDone(s));
const batch = todo.slice(0, max);

const totalSecs = batch.reduce((n, s) => n + CLIPS[s].seconds, 0);
console.log(`${slugs.length} clip(s) in scope, ${slugs.length - todo.length} done, ${todo.length} outstanding`);
console.log(`this run: ${batch.length} clip(s), ${totalSecs}s of video (free-tier cap --max ${max})`);
if (todo.length > batch.length) {
  console.log(`${todo.length - batch.length} clip(s) deferred to the next 24h window`);
}

if (!dryRun) ensureBrowser();

const failed = [];
for (const [n, slug] of batch.entries()) {
  console.log(`\n[${n + 1}/${batch.length}] ${slug} (${CLIPS[slug].seconds}s) -- ${CLIPS[slug].beats}`);
  let ok = false;
  for (let attempt = 1; attempt <= 2 && !ok; attempt++) {
    if (attempt > 1) { console.log(`  retry ${attempt}/2`); ensureBrowser(); }
    const a = [path.join(__dirname, 'fal_clip.js'), slug, OUT];
    if (dryRun) a.push('--dry-run');
    const r = spawnSync(process.execPath, a, { stdio: 'inherit', timeout: 30 * 60 * 1000, env: process.env });
    ok = r.status === 0;
  }
  if (ok) { if (!dryRun) markDone(slug); }
  else { console.log(`FAILED ${slug}`); failed.push(slug); }
}

console.log(`\ndone: ${batch.length - failed.length}/${batch.length}`);
if (failed.length) { console.log(`failed: ${failed.join(', ')}`); process.exit(1); }
