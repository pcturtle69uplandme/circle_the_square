// Scene 3 location plates -- INT. STAFF RESTAURANT / CANTEEN
// (CTS_Featurette_Episode.fountain L152+). Empty-set plates, no people, generated the
// same way Scene 2's stills are: node run_shot.js <slug> <outDir> with HF_SHOTS set.
//
// Structure follows the lesson from the jan_office_corridor mess (see
// location-refs/higgsfield/_archive-corridor-meetingroom-wrong/WHY_ARCHIVED.txt): the
// MASTER WIDE is text-to-image with no references at all, so nothing can contaminate
// it, and the two derived angles chain off the finished master. Do not generate
// derived angles from the layout text alone -- that is exactly what produced seven
// plates of a room the corridor does not contain.
//
// House style is fixed by Scenes 1-2: The Triangle, Cambridge -- dark red-brown brick
// with black banding, warm walnut, black metal frames. The canteen sits in the
// double-height atrium per LOCATION_PLATE_SHOT_LIST.md L07 ("canteen tables below")
// and L11 ("stainless servery, timber-fronted counter").

const MASTER = 'location-refs/higgsfield/coverage/staff_canteen/staff_canteen_master_wide.png';

// Repeated verbatim in the derived plates so the set cannot drift.
const CANTEEN = 'A staff restaurant and canteen inside a modern UK corporate building in the style of The Triangle, Cambridge. Double-height space. Exposed dark red-brown brick piers with black banding and warm walnut panelling, matching the rest of the building. A long timber-fronted servery counter with a stainless steel top runs along the LEFT side of the room, with a glass sneeze-guard display above it. Seating fills the middle and foreground: pale timber cafe tables with black moulded chairs, a run of high poseur tables with stools, and a few burnt-orange moulded accent chairs. Pale cream tiled floor, exposed dark grey concrete columns, recessed downlights and suspended linear pendants. A full-height glazed window wall runs along the RIGHT side, looking out onto a landscaped courtyard with trees and low-rise modern buildings.';

// The featurette is set in low-rise Cambridge; earlier generations kept defaulting to
// a London skyline, so it has to be excluded explicitly every time.
const NO_CITY = 'The view outside is LOW-RISE: trees, grass, modern low buildings of two or three storeys. Absolutely no skyscrapers, no tall towers, no city skyline, no London landmarks.';

const EMPTY = 'The room is COMPLETELY EMPTY - no people anywhere in frame, no staff, no diners, nobody behind the counter.';

const STYLE = 'Cinematic 35mm architectural interior photography, natural even daylight, well lit, photorealistic, no text, no signage, no captions, no on-screen graphics, no watermark.';

module.exports = {
  staff_canteen_master_wide: {
    beat: 'Canteen anchor plate -- every Scene 3 prompt attaches this',
    refs: [], // text-to-image on purpose; see header
    prompt: [
      'Photoreal architectural interior photograph, 35mm lens, wide establishing shot taking in the whole room: the servery counter on the left, the seating in the middle, and the glazed window wall on the right all visible in one frame.',
      CANTEEN, NO_CITY, EMPTY, STYLE,
    ].join(' '),
  },

  staff_canteen_servery_counter: {
    beat: 'Jan asks Maureen for a pain au chocolat; the empty tray is the story prop',
    refs: [MASTER],
    prompt: [
      'Photoreal architectural interior photograph, 35mm lens. Reproduce the canteen in the reference image EXACTLY - same materials, same counter, same floor, same lighting, same window wall. Camera stands in the seating area looking along the length of the timber-fronted servery counter toward the far end.',
      CANTEEN,
      'DETAIL THIS SHOT MUST SHOW - on the stainless counter top, under the glass sneeze guard, a row of large stainless steel serving trays that are EMPTY except for scattered crumbs and a few paper cake cases, as if the last pastry has just been taken. Beside them a tall stack of white china plates and a second stack of white china bowls, close to the counter edge.',
      NO_CITY, EMPTY, STYLE,
    ].join(' '),
  },

  staff_canteen_window_wall: {
    beat: 'The window Jan hurls a chair through -- must be established before it breaks',
    refs: [MASTER],
    prompt: [
      // Asking for a new angle while also saying "reproduce the reference exactly" just
      // gets the reference back: the first attempt returned the master's camera position
      // with a chair stack added. State the camera MOVE explicitly, and say what must
      // now be OUT of frame -- otherwise the reference is treated as the composition
      // too, not just the materials.
      'Photoreal architectural interior photograph, 35mm lens. Match the MATERIALS and FITTINGS of the reference image exactly - same brick piers with black banding, same walnut panelling, same cream tiled floor, same concrete columns, same black-framed glazing, same furniture. But this is a COMPLETELY DIFFERENT CAMERA POSITION: the camera has turned 90 degrees to the RIGHT compared with the reference. You are standing in the middle of the seating area facing the full-height glazed window wall HEAD-ON, square to the glass, so that the tall glass panes FILL THE FRAME from top to bottom and side to side. The servery counter is now BEHIND the camera and must NOT be visible anywhere in this shot. Do not reproduce the reference image composition.',
      CANTEEN,
      'DETAIL THIS SHOT MUST SHOW - the window wall is a run of tall floor-to-ceiling glass panes in slim black metal frames, each pane clean and completely INTACT and unbroken. Against the brick pier beside the window stands a neat stack of heavy dark grey upholstered meeting-room chairs with black metal frames, the kind wheeled in for large meetings.',
      NO_CITY, EMPTY, STYLE,
    ].join(' '),
  },
};
