import os
import sys
import torch
from diffusers import AutoPipelineForText2Image

out_dir = r"C:\ai\Circle the Square\storyboard-frames"
os.makedirs(out_dir, exist_ok=True)

print("Loading FLUX.2-klein-4B pipeline...")
pipe = AutoPipelineForText2Image.from_pretrained(
    "black-forest-labs/FLUX.2-klein-4B",
    torch_dtype=torch.bfloat16
)
pipe.to("cuda")
print(f"Pipeline ready on {torch.cuda.get_device_name(0)}!")

STYLE = (
    "Stylised British sitcom comic art, clean bold line art, flat muted colour palette, "
    "expressive caricature, cel-shaded, 16:9 widescreen crop. NOT photorealistic. "
    "Absolutely NO text, NO speech bubbles, NO captions, NO labels, NO sound effects, "
    "NO lettering of any kind anywhere in the image."
)

pending_frames = [
    {
        "id": "F01",
        "prompt": f"Wide shot still. Modern executive office with geometric triangle acoustic wall and walnut desk. Christina Dross, 38yo slim British woman with sharp dark bob fringe in charcoal trouser suit and orange lanyard, enters and stands opposite desk greeting her boss. Jan Peach, 52yo overweight British CEO with thinning comb-over in navy suit, looks up from his desk toward her. {STYLE}",
        "seed": 101
    },
    {
        "id": "F02",
        "prompt": f"Medium close-up on Jan Peach sitting at his walnut desk in modern executive office, giving a small put-upon sigh, leaning back in chair with bored smug expression. {STYLE}",
        "seed": 102
    },
    {
        "id": "F03",
        "prompt": f"Medium close-up on Christina Dross in charcoal trouser suit and cream blouse, upright and businesslike, mid-pitch holding digital tablet in modern executive office. {STYLE}",
        "seed": 103
    },
    {
        "id": "F04",
        "prompt": f"Medium close-up on Jan Peach at walnut desk, leaning forward slightly with hands on desk, curious interested expression. {STYLE}",
        "seed": 104
    },
    {
        "id": "F05",
        "prompt": f"Medium close-up on Christina Dross explaining calmly and matter-of-factly, gesturing slightly with hand, delivering pitch in modern executive office. {STYLE}",
        "seed": 105
    },
    {
        "id": "F06a",
        "prompt": f"Medium close-up. Jan Peach's eyes light up, fingers steepling together under his chin, chin raised, smugly enthused. {STYLE}",
        "seed": 106
    },
    {
        "id": "F06b",
        "prompt": f"Medium close-up on Jan Peach gesturing with one open hand, boastful expression, utterly convinced of his strategic genius. {STYLE}",
        "seed": 107
    },
    {
        "id": "F07",
        "prompt": f"Over-the-shoulder still from behind Jan Peach toward Christina Dross. Her expression is completely dry, flat, and unbothered. {STYLE}",
        "seed": 108
    },
    {
        "id": "F08",
        "prompt": f"Medium close-up on Jan Peach, brisk dismissive hand wave, arrogant executive posture. {STYLE}",
        "seed": 109
    },
    {
        "id": "F09",
        "prompt": f"Medium close-up on Christina Dross, a flicker of genuine confusion crossing her usually deadpan face. {STYLE}",
        "seed": 110
    },
    {
        "id": "F10",
        "prompt": f"Medium close-up on Jan Peach, mildly incredulous that she missed his pop culture reference. {STYLE}",
        "seed": 111
    },
    {
        "id": "F11",
        "prompt": f"Medium close-up on Christina Dross, deadpan expression with heavy sarcasm, subtle eyebrow raise. {STYLE}",
        "seed": 112
    },
    {
        "id": "F12",
        "prompt": f"Medium close-up on Jan Peach waving hand dismissively toward the door, distracted and impatient. {STYLE}",
        "seed": 113
    },
    {
        "id": "F13",
        "prompt": f"Medium close-up on Christina Dross turning near the glass office door, one eyebrow arched, needling him dryly. {STYLE}",
        "seed": 114
    },
    {
        "id": "F14",
        "prompt": f"Tight close-up on Jan Peach, visibly offended, sitting bolt upright, bristling with indignation. {STYLE}",
        "seed": 115
    },
    {
        "id": "F15",
        "prompt": f"Medium close-up on Christina Dross delivering deadpan punchline calmly before leaving. {STYLE}",
        "seed": 116
    },
    {
        "id": "F16",
        "prompt": f"Tight close-up on Jan Peach, face fully flushed furious red, screaming with mouth open in rage, neck veins popping. {STYLE}",
        "seed": 117
    },
    {
        "id": "F17",
        "prompt": f"Wide shot still. Christina Dross calmly exits through modern glass office door, completely unbothered, door clicking shut. {STYLE}",
        "seed": 118
    },
    {
        "id": "F18",
        "prompt": f"Medium close-up. Jan Peach, alone now, flustered and sweating profusely, begins unbuttoning his shirt collar. {STYLE}",
        "seed": 119
    },
    {
        "id": "F19",
        "prompt": f"Wide still. Jan Peach has pulled his shirt fully off, chest bared, mid-motion dropping it onto his desk in modern office, red flushed skin, comedic visual gag beat. {STYLE}",
        "seed": 120
    },
    {
        "id": "F20",
        "prompt": f"Wide still. Modern glass office door has just opened — Sharon Enfield in emerald green blouse walks in unannounced without knocking. Jan Peach, shirtless at desk, spins toward her in alarm. {STYLE}",
        "seed": 121
    },
    {
        "id": "F21",
        "prompt": f"Medium close-up on Sharon Enfield with wavy auburn hair in emerald green blouse, eyes flicking briefly down toward Jan's chest, expression staying completely neutral. {STYLE}",
        "seed": 122
    },
    {
        "id": "F22",
        "prompt": f"Medium close-up on Jan Peach shirtless in modern office, frozen in mortified realisation that she has seen him. {STYLE}",
        "seed": 123
    },
    {
        "id": "F23",
        "prompt": f"Medium close-up on composed Sharon Enfield in emerald green blouse speaking calmly and transactionally in modern executive office. {STYLE}",
        "seed": 124
    },
    {
        "id": "F24",
        "prompt": f"Medium close-up on flustered Jan Peach half-undressed waving hand defensively at Sharon Enfield in modern executive office. {STYLE}",
        "seed": 125
    },
    {
        "id": "F25",
        "prompt": f"Medium close-up on Sharon Enfield in emerald green blouse with arms crossed, calm composed posture, flat and matter-of-fact. {STYLE}",
        "seed": 126
    },
    {
        "id": "F26a",
        "prompt": f"Medium close-up of Jan Peach yanking venetian window blinds closed with both hands in modern glass office. {STYLE}",
        "seed": 127
    },
    {
        "id": "F26b",
        "prompt": f"Close-up of hand turning door lock knob on modern office glass door. {STYLE}",
        "seed": 128
    }
]

print(f"\n--- Batch Rendering {len(pending_frames)} Scene 1 Cartoon Frames with FLUX.2 Klein ---")

for item in pending_frames:
    out_path = os.path.join(out_dir, f"{item['id']}.jpg")
    print(f"Rendering {item['id']}...")
    with torch.inference_mode():
        image = pipe(
            prompt=item["prompt"],
            width=1024,
            height=576,
            num_inference_steps=4,
            guidance_scale=1.0,
            generator=torch.Generator("cuda").manual_seed(item["seed"])
        ).images[0]

    image.save(out_path, quality=95)
    print(f"-> Saved: {out_path}")

print("\nAll remaining Scene 1 cartoon FLUX.2 frames successfully generated!")
