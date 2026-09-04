// Scene 3 VIDEO clip definitions -- MiniMax H3 on Higgsfield (2K, 2560x1440).
//
// SIX clips, ~50s, covering CTS_Featurette_Episode.fountain L152-196. Combined from the
// eleven planned beats per VIDEO_BUDGET.md: Higgsfield bills per SECOND, not per clip,
// and Scene 3 has only 64 spoken words across eleven beats -- eight of which fall under
// the 5s minimum. Generating beat-by-beat wasted ~24% on padding. Chaining consecutive
// beats into one call takes it from 126 credits to 100.
//
// Combining is also better filmmaking here. Clips C, D and E are exactly the
// destruction pairs, so the china breaking, the window going and Jan dropping all happen
// as continuous motion inside one clip instead of across a cut.
//
// DIFFERENT FROM fal: Higgsfield's MiniMax H3 takes an ARBITRARY duration up to 15s
// (.agents/rules/clip_duration_rules.md), so nothing is snapped and there is no slack to
// direct. Durations below are the measured content lengths.
//
// Dialogue is verbatim from the fountain -- including Rick's "I knew this Taser would
// come in useful one day in this place", which scene_dialogue_audio_guide.md drops.
// Audio must be in the prompt: MiniMax generates it in the same pass and this project
// has no separate TTS or foley stage.

const S = 'scene3-stills';

const CAST = 'JAN is 52, overweight, thinning greying hair, in a too-tight dark navy suit jacket over a PALE BLUE shirt with a DARK RED tie (this is the NEXT MORNING, a different shirt and tie from the previous scenes). CHRIS is 32, lean, dark hair, LIGHT BLUE shirt with rolled sleeves and tan chinos. RICK is 40, broad, greying near-buzzcut, plain GREY POLO. MAUREEN is 58, short greying curly hair, reading glasses on a chain, beige apron over a white polo. The crowd are British office workers in smart-casual clothes with lanyards.';

const LOOK = 'Photoreal live-action comedy, 35mm lens, natural daylight through a full-height glazed wall, handheld-steady camera. Keep every face, costume and the set exactly as in the reference frame.';

// Learned on Scene 2's c01: giving a movement SPEED ("push in slowly") is read as
// licence and the camera overshoots, which breaks the join with the next clip. Give it
// a framing TARGET instead.
const FRAMING = 'CAMERA: hold the reference frame shot size. Any movement is a very slight drift only -- the framing at the END of the clip must still match the framing at the START. Do not push in, do not zoom, do not reframe to a tighter shot.';

const NOTEXT = 'No on-screen text, captions or subtitles.';

module.exports = {
  d01_christina_recipe: {
    beats: 'Clip 0 — THE DAY BEFORE: Christina dictates the high-sugar recipe',
    seconds: 6,
    startImage: `${S}/s3_00_christina_recipe.png`,
    prompt: [
      LOOK, CAST, FRAMING,
      'CHRISTINA DROSS is 38, slim, sleek dark brown bob with a blunt fringe, tailored charcoal blazer, cold and controlled.',
      'ACTION: this is the PREVIOUS DAY and the canteen is closed and empty. Christina holds out a printed recipe card to Maureen across the servery counter and taps one line on it with a manicured finger. Maureen, holding a large bag of sugar, looks down at it and starts to object, eyebrows raised. Christina gives a small cold reassuring smile that does not reach her eyes, waves the objection away, and turns to leave.',
      'DIALOGUE: MAUREEN (doubtful, professional): "That is... an awful lot of sugar." Then CHRISTINA (smooth, dismissive, already turning away): "It is fine. Make it exactly as written."',
      'AUDIO: quiet empty-canteen room tone, a kitchen extractor humming, the rustle of the sugar bag. No music.',
      NOTEXT,
    ].join(' '),
  },

  d02_busy_and_asks: {
    beats: 'Clips 1+2 — busy canteen, last pastry claimed, Jan asks Maureen',
    seconds: 9,
    startImage: `${S}/s3_01_canteen_busy.png`,
    endImage: `${S}/s3_02_jan_asks_maureen.png`,
    prompt: [
      LOOK, CAST,
      'ACTION: begin exactly on the first frame — a busy canteen at mid-morning, a queue along the servery, people eating and talking. An office worker at the front of the queue lifts the VERY LAST pain au chocolat off the tray with tongs onto their plate, leaving the tray empty but for crumbs. Jan then enters and crosses to the counter, looking down expectantly at the emptied trays. Maureen faces him from behind the counter and gives a small apologetic palms-up shrug. End exactly on the final frame.',
      'DIALOGUE: JAN (expectant, slightly impatient): "Is there any more pain au chocolat?" Then MAUREEN (apologetic but brisk): "Sorry, all gone."',
      'AUDIO: busy canteen ambience — cutlery, overlapping chatter, a coffee machine — continuing normally under the dialogue. The room has not noticed anything yet.',
      NOTEXT,
    ].join(' '),
  },

  d03_snap_and_sweep: {
    beats: 'Clips 3+4 — "OH THAT IS IT!" then the plates go on the floor',
    seconds: 8,
    // Keyframe pair: the china is intact in the first frame and smashed in the last, so
    // the sweep happens as motion between them. This is why clip 4's still was anchored
    // on aftermath rather than mid-action -- still models render shattering badly.
    startImage: `${S}/s3_03_that_is_it.png`,
    endImage: `${S}/s3_04_plates_swept.png`,
    prompt: [
      LOOK, CAST,
      'ACTION: begin exactly on the first frame with Jan at the counter, the stacks of white china plates and bowls beside him intact. He snaps — face flushing deep red and blotchy, veins standing out at his temple, fists clenching — and bellows. He then sweeps both arms violently across the counter, hurling the stacks of china onto the tiled floor where they SMASH. Every single person in the canteen stops and stares at him in frozen silence. Maureen puts a hand to her mouth. End exactly on the final frame, china in pieces across the floor.',
      'DIALOGUE: JAN (erupting, veins bulging): "OH THAT IS IT!"',
      'AUDIO: the busy ambience cutting out the instant he shouts, then a huge CRASH of shattering china, then total shocked silence. The silence is as important as the crash.',
      NOTEXT,
    ].join(' '),
  },

  d04_scream_and_window: {
    beats: 'Clips 5+6 — the MBA scream, then the chair through the window',
    seconds: 10,
    startImage: `${S}/s3_05_mba_scream.png`,
    endImage: `${S}/s3_06_chair_through_window.png`,
    prompt: [
      LOOK, CAST,
      'ACTION: begin exactly on the first frame — Jan standing amid the broken china, screaming at the whole room, head thrown back, arms flung wide, face purple-red. The crowd are frozen and appalled, some edging back. He then turns, seizes a heavy dark grey meeting chair from the stack against the brick pier, and HURLS it into the full-height glazed window wall, which SHATTERS. End exactly on the final frame — the pane gone, jagged glass in the frame, the chair out on the courtyard paving beyond, glass across the floor.',
      'DIALOGUE: JAN (screaming, unhinged): "I HAVE HAD IT WITH THIS PLACE! I HAVE AN MBA, NOBODY APPRECIATES MY IMMENSE TALENT!"',
      'AUDIO: his scream echoing off the hard floor, then a chair scraping off a stack, then a huge explosion of breaking plate glass and the chair clattering onto paving outside, then screams from the crowd.',
      NOTEXT,
    ].join(' '),
  },

  d05_second_chair_and_taser: {
    beats: 'Clips 7a+7b — Jan turns for a second chair, the discharge, he drops; Rick revealed',
    seconds: 8,
    startImage: `${S}/s3_07a_second_chair.png`,
    endImage: `${S}/s3_07b_taser_collapse.png`,
    prompt: [
      LOOK, CAST,
      'ACTION: begin exactly on the first frame — Jan has turned back to the chair stack and is lifting another heavy chair above his head, teeth bared, still in full rage. RICK steps into frame behind him holding a bright YELLOW and black handheld stun device, clearly a non-lethal prop and obviously not a firearm. There is a sharp electrical discharge. Jan FREEZES mid-motion, the chair drops from his hands and clatters to the floor, and he slumps forward and falls face-first onto the tiles, completely limp and unconscious. Rick lowers the device to his side and looks down at him, entirely calm and matter-of-fact. Onlookers gasp, hands over mouths. End exactly on the final frame.',
      'DIALOGUE: none. Nobody speaks.',
      'AUDIO: a loud electric POP-CRACKLE-ZZZZT discharge, the chair clattering onto tile, a heavy body thud, and gasps from the crowd. Then quiet.',
      NOTEXT,
    ].join(' '),
  },

  d06_killed_him_and_reply: {
    beats: 'Clips 8+9 — "Have you killed him?" and Rick\'s full reply, into FADE OUT',
    seconds: 13,
    startImage: `${S}/s3_08_have_you_killed_him.png`,
    endImage: `${S}/s3_09_rick_reply.png`,
    prompt: [
      LOOK, CAST, FRAMING,
      'ACTION: begin exactly on the first frame — Chris crouched on his haunches beside the unconscious Jan, looking up at Rick. Rick stands over them, calm and unhurried, then tucks the yellow stun device away into his trouser pocket without looking at it, faintly pleased with himself. A ring of office workers watches from a few paces back. End exactly on the final frame, then HOLD for a beat and FADE TO BLACK — this is the last shot of the episode.',
      'DIALOGUE: CHRIS (crouching, mild alarm and curiosity, looking up): "Have you killed him?" Then RICK (completely deadpan, unhurried, faintly satisfied): "No relax, he will be out for a while. I knew this Taser would come in useful one day in this place. I think we need the police here..."',
      'CRITICAL FOR RICK: he is utterly matter-of-fact throughout, as though this were a minor administrative task. No alarm, no urgency, no raised voice. The flatness is the joke.',
      'AUDIO: a shocked murmur returning from the crowd under the dialogue, then quiet as the picture fades.',
      NOTEXT,
    ].join(' '),
  },
};
