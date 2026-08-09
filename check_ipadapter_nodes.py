import json
import urllib.request

res = urllib.request.urlopen('http://127.0.0.1:8188/object_info')
data = json.loads(res.read().decode())

ipadapter_nodes = [k for k in data.keys() if 'ipadapter' in k.lower() or 'pulid' in k.lower()]
print("Found IP-Adapter & PuLID nodes in ComfyUI:")
for n in ipadapter_nodes:
    print(" -", n)

ip_models = data.get("IPAdapterModelLoader", {}).get("input", {}).get("required", {}).get("ipadapter_file", [[]])[0]
clip_vision_models = data.get("CLIPVisionLoader", {}).get("input", {}).get("required", {}).get("clip_name", [[]])[0]

print("\nAvailable IPAdapter models:", ip_models)
print("Available CLIP Vision models:", clip_vision_models)
