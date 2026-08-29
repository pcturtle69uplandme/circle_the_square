#!/usr/bin/env node
// One-off: re-derive result_url for each job_id in location-coverage-manifest.json
// and download the PNG to its expected disk path. This catches the case where
// the previous run generated the shots but failed to save the bytes to disk
// (e.g. a download step errored out), so the manifest says "ok" but the
// directory is empty.
//
// Usage:  node download-missing-angles.js <location-slug>
// Example: node download-missing-angles.js jan_office

const fs = require("fs");
const path = require("path");
const { execFileSync } = require("child_process");

const MANIFEST_PATH = path.join(__dirname, "location-coverage-manifest.json");
const COVERAGE_ROOT = path.join(__dirname, "..", "location-refs", "higgsfield", "coverage");

function hfJson(args) {
  const fullArgs = process.platform === "win32"
    ? ["/c", "higgsfield.cmd", ...args, "--json", "--no-color"]
    : [...args, "--json", "--no-color"];
  const out = execFileSync(process.platform === "win32" ? "cmd.exe" : "higgsfield",
    fullArgs, { encoding: "utf8", maxBuffer: 32 * 1024 * 1024 });
  return JSON.parse(out);
}

async function downloadTo(url, destPath) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`HTTP ${res.status} for ${url}`);
  const buf = Buffer.from(await res.arrayBuffer());
  fs.mkdirSync(path.dirname(destPath), { recursive: true });
  fs.writeFileSync(destPath, buf);
}

async function run(slug) {
  if (!slug) {
    console.error("Usage: node download-missing-angles.js <location-slug>");
    process.exit(1);
  }
  const manifest = JSON.parse(fs.readFileSync(MANIFEST_PATH, "utf8"));
  const loc = manifest[slug];
  if (!loc) {
    console.error(`No location "${slug}" in manifest. Known: ${Object.keys(manifest).join(", ")}`);
    process.exit(1);
  }

  const outDir = path.join(COVERAGE_ROOT, slug);
  let downloaded = 0, skipped = 0, failed = 0;

  for (const [angle, entry] of Object.entries(loc)) {
    const destPath = path.join(outDir, `${slug}_${angle}.png`);
    if (fs.existsSync(destPath) && fs.statSync(destPath).size > 0) {
      console.log(`  [skip] ${angle} (already on disk: ${path.basename(destPath)})`);
      skipped++;
      continue;
    }
    try {
      const job = hfJson(["generate", "get", entry.job_id]);
      if (job.status !== "completed" || !job.result_url) {
        console.error(`  [FAIL] ${angle}: job ${entry.job_id} status=${job.status}`);
        failed++;
        continue;
      }
      await downloadTo(job.result_url, destPath);
      console.log(`  [ok]   ${angle} -> ${path.basename(destPath)}  (${(fs.statSync(destPath).size / 1024).toFixed(0)} KB)`);
      downloaded++;
    } catch (e) {
      console.error(`  [ERROR] ${angle}: ${e.message}`);
      failed++;
    }
  }

  console.log(`\nDone. Downloaded: ${downloaded}, skipped: ${skipped}, failed: ${failed}`);
  if (failed > 0) process.exit(1);
}

const slug = process.argv[2];
run(slug).catch((e) => { console.error("Fatal:", e); process.exit(1); });
