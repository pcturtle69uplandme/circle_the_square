// Composite v3 of the corrected shot08 still, fixing both things that broke v2:
//
// 1. ASPECT RATIO: v2 defaulted to 1024x1024 against the scene's 1344x768/2752x1536,
//    producing a visibly square clip. This time the base image IS ALREADY 1344x768 (c06's
//    real last frame, straight from ffprobe) and we explicitly request that output size so
//    nano-banana-pro/edit has no default to fall back on. Verified again after the call --
//    see .agents/rules/location_continuity_rules.md ("Check the seed image's resolution").
//
// 2. VOICE SWAP: v2 named Rick in the CAST block alongside Jan and Chris, and Jan's line
//    came out in Chris's voice -- not proven as the cause, but avoided this time by NOT
//    giving Rick a named CAST entry at all. He's already correctly rendered pixel-for-pixel
//    in the base image (mid-walk, back to camera, from c06's actual render), so his identity
//    doesn't need a text description -- only Jan and Chris get named/voiced.
//
// User asked for Rick to still be visibly walking away AT THE START of c07 (continuing his
// exit from c06), not already gone -- so the base is c06's last frame as-is, back turned,
// still mid-corridor, and the edit only adds Chris further down toward the open-plan desks.

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
    'Photoreal live-action comedy, 35mm lens, natural office daylight. Picture 1 is the exact scene to preserve unchanged: Jan (navy suit, white shirt, loosened tie) in the foreground, a colleague in a grey polo shirt mid-corridor with his back turned, walking away, and the rest of the crowd, in the office corridor by the glazed "JAN\'S OFFICE" door. Do not alter Jan, the man walking away, the crowd, their positions, wardrobe, or the location in any way -- especially do not stop or reposition the man walking away, he must stay exactly as shown, still mid-stride, back to camera.',
    'Add ONE new person into the scene, further down the corridor toward the open-plan desks on the right, partially turned toward Jan: CHRIS, matching Picture 2 exactly (32, lean, dark hair, light blue shirt with rolled sleeves, tan chinos). Pose him mid-heckle -- both hands cupped near his mouth, shouting toward Jan, grinning.',
    'Keep the camera framing and image dimensions identical to Picture 1 -- same aspect ratio, same crop, only widen the visible area very slightly if needed to comfortably fit Chris. Photoreal, consistent lighting and color grade with Picture 1. No on-screen text or captions.',
  ].join(' ');

  const result = await fal.subscribe("fal-ai/nano-banana-pro/edit", {
    input: {
      prompt,
      image_urls: [baseUrl, chrisRefUrl],
      num_images: 1,
      aspect_ratio: "16:9",
      resolution: "2K",
    },
    logs: true,
    onQueueUpdate: (u) => { if (u.status === "IN_PROGRESS") (u.logs || []).forEach((l) => console.log("  ", l.message)); },
  });

  console.log("\nrequestId:", result.requestId);
  const imgUrl = result.data.images[0].url;
  const out = "scene2-stills/shot08a_dreaming_heckle_v3.png";
  await download(imgUrl, out);
  console.log("Saved:", out);
}

main().catch((err) => { console.error(err); process.exit(1); });
