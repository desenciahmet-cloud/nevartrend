import json
import os

json_path = r'C:\Users\user\Desktop\nevartrend_ev\data\fabric_types.json'

with open(json_path, 'r', encoding='utf-8') as f:
    fabrics = json.load(f)

for f in fabrics:
    fid = f["id"]
    jpg_path = f"static/images/fabrics/{fid}.jpg"
    webp_path = f"static/images/fabrics/{fid}.webp"
    
    if os.path.exists(jpg_path):
        f["image"] = f"/static/images/fabrics/{fid}.jpg"
    else:
        print(f"Warning: JPG missing for {fid}")
        
    if os.path.exists(webp_path):
        f["image_webp"] = f"/static/images/fabrics/{fid}.webp"
    else:
        print(f"Warning: WEBP missing for {fid}")

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(fabrics, f, ensure_ascii=False, indent=2)

print(f"Verified and updated json for {len(fabrics)} fabrics!")
