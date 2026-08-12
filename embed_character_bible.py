"""Make character-bible.html self-contained.

- Swaps each character-refs/<name>_cartoon_sheet.jpg reference to the new
  Flow-generated <name>_height_sheet.jpg (shared height scale versions).
- Embeds every local image as a base64 data URI so the HTML needs no files.

Overwrites character-bible.html (recoverable via git).
"""
import base64
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(ROOT, "character-bible.html")

with open(HTML, encoding="utf-8") as f:
    html = f.read()

def embed(m):
    src = m.group(1)
    if src.startswith(("data:", "http")):
        return m.group(0)
    path = src
    # prefer the new height-scale sheets over the old cartoon sheets
    height = src.replace("_cartoon_sheet.jpg", "_height_sheet.jpg")
    if "_cartoon_sheet.jpg" in src and os.path.exists(os.path.join(ROOT, height)):
        path = height
    full = os.path.join(ROOT, path)
    if not os.path.exists(full):
        print("MISSING:", src)
        return m.group(0)
    ext = os.path.splitext(full)[1].lower()
    mime = "image/png" if ext == ".png" else "image/jpeg"
    with open(full, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    print(f"embedded: {path} ({len(b64)//1024} KB b64)")
    return f'src="data:{mime};base64,{b64}"'

html = re.sub(r'src="([^"]+)"', embed, html)

with open(HTML, "w", encoding="utf-8") as f:
    f.write(html)
print("done ->", HTML, f"({os.path.getsize(HTML)//1024} KB)")
