import os
import sys
import urllib.request

url = "https://huggingface.co/SG161222/RealVisXL_V4.0/resolve/main/RealVisXL_V4.0.safetensors"
target_dir = r"C:\ai\ComfyUI\ComfyUI\models\checkpoints"
os.makedirs(target_dir, exist_ok=True)
target_path = os.path.join(target_dir, "RealVisXL_V4.0.safetensors")

print(f"Downloading full RealVisXL V4.0 SDXL checkpoint (6.46 GB)...")
print(f"Target: {target_path}")

try:
    def reporthook(blocknum, blocksize, totalsize):
        readsofar = blocknum * blocksize
        if totalsize > 0:
            percent = readsofar * 100 / totalsize
            mb_read = readsofar / (1024 * 1024)
            mb_total = totalsize / (1024 * 1024)
            sys.stdout.write(f"\rDownloading RealVisXL V4.0: {percent:5.1f}% ({mb_read:6.1f} MB / {mb_total:6.1f} MB)")
            sys.stdout.flush()

    urllib.request.urlretrieve(url, target_path, reporthook)
    print(f"\n[SUCCESS] Successfully downloaded RealVisXL V4.0 ({os.path.getsize(target_path) / (1024**3):.2f} GB)")
except Exception as e:
    print(f"\n[ERROR] Download failed: {e}")
