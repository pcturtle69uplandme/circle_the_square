// c04_shut_up -- Shot 07b-2: sniggering ripples, Jan flares up.
// ACCEPTED TAKE chains from c03's real last frame. A fresh-still take from
// shot07b2_shut_up_flareup.png was tried instead (avoiding drift) but rejected: that
// still is a frontal composite with Jan facing the camera almost directly, which reads
// as breaking the fourth wall once animated -- see scene2-clips/superseded/
// c04_shut_up_frontal_REJECTED_looking_at_camera.mp4. Chaining a short 1-2 link hop
// (c03->c04) is an acceptable trade-off here; the long-chain drift concern applies to
// longer sequences, not this length. RULE: never pick a start image/still where a
// character looks directly at camera -- prefer a fresh nano-banana-pro/GPT Image 2
// composite (character refs + location plate, posed off-camera) over both a
// camera-facing still and a long chain.

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
  'ACTION: begin exactly on the reference frame -- Jan pleased with himself, the crowd around him. Quiet sniggering spreads through the crowd person to person -- one snorts, another claps a hand over their mouth, shoulders shaking, people glancing at each other, all trying and failing not to laugh at him. Jan\'s face darkens and reddens as he notices and watches it spread, then he erupts, both hands raised and open in exasperation. The laughter cuts dead instantly. Jan does not move from his spot.',
  'DIALOGUE: @Jan (shouting in a furious English Home Counties accent): "SHUT UP! I am truly appalled by the lack of discipline in this place and that changes now! I have decided a new project is required to manage all the change around here."',
  'AUDIO: suppressed sniggering building and spreading, then abrupt total silence the instant he shouts. His voice echoes slightly off the hard floor.',
  "TIMING: the dialogue ends at about 12 seconds. HOLD the final 3 seconds on total frozen silence -- Jan breathing hard and glaring, the crowd rigid and not daring to move, camera unchanged. No further dialogue, no new action.",
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
  const startUrl = await resolveImage("scene2-clips/lastframes/c03_jan_addresses_last.png");

  const input = {
    prompt,
    image_url: startUrl,
    duration: 15,
    resolution: "768P",
    prompt_expansion_mode: "balanced",
    enable_safety_checker: false,
  };

  console.log("\nSubmitting c04_shut_up (fresh still, cut from c03)...\n");
  const result = await fal.subscribe("fal-ai/minimax-h3-turbo/image-to-video", {
    input, logs: true,
    onQueueUpdate: (u) => { if (u.status === "IN_PROGRESS") (u.logs || []).forEach((l) => console.log("  ", l.message)); },
  });

  console.log("\nrequestId:", result.requestId);
  console.log("expanded_prompt:", result.data.expanded_prompt);

  const out = "scene2-clips/c04_shut_up.mp4";
  await download(result.data.video.url, out);
  console.log("Saved:", out);

  console.log("\nCost check:");
  console.log(`  cd fal-tools/browser && node get_request_cost.js fal-ai/minimax-h3-turbo/image-to-video ${result.requestId}`);
}

main().catch((err) => { console.error(err); process.exit(1); });
