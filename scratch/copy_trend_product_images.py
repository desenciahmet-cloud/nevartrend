import os
import shutil
import json

app_dir = r'C:\Users\user\Desktop\nevartrend_ev'
prod_img_dir = os.path.join(app_dir, 'static', 'images', 'products')
os.makedirs(prod_img_dir, exist_ok=True)

# Generated image file mapping:
artifacts_dir = r'C:\Users\user\.gemini\antigravity\brain\ad1e2d41-48b4-4845-95fb-e5545a54cf17'

# Find the generated files
image_mapping = {
    "TP_001": ("kirlent_kilifi_mockup", "/static/images/products/TP_001.jpg"),
    "TP_002": ("ipek_fular_mockup", "/static/images/products/TP_002.jpg"),
    "TP_003": ("table_runner_mockup", "/static/images/products/TP_003.jpg"),
    "TP_004": ("kanvas_canta_mockup", "/static/images/products/TP_004.jpg"),
    "TP_005": ("muslin_blanket_mockup", "/static/images/products/TP_005.jpg"),
    "TP_006": ("kimono_robe_mockup", "/static/images/products/TP_006.jpg"),
    "TP_007": ("tayt_pantolon_mockup", "/static/images/products/TP_007.jpg")
}

# Scan artifacts dir for corresponding image files
art_files = os.listdir(artifacts_dir)

for tp_id, (prefix, rel_path) in image_mapping.items():
    found_file = None
    for f in art_files:
        if f.startswith(prefix) and f.endswith('.jpg'):
            found_file = os.path.join(artifacts_dir, f)
            break
    if found_file and os.path.exists(found_file):
        dest_path = os.path.join(app_dir, rel_path.lstrip('/'))
        shutil.copy(found_file, dest_path)
        print(f"Copied {prefix} -> {dest_path}")
    else:
        print(f"Warning: Could not find image for {prefix}")

# Update trend_products.json
json_path = os.path.join(app_dir, 'data', 'trend_products.json')
with open(json_path, 'r', encoding='utf-8') as f:
    products = json.load(f)

# Ensure TP_007 is included
has_tp007 = any(p['id'] == 'TP_007' for p in products)
if not has_tp007:
    products.append({
        "id": "TP_007",
        "code": "TP_007",
        "title": "Geometrik Baskılı Yüksek Bel Likralı Tayt & Pantolon",
        "category": "giyim-butik",
        "category_name": "Giyim & Butik Aksesuar",
        "price": 275.0,
        "old_price": 350.0,
        "badge": "Yeni Sezon",
        "image": "/static/images/products/TP_007.jpg",
        "size_options": ["S / 36", "M / 38", "L / 40", "XL / 42"],
        "fabric_type": "Likralı Scuba & Dalgıç",
        "description": "4 yana esnek, form koruyucu ve iç göstermeyen yüksek bel tasarım tayt. Spor ve günlük kombinler için maksimum konfor.",
        "features": [
            "4 yana esnek likra dokusu",
            "Yüksek bel toparlayıcı korse",
            "Nefes alan ve terletmeyen kumaş",
            "Solmayan canlı dijital baskı"
        ],
        "in_stock": True
    })

# Update images in products array
for p in products:
    pid = p['id']
    if pid in image_mapping:
        p['image'] = image_mapping[pid][1]

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(products, f, ensure_ascii=False, indent=2)

print("Updated data/trend_products.json successfully!")
