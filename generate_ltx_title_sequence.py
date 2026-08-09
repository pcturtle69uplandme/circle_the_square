import os
import sys
import torch

try:
    from diffusers import LTXPipeline
    from diffusers.utils import export_to_video
except ImportError as e:
    print("Error importing diffusers:", e)
    sys.exit(1)

output_dir = r"C:\ai\Circle the Square\clips"
os.makedirs(output_dir, exist_ok=True)

print("Loading LTX-Video Pipeline into VRAM...")
pipe = LTXPipeline.from_pretrained(
    "Lightricks/LTX-Video",
    torch_dtype=torch.bfloat16
)
pipe.to("cuda")
print(f"Pipeline ready on {torch.cuda.get_device_name(0)}!")

shots = [
    {
        "id": "OPENING_T02_ltx_atrium_orbit",
        "prompt": (
            "Cinematic 4K high aerial drone camera rotating slowly in an orbital sweep "
            "over a massive triangular modern office building with glazed atrium and green planted roof courtyards. "
            "Smooth 24fps drone rotation, bright daylight, architectural depth."
        ),
        "seed": 101,
        "frames": 97
    },
    {
        "id": "OPENING_T03_ltx_interior_cuts",
        "prompt": (
            "Cinematic 4K tracking shot gliding through a sleek modern corporate office atrium. "
            "Glass security speed gates opening smoothly, warm interior daylight, glass reflections, 24fps smooth motion."
        ),
        "seed": 202,
        "frames": 97
    },
    {
        "id": "OPENING_T04_ltx_drone_pullback",
        "prompt": (
            "Cinematic 4K high aerial drone pull-back shot revealing a large triangular corporate headquarters campus "
            "against the horizon at sunset. Smooth backward camera motion, dramatic sky, 24fps."
        ),
        "seed": 303,
        "frames": 97
    }
]

negative_prompt = "blurry, low quality, distorted, jitter, noise, oversaturated, text, watermark"

for shot in shots:
    out_path = os.path.join(output_dir, f"{shot['id']}.mp4")
    print(f"\n--- Generating {shot['id']} ({shot['frames']} frames at 24fps) ---")
    with torch.inference_mode():
        video = pipe(
            prompt=shot["prompt"],
            negative_prompt=negative_prompt,
            width=768,
            height=512,
            num_frames=shot["frames"],
            num_inference_steps=30,
            guidance_scale=3.0,
            generator=torch.Generator(device="cuda").manual_seed(shot["seed"])
        ).frames[0]

    export_to_video(video, out_path, fps=24)
    print(f"-> Saved: {out_path}")

print("\nAll Opening Title Sequence clips successfully generated!")
