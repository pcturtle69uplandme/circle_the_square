import json
import os
import time
import urllib.request

prompt_workflow = {
    "3": {
        "inputs": {
            "seed": 118,
            "steps": 8,
            "cfg": 2.0,
            "sampler_name": "euler",
            "scheduler": "normal",
            "denoise": 1.0,
            "model": ["4", 0],
            "positive": ["6", 0],
            "negative": ["7", 0],
            "latent_image": ["5", 0]
        },
        "class_type": "KSampler"
    },
    "4": {
        "inputs": {
            "ckpt_name": "realvisxlV50_v50LightningBakedvae.safetensors"
        },
        "class_type": "CheckpointLoaderSimple"
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
            "text": (
                "Cinematic photoreal film still frame from British workplace mockumentary. "
                "40s male corporate executive sitting alone at his wooden desk in a modern executive office, "
                "flustered and sweating, loosening his dark navy necktie and unbuttoning his top shirt collar. "
                "Geometric orange triangle wall pattern in background, natural daylight, 16:9 widescreen crop."
            ),
            "clip": ["4", 1]
        },
        "class_type": "CLIPTextEncode"
    },
    "7": {
        "inputs": {
            "text": "anime, 3d render, cartoon, illustration, blurry, lowres, distorted face, extra limbs, bad anatomy, watermark",
            "clip": ["4", 1]
        },
        "class_type": "CLIPTextEncode"
    },
    "8": {
        "inputs": {
            "samples": ["3", 0],
            "vae": ["4", 2]
        },
        "class_type": "VAEDecode"
    },
    "9": {
        "inputs": {
            "filename_prefix": "F18_ComfyUI",
            "images": ["8", 0]
        },
        "class_type": "SaveImage"
    }
}

p = {"prompt": prompt_workflow}
data = json.dumps(p).encode('utf-8')
req = urllib.request.Request("http://127.0.0.1:8188/prompt", data=data, headers={'Content-Type': 'application/json'})

print("Submitting F18 render job to ComfyUI API...")
start_time = time.time()
response = urllib.request.urlopen(req)
res_data = json.loads(response.read().decode())
prompt_id = res_data["prompt_id"]
print(f"Job queued successfully! Prompt ID: {prompt_id}")

# Wait for completion
while True:
    time.sleep(0.5)
    history_req = urllib.request.urlopen(f"http://127.0.0.1:8188/history/{prompt_id}")
    history = json.loads(history_req.read().decode())
    if prompt_id in history:
        print(f"Render completed in {time.time() - start_time:.2f} seconds!")
        outputs = history[prompt_id]["outputs"]["9"]["images"]
        for img in outputs:
            filename = img["filename"]
            subfolder = img["subfolder"]
            # Copy to storyboard-frames/F18.jpg
            src_path = os.path.join(r"C:\ai\ComfyUI\ComfyUI\output", subfolder, filename)
            dst_path = r"C:\ai\Circle the Square\storyboard-frames\F18.jpg"
            if os.path.exists(src_path):
                import shutil
                shutil.copy(src_path, dst_path)
                print(f"-> Successfully saved high-res photorealistic frame to: {dst_path}")
        break
