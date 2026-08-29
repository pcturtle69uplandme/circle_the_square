#!/usr/bin/env node
// Generates an 8-angle coverage set per location via Nano Banana 2, chaining off one
// master wide shot (image-edit, not independent text-to-image) so furniture/materials/
// colors stay locked across angles -- same principle as generate-cast-refs.js.
// Usage: node generate-location-coverage.js <locationSlug> [limit]

const { execFileSync } = require("child_process");
const fs = require("fs");
const path = require("path");

const OUT_ROOT = path.join(__dirname, "..", "location-refs", "higgsfield", "coverage");
const MANIFEST_PATH = path.join(__dirname, "location-coverage-manifest.json");

function hf(args) {
  const fullArgs = process.platform === "win32"
    ? ["/c", "higgsfield.cmd", ...args, "--json"]
    : [...args, "--json"];
  const bin = process.platform === "win32" ? "cmd.exe" : "higgsfield";
  const out = execFileSync(bin, fullArgs, { encoding: "utf8", maxBuffer: 1024 * 1024 * 20 });
  return JSON.parse(out);
}

const LOCATIONS = {
  goldfish_meeting_room: {
    name: "Goldfish Bowl Meeting Room (Glass Meeting Room, Location 05) - generic, reusable elsewhere, NOT Jan's office",
    base: "Photoreal small glazed meeting room, a stand-in set inside a modern UK open-plan office floor, in the style of The Triangle, Cambridge. Full-height glass partition walls on all sides, sliding glass door with a black metal frame. The door handle has a clearly visible thumb-turn privacy lock built into it - a small round or oblong turn-latch at the center of the vertical pull handle, distinct enough to read on camera, since a character locks this door as a scripted action. This is NOT a private walled office, it is a fully glass-enclosed room open to view from the surrounding open-plan floor. Frosted dot privacy film pattern across the glass at roughly eye-to-shoulder height, plus a triangle-motif decal accent on one glass panel (a printed/etched graphic on the glass itself, not a physical acoustic panel wall). Small white rectangular table seating 4, mesh-back black task chairs around it. A wall-mounted TV screen visible through the glass wall facing the corridor side. Fitted venetian blinds are mounted on the inside of the glass walls, currently raised/open, folded up neatly at the top of each glass panel - these blinds are a required practical prop, not decorative, since the room is used for a scripted beat where a character lowers them for privacy. Beyond the glass walls, a glimpse of an open-plan office floor - hot-desk workstations, a suspended triangle/hexagon acoustic sculpture hanging from the ceiling in the distance. No exterior windows in this room itself; light comes from the open-plan floor's own windows visible in the background. Cinematic 35mm architectural photography, natural even daylight, well-lit, no people in frame.",
  },
  jan_office: {
    name: "Jan's Office (private walnut-desk room)",
    base: "Photoreal modern executive office interior, UK corporate building inspired by The Triangle, Cambridge - dark red-brown brick with black banding on visible structural elements, warm walnut wood, red/black/white triangular geometric acoustic feature wall. Walnut desk with an angled orange-painted accent panel on the front face, black mesh office chair. Built-in walnut shelving unit with books, a small award, and a desk lamp. Large potted fig tree in a concrete planter. Dark wood herringbone flooring. Grey sofa with an orange throw cushion. One single glazed door with a black metal frame as the ONLY entrance - this door leads to an INTERIOR corridor / open-plan office floor, NOT outside; through the door's glass, a glimpse of the interior corridor and open-plan desks is visible, never sky, street, or a housing estate. The door handle has a visible thumb-turn privacy lock, since a character locks this door as a scripted action. Fitted venetian blinds are mounted inside the glass door and any glazed side panels, raised/open and folded up at the top unless a shot specifically calls for them lowered - a required practical prop, since a character lowers them for privacy as a scripted beat. Separately, one modest window (not a door) showing a brand new private housing estate outside - modern new-build houses, contemporary render and brick facades, low-rise, no skyscrapers or tall towers. Cinematic 35mm architectural photography, natural even daylight, well-lit, no people in frame.",
  },
  jan_office_corridor: {
    name: "Corridor outside Jan's Office",
    base: "Photoreal interior corridor / open-plan office floor in a modern UK corporate building, in the style of The Triangle, Cambridge - dark red-brown brick with black banding, warm walnut wood accents. In the foreground or midground, a single glazed door with a black metal frame and a visible thumb-turn lock on the handle - this is the exterior side of Jan's office door, matching the same door seen from inside his office. Through the door's glass, a hint of the office interior (walnut desk, red/black/white triangular feature wall) is visible. Fitted venetian blinds visible inside the door's glass, raised/open. Surrounding corridor/open-plan floor: hot-desk workstations, carpet tile flooring, overhead lighting, other glazed doors/partitions further down the corridor. Cinematic 35mm architectural photography, natural even daylight, well-lit, no people in frame.",
  },
};

// Shot 0 is the master: pure text-to-image, generated once. Every other angle is an
// image-edit off that master (--image), keeping furniture/materials/colors locked.
const MASTER_SLUG = "master_wide";
// Fixed room geography, repeated verbatim in every prompt so table/door position and
// glass-wall count stay pinned across angles instead of drifting shot to shot.
const ROOM_LAYOUT = "Fixed room layout: the sliding glass door is on the LEFT wall, opening onto " +
  "the open-plan floor corridor - this is the ONLY door. All four walls are full-height glass " +
  "partitions. The frosted dot privacy film sits at eye-to-shoulder height on the RIGHT-hand " +
  "glass wall, with the triangle-motif decal accent on that same panel. The small white 4-seat " +
  "table runs down the CENTER of the room, long axis pointing from the door toward the back wall, " +
  "mesh-back chairs on both long sides. The wall-mounted TV is fixed to the glass wall facing the " +
  "corridor, visible from outside the room. Fitted venetian blinds are mounted inside each glass " +
  "panel, raised/open and folded up at the top unless a shot specifically calls for them lowered. " +
  "Beyond the glass, the open-plan floor with hot-desk workstations and the suspended " +
  "triangle/hexagon ceiling sculpture is consistently visible in the background on the same side " +
  "each time.";
const keepRoom = `Keep this exact room, same table, same glass walls, same decal position, same TV position as the reference image. ${ROOM_LAYOUT} —`;

function buildShots(loc) {
  return [
    { slug: MASTER_SLUG, anchor: true, prompt: `${loc.base} ${ROOM_LAYOUT} Wide establishing shot from just inside the sliding door, showing the whole room, table and glass walls in frame, open-plan floor visible beyond.` },
    { slug: "table_head", prompt: `${keepRoom} camera at the head of the table looking down its length toward the far end, as if seated at the head chair.` },
    { slug: "table_reverse", prompt: `${keepRoom} reverse angle from the far end of the table looking back toward the sliding door.` },
    { slug: "table_side", prompt: `${keepRoom} side angle along the length of the table, glass walls visible on both sides of the frame.` },
    { slug: "decal_closeup", prompt: `${keepRoom} closer angle on the frosted dot privacy film and the triangle-motif decal on the glass, tighter framing than the wide shot.` },
    { slug: "corridor_view", prompt: `${keepRoom} camera positioned OUTSIDE the room, in the open-plan floor corridor, looking IN through the glass wall - the wall-mounted TV and the frosted dot pattern are visible from this angle, people at hot-desks visible in the foreground of this shot.` },
    { slug: "door_closed", prompt: `${keepRoom} the sliding glass door is shown closed, venetian blinds fitted inside the glass and lowered for privacy, emphasizing this as a deliberate, visible act from outside.` },
    { slug: "openplan_context_wide", prompt: `${keepRoom} wide shot taken from further out on the open-plan floor, showing the glass meeting room nested within the larger office floor, hot-desk workstations and the suspended triangle/hexagon sculpture prominent in the foreground.` },
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
  const slugs = onlySlug ? [onlySlug] : Object.keys(LOCATIONS);

  for (const slug of slugs) {
    const loc = LOCATIONS[slug];
    if (!loc) {
      console.error(`Unknown location slug: ${slug}`);
      continue;
    }
    const outDir = path.join(OUT_ROOT, slug);
    fs.mkdirSync(outDir, { recursive: true });
    manifest[slug] = manifest[slug] || {};

    const allShots = buildShots(loc);
    const shots = limit ? allShots.slice(0, limit) : allShots;
    console.log(`\n=== ${loc.name} (${shots.length}/${allShots.length} angles) ===`);
    let masterPath = null;

    for (const shot of shots) {
      const destPath = path.join(outDir, `${slug}_${shot.slug}.png`);
      if (fs.existsSync(destPath)) {
        console.log(`  [skip] ${shot.slug} (already exists)`);
        if (shot.anchor) masterPath = destPath;
        continue;
      }
      if (!shot.anchor && !masterPath) {
        console.error(`  [ABORT] ${shot.slug}: no master image generated yet for ${loc.name} — stopping.`);
        break;
      }
      try {
        const args = ["generate", "create", "nano_banana_flash", "--prompt", shot.prompt, "--aspect_ratio", "21:9"];
        if (!shot.anchor) args.push("--image", masterPath);
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
        if (shot.anchor) masterPath = destPath;
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
