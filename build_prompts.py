#!/usr/bin/env python3
"""
Single source of truth for the OUTRUN clip prompts.

    python build_prompts.py

Emits:
    prompts/<CLIP_ID>.txt        30 fully assembled, ready-to-paste Flow prompts
    OUTRUN_SHOT_DIRECTIONS.md    the human-readable per-clip direction sheet

Keeping both outputs in one script means the direction sheet and the prompts can
never disagree with each other.
"""
import os
import textwrap

OUT_PROMPTS = "prompts"
OUT_DOC = "OUTRUN_SHOT_DIRECTIONS.md"

PLATES = {
    "L1": "FLASHBACK2047-OutRun-1.jpg",
    "L2": "FLASHBACK2047-OutRun-2.jpg",
    "L3": "FLASHBACK2047-OutRun-3.jpg",
    "L4": "FLASHBACK2047-OutRun-4.jpg",
    "L5": "FLASHBACK2047-OutRun-5.jpg",
    "L6": "FLASHBACK2047-OutRun-6.jpg",
}

# --------------------------------------------------------------- fixed blocks

BIBLE = (
    "1980s Sega OutRun-inspired anime illustration, cel-shaded painterly key art, thick clean "
    "linework, saturated poster colours, 1986 arcade attract-mode energy. LOCKED CHASE CAMERA: a "
    "fixed low third-person view directly behind the car, camera height at boot level, the car "
    "centred in the lower third of frame and the horizon across the upper third. The camera never "
    "cuts, never orbits, never pans, never changes lens or height, and stays rigidly behind the car "
    "for the entire shot."
)

# Deliberately describes the car's GEOMETRY and never names a real model. Naming one
# invites the model to "correct" the car toward the real thing - and the plate car is
# not a real Testarossa (see OUTRUN_VIDEO_PLAN.md §9). It also keeps brand words out
# of the prompt, which the content filters are happier with.
CAR = (
    "HERO CAR: a red 1980s mid-engined Italian convertible supercar with the roof down, wide and low, "
    "seen square-on from directly behind. Its rear end has TWO round tail lights on each side (four in "
    "total) sitting outboard of a full-width black slatted grille panel, a small silver rearing-horse "
    "emblem centred on that panel, a black lower valance with a recessed rectangular number-plate "
    "panel, FOUR chrome exhaust tips arranged as two close-set pairs, and a rear deck with two black "
    "louvred engine-cover panels either side of a body-colour central spine. Black door mirrors on "
    "short stalks, five-spoke alloy wheels. The car's colour, shape, badges, lights, exhausts, wheels "
    "and proportions do not change for a single frame, and the car holds the exact same position and "
    "the exact same size in frame from the first frame to the last. Two occupants seen from behind: a "
    "male driver in the left seat with short dark brown wavy hair, and a blonde female passenger in "
    "the right seat with long hair streaming in the slipstream. Neither turns toward camera and "
    "neither leaves the car."
)

SPEED = (
    "SPEED: the car is travelling flat out at full motorway speed for the entire eight seconds. The "
    "tarmac, the lane markings and the roadside blur past in continuous hard horizontal streaks and "
    "the dashed centre line strobes past in a fast, steady rhythm. The speed is absolutely constant "
    "from the first frame to the last - the car never slows, never eases off the throttle and never "
    "decelerates towards the end of the shot. The final second is exactly as fast as the first."
)

ROAD = (
    "ROAD AND TRAFFIC: the hero car stays on the tarmac inside its own lane at all times, all four "
    "wheels on the road surface, never on the verge, never airborne, never crossing the guardrail. "
    "The road keeps the identical number of lanes for the whole shot - it never forks, never "
    "branches, never gains a junction, slip road or roundabout, and the surface, markings and "
    "guardrail never change type. AT LEAST THREE other vehicles are visible on the road at all "
    "times: period late-1980s sedans and coupes in the adjacent lanes and receding into the distance "
    "ahead. Other vehicles only ever enter the shot from the far distance ahead or from the left and "
    "right edges of frame, and they only ever leave it the same way - no vehicle ever materialises "
    "out of thin air in open road in the middle of frame, and no vehicle ever vanishes mid-frame. "
    "The FLASHBACK2047 wordmark stays fixed, static and legible in the bottom-left corner."
)

LOOP = (
    "LOOP: the shot begins and ends on the identical framing, the identical lighting and the "
    "identical hero-car position, so that it loops seamlessly and undetectably back to its own first "
    "frame."
)

# Used instead of LOOP when only the START frame is pinned (the chain architecture).
# Pinning the end frame made the model stop the world and teleport traffic into position
# over the last two seconds - see OUTRUN_VIDEO_PLAN.md section 12. This clause is the
# direct counter to that.
CHAIN = (
    "ENDING: this shot is one continuous leg of a much longer journey and it does NOT come to rest. "
    "It ends mid-drive with the car still travelling flat out - do not slow down, do not ease off, do "
    "not settle, do not coast and do not arrive anywhere. The very last frame must be moving exactly "
    "as fast as the very first, with the road still tearing past, and the shot should feel as though "
    "it was cut arbitrarily out of the middle of an hours-long drive. Traffic must keep moving "
    "naturally right through the final frame - no vehicle freezes, snaps into position, hovers above "
    "the road surface or slides sideways into place at the end."
)

NEG = (
    "NEGATIVE: no camera cuts, no scene changes, no change of time of day, no change of weather. No "
    "text, captions, subtitles, UI, HUD, logos or watermarks other than the existing bottom-left "
    "wordmark. No change to the car's colour, model or position in frame. No empty road. No "
    "pedestrians or characters outside vehicles. No crashes, no spin-outs, no skids. No car exiting "
    "frame. No zoom, no reframe, no slow motion, no speed ramp. No morphing of the hero car or its "
    "occupants. No spoken dialogue and no music."
)

ANCHORS = {
    "L1": ("Mediterranean Riviera at midday under towering white cumulus; a pale stone retaining wall "
           "and an arched tunnel mouth on the right, a hillside town of white villas rising above, "
           "deep blue sea to the left with white sailboats and a white motor yacht."),
    "L2": ("Big Sur / Pacific Coast Highway in the afternoon; raw tan cliffs on the right, white surf "
           "exploding over black rocks on the left, the highway S-bending away to the right into "
           "coastal haze."),
    "L3": ("Golden hour, the low sun sitting on the water to the left throwing a molten path across "
           "the sea; an ochre Riviera villa and stone arch on the right, palm silhouettes, long "
           "shadow bars striping the tarmac; warm amber grade."),
    "L4": ("Night; a full moon high on the left laying a glitter path on a dark sea, a skyline of lit "
           "city towers ahead on the right, sodium streetlamps, wet reflective asphalt streaked with "
           "light; deep blue palette, red tail lights ahead."),
    "L5": ("Santa Monica Ocean Avenue at midday; a colonnade of tall palms on both sides, white "
           "apartment towers on the right, a green highway sign reading OCEAN AVE 300 FT, brilliant "
           "cumulus over a turquoise Pacific."),
    "L6": ("Full sunset, the sun resting on the horizon to the left over the sea; an avenue of black "
           "palm silhouettes converging on a dead-centre vanishing point, condo towers on the right; "
           "near-monochrome burnt-orange grade."),
}

# Water direction. Waves are the one element that physically cannot hold still for a
# loop, so each sea is given an explicit one-cycle instruction: it must be back where
# it started by second 8.
SEA = {
    "L1": ("SEA: the bay is alive but calm - long slow swells crawl across the deep blue water, "
           "sunlight glitters and shifts on the surface, and the sailboats and the moored motor "
           "yacht rock gently. The water completes exactly one slow swell cycle across the eight "
           "seconds and returns to its opening state."),
    "L2": ("SEA: the surf is the second star of this shot. Big Pacific swells roll in from the left, "
           "rear up green-blue and detonate against the black rocks in exploding walls of white "
           "spray that hang in the air and fall back as foam, while the previous wave's foam drains "
           "and sucks back off the rocks. Exactly ONE complete wave cycle happens across the eight "
           "seconds - a swell rises, breaks, explodes, drains away, and a new identical swell has "
           "risen to precisely the same position and shape by the final frame, so the water loops as "
           "cleanly as the road does. The spray never reaches the carriageway and never touches the "
           "hero car."),
    "L3": ("SEA: the low sun's molten path on the water shimmers and breaks up continuously, small "
           "swells catching gold along their crests, the distant sailboats rocking. The shimmer "
           "completes one cycle and returns to its opening pattern."),
    "L4": ("SEA: the moon's glitter path on the black water ripples and re-forms continuously, the "
           "dark swells catching thin silver highlights. The ripple completes one cycle and returns "
           "to its opening pattern."),
    "L5": ("SEA: the turquoise Pacific runs with lines of small white breakers peeling along the "
           "beach, sunlight flashing on the chop. The breakers complete one cycle and return to "
           "their opening state."),
    "L6": ("SEA: the sun's orange road on the water flickers and re-forms, low swells catching fire "
           "along their crests. The shimmer completes one cycle and returns to its opening pattern."),
}

# --------------------------------------------------------------- the 30 clips
# beats = the four two-second phases: 0-2s, 2-4s, 4-6s, 6-8s

HERO = [
    # ---- L5 Ocean Ave noon -------------------------------------------------
    ("L5-A", "L5", "Cruise", "Opening statement of the whole film.",
     ["Dead-centre lane, flat out. The palm colonnade rips past on both sides, trunk after trunk "
      "strobing through frame.",
      "The white coupe in the right-hand lane is reeled in and drawn level, then falls back past the "
      "right edge of frame.",
      "The OCEAN AVE 300 FT sign sweeps in from the right edge and out of frame overhead; the red "
      "coupe and grey sedan hold station in the distance ahead.",
      "A fresh pair of cars has risen out of the far distance into exactly the positions the first "
      "pair held at second zero; palm spacing returns to the opening frame."],
     "Right lane: white coupe overtaken. Ahead: red coupe + grey sedan held at distance."),

    ("L5-C", "L5", "Curve", "Ocean Ave bends with the shoreline.",
     ["Flat out, centre lane, palms strobing.",
      "The highway begins a long lazy left-hand bend following the beach; the car leans into it, the "
      "palm colonnade swinging across frame.",
      "The bend reaches its deepest point - the guardrail and the beach sweep across the left of "
      "frame - then the road begins to straighten.",
      "The road is dead straight again and the car is back to precise dead centre, identical to the "
      "opening frame."],
     "Two cars ahead track through the bend; one grey sedan holds the right lane throughout."),

    ("L5-F", "L5", "Pack", "Traffic thickens - the OutRun dodge.",
     ["Centre lane, flat out, three cars visible ahead.",
      "Traffic builds: five vehicles now spread across the lanes ahead and alongside, closing up.",
      "The hero car threads the gap between a grey sedan on the left and a white coupe on the right, "
      "both sliding past and out of frame.",
      "The road ahead opens clear again and the traffic pattern has re-formed to exactly the opening "
      "arrangement."],
     "Peak of five vehicles at 3-5s, resolving back to three by 8s."),

    ("L5-B", "L5", "Overtake", "Pass on Ocean Avenue.",
     ["Centre lane, flat out, a white coupe ahead in the right-hand lane closing steadily.",
      "The hero car swings one lane right and draws level with the white coupe, wheel to wheel, "
      "palms strobing past above both of them.",
      "It clears the coupe cleanly and the coupe slides back and out of the bottom-right of frame.",
      "The hero car settles back into the centre lane at unchanged speed with clear road ahead and "
      "fresh traffic rising out of the distance."],
     "White coupe overtaken on the right; red coupe and grey sedan hold the far distance."),

    ("L5-D", "L5", "Surge", "Throttle down the palm colonnade.",
     ["Centre lane at speed, the palm colonnade rushing past on both sides.",
      "A burst of throttle - the quad exhausts flare hard, the motion streaks stretch out and the "
      "traffic ahead is hauled in fast.",
      "The surge holds at full pace; the guardrail and the beach on the left tear past in solid "
      "horizontal bands.",
      "The rush eases to a fast steady cruise - still flat out, never slowing - with new traffic "
      "ahead."],
     "Blur intensity rises then relaxes; the car never changes position in frame."),

    ("L5-E", "L5", "Crest", "The boulevard lifts and dips.",
     ["Flat out down Ocean Avenue, the sea flat and bright on the left.",
      "The road crests a gentle rise and the traffic ahead drops briefly below the horizon line.",
      "Over the top - the road dips away and the hidden cars spring back into view exactly where the "
      "geometry says they should be, no closer and no further.",
      "The road levels out and the horizon settles back, the car still travelling flat out."],
     "CAUTION: crest shots are the highest pop-in risk. QA this one hard."),

    # ---- L1 Riviera noon ---------------------------------------------------
    ("L1-A", "L1", "Cruise", "Arrival on the Riviera.",
     ["Centre lane, flat out along the corniche, the stone retaining wall ripping past on the right.",
      "The yellow coupe ahead is reeled in; below-left the bay opens out with sailboats and the white "
      "motor yacht cutting a wake.",
      "The arched tunnel mouth in the retaining wall sweeps past close on the right; the black "
      "convertible holds the right-hand lane.",
      "A second arch and a second yellow coupe have arrived in exactly the opening positions."],
     "Yellow coupe centre, dark sedan mid-distance, black convertible right lane."),

    ("L1-B", "L1", "Overtake", "The pass, and back home.",
     ["Centre lane, flat out, yellow coupe ahead closing.",
      "The hero car swings one lane right and pulls alongside the yellow coupe, wheel-to-wheel.",
      "It clears the coupe cleanly, which slides back and out of the bottom-right of frame.",
      "The hero car eases back into the centre lane and settles into precisely its opening position, "
      "dead centre."],
     "The overtake must complete and return - the car MUST be back dead centre by 8s."),

    ("L1-D", "L1", "Surge", "Throttle.",
     ["Centre lane at speed, the hill town of white villas stacked above on the right.",
      "A burst of throttle - the quad exhausts flare, the motion streaks stretch and intensify, the "
      "traffic ahead is hauled in fast.",
      "The surge holds; the guardrail and the sea below-left tear past in hard horizontal bands.",
      "The rush settles back to exactly the opening cruise speed with the traffic restored to its "
      "opening distances."],
     "NOTE: the surge is an intensification of blur, not a change of car position or camera."),

    # ---- L2 Big Sur --------------------------------------------------------
    ("L2-A", "L2", "Cruise", "Big Sur established.",
     ["Centre lane, flat out, tan cliffs towering on the right.",
      "Below-left a swell rears and detonates white against the black rocks.",
      "The red coupe and silver sedan ahead are gradually reeled in as the spray falls back.",
      "A new swell has risen to the identical shape and position as the opening frame."],
     "Red coupe + silver sedan ahead, dark sedan right lane."),

    ("L2-B", "L2", "Overtake", "Pass on the coast road.",
     ["Centre lane, flat out, silver sedan ahead closing.",
      "The hero car moves one lane right and draws level with the silver sedan.",
      "It clears the sedan, which falls back out of frame right; surf explodes below-left.",
      "Back into the centre lane and settled to exactly the opening position."],
     "Overtake completes and returns to dead centre by 8s."),

    ("L2-C", "L2", "Curve", "The S-bend.",
     ["Flat out into the approach of the right-hand bend.",
      "The highway sweeps hard right around the cliff face; the car leans in, the cliff wall filling "
      "the right of frame.",
      "The bend unwinds into the reverse left-hander, the ocean swinging back into view on the left.",
      "The road straightens and the car returns to dead centre, identical to the first frame."],
     "This is the plate's own S-bend animated - the most characteristic L2 shot."),

    ("L2-D", "L2", "Surge", "Full throttle on the PCH.",
     ["Centre lane at speed above the surf.",
      "Throttle - exhausts flare, blur streaks stretch out hard, the cars ahead are hauled in.",
      "Peak speed; the guardrail on the left is a solid horizontal band.",
      "Settles back to the opening speed and the opening traffic spacing."],
     "Blur intensity changes; car position does not."),

    ("L2-E", "L2", "Crest", "Rise and dip.",
     ["Flat out, the road running level above the rocks.",
      "The highway crests a rise - the traffic ahead drops briefly out of sight below the horizon "
      "line.",
      "The car comes over the top and the road dips away, the hidden traffic springing back into "
      "view ahead exactly where it should be.",
      "The road levels out and the horizon returns to the opening height."],
     "CAUTION: highest pop-in risk clip. Traffic must re-appear where geometry says it should, not "
     "somewhere new. QA this one hard."),

    ("L2-F", "L2", "Pack", "Traffic dense above the surf.",
     ["Centre lane, three cars ahead.",
      "Traffic builds to five across the lanes as a big swell rears below-left.",
      "The hero car threads between two sedans as the wave detonates; spray hangs white in the air.",
      "The road clears back to the opening three-car arrangement and the sea returns to its opening "
      "state."],
     "Peak five vehicles; resolves to three."),

    # ---- L3 Golden hour ----------------------------------------------------
    ("L3-A", "L3", "Cruise", "Golden hour established.",
     ["Centre lane, flat out, the low sun blazing off the water to the left.",
      "Long shadow bars from the roadside palms strobe across the bonnet and the tarmac in a steady "
      "rhythm.",
      "The red coupe ahead is reeled in; the ochre villa and stone arch sweep past on the right.",
      "The shadow rhythm and the traffic have returned to exactly the opening arrangement."],
     "Shadow bars are the signature of this look - keep them strobing steadily."),

    ("L3-C", "L3", "Curve", "The corniche bends into the sun.",
     ["Flat out, amber light, shadow bars strobing.",
      "The road curves left towards the sun; the glare swells across the left of frame.",
      "The bend deepens, the sea and its molten path swinging across frame, then begins to unwind.",
      "Straight again, dead centre, the glare back to its opening intensity."],
     "Glare must not bloom out the frame - it swells and recedes."),

    ("L3-D", "L3", "Surge", "Chasing the light.",
     ["Centre lane in amber light.",
      "Throttle - exhausts flare hot against the warm grade, the shadow bars strobe faster.",
      "Peak speed, the sun's path on the water tearing past on the left.",
      "Settles back to the opening speed and shadow rhythm."],
     "Shadow bar strobe rate rises then falls back - a good visible speed cue."),

    # ---- L6 Sunset ---------------------------------------------------------
    ("L6-A", "L6", "Cruise", "Sunset established.",
     ["Centre lane, flat out, the palm avenue converging on the dead-centre vanishing point.",
      "Palm silhouettes rip past on both sides in a fast steady rhythm; the sun sits on the horizon "
      "to the left.",
      "The three sedans in the right-hand lanes are gradually drawn in.",
      "Palm spacing and traffic have returned to the exact opening frame."],
     "The vanishing point must stay dead centre - it is the whole composition."),

    ("L6-B", "L6", "Overtake", "Pass into the sunset.",
     ["Centre lane, dark sedan ahead closing.",
      "One lane right, drawing level with the sedan, palm silhouettes flashing past.",
      "Clear of it; the sedan drops back out of frame right.",
      "Back to the centre lane and the exact opening position, vanishing point dead centre."],
     "Overtake completes and returns."),

    ("L6-E", "L6", "Crest", "The road rises to the sun.",
     ["Flat out down the palm avenue.",
      "The road crests gently; the cars ahead dip briefly below the horizon.",
      "Over the top - the traffic springs back into view against the orange sky.",
      "The road levels and the horizon returns to the opening height."],
     "Pop-in risk clip - QA hard."),

    # ---- L4 Night ----------------------------------------------------------
    ("L4-A", "L4", "Cruise", "Night established. Opening of the Last Wave section.",
     ["Centre lane, flat out, the moon high on the left over black water.",
      "Wet asphalt streaks past dragging long reflected highlights; streetlamps strobe overhead.",
      "The city towers ahead-right grow slowly closer, their lit windows glittering; two sets of red "
      "tail lights hold station ahead.",
      "The lamp rhythm and tail lights have returned to the opening arrangement."],
     "Reflections on wet tarmac are the signature - keep them streaking."),

    ("L4-B", "L4", "Overtake", "Night pass.",
     ["Centre lane, red tail lights ahead closing.",
      "One lane right, drawing level with the dark sedan, its interior lit by dash glow.",
      "Clear of it; it falls back out of frame right, tail lights smearing on the wet road.",
      "Back to centre lane, exact opening position."],
     "Overtake completes and returns."),

    ("L4-C", "L4", "Curve", "The bay road bends.",
     ["Flat out along the wet coast road.",
      "A long left-hand bend follows the bay; the moon's glitter path swings across frame.",
      "The bend deepens, the city skyline sliding right across frame, then unwinds.",
      "Straight again, dead centre, moon back to its opening position."],
     "The moon must stay top-left - it anchors the frame."),

    ("L4-D", "L4", "Surge", "Night throttle.",
     ["Centre lane at speed on wet tarmac.",
      "Throttle - the exhausts flare bright in the dark, reflections stretch into long light streaks.",
      "Peak speed; the streetlamps strobe fast overhead.",
      "Settles back to the opening speed and lamp rhythm."],
     "Exhaust flare reads strongest at night - the clearest speed cue of the six looks."),

    ("L4-E", "L4", "Crest", "Rise into the city lights.",
     ["Flat out, city towers glittering ahead-right.",
      "The road crests; the tail lights ahead dip briefly out of sight.",
      "Over the top - the traffic and the full skyline spring back into view.",
      "The road levels; horizon back to the opening height."],
     "Pop-in risk clip - QA hard."),

    ("L4-F", "L4", "Pack", "Night traffic.",
     ["Centre lane, two sets of tail lights ahead.",
      "Traffic builds - five vehicles now, a constellation of red tail lights across the lanes.",
      "The hero car threads between two of them, their reflections sliding across the wet road.",
      "The road clears back to the opening two-car arrangement."],
     "Closing texture of the film - the densest night shot."),
]

TRANSITIONS = [
    ("T5-1", "L5", "L1", "Santa Monica noon into Riviera noon",
     ["Flat out down the Ocean Avenue palm colonnade, turquoise Pacific to the left.",
      "The palm colonnade thins and the roadside begins to rise; the flat beach gives way to the "
      "first stone parapet.",
      "A pale stone retaining wall builds up along the right and the coastline below-left deepens to "
      "Mediterranean blue; white villas start stacking on the hillside above.",
      "Fully arrived on the Riviera corniche - stone wall and arched tunnel mouth on the right, "
      "sailboats and the white motor yacht on the bay below-left."]),

    ("T1-2", "L1", "L2", "Riviera cliffs opening out into Big Sur",
     ["Flat out along the Riviera corniche, retaining wall right, calm blue bay left.",
      "The villas thin out and fall away behind; the cliff face on the right turns rawer and more "
      "vertical.",
      "The manicured coast becomes wild - the stone wall gives way to bare tan rock and the calm bay "
      "roughens into open Pacific swell.",
      "Fully arrived on Big Sur - raw tan cliffs right, white surf exploding over black rocks left, "
      "the highway S-bending away ahead."]),

    ("T2-3", "L2", "L3", "Afternoon warming down into golden hour",
     ["Flat out on the Big Sur coast road, hard afternoon light, surf detonating below-left.",
      "The sun begins to drop toward the water on the left and the whole frame warms; shadows start "
      "to lengthen across the tarmac.",
      "Deep amber floods the scene; the raw cliffs soften into an ochre Riviera hillside and the "
      "first long palm shadow bars stripe the road.",
      "Fully arrived at golden hour - low sun on the water left, ochre villa and stone arch right, "
      "shadow bars striping the tarmac."]),

    ("T3-6", "L3", "L6", "Golden hour deepening into full sunset",
     ["Flat out in warm amber light, shadow bars strobing, the sun low on the water left.",
      "The sun sinks further; the sky saturates from gold toward deep orange and the shadows stretch "
      "to their limit.",
      "The roadside detail burns down into pure silhouette; the palms turn black against a blazing "
      "orange sky and the avenue lines up on a central vanishing point.",
      "Fully arrived at sunset - the sun resting on the horizon left, an avenue of black palm "
      "silhouettes converging dead centre, condo towers right."]),

    ("T6-4", "L6", "L4", "Sunset burning out into night",
     ["Flat out down the sunset palm avenue, sun on the horizon left.",
      "The sun slips below the water; the orange drains out of the sky from the top down and the "
      "first street lamps flicker on.",
      "Deep blue floods in from above, the city tower windows light up one bank at a time, and the "
      "tarmac darkens and turns wet and reflective.",
      "Fully arrived at night - full moon high left with its glitter path on black water, lit city "
      "towers ahead-right, wet asphalt streaked with light."]),

    ("T4-5", "L4", "L5", "Night lifting back to noon (end wrap - optional)",
     ["Flat out on the wet night coast road, moon high left, city towers glittering.",
      "The sky lightens at the horizon; the moon fades and the street lamps switch off one by one.",
      "Daylight floods in, the asphalt dries out and the city towers resolve into white apartment "
      "blocks; palms green up along both sides.",
      "Fully arrived back at Santa Monica noon - palm colonnade both sides, OCEAN AVE 300 FT sign "
      "right, brilliant cumulus over a turquoise Pacific."]),
]


def assemble_hero(cid, look, beats, chain=False):
    body = " ".join(f"SECONDS {i * 2}-{i * 2 + 2}: {b}" for i, b in enumerate(beats))
    tail = CHAIN if chain else LOOP
    return "\n\n".join([BIBLE, CAR, ANCHORS[look], body, SPEED, SEA[look], ROAD, tail, NEG])


def assemble_transition(cid, a, b, beats):
    body = " ".join(f"SECONDS {i * 2}-{i * 2 + 2}: {t}" for i, t in enumerate(beats))
    trans = (
        "TRANSITION: this is one unbroken eight-second take that travels continuously from the "
        "opening location and light into the closing location and light. The change is gradual and "
        "never cuts, never dissolves and never jumps - the world transforms around the car while the "
        "camera and the car hold exactly the same position in frame throughout."
    )
    seas = SEA[a] if SEA[a] == SEA[b] else (
        "SEA: the water stays continuously alive and in motion throughout, transforming with the "
        "light rather than cutting between states."
    )
    return "\n\n".join([BIBLE, CAR, body, trans, SPEED, seas, ROAD, NEG])


def main():
    os.makedirs(OUT_PROMPTS, exist_ok=True)
    doc = ["# OUTRUN — per-clip direction sheet",
           "",
           "Auto-generated by `build_prompts.py` — **edit that script, not this file.**",
           "Ready-to-paste prompts live in `prompts/<CLIP-ID>.txt`.",
           "",
           "Every hero clip is generated in Flow with **Frames to Video**, "
           "**start frame = end frame = its own plate**. Transitions use "
           "**start frame = plate A, end frame = plate B**.",
           "",
           "---",
           ""]

    doc += ["## Hero loops (24)", ""]
    os.makedirs(os.path.join(OUT_PROMPTS, "chain"), exist_ok=True)
    for cid, look, beat, note, beats, traffic in HERO:
        path = os.path.join(OUT_PROMPTS, f"{cid}.txt")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(assemble_hero(cid, look, beats))
        with open(os.path.join(OUT_PROMPTS, "chain", f"{cid}.txt"), "w", encoding="utf-8") as fh:
            fh.write(assemble_hero(cid, look, beats, chain=True))
        doc += [f"### `{cid}` — {look} · {beat}", "",
                f"*{note}*", "",
                f"**Plate (both ends):** `{PLATES[look]}`", "",
                "| t | direction |", "|---|---|"]
        for i, b in enumerate(beats):
            doc.append(f"| {i * 2}–{i * 2 + 2}s | {b} |")
        doc += ["", f"**Traffic:** {traffic}", "",
                f"**Prompt:** `prompts/{cid}.txt`", "", "---", ""]

    doc += ["## Transitions (6)", ""]
    for cid, a, b, title, beats in TRANSITIONS:
        path = os.path.join(OUT_PROMPTS, f"{cid}.txt")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(assemble_transition(cid, a, b, beats))
        doc += [f"### `{cid}` — {title}", "",
                f"**Start frame:** `{PLATES[a]}`  →  **End frame:** `{PLATES[b]}`", "",
                "| t | direction |", "|---|---|"]
        for i, bt in enumerate(beats):
            doc.append(f"| {i * 2}–{i * 2 + 2}s | {bt} |")
        doc += ["", f"**Prompt:** `prompts/{cid}.txt`", "", "---", ""]

    with open(OUT_DOC, "w", encoding="utf-8") as fh:
        fh.write("\n".join(doc))

    n = len(HERO) + len(TRANSITIONS)
    print(f"wrote {n} prompts to {OUT_PROMPTS}/ and the direction sheet to {OUT_DOC}")


if __name__ == "__main__":
    main()
