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

STYLE = "Photoreal single film-still frame, British workplace mockumentary photographic tone, natural daylight, 16:9 widescreen crop."

pending_frames = [
    {
        "id": "F19",
        "prompt": f"Wide shot of 40s male corporate executive shirtless in office, white shirt on desk, red flushed skin, comedic visual gag beat, {STYLE}",
        "seed": 119
    },
    {
        "id": "F21",
        "prompt": f"Medium close-up on mature female office worker in emerald green blouse looking down neutral expression at shirtless male boss in executive office, {STYLE}",
        "seed": 121
    },
    {
        "id": "F22",
        "prompt": f"Medium close-up of 40s male executive shirtless, mortified embarrassed posture, self-conscious face, {STYLE}",
        "seed": 122
    },
    {
        "id": "F23",
        "prompt": f"Medium close-up on composed mature female corporate manager in emerald green blouse speaking calmly in modern executive office, {STYLE}",
        "seed": 123
    },
    {
        "id": "F24",
        "prompt": f"Medium close-up on flustered male executive half-undressed waving hand defensively at female colleague, {STYLE}",
        "seed": 124
    },
    {
        "id": "F25",
        "prompt": f"Medium close-up on mature female corporate manager in emerald green blouse with arms crossed, calm composed posture, {STYLE}",
        "seed": 125
    },
    {
        "id": "F26a",
        "prompt": f"Medium close-up of male executive yanking venetian window blinds closed with both hands in modern glass office, {STYLE}",
        "seed": 126
    },
    {
        "id": "F26b",
        "prompt": f"Close-up of hand turning door lock knob on modern office glass door, {STYLE}",
        "seed": 127
    }
]

print(f"\n--- Batch Rendering {len(pending_frames)} Scene 1 Frames with FLUX.2 Klein ---")

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

print("\nAll remaining Scene 1 FLUX.2 frames successfully generated!")
