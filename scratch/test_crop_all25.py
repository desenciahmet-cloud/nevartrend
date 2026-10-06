import os
from PIL import Image

img_path = r'C:\Users\user\.gemini\antigravity\brain\ad1e2d41-48b4-4845-95fb-e5545a54cf17\.user_uploaded\media_1791314591028.png'
im = Image.open(img_path).convert('RGB')
w, h = im.size

col_boxes = [
    (16, 114),
    (122, 220),
    (228, 326),
    (334, 432),
    (440, 538)
]

row_boxes = [
    (142, 245),
    (308, 411),
    (474, 577),
    (640, 743),
    (805, 908)
]

fabric_ids_grid = [
    ["penang-75", "multi-sifon-75", "queen-krep-112", "cassandra-120", "charmus-saten-88"],
    ["cupra-saten-85", "yoryo-saten-90", "channel-saten-120", "bubbly-girl-115", "zara-saten-160"],
    ["luna-65", "soft-skin-115", "sifon-30-denye", "fransiz-kadife-240", "polyester-keten-145"],
    ["poly-poplin-likra-108", "shows-mango-saten-155", "saten-30-denye-50", "lycra-saten-cdc-85", "miracle-72"],
    ["jessica-saten-120", "dubai-jessica-130", "full-mat-likra-saten-95", "mat-likra-saten-95", "parlak-likra-saten-95"]
]

out_dir = r'C:\Users\user\Desktop\nevartrend_ev\static\images\fabrics'
os.makedirs(out_dir, exist_ok=True)

for r_idx in range(5):
    y1, y2 = row_boxes[r_idx]
    for c_idx in range(5):
        x1, x2 = col_boxes[c_idx]
        fid = fabric_ids_grid[r_idx][c_idx]

        cropped = im.crop((x1, y1, x2, y2))
        
        jpg_path = os.path.join(out_dir, f"{fid}.jpg")
        webp_path = os.path.join(out_dir, f"{fid}.webp")
        
        cropped.save(jpg_path, "JPEG", quality=95)
        cropped.save(webp_path, "WEBP", quality=92)

print("Finished exact test crop for 25 fabrics")
