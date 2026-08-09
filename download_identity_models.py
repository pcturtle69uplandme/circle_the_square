import os
import sys
import urllib.request

models_to_download = [
    {
        "name": "PuLID / IP-Adapter CLIP-Vision Encoder (CLIP-ViT-H-14)",
        "url": "https://huggingface.co/h94/IP-Adapter/resolve/main/models/image_encoder/model.safetensors",
        "dir": r"C:\ai\ComfyUI\ComfyUI\models\clip_vision",
        "filename": "CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors"
    },
    {
        "name": "IP-Adapter Plus SDXL",
        "url": "https://huggingface.co/h94/IP-Adapter/resolve/main/sdxl_models/ip-adapter-plus_sdxl_vit-h.safetensors",
        "dir": r"C:\ai\ComfyUI\ComfyUI\models\ipadapter",
        "filename": "ip-adapter-plus_sdxl_vit-h.safetensors"
    }
]

def download_file(item):
    os.makedirs(item["dir"], exist_ok=True)
    dst_path = os.path.join(item["dir"], item["filename"])
    
    if os.path.exists(dst_path) and os.path.getsize(dst_path) > 100_000_000:
        print(f"[SKIP] {item['name']} already exists at: {dst_path}")
        return True

    print(f"\n--- Downloading {item['name']} ---")
    print(f"URL: {item['url']}")
    print(f"Target: {dst_path}")

    try:
        def reporthook(blocknum, blocksize, totalsize):
            readsofar = blocknum * blocksize
            if totalsize > 0:
                percent = readsofar * 100 / totalsize
                mb_read = readsofar / (1024 * 1024)
                mb_total = totalsize / (1024 * 1024)
                sys.stdout.write(f"\rDownloading: {percent:5.1f}% ({mb_read:6.1f} MB / {mb_total:6.1f} MB)")
                sys.stdout.flush()

        urllib.request.urlretrieve(item["url"], dst_path, reporthook)
        print(f"\n[SUCCESS] Successfully downloaded {item['name']} ({os.path.getsize(dst_path) / (1024*1024):.1f} MB)")
        return True
    except Exception as e:
        print(f"\n[ERROR] Error downloading {item['name']}: {e}")
        return False

def main():
    print("Starting download of PuLID-FLUX and IP-Adapter local identity models...")
    success = True
    for item in models_to_download:
        ok = download_file(item)
        if not ok:
            success = False
    
    if success:
        print("\n[COMPLETE] ALL LOCAL IDENTITY CONDITIONING MODELS DOWNLOADED SUCCESSFULLY!")
    else:
        print("\n[WARNING] One or more downloads failed. Check log output.")

if __name__ == "__main__":
    main()
