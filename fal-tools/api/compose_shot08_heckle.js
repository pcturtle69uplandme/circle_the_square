// Composite a corrected shot08 still: Jan + Rick (carried over from c06's real last frame,
// so nothing about them has to be re-invented) PLUS Chris, who was missing from the original
// shot08a/shot08b stills. That omission is what made c07 read as Rick vanishing mid-scene --
// see .agents/rules/location_continuity_rules.md and the c06->c07 handoff discussion.
//
// Base image = c06's actual last frame (real render, not a fresh still) so Jan's raised-arm
// pose, Rick's position, the crowd and the location are all pixel-accurate continuations,
// not re-generated guesses. Chris is added via his character reference sheet.

const path = require("path");
const fs = require("fs");
const https = require("https");
const { fal } = require("./client");

async function resolveImage(p) {
  const abs = path.resolve(p);
  const url = await fal.storage.upload(new Blob([fs.readFileSync(abs)]));
  console.log(`Uploaded ${p} -> ${url}`);
  return url;
}

function download(url, dest) {
  return new Promise((resolve, reject) => {
    fs.mkdirSync(path.dirname(dest), { recursive: true });
    const file = fs.createWriteStream(dest);
    https.get(url, (res) => { res.pipe(file); file.on("finish", () => file.close(resolve)); })
      .on("error", (err) => { fs.unlink(dest, () => reject(err)); });
  });
}

async function main() {
  const baseUrl = await resolveImage("scene2-clips/lastframes/c06_naming_inception_last.png");
  const chrisRefUrl = await resolveImage("character-refs/higgsfield/chris/chris_fullbody_neutral.png");

  const prompt = [
    'Photoreal live-action comedy, 35mm lens, natural office daylight. Picture 1 is the exact scene to preserve unchanged: Jan (arm raised, navy suit, white shirt, loosened tie), Rick (arms folded, grey polo) beside him, and the crowd, in the office corridor by the glazed "JAN\'S OFFICE" door. Do not alter Jan, Rick, the crowd, their positions, wardrobe, expressions, or the location in any way.',
    'Add ONE new person into the scene, further down the corridor toward the open-plan desks on the right, partially turned toward the group: CHRIS, matching Picture 2 exactly (32, lean, dark hair, light blue shirt with rolled sleeves, tan chinos). Pose him mid-heckle -- both hands cupped near his mouth, shouting toward Jan and Rick, grinning.',
    'Keep the camera framing close to Picture 1 but widen very slightly to the right to comfortably include Chris in frame. Photoreal, consistent lighting and color grade with Picture 1. No on-screen text or captions.',
  ].join(' ');

  const result = await fal.subscribe("fal-ai/nano-banana-pro/edit", {
    input: {
      prompt,
      image_urls: [baseUrl, chrisRefUrl],
      num_images: 1,
    },
    logs: true,
    onQueueUpdate: (u) => { if (u.status === "IN_PROGRESS") (u.logs || []).forEach((l) => console.log("  ", l.message)); },
  });

  console.log("\nrequestId:", result.requestId);
  const imgUrl = result.data.images[0].url;
  const out = "scene2-stills/shot08a_dreaming_heckle_v2.png";
  await download(imgUrl, out);
  console.log("Saved:", out);
}

main().catch((err) => { console.error(err); process.exit(1); });
