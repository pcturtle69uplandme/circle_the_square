import sys
import torch

try:
    from diffusers import FluxPipeline, StableDiffusionXLPipeline
    print("Diffusers Flux & SDXL imports OK!")
except ImportError as e:
    print("Diffusers import error:", e)
    sys.exit(1)

print(f"CUDA device: {torch.cuda.get_device_name(0)}")

# Test loading SDXL base from HuggingFace cache or online
try:
    print("Testing SDXL pipeline load...")
    pipe = StableDiffusionXLPipeline.from_pretrained(
        "stabilityai/stable-diffusion-xl-base-1.0",
        torch_dtype=torch.float16,
        variant="fp16"
    )
    pipe.to("cuda")
    print("SDXL loaded successfully!")
    
    prompt = "Photoreal film still, British workplace mockumentary tone, 40s corporate executive in modern glass office, 16:9 cinematic"
    img = pipe(prompt=prompt, num_inference_steps=25, guidance_scale=7.0).images[0]
    img.save(r"C:\ai\Circle the Square\test_local_sdxl.jpg")
    print("Saved test_local_sdxl.jpg!")
except Exception as e:
    print("SDXL load/gen error:", e)
