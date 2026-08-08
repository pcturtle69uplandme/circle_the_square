"""
Circle the Square — MASTER VIDEO GENERATOR
Gate-Based Sequential Shot Production for "Project Inception" Featurette

Generates shots S01 through S19 one at a time.
Pauses after each clip for your review and approval before continuing.

USAGE:
  python generate_all_shots.py

  Or start from a specific shot:
  python generate_all_shots.py --start S05

FIRST TIME SETUP:
  1. Go to: https://aistudio.google.com/apikey
  2. Create a key with Veo 2 access enabled
  3. Paste it into API_KEY below
"""

import os
import sys
import time
import urllib.request
import argparse
from google import genai
from google.genai import types

# ============================================================
# PASTE YOUR VEO-2-ENABLED API KEY FROM AI STUDIO HERE:
API_KEY = "PASTE_YOUR_AI_STUDIO_API_KEY_HERE"
# ============================================================

OUTPUT_DIR = r"C:\ai\Circle the Square\clips"
CHAR_DIR = r"C:\ai\Circle the Square\character-refs"
BUILD_DIR = r"C:\ai\Circle the Square\building-reference\use-images"

STYLE_ANCHOR = (
    "Photoreal cinematic 35mm footage. Modern UK corporate office building interior. "
    "Warm cream/sand brick and pale concrete architecture. Fair-faced grey concrete columns. "
    "Full-height glazing with natural Northern European daylight. Oak/timber slat joinery accents. "
    "Grey carpet tile floors. No lens flare. No visible real-world branding or crests. "
    "Documentary-style handheld camera. British corporate mockumentary tone. "
    "Shallow depth of field on close-ups, deep focus on wide shots. 2.39:1 aspect ratio."
)

# ============================================================
# SHOT DEFINITIONS
# Each shot: id, filename, duration, prompt, images, gate_checks
# ============================================================

SHOTS = [
    {
        "id": "S01",
        "name": "Jan's Office — Establishing Wide",
        "duration": 6,
        "output": "S01_office_establishing.mp4",
        "images": [
            os.path.join(BUILD_DIR, "IMG_20260804_131855397.jpg"),
            os.path.join(CHAR_DIR, "jan_peach_identity_sheet.jpg"),
        ],
        "prompt": (
            "A locked-off wide shot of a modern UK corporate glass-walled office. "
            "A 52-year-old overweight male CEO in a dark navy suit sits behind a desk "
            "with a smug thin-lipped expression, fingers steepled. Opposite him stands "
            "a 38-year-old female executive in a charcoal blazer and cream blouse, "
            "posture upright and composed, holding a tablet. They are mid-conversation. "
            "The background features a faceted ochre-orange reception desk and a "
            "striking black-and-white geometric triangle pattern wall. "
            "Warm office interior lighting. Static wide shot, 6 seconds."
        ),
        "continuity": "Jan: Shirt BUTTONED. Christina: Charcoal blazer.",
        "gate": [
            "Orange faceted desk & triangle wall visible in background",
            "Jan reads as 50s, overweight CEO-type in navy suit",
            "Christina reads as professional, poised female executive",
            "Warm indoor lighting — not cold or sterile",
        ],
    },
    {
        "id": "S02",
        "name": "Jan's Office — MCU Jan Pompous",
        "duration": 8,
        "output": "S02_jan_pompous_mcu.mp4",
        "images": [
            os.path.join(BUILD_DIR, "IMG_20260804_131855397.jpg"),
            os.path.join(CHAR_DIR, "jan_peach_identity_sheet.jpg"),
        ],
        "prompt": (
            "A medium close-up shot on a 52-year-old overweight male CEO in a dark navy "
            "suit sitting at his desk. He speaks with exaggerated self-importance — chin "
            "raised, brows half-raised, fingers steepled then gesturing. His expression "
            "is smug and convinced of his own brilliance. He references his MBA without "
            "any irony. Shallow depth of field, blurred office background with orange "
            "desk visible. Slight push-in as he speaks. 8 seconds."
        ),
        "continuity": "Jan: Shirt BUTTONED, no sweat yet, smug not red.",
        "gate": [
            "Jan's face matches character sheet (age, weight, hair)",
            "Shirt clearly BUTTONED — continuity check",
            "Pompous, not yet stressed — wrong if he looks angry here",
        ],
    },
    {
        "id": "S03",
        "name": "Jan's Office — OTS Christina Deadpan",
        "duration": 6,
        "output": "S03_christina_deadpan_ots.mp4",
        "images": [
            os.path.join(BUILD_DIR, "IMG_20260804_131855397.jpg"),
            os.path.join(CHAR_DIR, "christina_dross_identity_sheet.jpg"),
        ],
        "prompt": (
            "An over-the-shoulder shot from behind a 52-year-old male CEO looking toward "
            "a 38-year-old female executive in a charcoal blazer. She responds to something "
            "with a completely flat, unimpressed deadpan expression — a slight head tilt is "
            "her only reaction. Her voice is measured and professionally savage. She holds a "
            "tablet at her side. Shallow depth of field. 6 seconds."
        ),
        "continuity": "Christina: Charcoal blazer, composed, no emotional tell.",
        "gate": [
            "Christina reads as deadpan — NOT smiling, NOT angry",
            "Two-shot depth feels natural — Jan's shoulder visible",
        ],
    },
    {
        "id": "S04",
        "name": "Jan's Office — CU Jan Stress Build",
        "duration": 5,
        "output": "S04_jan_stress_build_cu.mp4",
        "images": [
            os.path.join(BUILD_DIR, "IMG_20260804_131855397.jpg"),
            os.path.join(CHAR_DIR, "jan_peach_identity_sheet.jpg"),
        ],
        "prompt": (
            "A tight close-up on the face of a 52-year-old overweight male CEO. His face "
            "is beginning to flush red at the cheeks and neck. He loosens his shirt collar "
            "with one finger. A thin film of sweat is starting to appear on his forehead. "
            "He is speaking through increasingly gritted teeth, trying to maintain authority "
            "but visibly losing it. Very shallow depth of field. 5 seconds."
        ),
        "continuity": "Jan: Shirt UNBUTTONING BEGINS — collar open, tie loosened. Face 30% red.",
        "gate": [
            "Clear visible transition from smug to stressed in face colour",
            "Shirt collar open/loosening — continuity bridge to S05",
        ],
    },
    {
        "id": "S05",
        "name": "Jan's Office — Shirtless Arrow Reveal + Sharon Enters",
        "duration": 8,
        "output": "S05_shirtless_arrow_sharon.mp4",
        "images": [
            os.path.join(BUILD_DIR, "IMG_20260804_131855397.jpg"),
            os.path.join(CHAR_DIR, "jan_peach_identity_sheet.jpg"),
            os.path.join(CHAR_DIR, "sharon_enfield_identity_sheet.jpg"),
        ],
        "prompt": (
            "A wide shot in a modern corporate glass-walled office. A flustered, sweating "
            "52-year-old overweight male CEO has just removed his white dress shirt. His "
            "chest and stomach hair has been carefully shaved and styled into a large "
            "downward-pointing arrow toward his waistband. At that exact moment the glass "
            "office door opens and a 34-year-old curvy woman in a fitted emerald jewel-tone "
            "blouse enters the room without knocking. She looks at him. Her eyes travel "
            "briefly downward to the arrow. Her expression remains completely neutral and "
            "unbothered. The CEO freezes in horror and immediately begins scrambling to "
            "close the window blinds. 8 seconds."
        ),
        "continuity": "Jan: Shirt FULLY OFF. Sharon: State A (composed) — emerald blouse, hair tidy.",
        "gate": [
            "Manscaped arrow is clearly visible and reads as intentional comedy",
            "Sharon's expression is NEUTRAL — NOT shocked, NOT laughing",
            "This is the comedy peak of Scene 1 — must land visually",
        ],
    },
    {
        "id": "S06",
        "name": "Jan's Office — Sharon Unbothered MCU",
        "duration": 4,
        "output": "S06_sharon_unbothered_mcu.mp4",
        "images": [
            os.path.join(BUILD_DIR, "IMG_20260804_131855397.jpg"),
            os.path.join(CHAR_DIR, "sharon_enfield_identity_sheet.jpg"),
        ],
        "prompt": (
            "A medium close-up on a 34-year-old curvy woman in a fitted emerald jewel-tone "
            "blouse. She glances briefly downward off-frame, then back up to face-level. "
            "Her expression does not change — completely flat, transactional, unbothered. "
            "She begins speaking matter-of-factly as if nothing unusual has happened. "
            "4 seconds."
        ),
        "continuity": "Sharon: State A (composed, emerald blouse buttoned, hair tidy).",
        "gate": [
            "Sharon reads as genuinely, comically unbothered — not nervous",
            "Emerald blouse reads as composed/professional",
        ],
    },
    {
        "id": "S07",
        "name": "Jan's Office — Jan Locks Blinds MCU",
        "duration": 5,
        "output": "S07_jan_locks_blinds.mp4",
        "images": [
            os.path.join(BUILD_DIR, "IMG_20260804_131855397.jpg"),
            os.path.join(CHAR_DIR, "jan_peach_identity_sheet.jpg"),
        ],
        "prompt": (
            "A medium close-up of a shirtless, sweating, deeply red-faced 52-year-old "
            "overweight man at a glass office window. He yanks down venetian blinds with "
            "both hands with panicked urgency. He then turns sharply and reaches to the "
            "door handle and clicks a lock. His breathing is heavy and audible. His "
            "expression is somewhere between mortified and resigned. 5 seconds."
        ),
        "continuity": "Jan: Shirt still OFF, deeply flushed, sweaty.",
        "gate": [
            "Blinds close action reads clearly",
            "Jan is visibly shirtless — continuity from S05",
        ],
    },
    {
        "id": "S08",
        "name": "Corridor — Tracking Wide Sharon Exits Dishevelled",
        "duration": 8,
        "output": "S08_sharon_exits_dishevelled.mp4",
        "images": [
            os.path.join(BUILD_DIR, "P20.jpg"),
            os.path.join(CHAR_DIR, "sharon_enfield_identity_sheet.jpg"),
        ],
        "prompt": (
            "A wide tracking shot down a modern open-plan corporate office corridor. "
            "A 34-year-old woman in a fitted emerald jewel-tone blouse walks past camera "
            "— her hair is visibly mussed, lipstick slightly smudged, blouse untucked "
            "at one side. She carries her heels in one hand and walks with complete "
            "unhurried confidence. Two male office workers lean against a nearby desk "
            "watching her pass — a lean 32-year-old in a light blue shirt with a deadpan "
            "smirk, and a stocky 40-year-old in a grey polo shirt with arms crossed and "
            "a flat expression. 8 seconds."
        ),
        "continuity": "Sharon: State B — hair mussed, blouse untucked, heels in hand. Chris & Rick first appearance together.",
        "gate": [
            "Sharon's dishevelment reads clearly — this is the visual joke",
            "Her expression is UNBOTHERED — critical comedy beat",
            "Chris & Rick visible in background watching",
        ],
    },
    {
        "id": "S09",
        "name": "Corridor — 2-Shot Chris & Rick Dry Exchange",
        "duration": 6,
        "output": "S09_chris_rick_2shot.mp4",
        "images": [
            os.path.join(BUILD_DIR, "P12.jpg"),
            os.path.join(CHAR_DIR, "chris_identity_sheet.jpg"),
        ],
        "prompt": (
            "A medium two-shot of two male office workers leaning against a desk in a "
            "modern open-plan office with white desk rows and hanging geometric triangle "
            "acoustic felt ceiling panels. A lean 32-year-old in a light blue shirt with "
            "sleeves rolled up delivers a dry, deadpan comment to camera with a barely "
            "suppressed smirk. A stocky 40-year-old in a grey polo shirt with arms "
            "crossed responds flatly, completely unsurprised. They both look off-frame "
            "where Sharon just walked. 6 seconds."
        ),
        "continuity": "Chris: Light blue shirt, sleeves rolled. Rick: Grey polo, arms crossed.",
        "gate": [
            "Chris and Rick are visually distinct — different builds, colours",
            "Office background has hanging triangle baffles visible",
            "Neither looks shocked — they've seen this before",
        ],
    },
    {
        "id": "S10",
        "name": "Open-Plan — High Wide Jan Announces Project Inception",
        "duration": 8,
        "output": "S10_jan_inception_wide.mp4",
        "images": [
            os.path.join(BUILD_DIR, "P12.jpg"),
            os.path.join(CHAR_DIR, "jan_peach_identity_sheet.jpg"),
            os.path.join(CHAR_DIR, "rick_identity_sheet.jpg"),
        ],
        "prompt": (
            "A high-angle wide shot of a modern open-plan corporate office floor. A "
            "52-year-old overweight CEO in a dark navy suit (shirt re-buttoned visibly "
            "askew, collar crooked, still sweating) enters from one side and claps his "
            "hands loudly and repeatedly to summon the surrounding office workers. Workers "
            "at desks stop typing and reluctantly turn in their chairs or stand and drift "
            "toward him. The CEO plants himself in the central aisle between two desk rows "
            "with his hands on his hips, chest puffed out. Geometric triangle felt acoustic "
            "baffles hang from the ceiling above. 8 seconds."
        ),
        "continuity": "Jan: Shirt RE-BUTTONED ASKEW — visible continuity from S07. Still sweaty.",
        "gate": [
            "Shirt mis-buttoning is visible — key comedy continuity detail",
            "Office crowd gathering reads as reluctant/unenthusiastic",
            "Triangle ceiling baffles visible",
        ],
    },
    {
        "id": "S11",
        "name": "Open-Plan — MCU Jan £50k Pay Rise Announcement",
        "duration": 8,
        "output": "S11_jan_50k_mcu.mp4",
        "images": [
            os.path.join(BUILD_DIR, "P12.jpg"),
            os.path.join(CHAR_DIR, "jan_peach_identity_sheet.jpg"),
        ],
        "prompt": (
            "A medium close-up with a slight push-in on a 52-year-old overweight CEO "
            "in a mis-buttoned dark navy suit shirt. He announces with complete self "
            "satisfaction that the position of Project Lead has been filled — by himself "
            "— and that this will add 50,000 pounds to his annual salary. His expression "
            "is a bizarre mix of smugness and defensive bluster — chin up, eyes scanning "
            "for dissent. Blurred office workers visible behind him. 8 seconds."
        ),
        "continuity": "Jan: Shirt askew, sweaty, neck veins just visible at collar.",
        "gate": [
            "Jan's self-satisfaction reads as genuinely deluded — not villainous",
            "Shirt mis-buttoning still visible",
        ],
    },
    {
        "id": "S12",
        "name": "Open-Plan — Crowd Reaction Cuts",
        "duration": 6,
        "output": "S12_crowd_reaction.mp4",
        "images": [
            os.path.join(BUILD_DIR, "P12.jpg"),
            os.path.join(CHAR_DIR, "chris_identity_sheet.jpg"),
        ],
        "prompt": (
            "Three rapid reaction cuts in a modern open-plan office. First cut: a lean "
            "32-year-old in a light blue shirt with a barely suppressed amused smirk. "
            "Second cut: a group of two or three anonymous office workers exchanging "
            "disbelieving glances. Third cut: a stocky 40-year-old in a grey polo shirt "
            "with arms crossed, giving a completely flat, unsurprised stare to camera. "
            "Each cut is approximately 2 seconds. Shallow depth of field on each. "
            "Documentary handheld style. 6 seconds total."
        ),
        "continuity": "Chris: Light blue shirt same smirk. Rick: Grey polo same flat stare.",
        "gate": [
            "Chris is recognisable from S09 — same shirt, same smirk",
            "Rick is recognisable — same grey polo, same flat stare",
            "Reactions feel authentic not pantomime",
        ],
    },
    {
        "id": "S13",
        "name": "Canteen — Wide Establishing, Pastry Tray Empty",
        "duration": 6,
        "output": "S13_canteen_establishing.mp4",
        "images": [
            os.path.join(BUILD_DIR, "ep_tri_372-c-raftery-lowe-resized.jpg"),
            os.path.join(CHAR_DIR, "jan_peach_identity_sheet.jpg"),
        ],
        "prompt": (
            "A wide locked-off establishing shot of a modern corporate staff canteen "
            "set within a bright, large-windowed contemporary building interior with grey "
            "concrete columns. Morning light fills the space. Office workers in casual "
            "business attire sit at canteen tables eating pain au chocolat pastries. "
            "A canteen counter is visible to one side with a serving tray — the tray is "
            "now visibly empty, crumbs remaining. A canteen worker in a beige apron stands "
            "behind the counter. The CEO has not yet arrived. 6 seconds."
        ),
        "continuity": "Jan NOT present yet. Empty pastry tray must be clearly visible.",
        "gate": [
            "Canteen feels distinct from the office — different space, different furniture",
            "Empty pastry tray is clearly visible — plot-critical prop",
            "Canteen worker in beige apron identifiable behind counter",
        ],
    },
    {
        "id": "S14",
        "name": "Canteen — Jan Arrives, Discovers Empty Tray",
        "duration": 8,
        "output": "S14_jan_discovers_no_pastries.mp4",
        "images": [
            os.path.join(BUILD_DIR, "ep_tri_372-c-raftery-lowe-resized.jpg"),
            os.path.join(CHAR_DIR, "jan_peach_identity_sheet.jpg"),
        ],
        "prompt": (
            "A handheld tracking shot following a 52-year-old overweight CEO in a dark "
            "navy suit as he strides purposefully into a corporate canteen. He reaches "
            "the serving counter and looks down at the pastry tray — which is completely "
            "empty, only crumbs remaining. He looks up at the canteen worker behind the "
            "counter with an expression of disbelief beginning to tip into rage. His face "
            "begins to flush deep red. A vein in his neck becomes visible. 8 seconds."
        ),
        "continuity": "Jan: Full suit on, sweating slightly. Rage building from 0%.",
        "gate": [
            "Jan's face transition from confident to disbelief to rage-beginning reads clearly",
            "Empty tray is clearly visible — camera must show it",
        ],
    },
    {
        "id": "S15",
        "name": "Canteen — Full Meltdown: Plates Crash & Chair Through Window",
        "duration": 10,
        "output": "S15_canteen_meltdown_plates_chair.mp4",
        "images": [
            os.path.join(BUILD_DIR, "ep_tri_372-c-raftery-lowe-resized.jpg"),
            os.path.join(CHAR_DIR, "jan_peach_identity_sheet.jpg"),
            os.path.join(CHAR_DIR, "rick_identity_sheet.jpg"),
        ],
        "prompt": (
            "A wide static shot of a corporate canteen. A 52-year-old overweight CEO "
            "in a dark navy suit, face a deep furious crimson with visible neck veins "
            "and heavy sweat, suddenly screams at full volume. He grabs the plates from "
            "the canteen counter with both hands and sweeps them violently onto the hard "
            "floor — a massive crash of shattering china. The entire canteen falls silent, "
            "everyone frozen, staring. He grabs a heavy corporate meeting chair from a "
            "nearby table, raises it above his head with effort, and hurls it directly "
            "into the nearest large floor-to-ceiling window. The glass shatters. He "
            "reaches for a second chair. A stocky 40-year-old man in a grey polo shirt "
            "is visible at the back of the crowd, quietly and calmly stepping forward. "
            "10 seconds."
        ),
        "continuity": "Jan: Full rage state — crimson, neck veins, sweat-soaked. Rick calmly stepping forward in bg.",
        "gate": [
            "Plate smash reads as shocking — physical comedy climax",
            "Chair-through-window clearly depicted",
            "Rick calmly stepping forward is visible in background",
        ],
    },
    {
        "id": "S16",
        "name": "Canteen — Rick Draws Taser (Low MCU)",
        "duration": 5,
        "output": "S16_rick_draws_taser.mp4",
        "images": [
            os.path.join(BUILD_DIR, "ep_tri_372-c-raftery-lowe-resized.jpg"),
            os.path.join(CHAR_DIR, "rick_identity_sheet.jpg"),
        ],
        "prompt": (
            "A low-angle medium close-up on a stocky 40-year-old man in a grey polo "
            "shirt. With complete calm and no hurry, he reaches into his pocket and "
            "produces a small prop taser device — visibly toy-like and non-functional "
            "in appearance. He raises it deliberately toward something off-camera to "
            "his left. His expression does not change — flat, composed, entirely "
            "unsurprised. This is a man who has been waiting for this moment for years. "
            "5 seconds."
        ),
        "continuity": "Rick: Grey polo, taser prop clearly looks FAKE/toy-like.",
        "gate": [
            "Taser prop reads as clearly NON-FUNCTIONAL/toy-like — must NOT look like real weapon",
            "Rick's expression is FLAT CALM — NOT heroic, NOT angry",
        ],
    },
    {
        "id": "S17",
        "name": "Canteen — INSERT: Taser Flash",
        "duration": 3,
        "output": "S17_taser_insert_flash.mp4",
        "images": [
            os.path.join(BUILD_DIR, "ep_tri_372-c-raftery-lowe-resized.jpg"),
        ],
        "prompt": (
            "An extreme close-up insert shot of a small toy-like prop taser device "
            "firing. A brief blue-white electric arc crackle flashes from the tip for "
            "approximately 2 seconds. The device reads as clearly fake/prop quality — "
            "not a real weapon. The flash illuminates the surrounding air. "
            "Cut to black. 3 seconds."
        ),
        "continuity": "Prop only. Electric arc = comedic not threatening.",
        "gate": [
            "Electric arc is clearly a prop effect — comedic not threatening",
            "Short and punchy — 3 seconds max",
        ],
    },
    {
        "id": "S18",
        "name": "Canteen — Jan Slumps Face-Down",
        "duration": 5,
        "output": "S18_jan_slumps.mp4",
        "images": [
            os.path.join(BUILD_DIR, "ep_tri_372-c-raftery-lowe-resized.jpg"),
            os.path.join(CHAR_DIR, "jan_peach_identity_sheet.jpg"),
        ],
        "prompt": (
            "A wide shot. A 52-year-old overweight CEO in a dark navy suit suddenly "
            "freezes mid-motion — arms dropping, body going limp — and falls heavily "
            "forward, landing face-first on the hard canteen floor with a loud thud. "
            "He lies completely motionless, one arm splayed to the side, jacket rucked "
            "up, surrounded by shattered china on the floor. The canteen is completely "
            "silent. Everyone stares. The cracked window is visible in background. "
            "5 seconds."
        ),
        "continuity": "Jan: Face-down, unconscious, splayed arm. Broken china on floor.",
        "gate": [
            "Fall reads as sudden and physical — not slow or graceful",
            "Jan is clearly face-down and motionless",
            "Broken china on floor visible — continuity from S15",
        ],
    },
    {
        "id": "S19",
        "name": "Canteen — Final 2-Shot: Have You Killed Him?",
        "duration": 8,
        "output": "S19_have_you_killed_him.mp4",
        "images": [
            os.path.join(BUILD_DIR, "ep_tri_372-c-raftery-lowe-resized.jpg"),
            os.path.join(CHAR_DIR, "chris_identity_sheet.jpg"),
            os.path.join(CHAR_DIR, "rick_identity_sheet.jpg"),
        ],
        "prompt": (
            "A medium two-shot in a wrecked corporate canteen. A lean 32-year-old in "
            "a light blue shirt is crouched down next to an unconscious overweight man "
            "lying face-down on the floor surrounded by broken china. He looks up at a "
            "stocky 40-year-old in a grey polo shirt who is calmly and methodically "
            "sliding a small prop taser back into his trouser pocket. The 32-year-old's "
            "expression is somewhere between concerned and amused. The 40-year-old's "
            "expression is completely flat and calm. Behind them: shattered window, "
            "overturned chairs, stunned canteen workers in the background. 8 seconds."
        ),
        "continuity": "Chris: Light blue shirt. Rick: Grey polo. Jan unconscious visible in foreground.",
        "gate": [
            "Chris's expression lands the comedy — not pure horror, not pure amusement — the mix",
            "Rick's flat calm delivery is the final punchline",
            "Jan's unconscious form is visible in foreground/frame",
            "Broken china, cracked window — visual mess matches S15-S18 continuity",
        ],
    },
]


def load_image(path):
    with open(path, "rb") as f:
        data = f.read()
    ext = path.lower().split(".")[-1]
    mime = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png"}.get(ext, "image/jpeg")
    return types.Part.from_bytes(data=data, mime_type=mime)


def generate_shot(client, shot):
    shot_id = shot["id"]
    output_path = os.path.join(OUTPUT_DIR, shot["output"])

    print("\n" + "=" * 65)
    print(f"  🎬  GENERATING {shot_id}: {shot['name']}")
    print(f"  ⏱️   Duration: {shot['duration']}s")
    print(f"  📁  Output: {output_path}")
    print("=" * 65)

    if os.path.exists(output_path):
        print(f"\n  ⚠️  Clip already exists: {output_path}")
        choice = input("  Regenerate? (y/N): ").strip().lower()
        if choice != "y":
            print("  ⏭️  Skipping generation — using existing clip.")
            return True

    # Load images
    image_parts = []
    for img_path in shot["images"]:
        if os.path.exists(img_path):
            image_parts.append(load_image(img_path))
            print(f"  ✅ Image ref: {os.path.basename(img_path)}")
        else:
            print(f"  ⚠️  Missing image (skipping): {img_path}")

    full_prompt = shot["prompt"] + "\n\n" + STYLE_ANCHOR
    print(f"\n  📝 Submitting prompt ({len(full_prompt)} chars)...")

    operation = client.models.generate_videos(
        model="veo-2.0-generate-001",
        prompt=full_prompt,
        config=types.GenerateVideosConfig(
            duration_seconds=shot["duration"],
            aspect_ratio="16:9",
            number_of_videos=1,
        ),
    )

    print(f"  ✅ Operation submitted: {operation.name}")
    print("  ⏳ Waiting for generation (2-5 minutes)...")

    dots = 0
    while not operation.done:
        time.sleep(15)
        operation = client.operations.get(operation)
        dots += 1
        print(f"  ⏳ Still processing... ({dots * 15}s elapsed)", flush=True)

    if not (operation.response and operation.response.generated_videos):
        print(f"\n  ❌ Generation failed for {shot_id}")
        if operation.error:
            print(f"     Error: {operation.error}")
        return False

    video_uri = operation.response.generated_videos[0].video.uri
    print(f"\n  ✅ Video ready — downloading...")
    urllib.request.urlretrieve(video_uri, output_path)
    print(f"  ✅ SAVED: {output_path}")
    return True


def gate_check(shot):
    print("\n" + "-" * 65)
    print(f"  🚦  GATE CHECK — {shot['id']}: {shot['name']}")
    print(f"  🎭  Continuity: {shot['continuity']}")
    print("\n  Watch the clip and verify:")
    for i, check in enumerate(shot["gate"], 1):
        print(f"    [{i}] {check}")
    print("-" * 65)

    while True:
        choice = input("\n  APPROVE this shot? (y = Approved / n = Reject & stop): ").strip().lower()
        if choice == "y":
            print(f"  ✅ {shot['id']} APPROVED — moving to next shot.")
            return True
        elif choice == "n":
            print(f"  ❌ {shot['id']} REJECTED.")
            print("  → Edit the prompt for this shot in generate_all_shots.py SHOTS list")
            print("  → Re-run with: python generate_all_shots.py --start " + shot["id"])
            return False
        else:
            print("  Please enter 'y' or 'n'.")


def main():
    parser = argparse.ArgumentParser(description="Circle the Square — Gate-Based Shot Generator")
    parser.add_argument("--start", default="S01", help="Shot ID to start from (e.g. --start S05)")
    args = parser.parse_args()

    if API_KEY == "PASTE_YOUR_AI_STUDIO_API_KEY_HERE":
        print("\n❌ ERROR: No API key set.")
        print("   Open generate_all_shots.py and paste your AI Studio API key into the API_KEY variable.")
        print("   Get your key at: https://aistudio.google.com/apikey")
        sys.exit(1)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    client = genai.Client(api_key=API_KEY)

    # Find starting shot index
    start_index = 0
    for i, shot in enumerate(SHOTS):
        if shot["id"] == args.start:
            start_index = i
            break
    else:
        print(f"❌ Shot ID '{args.start}' not found. Valid IDs: {[s['id'] for s in SHOTS]}")
        sys.exit(1)

    print("\n" + "=" * 65)
    print("  🎬  CIRCLE THE SQUARE — FEATURETTE VIDEO GENERATOR")
    print("  📋  Mode: Gate-Based Sequential Production")
    print(f"  🚀  Starting from: {args.start}")
    print(f"  🎯  Total shots remaining: {len(SHOTS) - start_index}")
    print("=" * 65)

    approved = 0
    for shot in SHOTS[start_index:]:
        # Generate
        success = generate_shot(client, shot)
        if not success:
            print(f"\n❌ Generation failed for {shot['id']}. Stopping.")
            break

        # Gate check
        passed = gate_check(shot)
        if not passed:
            print(f"\n⛔ Pipeline stopped at {shot['id']}.")
            print(f"   {approved} shots approved before stopping.")
            break

        approved += 1
        print(f"\n  Progress: {approved} / {len(SHOTS) - start_index} shots approved ✅")

    else:
        print("\n" + "=" * 65)
        print(f"  🎉  ALL {len(SHOTS)} SHOTS GENERATED AND APPROVED!")
        print(f"  📁  Clips saved to: {OUTPUT_DIR}")
        print("\n  NEXT STEP: Import all clips into DaVinci / Premiere in order:")
        for shot in SHOTS:
            print(f"    {shot['id']} → {shot['output']}")
        print("\n  Then dub Qwen3-TTS dialogue from: C:\\ai\\Circle the Square\\audio-refs\\")
        print("=" * 65)


if __name__ == "__main__":
    main()
