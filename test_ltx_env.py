import sys
import torch

print("Python:", sys.version)
print("CUDA:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("GPU:", torch.cuda.get_device_name(0))
    print("VRAM Free (GB):", torch.cuda.mem_get_info()[0] / 1024**3)
    print("VRAM Total (GB):", torch.cuda.mem_get_info()[1] / 1024**3)

try:
    from diffusers import LTXPipeline, LTXImageToVideoPipeline
    print("Diffusers LTX import successful!")
except ImportError as e:
    print("Diffusers import error:", e)

try:
    import comfy
    print("Comfy package available!")
except ImportError as e:
    print("Comfy import error:", e)
