"""Generate character turnaround identity sheets for Circle the Square using Google AI Gemini / Imagen models.
"""

import os
import sys
import subprocess
from pathlib import Path

AI_DIR = Path(r"C:\ai\AI")
OUT_DIR = Path(r"C:\kontitemp\ai\circle_the_square\character-refs")
OUT_DIR.mkdir(parents=True, exist_ok=True)

CHARACTERS = [
    {
        "name": "Jan Peach",
        "file_prefix": "jan_peach_sheet",
        "prompt": (
            "MAIN IDENTITY & SCALE SHEET: Character turnaround sheet showing front view, 3/4 view, side view, back view of Jan Peach, "
            "52-year-old male corporate CEO, white British. Soft overweight build with a noticeable gut straining suit shirt buttons, rounded shoulders. "
            "Wearing a slightly tight dark navy two-button suit (#1B2436), white dress shirt (#F5F1E6) with top button undone, and a Prism burnt orange lanyard (#B0381F) with ID badge. "
            "Mid-brown product-slicked comb-over hair greying at temples. Smug thin-lipped default expression held across all views. "
            "Neutral studio grey backdrop, even studio lighting, scale ruler 0-190cm on the left, clean character design reference sheet, photorealistic, 4K."
        )
    },
    {
        "name": "Christina Dross",
        "file_prefix": "christina_dross_sheet",
        "prompt": (
            "MAIN IDENTITY & SCALE SHEET: Character turnaround sheet showing front view, 3/4 view, side view, back view of Christina Dross, "
            "38-year-old female corporate comms lead, white British. Slim, upright build with squared shoulders. "
            "Dark brown sleek bob haircut with blunt fringe (#2E211A). Wearing a charcoal navy tailored blazer (#2B2E33), cream blouse (#EFE6D8), "
            "tailored trousers, low block heels, and a Prism burnt orange lanyard (#B0381F). Holding a silver tablet. "
            "Composed, calm, dry deadpan half-smile held across all views. "
            "Neutral studio grey backdrop, even studio lighting, scale ruler 0-180cm on the left, clean character design reference sheet, photorealistic, 4K."
        )
    },
    {
        "name": "Sharon Enfield",
        "file_prefix": "sharon_enfield_sheet",
        "prompt": (
            "MAIN IDENTITY & SCALE SHEET: Character turnaround sheet showing front view, 3/4 view, side view, back view of Sharon Enfield, "
            "34-year-old female office staff member, white British. Curvy build, shoulder-length wavy auburn hair (#7A3B2E). "
            "Wearing a fitted emerald jewel-tone blouse (#1F5C4A), black pencil skirt (#1A1A1A), heels, and a Prism burnt orange lanyard (#B0381F). "
            "Confident, unbothered, transactionally calm expression held across all views. "
            "Neutral studio grey backdrop, even studio lighting, scale ruler 0-175cm on the left, clean character design reference sheet, photorealistic, 4K."
        )
    },
    {
        "name": "Chris",
        "file_prefix": "chris_sheet",
        "prompt": (
            "MAIN IDENTITY & SCALE SHEET: Character turnaround sheet showing front view, 3/4 view, side view, back view of Chris, "
            "32-year-old male office staff worker, white British. Lean build, short textured dark hair (#1F1B18). "
            "Wearing a light blue casual shirt with sleeves rolled up (#6E93B5), untucked, dark casual trousers (#2A2A2A), sneakers, and a Prism burnt orange lanyard (#B0381F). "
            "Relaxed slouched stance, deadpan amused smirk with one cocked eyebrow held across all views. "
            "Neutral studio grey backdrop, even studio lighting, scale ruler 0-185cm on the left, clean character design reference sheet, photorealistic, 4K."
        )
    },
    {
        "name": "Rick",
        "file_prefix": "rick_sheet",
        "prompt": (
            "MAIN IDENTITY & SCALE SHEET: Character turnaround sheet showing front view, 3/4 view, side view, back view of Rick, "
            "40-year-old male office staff member, white British. Sturdy, broad build, short greying hair (#6E6A63). "
            "Wearing a plain grey polo shirt with sleeves rolled up (#55585C), sturdy navy trousers (#262B33), practical shoes, and a Prism burnt orange lanyard (#B0381F). "
            "Arms crossed, feet planted, flat unimpressed calm expression held across all views. "
            "Neutral studio grey backdrop, even studio lighting, scale ruler 0-190cm on the left, clean character design reference sheet, photorealistic, 4K."
        )
    }
]

def generate_sheets(model="pro", aspect="16:9", size="2K"):
    print(f"Generating {len(CHARACTERS)} character turnaround sheets with model={model}, aspect={aspect}, size={size}...")
    for idx, char in enumerate(CHARACTERS, 1):
        print(f"\n[{idx}/{len(CHARACTERS)}] Generating sheet for {char['name']}...")
        cmd = [
            sys.executable,
            str(AI_DIR / "gen_image.py"),
            char["prompt"],
            "-m", model,
            "--aspect", aspect,
            "-o", str(OUT_DIR),
            "--yes"
        ]
        if size:
            cmd.extend(["--size", size])
            
        res = subprocess.run(cmd, cwd=str(AI_DIR), capture_output=True, text=True)
        if res.returncode == 0:
            print(f"  Success! Output:\n{res.stdout.strip()}")
        else:
            print(f"  Error generating {char['name']}:\n{res.stderr.strip()}")

if __name__ == "__main__":
    model_choice = sys.argv[1] if len(sys.argv) > 1 else "pro"
    generate_sheets(model=model_choice)
