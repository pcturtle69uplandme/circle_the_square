#!/usr/bin/env node
// Generates a 12-shot photoreal reference set per main cast character via Nano
// Banana 2, saving into character-refs/higgsfield/<character>/.
// Usage: node generate-cast-refs.js [characterSlug]   (omit to run all characters)

const { execFileSync } = require("child_process");
const fs = require("fs");
const path = require("path");

const OUT_ROOT = path.join(__dirname, "..", "character-refs", "higgsfield");
const MANIFEST_PATH = path.join(__dirname, "cast-refs-manifest.json");

function hf(args) {
  const fullArgs = process.platform === "win32"
    ? ["/c", "higgsfield.cmd", ...args, "--json"]
    : [...args, "--json"];
  const bin = process.platform === "win32" ? "cmd.exe" : "higgsfield";
  const out = execFileSync(bin, fullArgs, { encoding: "utf8", maxBuffer: 1024 * 1024 * 20 });
  return JSON.parse(out);
}

const CHARACTERS = {
  jan: {
    name: "Jan Peach",
    base: "Photorealistic reference image of a 52-year-old British man, Jan Peach. Visibly overweight build, 5'10\", a prominent round belly straining and pulling at his shirt buttons, soft double chin, rounded slumped shoulders. Thinning mid-brown hair greying at the temples, combed sideways in a clear side parting over a receding hairline, visibly product-slicked and flat. Slightly-too-tight dark navy two-button suit jacket open over a white dress shirt stretched across his stomach, top button undone, tie visibly loosened and hanging askew (not tightly knotted), oversized flashy gold wristwatch, wedding ring.",
    expressionInCharacter: "Arrogant, pompous expression, chin raised, mid-sentence as if lecturing someone.",
    fullBodyCharacteristic: "Standing with hands on hips in a self-important power pose, chest puffed out.",
  },
  christina: {
    name: "Christina Dross",
    base: "Photorealistic reference image of a 38-year-old British woman, Christina Dross. Slim, upright build with squared shoulders, 5'6\". Sleek dark brown bob with a blunt fringe or crisp side part, always neatly set. Tailored charcoal or navy blazer over a cream blouse, tailored trousers or pencil skirt, low block heels, minimal gold jewellery, company lanyard.",
    expressionInCharacter: "Cold, controlled, faint deadpan smile, appraising look.",
    fullBodyCharacteristic: "Standing holding a tablet against her chest, poised and composed.",
  },
  sharon: {
    name: "Sharon Enfield",
    base: "Photorealistic reference image of a 34-year-old British woman, Sharon Enfield. Curvy build, 5'5\". Shoulder-length wavy auburn hair worn loose. Fitted jewel-tone blouse, pencil skirt, heels, hair and makeup neatly done, company lanyard.",
    expressionInCharacter: "Warm, knowing half-smile, relaxed confidence.",
    fullBodyCharacteristic: "Standing with one hand on hip, phone in the other hand, casual confident stance.",
  },
  chris: {
    name: "Chris",
    base: "Photorealistic reference image of a 32-year-old British man, Chris. Lean build, 5'11\". Short, textured dark hair. Casual-smart office wear, shirt untucked or sleeves rolled, no tie, company lanyard, casual shoes.",
    expressionInCharacter: "Sarcastic smirk, one eyebrow raised, amused.",
    fullBodyCharacteristic: "Standing leaning slightly to one side, coffee cup in hand, relaxed slouched posture.",
  },
  rick: {
    name: "Rick",
    base: "Photorealistic reference image of a 40-year-old British man, Rick. Sturdy, broad build, 6'0\". Short greying hair, near-buzzcut. Plain button-down or polo shirt, sleeves rolled, sturdy trousers, practical shoes, company lanyard.",
    expressionInCharacter: "Flat, unbothered, unblinking stare, arms crossed.",
    fullBodyCharacteristic: "Standing at ease with arms crossed, sturdy stance, watching something off camera.",
  },
  maureen: {
    name: "Maureen",
    base: "Photorealistic reference image of a 58-year-old British woman, Maureen, a canteen worker. Average build. Short greying curly hair pinned back, reading glasses on a chain. Beige apron over a white polo shirt.",
    expressionInCharacter: "Warm, no-nonsense, faint smile, practical demeanor.",
    fullBodyCharacteristic: "Standing behind a counter gesture, wiping hands on apron, welcoming but brisk posture.",
  },
  gemma: {
    name: "Gemma Ashcroft",
    base: "Photorealistic reference image of a 26-year-old British woman, Gemma Ashcroft, a receptionist. Slim build, 5'7\". Sleek dark blonde hair in a high ponytail. White blouse, slate-grey blazer, pencil skirt, black low heels, orange lanyard, discreet telephone headset.",
    expressionInCharacter: "Polished, professional customer-service smile, warm and welcoming.",
    fullBodyCharacteristic: "Standing with one hand near her ear adjusting the telephone headset, professional welcoming posture.",
  },
  trevor: {
    name: "Trevor",
    // NOTE: unlike the other characters, Trevor has no documented age/build/hair in the
    // project bible (CARTOON_CAST_BIBLE.md explicitly flags he was never fully built out).
    // Wardrobe/demeanor below are sourced from GROUP_PHOTO_SHOT_SPEC.md; age/build/hair are
    // invented placeholders, not established canon -- confirm before treating as final.
    base: "Photorealistic reference image of a 35-year-old British man, Trevor, a data analyst. Average build, 5'10\". Short neat brown hair, clean-shaven. Charcoal overcoat over a slate-grey shirt, dark trousers, cross-body messenger bag, company lanyard.",
    expressionInCharacter: "Completely deadpan, blank stare directly into camera, no expression.",
    fullBodyCharacteristic: "Standing perfectly still, arms at sides, blank deadpan expression, messenger bag across his body.",
  },
};

const HEADSHOT_SUFFIX = "shoulders-up framing, plain neutral studio background, office environment lighting.";
const FULLBODY_SUFFIX = "full-body head-to-shoe reference shot, standing, plain neutral studio background, even lighting.";

// Shot 0 is the anchor: pure text-to-image, generated once. Every other shot
// is an image-edit off that anchor (--image), not an independent text-to-image
// call, so the face/build/wardrobe stay locked instead of re-rolling each time.
const ANCHOR_SLUG = "front";

function buildShots(c) {
  const keepIdentity = "Keep the exact same person, face, build, and outfit as the reference image —";
  return [
    { slug: ANCHOR_SLUG, anchor: true, prompt: `${c.base} Front-facing, direct eye contact with camera, neutral relaxed expression. ${HEADSHOT_SUFFIX}` },
    { slug: "three_quarter_left", prompt: `${keepIdentity} turn the head and shoulders to a three-quarter angle from the left. ${HEADSHOT_SUFFIX}` },
    { slug: "three_quarter_right", prompt: `${keepIdentity} turn the head and shoulders to a three-quarter angle from the right. ${HEADSHOT_SUFFIX}` },
    { slug: "profile", prompt: `${keepIdentity} turn to a full side profile view. ${HEADSHOT_SUFFIX}` },
    { slug: "slight_up", prompt: `${keepIdentity} angle the camera slightly upward toward the face, looking past camera. ${HEADSHOT_SUFFIX}` },
    { slug: "slight_down", prompt: `${keepIdentity} angle the camera slightly downward toward the face, looking past camera. ${HEADSHOT_SUFFIX}` },
    { slug: "expression_neutral", prompt: `${keepIdentity} calm neutral expression, front-facing. ${HEADSHOT_SUFFIX}` },
    { slug: "expression_incharacter", prompt: `${keepIdentity} change the expression to: ${c.expressionInCharacter} ${HEADSHOT_SUFFIX}` },
    { slug: "fullbody_neutral", prompt: `${keepIdentity} show the full body head-to-shoe, standing, arms relaxed at sides, front-facing. ${FULLBODY_SUFFIX}` },
    { slug: "fullbody_characteristic", prompt: `${keepIdentity} show the full body head-to-shoe in this pose: ${c.fullBodyCharacteristic} ${FULLBODY_SUFFIX}` },
    { slug: "lighting_soft", prompt: `${keepIdentity} front-facing, neutral expression, relit with soft diffused studio lighting, minimal shadow. ${HEADSHOT_SUFFIX}` },
    { slug: "lighting_harsh", prompt: `${keepIdentity} front-facing, neutral expression, relit with harsh directional office window lighting, visible shadow. ${HEADSHOT_SUFFIX}` },
  ];
}

async function downloadImage(url, destPath) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Download failed: ${res.status}`);
  const buf = Buffer.from(await res.arrayBuffer());
  fs.writeFileSync(destPath, buf);
}

function loadManifest() {
  if (!fs.existsSync(MANIFEST_PATH)) return {};
  return JSON.parse(fs.readFileSync(MANIFEST_PATH, "utf8"));
}

function saveManifest(m) {
  fs.writeFileSync(MANIFEST_PATH, JSON.stringify(m, null, 2));
}

async function run(onlySlug, limit) {
  const manifest = loadManifest();
  const slugs = onlySlug ? [onlySlug] : Object.keys(CHARACTERS);

  for (const slug of slugs) {
    const c = CHARACTERS[slug];
    if (!c) {
      console.error(`Unknown character slug: ${slug}`);
      continue;
    }
    const outDir = path.join(OUT_ROOT, slug);
    fs.mkdirSync(outDir, { recursive: true });
    manifest[slug] = manifest[slug] || {};

    const allShots = buildShots(c);
    const shots = limit ? allShots.slice(0, limit) : allShots;
    console.log(`\n=== ${c.name} (${shots.length}/${allShots.length} shots) ===`);
    let anchorPath = null;

    for (const shot of shots) {
      const destPath = path.join(outDir, `${slug}_${shot.slug}.png`);
      if (fs.existsSync(destPath)) {
        console.log(`  [skip] ${shot.slug} (already exists)`);
        if (shot.anchor) anchorPath = destPath;
        continue;
      }
      if (!shot.anchor && !anchorPath) {
        console.error(`  [ABORT] ${shot.slug}: no anchor image generated yet for ${c.name} — stopping this character.`);
        break;
      }
      try {
        const args = ["generate", "create", "nano_banana_flash", "--prompt", shot.prompt];
        if (!shot.anchor) args.push("--image", anchorPath);
        args.push("--wait");
        const result = hf(args);
        const job = Array.isArray(result) ? result[0] : result;
        if (job.status !== "completed" || !job.result_url) {
          console.error(`  [FAIL] ${shot.slug}: status=${job.status}`);
          manifest[slug][shot.slug] = { status: "failed", detail: job.status };
          continue;
        }
        await downloadImage(job.result_url, destPath);
        manifest[slug][shot.slug] = { status: "ok", file: destPath, job_id: job.id };
        if (shot.anchor) anchorPath = destPath;
        console.log(`  [ok]   ${shot.slug} -> ${path.basename(destPath)}`);
      } catch (e) {
        console.error(`  [ERROR] ${shot.slug}: ${e.message}`);
        manifest[slug][shot.slug] = { status: "error", detail: e.message };
      }
      saveManifest(manifest);
    }
  }

  console.log("\nDone. Manifest: " + MANIFEST_PATH);
}

const onlySlug = process.argv[2];
const limit = process.argv[3] ? Number(process.argv[3]) : null;
run(onlySlug, limit).catch((e) => {
  console.error("Fatal:", e);
  process.exit(1);
});
