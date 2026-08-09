import os

dirs_to_search = [r"C:\ai", r"C:\Users\konti\.cache"]

found = []
for base in dirs_to_search:
    for root, _, files in os.walk(base):
        for f in files:
            if f.endswith(('.safetensors', '.ckpt', '.bin', '.pth')):
                path = os.path.join(root, f)
                try:
                    size_gb = os.path.getsize(path) / (1024**3)
                    if size_gb > 0.5: # larger than 500MB
                        found.append((path, size_gb))
                except Exception:
                    pass

found.sort(key=lambda x: x[1], reverse=True)
print("Found checkpoints/models (>500MB):")
for path, size in found:
    print(f"  {size:.2f} GB : {path}")
