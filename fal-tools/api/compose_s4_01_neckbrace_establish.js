// Scene 4, Beat 1 -- s4_01_neckbrace_establish. Anchor shot for the whole beat: this is
// where Jan's new DAY 3 look (foam neck brace, chair-leg-shaped plaster, creased Scene 3
// wardrobe, pile of PROJECT INCEPTION stress balls on the desk) gets established for the
// first time. Every later Beat 1 shot should chain/composite off THIS still (or its
// approved successor), not reinvent the neck brace from text alone each time.
//
// Location base: jan_office_desk_front.png -- the angle with the triangle feature wall
// behind the desk (Scene 1's signature element) and the glazed door on the left for
// Christina's entrance. The reference plate's chair faces side-on/away; the prompt
// explicitly overrides that to face the camera since no seated-Jan plate exists yet.

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
  const [locUrl, janUrl, christinaUrl] = await Promise.all([
    resolveImage("location-refs/higgsfield/coverage/jan_office/jan_office_desk_front.png"),
    resolveImage("character-refs/higgsfield/jan/jan_fullbody_neutral.png"),
    resolveImage("character-refs/higgsfield/christina/christina_fullbody_neutral.png"),
  ]);

  const prompt = [
    'Photoreal cinematic film still, 35mm lens, natural daylight, medium-wide two-shot. THIRD-PERSON SHOT, camera positioned across the room as an observer -- NOT a point-of-view shot.',
    'LOCATION: reproduce Picture 1 (the office) exactly -- the black-and-white-and-red triangular feature wall behind the desk, the walnut desk with an orange-panelled front, the built-in bookshelves, the glazed black-framed door on the left with raised venetian blinds, the dark herringbone wood floor, the fiddle-leaf fig plant, the grey mesh office chair. Do not alter the room.',
    'CHAIR OVERRIDE: unlike Picture 1, the black mesh office chair is turned to face forward toward the camera and the door, not side-on.',
    'JAN (from Picture 2, keep his exact face and build): 52-year-old British man, overweight, thinning grey-brown side-parted hair. He sits behind the desk in the forward-facing chair. He wears a large white FOAM NECK BRACE/cervical collar around his neck and chin. He is wearing the SAME too-tight dark navy suit jacket over a PALE BLUE dress shirt with a DARK RED tie as the previous scene, but now visibly creased and slept-in, the shirt buttoned crookedly one button off, the tie loosened further askew. On his forehead, above one eyebrow, a small butterfly plaster is visible, distinctly shaped like a chair leg (a thin plaster with a small foot-shaped end). Both hands are in front of him on the desk, rhythmically squeezing a small stress ball. On the desk in front of him sits a small heaped pile of a dozen identical branded stress balls printed "PROJECT INCEPTION". His expression is dazed, faintly pained, staring blankly ahead.',
    'CHRISTINA (from Picture 3, keep her exact face and build): 38-year-old British woman, slim, sleek dark brown bob with a blunt fringe, tailored charcoal blazer over a cream blouse. She is caught mid-stride entering through the open glazed door on the left, holding a closed slim manila document folder flat against her chest in one arm -- NOT a tablet, NOT a laptop, a plain paper folder -- and a takeaway coffee cup in the other hand, her cool deadpan expression already fixed on Jan.',
    'No on-screen text, captions, subtitles, or watermark.',
  ].join(' ');

  const result = await fal.subscribe("fal-ai/nano-banana-pro/edit", {
    input: {
      prompt,
      image_urls: [locUrl, janUrl, christinaUrl],
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
