// Scene 4, Beat 1 -- video clips via fal-ai/minimax-h3-turbo/image-to-video, 768P, per
// .agents/rules/fal_video_model_rules.md. One clip per row of SCENE4_SHOT_LIST.md's Beat
// 1 table. s4_10 is the one exception: it is a mid-line continuation of s4_09's speech
// and MUST chain from s4_09's real rendered last frame (per
// .agents/rules/location_continuity_rules.md), never from an independently composited
// still -- this script extracts that frame with ffmpeg automatically once s4_09 exists.
//
//   node run_scene4_beat1_video_batch.js [slug ...]      -- omit args to run every shot
//
// Resumable: skips any slug whose output .mp4 already exists.

const path = require("path");
const fs = require("fs");
const https = require("https");
const { execFileSync } = require("child_process");
const { fal } = require("./client");

const STILLS = "scene4-stills";
const CLIPS = "scene4-clips";
const LASTFRAMES = path.join(CLIPS, "lastframes");

const CAST = 'JAN is 52, overweight, thinning grey-brown side-parted hair, in the same too-tight dark navy suit jacket over a PALE BLUE shirt with a DARK RED tie, now visibly creased and slept-in, shirt buttoned one button crooked, tie loosened further askew. He wears a large white FOAM NECK BRACE around his neck and chin, and a small plaster above one eyebrow. CHRISTINA DROSS is 38, slim, sleek dark brown bob with a blunt fringe, tailored charcoal blazer over a cream blouse, cold and controlled.';
const LOOK = 'Photoreal live-action comedy, 35mm lens, natural daylight, handheld-steady camera. Keep every face, costume and the set exactly as in the reference frame -- do not change the camera framing from the start frame unless the action explicitly describes movement.';
const NOTEXT = 'No on-screen text, captions or subtitles.';

const shots = [
  { slug: "s4_01_neckbrace_establish", duration: 5,
    action: "Jan sits alone behind his desk, compulsively squeezing a stress ball in a slow steady rhythm, staring blankly ahead, dazed. Christina pushes open the glazed door on the left and walks steadily and naturally across the room, arriving at the near side of the desk by the end of the clip, a closed manila document folder against her chest (not a tablet, not a laptop), coffee in her other hand, eyes fixed on Jan with cool appraisal. She has FULLY CROSSED THE ROOM and is already standing at the desk in the final frame -- not still near the door.",
    dialogue: null,
    audio: "Quiet office room tone, the soft rhythmic squeeze of the stress ball, the door latch and Christina's footsteps entering." },

  { slug: "s4_02_alive_then", duration: 14, chainFrom: "s4_01_neckbrace_establish",
    action: "Continuing in ONE continuous unbroken shot from the previous frame -- no cut, and Christina does NOT move or travel any further; she is already standing at the desk right where the previous frame left her. She looks at Jan with flat unimpressed appraisal. Jan looks up at her from his stress ball, slightly indignant. As they begin talking, the camera slowly and gently pushes in toward Jan, gradually settling into a closer over-the-shoulder framing on him by partway through the clip -- a small, smooth camera move only, not a large repositioning. Jan launches into his explanation, gesturing with one hand while the other still holds a stress ball, chin lifted with wounded dignity.",
    dialogue: 'CHRISTINA (flat): "You\'re alive then. Shame." JAN (wounded): "It takes more than eight thousand volts to put Jan Peach down, Christina. I\'ve decided to reframe it internally as a live team-cohesion stress-test. Very on-brand for Inception, if you think about it."',
    audio: "Office room tone, Christina's low heels settling on the floor, the faint squeak of the stress ball." },

  { slug: "s4_03_forty_witnesses", duration: 13, chainFrom: "s4_02_alive_then",
    action: "Continuing in ONE continuous unbroken shot from the previous frame -- no cut. This is a SMALL, SUBTLE camera move only -- barely more than a refocus, NOT a pan or swing to a new angle. The camera does not rotate, arc, or reveal any new geography at all: keep the exact same background elements in the exact same positions as the previous frame (the same triangular feature wall and bookshelf, if visible there; if the previous frame showed a bookshelf close behind Jan, that same bookshelf stays exactly there). Absolutely do NOT cut to or reveal a corridor, glass meeting-room walls, wooden doors, or any office area -- this shot stays inside Jan's office only, tight on the two of them. Christina does not move her feet; she stays exactly where she is standing, holding the SAME closed manila document folder against her chest throughout -- it does not disappear. She shifts the folder to one arm, freeing her other hand to tick a point off on one raised finger as she lists off witnesses, completely deadpan. Jan's visible profile in the foreground looks increasingly ill as she talks, then delivers his flippant reply with a small dismissive shrug.",
    dialogue: 'CHRISTINA (deadpan): "Rick tasered you in front of forty witnesses, the canteen\'s insurance assessor, and a man from Environmental Health who was only there about the extractor fan." JAN: "Yes, well. Nolan films are famously misunderstood on first viewing."',
    audio: "Quiet office room tone only." },

  { slug: "s4_04_crumb_ratio", duration: 13, chainFrom: "s4_03_forty_witnesses",
    action: "Continuing the exact same held shot with no cut -- Christina continues, unimpressed, recounting the incident flatly. Jan's visible profile brightens slightly with an odd, proud half-smile as he asks his question, genuinely curious rather than ashamed.",
    dialogue: 'CHRISTINA: "It wasn\'t a film, Jan. You threw a chair through a window and collapsed face-first into a tray of pain au chocolat crumbs." JAN (pause, proud): "Did I get a good crumb-to-face ratio? I don\'t remember that part."',
    audio: "Quiet office room tone only." },

  { slug: "s4_05_for_the_file", duration: 5,
    action: "Christina answers flatly, then Jan's eyes go wide with sudden panic, mouth open, both hands freezing around the stress ball, leaning forward.",
    dialogue: 'CHRISTINA: "Ninety percent coverage. HR has photos. For the file." JAN (sudden panic): "There\'s a FILE?!"',
    audio: "Quiet office room tone only." },

  { slug: "s4_06_keynote_offer", duration: 11, chainFrom: "s4_05_for_the_file",
    action: "Continuing in ONE continuous unbroken shot from the previous frame -- no cut, and NO ROTATING away from the desk area. The camera simply pulls back a little and reframes slightly sideways to bring more of Christina into frame -- the SAME triangular black-white-red feature wall and the SAME built-in bookshelf stay visible in the background throughout, just seen from a little further away. Do not reveal a window wall, a different door, or any part of the room not already visible in the previous frame. Jan remains seated at the desk in the background, small and soft-focused, still in front of the triangular wall. As the camera settles, Christina recites an escalating list off an invisible mental checklist, completely deadpan, gesturing minutely as if counting.",
    dialogue: 'CHRISTINA: "There\'s several. Legal opened one. So did the landlord. So did, somehow, a man on LinkedIn calling himself a \'workplace culture strategist\' who is already offering us a keynote."',
    audio: "Quiet office room tone only." },

  { slug: "s4_07_book_him", duration: 9, chainFrom: "s4_06_keynote_offer",
    action: "Continuing in ONE continuous unbroken shot from the previous frame -- no cut. Both people are calm and mostly still. Christina remains standing exactly where she was, arms loosely folded, not moving her feet. Jan remains seated and relaxed behind the desk, unmoving from the waist down, resting back in his chair -- he smiles faintly and gives one small pointing gesture with a single hand and a small nod of his head. That is the only movement he makes. The camera pans gently from Christina back toward Jan.",
    dialogue: 'JAN (brightening): "Book him." CHRISTINA: "Jan." JAN: "BOOK. HIM. If a man on the internet believes I have \'culture,\' I am not going to be the one to argue."',
    audio: "Quiet office room tone only." },

  { slug: "s4_08_own_facilities", duration: 5,
    action: "Christina, arms folded, a closed manila document folder under one arm (not a tablet, not a laptop), delivers the line flatly to Jan seated small in the background behind the desk.",
    dialogue: 'CHRISTINA (flat): "There\'s also the small matter of you being tasered by your own Head of Facilities."',
    audio: "Quiet office room tone only." },

  { slug: "s4_09_risk_management", duration: 13,
    action: "Jan, in medium close-up, launches into an expansive self-justifying rationalization, both hands spread, chin raised despite the neck brace, working himself up to sound reasonable, gathering steam as he goes.",
    dialogue: 'JAN: "Rick was well within his rights. I was clearly out of control. I could\'ve seriously injured myself on that second chair, and then where would this company be? Chairless AND Jan-less. It\'s called risk management. I invented it. Well -- not invented."',
    audio: "Quiet office room tone only.",
    timing: "He must still be mid-sentence, mouth open, on the final frame -- this speech continues directly into the next clip. Do not let him reach a natural conclusion or close his mouth by the end." },

  { slug: "s4_10_studied_mba", duration: 5, chainFrom: "s4_09_risk_management",
    action: "Jan continues the exact same sentence without any beat or pause, correcting himself mid-thought, one hand raised as if catching himself.",
    dialogue: 'JAN (cont., correcting himself): "Studied. At my MBA."',
    audio: "Quiet office room tone only." },

  { slug: "s4_11_made_up_place", duration: 9,
    action: "Wide two-shot, both Jan and Christina fully visible, leaning toward each other over the desk in a rapid back-and-forth volley -- Jan gesturing indignantly each time he speaks, Christina replying instantly and flatly each time. Comic rhythm; the camera itself holds still throughout.",
    dialogue: 'CHRISTINA (flat): "The University of Made Up Place." JAN (through gritted teeth): "Buckinghamshire College of Advanced Enterprise Studies." CHRISTINA: "Which closed in 2011." JAN: "Which closed WELL. With dignity. Unlike this canteen window."',
    audio: "Quiet office room tone only." },

  { slug: "s4_12_incident_form", duration: 9,
    action: "Christina stands at the desk delivering her line, holding a closed manila document folder flat against her chest (not a tablet, not a laptop), completely unbothered and matter-of-fact. She does NOT walk toward the door and does NOT leave the room in this clip -- she remains standing in roughly the same spot throughout, near the desk, facing Jan. Camera does not follow her anywhere; there is no exit.",
    dialogue: 'CHRISTINA: "Speaking of which -- HR needs you to complete an Incident Reflection Form before you\'re cleared to re-enter any room with furniture in it."',
    audio: "Quiet office room tone only." },

  { slug: "s4_13_give_it_here", duration: 5,
    action: "Jan sighs and extends one open hand across the desk toward Christina, resigned. Christina opens the closed manila folder she has been carrying this whole scene and draws out THE DOCUMENT -- a stapled bundle of roughly fourteen off-white A4 pages, about 5-6mm thick, a single silver staple through the top-left corner, slightly curled page corners -- handing it across the desk to Jan. The now-empty folder is tucked under her other arm. A beat later Jan's eyes widen in fresh alarm as he registers its thickness.",
    dialogue: 'JAN (sighing): "Fine. Give it here." CHRISTINA: "It\'s fourteen pages." JAN: "FOURTEEN?! For a taser?!"',
    audio: "Quiet office room tone, the rustle/thump of the document changing hands." },

  { slug: "s4_14_relationship_authority", duration: 8, chainFrom: "s4_13_give_it_here",
    action: "Continuing in ONE continuous unbroken shot from the previous frame -- no cut, and NO ROTATING away from the desk area -- the SAME triangular feature wall and bookshelf stay visible, do not reveal a window wall or any part of the room not already visible. The camera pulls back a little and reframes slightly to bring more of Christina into view. She holds the empty manila folder under one arm and gestures toward the document -- the EXACT SAME physical document Jan is now holding, same thickness, same curled corners, unchanged -- with clinical bureaucratic calm as she explains its contents. Jan, small in the background, stares down at that same document in dawning horror as he flips through it.",
    dialogue: 'CHRISTINA (clinical): "Page one is the taser. Pages two through fourteen are follow-up questions about your \'relationship with authority,\' prompted by page one."',
    audio: "Quiet office room tone, the soft rustle of turning pages." },

  { slug: "s4_15_coversheet_memo", duration: 8, chainFrom: "s4_14_relationship_authority",
    action: "Continuing in ONE continuous unbroken shot from the previous frame -- no cut, and NO ROTATING to reveal any part of the room not already established (the same triangular wall, bookshelf and glazed door area). The camera pulls back further to a wide two-shot. Jan mutters down at the SAME document -- unchanged thickness -- defeated, one hand rubbing his forehead near the plaster. Christina, folder still under one arm, steps away toward the glazed door on the left and delivers her closing line back over her shoulder without breaking stride, then exits through the door, pulling it most of the way closed behind her.",
    dialogue: 'JAN (muttering): "This is worse than the coversheet memo." CHRISTINA (leaving, over her shoulder): "Everything is worse than the coversheet memo, Jan. That\'s why we keep sending it."',
    audio: "Quiet office room tone, Christina's footsteps receding, the door clicking mostly shut at the very end." },
];

function ffmpegBin() {
  try {
    return execFileSync(process.platform === "win32" ? "where" : "which", ["ffmpeg"]).toString().split(/\r?\n/)[0].trim();
  } catch { return "ffmpeg"; }
}

function extractLastFrame(clipSlug) {
  const src = path.join(CLIPS, `${clipSlug}.mp4`);
  if (!fs.existsSync(src)) throw new Error(`cannot chain: ${src} does not exist yet -- generate it first`);
  const out = path.join(LASTFRAMES, `${clipSlug}_last.png`);
  fs.mkdirSync(LASTFRAMES, { recursive: true });
  execFileSync(ffmpegBin(), ["-y", "-sseof", "-0.5", "-i", src, "-update", "1", "-frames:v", "1", "-q:v", "2", out], { stdio: "pipe" });
  console.log(`  extracted last frame: ${out}`);
  return out;
}

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
  const only = process.argv.slice(2);

  for (const shot of shots) {
    if (only.length && !only.includes(shot.slug)) continue;
    const dest = path.join(CLIPS, `${shot.slug}.mp4`);
    if (fs.existsSync(dest)) { console.log(`[skip] ${shot.slug} already exists`); continue; }

    const startImagePath = shot.chainFrom ? extractLastFrame(shot.chainFrom) : path.join(STILLS, `${shot.slug}.png`);
    if (!fs.existsSync(startImagePath)) { console.error(`[FAIL] ${shot.slug}: missing start image ${startImagePath}`); continue; }

    const prompt = [
      LOOK, CAST,
      `ACTION: ${shot.action}`,
      shot.dialogue ? `DIALOGUE: ${shot.dialogue}` : "No dialogue in this clip.",
      `AUDIO: ${shot.audio}`,
      shot.timing ? `TIMING: ${shot.timing}` : "",
      NOTEXT,
    ].filter(Boolean).join(" ");

    console.log(`\n=== ${shot.slug} (${shot.duration}s${shot.chainFrom ? ", chained from " + shot.chainFrom : ""}) ===`);
    try {
      const startUrl = await resolveImage(startImagePath);
      const result = await fal.subscribe("fal-ai/minimax-h3-turbo/image-to-video", {
        input: { prompt, image_url: startUrl, duration: shot.duration, resolution: "768P", prompt_expansion_mode: "balanced", enable_safety_checker: false },
        logs: true,
        onQueueUpdate: (u) => { if (u.status === "IN_PROGRESS") (u.logs || []).forEach((l) => console.log("  ", l.message)); },
      });
      await download(result.data.video.url, dest);
      console.log(`[ok] ${shot.slug} -> ${dest} (requestId ${result.requestId})`);
    } catch (e) {
      console.error(`[FAIL] ${shot.slug}: ${e.message}`);
    }
  }
}

main().catch((err) => { console.error(err); process.exit(1); });
