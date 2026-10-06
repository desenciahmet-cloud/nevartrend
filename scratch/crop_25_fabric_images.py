import os
import json
from PIL import Image

img_path = r'C:\Users\user\.gemini\antigravity\brain\ad1e2d41-48b4-4845-95fb-e5545a54cf17\.user_uploaded\media_1791314591028.png'
save_dir = r'C:\Users\user\Desktop\nevartrend_ev\static\images\fabrics'
os.makedirs(save_dir, exist_ok=True)

im = Image.open(img_path)
w, h = im.size

# Precise column X coordinates for 5 columns:
# Col 0: 16 -> 113
# Col 1: 122 -> 219
# Col 2: 228 -> 325
# Col 3: 334 -> 431
# Col 4: 440 -> 537

col_boxes = [
    (16, 114),
    (122, 220),
    (228, 326),
    (334, 432),
    (440, 538)
]

# Precise row Y coordinates for 5 rows of images:
# Row 0: 142 -> 245
# Row 1: 307 -> 410
# Row 2: 472 -> 575
# Row 3: 637 -> 740
# Row 4: 802 -> 905

row_boxes = [
    (142, 245),
    (307, 410),
    (472, 575),
    (637, 740),
    (802, 905)
]

fabric_ids_grid = [
    ["penang-75", "multi-sifon-75", "queen-krep-112", "cassandra-120", "charmus-saten-88"],
    ["cupra-saten-85", "yoryo-saten-90", "channel-saten-120", "bubbly-girl-115", "zara-saten-160"],
    ["luna-65", "soft-skin-115", "sifon-30-denye", "fransiz-kadife-240", "polyester-keten-145"],
    ["poly-poplin-likra-108", "shows-mango-saten-155", "saten-30-denye-50", "lycra-saten-cdc-85", "miracle-72"],
    ["jessica-saten-120", "dubai-jessica-130", "full-mat-likra-saten-95", "mat-likra-saten-95", "parlak-likra-saten-95"]
]

cropped_count = 0
for r_idx in range(5):
    y1, y2 = row_boxes[r_idx]
    for c_idx in range(5):
        x1, x2 = col_boxes[c_idx]
        fid = fabric_ids_grid[r_idx][c_idx]

        cropped = im.crop((x1, y1, x2, y2))
        
        # Save as JPG & WEBP for high quality & fast loading
        jpg_file = os.path.join(save_dir, f"{fid}.jpg")
        webp_file = os.path.join(save_dir, f"{fid}.webp")
        
        cropped.convert("RGB").save(jpg_file, "JPEG", quality=92)
        cropped.convert("RGB").save(webp_file, "WEBP", quality=90)
        cropped_count += 1

print(f"Successfully cropped and saved {cropped_count} fabric images!")

# Now update data/fabric_types.json with "image" paths
json_path = r'C:\Users\user\Desktop\nevartrend_ev\data\fabric_types.json'
with open(json_path, 'r', encoding='utf-8') as f:
    fabrics = json.load(f)

for f in fabrics:
    fid = f["id"]
    f["image"] = f"/static/images/fabrics/{fid}.jpg"
    f["image_webp"] = f"/static/images/fabrics/{fid}.webp"

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(fabrics, f, ensure_ascii=False, indent=2)

print("Updated data/fabric_types.json with image references!")
