import os
import sys
from PIL import Image, ImageFilter, ImageEnhance

def upscale_image(src_path, dst_path, scale=2.0, sharpen=True):
    if not os.path.exists(src_path):
        print(f"Source file not found: {src_path}")
        return False
    
    img = Image.open(src_path).convert("RGB")
    orig_w, orig_h = img.size
    new_w = int(orig_w * scale)
    new_h = int(orig_h * scale)
    
    print(f"Upscaling {src_path} from {orig_w}x{orig_h} -> {new_w}x{new_h} ({scale}x)...")
    
    # Lanczos high-quality resample
    upscaled = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    if sharpen:
        # Edge-preserving subtle sharpness boost tailored for comic line art
        enhancer = ImageEnhance.Sharpness(upscaled)
        upscaled = enhancer.enhance(1.3)
    
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    upscaled.save(dst_path, quality=98, subsampling=0)
    print(f"[SUCCESS] Saved upscaled frame to: {dst_path}")
    return True

if __name__ == "__main__":
    src = r"C:\ai\Circle the Square\storyboard-frames\F01.jpg"
    dst_2k = r"C:\ai\Circle the Square\storyboard-frames\F01_2K.jpg"
    dst_4k = r"C:\ai\Circle the Square\storyboard-frames\F01_4K.jpg"
    
    # 2K upscale (2752x1536)
    upscale_image(src, dst_2k, scale=2.0)
    
    # 4K upscale (3840x2144)
    upscale_image(src, dst_4k, scale=2.79)
