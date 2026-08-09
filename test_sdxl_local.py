import sys
import torch

try:
    from diffusers import StableDiffusionXLPipeline, EulerDiscreteScheduler
except ImportError as e:
    print("Diffusers SDXL import error:", e)
    sys.exit(1)

model_path = r"C:\ai\ComfyUI\realvisxlV50_v50LightningBakedvae.safetensors"
print(f"Testing SDXL model load from: {model_path}")
print(f"GPU: {torch.cuda.get_device_name(0)}")

try:
    pipe = StableDiffusionXLPipeline.from_single_file(
        model_path,
        torch_dtype=torch.float16,
        use_safetensors=True
    )
    pipe.to("cuda")
    print("RealVisXL V5.0 Lightning SDXL model loaded successfully into VRAM!")
except Exception as e:
    print("SDXL model load error:", e)
    sys.exit(1)
