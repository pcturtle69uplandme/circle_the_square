"""Generate photoreal turnaround identity sheets for the 6 missing supporting cast members,
matching the style of the existing 5 principal sheets in character-refs/_photoreal-archive/
(grey studio backdrop, height ruler, FRONT / 3/4 FRONT / SIDE / BACK, orange PRISM lanyard).
"""

import sys
import subprocess
from pathlib import Path

AI_DIR = Path(r"C:\ai\AI")
OUT_DIR = Path(r"C:\ai\Circle the Square\character-refs\_photoreal-archive")
OUT_DIR.mkdir(parents=True, exist_ok=True)

CHARACTERS = [
    {
        "name": "Maureen",
        "file_prefix": "maureen_sheet",
        "prompt": (
            "MAIN IDENTITY & SCALE SHEET: Character turnaround sheet showing front view, 3/4 view, side view, back view of Maureen, "
            "58-year-old female canteen worker, white British. Sturdy build, short greying curly hair pinned back (#8A857D). "
            "Wearing a beige apron (#D8C8A8) over a white polo shirt, black trousers, black non-slip flats, and reading glasses on a chain. "
            "No lanyard. Kindly but no-nonsense expression held across all views. "
            "Neutral studio grey backdrop, even studio lighting, scale ruler 0-165cm on the left, clean character design reference sheet, photorealistic, 4K."
        ),
    },
    {
        "name": "Gemma Ashcroft",
        "file_prefix": "gemma_ashcroft_sheet",
        "prompt": (
            "MAIN IDENTITY & SCALE SHEET: Character turnaround sheet showing front view, 3/4 view, side view, back view of Gemma Ashcroft, "
            "26-year-old female front-of-house receptionist, white British. Slim build, sleek dark blonde high ponytail (#B8965A). "
            "Wearing a white blouse, slate-grey tailored blazer and pencil skirt (#5C6066), black low heels, a Prism burnt orange lanyard (#B0381F), "
            "and a discreet telephone headset. Polished customer-service smile held across all views. "
            "Neutral studio grey backdrop, even studio lighting, scale ruler 0-172cm on the left, clean character design reference sheet, photorealistic, 4K."
        ),
    },
    {
        "name": "Priya Raghavan",
        "file_prefix": "priya_raghavan_sheet",
        "prompt": (
            "MAIN IDENTITY & SCALE SHEET: Character turnaround sheet showing front view, 3/4 view, side view, back view of Priya Raghavan, "
            "29-year-old female office staff member, British Indian. Slim build, long dark hair in a low ponytail (#1A1512). "
            "Wearing a mustard cardigan (#C9992E) over a white blouse, navy trousers, tan ankle boots, and a Prism burnt orange lanyard (#B0381F). "
            "Bright, alert expression held across all views. "
            "Neutral studio grey backdrop, even studio lighting, scale ruler 0-166cm on the left, clean character design reference sheet, photorealistic, 4K."
        ),
    },
    {
        "name": "Barbara Whitlock",
        "file_prefix": "barbara_whitlock_sheet",
        "prompt": (
            "MAIN IDENTITY & SCALE SHEET: Character turnaround sheet showing front view, 3/4 view, side view, back view of Barbara Whitlock, "
            "55-year-old female senior administrator, white British. Short, round build, ash-blonde greying bob (#B8AFA0), "
            "large round glasses on a beaded chain. Wearing a teal blouse (#1F6B66), navy cardigan, grey A-line skirt, low black heels, "
            "and a Prism burnt orange lanyard (#B0381F). Sceptical, pursed expression held across all views. "
            "Neutral studio grey backdrop, even studio lighting, scale ruler 0-162cm on the left, clean character design reference sheet, photorealistic, 4K."
        ),
    },
    {
        "name": "Dev Osei",
        "file_prefix": "dev_osei_sheet",
        "prompt": (
            "MAIN IDENTITY & SCALE SHEET: Character turnaround sheet showing front view, 3/4 view, side view, back view of Dev Osei, "
            "26-year-old male junior data analyst, Black British. Slim build, short cropped black hair, thick black-rimmed glasses. "
            "Wearing a burgundy jumper (#5C1F26) over a pale blue collared shirt, dark grey chinos, white trainers, and a Prism burnt orange lanyard (#B0381F). "
            "Earnest, slightly nervous expression held across all views. "
            "Neutral studio grey backdrop, even studio lighting, scale ruler 0-180cm on the left, clean character design reference sheet, photorealistic, 4K."
        ),
    },
    {
        "name": "Tomasz Wojcik",
        "file_prefix": "tomasz_wojcik_sheet",
        "prompt": (
            "MAIN IDENTITY & SCALE SHEET: Character turnaround sheet showing front view, 3/4 view, side view, back view of Tomasz Wojcik, "
            "35-year-old male facilities and maintenance worker, Polish British. Tall, heavyset build, shaved head, short dark beard. "
            "Wearing a dark blue work shirt with sleeves rolled up, a tool pouch on his belt, black work trousers, brown work boots, "
            "and a Prism burnt orange lanyard (#B0381F). Calm, unhurried expression held across all views. "
            "Neutral studio grey backdrop, even studio lighting, scale ruler 0-188cm on the left, clean character design reference sheet, photorealistic, 4K."
        ),
    },
]


def generate_sheets(model="pro", aspect="16:9", size="2K"):
    print(f"Generating {len(CHARACTERS)} supporting character turnaround sheets with model={model}, aspect={aspect}, size={size}...")
    for idx, char in enumerate(CHARACTERS, 1):
        print(f"\n[{idx}/{len(CHARACTERS)}] Generating sheet for {char['name']}...")
        cmd = [
            sys.executable,
            str(AI_DIR / "gen_image.py"),
            char["prompt"],
            "-m", model,
            "--aspect", aspect,
            "-o", str(OUT_DIR),
            "--yes",
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
