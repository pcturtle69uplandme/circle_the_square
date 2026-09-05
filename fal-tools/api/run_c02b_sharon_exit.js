// Rule: NEVER use end_image_url -- see run_c02a_blinds.js header for why.
//
// c02b: start = shot07, which already contains Sharon, Jan, Chris AND Rick all in frame
// -- everyone whose identity matters is real pixels, not invented from text. Jan's
// dishevelment is described as his ALREADY-VISIBLE state in that reference (tie loose,
// flushed, sweating) plus a small in-character motion, not a big invented dressing action
// -- he cannot be shown mid-dress here because there is no earlier frame to dress FROM.

const path = require("path");
const fs = require("fs");
const https = require("https");
const { fal } = require("./client");

const CAST = 'JAN is 52, overweight, thinning greying hair, too-tight navy suit over a white shirt with the tie loosened askew, shirt re-buttoned crookedly. CHRIS is 32, lean, dark hair, LIGHT BLUE shirt with rolled sleeves and tan chinos. RICK is 40, broad, greying near-buzzcut, plain GREY POLO.';
const LANG = 'ALL SPOKEN DIALOGUE IS IN ENGLISH, spoken by British characters with British accents. Do not speak, sing or caption any other language. No Mandarin, no Chinese. There is no dialogue in this clip -- keep everyone silent.';
const LOOK = 'Photoreal live-action comedy, 35mm lens, natural office daylight, handheld-steady camera. Keep every face, costume and the set exactly as in the reference frame. No on-screen text, captions or subtitles.';
const FRAMING = 'CAMERA: fixed static shot size and position, matching the reference frame exactly for the entire clip. Do NOT push in, zoom, cut, or change angle at any point. Do NOT go to a close-up. Only gentle handheld life (small natural shake) is allowed -- the framing at the last frame must look like the same locked-off camera setup as the first frame, just with people having moved within it.';

const prompt = [
  LOOK, CAST, LANG, FRAMING,
  'ACTION: begin exactly on the reference frame -- Sharon already in the open office doorway, Jan already seated at his desk inside behind her, Chris and Rick already in the corridor. Sharon walks OUT of the doorway and away down the corridor toward camera in one continuous, steady, uninterrupted stride -- she never pauses, reverses or repositions -- smoothing her creased blouse and pushing her mussed hair back, eyes down, dazed but trying to compose herself, hair visibly disheveled, a light sheen of sweat. Jan stays seated inside exactly where the reference frame puts him -- he is visibly flushed and sweating, his tie still loose and askew as already shown -- he mops his brow once with the back of his hand and tugs at his collar, still trying to catch his breath, and does not look out. CHRIS AND RICK DO NOT MOVE OR WALK -- they stay exactly where the reference frame puts them and simply turn their heads to watch her pass, Chris smirking slightly, Rick impassive.',
  'DIALOGUE: none. Nobody speaks.',
  "AUDIO: quiet office ambience, Sharon's heels on carpet tile, and one quiet snigger from Chris as she passes.",
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
  const startUrl = await resolveImage("scene2-stills/shot07_sharon_exits.png");

  const input = {
    prompt,
    image_url: startUrl,
    duration: 10,
    resolution: "768P",
    prompt_expansion_mode: "balanced",
    enable_safety_checker: false,
  };

  console.log("\nSubmitting c02b_sharon_exits...\n");
  const result = await fal.subscribe("fal-ai/minimax-h3-turbo/image-to-video", {
    input, logs: true,
    onQueueUpdate: (u) => { if (u.status === "IN_PROGRESS") (u.logs || []).forEach((l) => console.log("  ", l.message)); },
  });

  console.log("\nrequestId:", result.requestId);
  console.log("expanded_prompt:", result.data.expanded_prompt);

  const out = "scene2-clips/c02b_sharon_exits_v2.mp4";
  await download(result.data.video.url, out);
  console.log("Saved:", out);
  console.log("\nCost check:");
  console.log(`  cd fal-tools/browser && node get_request_cost.js fal-ai/minimax-h3-turbo/image-to-video ${result.requestId}`);
}

main().catch((err) => { console.error(err); process.exit(1); });
