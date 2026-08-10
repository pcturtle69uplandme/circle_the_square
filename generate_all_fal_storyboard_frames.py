import os
import sys
import time
from pathlib import Path

# Add parent dir to import fal_key
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import fal_client
from fal_key import require_fal_key

require_fal_key()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRAMES_DIR = os.path.join(BASE_DIR, "storyboard-frames")
os.makedirs(FRAMES_DIR, exist_ok=True)

STYLE_ANCHOR = (
    "Photoreal single film-still frame, not video. Documentary British mockumentary photographic tone. "
    "Natural Northern European daylight. Shallow depth of field on close-ups, deep focus on wides. "
    "2.39:1 cinematic widescreen still crop. "
)

CHAR_JAN = "Jan Peach, a 52-year-old British male corporate executive with a soft overweight build, pale skin, thinning brown comb-over hair, wearing a tight navy suit and dark tie. "
CHAR_CHRISTINA = "Christina Dross, a 38-year-old British female corporate manager, slim build, sharp dark bob haircut, wearing a crisp charcoal blazer. "
CHAR_SHARON = "Sharon Enfield, a 34-year-old British female corporate employee, curvy build, auburn hair, wearing an emerald green blouse. "
CHAR_CHRIS = "Chris, a 32-year-old male staff worker, lean build, light blue collared shirt, smirking expression. "
CHAR_RICK = "Rick, a 40-year-old male corporate security officer, broad muscular build, grey polo shirt, deadpan. "
LOC_OFFICE = "Inside a modern corporate executive office with glass partitions and sleek timber desk. "
LOC_OPENPLAN = "Inside a bright open-plan office floor with desk rows, computer monitors, and overhead acoustic baffles. "
LOC_CANTEEN = "Inside a modern corporate staff canteen with stainless steel food counters and glass wall partitions. "

FRAMES = [
    # SCENE 1 — JAN'S OFFICE
    ("F01", STYLE_ANCHOR + LOC_OFFICE + CHAR_CHRISTINA + "enters and stands opposite " + CHAR_JAN + "'s desk, relaxed and professional. Jan looks up from his desk toward her."),
    ("F02", STYLE_ANCHOR + LOC_OFFICE + CHAR_JAN + "leaning back in his desk chair with a put-upon, exhausted expression, small sigh."),
    ("F03", STYLE_ANCHOR + LOC_OFFICE + CHAR_CHRISTINA + "upright, businesslike and mid-pitch, holding a tablet."),
    ("F04", STYLE_ANCHOR + LOC_OFFICE + CHAR_JAN + "leaning forward slightly, genuinely curious."),
    ("F05", STYLE_ANCHOR + LOC_OFFICE + CHAR_CHRISTINA + "explaining calmly and matter-of-factly with one hand gesturing slightly."),
    ("F06a", STYLE_ANCHOR + LOC_OFFICE + CHAR_JAN + "eyes lighting up, fingers steepling, chin raised, genuinely enthused."),
    ("F06b", STYLE_ANCHOR + LOC_OFFICE + CHAR_JAN + "gesturing with an open hand, smugly convinced of his own brilliance."),
    ("F07", STYLE_ANCHOR + LOC_OFFICE + "Over-the-shoulder still behind " + CHAR_JAN + " toward " + CHAR_CHRISTINA + ". Her expression is completely flat and dry."),
    ("F08", STYLE_ANCHOR + LOC_OFFICE + CHAR_JAN + "brisk and dismissive, waving his hand."),
    ("F09", STYLE_ANCHOR + LOC_OFFICE + CHAR_CHRISTINA + "a flicker of genuine confusion crossing her usually flat expression."),
    ("F10", STYLE_ANCHOR + LOC_OFFICE + CHAR_JAN + "mildly incredulous, gesturing about Star Trek."),
    ("F11", STYLE_ANCHOR + LOC_OFFICE + CHAR_CHRISTINA + "deadpan with heavy sarcasm."),
    ("F12", STYLE_ANCHOR + LOC_OFFICE + CHAR_JAN + "waving a hand toward the door, distracted."),
    ("F13", STYLE_ANCHOR + LOC_OFFICE + CHAR_CHRISTINA + "one eyebrow raised, needling him on her way out."),
    ("F14", STYLE_ANCHOR + LOC_OFFICE + CHAR_JAN + "visibly offended, sitting up straight, bristling."),
    ("F15", STYLE_ANCHOR + LOC_OFFICE + CHAR_CHRISTINA + "cutting him off mid-sentence with a flat deadpan delivery."),
    ("F16", STYLE_ANCHOR + LOC_OFFICE + CHAR_JAN + "face fully flushed red, screaming furiously, neck veins bulging."),
    ("F17", STYLE_ANCHOR + LOC_OFFICE + CHAR_CHRISTINA + "walks out and shuts the glass office door calmly behind her, unbothered."),
    ("F18", STYLE_ANCHOR + LOC_OFFICE + CHAR_JAN + "alone now, flustered and sweating profusely, mid-motion unbuttoning his navy suit shirt collar and tie."),
    ("F19", STYLE_ANCHOR + LOC_OFFICE + CHAR_JAN + "has pulled his navy suit shirt fully off, chest bared with black necktie around his neck, mid-motion dropping the shirt onto his desk."),
    ("F20", STYLE_ANCHOR + LOC_OFFICE + CHAR_SHARON + "opens the glass door walking in unannounced. Shirtless " + CHAR_JAN + " spins around in shock."),
    ("F21", STYLE_ANCHOR + LOC_OFFICE + CHAR_SHARON + "eyes flicking briefly down toward " + CHAR_JAN + "'s chest, expression staying completely neutral."),
    ("F22", STYLE_ANCHOR + LOC_OFFICE + CHAR_JAN + "frozen in mortified realization that she has seen him shirtless."),
    ("F23", STYLE_ANCHOR + LOC_OFFICE + CHAR_SHARON + "looking flat and transactional, as if nothing unusual is happening."),
    ("F24", STYLE_ANCHOR + LOC_OFFICE + CHAR_JAN + "flustered, trying to wave her off while half-undressed."),
    ("F25", STYLE_ANCHOR + LOC_OFFICE + CHAR_SHARON + "flat and matter-of-fact, unmoved by his protest."),
    ("F26a", STYLE_ANCHOR + LOC_OFFICE + CHAR_JAN + "shirtless and sweating, yanking venetian blinds down with both hands."),
    ("F26b", STYLE_ANCHOR + LOC_OFFICE + CHAR_JAN + "turning and locking the office door."),

    # SCENE 2 — OPEN PLAN FLOOR
    ("F27", STYLE_ANCHOR + LOC_OPENPLAN + CHAR_CHRIS + " and " + CHAR_RICK + " stand by a desk run, relaxed, mid-conversation."),
    ("F28", STYLE_ANCHOR + LOC_OPENPLAN + CHAR_CHRIS + "dry smirk, delivering line to Rick."),
    ("F29", STYLE_ANCHOR + LOC_OPENPLAN + CHAR_RICK + "completely flat, unbothered, responding without missing a beat."),
    ("F30", STYLE_ANCHOR + LOC_OPENPLAN + CHAR_SHARON + "walks past " + CHAR_CHRIS + " and " + CHAR_RICK + ", dripping sweat, hair dishevelled, unhurried."),
    ("F31", STYLE_ANCHOR + LOC_OPENPLAN + CHAR_JAN + "emerges onto open plan floor, shirt re-buttoned askew, clapping hands loudly."),
    ("F32", STYLE_ANCHOR + LOC_OPENPLAN + CHAR_CHRIS + "needling, half-smirking, calling out from the crowd."),
    ("F33", STYLE_ANCHOR + LOC_OPENPLAN + CHAR_JAN + "caught off guard, covering quickly."),
    ("F34", STYLE_ANCHOR + LOC_OPENPLAN + "Wide still of gathered office crowd, quiet sniggering rippling through workers."),
    ("F35", STYLE_ANCHOR + LOC_OPENPLAN + CHAR_JAN + "flushed, snapping at crowd, gesturing sharply about a new project."),
    ("F36", STYLE_ANCHOR + LOC_OPENPLAN + CHAR_RICK + "arms crossed, flat and pointed."),
    ("F37a", STYLE_ANCHOR + LOC_OPENPLAN + CHAR_JAN + "defensive and blustering, justifying himself."),
    ("F37b", STYLE_ANCHOR + LOC_OPENPLAN + CHAR_JAN + "peak self-satisfaction as he announces Project Inception."),
    ("F38", STYLE_ANCHOR + LOC_OPENPLAN + CHAR_CHRIS + "shouting out to laughing crowd, delighted."),
    ("F39", STYLE_ANCHOR + LOC_OPENPLAN + CHAR_JAN + "confused, thrown off."),
    ("F40", STYLE_ANCHOR + LOC_OPENPLAN + CHAR_CHRIS + "explaining with a smirk."),
    ("F41", STYLE_ANCHOR + LOC_OPENPLAN + CHAR_JAN + "flustered, backpedalling, trying to save face."),
    ("F42", STYLE_ANCHOR + LOC_OPENPLAN + "Close-up insert of stacked merchandise: stress balls, pens, t-shirts printed with PROJECT INCEPTION."),
    ("F43", STYLE_ANCHOR + LOC_OPENPLAN + CHAR_CHRIS + "genuinely curious this time."),
    ("F44", STYLE_ANCHOR + LOC_OPENPLAN + CHAR_JAN + "chin raised, savouring the moment, announcing he will lead it."),
    ("F45", STYLE_ANCHOR + LOC_OPENPLAN + "Wide still of open plan crowd, collective groan rippling through them."),
    ("F46", STYLE_ANCHOR + LOC_OPENPLAN + CHAR_JAN + "defiant, sweating, jabbing finger for emphasis, announcing 50k raise."),

    # SCENE 3 — CANTEEN
    ("F47", STYLE_ANCHOR + LOC_CANTEEN + "Morning canteen, corporate workers seated eating pastries, high demand."),
    ("F48", STYLE_ANCHOR + LOC_CANTEEN + "Insert still of empty stainless steel pastry tray with only crumbs left."),
    ("F49", STYLE_ANCHOR + LOC_CANTEEN + CHAR_JAN + "strides purposefully into canteen, confident, full suit on."),
    ("F50", STYLE_ANCHOR + LOC_CANTEEN + CHAR_JAN + "reaches counter, looking around for pain au chocolat."),
    ("F51", STYLE_ANCHOR + LOC_CANTEEN + "Canteen worker in beige apron behind counter shaking head apologetically."),
    ("F52", STYLE_ANCHOR + LOC_CANTEEN + CHAR_JAN + "face deep red, neck vein bulging, tipping into full fury."),
    ("F53", STYLE_ANCHOR + LOC_CANTEEN + CHAR_JAN + "grabs ceramic plates from counter with both hands, sweeping them violently off counter."),
    ("F54", STYLE_ANCHOR + LOC_CANTEEN + "China shattered across floor tiles, entire canteen frozen in shock."),
    ("F55", STYLE_ANCHOR + LOC_CANTEEN + CHAR_JAN + "deep crimson, sweat-soaked, screaming at full volume with arms wide."),
    ("F56", STYLE_ANCHOR + LOC_CANTEEN + CHAR_JAN + "hurling heavy meeting chair into floor-to-ceiling glass wall, glass mid-shatter."),
    ("F57", STYLE_ANCHOR + LOC_CANTEEN + CHAR_JAN + "reaches for second chair. Behind him, " + CHAR_RICK + " steps forward calm, raising prop taser."),
    ("F58", STYLE_ANCHOR + LOC_CANTEEN + "Extreme close-up insert of toy prop taser firing with blue-white electric spark arc."),
    ("F59", STYLE_ANCHOR + LOC_CANTEEN + CHAR_JAN + "slumped face-first onto floor tiles unconscious amidst broken china, " + CHAR_RICK + " standing calm."),
    ("F60", STYLE_ANCHOR + LOC_CANTEEN + CHAR_CHRIS + "crouches next to unconscious Jan, looking up at " + CHAR_RICK + " amused and concerned."),
    ("F61", STYLE_ANCHOR + LOC_CANTEEN + CHAR_RICK + "calmly stowing prop taser, expression completely flat and unbothered.")
]

print(f"=== Starting fal.ai Flux Schnell Batch Generation ({len(FRAMES)} Frames total) ===")
print("Est. Total Cost: ~$" + f"{len(FRAMES) * 0.003:.3f}")

successful = 0
failed = 0

for idx, (frame_id, prompt) in enumerate(FRAMES, 1):
    out_path = Path(FRAMES_DIR) / f"{frame_id}.jpg"
    print(f"[{idx}/{len(FRAMES)}] Generating {frame_id} -> {out_path.name} ...", flush=True)
    try:
        result = fal_client.subscribe(
            "fal-ai/flux/schnell",
            arguments={
                "prompt": prompt,
                "image_size": "landscape_16_9",
                "num_images": 1,
                "enable_safety_checker": False
            }
        )
        images = result.get("images") or []
        if images and "url" in images[0]:
            import urllib.request
            req = urllib.request.Request(images[0]["url"], headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=120) as resp:
                out_path.write_bytes(resp.read())
            successful += 1
            print(f"  [OK] Saved {frame_id}.jpg")
        else:
            print(f"  [FAIL] Failed: No URL returned for {frame_id}")
            failed += 1
    except Exception as e:
        print(f"  [FAIL] Error generating {frame_id}: {e}")
        failed += 1
    time.sleep(0.2)

print(f"\n=== Batch Complete! ===")
print(f"Successfully generated: {successful}/{len(FRAMES)} frames")
print(f"Saved to: {FRAMES_DIR}")
