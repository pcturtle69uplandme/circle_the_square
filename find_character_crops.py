import os
from PIL import Image

base_dir = r"C:\ai\Circle the Square"
sheets = ["jan_peach_identity_sheet.jpg", "christina_dross_identity_sheet.jpg", "sharon_enfield_identity_sheet.jpg", "chris_identity_sheet.jpg", "rick_identity_sheet.jpg"]

for s in sheets:
    path = os.path.join(base_dir, "character-refs", s)
    img = Image.open(path)
    print(f"Sheet: {s}, Size: {img.size}")
