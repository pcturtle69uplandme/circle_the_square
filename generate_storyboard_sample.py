"""Generate a small sample batch of storyboard stills for Circle the Square via
Gemini (gen_image.py), pausing between calls to stay well under free-tier quota.

Run from anywhere:
    python generate_storyboard_sample.py

Generates F01-F05 (the Scene 1 office-greeting beats) into storyboard-frames/,
one at a time, with a pause between each. Check the results in
storyboard_slideshow.html before extending FRAMES to cover more of the 64
frames in featurette_storyboard_image_prompts.md.

Each frame only attaches the reference images it actually needs (the
characters appearing in that specific still + the scene's location sheet),
which is cheaper and faster than uploading every reference every time.
"""

import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).parent
AI_DIR = Path(r"C:\ai\AI")
OUT_DIR = ROOT / "storyboard-frames"
CHAR = ROOT / "character-refs"
LOC = ROOT / "location-refs"

MODEL = "flash"          # cheap/fast tier for sampling; switch to "pro" once approved
ASPECT = "21:9"           # closest gen_image.py preset to the 2.39:1 style anchor
GAP_SECONDS = 90          # pause between generations - adjust to 60-120 as needed

STYLE_ANCHOR = (
    "Photoreal single film-still frame, not video. Documentary British "
    "mockumentary photographic tone. Natural Northern European daylight. "
    "Shallow depth of field on close-ups, deep focus on wides. No visible "
    "real-world branding or crests. Character appearance must exactly match "
    "the attached reference images, in the order given - do not invent or "
    "alter appearance, age, or wardrobe colour beyond what this prompt "
    "specifies as a state change."
)

FRAMES = [
    {
        "id": "F01",
        "refs": [
            ("Jan Peach", CHAR / "jan_peach_identity_sheet.jpg"),
            ("Christina Dross", CHAR / "christina_dross_identity_sheet.jpg"),
            ("the office location", LOC / "jan_office_location_sheet.jpg"),
        ],
        "action": (
            "Wide still. Christina (2nd reference image) enters and stands "
            "opposite Jan's (1st reference image) desk, mid-greeting, relaxed "
            "and professional. Jan looks up from his desk toward her, in the "
            "office shown in the 3rd reference image."
        ),
    },
    {
        "id": "F02",
        "refs": [
            ("Jan Peach", CHAR / "jan_peach_identity_sheet.jpg"),
            ("Christina Dross", CHAR / "christina_dross_identity_sheet.jpg"),
            ("the office location", LOC / "jan_office_location_sheet.jpg"),
        ],
        "action": (
            "Same two-shot as before, slightly closer on Jan (1st reference "
            "image). He gives a small sigh, leaning back in his chair with a "
            "put-upon expression. Christina (2nd reference image) stands "
            "opposite. Office shown in the 3rd reference image."
        ),
    },
    {
        "id": "F03",
        "refs": [
            ("Christina Dross", CHAR / "christina_dross_identity_sheet.jpg"),
            ("Jan Peach", CHAR / "jan_peach_identity_sheet.jpg"),
            ("the office location", LOC / "jan_office_location_sheet.jpg"),
        ],
        "action": (
            "Medium close-up on Christina (1st reference image), upright and "
            "businesslike, mid-pitch, tablet in hand, in the office shown in "
            "the 3rd reference image. Jan (2nd reference image) softly out of "
            "focus in the background."
        ),
    },
    {
        "id": "F04",
        "refs": [
            ("Jan Peach", CHAR / "jan_peach_identity_sheet.jpg"),
            ("the office location", LOC / "jan_office_location_sheet.jpg"),
        ],
        "action": (
            "Medium close-up on Jan (1st reference image), leaning forward "
            "slightly, genuinely curious, in the office shown in the 2nd "
            "reference image."
        ),
    },
    {
        "id": "F05",
        "refs": [
            ("Christina Dross", CHAR / "christina_dross_identity_sheet.jpg"),
            ("the office location", LOC / "jan_office_location_sheet.jpg"),
        ],
        "action": (
            "Medium close-up on Christina (1st reference image), explaining "
            "calmly and matter-of-factly, one hand gesturing slightly to "
            "illustrate a plan, in the office shown in the 2nd reference image."
        ),
    },
]


def build_prompt(frame):
    ref_lines = "\n".join(
        f"- Reference image {i + 1}: {label}" for i, (label, _) in enumerate(frame["refs"])
    )
    return f"{ref_lines}\n\n{frame['action']}\n\n{STYLE_ANCHOR}"


def run_frame(frame):
    out_path = OUT_DIR / f"{frame['id']}.jpg"
    if out_path.exists():
        print(f"[skip] {frame['id']} already exists at {out_path}")
        return True

    for label, path in frame["refs"]:
        if not path.is_file():
            print(f"  !! missing reference for {label}: {path}")
            return False

    prompt = build_prompt(frame)
    cmd = [sys.executable, str(AI_DIR / "gen_image.py"), prompt,
           "-m", MODEL, "--aspect", ASPECT, "-o", str(OUT_DIR), "--yes"]
    for _, path in frame["refs"]:
        cmd.extend(["--image", str(path)])

    print(f"\n=== {frame['id']} ===")
    result = subprocess.run(cmd, cwd=str(AI_DIR), capture_output=True, text=True)
    print(result.stdout.strip())
    if result.stderr.strip():
        print(result.stderr.strip())

    if result.returncode != 0:
        print(f"  generation failed for {frame['id']} - stopping so you can check quota/errors.")
        return False

    m = re.search(r"saved (.+?\.(?:jpg|jpeg|png))", result.stdout, re.IGNORECASE)
    if not m:
        print(f"  no 'saved' path found in output for {frame['id']} - check above for an error "
              f"(e.g. filtered prompt, quota hit).")
        return False

    generated = Path(m.group(1))
    if generated.exists() and generated != out_path:
        generated.rename(out_path)
    print(f"  -> {out_path}")
    return True


def main():
    OUT_DIR.mkdir(exist_ok=True)
    print(f"Sampling {len(FRAMES)} frame(s), model={MODEL}, {GAP_SECONDS}s gap between calls.")
    input("Press Enter to start (Ctrl+C to cancel)... ")

    for i, frame in enumerate(FRAMES):
        ok = run_frame(frame)
        if not ok:
            break
        if i < len(FRAMES) - 1:
            print(f"  waiting {GAP_SECONDS}s before next frame (quota pacing)...")
            time.sleep(GAP_SECONDS)

    print("\nDone. Open storyboard_slideshow.html and refresh to review.")


if __name__ == "__main__":
    main()
