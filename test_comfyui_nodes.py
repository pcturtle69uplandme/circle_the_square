import json
import urllib.request

res = urllib.request.urlopen('http://127.0.0.1:8188/object_info')
data = json.loads(res.read().decode())
keys = list(data.keys())

checkpoints = data.get("CheckpointLoaderSimple", {}).get("input", {}).get("required", {}).get("ckpt_name", [[]])[0]
clip_models = data.get("CLIPLoader", {}).get("input", {}).get("required", {}).get("clip_name", [[]])[0]
unet_models = data.get("UNETLoader", {}).get("input", {}).get("required", {}).get("unet_name", [[]])[0]

print("Total nodes available in ComfyUI:", len(keys))
print("Available Checkpoints:", checkpoints)
print("Available CLIP models:", clip_models)
print("Available UNET models:", unet_models)
