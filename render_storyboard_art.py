import os
from PIL import Image, ImageDraw, ImageFont

# Canvas dimensions (16:9 4K resolution)
width, height = 1920, 1080
img = Image.new('RGB', (width, height), color='#0B0D12')
draw = ImageDraw.Draw(img, 'RGBA')

# Color Palette
burnt_orange = '#B0381F'
amber_gold = '#F2A34D'
ink_navy = '#141722'
slate_grey = '#64748B'
bone_white = '#F4F3EF'

# Draw Background Atrium & Triangle Wall
# Top wall gradient grid
for i in range(0, width, 80):
    draw.line([(i, 0), (i, 600)], fill=(100, 116, 139, 40), width=1)
for j in range(0, 600, 60):
    draw.line([(0, j), (width, j)], fill=(100, 116, 139, 40), width=1)

# Large Geometric Triangle Feature Wall (Center Background)
triangles = [
    [(960, 120), (840, 320), (1080, 320)],
    [(840, 320), (720, 520), (960, 520)],
    [(1080, 320), (960, 520), (1200, 520)],
    [(960, 320), (840, 520), (1080, 520)],
    [(720, 320), (600, 520), (840, 520)],
    [(1200, 320), (1080, 520), (1320, 520)],
]

for idx, tri in enumerate(triangles):
    color = (176, 56, 31, 180) if idx % 2 == 0 else (242, 163, 77, 160)
    draw.polygon(tri, fill=color, outline=(244, 243, 239, 100))

# Faceted Orange Reception Desk (Foreground Center)
desk_points = [(520, 680), (1400, 680), (1300, 920), (620, 920)]
draw.polygon(desk_points, fill=(176, 56, 31, 240), outline=(242, 163, 77, 255))

# Draw Desk Highlight Facets
facet_line = [(620, 920), (850, 780), (1400, 680)]
draw.line(facet_line, fill=(244, 243, 239, 150), width=3)

# CHARACTERS STAGING & SILHOUETTE ARTWORK

# 1. TREVOR (Far Left - Blank Motionless Stare)
draw.ellipse([260, 480, 360, 580], fill=(71, 85, 105, 255), outline=bone_white)
draw.rectangle([250, 580, 370, 880], fill=(51, 65, 85, 255))
# Messenger Bag Strap
draw.line([(270, 580), (360, 760)], fill=burnt_orange, width=6)

# 2. SHARON ENFIELD (Center-Left - Arms Crossed Glare)
draw.ellipse([580, 470, 680, 570], fill=(21, 128, 61, 255), outline=bone_white)
draw.rectangle([570, 570, 690, 780], fill=(22, 101, 52, 255))
# Crossed Arms
draw.line([(550, 630), (710, 630)], fill=bone_white, width=12)

# 3. JAN PEACH (CEO Center Front - Screaming Rage)
draw.ellipse([880, 430, 1040, 590], fill=(239, 68, 68, 255), outline=(255, 255, 255, 255))
draw.rectangle([840, 590, 1080, 840], fill=(27, 36, 54, 255))
# Screaming Mouth
draw.ellipse([935, 525, 985, 565], fill=(15, 23, 42, 255))
# Clenched Fists
draw.ellipse([800, 700, 850, 750], fill=(239, 68, 68, 255), outline=bone_white)
draw.ellipse([1070, 700, 1120, 750], fill=(239, 68, 68, 255), outline=bone_white)

# 4. CHRIS & RICK (Background Center - Bunny Ears & Stress Ball)
# Rick (Security Uniform)
draw.ellipse([1100, 430, 1190, 520], fill=(30, 58, 138, 255))
draw.rectangle([1090, 520, 1200, 680], fill=(30, 41, 59, 255))
# Chris (Grey Polo)
draw.ellipse([1210, 440, 1290, 520], fill=(59, 130, 246, 255))
draw.rectangle([1200, 520, 1300, 680], fill=(71, 85, 105, 255))
# Bunny Ears behind Chris
draw.line([(1230, 420), (1220, 360)], fill=bone_white, width=8)
draw.line([(1250, 420), (1260, 360)], fill=bone_white, width=8)

# 5. CHRISTINA DROSS (Far Right - Compact Mirror Lipstick)
draw.ellipse([1520, 470, 1620, 570], fill=(203, 213, 225, 255), outline=bone_white)
draw.rectangle([1510, 570, 1630, 840], fill=(43, 46, 51, 255))
# Compact Mirror in hand
draw.ellipse([1450, 520, 1490, 560], fill=amber_gold, outline=bone_white)

# TRIPOD LOCK 35mm OVERLAY FRAME
draw.rectangle([60, 60, width - 60, height - 60], fill=None, outline=(176, 56, 31, 255), width=6)

# Labels & Header Overlay
draw.rectangle([60, 60, 700, 130], fill=(11, 13, 18, 230))
draw.text((80, 75), "CIRCLE THE SQUARE — SHOT S58.5 GROUPSHOOT STINGER", fill=amber_gold)
draw.text((80, 100), "CAM: Tripod Lock 35mm (2.39:1 Aspect Ratio) • Prism Atrium Lobby", fill=bone_white)

# Save high-res PNG image
output_path = os.path.join(r"C:\kontitemp\ai\circle_the_square", "storyboard_group_photo_render.png")
img.save(output_path, "PNG")
print(f"Successfully generated image: {output_path}")
