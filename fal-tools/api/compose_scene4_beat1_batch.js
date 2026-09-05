// Scene 4, Beat 1 -- remaining start-frame stills (s4_05 through s4_15, skipping s4_10:
// that clip is a mid-line continuation of s4_09's speech and must chain from s4_09's real
// rendered video last-frame per .agents/rules/location_continuity_rules.md, not from an
// independently composited still). s4_02/03/04 already done (s4_02 via fal, s4_03/04 via
// Flow, chained forward) -- this batch skips them via the on-disk check below.
//
// RE-GROUNDED ON THE ORIGINAL CHARACTER SHEETS, not chained forward from the previous
// shot -- the user opted to spend fal credits rather than risk compounding drift from
// chaining s4_05+ off s4_04 (itself chained off s4_03, off s4_01). Every shot here
// composites THREE references: Picture 1 = the s4_01 anchor (locks the neck brace,
// creased Day-3 wardrobe, PROJECT INCEPTION stress-ball pile, and room), Picture 2 =
// Jan's actual character-sheet image, Picture 3 = Christina's actual character-sheet
// image (both from character-refs/higgsfield/, the same files cast-bible.html shows).
//
// Framing alternates over-the-shoulder favoring whichever character carries more of
// that shot's dialogue, per the user's request for OTS start-position references; two
// shots (11, 15) are wide two-shots instead, for a rapid one-liner volley and an exit
// beat respectively.

const path = require("path");
const fs = require("fs");
const https = require("https");
const { fal } = require("./client");

const ANCHOR = "scene4-stills/s4_01_neckbrace_establish.png";
const JAN_REF = "character-refs/higgsfield/jan/jan_fullbody_neutral.png";
const CHRISTINA_REF = "character-refs/higgsfield/christina/christina_fullbody_neutral.png";

const PRESERVE = 'LOCATION AND CONTINUITY: reproduce Picture 1 exactly -- the same office (triangular feature wall, walnut desk with orange panel, built-in bookshelves, glazed door on the left), the same desk-front camera setup unless stated otherwise, JAN in the same white foam neck brace, the same creased pale-blue-shirt-and-dark-red-tie under the same too-tight navy suit jacket, the same chair-leg-shaped plaster on his forehead, the same pile of PROJECT INCEPTION stress balls on the desk, and CHRISTINA in the same charcoal blazer over a cream blouse with the same dark bob. JAN\'s exact face and build must match Picture 2. CHRISTINA\'s exact face and build must match Picture 3. Photoreal cinematic film still, 35mm lens, natural daylight. THIRD-PERSON SHOT, camera positioned across the room as an observer -- NOT a point-of-view shot. No on-screen text, captions, subtitles, or watermark.';

const shots = [
  {
    slug: "s4_02_alive_then",
    camera: "Over-the-shoulder shot FAVORING JAN: camera positioned just behind Christina's shoulder and head (soft, out-of-focus in the near foreground on the left), looking across the desk at Jan who fills the rest of the frame.",
    action: "Jan is mid-speech, one hand still holding a stress ball, gesturing slightly with the other, chin lifted, wounded and defensive dignity on his face as he explains himself. Christina's visible profile is utterly unimpressed.",
  },
  {
    slug: "s4_03_forty_witnesses",
    camera: "Over-the-shoulder shot FAVORING CHRISTINA: camera positioned just behind Jan's shoulder and head (soft, out-of-focus in the near foreground on the right), looking across the desk at Christina who fills the rest of the frame, now standing further into the room near the desk.",
    action: "Christina is mid-list, completely deadpan, ticking an invisible point off with one raised finger. Jan's visible profile looks faintly ill.",
  },
  {
    slug: "s4_04_crumb_ratio",
    camera: "Over-the-shoulder shot FAVORING CHRISTINA, same setup as the previous shot (behind Jan's shoulder looking at Christina).",
    action: "Christina describes the chair-through-the-window incident with total flatness, one eyebrow raised. Jan's visible profile has gone very still and thoughtful, about to ask something inappropriate.",
  },
  {
    slug: "s4_05_for_the_file",
    camera: "Over-the-shoulder shot FAVORING JAN, same setup as shot 2 (behind Christina's shoulder looking at Jan). CRITICAL -- there is only ONE Christina in this image, the soft out-of-focus shoulder/head in the foreground. The glazed door and the corridor beyond it must NOT be visible anywhere in this frame, so there is no second Christina standing in a doorway in the background. Single subject count: exactly one Jan, exactly one Christina.",
    action: "Jan's eyes have gone wide with sudden panic, mouth open mid-exclamation, both hands frozen around the stress ball he was squeezing, leaning forward slightly. Christina's visible profile watches him with weary patience.",
  },
  {
    slug: "s4_06_keynote_offer",
    camera: "Medium shot on Christina alone, camera positioned side-on to the desk, Christina in sharp focus with Jan visible small and soft-focused in the background behind the desk.",
    action: "Christina recites an escalating list off an invisible mental checklist, completely deadpan, gesturing minutely with one hand as if counting. She is enjoying this slightly more than she is letting on.",
  },
  {
    slug: "s4_07_book_him",
    camera: "Over-the-shoulder shot FAVORING JAN, same setup as shot 2 (behind Christina's shoulder looking at Jan). CRITICAL -- CHRISTINA IS STANDING, not sitting. She stands beside the desk exactly as in every other shot of this scene; there is no chair under her and she never sits down at any point in this scene.",
    action: "Jan's whole face has brightened, sitting up straighter despite the neck brace, one finger pointed decisively toward Christina, delighted with his own decision. Christina, standing, her visible profile has one eyebrow raised in silent warning.",
  },
  {
    slug: "s4_08_own_facilities",
    camera: "Medium shot on Christina alone, camera positioned side-on to the desk, same framing as shot 6.",
    action: "Christina delivers the line flatly, arms now folded, a closed manila document folder tucked under one arm (not a tablet, not a laptop), coffee cup set down on the desk edge. Jan is small and soft-focused behind her, slumping slightly.",
  },
  {
    slug: "s4_09_risk_management",
    camera: "Medium close-up on Jan alone, camera pushed in tighter than the earlier OTS shots, straight-on across the desk. Christina is visible only as a soft out-of-focus shape at the very edge of frame.",
    action: "Jan is mid-rationalization, both hands spread in an expansive, self-justifying gesture, chin raised despite the neck brace, working himself up to sounding reasonable. This is the START of a continuous speech that continues into the next clip -- his mouth is open mid-sentence, not at a natural pause.",
  },
  {
    slug: "s4_11_made_up_place",
    camera: "Wide two-shot holding BOTH Jan and Christina in frame together, camera pulled back to the desk-front master framing (matching Picture 1's original wide composition), for a rapid back-and-forth volley of short lines. CRITICAL -- JAN REMAINS SEATED in his desk chair the entire time, exactly as in Picture 1; he never stands up. Christina stands on the near side of the desk as usual.",
    action: "Jan and Christina are mid-volley, trading quick one-line jabs -- Jan seated, leaning forward across the desk from his chair and gesturing indignantly with one hand, Christina standing at the desk edge replying with flat, immediate put-downs, leaning slightly toward him with both hands pressed flat on the desk. Her closed manila document folder is set down flat on the desk in front of her hands -- clearly visible, the same folder she has been carrying all scene, not held right now because she needs both hands on the desk to lean in. Comic rhythm, both fully visible at all times. Jan's chair and lower body are visible, seated, not standing.",
  },
  {
    slug: "s4_12_incident_form",
    camera: "Medium shot on Christina alone, camera positioned side-on to the desk, same general area and same standing position relative to the desk as the earlier Christina-solo shots -- NOT near the door, the door is not the focus of this shot. Jan visible small and soft-focused behind the desk, seated, same relative position as always.",
    action: "Christina delivers her line standing at the desk, holding a closed slim manila document folder flat against her chest with both arms -- NOT a tablet, NOT a laptop, just a plain closed folder -- completely unbothered, already mentally checked out of the conversation but still physically present in the room -- she does NOT walk toward the door or leave in this shot. That happens later, at the very end of the scene, not here.",
  },
  {
    slug: "s4_13_give_it_here",
    camera: "Over-the-shoulder shot FAVORING JAN, same setup as shot 2 (behind Christina's shoulder looking at Jan).",
    action: "Jan sighs and extends one open hand across the desk, resigned. Christina has just opened the closed manila folder she was carrying and pulled out THE DOCUMENT -- a stapled bundle of roughly fourteen off-white A4 pages, about 5-6mm thick, with a single silver staple through the top-left corner and slightly curled page corners -- and is holding it out, already handing it across the desk to Jan. A beat later Jan's eyes widen in fresh alarm as he registers its thickness. The empty manila folder is now tucked under Christina's other arm.",
  },
  {
    slug: "s4_14_relationship_authority",
    camera: "Medium shot on Christina alone, camera positioned side-on to the desk, same framing as shot 6.",
    action: "Christina explains the form's contents with clinical, bureaucratic calm, gesturing very slightly toward the document. Jan is small and soft-focused behind her, staring down at the stapled pages in dawning horror.",
  },
  {
    slug: "s4_15_coversheet_memo",
    camera: "Wide two-shot, camera pulled back to the desk-front master framing (matching Picture 1), Christina now walking away toward the open glazed door on the left while Jan remains seated at the desk on the right.",
    action: "Jan mutters down at the document, defeated, one hand rubbing his forehead near the plaster. Christina, mid-stride toward the door, delivers her closing line back over her shoulder without breaking stride, entirely unbothered.",
  },
];

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
  const [anchorUrl, janUrl, christinaUrl] = await Promise.all([
    resolveImage(ANCHOR),
    resolveImage(JAN_REF),
    resolveImage(CHRISTINA_REF),
  ]);
  const only = process.argv[2] ? process.argv.slice(2) : null;

  for (const shot of shots) {
    if (only && !only.includes(shot.slug)) continue;
    const dest = `scene4-stills/${shot.slug}.png`;
    if (fs.existsSync(dest)) { console.log(`[skip] ${shot.slug} already exists`); continue; }

    const prompt = [PRESERVE, shot.camera, shot.action].join(' ');
    console.log(`\n=== ${shot.slug} ===`);
    try {
      const result = await fal.subscribe("fal-ai/nano-banana-pro/edit", {
        input: { prompt, image_urls: [anchorUrl, janUrl, christinaUrl], num_images: 1, aspect_ratio: "16:9", resolution: "2K" },
        logs: true,
        onQueueUpdate: (u) => { if (u.status === "IN_PROGRESS") (u.logs || []).forEach((l) => console.log("  ", l.message)); },
      });
      await download(result.data.images[0].url, dest);
      console.log(`[ok] ${shot.slug} -> ${dest} (requestId ${result.requestId})`);
    } catch (e) {
      console.error(`[FAIL] ${shot.slug}: ${e.message}`);
    }
  }
}

main().catch((err) => { console.error(err); process.exit(1); });
