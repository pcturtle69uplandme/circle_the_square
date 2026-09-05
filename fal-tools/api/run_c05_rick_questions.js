// c05_rick_questions -- Shot 07c-1: Rick challenges the old project, Jan starts justifying.
// Fresh still (shot07c1_rick_questions.png), not chained -- pre-checked for camera-facing
// (both Rick and Jan are in profile/three-quarter facing each other, nobody to-camera).

const path = require("path");
const fs = require("fs");
const https = require("https");
const { fal } = require("./client");

const CAST = 'JAN is 52, overweight, thinning greying hair, too-tight navy suit over a white shirt with the tie loosened askew, shirt re-buttoned crookedly. RICK is 40, broad, greying near-buzzcut, plain GREY POLO. The crowd are British office workers in smart-casual clothes with lanyards, exactly as shown in the reference frame -- keep every crowd member\'s face, hair and outfit exactly as reference, do not invent new people or remove anyone.';
const LANG = 'ALL SPOKEN DIALOGUE IS IN ENGLISH, spoken by British characters with British accents. Do not speak, sing or caption any other language. No Mandarin, no Chinese.';
const LOOK = 'Photoreal live-action comedy, 35mm lens, natural office daylight, handheld-steady camera. Keep every face, costume and the set exactly as in the reference frame. No on-screen text, captions or subtitles.';
const FRAMING = 'CAMERA: fixed static shot size and position, matching the reference frame exactly for the entire clip. Do NOT push in, zoom, cut, or change angle at any point. Only gentle handheld life (small natural shake) is allowed.';

const prompt = [
  LOOK, CAST, LANG, FRAMING,
  'ACTION: begin exactly on the reference frame -- Rick facing Jan, arms folded. Rick delivers his question flat and blunt, with a small deliberate pause before the last three words. Jan\'s pleased expression curdles as he listens. He turns slightly to face Rick and begins a long defensive explanation, one hand raised palm-up in a placating, patronising gesture, chin lifted. The rest of the crowd watch, a few exchanging looks with each other.',
  'DIALOGUE: @Rick (speaking in a flat deadpan northern English accent): "What happened to the last project for this, isn\'t it ongoing? By that I mean... completely failing." Then @Jan (speaking in a defensive, patronising English Home Counties accent): "There\'s no need for the previous project as everything has been a great success even though most things were not delivered on time or within budget."',
  'AUDIO: a low ripple of amusement from the crowd after Rick\'s line, quickly suppressed. Otherwise quiet office ambience.',
].join(' ');

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
  const startUrl = await resolveImage("scene2-stills/shot07c1_rick_questions.png");

  const input = {
    prompt,
    image_url: startUrl,
    duration: 15,
    resolution: "768P",
    prompt_expansion_mode: "balanced",
    enable_safety_checker: false,
  };

  console.log("\nSubmitting c05_rick_questions...\n");
  const result = await fal.subscribe("fal-ai/minimax-h3-turbo/image-to-video", {
    input, logs: true,
    onQueueUpdate: (u) => { if (u.status === "IN_PROGRESS") (u.logs || []).forEach((l) => console.log("  ", l.message)); },
  });

  console.log("\nrequestId:", result.requestId);
  console.log("expanded_prompt:", result.data.expanded_prompt);

  const out = "scene2-clips/c05_rick_questions.mp4";
  await download(result.data.video.url, out);
  console.log("Saved:", out);
  console.log("\nCost check:");
  console.log(`  cd fal-tools/browser && node get_request_cost.js fal-ai/minimax-h3-turbo/image-to-video ${result.requestId}`);
}

main().catch((err) => { console.error(err); process.exit(1); });
