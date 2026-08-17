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

# Reference files mapping and sync to ComfyUI input directory
comfy_input_dir = r"C:\ai\ComfyUI\ComfyUI\input"
char_refs_dir = r"C:\ai\Circle the Square\character-refs"

pending_frames = [
    {
        "id": "F18",
        "char_img": "jan_peach_cartoon_sheet.jpg",
        "prompt": f"Medium close-up. Jan Peach, CEO of PRISM, alone at his wooden desk in modern executive office, flustered and sweating profusely, begins unbuttoning his shirt. {STYLE_ANCHOR}",
        "seed": 118
    },
    {
        "id": "F19",
        "char_img": "jan_peach_cartoon_sheet.jpg",
        "prompt": f"Wide still. Jan Peach has pulled his shirt fully off, chest bared, mid-motion dropping it on his wooden executive desk in modern executive office, red flushed skin, comedic visual gag beat. {STYLE_ANCHOR}",
        "seed": 119
    },
    {
        "id": "F20",
        "char_img": "jan_peach_cartoon_sheet.jpg",
        "prompt": f"Wide still. Modern glass office door has just opened — Sharon Enfield walks in without knocking. Jan Peach, shirtless at his desk, spins toward her in alarm. {STYLE_ANCHOR}",
        "seed": 120
    },
    {
        "id": "F21",
        "char_img": "sharon_enfield_cartoon_sheet.jpg",
        "prompt": f"Medium close-up on Sharon Enfield in emerald green blouse, her eyes flicking briefly down toward Jan's chest, expression staying completely neutral. {STYLE_ANCHOR}",
        "seed": 121
    },
    {
        "id": "F22",
        "char_img": "jan_peach_cartoon_sheet.jpg",
        "prompt": f"Medium close-up on Jan Peach shirtless in executive office, frozen in mortified realisation and embarrassed posture. {STYLE_ANCHOR}",
        "seed": 122
    },
    {
        "id": "F23",
        "char_img": "sharon_enfield_cartoon_sheet.jpg",
        "prompt": f"Medium close-up on Sharon Enfield in emerald green blouse, flat and transactional, speaking calmly in modern executive office. {STYLE_ANCHOR}",
        "seed": 123
    },
    {
        "id": "F24",
        "char_img": "jan_peach_cartoon_sheet.jpg",
        "prompt": f"Medium close-up on flustered Jan Peach half-undressed waving hand defensively at female colleague in modern executive office. {STYLE_ANCHOR}",
        "seed": 124
    },
    {
        "id": "F25",
        "char_img": "sharon_enfield_cartoon_sheet.jpg",
        "prompt": f"Medium close-up on Sharon Enfield in emerald green blouse with arms crossed, calm composed posture, flat and matter-of-fact. {STYLE_ANCHOR}",
        "seed": 125
    },
    {
        "id": "F26a",
        "char_img": "jan_peach_cartoon_sheet.jpg",
        "prompt": f"Medium close-up of Jan Peach yanking venetian window blinds closed with both hands in modern glass executive office. {STYLE_ANCHOR}",
        "seed": 126
    },
    {
        "id": "F26b",
        "char_img": "jan_peach_cartoon_sheet.jpg",
        "prompt": f"Close-up of hand turning door lock knob on modern office glass door. {STYLE_ANCHOR}",
        "seed": 127
    }
]

# Ensure input sheets exist in ComfyUI input folder if available
if os.path.exists(comfy_input_dir):
    for item in pending_frames:
        src = os.path.join(char_refs_dir, item["char_img"])
        dst = os.path.join(comfy_input_dir, item["char_img"])
        if os.path.exists(src) and not os.path.exists(dst):
            shutil.copy(src, dst)

out_dir = r"C:\ai\Circle the Square\storyboard-frames"
os.makedirs(out_dir, exist_ok=True)

print(f"Starting batch cartoon IP-Adapter character-locked rendering for {len(pending_frames)} frames...")

for item in pending_frames:
    workflow = {
        "1": {
            "inputs": {
                "image": item["char_img"]
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
                "text": item["prompt"],
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
                "seed": item["seed"],
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
                "filename_prefix": f"Cartoon_IPAdapter_{item['id']}",
                "images": ["9", 0]
            },
            "class_type": "SaveImage"
        }
    }

    p = {"prompt": workflow}
    data = json.dumps(p).encode('utf-8')
    req = urllib.request.Request("http://127.0.0.1:8188/prompt", data=data, headers={'Content-Type': 'application/json'})

    print(f"\n--- Submitting {item['id']} ({item['char_img']}) ---")
    start_time = time.time()
    response = urllib.request.urlopen(req)
    res_data = json.loads(response.read().decode())
    prompt_id = res_data["prompt_id"]

    while True:
        time.sleep(1.0)
        history_req = urllib.request.urlopen(f"http://127.0.0.1:8188/history/{prompt_id}")
        history = json.loads(history_req.read().decode())
        if prompt_id in history:
            duration = time.time() - start_time
            outputs = history[prompt_id]["outputs"]
            if "10" in outputs and "images" in outputs["10"]:
                for img in outputs["10"]["images"]:
                    filename = img["filename"]
                    subfolder = img["subfolder"]
                    src_path = os.path.join(r"C:\ai\ComfyUI\ComfyUI\output", subfolder, filename)
                    dst_path = os.path.join(out_dir, f"{item['id']}.jpg")
                    if os.path.exists(src_path):
                        shutil.copy(src_path, dst_path)
                        print(f"[SUCCESS] Saved cartoon character-locked {item['id']} ({duration:.1f}s) -> {dst_path}")
            else:
                print(f"[ERROR] Output error for {item['id']}:", outputs)
            break

print("\n[COMPLETE] All Scene 1 cartoon character-locked frames rendered successfully!")
