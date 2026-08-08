import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

base_dir = r"C:\ai\Circle the Square"

# 1. Load Real Office Background Photo (Faceted Orange Desk & Triangle Wall)
bg_path = os.path.join(base_dir, "building-reference", "use-images", "IMG_20260804_131855397.jpg")
bg_img = Image.open(bg_path).convert('RGBA')

# Target resolution: 1920x1080 (16:9 cinematic)
bg_img = bg_img.resize((1920, 1080), Image.Resampling.LANCZOS)

# 2. Load Character Identity Sheets (Size: 1376x768)
jan_sheet = Image.open(os.path.join(base_dir, "character-refs", "jan_peach_identity_sheet.jpg")).convert('RGBA')
christina_sheet = Image.open(os.path.join(base_dir, "character-refs", "christina_dross_identity_sheet.jpg")).convert('RGBA')
sharon_sheet = Image.open(os.path.join(base_dir, "character-refs", "sharon_enfield_identity_sheet.jpg")).convert('RGBA')
chris_sheet = Image.open(os.path.join(base_dir, "character-refs", "chris_identity_sheet.jpg")).convert('RGBA')
rick_sheet = Image.open(os.path.join(base_dir, "character-refs", "rick_identity_sheet.jpg")).convert('RGBA')

# Function to extract human turnaround figure cutout with soft oval background fade
def extract_photoreal_human(sheet_img, crop_box, target_size):
    crop = sheet_img.crop(crop_box)
    crop = crop.resize(target_size, Image.Resampling.LANCZOS)
    
    # Create subtle vignette alpha mask around the photorealistic figure
    mask = Image.new('L', target_size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse([0, 0, target_size[0], target_size[1]], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(12))
    
    crop.putalpha(mask)
    return crop

# Extract photorealistic character figures from the right side of each sheet (700 -> 1350)
jan_figure = extract_photoreal_human(jan_sheet, (720, 40, 1320, 720), (450, 520))
christina_figure = extract_photoreal_human(christina_sheet, (720, 40, 1320, 720), (380, 440))
sharon_figure = extract_photoreal_human(sharon_sheet, (720, 40, 1320, 720), (380, 440))
chris_figure = extract_photoreal_human(chris_sheet, (720, 40, 1320, 720), (360, 420))
rick_figure = extract_photoreal_human(rick_sheet, (720, 40, 1320, 720), (360, 420))

# 3. Create Composite Canvas
canvas = bg_img.copy()

# Add subtle dark ambient vignette to ground characters into room lighting
vignette = Image.new('RGBA', (1920, 1080), (11, 13, 18, 90))
canvas = Image.alpha_composite(canvas, vignette)

# STAGING CHARACTERS IN THE ATRIUM RECEPTION LOBBY

# (A) Background Center: Rick & Chris Goofing Around
canvas.paste(rick_figure, (920, 310), rick_figure)
canvas.paste(chris_figure, (1120, 320), chris_figure)

# (B) Center-Left: Sharon Enfield Glaring (Operations)
canvas.paste(sharon_figure, (240, 360), sharon_figure)

# (C) Far-Right: Christina Dross Powdering Face (Strategy)
canvas.paste(christina_figure, (1400, 360), christina_figure)

# (D) Center Front Hero: Jan Peach CEO Screaming Rage
canvas.paste(jan_figure, (720, 380), jan_figure)

# 4. Draw Cinematic Overlays & Badges
overlay = ImageDraw.Draw(canvas, 'RGBA')

# Burnt-Orange Letterbox Framing (2.39:1 Cinema Crop)
overlay.rectangle([0, 0, 1920, 95], fill=(11, 13, 18, 240))
overlay.rectangle([0, 985, 1920, 1080], fill=(11, 13, 18, 240))

# Gold/Orange Accent Lines
overlay.line([(0, 95), (1920, 95)], fill=(176, 56, 31, 255), width=4)
overlay.line([(0, 985), (1920, 985)], fill=(176, 56, 31, 255), width=4)

# Text Header
overlay.text((60, 25), "CIRCLE THE SQUARE — SHOT S58.5 GROUPSHOOT STINGER (PHOTOREAL COMPOSITE)", fill=(242, 163, 77, 255))
overlay.text((60, 55), "ENVIRONMENT: Real Office Atrium Plate (IMG_20260804_131855397) • CHARACTERS: Photorealistic Identity Sheet Turnarounds", fill=(244, 243, 239, 220))

# Character Name Badges
def draw_badge(x, y, name, text_color='#F2A34D'):
    overlay.rectangle([x, y, x + 220, y + 34], fill=(11, 13, 18, 230), outline=(176, 56, 31, 255))
    overlay.text((x + 12, y + 8), name, fill=text_color)

draw_badge(280, 810, "SHARON (Operations Glare)")
draw_badge(750, 890, "JAN PEACH (CEO Rage)", '#EF4444')
draw_badge(940, 710, "RICK (Security Bunny-Ears)")
draw_badge(1140, 720, "CHRIS (Staff Stress Ball)")
draw_badge(1420, 800, "CHRISTINA (Compact Lipstick)")

# Save Final Photorealistic Composite Image
final_img = canvas.convert('RGB')
output_path = os.path.join(base_dir, "photorealistic_opening_stinger.jpg")
final_img.save(output_path, "JPEG", quality=98)
print(f"Successfully generated refined photorealistic composite: {output_path}")
