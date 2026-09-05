// c09_groans -- Shot 09-1: the crowd groans, Jan justifies the £50k.
// CHAINS from c08's real last frame, NOT the independently adopted shot09_1_groans.png
// still. The fountain has no scene/beat break between c08's ending and "GROANS echo from
// the crowd" -- it's the same continuous beat (Jan's merch reveal lands, the crowd groans
// at it), same people already on screen (Jan, Chris, crowd). Chain, per
// .agents/rules/location_continuity_rules.md.

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
  'ACTION: begin exactly on the reference frame -- continuing directly, no cut, straight from the crowd\'s stunned reaction to Jan\'s reveal. The stunned silence breaks into a groan -- heads tipping back, eyes rolling, hands rubbing faces, arms folding, shoulders slumping. Weary rather than angry. Jan faces them entirely untroubled, raising one hand palm-down to quiet them, wearing a small self-satisfied smile, and talks straight over the noise.',
  'DIALOGUE: @Jan (speaking in a smug English Home Counties accent): "Yes groan all you like, but I am the one with the most talent and skills to deliver this. It will add fifty thousand pounds to my salary as I simply add this role into my duties."',
  'AUDIO: a loud collective groan opening the clip, subsiding into resentful muttering under his line.',
  'TIMING: the dialogue ends at about 13 seconds. HOLD the final 2 seconds on Jan\'s self-satisfied face over the resentful muttering, camera unchanged. No further dialogue.',
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
  const startUrl = await resolveImage("scene2-clips/lastframes/c08_merch_gag_last.png");

  const input = {
    prompt,
    image_url: startUrl,
    duration: 15,
    resolution: "768P",
    prompt_expansion_mode: "balanced",
    enable_safety_checker: false,
  };

  console.log("\nSubmitting c09_groans (chained from c08's last frame)...\n");
  const result = await fal.subscribe("fal-ai/minimax-h3-turbo/image-to-video", {
    input, logs: true,
    onQueueUpdate: (u) => { if (u.status === "IN_PROGRESS") (u.logs || []).forEach((l) => console.log("  ", l.message)); },
  });

  console.log("\nrequestId:", result.requestId);
  console.log("expanded_prompt:", result.data.expanded_prompt);

  const out = "scene2-clips/c09_groans.mp4";
  await download(result.data.video.url, out);
  console.log("Saved:", out);
  console.log("\nCost check:");
  console.log(`  cd fal-tools/browser && node get_request_cost.js fal-ai/minimax-h3-turbo/image-to-video ${result.requestId}`);
}

main().catch((err) => { console.error(err); process.exit(1); });
