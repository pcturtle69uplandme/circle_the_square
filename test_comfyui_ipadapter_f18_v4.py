import json
import os
import time
import urllib.request
import shutil

workflow = {
    "1": {
        "inputs": {
            "image": "jan_peach_identity_sheet.jpg"
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
            "filename_prefix": "F18_IPAdapter_Jan_V4",
            "images": ["9", 0]
        },
        "class_type": "SaveImage"
    }
}

p = {"prompt": workflow}
data = json.dumps(p).encode('utf-8')
req = urllib.request.Request("http://127.0.0.1:8188/prompt", data=data, headers={'Content-Type': 'application/json'})

print("Submitting character-locked IP-Adapter render job for Frame F18...")
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
        print(f"Character-locked render completed in {time.time() - start_time:.2f} seconds!")
        outputs = history[prompt_id]["outputs"]
        if "10" in outputs and "images" in outputs["10"]:
            for img in outputs["10"]["images"]:
                filename = img["filename"]
                subfolder = img["subfolder"]
                src_path = os.path.join(r"C:\ai\ComfyUI\ComfyUI\output", subfolder, filename)
                dst_path = r"C:\ai\Circle the Square\storyboard-frames\F18.jpg"
                if os.path.exists(src_path):
                    shutil.copy(src_path, dst_path)
                    print(f"🎉 Successfully saved character-locked frame F18 to: {dst_path}")
        else:
            print("Outputs:", outputs)
        break
