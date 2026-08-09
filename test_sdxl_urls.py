import urllib.request

urls = [
    ("RealVisXL V4.0", "https://huggingface.co/SG161222/RealVisXL_V4.0/resolve/main/RealVisXL_V4.0.safetensors"),
    ("RealVisXL V5.0", "https://huggingface.co/SG161222/RealVisXL_V5.0/resolve/main/RealVisXL_V5.0.safetensors"),
    ("SDXL Base 1.0", "https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/sd_xl_base_1.0.safetensors"),
    ("SDXL Lightning 8-step", "https://huggingface.co/ByteDance/SDXL-Lightning/resolve/main/sdxl_lightning_8step_unet.safetensors")
]

for name, url in urls:
    try:
        req = urllib.request.Request(url, method='HEAD')
        res = urllib.request.urlopen(req)
        print(f"[FOUND] {name}: Status {res.status}, Size: {int(res.headers.get('Content-Length', 0))/(1024**3):.2f} GB")
    except Exception as e:
        print(f"[NOT FOUND] {name}: {e}")
