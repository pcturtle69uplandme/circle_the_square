// Rebuilds scene4-clips/scene4_beat1_running_preview.mp4 from whatever clips currently
// sit directly in scene4-clips/ (not in lastframes/ or qa/, and not a leading-underscore
// build artifact), in filename order (s4_01, s4_02, ...). Mirrors build_scene3_preview.js.
//
//   node build_scene4_preview.js

const fs = require("fs");
const path = require("path");
const { execFileSync } = require("child_process");

const DIR = path.resolve(__dirname, "..", "..", "scene4-clips");
const OUT = path.join(DIR, "scene4_beat1_running_preview.mp4");
const CONCAT_LIST = path.join(DIR, "_concat.txt");

const clips = fs.readdirSync(DIR)
  .filter((f) => f.endsWith(".mp4") && f !== path.basename(OUT) && !f.startsWith("_"))
  .sort();

if (clips.length === 0) {
  console.error("No clips found directly in scene4-clips/");
  process.exit(1);
}

fs.writeFileSync(CONCAT_LIST, clips.map((f) => `file '${f}'`).join("\n") + "\n");

console.log("Clips in order:");
clips.forEach((c) => console.log("  " + c));

execFileSync("ffmpeg", [
  "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", CONCAT_LIST,
  "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
  "-c:a", "aac", "-b:a", "192k",
  OUT,
], { cwd: DIR });

const dur = execFileSync("ffprobe", [
  "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", OUT,
]).toString().trim();

console.log(`\nWritten: ${OUT} (${dur}s)`);
