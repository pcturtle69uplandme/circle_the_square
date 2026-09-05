// c06_naming_inception -- Shot 07c-2: Jan finishes justifying and names the project.
// CHAINS from c05's real last frame, NOT the independently adopted shot07c2 still. Jan's
// justification-into-naming is one unbroken speech in the fountain (L122) split into two
// clips only for fal's 15s cap -- there is no scene/beat break here. An earlier take used
// shot07c2_naming_inception.png (a different, wider angle by Jan's office door) reasoned
// as an intentional reveal cut; it rendered and passed QA but read as Jan warping to a new
// shot mid-sentence, since the script never cuts here. See
// .agents/rules/location_continuity_rules.md ("Never let a still-speaking character warp
// to a different shot mid-line"). Wasted a render -- redone chained here.
//
// Because we're chaining from c05's actual pose (still mid-explanation, not yet raising
// his arm), the ACTION arc restores the original "gathers pomposity, then builds to" the
// triumphant announcement -- there IS room to build to now that we start from the real
// pre-announcement frame instead of one that had already skipped to the landed pose.
//
// v2: c07's accepted take (the shot08a/shot08b keyframe pair) never included RICK, which
// read as him vanishing between c06 and c07. A composited fix for c07 itself broke worse
// (wrong aspect ratio, voice swap -- see run_c07_inception_exchange_v2_REJECTED.js), so
// instead this clip now has Rick write HIMSELF out: unimpressed by the whole announcement,
// he turns and walks off during the silent hold, so he's already gone by c06's last frame
// and his absence at the start of c07 is a motivated exit, not an unexplained cut. v1 kept
// at scene2-clips/superseded/c06_naming_inception_v1_kept_as_fallback.mp4 in case this
// doesn't land cleanly.

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
  'ACTION: begin exactly on the reference frame -- continuing directly from Jan\'s explanation, mid-conversation, no cut. Jan gathers pomposity as he keeps talking, chest puffing up, then builds to the announcement -- one arm raising high and presenting, palm open, beaming as if unveiling a moon landing. Rick stays arms folded beside him at first, staring flatly, entirely unimpressed. The rest of the crowd\'s reaction is flat and unenthused throughout and does not change.',
  'DIALOGUE: @Jan (speaking in a pompous English Home Counties accent): "I know because I see everything happening so am best placed to judge. We need a new project to continue the success of the previous project. So I have decided to call the project... Inception."',
  'AUDIO: dead silence on the announcement -- no applause, no reaction at all from the crowd, which is the joke. Rick\'s footsteps as he walks off.',
  'TIMING: the dialogue ends at about 13 seconds. For the final 2 seconds: the crowd stays frozen in silence, nobody reacts to the name -- except RICK, who exhales, unfolds his arms, shakes his head slightly, turns his back on Jan and walks away down the corridor toward the far end, out of frame, done with the whole thing. He is fully out of shot by the very last frame. Camera does not move. No further dialogue.',
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
  const startUrl = await resolveImage("scene2-clips/lastframes/c05_rick_questions_last.png");

  const input = {
    prompt,
    image_url: startUrl,
    duration: 15,
    resolution: "768P",
    prompt_expansion_mode: "balanced",
    enable_safety_checker: false,
  };

  console.log("\nSubmitting c06_naming_inception (chained from c05's last frame)...\n");
  const result = await fal.subscribe("fal-ai/minimax-h3-turbo/image-to-video", {
    input, logs: true,
    onQueueUpdate: (u) => { if (u.status === "IN_PROGRESS") (u.logs || []).forEach((l) => console.log("  ", l.message)); },
  });

  console.log("\nrequestId:", result.requestId);
  console.log("expanded_prompt:", result.data.expanded_prompt);

  const out = "scene2-clips/c06_naming_inception.mp4";
  await download(result.data.video.url, out);
  console.log("Saved:", out);
  console.log("\nCost check:");
  console.log(`  cd fal-tools/browser && node get_request_cost.js fal-ai/minimax-h3-turbo/image-to-video ${result.requestId}`);
}

main().catch((err) => { console.error(err); process.exit(1); });
