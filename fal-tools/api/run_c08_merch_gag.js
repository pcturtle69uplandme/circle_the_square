// c08_merch_gag -- Shot 08c: the branded merch box, and Jan appoints himself.
// CHAINS from c07's real last frame, NOT the independently adopted shot08c_merch_gag.png
// still. The fountain has no scene/beat break between Jan's "...it is also the name of
// this project" (end of c07) and "Will there be a lead for this?" (start of this clip) --
// it's the same continuous paragraph, same two people already on screen (Jan, Chris). Per
// .agents/rules/location_continuity_rules.md, that means chain, not cut to a fresh still.
//
// The merch box is a new PROP, not a new character, so it doesn't carry the identity-lock
// risk that blocked chaining for c07 (Chris wasn't in c06's last frame). Described in text
// only, referencing shot08c_merch_gag.png (kept as the intended look: cardboard box printed
// "PROJECT INCEPTION", foam stress balls / pens / folded t-shirts inside) rather than passed
// as a second image, since fal's image-to-video takes only one seed image when chaining.

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
  'ACTION: begin exactly on the reference frame -- continuing directly, no cut. On the desk beside Jan sits a large open cardboard box of branded merchandise -- foam stress balls, pens and folded t-shirts, all printed "PROJECT INCEPTION", the same printed boldly on the box itself. Jan glances down at it and his face falls as he realises he has already ordered a thousand of them and it is far too late to change the name. He gestures at the box with a caught-out, sheepish shrug. Chris, facing him, asks a straight question. Jan rallies into smugness, pauses deliberately, and delivers the reveal. The crowd draws breath.',
  'DIALOGUE: @Chris (speaking in a South London Estuary English accent): "Will there be a lead for this?" Then @Jan (speaking in a pompous English Home Counties accent, with a deliberate pause before the last two words): "At last something sensible is asked. Yes there will. However, it is with regret that I have to inform you all that the position has already been filled... by me."',
  'AUDIO: cardboard shifting as he gestures at the box; a collective intake of breath on the reveal.',
  'TIMING: the dialogue ends at about 14 seconds. HOLD the final 1 second on the crowd\'s stunned faces, camera unchanged. No further dialogue.',
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
  const startUrl = await resolveImage("scene2-clips/lastframes/c07_inception_exchange_last.png");

  const input = {
    prompt,
    image_url: startUrl,
    duration: 15,
    resolution: "768P",
    prompt_expansion_mode: "balanced",
    enable_safety_checker: false,
  };

  console.log("\nSubmitting c08_merch_gag (chained from c07's last frame)...\n");
  const result = await fal.subscribe("fal-ai/minimax-h3-turbo/image-to-video", {
    input, logs: true,
    onQueueUpdate: (u) => { if (u.status === "IN_PROGRESS") (u.logs || []).forEach((l) => console.log("  ", l.message)); },
  });

  console.log("\nrequestId:", result.requestId);
  console.log("expanded_prompt:", result.data.expanded_prompt);

  const out = "scene2-clips/c08_merch_gag.mp4";
  await download(result.data.video.url, out);
  console.log("Saved:", out);
  console.log("\nCost check:");
  console.log(`  cd fal-tools/browser && node get_request_cost.js fal-ai/minimax-h3-turbo/image-to-video ${result.requestId}`);
}

main().catch((err) => { console.error(err); process.exit(1); });
