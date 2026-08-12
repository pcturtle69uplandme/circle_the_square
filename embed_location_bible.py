"""Add the second Flow batch (project f2f0d2c9, 2026-08-12) to the location bible.

1. Copies new cartoon plates into location-refs/cartoon-plates/ (FLOW2_ prefix)
2. Appends them to PLATES_MANIFEST.md
3. Inserts a gallery section into location-bible.html
4. Embeds every local image in location-bible.html as base64 (self-contained)
"""
import base64
import os
import re
import shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
DL = os.path.join(ROOT, "character-refs", "flow_downloads")
PLATES = os.path.join(ROOT, "location-refs", "cartoon-plates")
HTML = os.path.join(ROOT, "location-bible.html")
MANIFEST = os.path.join(PLATES, "PLATES_MANIFEST.md")

# src file -> (new name, description)
EXTERIORS = [
    ("grid_33_1cb1fcf1.jpg", "FLOW2_courtyard_dusk_clean.jpg", "Entrance courtyard at dusk, lit glazing, glowing tower - clean plate, no people"),
    ("grid_34_802a4a55.jpg", "FLOW2_plaza_day_tower.jpg", "Wide plaza day view, brick blocks, tower behind, overcast"),
    ("grid_35_8871dab3.jpg", "FLOW2_courtyard_garden_day.jpg", "Landscaped courtyard garden, hedges, picnic tables, day"),
    ("grid_36_d39d6e87.jpg", "FLOW2_garden_pines_fin_facade.jpg", "Garden courtyard with pines and planted mound, colourful fin facade"),
    ("grid_37_45c496b5.jpg", "FLOW2_corner_street_keepclear.jpg", "Street-level corner view of brick block, KEEP CLEAR road marking, day"),
    ("grid_38_99a7289c.jpg", "FLOW2_corner_low_angle_day.jpg", "Low-angle worm's-eye corner shot of brick building against sky, day"),
    ("grid_39_49a529eb.jpg", "FLOW2_curved_building_day.jpg", "Curved brick building from street, trees, CCTV pole, day"),
    ("grid_40_f453f72f.jpg", "FLOW2_aerial_complex_day.jpg", "Aerial top-down of whole complex, yellow tower, railway tracks, day"),
    ("grid_41_d9cd8508.jpg", "FLOW2_billboard_railway_winter.jpg", "Curved building behind blue crest billboard, tram tracks, bare winter trees, overcast"),
    ("grid_42_32b07252.jpg", "FLOW2_railway_dusk_tower.jpg", "Street view at dusk, tram tracks foreground, lit tower, pink cloud"),
]
INTERIORS = [
    ("grid_19_22e481a4.jpg", "FLOW2_int_jans_office_day.jpg", "Executive office, geometric triangle feature wall, railway + houses through window, day"),
    ("grid_20_d0207e51.jpg", "FLOW2_int_breakout_foosball_mezz.jpg", "Games/breakout mezzanine, foosball + arcade machine, atrium behind"),
    ("grid_21_df9fa4e1.jpg", "FLOW2_int_corridor_phone_bar.jpg", "Open office corridor with phone bar, stools, wall display"),
    ("grid_22_5bae45cf.jpg", "FLOW2_int_meeting_room_glass.jpg", "Glass-walled meeting room with dotted manifestation, empty"),
    ("grid_23_755783bc.jpg", "FLOW2_int_corridor_lockers.jpg", "Corridor with lockers and plants, distant figure"),
    ("grid_24_9e1ec1a5.jpg", "FLOW2_int_open_plan_day.jpg", "Open-plan office floor, bench tables, lockers, windows, day"),
    ("grid_25_34399243.jpg", "FLOW2_int_open_plan_triangle_wall.jpg", "Open-plan office, long desks with lamps, red/black triangle acoustic wall"),
    ("grid_26_ceb1218a.jpg", "FLOW2_int_atrium_revolving_doors.jpg", "Atrium/reception with revolving doors, turnstiles, brick columns, day"),
    ("grid_27_91bbc72f.jpg", "FLOW2_int_atrium_stair_canteen.jpg", "Atrium staircase from above, canteen left, two figures descending"),
    ("grid_28_2d4842c3.jpg", "FLOW2_int_turnstiles_lift_lobby.jpg", "Security turnstiles by lift lobby, empty"),
    ("grid_29_2de3eef4.jpg", "FLOW2_int_reception_orange_desk.jpg", "Reception atrium, orange faceted desk, receptionists, staircase behind"),
    ("grid_30_85f67179.jpg", "FLOW2_int_atrium_cafe.jpg", "Atrium with turnstiles and cafe, revolving door right"),
    ("grid_31_70aa0a83.jpg", "FLOW2_int_atrium_mirrored_ceiling.jpg", "Atrium looking up, mirrored ceiling, revolving doors, day"),
    ("grid_32_8ac97b9c.jpg", "FLOW2_int_lobby_revolving_doors_dusk.jpg", "Entrance lobby revolving doors from inside, figure walking through, dusk"),
]
TITLE_CARDS = [
    ("grid_15_a8faf13b.jpg", "FLOW2_TITLE_CARD_lineup.jpg", "TITLE CARD - CIRCLE THE SQUARE over 6-character lineup in courtyard, dusk"),
    ("grid_18_841bf975.jpg", "FLOW2_TITLE_CARD_courtyard.jpg", "TITLE CARD - CIRCLE THE SQUARE over courtyard dusk exterior, staff silhouettes"),
]

GROUPS = [("Exteriors", EXTERIORS), ("Interiors", INTERIORS), ("Title cards", TITLE_CARDS)]

# 1. copy plates
for group in (EXTERIORS, INTERIORS, TITLE_CARDS):
    for src, name, _ in group:
        dst = os.path.join(PLATES, name)
        if not os.path.exists(dst):
            shutil.copy2(os.path.join(DL, src), dst)
print("plates copied:", sum(len(g) for g in (EXTERIORS, INTERIORS, TITLE_CARDS)))

# 2. append to manifest (once)
with open(MANIFEST, encoding="utf-8") as f:
    manifest = f.read()
if "FLOW2_" not in manifest:
    lines = ["", "", "## Second batch - Flow project f2f0d2c9, downloaded 2026-08-12", "",
             "Same cartoon style, 1376x768. FLOW2_ prefix to distinguish from the first batch.", "",
             "| File | What it is |", "|---|---|"]
    for group in (EXTERIORS, INTERIORS, TITLE_CARDS):
        for src, name, desc in group:
            lines.append(f"| `{name}` | {desc} |")
    with open(MANIFEST, "a", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("manifest updated")

# 3. insert gallery section into HTML (once)
with open(HTML, encoding="utf-8") as f:
    html = f.read()
if 'id="flow2"' not in html:
    parts = ['  <section class="file" id="flow2">',
             '    <div class="file-head">',
             '      <div>',
             '        <div class="file-name">Flow cartoon plates — second batch (12 Aug 2026)</div>',
             '        <div class="file-role">New cartoon building/interior plates generated in Google Flow '
             '(project f2f0d2c9). Files in location-refs/cartoon-plates/, FLOW2_ prefix.</div>',
             '      </div>',
             '    </div>']
    for title, group in GROUPS:
        parts += [f'    <div class="gallery">', f'      <h4>{title}</h4>',
                  '      <div class="gallery-grid">']
        for src, name, desc in group:
            cap = desc.split(" - ")[0].split(",")[0]
            parts.append(f'        <figure><img src="location-refs/cartoon-plates/{name}" '
                         f'alt="{desc}"><figcaption>{cap}</figcaption></figure>')
        parts += ['      </div>', '    </div>']
    parts.append('  </section>')
    section = "\n".join(parts) + "\n\n"
    html = html.replace('  <div class="notes">', section + '  <div class="notes">', 1)
    print("html section inserted")

# 4. embed all local images as base64 (downscaled: max 1600px, JPEG q82)
from io import BytesIO

from PIL import Image

MAX_DIM = 1600

def embed(m):
    src = m.group(1)
    if src.startswith(("data:", "http")):
        return m.group(0)
    full = os.path.join(ROOT, src)
    if not os.path.exists(full):
        print("MISSING:", src)
        return m.group(0)
    ext = os.path.splitext(full)[1].lower()
    im = Image.open(full)
    if max(im.size) > MAX_DIM:
        im.thumbnail((MAX_DIM, MAX_DIM), Image.LANCZOS)
    buf = BytesIO()
    if ext == ".png":
        im.save(buf, "PNG")
        mime = "image/png"
    else:
        im.convert("RGB").save(buf, "JPEG", quality=82)
        mime = "image/jpeg"
    b64 = base64.b64encode(buf.getvalue()).decode()
    return f'src="data:{mime};base64,{b64}"'

html, n = re.subn(r'src="([^"]+)"', embed, html)
with open(HTML, "w", encoding="utf-8") as f:
    f.write(html)
print(f"embedded {n} images -> {HTML} ({os.path.getsize(HTML)//1024} KB)")
