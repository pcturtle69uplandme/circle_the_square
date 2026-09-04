// Extract the LAST frame of a generated clip, for chaining the next clip off it.
//
//   node last_frame.js <clipSlug> [outPath]
//
// Why this exists: a clip's prompt can ask for a slow push-in, and the model will
// happily deliver a bigger move than asked. c01 was written as a wide two-shot with a
// slow push and came back a medium two-shot. That is fine inside the clip, but it
// breaks the JOIN -- the next clip's start frame is the original wide still, so cutting
// c01 -> c02 would jump backwards to a framing the camera has already left.
//
// Chaining off the real last frame guarantees the join regardless of how far the camera
// actually travelled.
//
// ⚠️ Do not chain indefinitely. Scene 1 measured generational drift compounding when
// each clip seeds off an ever-more-derivative frame -- brightness fell and shadows
// crushed roughly twice every ~4 generations deep. Reset to an adopted still at every
// natural cut, and never run more than ~6 chained links. See
// .agents/rules/location_continuity_rules.md and SCENE1_MINIMAX_TRACKER.md.
const { execFileSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const REPO = path.resolve(__dirname, '..', '..');
const CLIPS = path.join(REPO, 'scene2-clips');
const FRAMES = path.join(CLIPS, 'lastframes');

function ffmpeg() {
  try {
    return execFileSync(process.platform === 'win32' ? 'where' : 'which', ['ffmpeg'])
      .toString().split(/\r?\n/)[0].trim();
  } catch { return 'ffmpeg'; }
}

const slug = process.argv[2];
if (!slug) throw new Error('usage: node last_frame.js <clipSlug> [outPath]');

const src = path.join(CLIPS, `${slug}.mp4`);
if (!fs.existsSync(src)) throw new Error(`no such clip: ${src}`);

const out = process.argv[3] || path.join(FRAMES, `${slug}_last.png`);
fs.mkdirSync(path.dirname(out), { recursive: true });

// sseof seeks from the END, so this does not need the duration up front. -update 1
// keeps overwriting the single output so we finish holding the final decoded frame.
execFileSync(ffmpeg(), [
  '-y', '-sseof', '-0.5', '-i', src,
  '-update', '1', '-frames:v', '1', '-q:v', '2',
  out,
], { stdio: 'pipe' });

const rel = path.relative(REPO, out).replace(/\\/g, '/');
console.log(`${rel}  (${fs.statSync(out).size} bytes)`);
