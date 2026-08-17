import json
import os
import time
import urllib.request
import shutil

STYLE_ANCHOR = (
    "Stylised British sitcom comic art, clean bold line art, flat muted colour palette, "
    "expressive caricature, cel-shaded, 16:9 widescreen crop. NOT photorealistic. "
    "Absolutely NO text, NO speech bubbles, NO captions, NO labels, NO sound effects, "
    "NO lettering of any kind anywhere in the image."
)

NEGATIVE_PROMPT = (
    "photorealistic, 3d render, realistic photograph, photo, realistic skin texture, "
    "blurry, lowres, distorted face, extra limbs, bad anatomy, text, watermark, signature, "
    "speech bubbles, captions, lettering"
)

# Ensure reference image is in ComfyUI input directory if directory exists
comfy_input_dir = r"C:\ai\ComfyUI\ComfyUI\input"
ref_src = r"C:\ai\Circle the Square\character-refs\jan_peach_cartoon_sheet.jpg"
ref_name = "jan_peach_cartoon_sheet.jpg"
if os.path.exists(comfy_input_dir) and os.path.exists(ref_src):
    shutil.copy(ref_src, os.path.join(comfy_input_dir, ref_name))

workflow = {
    "1": {
        "inputs": {
            "image": ref_name
        },
        "class_type": "LoadImage"
    },
    "4": {
        "inputs": {
            "ckpt_name": "RealVisXL_V4.0.safetensors"
        },
        "class_type": "CheckpointLoaderSimple"
    },
    "2": {
        "inputs": {
            "preset": "PLUS (high strength)",
            "model": ["4", 0]
        },
        "class_type": "IPAdapterUnifiedLoader"
    },
    "3": {
        "inputs": {
            "weight": 0.80,
            "weight_type": "linear",
            "combine_embeds": "concat",
            "start_at": 0.0,
            "end_at": 1.0,
            "embeds_scaling": "V only",
            "model": ["2", 0],
            "ipadapter": ["2", 1],
            "image": ["1", 0]
        },
        "class_type": "IPAdapterAdvanced"
    },
    "5": {
        "inputs": {
            "width": 1024,
            "height": 576,
            "batch_size": 1
        },
        "class_type": "EmptyLatentImage"
    },
    "6": {
        "inputs": {
            "text": f"Medium close-up. Jan Peach, CEO of PRISM, alone at his wooden desk in modern executive office, flustered and sweating profusely, begins unbuttoning his shirt. {STYLE_ANCHOR}",
            "clip": ["4", 1]
        },
        "class_type": "CLIPTextEncode"
    },
    "7": {
        "inputs": {
            "text": NEGATIVE_PROMPT,
            "clip": ["4", 1]
        },
        "class_type": "CLIPTextEncode"
    },
    "8": {
        "inputs": {
            "seed": 118,
            "steps": 25,
            "cfg": 6.5,
            "sampler_name": "dpmpp_2m",
            "scheduler": "karras",
            "denoise": 1.0,
            "model": ["3", 0],
            "positive": ["6", 0],
            "negative": ["7", 0],
            "latent_image": ["5", 0]
        },
        "class_type": "KSampler"
    },
    "9": {
        "inputs": {
            "samples": ["8", 0],
            "vae": ["4", 2]
        },
        "class_type": "VAEDecode"
    },
    "10": {
        "inputs": {
            "filename_prefix": "F18_Cartoon_IPAdapter_Jan",
            "images": ["9", 0]
        },
        "class_type": "SaveImage"
    }
}

p = {"prompt": workflow}
data = json.dumps(p).encode('utf-8')
req = urllib.request.Request("http://127.0.0.1:8188/prompt", data=data, headers={'Content-Type': 'application/json'})

print("Submitting cartoon character-locked IP-Adapter render job for Frame F18...")
start_time = time.time()
response = urllib.request.urlopen(req)
res_data = json.loads(response.read().decode())
prompt_id = res_data["prompt_id"]
print(f"Job queued! Prompt ID: {prompt_id}")

while True:
    time.sleep(1.0)
    history_req = urllib.request.urlopen(f"http://127.0.0.1:8188/history/{prompt_id}")
    history = json.loads(history_req.read().decode())
    if prompt_id in history:
        print(f"Cartoon character-locked render completed in {time.time() - start_time:.2f} seconds!")
        outputs = history[prompt_id]["outputs"]
        if "10" in outputs and "images" in outputs["10"]:
            for img in outputs["10"]["images"]:
                filename = img["filename"]
                subfolder = img["subfolder"]
                src_path = os.path.join(r"C:\ai\ComfyUI\ComfyUI\output", subfolder, filename)
                dst_path = r"C:\ai\Circle the Square\storyboard-frames\F18.jpg"
                if os.path.exists(src_path):
                    shutil.copy(src_path, dst_path)
                    print(f"[SUCCESS] Saved cartoon character-locked frame F18 to: {dst_path}")
        else:
            print("Outputs:", outputs)
        break
