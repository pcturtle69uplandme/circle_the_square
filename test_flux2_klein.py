import sys
import traceback
import torch

try:
    from diffusers import AutoPipelineForText2Image
    print("Diffusers AutoPipeline import OK!")
except ImportError as e:
    print("Diffusers import error:", e)
    sys.exit(1)

print(f"Target GPU: {torch.cuda.get_device_name(0)}")

try:
    print("Loading FLUX.2-klein-4B using AutoPipelineForText2Image...")
    pipe = AutoPipelineForText2Image.from_pretrained(
        "black-forest-labs/FLUX.2-klein-4B",
        torch_dtype=torch.bfloat16
    )
    pipe.to("cuda")
    print(f"Pipeline class loaded: {pipe.__class__.__name__}")

    prompt_str = (
        "Cinematic photoreal film still frame from British workplace mockumentary. "
        "40s male corporate executive sitting alone at his wooden desk in a modern executive office, "
        "flustered and sweating, loosening his dark navy necktie and unbuttoning his top shirt collar. "
        "Geometric orange triangle wall pattern in background, natural daylight, 16:9 widescreen crop."
    )

    print("Generating 1024x576 frame with FLUX.2 Klein...")
    with torch.inference_mode():
        image = pipe(
            prompt=prompt_str,
            width=1024,
            height=576,
            num_inference_steps=4,
            guidance_scale=1.0,
            generator=torch.Generator("cuda").manual_seed(118)
        ).images[0]

    out_path = r"C:\ai\Circle the Square\storyboard-frames\F18.jpg"
    image.save(out_path, quality=95)
    print(f"-> Successfully saved photorealistic FLUX.2 frame to: {out_path}")

except Exception as e:
    print("FLUX.2 execution error:", e)
    traceback.print_exc()
    sys.exit(1)
