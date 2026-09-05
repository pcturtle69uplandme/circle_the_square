// Rebuilds scene2-clips/scene2_running_preview.mp4 from whatever accepted clips
// currently sit directly in scene2-clips/ (not in rejected/ or superseded/), in
// filename order (c01, c02, c02b, c03, c04, ...). Run this after every accepted beat
// so there's always an up-to-date full-scene cut to review, not just isolated clips.
//
//   node build_scene2_preview.js

const fs = require("fs");
const path = require("path");
const { execFileSync } = require("child_process");

const DIR = path.resolve(__dirname, "..", "..", "scene2-clips");
const OUT = path.join(DIR, "scene2_running_preview.mp4");
const CONCAT_LIST = path.join(DIR, "_concat.txt");

const clips = fs.readdirSync(DIR)
  .filter((f) => f.endsWith(".mp4") && f !== "scene2_running_preview.mp4")
  .sort();

if (clips.length === 0) {
  console.error("No clips found directly in scene2-clips/");
  process.exit(1);
}

fs.writeFileSync(CONCAT_LIST, clips.map((f) => `file '${f}'`).join("\n") + "\n");

console.log("Clips in order:");
clips.forEach((c) => console.log("  " + c));

execFileSync("ffmpeg", [
  "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", CONCAT_LIST,
  "-c:v", "libx264", "-preset", "medium", "-crf", "18",
  "-c:a", "aac", "-b:a", "192k",
  OUT,
], { cwd: DIR });

const dur = execFileSync("ffprobe", [
  "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", OUT,
]).toString().trim();

console.log(`\nWritten: ${OUT} (${dur}s)`);
