// c03_jan_addresses -- Shot 07b-1: Jan emerges, claps, is asked about Sharon, deflects.
// New setup/location (corridor meets open-plan desks, crowd gathered) vs c01/c02's
// corridor-by-the-door framing -- treated as a genuine cut, not chained. Single start
// frame only (shot07b1_jan_addresses.png), no end_image_url, locked camera.

const path = require("path");
const fs = require("fs");
const https = require("https");
const { fal } = require("./client");

const CAST = 'JAN is 52, overweight, thinning greying hair, too-tight navy suit over a white shirt with the tie loosened askew, shirt re-buttoned crookedly. CHRIS is 32, lean, dark hair, LIGHT BLUE shirt with rolled sleeves and tan chinos. The crowd are British office workers in smart-casual clothes with lanyards, exactly as shown in the reference frame -- keep every crowd member\'s face, hair and outfit exactly as reference, do not invent new people or remove anyone.';
const LANG = 'ALL SPOKEN DIALOGUE IS IN ENGLISH, spoken by British characters with British accents. Do not speak, sing or caption any other language. No Mandarin, no Chinese.';
const LOOK = 'Photoreal live-action comedy, 35mm lens, natural office daylight, handheld-steady camera. Keep every face, costume and the set exactly as in the reference frame. No on-screen text, captions or subtitles.';
const FRAMING = 'CAMERA: fixed static shot size and position, matching the reference frame exactly for the entire clip. Do NOT push in, zoom, cut, or change angle at any point. Do NOT go to a close-up. Only gentle handheld life (small natural shake) is allowed.';

const prompt = [
  LOOK, CAST, LANG, FRAMING,
  'ACTION: begin exactly on the reference frame -- Jan mid-clap at the focal point where the corridor meets the open-plan desks, the crowd already gathered around him, Chris facing him at the front of the crowd. Jan finishes clapping and begins his address, chin raised, self-important and pleased with himself. Chris half-raises a hand and cuts in with a pointed question. Jan\'s composure slips for a moment -- eyes flicking away, a tug at his collar -- before he recovers and answers smoothly. The rest of the crowd stand and watch, mostly still.',
  'DIALOGUE: @Jan (speaking in a booming, self-important English Home Counties accent): "Right guys, as you know —" Then @Chris (speaking in a South London Estuary English accent, interrupting): "Does Sharon get a pass on attending this?" Then @Jan (speaking in an evasive English Home Counties accent): "Err... yes she does. I have given her the rest of the day off for personal reasons."',
  'AUDIO: quiet attentive office ambience under the dialogue, a couple of quiet chair scrapes as latecomers settle. No music.',
  "TIMING: the dialogue occupies the first 13 seconds. HOLD the final 2 seconds on Jan looking pleased with his own answer while the crowd stare back flatly, camera unchanged. No further dialogue, no new action.",
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
  const startUrl = await resolveImage("scene2-stills/shot07b1_jan_addresses.png");

  const input = {
    prompt,
    image_url: startUrl,
    duration: 15,
    resolution: "768P",
    prompt_expansion_mode: "balanced",
    enable_safety_checker: false,
  };

  console.log("\nSubmitting c03_jan_addresses...\n");
  const result = await fal.subscribe("fal-ai/minimax-h3-turbo/image-to-video", {
    input, logs: true,
    onQueueUpdate: (u) => { if (u.status === "IN_PROGRESS") (u.logs || []).forEach((l) => console.log("  ", l.message)); },
  });

  console.log("\nrequestId:", result.requestId);
  console.log("expanded_prompt:", result.data.expanded_prompt);

  const out = "scene2-clips/c03_jan_addresses.mp4";
  await download(result.data.video.url, out);
  console.log("Saved:", out);
  console.log("\nCost check:");
  console.log(`  cd fal-tools/browser && node get_request_cost.js fal-ai/minimax-h3-turbo/image-to-video ${result.requestId}`);
}

main().catch((err) => { console.error(err); process.exit(1); });
