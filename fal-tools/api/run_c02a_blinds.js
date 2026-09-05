// Rule: NEVER use end_image_url. A character not present in the single start frame gets
// invented by the model to satisfy a forced end state, which produced the pop-in/reposition
// glitch on the first c02_merged attempt (see scene2-clips/rejected/). Single start frame
// only -- everyone whose identity matters must already be IN it.
//
// c02a: start = shot06 (Chris + Rick only, both already anchored). Blinds raise, door
// opens. Nobody unestablished is revealed, so there is no identity risk here.

const path = require("path");
const fs = require("fs");
const https = require("https");
const { fal } = require("./client");

const CAST = 'JAN is 52, overweight, thinning greying hair, too-tight navy suit over a white shirt with the tie loosened askew, shirt re-buttoned crookedly. CHRIS is 32, lean, dark hair, LIGHT BLUE shirt with rolled sleeves and tan chinos. RICK is 40, broad, greying near-buzzcut, plain GREY POLO.';
const LANG = 'ALL SPOKEN DIALOGUE IS IN ENGLISH, spoken by British characters with British accents. Do not speak, sing or caption any other language. No Mandarin, no Chinese. There is no dialogue in this clip -- keep everyone silent.';
const LOOK = 'Photoreal live-action comedy, 35mm lens, natural office daylight, handheld-steady camera. Keep every face, costume and the set exactly as in the reference frame. No on-screen text, captions or subtitles.';
const FRAMING = 'CAMERA: stay close to the reference frame shot size. Gentle handheld life and a small drift are welcome, but do not travel to a significantly tighter or wider framing.';

const prompt = [
  LOOK, CAST, LANG, FRAMING,
  'ACTION: hold on the corridor exactly as the reference frame -- Chris and Rick standing beside the glazed office door, its venetian blinds closed flat and opaque, nothing inside visible. Partway through, the blinds are RAISED from inside, folding up to the top of the glass and revealing the lit office interior behind it -- through the glass a blurred, indistinct figure can be glimpsed moving inside but stays too obscured by the blind slats and glare to make out clearly. The door handle turns and the door begins to open. Nobody steps out yet -- the clip ends as the door swings open on the doorway, still empty. Chris and Rick DO NOT MOVE OR WALK -- they stay exactly where the reference frame puts them and simply turn their heads toward the movement.',
  'DIALOGUE: none. Nobody speaks.',
  'AUDIO: quiet office ambience, then the distinct rattle and clack of a venetian blind being raised, then a door latch turning.',
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
  const startUrl = await resolveImage("scene2-stills/shot06_corridor_gossip.png");

  const input = {
    prompt,
    image_url: startUrl,
    duration: 5,
    resolution: "768P",
    prompt_expansion_mode: "balanced",
    enable_safety_checker: false,
  };

  console.log("\nSubmitting c02a_blinds_raised...\n");
  const result = await fal.subscribe("fal-ai/minimax-h3-turbo/image-to-video", {
    input, logs: true,
    onQueueUpdate: (u) => { if (u.status === "IN_PROGRESS") (u.logs || []).forEach((l) => console.log("  ", l.message)); },
  });

  console.log("\nrequestId:", result.requestId);
  console.log("expanded_prompt:", result.data.expanded_prompt);

  const out = "scene2-clips/c02a_blinds_raised.mp4";
  await download(result.data.video.url, out);
  console.log("Saved:", out);
  console.log("\nCost check:");
  console.log(`  cd fal-tools/browser && node get_request_cost.js fal-ai/minimax-h3-turbo/image-to-video ${result.requestId}`);
}

main().catch((err) => { console.error(err); process.exit(1); });
