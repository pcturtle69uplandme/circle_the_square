// Scene 2 VIDEO clip definitions -- MiniMax H3 Max on fal.ai.
//
// Ten clips, ~109s, covering CTS_Featurette_Episode.fountain L88-151. Derived from
// SCENE2_VIDEO_SCRIPT.md's beat-by-beat audit and costed in VIDEO_BUDGET.md.
//
// THREE THINGS ARE ENCODED HERE THAT THE STILLS COULD NOT CARRY:
//
// 1. DIALOGUE IS VERBATIM FROM THE FOUNTAIN, never from scene_dialogue_audio_guide.md.
//    The guide deletes "You're dreaming Jan!" and "What?!" from the Inception exchange,
//    which removes the double meaning and Jan missing it, leaving Chris merely stating
//    a film fact. It also paraphrases Jan's closing speech. See SCENE2_VIDEO_SCRIPT 1.1.
//
// 2. AUDIO IS PART OF THE PROMPT. MiniMax H3 Max generates synchronised audio in the
//    same pass -- there is no separate TTS, foley or lip-sync stage anywhere in this
//    project -- so every line, SFX and ambience change has to be described here.
//
// 3. KEYFRAME PAIRS. Clips with an `endImage` are first-to-last frame generations: the
//    model animates BETWEEN two adopted stills. That is how the blinds open (c02) and
//    how Jan's reaction lands (c07) without either state having to be invented.
//
// CAMERA DRIFT AND CHAINING. A clip's prompt can ask for a slow push-in and get a much
// bigger move: c01 was written wide and came back a medium two-shot. That is fine inside
// a clip but breaks the JOIN, because the next clip would seed from a framing the camera
// has already left. Clips that continue the same action therefore carry `chainFrom`,
// which seeds them from the PREVIOUS clip's real last frame instead of an adopted still
// (extract it with last_frame.js).
//
// Do not chain everywhere. Scene 1 measured generational drift compounding down a chain
// -- brightness falling and shadows crushing roughly twice every ~4 links -- so reset to
// an adopted still at every genuine cut, which is most of this scene. Only c02 continues
// c01's action; the rest are cuts and keep their own stills.
//
// HANDLING THE FIXED DURATIONS. fal offers only 5s/10s/15s, and every clip is snapped
// UP so no line is ever cut mid-delivery. The danger of snapping up is NOT dead air --
// it is that the model invents business, repeats a gesture, or worst of all invents
// dialogue, to fill time it was given and told nothing about. So every clip with slack
// carries an explicit TIMING line saying where the dialogue ends and exactly what to
// hold on for the remainder, always ending "No further dialogue."
//
// In practice the slack is an asset rather than a cost: the held beats are the silence
// after "SHUT UP!", the blank non-reaction to the name "Inception", and the room
// emptying around Jan at the end. Those are comedy beats the scene wants anyway.
//
// DURATION IS NOT FREE-FORM. fal's sandbox offers only 5s, 10s and 15s -- verified on
// the live page 2026-09-04. Every clip below is snapped UP to the next allowed value so
// a line can never be cut off mid-delivery; the spare tail is trimmed in the edit. The
// beat estimates the snapping came from are in VIDEO_BUDGET.md.

const S = 'scene2-stills';

// Restated in every clip: the model gets one still, not the scene bible.
const CAST = 'JAN is 52, overweight, thinning greying hair, too-tight navy suit over a white shirt with the tie loosened askew, shirt re-buttoned crookedly. CHRIS is 32, lean, dark hair, LIGHT BLUE shirt with rolled sleeves and tan chinos. RICK is 40, broad, greying near-buzzcut, plain GREY POLO. The crowd are British office workers in smart-casual clothes with lanyards.';

// LANGUAGE PIN. MiniMax H3 is a Chinese model and drifts: two identical-setup renders
// of c01 produced one perfect English take and one entirely in MANDARIN (Whisper:
// 你會衝動,你會再接觸). Nothing in the prompt said which language to speak. State it
// explicitly on every clip, and verify every render with verify_clip_audio.py.
const LANG = 'ALL SPOKEN DIALOGUE IS IN ENGLISH, spoken by British characters with British accents. Do not speak, sing or caption any other language. No Mandarin, no Chinese.';

const LOOK = 'Photoreal live-action comedy, 35mm lens, natural office daylight, handheld-steady camera. Keep every face, costume and the set exactly as in the reference frame. No on-screen text, captions or subtitles.';

// c01 was written as a wide two-shot with "push in very slowly" and came back a MEDIUM
// two-shot -- a much bigger move than asked. That is survivable inside a clip but it
// breaks the join with the next one. State the shot size at the START and at the END so
// the model has a framing target rather than a vague speed, and cap the travel.
const FRAMING = 'CAMERA: stay close to the reference frame shot size. Gentle handheld life and a small drift are welcome, but do not travel to a significantly tighter or wider framing -- the shot should still read as the same setup at the end as at the start.';

module.exports = {
  c01_corridor_gossip: {
    beats: 'Shot 06 — Chris and Rick gossip outside Jan\'s shut office door',
    seconds: 10,
    startImage: `${S}/shot06_corridor_gossip.png`,
    prompt: [
      LOOK, CAST, LANG, FRAMING,
      'ACTION: Chris and Rick stand in the corridor beside the desk run. The glazed office door behind them stays shut with its venetian blinds closed flat and opaque throughout — nothing inside is ever visible. Chris tilts his head toward the shut door as he speaks, exasperated and amused. Rick does not react at all, arms folded, staring flatly ahead — his complete lack of reaction is the joke. Camera holds steady.',
      'DIALOGUE: @Chris (speaking in a dry, wry South London Estuary English accent): "Christ! They don\'t even try to hide it any more do they." Then RICK : "Never have. Give it another five minutes." CRITICAL FOR RICK: he delivers this in a completely FLAT monotone with a DEAD, MOTIONLESS face. His eyebrows do not move, he does not smile, he does not turn to look at Chris, he does not react in any way at all. Only his mouth moves to form the words. His total non-reaction IS the joke and must read as deliberate deadpan, not as ordinary conversation.',
      'AUDIO: quiet open-plan office ambience — distant keyboards, a phone ringing far off. No music.',
      "TIMING: the dialogue occupies the first 8 seconds. HOLD the final 2 seconds on Rick's completely blank, unmoving deadpan while Chris waits for a reaction that never comes. No further dialogue, no new action.",
    ].join(' '),
  },



  c02a_blinds_raised: {
    beats: 'Shot 06→07 bridge — the blinds go up and the door opens, before Sharon appears',
    // Nobody who needs identity-locking is in this shot, so a start frame alone is
    // enough. Splitting the blinds action out gives it the whole clip instead of
    // competing with Sharon's exit, which is what the single combined attempt failed at.
    seconds: 5,
    startImage: `${S}/shot06_corridor_gossip.png`,
    prompt: [
      LOOK, CAST, LANG, FRAMING,
      'ACTION: hold on the corridor with the glazed office door shut and its venetian blinds closed flat and opaque. Partway through, the blinds are RAISED from inside, folding up to the top of the glass and revealing the lit office interior behind it. The door handle turns and the door begins to open. Nobody comes out yet — the clip ends as the door swings open on the empty-looking doorway. Chris and Rick stand where they are and turn their heads toward the movement.',
      'DIALOGUE: none. Nobody speaks.',
      'AUDIO: quiet office ambience, then the distinct rattle and clack of a venetian blind being raised, then a door latch turning.',
    ].join(' '),
  },

  c02b_sharon_exits: {
    beats: 'Shot 07 — the blinds go up, the door opens, Sharon leaves dishevelled',
    seconds: 10,
    // Keyframe pair. Fixes the continuity hole flagged in SCENE2_VIDEO_SCRIPT 2.1:
    // clip 1 ends with the blinds shut, clip 2's still has them open, and nothing
    // showed the change. Animating between the two frames IS the explanation.
    //
    // chainFrom was TRIED HERE AND REVERTED. c01 overshot to a medium two-shot, so
    // chaining asked the model to pull the camera back out, relocate Chris and Rick,
    // raise the blinds, open the door AND produce Sharon in five seconds. It dropped the
    // actions and teleported the people: Sharon simply appeared mid-corridor having never
    // come out of the office. Chaining only helps when the previous clip's END framing
    // already matches this clip's intended START -- otherwise it propagates the error.
    //
    // shot06 -> shot07 is the correct pair: same camera, same geography, Chris and Rick
    // in identical positions in both. The only changes are blinds up, door open, Sharon
    // walks out -- a small coherent transformation the model can actually perform.
    // START FROM shot07, NOT shot06. This is the architectural difference from
    // Higgsfield: there you attach a gallery of character references, but fal gives you
    // only first frame / last frame, so EVERY character who needs identity-locking must
    // already be IN the start frame. shot06 contains only Chris and Rick, so starting
    // there left Sharon and Jan to be invented from text -- and Sharon has to match her
    // Scene 1 appearance. shot07 contains all four (Sharon mid-exit, Jan seated inside,
    // Chris and Rick watching), so it anchors everyone.
    //
    // The cost is that shot07 already has the blinds up and the door open, so the
    // blinds-raise is no longer inside this clip -- see c02a below, which does it with
    // nobody in shot and therefore needs no anchoring.
    startImage: `${S}/shot07_sharon_exits.png`,
    prompt: [
      LOOK, CAST, LANG,
      'ACTION: begin exactly on the first frame — Sharon in the open office doorway, Jan seated at his desk inside behind her, Chris and Rick further down the corridor. Sharon walks OUT of the doorway and away down the corridor toward camera, smoothing her creased blouse and pushing her mussed hair back, eyes down, dazed but trying to compose herself. She is dishevelled: hair out of place, makeup smudged, a light sheen of sweat. Jan stays seated inside and does not look out. CHRIS AND RICK DO NOT MOVE — they stay where the first frame puts them and simply turn their heads to watch her pass.',
      'DIALOGUE: none. Nobody speaks.',
      'AUDIO: the rattle and clack of a venetian blind being raised, a door handle, her heels on carpet tile, and a single quiet snigger from Chris.',
    ].join(' '),
  },

  c03_jan_addresses: {
    beats: 'Shot 07b-1 — Jan emerges, claps, is asked about Sharon, deflects',
    seconds: 15,
    startImage: `${S}/shot07b1_jan_addresses.png`,
    prompt: [
      LOOK, CAST, LANG, FRAMING,
      'ACTION: Jan stands at the focal point where the corridor meets the open-plan desks, shirt re-buttoned askew, tie crooked, self-important and pleased with himself. He claps his hands together twice to gather everyone, and the staff drift in around him. He begins his address, chin raised. Chris, standing in the crowd on the right, half-raises a hand and cuts in with a pointed question. Jan\'s composure slips for a moment — eyes flicking away, a tug at his collar — before he recovers and answers smoothly.',
      'DIALOGUE: @Jan (speaking in a booming, self-important English Home Counties accent): "Right guys, as you know —" Then @Chris (speaking in a South London Estuary English accent, interrupting): "Does Sharon get a pass on attending this?" Then @Jan (speaking in an evasive English Home Counties accent): "Err... yes she does. I have given her the rest of the day off for personal reasons."',
      'AUDIO: two sharp handclaps, footsteps and chair scrapes as people gather, then attentive quiet under the dialogue.',
      'TIMING: the dialogue occupies the first 13 seconds. HOLD the final 2 seconds on Jan looking pleased with his own answer while the crowd stare back flatly. No further dialogue.',
    ].join(' '),
  },

  c04_shut_up: {
    beats: 'Shot 07b-2 — sniggering ripples, Jan flares up',
    seconds: 15,
    startImage: `${S}/shot07b2_shut_up_flareup.png`,
    prompt: [
      LOOK, CAST, LANG, FRAMING,
      'ACTION: the shot opens on the crowd. Quiet sniggering spreads through them person to person — one snorts, another claps a hand over their mouth, shoulders shaking, people glancing at each other, all trying and failing not to laugh at him. Jan\'s face darkens and reddens as he watches it spread, then he erupts, both hands raised and open in exasperation. The laughter cuts dead instantly. Camera holds steady on Jan as he shouts.',
      'DIALOGUE: @Jan (shouting in a furious English Home Counties accent): "SHUT UP! I am truly appalled by the lack of discipline in this place and that changes now! I have decided a new project is required to manage all the change around here."',
      'AUDIO: suppressed sniggering building and spreading, then abrupt total silence the instant he shouts. His voice echoes slightly off the hard floor.',
      'TIMING: the dialogue ends at about 12 seconds. HOLD the final 3 seconds on total frozen silence -- Jan breathing hard and glaring, the crowd rigid and not daring to move. The silence after the outburst is the joke. No further dialogue.',
    ].join(' '),
  },

  c05_rick_questions: {
    beats: 'Shot 07c-1 — Rick challenges the old project, Jan starts justifying',
    seconds: 15,
    startImage: `${S}/shot07c1_rick_questions.png`,
    prompt: [
      LOOK, CAST, LANG, FRAMING,
      'ACTION: Rick, arms folded, delivers his question flat and blunt, with a small deliberate pause before the last three words. Jan\'s pleased expression curdles. He turns to face Rick and begins a long defensive explanation, one hand raised palm-up in a placating, patronising gesture, chin lifted. The crowd watch, a few exchanging looks.',
      'DIALOGUE: @Rick (speaking in a flat deadpan northern English accent): "What happened to the last project for this, isn\'t it ongoing? By that I mean... completely failing." Then @Jan (speaking in a defensive, patronising English Home Counties accent): "There\'s no need for the previous project as everything has been a great success even though most things were not delivered on time or within budget."',
      'AUDIO: a low ripple of amusement from the crowd after Rick\'s line, quickly suppressed. Otherwise quiet.',
    ].join(' '),
  },

  c06_naming_inception: {
    beats: 'Shot 07c-2 — Jan finishes justifying and names the project',
    seconds: 15,
    // ACCEPTED TAKE chains from c05's real last frame, NOT shot07c2_naming_inception.png.
    // Jan's justification-into-naming is one unbroken speech in the fountain, split only
    // for fal's 15s cap -- no scene/beat break here. A fresh-still take from shot07c2 (a
    // different, wider angle by Jan's office door) rendered and passed QA but read as Jan
    // warping to a new shot mid-sentence. See
    // .agents/rules/location_continuity_rules.md ("Never let a still-speaking character
    // warp to a different shot mid-line").
    //
    // v2: also has RICK WALK OFF during the final silent hold. c07's accepted take (the
    // shot08a/shot08b keyframe pair) never included Rick, which read as him vanishing
    // between clips. Rather than risk another broken fix on c07 (already tried once, see
    // run_c07_inception_exchange_v2_REJECTED.js), c06 now motivates his absence instead:
    // unimpressed, he turns and walks away down the corridor, back to camera, before c06
    // ends -- so c07 opening without him reads as a deliberate exit, not a continuity error.
    startImage: `${S}/../scene2-clips/lastframes/c05_rick_questions_last.png`,
    prompt: [
      LOOK, CAST, LANG, FRAMING,
      'ACTION: begin exactly on the reference frame -- continuing directly from Jan\'s explanation, mid-conversation, no cut. Jan gathers pomposity as he keeps talking, chest puffing up, then builds to the announcement -- one arm raising high and presenting, palm open, beaming as if unveiling a moon landing. Rick stays arms folded beside him, staring flatly, entirely unimpressed. The crowd\'s reaction is flat and unenthused.',
      'DIALOGUE: @Jan (speaking in a pompous English Home Counties accent): "I know because I see everything happening so am best placed to judge. We need a new project to continue the success of the previous project. So I have decided to call the project... Inception."',
      'AUDIO: dead silence on the announcement — no applause, no reaction at all, which is the joke.',
      'TIMING: the dialogue ends at about 13 seconds. HOLD the final 2 seconds on complete silence and blank faces -- nobody reacts to the name at all. That non-reaction is the joke. No further dialogue.',
    ].join(' '),
  },

  c07_inception_exchange: {
    beats: 'Shots 08a + 08b — all FOUR turns of the Inception gag',
    seconds: 10,
    // ACCEPTED TAKE (v3) is a single start image: shot08a_dreaming_heckle_v3.png, composited
    // (fal-tools/api/compose_shot08_heckle_v3.js) from c06's REAL last frame -- so Jan, the
    // crowd, and Rick (still mid-corridor, back turned, walking away) are pixel-accurate --
    // plus Chris added via his character reference sheet. Fixes the two problems the v2
    // composite had: pass `aspect_ratio`/`resolution` explicitly on the nano-banana-pro/edit
    // call (came back 2752x1536, matching the scene, vs. v2's default 1024x1024 square), and
    // leave Rick out of the CAST/dialogue prompt entirely -- he has no lines and is already
    // correctly rendered in the seed image, and naming him alongside Jan/Chris in v2
    // coincided with a voice-swap (Jan's line coming out in Chris's voice). See
    // .agents/rules/location_continuity_rules.md for the full history: v1 (this keyframe
    // pair, kept at scene2-clips/superseded/) had correct aspect/voices but no Rick at all;
    // v2 (run_c07_inception_exchange_v2_REJECTED.js) added him back but broke both.
    startImage: `${S}/shot08a_dreaming_heckle.png`,
    endImage: `${S}/shot08b_inception_explained.png`,
    prompt: [
      LOOK, CAST, LANG,
      'ACTION, ending in the state of the final reference frame (Jan flustered and deflated) -- reach that STATE, the exact framing need not match: Chris shouts from across the room, hands cupped near his mouth, grinning, over rising laughter. Jan turns toward him, genuinely baffled — a blank, uncomprehending stare, he has not got it. Chris then explains patiently with a raised hand, as if to a child, to more laughter. Jan understands, and deflates: mouth open, eyes darting sideways, shoulders dropping, one hand raised in a weak dismissive wave as he covers badly.',
      'DIALOGUE, four turns in order: @Chris (shouting in a South London Estuary English accent): "You\'re dreaming Jan!" Then @Jan (speaking in a baffled English Home Counties accent): "What?!" Then @Chris (speaking in a patient, amused South London Estuary English accent): "Inception is the name of a film about dreams Jan." Then @Jan (speaking in a flustered English Home Counties accent): "Oh, well... it is also the name of this project."',
      'AUDIO: a big laugh on the heckle, a beat of silence on Jan\'s "What?!", then broader laughter on the explanation which Jan talks weakly over.',
    ].join(' '),
  },

  c08_merch_gag: {
    beats: 'Shot 08c — the branded merch, and Jan appoints himself',
    seconds: 15,
    // ACCEPTED TAKE chains from c07's real last frame, NOT shot08c_merch_gag.png. No
    // scene/beat break in the fountain between c07's last line and this one -- same
    // continuous paragraph, same two people (Jan, Chris) already on screen. The merch box
    // is a new PROP, not a new character, so it carries none of the identity-lock risk
    // that ruled out chaining for c07 -- described in text only, referencing this still for
    // the intended look (cardboard box printed "PROJECT INCEPTION", foam balls/pens/shirts
    // inside). See fal-tools/api/run_c08_merch_gag.js and
    // .agents/rules/location_continuity_rules.md.
    startImage: `${S}/shot08c_merch_gag.png`,
    prompt: [
      LOOK, CAST, LANG, FRAMING,
      'ACTION: Jan glances down at a large open cardboard box of branded merchandise on a desk beside him — foam stress balls, pens and folded t-shirts, all printed "PROJECT INCEPTION", with the same printed on the box. His face falls as he realises he has already ordered a thousand of them and it is far too late to change the name. He gestures at the box with a caught-out, sheepish shrug. Chris, facing him, asks a straight question. Jan rallies into smugness, pauses deliberately, and delivers the reveal. The crowd draws breath.',
      'DIALOGUE: @Chris (speaking in a South London Estuary English accent): "Will there be a lead for this?" Then @Jan (speaking in a pompous English Home Counties accent, with a deliberate pause before the last two words): "At last something sensible is asked. Yes there will. However, it is with regret that I have to inform you all that the position has already been filled... by me."',
      'AUDIO: cardboard shifting as he gestures at the box; a collective intake of breath on the reveal.',
      "TIMING: the dialogue ends at about 14 seconds. HOLD the final 1 second on the crowd's stunned faces. No further dialogue.",
    ].join(' '),
  },

  c09_groans: {
    beats: 'Shot 09-1 — the crowd groans, Jan justifies the 50k',
    seconds: 15,
    // ACCEPTED TAKE chains from c08's real last frame, NOT shot09_1_groans.png -- no
    // scene/beat break in the fountain between the merch reveal and the crowd's groan.
    // See fal-tools/api/run_c09_groans.js and .agents/rules/location_continuity_rules.md.
    startImage: `${S}/shot09_1_groans.png`,
    prompt: [
      LOOK, CAST, LANG, FRAMING,
      'ACTION: the clip opens on the groan — heads tipping back, eyes rolling, hands rubbing faces, arms folding, shoulders slumping. Weary rather than angry. Jan faces them entirely untroubled, raising one hand palm-down to quiet them, wearing a small self-satisfied smile, and talks straight over the noise.',
      'DIALOGUE: @Jan (speaking in a smug English Home Counties accent): "Yes groan all you like, but I am the one with the most talent and skills to deliver this. It will add fifty thousand pounds to my salary as I simply add this role into my duties."',
      'AUDIO: a loud collective groan opening the clip, subsiding into resentful muttering under his line.',
      "TIMING: the dialogue ends at about 13 seconds. HOLD the final 2 seconds on Jan's self-satisfied face over the resentful muttering. No further dialogue.",
    ].join(' '),
  },

  c10_get_back_to_work: {
    beats: 'Shot 09-2 — "now GET BACK TO WORK!"',
    seconds: 10,
    // ACCEPTED TAKE chains from c09's real last frame, NOT shot09_2_50k_outburst.png --
    // one unbroken speech in the fountain, split into c09/c10 only for the duration cap.
    // See fal-tools/api/run_c10_get_back_to_work.js and
    // .agents/rules/location_continuity_rules.md.
    startImage: `${S}/shot09_2_50k_outburst.png`,
    prompt: [
      LOOK, CAST, LANG, FRAMING,
      'ACTION: Jan escalates from smug calm into a full bellow — fist raised, face flushing deep red, sweat at his hairline, mouth wide. The crowd recoil and immediately start turning away to their desks, some wincing, some with heads in hands. Camera holds the reference framing throughout.',
      'DIALOGUE: @Jan (speaking then bellowing in an English Home Counties accent): "I will let you know when more information is available, now GET BACK TO WORK!"',
      'AUDIO: his shout, then chairs scraping and footsteps as people disperse fast. Cut to office ambience.',
      'TIMING: the shout lands at about 6 seconds. USE the final 4 seconds for the crowd breaking up and hurrying back to their desks, leaving Jan standing alone in the middle of the floor, chest heaving, as the room empties around him. This is the last shot of the scene, so let it breathe. No further dialogue.',
    ].join(' '),
  },
};
