// c10_get_back_to_work -- Shot 09-2: "now GET BACK TO WORK!" -- last shot of the scene.
// CHAINS from c09's real last frame, NOT the independently adopted shot09_2_50k_outburst.png
// still. Jan's whole "Yes groan all you like... now GET BACK TO WORK!" speech is one
// unbroken block in the fountain, split into c09/c10 only for fal's 15s cap -- same pattern
// as c05/c06 and c07/c08/c09. See .agents/rules/location_continuity_rules.md.

const path = require("path");
const fs = require("fs");
const https = require("https");
const { fal } = require("./client");

const CAST = 'JAN is 52, overweight, thinning greying hair, too-tight navy suit over a white shirt with the tie loosened askew, shirt re-buttoned crookedly. CHRIS is 32, lean, dark hair, LIGHT BLUE shirt with rolled sleeves and tan chinos. The crowd are British office workers in smart-casual clothes with lanyards, exactly as shown in the reference frame -- keep every crowd member\'s face, hair and outfit exactly as reference, do not invent new people or remove anyone.';
const LANG = 'ALL SPOKEN DIALOGUE IS IN ENGLISH, spoken by British characters with British accents. Do not speak, sing or caption any other language. No Mandarin, no Chinese.';
const LOOK = 'Photoreal live-action comedy, 35mm lens, natural office daylight, handheld-steady camera. Keep every face, costume and the set exactly as in the reference frame. No on-screen text, captions or subtitles.';
const FRAMING = 'CAMERA: fixed static shot size and position, matching the reference frame exactly for the entire clip. Do NOT push in, zoom, cut, or change angle at any point. Only gentle handheld life (small natural shake) is allowed.';

const prompt = [
  LOOK, CAST, LANG, FRAMING,
  'ACTION: begin exactly on the reference frame -- continuing directly, no cut. Jan escalates from smug calm into a full bellow -- fist raised, face flushing deep red, sweat at his hairline, mouth wide. The crowd recoil and immediately start turning away to their desks, some wincing, some with heads in hands, breaking apart and dispersing fast in every direction down the corridor and into the open-plan desks. By the end Jan is left standing alone in the middle of the floor, chest heaving, as the room empties around him.',
  'DIALOGUE: @Jan (speaking then bellowing in an English Home Counties accent): "I will let you know when more information is available, now GET BACK TO WORK!"',
  'AUDIO: his shout, then chairs scraping and footsteps as people disperse fast, fading into quiet office ambience.',
  'TIMING: the shout lands at about 6 seconds. USE the final 4 seconds for the crowd breaking up and hurrying back to their desks, leaving Jan alone, chest heaving, camera unchanged. This is the last shot of the scene, so let it breathe. No further dialogue.',
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
  const startUrl = await resolveImage("scene2-clips/lastframes/c09_groans_last.png");

  const input = {
    prompt,
    image_url: startUrl,
    duration: 10,
    resolution: "768P",
    prompt_expansion_mode: "balanced",
    enable_safety_checker: false,
  };

  console.log("\nSubmitting c10_get_back_to_work (chained from c09's last frame)...\n");
  const result = await fal.subscribe("fal-ai/minimax-h3-turbo/image-to-video", {
    input, logs: true,
    onQueueUpdate: (u) => { if (u.status === "IN_PROGRESS") (u.logs || []).forEach((l) => console.log("  ", l.message)); },
  });

  console.log("\nrequestId:", result.requestId);
  console.log("expanded_prompt:", result.data.expanded_prompt);

  const out = "scene2-clips/c10_get_back_to_work.mp4";
  await download(result.data.video.url, out);
  console.log("Saved:", out);
  console.log("\nCost check:");
  console.log(`  cd fal-tools/browser && node get_request_cost.js fal-ai/minimax-h3-turbo/image-to-video ${result.requestId}`);
}

main().catch((err) => { console.error(err); process.exit(1); });
