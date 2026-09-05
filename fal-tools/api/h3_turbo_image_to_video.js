// fal-ai/minimax-h3-turbo/image-to-video via the paid REST API (queue.fal.ai), not the browser.
// Usage:
//   node h3_turbo_image_to_video.js --image <url> --prompt "..." --duration 8 --out clips/shot.mp4 \
//        [--end-image <url>] [--resolution 480P|768P] [--expansion balanced|quality] [--seed N] [--safety]
//
// Prints the fal request id, expanded prompt, timings, and cost-relevant fields as they
// come back, then downloads the resulting video to --out.

const fs = require("fs");
const path = require("path");
const https = require("https");
const { fal } = require("./client");

function parseArgs(argv) {
  const out = { resolution: "768P", expansion: "balanced", safety: false };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    const val = () => argv[++i];
    switch (a) {
      case "--image": out.image = val(); break;
      case "--end-image": out.endImage = val(); break;
      case "--prompt": out.prompt = val(); break;
      case "--duration": out.duration = Number(val()); break;
      case "--resolution": out.resolution = val(); break;
      case "--expansion": out.expansion = val(); break;
      case "--seed": out.seed = Number(val()); break;
      case "--safety": out.safety = true; break;
      case "--out": out.out = val(); break;
      default:
        console.error(`Unknown arg: ${a}`);
        process.exit(1);
    }
  }
  if (!out.prompt || !out.out) {
    console.error("Required: --prompt \"...\" --out path/to/file.mp4 (and usually --image <url>)");
    process.exit(1);
  }
  return out;
}

function download(url, dest) {
  return new Promise((resolve, reject) => {
    fs.mkdirSync(path.dirname(dest), { recursive: true });
    const file = fs.createWriteStream(dest);
    https.get(url, (res) => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        file.close();
        fs.unlinkSync(dest);
        return download(res.headers.location, dest).then(resolve, reject);
      }
      res.pipe(file);
      file.on("finish", () => file.close(resolve));
    }).on("error", (err) => {
      fs.unlink(dest, () => reject(err));
    });
  });
}

async function resolveImage(pathOrUrl) {
  if (!pathOrUrl) return undefined;
  if (/^https?:\/\//i.test(pathOrUrl)) return pathOrUrl;
  const abs = path.resolve(pathOrUrl);
  if (!fs.existsSync(abs)) {
    throw new Error(`Image not found: ${abs}`);
  }
  console.log(`Uploading ${abs} to fal storage...`);
  const buf = fs.readFileSync(abs);
  const blob = new Blob([buf]);
  const url = await fal.storage.upload(blob);
  console.log("  ->", url);
  return url;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));

  const input = {
    prompt: args.prompt,
    prompt_expansion_mode: args.expansion,
    resolution: args.resolution,
    enable_safety_checker: args.safety,
  };
  if (args.image) input.image_url = await resolveImage(args.image);
  if (args.endImage) input.end_image_url = await resolveImage(args.endImage);
  if (args.duration) input.duration = args.duration;
  if (Number.isFinite(args.seed)) input.seed = args.seed;

  console.log("Submitting:", JSON.stringify(input, null, 2));

  const result = await fal.subscribe("fal-ai/minimax-h3-turbo/image-to-video", {
    input,
    logs: true,
    onQueueUpdate: (update) => {
      if (update.status === "IN_PROGRESS") {
        (update.logs || []).map((l) => l.message).forEach((m) => console.log("  ", m));
      }
    },
  });

  console.log("requestId:", result.requestId);
  console.log("expanded_prompt:", result.data.expanded_prompt);
  console.log("timings:", result.data.timings);
  console.log("video:", result.data.video);

  await download(result.data.video.url, args.out);
  console.log("Saved:", args.out);

  console.log("\nTo confirm actual billed cost (the API returns none):");
  console.log(`  cd fal-tools/browser && node get_request_cost.js fal-ai/minimax-h3-turbo/image-to-video ${result.requestId}`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
