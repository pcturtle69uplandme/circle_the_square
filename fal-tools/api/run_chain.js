// The story-flow rule: clips that continue the same action chain from the PREVIOUS
// clip's real last frame (extracted with ffmpeg), never a manufactured end_image_url.
// That is what guarantees zero jump cuts between clips that are meant to read as one
// continuous scene -- whatever pixels end clip N are exactly what starts clip N+1.
//
// This chains three shots for Scene 2's blinds/Sharon-exit beat:
//   c01 (Chris+Rick gossip, camera LOCKED wide -- the previous c01 take drifted into an
//        extreme close-up and lost the door from frame, which is exactly what NOT to do
//        when the next clip needs that same door in view)
//   -> c02_blinds_sharon (Sharon raises the blinds from inside and is glimpsed doing it,
//        Jan dressing behind her, door opens)
//   -> c02b_sharon_exits (Sharon walks out toward camera, Chris/Rick react)
//
// Usage: node run_chain.js

const path = require("path");
const fs = require("fs");
const https = require("https");
const { execFileSync } = require("child_process");
const { fal } = require("./client");

const CAST = 'JAN is 52, overweight, thinning greying hair, too-tight navy suit over a white shirt with the tie loosened askew, shirt re-buttoned crookedly. CHRIS is 32, lean, dark hair, LIGHT BLUE shirt with rolled sleeves and tan chinos. RICK is 40, broad, greying near-buzzcut, plain GREY POLO. SHARON is a woman with shoulder-length wavy AUBURN/RED hair, wearing a JEWEL-TONE TEAL/DARK-GREEN silky short-sleeve blouse and a BLACK PENCIL SKIRT, black heels, NO cardigan, NO jacket, NO lanyard or ID badge. Nobody else appears in shot -- no other background characters, no extras.';
const LANG = 'ALL SPOKEN DIALOGUE IS IN ENGLISH, spoken by British characters with British accents. Do not speak, sing or caption any other language. No Mandarin, no Chinese.';
const LOOK = 'Photoreal live-action comedy, 35mm lens, natural office daylight. Keep every face, costume and the set exactly as in the reference frame. No on-screen text, captions or subtitles.';

const STEPS = [
  {
    name: "c01_corridor_gossip",
    startImage: "scene2-stills/shot06_corridor_gossip.png",
    duration: 10,
    prompt: [
      LOOK, CAST, LANG,
      'CAMERA: LOCKED wide two-shot, framing exactly as the reference frame for the ENTIRE clip -- the glazed office door and its closed blinds, and both Chris and Rick full-figure, must all stay visible in frame from the first second to the last. Do NOT push in, zoom, or drift to a tighter framing at any point -- this is a hard rule, not a suggestion. Only the smallest natural handheld shake is allowed.',
      'ACTION: Chris and Rick stand in the corridor beside the glazed office door. The door stays shut, its venetian blinds closed flat and opaque throughout -- nothing inside is ever visible. Chris tilts his head toward the shut door as he speaks, exasperated and amused. Rick does not react at all, arms folded, staring flatly ahead -- his complete lack of reaction is the joke.',
      'DIALOGUE: @Chris (dry, wry South London Estuary English accent): "Christ! They don\'t even try to hide it any more do they." Then @Rick (completely flat monotone, dead motionless face, only his mouth moves): "Never have. Give it another five minutes."',
      'AUDIO: quiet open-plan office ambience -- distant keyboards, a phone ringing far off. No music.',
      "TIMING: dialogue occupies the first 8 seconds. HOLD the final 2 seconds on Rick's blank deadpan, camera framing unchanged. No further dialogue, no new action.",
    ].join(' '),
  },
  {
    name: "c02_blinds_sharon",
    startImage: null, // filled in from previous step's last frame
    duration: 8,
    prompt: [
      LOOK, CAST, LANG,
      'CAMERA: begin exactly on the reference frame\'s framing. A gentle, slow, controlled pull-back is allowed as the blinds rise, to reveal a little more of the door -- small amplitude only, no whip pans, no push-in, never so much that Chris or Rick leave frame.',
      'ACTION, IN THIS EXACT ORDER: (1) hold on the corridor exactly as the reference frame, door shut, blinds closed flat and opaque, Chris and Rick standing where the reference frame puts them. (2) The venetian blinds are physically RAISED from inside -- they visibly fold and stack upward slat by slat like real venetian blinds being pulled up on their cord, NOT fading or turning transparent. SHARON is the one raising them: her hand and arm become visible pulling the blind cord as the slats fold up, and as they rise she becomes visible standing just inside the glass. (3) Behind and beside her, JAN is visible inside the office, red-faced and out of breath, hurriedly tucking his shirt back into his trousers and doing up his jacket button, straightening his tie -- he does not look out. (4) Once the blinds are fully up, Sharon opens the door and steps into the doorway, one hand still on the door handle, pausing there. Chris and Rick turn their heads toward the movement but DO NOT WALK OR CHANGE POSITION.',
      'DIALOGUE: none. Nobody speaks.',
      'AUDIO: the real mechanical rattle and clack of venetian blinds being pulled up slat by slat, then a door latch turning and the door opening.',
    ].join(' '),
  },
  {
    name: "c02b_sharon_exits",
    startImage: null,
    duration: 8,
    prompt: [
      LOOK, CAST, LANG,
      'CAMERA: fixed static shot size and position, matching the reference frame exactly for the entire clip. Do NOT push in, zoom, cut, or change angle. Only gentle handheld life (small natural shake) is allowed.',
      'ACTION: begin exactly on the reference frame -- Sharon in the doorway, hand on the handle, Jan visible seated/standing inside still composing himself, Chris and Rick in the corridor. Sharon steps fully out of the doorway and walks away down the corridor toward camera in one continuous, steady, uninterrupted stride -- she never pauses, reverses or repositions -- smoothing her creased blouse and pushing her mussed hair back, eyes down, dazed but trying to compose herself, hair visibly disheveled, a light sheen of sweat. Jan stays where the reference frame puts him, visibly flushed and sweating, and does not look out. CHRIS AND RICK DO NOT MOVE OR WALK -- they stay exactly where the reference frame puts them and simply turn their heads to watch her pass, Chris smirking slightly, Rick impassive.',
      'DIALOGUE: none. Nobody speaks.',
      "AUDIO: quiet office ambience, Sharon's heels on carpet tile, and one quiet snigger from Chris as she passes.",
    ].join(' '),
  },
];

async function resolveImage(p) {
  const abs = path.resolve(p);
  const url = await fal.storage.upload(new Blob([fs.readFileSync(abs)]));
  console.log(`  uploaded ${p} -> ${url}`);
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

function extractLastFrame(videoPath, outPngPath) {
  fs.mkdirSync(path.dirname(outPngPath), { recursive: true });
  execFileSync("ffmpeg", ["-y", "-v", "error", "-sseof", "-0.15", "-i", videoPath, "-frames:v", "1", outPngPath]);
}

async function main() {
  const fromArgIdx = process.argv.indexOf("--from");
  const fromStep = fromArgIdx >= 0 ? process.argv[fromArgIdx + 1] : null;
  const startIdx = fromStep ? STEPS.findIndex((s) => s.name === fromStep) : 0;
  if (startIdx < 0) throw new Error(`--from ${fromStep}: no such step`);

  let nextStartUrl = null;
  if (startIdx > 0) {
    const prevLastFrame = `scene2-clips/lastframes/${STEPS[startIdx - 1].name}_last.png`;
    console.log(`Resuming from existing last frame: ${prevLastFrame}`);
    nextStartUrl = await resolveImage(prevLastFrame);
  }

  for (const step of STEPS.slice(startIdx)) {
    console.log(`\n=== ${step.name} ===`);
    const startUrl = step.startImage ? await resolveImage(step.startImage) : nextStartUrl;
    if (!startUrl) throw new Error(`${step.name}: no start image available`);

    const input = {
      prompt: step.prompt,
      image_url: startUrl,
      duration: step.duration,
      resolution: "768P",
      prompt_expansion_mode: "balanced",
      enable_safety_checker: false,
    };

    const result = await fal.subscribe("fal-ai/minimax-h3-turbo/image-to-video", {
      input, logs: true,
      onQueueUpdate: (u) => { if (u.status === "IN_PROGRESS") (u.logs || []).forEach((l) => console.log("  ", l.message)); },
    });

    console.log("requestId:", result.requestId);
    console.log("expanded_prompt:", result.data.expanded_prompt.slice(0, 400) + "...");

    const outVideo = `scene2-clips/${step.name}.mp4`;
    await download(result.data.video.url, outVideo);
    console.log("saved:", outVideo);
    console.log("cost check: cd fal-tools/browser && node get_request_cost.js fal-ai/minimax-h3-turbo/image-to-video " + result.requestId);

    const lastFramePath = `scene2-clips/lastframes/${step.name}_last.png`;
    extractLastFrame(outVideo, lastFramePath);
    console.log("last frame:", lastFramePath);
    nextStartUrl = await resolveImage(lastFramePath);
  }
}

main().catch((err) => { console.error(err); process.exit(1); });
