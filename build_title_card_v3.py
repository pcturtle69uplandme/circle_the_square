"""Generate high-resolution video Title Card for Circle the Square (ALL UNDER ONE ROOF).

Output: clips/title_card_v03.mp4
Format: 1920x1080 @ 24fps (16:9 / 2.39:1 crop framing), 8.0s duration.
Zero API cost — Uses local PIL & FFMPEG rendering.
"""
import os
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).parent
CLIPS_DIR = HERE / "clips"
OUT_FILE = CLIPS_DIR / "title_card_v03.mp4"

# Canvas parameters
W, H, FPS = 1920, 1080, 24
DUR = 8.0
TOTAL_FRAMES = int(W * H)

# Colors
INK_NAVY = (11, 13, 18)
BURNT_ORANGE = (176, 56, 31)
BONE_WHITE = (244, 243, 239)
SLATE_GREY = (148, 163, 184)
GRID_LINE = (42, 47, 64)

# FFMPEG resolution check
def get_ffmpeg():
    # Try winget / system path
    try:
        r = subprocess.run(["ffmpeg", "-version"], capture_output=True)
        if r.returncode == 0:
            return "ffmpeg"
    except Exception:
        pass
    
    # Try common local WinGet path
    winget_path = Path(os.path.expanduser("~")) / "AppData/Local/Microsoft/WinGet/Packages"
    for p in winget_path.glob("**/ffmpeg.exe"):
        return str(p)
    return "ffmpeg"


def create_title_frame(t: float, font_title, font_sub, font_mono) -> Image.Image:
    im = Image.new("RGB", (W, H), INK_NAVY)
    draw = ImageDraw.Draw(im)

    # 1. Subtle background geometric triangle overlay
    t_plan_alpha = min(1.0, max(0.0, (t - 0.5) / 1.5))
    if t_plan_alpha > 0:
        center_x, center_y = W // 2, H // 2 - 20
        r = 280
        # Draw soft triangle outline
        pts = [
            (center_x, center_y - r),
            (center_x - r * 1.15, center_y + r * 0.75),
            (center_x + r * 1.15, center_y + r * 0.75),
        ]
        line_col = tuple(int(GRID_LINE[i] * t_plan_alpha + INK_NAVY[i] * (1 - t_plan_alpha)) for i in range(3))
        draw.polygon(pts, outline=line_col, width=3)

    # 2. Main Title: "CIRCLE THE SQUARE" (Fade in t=1.2 to 2.5)
    t_title_alpha = min(1.0, max(0.0, (t - 1.2) / 1.3))
    if t_title_alpha > 0:
        title_text = "C I R C L E   T H E   S Q U A R E"
        title_col = tuple(int(BONE_WHITE[i] * t_title_alpha + INK_NAVY[i] * (1 - t_title_alpha)) for i in range(3))
        
        # Calculate text width & position
        bbox = draw.textbbox((0, 0), title_text, font=font_title)
        tw = bbox[2] - bbox[0]
        tx = (W - tw) // 2
        ty = H // 2 - 60
        draw.text((tx, ty), title_text, font=font_title, fill=title_col)

    # 3. Subtitle: "ALL UNDER ONE ROOF" (Fade in t=2.8 to 4.0)
    t_sub_alpha = min(1.0, max(0.0, (t - 2.8) / 1.2))
    if t_sub_alpha > 0:
        sub_text = "───  ALL UNDER ONE ROOF  ───"
        sub_col = tuple(int(BURNT_ORANGE[i] * t_sub_alpha + INK_NAVY[i] * (1 - t_sub_alpha)) for i in range(3))
        
        bbox = draw.textbbox((0, 0), sub_text, font=font_sub)
        sw = bbox[2] - bbox[0]
        sx = (W - sw) // 2
        sy = H // 2 + 30
        draw.text((sx, sy), sub_text, font=font_sub, fill=sub_col)

    # 4. Location Code: "PRISM HQ — CAMBRIDGE ASSESSMENT" (Fade in t=4.2 to 5.2)
    t_mono_alpha = min(1.0, max(0.0, (t - 4.2) / 1.0))
    if t_mono_alpha > 0:
        mono_text = "PRISM HQ  |  CAMBRIDGE ASSESSMENT MOTHERSHIP"
        mono_col = tuple(int(SLATE_GREY[i] * t_mono_alpha + INK_NAVY[i] * (1 - t_mono_alpha)) for i in range(3))
        
        bbox = draw.textbbox((0, 0), mono_text, font=font_mono)
        mw = bbox[2] - bbox[0]
        mx = (W - mw) // 2
        my = H // 2 + 100
        draw.text((mx, my), mono_text, font=font_mono, fill=mono_col)

    return im


def main():
    CLIPS_DIR.mkdir(parents=True, exist_ok=True)
    ffmpeg_bin = get_ffmpeg()
    print(f"Using FFMPEG: {ffmpeg_bin}")

    # Load system fonts with fallback
    try:
        font_title = ImageFont.truetype("arialbd.ttf", 52)
        font_sub = ImageFont.truetype("arialbd.ttf", 26)
        font_mono = ImageFont.truetype("consola.ttf", 20)
    except Exception:
        font_title = font_sub = font_mono = ImageFont.load_default()

    total_frames = int(DUR * FPS)
    print(f"Rendering Title Card: {W}x{H} @ {FPS}fps, {total_frames} frames ({DUR}s)...")

    cmd = [
        ffmpeg_bin,
        "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{W}x{H}",
        "-pix_fmt", "rgb24",
        "-r", str(FPS),
        "-i", "-",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-crf", "18",
        str(OUT_FILE),
    ]

    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)

    for frame_idx in range(total_frames):
        t = frame_idx / FPS
        im = create_title_frame(t, font_title, font_sub, font_mono)
        proc.stdin.write(im.tobytes())

    proc.stdin.close()
    proc.wait()

    if proc.returncode == 0:
        print(f"\n[DONE] Title card video generated successfully: {OUT_FILE}")
        return 0
    else:
        print(f"\n[FAIL] FFMPEG exited with code {proc.returncode}")
        return proc.returncode


if __name__ == "__main__":
    sys.exit(main())
