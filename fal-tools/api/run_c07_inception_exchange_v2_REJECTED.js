// c07_inception_exchange -- Shots 08a + 08b: all FOUR turns of the Inception gag.
//
// v2: single start image, NOT a keyframe pair. The original attempt used the pre-existing
// shot08a/shot08b stills, which never included RICK -- so the cut read as Rick vanishing
// mid-scene, not a camera choice (flagged on review). Composited a corrected start still
// (compose_shot08_heckle.js) from c06's REAL last frame (Jan, Rick, crowd, location all
// pixel-accurate) with Chris added via his character reference sheet, so nobody who was on
// screen a moment ago goes missing. Chris being newly introduced here IS a legitimate cut
// per .agents/rules/location_continuity_rules.md -- the problem was only ever Rick.
//
// No end_image_url: project rule (see run_c02b_sharon_exit.js) is NEVER use it, and c07
// doesn't need it now anyway -- the whole four-turn arc plays out from one start frame via
// the ACTION prompt instead of forcing a hard landing on a second still.

const path = require("path");
const fs = require("fs");
const https = require("https");
const { fal } = require("./client");

const CAST = 'JAN is 52, overweight, thinning greying hair, too-tight navy suit over a white shirt with the tie loosened askew, shirt re-buttoned crookedly. RICK is 40, broad, greying near-buzzcut, plain GREY POLO. CHRIS is 32, lean, dark hair, LIGHT BLUE shirt with rolled sleeves and tan chinos. The crowd are British office workers in smart-casual clothes with lanyards, exactly as shown in the reference frame -- keep every crowd member\'s face, hair and outfit exactly as reference, do not invent new people or remove anyone.';
const LANG = 'ALL SPOKEN DIALOGUE IS IN ENGLISH, spoken by British characters with British accents. Do not speak, sing or caption any other language. No Mandarin, no Chinese.';
const LOOK = 'Photoreal live-action comedy, 35mm lens, natural office daylight, handheld-steady camera. Keep every face, costume and the set exactly as in the reference frame. No on-screen text, captions or subtitles.';

const prompt = [
  LOOK, CAST, LANG,
  'ACTION: begin exactly on the reference frame -- continuing directly from Jan\'s announcement, no cut. His raised arm is already relaxing back down as the silence lingers. Chris, further down the corridor toward the desks, shouts over with a grin, hands cupped near his mouth, to a rising laugh from the crowd. Jan turns toward him, genuinely baffled -- a blank, uncomprehending stare, he has not got it. Chris then explains patiently with a raised hand, as if to a child, to more laughter. Jan understands, and deflates: mouth open, eyes darting sideways, shoulders dropping, one hand raised in a weak dismissive wave as he covers badly. Rick does not move or react beyond perhaps the barest smirk -- arms folded throughout.',
  'DIALOGUE, four turns in order: @Chris (shouting in a South London Estuary English accent): "You\'re dreaming Jan!" Then @Jan (speaking in a baffled English Home Counties accent): "What?!" Then @Chris (speaking in a patient, amused South London Estuary English accent): "Inception is the name of a film about dreams Jan." Then @Jan (speaking in a flustered English Home Counties accent): "Oh, well... it is also the name of this project."',
  'AUDIO: a big laugh on the heckle, a beat of silence on Jan\'s "What?!", then broader laughter on the explanation which Jan talks weakly over.',
  'TIMING: the four lines occupy the whole clip, ending around 9 seconds. HOLD any remaining time on Jan\'s flustered, deflated reaction. No further dialogue.',
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
  const startUrl = await resolveImage("scene2-stills/shot08a_dreaming_heckle_v2.png");

  const input = {
    prompt,
    image_url: startUrl,
    duration: 10,
    resolution: "768P",
    prompt_expansion_mode: "balanced",
    enable_safety_checker: false,
  };

  console.log("\nSubmitting c07_inception_exchange (v2, corrected start still)...\n");
  const result = await fal.subscribe("fal-ai/minimax-h3-turbo/image-to-video", {
    input, logs: true,
    onQueueUpdate: (u) => { if (u.status === "IN_PROGRESS") (u.logs || []).forEach((l) => console.log("  ", l.message)); },
  });

  console.log("\nrequestId:", result.requestId);
  console.log("expanded_prompt:", result.data.expanded_prompt);

  const out = "scene2-clips/c07_inception_exchange.mp4";
  await download(result.data.video.url, out);
  console.log("Saved:", out);
  console.log("\nCost check:");
  console.log(`  cd fal-tools/browser && node get_request_cost.js fal-ai/minimax-h3-turbo/image-to-video ${result.requestId}`);
}

main().catch((err) => { console.error(err); process.exit(1); });
