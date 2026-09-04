// Scene 2 still definitions -- INT. CORRIDOR / OPEN-PLAN FLOOR - CONTINUOUS
// (CTS_Featurette_Episode.fountain L88-151). One entry per planned video clip, per
// SCENE2_VIDEO_PLAN.md's clip breakdown: 07c and 09 each split into a calmer opening
// half and a climactic second half, because verbatim they overflow the 15s ceiling.
//
// Every crowd shot names extra_01..04 explicitly and attaches their reference photos.
// Without that, Nano Banana 2 invents a fresh set of background workers per image and
// the crowd reads as different colleagues in every cut (see SCENE2_VIDEO_PLAN.md's
// crowd-consistency section).
//
// Wardrobe is pinned from the script's own parentheticals -- CHRIS "light blue shirt",
// RICK "grey polo". The cast reference photos do NOT lock shirt colour, so it has to
// be restated in every prompt or it drifts: the first-pass shot06 put Rick in a navy
// button-down, which is part of why this file exists.

const LOC = 'location-refs/higgsfield/coverage/jan_office_corridor/jan_office_corridor_master_wide.png';
const JAN = 'character-refs/higgsfield/jan/jan_front.png';
const CHRIS = 'character-refs/higgsfield/chris/chris_front.png';
const RICK = 'character-refs/higgsfield/rick/rick_front.png';
const SHARON = 'character-refs/higgsfield/sharon/sharon_front.png';
const E1 = 'character-refs/higgsfield/extra_01/extra_01_fullbody_neutral.png';
const E2 = 'character-refs/higgsfield/extra_02/extra_02_fullbody_neutral.png';
const E3 = 'character-refs/higgsfield/extra_03/extra_03_fullbody_neutral.png';
const E4 = 'character-refs/higgsfield/extra_04/extra_04_fullbody_neutral.png';

// Repeated verbatim in every prompt so the set cannot drift between shots.
const LOCATION = "LOCATION - reproduce the corridor reference image exactly: the same corridor and open-plan office floor, exposed dark red-brick and warm walnut panelling with black banding, grey carpet-tile flooring, hot-desk workstations on the right, a daylight window at the far end of the corridor, recessed ceiling lights and a suspended linear pendant. Jan's black-framed glazed office door and the large glazed panel beside it are on the LEFT of frame.";

// Signage on the office door (e.g. a "JAN'S OFFICE" vinyl on the glass) is fine --
// user call, 2026-09-04. This rule is only about captions/watermarks/overlays.
const STYLE = 'Natural office daylight, photorealistic, shallow depth of field, no captions, no subtitles, no on-screen graphics, no watermark.';

// Character descriptions, restated every time -- the reference photos are neutral
// studio shots and carry no emotional or physical state of their own.
const C = {
  jan: 'JAN - 52, visibly overweight, 5 foot 10, prominent round belly straining his shirt buttons, soft double chin, thinning mid-brown hair greying at the temples slicked into a side parting over a receding hairline, too-tight dark navy suit jacket open over a white dress shirt, tie loosened and hanging askew, gold wristwatch, wedding ring.',
  chris: 'CHRIS - 32, lean, 5 foot 11, short textured dark hair, wearing a LIGHT BLUE shirt with sleeves rolled up, tan chino trousers, company lanyard.',
  rick: 'RICK - 40, broad and sturdy, 6 foot, short greying near-buzzcut hair with light stubble, wearing a plain GREY POLO SHIRT with sleeves rolled, dark sturdy trousers, company lanyard.',
  sharon: 'SHARON - 34, curvy, 5 foot 5, shoulder-length wavy auburn hair, fitted jewel-tone blouse, pencil skirt, heels, company lanyard.',
};

// The recurring background extras, described to match the reference photos attached
// alongside them so the same faces recur from cut to cut.
const CROWD = 'THE CROWD - a gathered crowd of about ten to twelve British office workers in smart-casual clothes with company lanyards, standing in a loose semicircle. Four of them are the specific people in the four full-body studio reference photos and MUST match those photos exactly: a 45-year-old Black British woman with short natural curly black hair in a mustard-yellow knit top and grey trousers; a 55-year-old British South Asian man with greying hair and a short grey beard in a charcoal crew-neck jumper over a pale blue collar and navy chinos; a woman in her thirties with long light brown wavy hair in a white floral-print blouse and navy trousers; a man in his thirties with dark hair and glasses in a blue checked shirt. Place these four clearly visible in the crowd. The remaining background workers are unnamed and stay out of focus.';

module.exports = {
  shot06_corridor_gossip: {
    beat: 'Chris and Rick gossip; blinds shut, Sharon and Jan still inside',
    refs: [LOC, CHRIS, RICK],
    prompt: [
      'Photoreal cinematic film still, 35mm lens, natural daylight, medium-wide two-shot. FRAMING - stand well back: the frame must take in the WHOLE of the glazed office door and its surrounding frame on the left, both men from the knees up on the right, and the corridor receding behind them toward the daylight window. Do not crop in tight on the two men.',
      LOCATION,
      // Saying "lowered" or even "tilted shut" is not enough -- the model keeps
      // rendering slats you can see straight through (the red triangle feature wall
      // and the desk chair show up in the glass). Describing the RESULT rather than
      // the mechanism -- a solid opaque panel, interior completely hidden -- is what
      // makes it stick. See SCENE2_CONTINUITY_NOTES.md, Shot 06.
      'FIXTURE STATE, CRITICAL - the office door is shut and EVERY pane of glass in that office frontage has its venetian blind FULLY LOWERED with the slats CLOSED FLAT: the wide glazed door, the tall narrow side panel beside it, and the glazed panel on the corner return. ALL of them, with no exceptions. Every one of those panes must read as a SOLID OPAQUE PALE PANEL, like a blank white wall. You CANNOT see through any of them at all: no furniture, no desk, no chair, no bookshelf, no red or orange or black shapes, no triangle wall pattern, no colour and no silhouettes of any kind showing through any pane. The interior of the office is completely hidden from view. The closed slats must still read clearly as a VENETIAN BLIND - fine horizontal slat lines visible across every pane - not as frosted or sandblasted glass.',
      'WHO IS IN FRAME - exactly two men and nobody else, no other people anywhere in the frame.',
      C.chris,
      'He is turned slightly toward the closed glazed door, mid-sentence, exasperated and amused, speaking out of the side of his mouth.',
      C.rick,
      'He stands beside Chris with his arms folded, flat unbothered deadpan expression, not looking at Chris.',
      'Both stand in the corridor beside the desk run, angled toward the shut office door.',
      STYLE,
    ].join(' '),
  },

  shot07_sharon_exits: {
    beat: 'Sharon leaves Jan’s room dishevelled; Jan still inside, Chris and Rick watching',
    refs: [LOC, SHARON, CHRIS, RICK, JAN],
    prompt: [
      'Photoreal cinematic film still, 35mm lens, natural daylight, wide shot.',
      LOCATION,
      'FIXTURE STATE - the office door is now OPEN and the venetian blinds are RAISED, so the inside of the office is visible through the doorway and the glazed panel.',
      C.sharon,
      'She is the foreground focus, mid-stride walking out of the office door toward camera, visibly dishevelled: hair mussed with strands out of place, makeup smudged, a light sheen of sweat on her face and neck, blouse slightly untucked and creased, expression dazed but trying to compose herself, eyes down.',
      'INSIDE THE OFFICE, clearly visible through the open door - ' + C.jan + ' He is still inside, seated at his walnut desk with his back three-quarters to camera, composure not yet regained, not looking out. The room must read as occupied, not empty.',
      'IN THE BACKGROUND - ' + C.chris + ' and ' + C.rick + ' They stand together further down the corridor by the desk run, both watching Sharon leave, Chris smirking, Rick with arms folded and deadpan.',
      'No other people in frame.',
      STYLE,
    ].join(' '),
  },

  shot07b1_jan_addresses: {
    beat: 'Jan emerges, claps to gather everyone; Chris asks whether Sharon gets a pass',
    refs: [LOC, JAN, CHRIS, E3, E4],
    prompt: [
      'Photoreal cinematic film still, 35mm lens, natural daylight, medium-wide shot.',
      LOCATION,
      'FIXTURE STATE - the office door stands open behind Jan, venetian blinds raised.',
      C.jan,
      'He has just emerged from his office and stands at the focal point where the corridor meets the open-plan desks, hands still together mid-clap having just clapped to gather everyone, chin raised, self-important and mid-sentence addressing the assembled staff. His white shirt is re-buttoned ASKEW - one button out of line, the hem uneven - and his tie is loosened and crooked. He is composed and pleased with himself here, not yet angry.',
      C.chris,
      'He stands within the crowd on the right side of frame, one hand half-raised, asking a pointed question with a knowing smirk.',
      CROWD,
      'They are calm and attentive at this moment, a few glancing sideways at each other.',
      STYLE,
    ].join(' '),
  },

  shot07b2_shut_up_flareup: {
    beat: 'Sniggering ripples through the crowd; Jan flares up with SHUT UP',
    refs: [LOC, JAN, E1, E2, E3, E4],
    prompt: [
      'Photoreal cinematic film still, 35mm lens, natural daylight, medium shot, pushed in slightly on Jan.',
      LOCATION,
      C.jan,
      'He is at the focal point mid-outburst, both hands raised and open in exasperation, mouth wide open shouting, face flushed deep red, brow furrowed - defensive and humiliated, having just been caught out over Sharon and overreacting badly. Shirt re-buttoned askew, tie crooked.',
      CROWD,
      'They are sniggering at him with poorly suppressed laughter - hands over mouths, shoulders shaking, tight smirks, some looking down to hide their faces, glancing at each other. Not open laughter: they are trying and failing not to laugh at him.',
      STYLE,
    ].join(' '),
  },

  shot07c1_rick_questions: {
    beat: 'Rick asks what happened to the last project; Jan begins justifying',
    refs: [LOC, JAN, RICK, E3, E4],
    prompt: [
      'Photoreal cinematic film still, 35mm lens, natural daylight, medium two-shot favouring Rick.',
      LOCATION,
      C.rick,
      'He stands within the crowd, arms folded, one eyebrow slightly raised, mid-question - flat, blunt and openly skeptical, entirely unimpressed.',
      C.jan,
      'He faces Rick from the focal point, mouth open beginning a long defensive explanation, one hand raised palm-up in a placating self-justifying gesture, chin lifted, patronising rather than angry. Shirt re-buttoned askew, tie crooked, face still slightly flushed.',
      CROWD,
      'They watch the exchange, a few exchanging knowing looks.',
      STYLE,
    ].join(' '),
  },

  shot07c2_naming_inception: {
    beat: 'Jan announces he will call the project Inception',
    refs: [LOC, JAN, RICK, E3, E4],
    prompt: [
      'Photoreal cinematic film still, 35mm lens, natural daylight, medium-wide shot.',
      LOCATION,
      C.jan,
      'He is mid-triumphant-announcement at the focal point, one arm raised high and presenting, palm open, chest puffed out, beaming with self-satisfaction as he names the project. Shirt re-buttoned askew, tie crooked.',
      C.rick,
      'He stands beside and slightly behind Jan, arms folded, visibly unimpressed and deadpan, staring flatly at him.',
      CROWD,
      'They flank both sides of frame watching, expressions flat and unenthused.',
      STYLE,
    ].join(' '),
  },

  shot08_project_inception_heckle: {
    beat: 'Chris heckles across the crowd: you are dreaming Jan',
    refs: [LOC, JAN, CHRIS, E1, E2, E3, E4],
    prompt: [
      'Photoreal cinematic film still, 35mm lens, natural daylight, wide shot taking in Jan and the whole crowd.',
      LOCATION,
      C.jan,
      'He stands at the focal point addressing the staff, caught mid-flow and turning toward the heckle with a startled indignant expression, mouth open. Shirt re-buttoned askew, tie crooked.',
      C.chris,
      'IMPORTANT - Chris is NOT standing next to Jan. He is positioned across the room within the crowd, on the far side of frame from Jan, shouting the heckle over the heads of the others with his hands cupped near his mouth, grinning broadly.',
      CROWD,
      'They are laughing openly at the heckle, heads turning between Chris and Jan.',
      STYLE,
    ].join(' '),
  },

  shot08b_merch_gag: {
    beat: 'Branded merch sight gag, then the lead position is revealed as filled by Jan',
    refs: [LOC, JAN, CHRIS, E3, E4],
    prompt: [
      'Photoreal cinematic film still, 35mm lens, natural daylight, medium two-shot.',
      LOCATION,
      C.jan,
      'He stands beside a large open cardboard box resting on a desk, one hand gesturing sheepishly at its contents with a caught-out shrug and an embarrassed half-smile, having clearly ordered the merchandise before anyone questioned the name.',
      'THE PROP, and this is the whole joke so the text must be clearly legible - the open cardboard box is packed with cheap branded office merchandise all printed with the words "PROJECT INCEPTION" in bold capitals: foam stress balls, branded pens, and folded t-shirts. The words "PROJECT INCEPTION" are also printed in large bold capitals on the side of the cardboard box itself.',
      C.chris,
      'He stands facing Jan across the desk, head tilted, asking a straightforward question with a curious raised-eyebrow expression, not yet reacting.',
      CROWD,
      'They stand watching in the background, slightly out of focus.',
      'Natural office daylight, photorealistic, shallow depth of field, no captions, no on-screen graphics, no watermark - the only text anywhere in frame is "PROJECT INCEPTION" printed on the box and on the merchandise.',
    ].join(' '),
  },

  shot09_1_groans: {
    beat: 'Groans from the crowd; Jan calmly justifies the 50k',
    refs: [LOC, JAN, E1, E2, E3, E4],
    prompt: [
      'Photoreal cinematic film still, 35mm lens, natural daylight, medium-wide shot over the crowd toward Jan.',
      LOCATION,
      CROWD,
      'They are groaning and visibly exasperated - heads tipped back, eyes rolling, hands rubbing faces, arms folded, one or two wincing, shoulders slumped. Weary rather than angry.',
      C.jan,
      'He stands at the focal point facing them, calm and smug rather than shouting, one hand raised palm-down to quiet them, a self-satisfied little smile, entirely untroubled by the groaning. Shirt re-buttoned askew, tie crooked.',
      STYLE,
    ].join(' '),
  },

  shot09_2_50k_outburst: {
    beat: 'Jan bellows GET BACK TO WORK',
    refs: [LOC, JAN, E1, E2, E3, E4],
    prompt: [
      'Photoreal cinematic film still, 35mm lens, natural daylight, medium shot pushed in tighter on Jan than the earlier outburst.',
      LOCATION,
      C.jan,
      'He is mid-shout at the focal point, one fist raised, face flushed deep red, mouth wide open bellowing an order, furious and domineering. Shirt re-buttoned askew, tie crooked, sweat at his hairline.',
      CROWD,
      'They recoil and react with weary exasperation - heads in hands, arms folded, wincing, a few already turning away to go back to their desks.',
      STYLE,
    ].join(' '),
  },
};
