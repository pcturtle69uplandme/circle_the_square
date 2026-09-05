// First real production test on the paid fal.ai API (fal-ai/minimax-h3-turbo/image-to-video).
// Merges c02a_blinds_raised + c02b_sharon_exits from fal-tools/browser/scene2_clips.js into
// ONE clip per the user's direction: blinds go up, door opens, Sharon exits dishevelled,
// Jan visible behind her flushed and still pulling himself together, Chris and Rick hold
// their positions in the corridor and react. All previously separate because the sandbox
// only allowed a single start image; the real API takes a first+last keyframe pair, so we
// can now do the whole beat in one clip: start = shot06 (blinds shut, Chris+Rick only),
// end = shot07 (blinds up, door open, Sharon mid-exit, Jan seated, Chris+Rick unmoved).

const path = require("path");
const { fal } = require("./client");
const fs = require("fs");
const https = require("https");

const CAST = 'JAN is 52, overweight, thinning greying hair, too-tight navy suit over a white shirt with the tie loosened askew, shirt re-buttoned crookedly. CHRIS is 32, lean, dark hair, LIGHT BLUE shirt with rolled sleeves and tan chinos. RICK is 40, broad, greying near-buzzcut, plain GREY POLO.';

const LANG = 'ALL SPOKEN DIALOGUE IS IN ENGLISH, spoken by British characters with British accents. Do not speak, sing or caption any other language. No Mandarin, no Chinese. There is no dialogue in this clip -- keep everyone silent, no mouths forming words.';

const LOOK = 'Photoreal live-action comedy, 35mm lens, natural office daylight, handheld-steady camera. Keep every face, costume and the set exactly as in the reference frames. No on-screen text, captions or subtitles.';

const prompt = [
  LOOK, CAST, LANG,
  'ACTION: begins exactly on the first reference frame -- the corridor, Chris and Rick standing beside the glazed office door, its venetian blinds closed flat and opaque, nothing inside visible, SHARON NOT YET VISIBLE ANYWHERE. Partway through, the blinds are RAISED from inside, folding up the glass and revealing the lit office interior. Behind the glass, JAN is caught still pulling himself together -- face flushed deep red and sweating, hurriedly tucking his shirt in and doing up his jacket button, straightening his loosened tie -- before he drops into his desk chair and sits, trying to look composed just as the door opens. The door handle turns and the door swings open, and ONLY THEN does SHARON first become visible, stepping out through the doorway. From the instant she appears, she walks in ONE single continuous, smooth, uninterrupted stride down the corridor toward camera, smoothing her creased blouse and pushing her mussed hair back, eyes down, dazed but trying to compose herself, hair visibly disheveled, a light sheen of sweat. HER MOTION MUST NEVER REVERSE, PAUSE, TELEPORT OR REPOSITION -- she does not flicker in and out of frame, does not step backward, does not jump to a different spot; she is a single continuous body moving forward at a steady walking pace from doorway to corridor for the entire remainder of the clip. CHRIS AND RICK DO NOT MOVE OR WALK -- they stay exactly where the first frame puts them and simply turn their heads to watch, Chris smirking slightly, Rick impassive. Ends exactly on the second reference frame: Jan seated inside at his desk not looking out, Sharon walking past Chris and Rick in the corridor.',
  'DIALOGUE: none. Nobody speaks a single word.',
  'AUDIO: quiet office ambience, then the distinct rattle and clack of a venetian blind being raised, a door latch turning, Sharon\'s heels on carpet tile, and one quiet snigger from Chris as she passes. No music, no speech.',
].join(' ');

async function resolveImage(p) {
  const abs = path.resolve(p);
  const buf = fs.readFileSync(abs);
  const blob = new Blob([buf]);
  const url = await fal.storage.upload(blob);
  console.log(`Uploaded ${p} -> ${url}`);
  return url;
}

function download(url, dest) {
  return new Promise((resolve, reject) => {
    fs.mkdirSync(path.dirname(dest), { recursive: true });
    const file = fs.createWriteStream(dest);
    https.get(url, (res) => {
      res.pipe(file);
      file.on("finish", () => file.close(resolve));
    }).on("error", (err) => {
      fs.unlink(dest, () => reject(err));
    });
  });
}

async function main() {
  const startUrl = await resolveImage("scene2-stills/shot06_corridor_gossip.png");
  const endUrl = await resolveImage("scene2-stills/shot07_sharon_exits.png");

  const input = {
    prompt,
    image_url: startUrl,
    end_image_url: endUrl,
    duration: 15,
    resolution: "768P",
    prompt_expansion_mode: "balanced",
    enable_safety_checker: false,
  };

  console.log("\nSubmitting c02_merged (blinds + Sharon exit)...\n");
  const result = await fal.subscribe("fal-ai/minimax-h3-turbo/image-to-video", {
    input,
    logs: true,
    onQueueUpdate: (update) => {
      if (update.status === "IN_PROGRESS") {
        (update.logs || []).map((l) => l.message).forEach((m) => console.log("  ", m));
      }
    },
  });

  console.log("\nrequestId:", result.requestId);
  console.log("expanded_prompt:", result.data.expanded_prompt);
  console.log("timings:", result.data.timings);
  console.log("video:", result.data.video);

  const out = "scene2-clips/c02_merged_blinds_sharon_exit_v2.mp4";
  await download(result.data.video.url, out);
  console.log("Saved:", out);

  console.log("\nTo confirm actual billed cost (the API returns none):");
  console.log(`  cd fal-tools/browser && node get_request_cost.js fal-ai/minimax-h3-turbo/image-to-video ${result.requestId}`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
