// Debbie Vance (HR manager, Scene 4) -- 12-shot reference set, same recipe as
// generate-cast-refs.js used for Jan/Christina/Sharon/Chris/Rick/Maureen/Gemma, but
// driven through the free-tier Higgsfield web UI via Playwright (hf_up.js/run_shot.js)
// instead of the higgsfield.cmd CLI -- the CLI is locked to the paid cheungtai37
// account and the MCP server only has 2.07 credits, neither of which covers a 12-shot
// sheet. Run with:
//
//   HF_SHOTS=./debbie_refs.js HF_OUT=<repo>/character-refs/higgsfield/debbie node run_batch.js
//
// Shot 0 (debbie_front) is the anchor: pure text-to-image, no refs. Every other shot
// attaches that anchor as a reference and asks for an angle/expression/lighting change
// while keeping the same person, exactly mirroring buildShots() in
// ../generate-cast-refs.js so Debbie's folder has the same 12 filenames as every other
// character (front, three_quarter_left/right, profile, slight_up/down,
// expression_neutral/incharacter, fullbody_neutral/characteristic, lighting_soft/harsh).

const BASE = "Photorealistic reference image of a 45-year-old British woman, Debbie Vance, an HR manager. Average sturdy build, 5'6\". Straight shoulder-length mousy brown hair with a blunt fringe, practical and unstyled. Plain forest-green cardigan over a cream blouse, sensible navy trousers, flat shoes, an HR lanyard with a laminated badge, reading glasses pushed up on top of her head.";

const EXPRESSION_INCHARACTER = "Completely unbothered, professionally blank deadpan expression -- the look of someone who stopped being surprised by anything in this building years ago.";

const FULLBODY_CHARACTERISTIC = "Standing holding a clipboard against her chest with both hands, weight on one hip, patiently waiting.";

const HEADSHOT_SUFFIX = "shoulders-up framing, plain neutral studio background, office environment lighting.";
const FULLBODY_SUFFIX = "full-body head-to-shoe reference shot, standing, plain neutral studio background, even lighting.";
const KEEP_IDENTITY = "Keep the exact same person, face, build, and outfit as the reference image --";

const ANCHOR = 'character-refs/higgsfield/debbie/debbie_front.png';

module.exports = {
  debbie_front: {
    beat: 'ANCHOR -- text-to-image, front-facing neutral',
    refs: [],
    prompt: `${BASE} Front-facing, direct eye contact with camera, neutral relaxed expression. ${HEADSHOT_SUFFIX}`,
  },
  debbie_three_quarter_left: {
    beat: 'Three-quarter angle from the left',
    refs: [ANCHOR],
    prompt: `${KEEP_IDENTITY} turn the head and shoulders to a three-quarter angle from the left. ${HEADSHOT_SUFFIX}`,
  },
  debbie_three_quarter_right: {
    beat: 'Three-quarter angle from the right',
    refs: [ANCHOR],
    prompt: `${KEEP_IDENTITY} turn the head and shoulders to a three-quarter angle from the right. ${HEADSHOT_SUFFIX}`,
  },
  debbie_profile: {
    beat: 'Full side profile',
    refs: [ANCHOR],
    prompt: `${KEEP_IDENTITY} turn to a full side profile view. ${HEADSHOT_SUFFIX}`,
  },
  debbie_slight_up: {
    beat: 'Camera angled slightly up',
    refs: [ANCHOR],
    prompt: `${KEEP_IDENTITY} angle the camera slightly upward toward the face, looking past camera. ${HEADSHOT_SUFFIX}`,
  },
  debbie_slight_down: {
    beat: 'Camera angled slightly down',
    refs: [ANCHOR],
    prompt: `${KEEP_IDENTITY} angle the camera slightly downward toward the face, looking past camera. ${HEADSHOT_SUFFIX}`,
  },
  debbie_expression_neutral: {
    beat: 'Calm neutral expression, front-facing',
    refs: [ANCHOR],
    prompt: `${KEEP_IDENTITY} calm neutral expression, front-facing. ${HEADSHOT_SUFFIX}`,
  },
  debbie_expression_incharacter: {
    beat: 'In-character deadpan expression',
    refs: [ANCHOR],
    prompt: `${KEEP_IDENTITY} change the expression to: ${EXPRESSION_INCHARACTER} ${HEADSHOT_SUFFIX}`,
  },
  debbie_fullbody_neutral: {
    beat: 'Full body, neutral standing pose',
    refs: [ANCHOR],
    prompt: `${KEEP_IDENTITY} show the full body head-to-shoe, standing, arms relaxed at sides, front-facing. ${FULLBODY_SUFFIX}`,
  },
  debbie_fullbody_characteristic: {
    beat: 'Full body, characteristic clipboard pose',
    refs: [ANCHOR],
    prompt: `${KEEP_IDENTITY} show the full body head-to-shoe in this pose: ${FULLBODY_CHARACTERISTIC} ${FULLBODY_SUFFIX}`,
  },
  debbie_lighting_soft: {
    beat: 'Relit -- soft diffused studio lighting',
    refs: [ANCHOR],
    prompt: `${KEEP_IDENTITY} front-facing, neutral expression, relit with soft diffused studio lighting, minimal shadow. ${HEADSHOT_SUFFIX}`,
  },
  debbie_lighting_harsh: {
    beat: 'Relit -- harsh directional office window lighting',
    refs: [ANCHOR],
    prompt: `${KEEP_IDENTITY} front-facing, neutral expression, relit with harsh directional office window lighting, visible shadow. ${HEADSHOT_SUFFIX}`,
  },
};
