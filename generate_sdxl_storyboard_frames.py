import os
import sys
import torch

try:
    from diffusers import StableDiffusionXLPipeline, EulerDiscreteScheduler
except ImportError as e:
    print("Diffusers import error:", e)
    sys.exit(1)

model_path = r"C:\ai\ComfyUI\realvisxlV50_v50LightningBakedvae.safetensors"
out_dir = r"C:\ai\Circle the Square\storyboard-frames"
os.makedirs(out_dir, exist_ok=True)

print(f"Loading RealVisXL V5.0 Lightning SDXL model on {torch.cuda.get_device_name(0)}...")
pipe = StableDiffusionXLPipeline.from_single_file(
    model_path,
    torch_dtype=torch.float16,
    use_safetensors=True
)
pipe.scheduler = EulerDiscreteScheduler.from_config(pipe.scheduler.config, timestep_spacing="trailing")
pipe.to("cuda")
print("Model ready!")

# Style Anchor for Photorealistic Mockumentary Tone
STYLE = (
    "photoreal film still, British workplace mockumentary tone, natural European interior daylight, "
    "shallow depth of field, sharp focus, 8k resolution, cinematic 16:9 framing, detailed face, photorealistic office."
)

NEG_PROMPT = "anime, 3d render, illustration, vector, cartoon, blurry, lowres, distorted face, extra limbs, bad anatomy, watermark"

frames_to_generate = [
    {
        "id": "F18",
        "prompt": f"Medium close-up of 40s male corporate executive sitting alone at office desk, flustered, sweating, loosening tie and unbuttoning collar, {STYLE}",
        "seed": 118
    },
    {
        "id": "F19",
        "prompt": f"Wide shot of 40s male corporate executive shirtless in office, white shirt on desk, red flushed skin, comedy beat, {STYLE}",
        "seed": 119
    },
    {
        "id": "F21",
        "prompt": f"Medium shot of mature female office worker in green blouse looking down neutral expression at shirtless male boss in executive office, {STYLE}",
        "seed": 121
    },
    {
        "id": "F22",
        "prompt": f"Medium close-up of 40s male executive shirtless, mortified embarrassed expression, hands covering chest, {STYLE}",
        "seed": 122
    },
    {
        "id": "F23",
        "prompt": f"Medium shot of composed female corporate manager in green top speaking calmly in modern executive office, {STYLE}",
        "seed": 123
    },
    {
        "id": "F24",
        "prompt": f"Medium shot of flustered male executive half-undressed waving hand defensively at female colleague, {STYLE}",
        "seed": 124
    },
    {
        "id": "F25",
        "prompt": f"Medium shot of female corporate manager with arms crossed, calm composed posture, {STYLE}",
        "seed": 125
    },
    {
        "id": "F26a",
        "prompt": f"Medium shot of male executive yanking venetian window blinds closed with both hands in modern glass office, {STYLE}",
        "seed": 126
    },
    {
        "id": "F26b",
        "prompt": f"Close-up of hand turning door lock knob on modern office glass door, {STYLE}",
        "seed": 127
    }
]

print(f"\n--- Generating {len(frames_to_generate)} Photorealistic Storyboard Frames ---")

for item in frames_to_generate:
    out_path = os.path.join(out_dir, f"{item['id']}.jpg")
    print(f"Generating {item['id']}...")
    image = pipe(
        prompt=item["prompt"],
        negative_prompt=NEG_PROMPT,
        width=1024,
        height=576,
        num_inference_steps=8,  # Lightning model fast 8 steps
        guidance_scale=2.0,
        generator=torch.Generator(device="cuda").manual_seed(item["seed"])
    ).images[0]

    image.save(out_path, quality=95)
    print(f"  -> Saved photorealistic frame: {out_path}")

print("\nAll pending Scene 1 photorealistic frames successfully generated!")
