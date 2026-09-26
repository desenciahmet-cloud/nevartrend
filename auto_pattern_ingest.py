"""
Nevartrend Otomatik Desen Yükleme, İsimlendirme ve Renk Paleti Çıkarma Aracı
Kullanım:
  python auto_pattern_ingest.py
  (veya parametre olarak görsel yolu verebilirsiniz: python auto_pattern_ingest.py "desen1.jpg" "desen2.png")
"""

import os
import sys
import json
import shutil
from pathlib import Path
from PIL import Image

BASE_DIR = Path(__file__).parent.resolve()
DATA_DIR = BASE_DIR / "data"
PRODUCTS_FILE = DATA_DIR / "products.json"
CATEGORIES_FILE = DATA_DIR / "categories.json"
IMAGES_DIR = BASE_DIR / "static" / "images"
GITHUB_DIR = Path("C:/Users/user/Desktop/GITHUB_YUKLENECEK_TEMPLATES")

def extract_dominant_colors(image_path, num_colors=4):
    """Görselden en baskın renkleri HEX kodu olarak çıkarır."""
    try:
        with Image.open(image_path) as img:
            img = img.convert("RGB")
            img = img.resize((150, 150))
            result = img.quantize(colors=num_colors, method=Image.Quantize.MEDIANCUT)
            palette = result.getpalette()[:num_colors * 3]
            colors = []
            for i in range(0, len(palette), 3):
                r, g, b = palette[i], palette[i+1], palette[i+2]
                hex_color = f"#{r:02x}{g:02x}{b:02x}"
                colors.append(hex_color)
            return colors
    except Exception as e:
        print(f"Renk çıkarılırken hata: {e}")
        return ["#1e293b", "#059669", "#d97706", "#f8fafc"]

def get_next_pattern_id(products):
    """En son NT_xxx kodunu bulup bir sonrakini üretir."""
    max_num = 0
    for p in products:
        code = p.get("id", "")
        if code.startswith("NT_"):
            try:
                num = int(code.replace("NT_", "").split("_")[0])
                if num > max_num:
                    max_num = num
            except ValueError:
                pass
    next_num = max_num + 1
    return f"NT_{next_num:03d}"

def optimize_image(src_path, dest_path, max_dim=2000, quality=85):
    """Görseli web için optimize ederek kaydeder."""
    with Image.open(src_path) as img:
        img = img.convert("RGB")
        w, h = img.size
        if max(w, h) > max_dim:
            if w > h:
                new_w = max_dim
                new_h = int(h * (max_dim / w))
            else:
                new_h = max_dim
                new_w = int(w * (max_dim / h))
            img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        img.save(dest_path, "JPEG", quality=quality, optimize=True)
    return dest_path

def ingest_patterns(file_paths=None, titles=None, categories=None):
    """Yeni desenleri sisteme ekler."""
    if not PRODUCTS_FILE.exists():
        print(f"Hata: {PRODUCTS_FILE} bulunamadı!")
        return

    with open(PRODUCTS_FILE, "r", encoding="utf-8") as f:
        products = json.load(f)

    existing_images = {p.get("image", "").split("/")[-1] for p in products}

    # Eğer özel dosya verilmediyse, static/images içindeki yeni dosyaları tara
    if not file_paths:
        file_paths = []
        raw_candidates = list(IMAGES_DIR.glob("*.jpg")) + list(IMAGES_DIR.glob("*.png")) + list(IMAGES_DIR.glob("*.jpeg"))
        for p in raw_candidates:
            if p.name not in existing_images and not p.name.startswith("NT_"):
                file_paths.append(p)

    if not file_paths:
        print("İşlenecek yeni desen bulunamadı.")
        print(f"İpucu: Desenlerinizi {IMAGES_DIR} klasörüne bırakıp bu komutu tekrar çalıştırın.")
        return

    print(f"\n✨ {len(file_paths)} yeni desen tespit edildi. İşlem başlıyor...")

    added_products = []

    for idx, fpath in enumerate(file_paths):
        src_path = Path(fpath)
        if not src_path.exists():
            print(f"Dosya bulunamadı: {src_path}")
            continue

        pattern_id = get_next_pattern_id(products)
        dest_filename = f"{pattern_id}.jpg"
        dest_path = IMAGES_DIR / dest_filename

        print(f"[{idx+1}/{len(file_paths)}] İşleniyor: {src_path.name} -> {dest_filename}")

        # Optimize et ve kaydet
        optimize_image(src_path, dest_path)

        # Renkleri çıkar
        dominant_colors = extract_dominant_colors(dest_path)

        # Başlık ve kategori belirle
        custom_title = titles[idx] if (titles and idx < len(titles)) else f"Trenddesen {pattern_id} Özel Seri"
        custom_cat = categories[idx] if (categories and idx < len(categories)) else "desenler"
        cat_name = "Baskı & Dijital Koleksiyon"

        new_item = {
            "id": pattern_id,
            "code": pattern_id,
            "title": custom_title,
            "category": custom_cat,
            "category_name": cat_name,
            "print_type": "Dijital & Emprime Uyumlu",
            "separation_ready": True,
            "screen_count": 6,
            "base_price": 185.0,
            "rating": 5.0,
            "reviews_count": 12,
            "tags": ["Yeni", "Trenddesen", "Özel Baskı", "Dikişsiz Rapor"],
            "image": f"/static/images/{dest_filename}",
            "pattern_tile": f"/static/images/{dest_filename}",
            "description": f"Trenddesen yeni sezon özel dijital ve emprime baskı kumaş deseni. {custom_title}.",
            "colors": dominant_colors,
            "featured": True,
            "is_new": True,
            "discount_pct": 0,
            "sales_count": 24
        }

        products.insert(0, new_item)
        added_products.append(new_item)

    # products.json güncelle
    with open(PRODUCTS_FILE, "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=2)

    print(f"\n✅ {len(added_products)} yeni desen products.json dosyasına eklendi.")

    # GITHUB_YUKLENECEK_TEMPLATES klasörünü senkronize et
    if GITHUB_DIR.exists():
        gh_data_dir = GITHUB_DIR / "data"
        gh_img_dir = GITHUB_DIR / "static" / "images"
        gh_tpl_dir = GITHUB_DIR / "templates"

        gh_data_dir.mkdir(parents=True, exist_ok=True)
        gh_img_dir.mkdir(parents=True, exist_ok=True)
        gh_tpl_dir.mkdir(parents=True, exist_ok=True)

        shutil.copy(PRODUCTS_FILE, gh_data_dir / "products.json")
        shutil.copy(BASE_DIR / "templates" / "product-detail.html", gh_tpl_dir / "product-detail.html")
        shutil.copy(BASE_DIR / "templates" / "index.html", gh_tpl_dir / "index.html")
        shutil.copy(BASE_DIR / "templates" / "fabrics.html", gh_tpl_dir / "fabrics.html")

        for p in added_products:
            img_file = IMAGES_DIR / f"{p['id']}.jpg"
            if img_file.exists():
                shutil.copy(img_file, gh_img_dir / f"{p['id']}.jpg")

        print("🚀 GITHUB_YUKLENECEK_TEMPLATES klasörü otomatik olarak güncellendi!")

    print("\n🎉 Tüm işlemler başarıyla tamamlandı!")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        ingest_patterns(sys.argv[1:])
    else:
        ingest_patterns()
