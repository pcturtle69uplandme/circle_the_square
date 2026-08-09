import os
import sys
import torch

try:
    from diffusers import LTXPipeline
    from diffusers.utils import export_to_video
except ImportError as e:
    print("Error importing diffusers:", e)
    sys.exit(1)

ckpt_path = r"C:\ai\ComfyUI\ComfyUI\models\checkpoints\ltx-video-2b-v0.9.safetensors"
output_dir = r"C:\ai\Circle the Square\clips"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "OPENING_T01_ltx_drone_prow.mp4")

print(f"Loading LTX-Video model from local checkpoint: {ckpt_path}")
print(f"Target GPU: {torch.cuda.get_device_name(0)}")

try:
    # Load pipeline from single safetensors file
    pipe = LTXPipeline.from_single_file(
        ckpt_path,
        torch_dtype=torch.bfloat16
    )
    pipe.to("cuda")
    print("LTXPipeline loaded successfully into VRAM!")
except Exception as e:
    print(f"Single file load error ({e}), trying HuggingFace model ID 'Lightricks/LTX-Video'...")
    try:
        pipe = LTXPipeline.from_pretrained(
            "Lightricks/LTX-Video",
            torch_dtype=torch.bfloat16
        )
        pipe.to("cuda")
        print("HuggingFace pipeline loaded successfully into VRAM!")
    except Exception as e2:
        print("Model load error:", e2)
        sys.exit(1)

prompt = (
    "Cinematic 4K low drone camera flyby sliding past the curved buff-brick acute prow "
    "of a modern corporate mothership office building at cold blue-hour dawn. "
    "Smooth 24fps sliding camera movement, crisp architecture, hyper-realistic daylight."
)

negative_prompt = "blurry, low quality, distorted, jitter, noise, oversaturated, text, watermark"

print("Generating 97-frame 24fps video clip for Shot T-01...")
with torch.inference_mode():
    video = pipe(
        prompt=prompt,
        negative_prompt=negative_prompt,
        width=768,
        height=512,
        num_frames=97,
        num_inference_steps=30,
        guidance_scale=3.0,
        generator=torch.Generator(device="cuda").manual_seed(42)
    ).frames[0]

export_to_video(video, output_path, fps=24)
print(f"Successfully generated LTX-Video clip: {output_path}")
