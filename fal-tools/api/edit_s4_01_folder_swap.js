// Targeted edit of the ACCEPTED s4_01 anchor still: swap Christina's tablet for a closed
// manila document folder, changing nothing else. A from-scratch regenerate (tried once)
// drifted badly -- red stress balls, wrong plaster shape, different room framing -- because
// it re-rolled the whole composition from character sheets instead of editing the specific
// accepted pixels. This uses the accepted image itself as the base reference so everything
// else (white PROJECT INCEPTION balls, chair-leg plaster, room framing, lighting) is locked.

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
  const baseUrl = await resolveImage("scene4-stills/s4_01_neckbrace_establish.png");

  const prompt = [
    'Picture 1 is the exact scene to preserve unchanged: the room, the camera framing and lighting, Jan (his neck brace, chair-leg-shaped plaster, creased pale-blue-shirt-and-dark-red-tie, navy suit jacket, both hands squeezing a stress ball), the small heaped pile of WHITE stress balls printed "PROJECT INCEPTION" on the desk, Christina\'s face, hair, charcoal blazer, cream blouse, and her exact walking pose entering through the glazed door. Do not alter any of this.',
    'CHANGE ONLY ONE THING: replace the object Christina is holding against her chest. Instead of a tablet, she is holding a closed, slim, plain manila document folder flat against her chest with one arm -- no visible screen, no tablet, no laptop. She still holds a takeaway coffee cup in her other hand exactly as before.',
    'No on-screen text, captions, subtitles, or watermark.',
  ].join(' ');

  const result = await fal.subscribe("fal-ai/nano-banana-pro/edit", {
    input: {
      prompt,
      image_urls: [baseUrl],
      num_images: 1,
      aspect_ratio: "16:9",
      resolution: "2K",
    },
    logs: true,
    onQueueUpdate: (u) => { if (u.status === "IN_PROGRESS") (u.logs || []).forEach((l) => console.log("  ", l.message)); },
  });

  console.log("\nrequestId:", result.requestId);
  const imgUrl = result.data.images[0].url;
  const out = "scene4-stills/s4_01_neckbrace_establish.png";
  await download(imgUrl, out);
  console.log("Saved:", out);
}

main().catch((err) => { console.error(err); process.exit(1); });
