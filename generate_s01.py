"""
Circle the Square — S01 Video Generator
Shot: S01 — Jan's Office Establishing Wide
Duration: 6 seconds
Model: veo-2.0-generate-001

INSTRUCTIONS:
1. Go to https://aistudio.google.com/apikey
2. Create a new API key (or use existing one that has Veo 2 access)
3. Paste your key into the API_KEY variable below
4. Run: python generate_s01.py
5. Video will be saved to: clips/S01_office_establishing.mp4

GATE CHECK after watching the clip:
  - Orange faceted desk & triangle wall visible in background?
  - Jan reads as 50s, overweight, CEO-type in navy suit?
  - Christina reads as professional, poised female executive?
  - Lighting warm indoor, not cold/sterile?
If YES to all → rename status in featurette_prompt_engine.md to APPROVED, run generate_s02.py
If NO → update STYLE_ANCHOR or PROMPT below, re-run this script
"""

import os
import time
import urllib.request
from google import genai
from google.genai import types

# ============================================================
# PASTE YOUR VEO-2-ENABLED API KEY FROM AI STUDIO HERE:
API_KEY = "PASTE_YOUR_AI_STUDIO_API_KEY_HERE"
# ============================================================

STYLE_ANCHOR = """
Photoreal cinematic 35mm footage. Modern UK corporate office building interior.
Warm cream/sand brick and pale concrete architecture. Fair-faced grey concrete columns.
Full-height glazing with natural Northern European daylight. Oak/timber slat joinery accents.
Grey carpet tile floors. No lens flare. No visible real-world branding or crests.
Documentary-style handheld camera. British corporate mockumentary tone.
Shallow depth of field on close-ups, deep focus on wide/establishing shots.
2.39:1 cinematic widescreen aspect ratio.
"""

PROMPT = f"""
A locked-off wide shot of a modern UK corporate glass-walled office. A 52-year-old overweight
male CEO in a dark navy suit sits behind a desk with a smug thin-lipped expression, fingers
steepled. Opposite him stands a 38-year-old female executive in a charcoal blazer and cream
blouse, posture upright and composed, holding a tablet. They are mid-conversation. The background
features a faceted ochre-orange reception desk and a striking black-and-white geometric triangle
pattern wall. Warm office interior lighting. Static wide shot, 6 seconds.
{STYLE_ANCHOR}
"""

REFERENCE_IMAGES = [
    r"C:\ai\Circle the Square\building-reference\use-images\IMG_20260804_131855397.jpg",
    r"C:\ai\Circle the Square\character-refs\jan_peach_identity_sheet.jpg",
]

OUTPUT_DIR = r"C:\ai\Circle the Square\clips"
OUTPUT_FILE = r"C:\ai\Circle the Square\clips\S01_office_establishing.mp4"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_image(path):
    with open(path, "rb") as f:
        data = f.read()
    ext = path.lower().split(".")[-1]
    mime = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png"}.get(ext, "image/jpeg")
    return types.Part.from_bytes(data=data, mime_type=mime)

def main():
    client = genai.Client(api_key=API_KEY)

    print("=" * 60)
    print("CIRCLE THE SQUARE — S01 VIDEO GENERATOR")
    print("Shot: Jan's Office Establishing Wide (6 seconds)")
    print("=" * 60)

    # Load reference images
    print("\nLoading reference images...")
    image_parts = []
    for img_path in REFERENCE_IMAGES:
        if os.path.exists(img_path):
            image_parts.append(load_image(img_path))
            print(f"  ✅ Loaded: {os.path.basename(img_path)}")
        else:
            print(f"  ⚠️  Not found (skipping): {img_path}")

    # Build source from images + prompt
    print("\nSubmitting to Veo 2...")

    # Use the new source-based API
    source_images = [
        types.VideoGenerationSource(image=part) for part in image_parts
    ] if image_parts else None

    operation = client.models.generate_videos(
        model="veo-2.0-generate-001",
        prompt=PROMPT,
        config=types.GenerateVideosConfig(
            duration_seconds=6,
            aspect_ratio="16:9",
            number_of_videos=1,
        ),
    )

    print(f"  ✅ Operation submitted: {operation.name}")
    print("\nWaiting for generation to complete (this takes 2-5 minutes)...")

    # Poll until complete
    while not operation.done:
        print("  ⏳ Still generating...", flush=True)
        time.sleep(15)
        operation = client.operations.get(operation)

    if operation.response and operation.response.generated_videos:
        video = operation.response.generated_videos[0]
        video_uri = video.video.uri

        print(f"\n  ✅ Video ready: {video_uri}")
        print(f"  ⬇️  Downloading to: {OUTPUT_FILE}")

        # Download the video
        urllib.request.urlretrieve(video_uri, OUTPUT_FILE)
        print(f"\n✅ SAVED: {OUTPUT_FILE}")
        print("\n" + "=" * 60)
        print("GATE CHECK — Watch the clip and verify:")
        print("  [ ] Orange faceted desk & triangle wall visible?")
        print("  [ ] Jan reads as 50s, overweight, navy suit CEO?")
        print("  [ ] Christina reads as professional, poised?")
        print("  [ ] Warm indoor lighting, not cold/sterile?")
        print("=" * 60)
        print("\nIf ALL PASS → update S01 status to APPROVED in featurette_prompt_engine.md")
        print("             → then run: python generate_s02.py")
        print("If FAIL     → edit PROMPT or STYLE_ANCHOR in this file → re-run")
    else:
        print("\n❌ Generation failed or returned no video.")
        if operation.error:
            print(f"   Error: {operation.error}")

if __name__ == "__main__":
    main()
