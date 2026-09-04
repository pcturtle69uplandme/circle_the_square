// Scene 3 beat stills -- INT. STAFF RESTAURANT / CANTEEN - NEXT MORNING
// (CTS_Featurette_Episode.fountain L152-196, the final scene). Nine clips, planned in
// SCENE3_SHOT_LIST.md. Run with:
//
//   HF_SHOTS=./scene3_shots.js HF_OUT=<repo>/scene3-stills node run_batch.js
//
// Two decisions baked in here, both from SCENE3_SHOT_LIST.md:
//
// 1. JAN'S WARDROBE CHANGES. Scenes 1-2 are one continuous moment; this is NEXT
//    MORNING, the only scene that is not. So the askew white shirt and crooked navy
//    tie belong to yesterday. Same too-tight navy suit (he stays recognisable by
//    silhouette), fresh pale blue shirt and dark red tie -- worn just as badly.
//    Chris's light blue shirt and Rick's grey polo are script parentheticals and do
//    NOT change.
//
// 2. THE DESTRUCTION BEATS ANCHOR ON AFTERMATH, NOT MID-ACTION. Still models render
//    shattering china and breaking glass badly. Clips 4 and 6 are therefore the state
//    AFTER the break; the state before is already clip 3 and clip 5. That gives
//    MiniMax H3 a clean start frame and end frame to do the break between, which is
//    what its keyframe mode is for, and keeps the scene at nine shots.
//
// Continuity is cumulative and irreversible here -- trays empty, china smashes, glass
// breaks, Jan goes down. Nothing may un-happen in a later clip. See the state table in
// SCENE3_SHOT_LIST.md.

const MASTER = 'location-refs/higgsfield/coverage/staff_canteen/staff_canteen_master_wide.png';
const SERVERY = 'location-refs/higgsfield/coverage/staff_canteen/staff_canteen_servery_counter.png';
const WINDOW = 'location-refs/higgsfield/coverage/staff_canteen/staff_canteen_window_wall.png';

const JAN = 'character-refs/higgsfield/jan/jan_front.png';
const CHRIS = 'character-refs/higgsfield/chris/chris_front.png';
const RICK = 'character-refs/higgsfield/rick/rick_front.png';
const MAUREEN = 'character-refs/higgsfield/maureen/maureen_front.png';
const CHRISTINA = 'character-refs/higgsfield/christina/christina_front.png';
const E1 = 'character-refs/higgsfield/extra_01/extra_01_fullbody_neutral.png';
const E2 = 'character-refs/higgsfield/extra_02/extra_02_fullbody_neutral.png';
const E3 = 'character-refs/higgsfield/extra_03/extra_03_fullbody_neutral.png';
const E4 = 'character-refs/higgsfield/extra_04/extra_04_fullbody_neutral.png';

const LOCATION = 'LOCATION - reproduce the canteen in the location reference image exactly: the same staff restaurant with exposed dark red-brown brick piers with black banding, warm walnut panelling, a long timber-fronted servery counter with a stainless steel top and glass sneeze guard, pale timber cafe tables with black moulded chairs, high poseur tables with stools, burnt-orange moulded accent chairs, pale cream tiled floor, exposed dark grey concrete columns, and a full-height glazed window wall in slim black metal frames looking onto a landscaped courtyard.';

const NO_CITY = 'Outside the glazing is LOW-RISE: trees, grass, modern buildings of two or three storeys. No skyscrapers, no city skyline.';

const STYLE = 'Natural daylight, photorealistic, shallow depth of field, no captions, no subtitles, no on-screen graphics, no watermark.';

const C = {
  jan: 'JAN - 52, visibly overweight, 5 foot 10, prominent round belly straining his shirt buttons, soft double chin, thinning mid-brown hair greying at the temples slicked into a side parting over a receding hairline, gold wristwatch, wedding ring. NEXT MORNING WARDROBE - the same too-tight dark navy suit jacket, but now over a PALE BLUE dress shirt with a DARK RED tie, the collar open and the tie loosened and hanging askew.',
  chris: 'CHRIS - 32, lean, 5 foot 11, short textured dark hair, wearing a LIGHT BLUE shirt with sleeves rolled up, tan chino trousers, company lanyard.',
  rick: 'RICK - 40, broad and sturdy, 6 foot, short greying near-buzzcut hair with light stubble, wearing a plain GREY POLO SHIRT with sleeves rolled, dark sturdy trousers, company lanyard.',
  christina: 'CHRISTINA DROSS - 38, slim and upright with squared shoulders, 5 foot 6, sleek dark brown bob with a blunt fringe, tailored charcoal blazer over a cream blouse, tailored trousers, low block heels, minimal gold jewellery, company lanyard. Cold, controlled, faint deadpan smile.',
  maureen: 'MAUREEN the canteen worker - 58, average build, short greying curly hair pinned back, reading glasses on a chain around her neck, a beige apron over a white polo shirt. She stands behind the servery counter.',
};

const CROWD = 'THE CROWD - about ten to twelve British office workers in smart-casual clothes with company lanyards. Four of them are the specific people in the full-body studio reference photos and MUST match those photos exactly: a 45-year-old Black British woman with short natural curly black hair in a mustard-yellow knit top and grey trousers; a 55-year-old British South Asian man with greying hair and a short grey beard in a charcoal crew-neck jumper over a pale blue collar and navy chinos; a woman in her thirties with long light brown wavy hair in a white floral-print blouse and navy trousers; a man in his thirties with dark hair and glasses in a blue checked shirt.';

// The prop taser, described by APPEARANCE so it reads unmistakably as a stun device
// rather than a pistol silhouette. The first pass returned a plain black blocky
// object that was legible but generic. No brand name is printed on the prop.
const TASER = 'THE PROP - a bright YELLOW and black handheld electroshock stun device of the familiar police pattern: a chunky high-visibility yellow plastic body with a black grip and a black squared-off front, clearly a non-lethal stun device and obviously NOT a firearm. It is unmistakably yellow. No brand name or lettering on it.';

// State that must persist once it has happened.
const SMASHED_CHINA = 'ON THE FLOOR - broken white china plates and bowls lie smashed across the pale tiled floor in front of the servery counter, in scattered shards and larger fragments. This mess stays on the floor and is never cleared.';
const BROKEN_WINDOW = 'THE WINDOW - one tall glass pane of the window wall is now SHATTERED and mostly gone, leaving a jagged empty black metal frame with glass teeth around the edge and a wide spray of broken glass across the floor beneath it. Daylight and outside air come straight through the hole. The other panes are still intact.';

module.exports = {
  // Restores the scene's causal setup, which was in the script but in no asset:
  // "prepared by the canteen team to a specific high-sugar recipe given by Christina.
  // Even the canteen staff thought the sugar content was far too high, but Christina
  // assured them it was fine." Without it Jan simply explodes about a pastry and the
  // Christina throughline from Scene 1 pays off nowhere. Set the PREVIOUS DAY, so the
  // counter is dressed differently: full trays, no crowd, no mess.
  s3_00_christina_recipe: {
    beat: 'THE DAY BEFORE - Christina dictates the high-sugar recipe over Maureen objecting',
    refs: [SERVERY, CHRISTINA, MAUREEN],
    prompt: [
      'Photoreal cinematic film still, 35mm lens, natural daylight, medium two-shot across the servery counter.',
      LOCATION,
      'THIS IS THE PREVIOUS DAY, BEFORE THE MAIN SCENE - the canteen is quiet and closed, no queue and no diners, and the counter is clean and undamaged.',
      C.christina,
      'She stands on the near side of the counter holding out a printed recipe card toward Maureen, tapping one line on it with a manicured finger, chin slightly raised, giving a small cold reassuring smile that does not reach her eyes. Entirely unbothered.',
      C.maureen,
      'She is behind the counter holding a large catering bag of white sugar in one hand, looking down at the recipe card with her eyebrows raised and her mouth open in doubt, clearly about to object to the quantity.',
      'ON THE COUNTER between them - baking trays of unbaked pain au chocolat pastries ready for the oven, a set of kitchen scales, and an open bag of sugar. No people other than these two.',
      NO_CITY, STYLE,
    ].join(' '),
  },

  s3_01_canteen_busy: {
    beat: 'Canteen busy with free pastries; the last one is claimed just before Jan enters',
    refs: [MASTER, CHRIS, E1, E2, E3, E4],
    prompt: [
      'Photoreal cinematic film still, 35mm lens, natural daylight, wide establishing shot of a busy staff canteen at mid-morning.',
      LOCATION,
      CROWD,
      'They are queueing along the servery counter and sitting at the tables eating and talking, relaxed and cheerful, trays and coffee cups on the tables. There is a real crush of people around the counter because the food is free.',
      'ALSO IN THE CROWD - ' + C.chris + ' He is in the queue partway along the counter, holding a tray, chatting to the person beside him. He is present but not the focus.',
      'THE STORY DETAIL - on the counter under the glass sneeze guard, large stainless serving trays of pain au chocolat pastries, nearly all taken. One office worker at the front of the queue is lifting the very LAST pastry off the tray with tongs onto their plate, leaving the tray empty behind them.',
      NO_CITY, STYLE,
    ].join(' '),
  },

  s3_02_jan_asks_maureen: {
    beat: 'Jan asks for a pain au chocolat; Maureen: "Sorry, all gone."',
    refs: [SERVERY, JAN, MAUREEN, E3, E4],
    prompt: [
      'Photoreal cinematic film still, 35mm lens, natural daylight, medium two-shot across the servery counter.',
      LOCATION,
      C.jan,
      'He stands on the near side of the servery counter looking down at the empty trays, expectant and slightly impatient, mid-question, one hand resting on the counter edge.',
      C.maureen,
      'She faces him from behind the counter, apologetic but brisk, giving a small palms-up shrug.',
      'THE STORY DETAIL - the large stainless serving trays between them are EMPTY except for scattered crumbs and a few discarded paper cake cases. Beside them, tall stacks of white china plates and bowls sit close to the counter edge, intact.',
      'A few other office workers are queueing behind Jan, including the Black British woman in the mustard-yellow knit top and the South Asian man with the grey beard in the charcoal jumper.',
      NO_CITY, STYLE,
    ].join(' '),
  },

  s3_03_that_is_it: {
    beat: 'Jan, veins bulging: "OH THAT IS IT!"',
    // The crowd has to be here. The canteen was established busy in clip 1 and every
    // person in it freezes and stares in clip 4, so an empty room in between reads as a
    // jump cut to a different time of day. First attempt omitted them and came back
    // deserted.
    refs: [SERVERY, JAN, MAUREEN, E3, E4],
    prompt: [
      'Photoreal cinematic film still, 35mm lens, natural daylight, medium close shot on Jan, pushed in tight.',
      LOCATION,
      C.jan,
      'He has snapped: face flushed deep red and blotchy, veins standing out at his temple and neck, eyes bulging, mouth wide open bellowing, both fists clenched at his sides, leaning forward over the counter. Utterly disproportionate rage over a pastry.',
      C.maureen,
      'She is behind the counter recoiling slightly, eyebrows up, startled and unimpressed rather than frightened.',
      'The empty crumb-strewn trays and the intact stacks of white china plates are still on the counter between them.',
      'WARDROBE CHECK - his DARK RED TIE must be clearly visible, knotted at the open collar and hanging loose down the front of his pale blue shirt. He is wearing a tie in this shot, as he is in every other shot of this scene.',
      'THE ROOM IS BUSY - other office workers are queueing behind Jan along the counter and sitting at the tables beyond, including the Black British woman in the mustard-yellow knit top and the South Asian man with the grey beard in the charcoal jumper. Several of them have turned toward the noise and are starting to look at Jan. The canteen is NOT empty.',
      NO_CITY, STYLE,
    ].join(' '),
  },

  s3_04_plates_swept: {
    beat: 'AFTERMATH - plates swept off the counter, china smashed, the room frozen and staring',
    refs: [SERVERY, JAN, MAUREEN, CHRIS, E3, E4],
    prompt: [
      'Photoreal cinematic film still, 35mm lens, natural daylight, wide shot taking in the counter, Jan, and the watching room.',
      LOCATION,
      'This is the MOMENT IMMEDIATELY AFTER Jan has swept the stacks of china off the counter onto the floor.',
      C.jan,
      'He stands at the counter with both arms still flung out sideways at the end of the sweeping motion, breathing hard, face flushed, glaring. The counter top in front of him is now BARE and wiped clear where the plates used to be.',
      SMASHED_CHINA,
      C.maureen,
      'She stands behind the counter with a hand to her mouth, staring at the mess.',
      CROWD,
      'ALSO IN THE CROWD - ' + C.chris + ' He stands among the onlookers holding his tray, staring at Jan like everyone else. Present but not the focus.',
      'CRITICAL - every single person in the room has STOPPED and is staring at Jan in frozen silence. Forks halfway to mouths, mid-conversation, heads all turned toward him, nobody eating, nobody talking. The whole canteen is frozen.',
      NO_CITY, STYLE,
    ].join(' '),
  },

  s3_05_mba_scream: {
    beat: '"I HAVE HAD IT WITH THIS PLACE! I HAVE AN MBA, NOBODY APPRECIATES MY IMMENSE TALENT!"',
    refs: [MASTER, JAN, E1, E2, E3, E4],
    prompt: [
      'Photoreal cinematic film still, 35mm lens, natural daylight, medium-wide shot on Jan with the frozen room behind him.',
      LOCATION,
      C.jan,
      'He stands in the middle of the canteen floor screaming at the whole room, head thrown back, mouth wide open, face flushed purple-red, veins standing out, both arms flung wide, spittle flying, completely unhinged.',
      SMASHED_CHINA,
      CROWD,
      'They are frozen and staring at him in appalled silence, some half-risen from their seats, a few edging back. Nobody is laughing at him now.',
      'The full-height glazed window wall behind them is still completely INTACT and unbroken.',
      NO_CITY, STYLE,
    ].join(' '),
  },

  s3_06_chair_through_window: {
    beat: 'AFTERMATH - the chair has gone through the window, glass shattered',
    refs: [WINDOW, JAN, E3, E4],
    prompt: [
      'Photoreal cinematic film still, 35mm lens, natural daylight, wide shot facing the window wall.',
      LOCATION,
      'This is the MOMENT IMMEDIATELY AFTER Jan has hurled a heavy meeting chair through the glass.',
      BROKEN_WINDOW,
      'The heavy dark grey upholstered meeting chair that went through it now lies on its side out on the paving of the courtyard, just beyond the hole, among glittering broken glass.',
      C.jan,
      'He stands a few paces back inside the canteen at the end of his throwing follow-through, arms still extended toward the window, body twisted from the effort, face flushed and furious, chest heaving. Beside him the stack of remaining meeting chairs against the brick pier is now visibly one chair shorter and slightly disturbed.',
      'A few office workers are visible further back, frozen, staring, one with hands over their mouth.',
      NO_CITY, STYLE,
    ].join(' '),
  },

  // Clip 7 was carrying four distinct actions plus Rick's reveal behind a single
  // aftermath frame -- Jan turning back, grabbing a second chair, freezing at the
  // discharge, and dropping. Split so the video has a real start frame for the grab
  // instead of inventing it. Rick must NOT appear here; the reveal belongs to 07b.
  s3_07a_second_chair: {
    beat: 'Jan turns back and grabs a second chair -- the moment before the discharge',
    refs: [WINDOW, JAN, E3, E4],
    prompt: [
      'Photoreal cinematic film still, 35mm lens, natural daylight, medium-wide shot facing the window wall.',
      LOCATION,
      C.jan,
      'He has turned BACK toward the stack of heavy meeting chairs against the brick pier and has both hands on the topmost chair, lifting it clear of the stack, body braced and twisted with the effort, face flushed deep red, teeth bared, still mid-rage and about to throw again.',
      BROKEN_WINDOW,
      'The first chair he already threw lies on its side out on the courtyard paving beyond the hole.',
      'CRITICAL - Rick is NOT in this shot and must not appear anywhere in frame. Office workers stand well back around the edges of the room, frozen and appalled, some with hands over their mouths, nobody intervening.',
      NO_CITY, STYLE,
    ].join(' '),
  },

  s3_07b_taser_collapse: {
    beat: 'Jan face-down unconscious; Rick revealed behind him with the prop taser',
    refs: [WINDOW, JAN, RICK, E3, E4],
    prompt: [
      'Photoreal cinematic film still, 35mm lens, natural daylight, wide shot.',
      LOCATION,
      'This is the MOMENT IMMEDIATELY AFTER Jan has dropped. Nothing violent is happening in this frame - it is the calm aftermath.',
      'JAN lies FACE-DOWN on the pale tiled floor, completely limp and unconscious, arms loose at his sides, cheek against the tiles, eyes closed. He is a 52-year-old overweight British man in a too-tight dark navy suit jacket over a pale blue shirt and a dark red tie, thinning greying mid-brown hair. A second meeting chair lies on the floor beside him where he dropped it.',
      C.rick,
      TASER,
      'He stands calmly a couple of paces BEHIND Jan, looking down at him, entirely unbothered and matter-of-fact, holding the yellow prop stun device loosely at his side, already lowering it, its yellow body clearly visible against his dark trousers. His expression is mild, almost bored - the demeanour of a man who has solved a minor problem.',
      BROKEN_WINDOW,
      'Office workers stand further back around the edges of the room, frozen mid-gasp, hands over mouths, staring.',
      NO_CITY, STYLE,
    ].join(' '),
  },

  s3_08_have_you_killed_him: {
    beat: 'Chris crouches over Jan: "Have you killed him?"',
    refs: [WINDOW, JAN, CHRIS, RICK],
    prompt: [
      'Photoreal cinematic film still, 35mm lens, natural daylight, low medium shot close to floor level.',
      LOCATION,
      'JAN lies face-down and motionless on the pale tiled floor in the foreground, unconscious, a 52-year-old overweight British man in a too-tight dark navy suit jacket over a pale blue shirt and dark red tie.',
      C.chris,
      'He is CROUCHED down on his haunches beside Jan, one forearm resting on his knee, leaning over to peer at Jan\'s face with an expression of mild alarm mixed with curiosity, mid-question, looking UP and off to the side toward Rick rather than at Jan.',
      C.rick,
      'He stands above and behind them both, looking down, calm and unhurried.',
      BROKEN_WINDOW,
      NO_CITY, STYLE,
    ].join(' '),
  },

  s3_09_rick_reply: {
    beat: 'Rick stows the prop taser: "...I think we need the police here..."',
    refs: [WINDOW, JAN, RICK, CHRIS, E3, E4],
    prompt: [
      'Photoreal cinematic film still, 35mm lens, natural daylight, medium two-shot on Rick and Chris with Jan on the floor.',
      LOCATION,
      C.rick,
      TASER,
      'He is the focus of the shot, standing over the unconscious Jan, calmly tucking the yellow prop stun device away into his trouser pocket without looking at it, the yellow body still clearly visible in his hand as it goes, mid-sentence, completely relaxed and matter-of-fact, faintly pleased with himself.',
      C.chris,
      'He is still crouched beside Jan, looking up at Rick, eyebrows raised, listening.',
      'JAN lies face-down and motionless on the tiled floor between and below them, unconscious, in the too-tight navy suit jacket over a pale blue shirt and dark red tie.',
      BROKEN_WINDOW,
      'A ring of office workers stands watching from a few paces back, including the Black British woman in the mustard-yellow knit top and the South Asian man with the grey beard in the charcoal jumper.',
      NO_CITY, STYLE,
    ].join(' '),
  },
};
