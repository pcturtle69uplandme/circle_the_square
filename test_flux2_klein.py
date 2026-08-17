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

    STYLE_ANCHOR = (
        "Stylised British sitcom comic art, clean bold line art, flat muted colour palette, "
        "expressive caricature, cel-shaded, 16:9 widescreen crop. NOT photorealistic. "
        "Absolutely NO text, NO speech bubbles, NO captions, NO labels, NO sound effects, "
        "NO lettering of any kind anywhere in the image."
    )

    prompt_str = (
        f"Wide shot still. Modern executive office with geometric triangle acoustic wall and walnut desk. "
        f"Christina Dross, 38yo slim British woman with sharp dark bob fringe in charcoal trouser suit and orange lanyard, "
        f"enters and stands opposite desk greeting her boss. Jan Peach, 52yo overweight British CEO with thinning comb-over "
        f"in navy suit, looks up from his desk toward her. {STYLE_ANCHOR}"
    )

    print("Generating Frame F01 (1024x576) with FLUX.2 Klein 4B...")
    with torch.inference_mode():
        image = pipe(
            prompt=prompt_str,
            width=1024,
            height=576,
            num_inference_steps=4,
            guidance_scale=1.0,
            generator=torch.Generator("cuda").manual_seed(101)
        ).images[0]

    out_path = r"C:\ai\Circle the Square\storyboard-frames\F01.jpg"
    image.save(out_path, quality=95)
    print(f"-> Successfully saved cartoon FLUX.2 frame to: {out_path}")

except Exception as e:
    print("FLUX.2 execution error:", e)
    traceback.print_exc()
    sys.exit(1)
