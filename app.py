import os
import json
import uuid
from datetime import datetime
from typing import Optional, List
from fastapi import FastAPI, Request, Form, File, UploadFile, HTTPException, Query
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="nevartrend | Trenddesen E-Ticaret")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
UPLOAD_DIR = os.path.join(BASE_DIR, "static", "uploads", "patterns")
os.makedirs(UPLOAD_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    ico_path = os.path.join(BASE_DIR, "static", "img", "favicon.ico")
    if os.path.exists(ico_path):
        return FileResponse(ico_path, media_type="image/x-icon")
    fav_path = os.path.join(BASE_DIR, "static", "img", "favicon.svg")
    return FileResponse(fav_path, media_type="image/svg+xml")

@app.get("/manifest.json", include_in_schema=False)
async def manifest_json():
    return FileResponse(os.path.join(BASE_DIR, "static", "manifest.json"), media_type="application/manifest+json")

@app.get("/sw.js", include_in_schema=False)
async def service_worker():
    return FileResponse(os.path.join(BASE_DIR, "static", "sw.js"), media_type="application/javascript")




DEFAULT_PRODUCTS = json.loads('''[
  {
    "id": "NT_074",
    "code": "NT_074",
    "title": "Gece Siyahı & Zümrüt Mor Lüks Botanik Bahçe",
    "category": "cicekli-botanik",
    "category_name": "Çiçekli & Botanik",
    "print_type": "Emprime & Dijital Baskı",
    "separation_ready": true,
    "screen_count": 6,
    "base_price": 195.0,
    "rating": 5.0,
    "reviews_count": 45,
    "tags": [
      "Yeni",
      "Siyah",
      "Zümrüt",
      "Mor",
      "Lüks",
      "Botanik"
    ],
    "image": "/static/images/NT_074.jpg",
    "pattern_tile": "/static/images/NT_074.jpg",
    "description": "Gece siyahı zemin üstünde zümrüt yeşili ve mor orkide ışıltılı lüks botanik.",
    "colors": [
      "#60907d",
      "#5d5766",
      "#831d81",
      "#1b2033"
    ],
    "featured": true,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 67
  },
  {
    "id": "NT_073",
    "code": "NT_073",
    "title": "İndigo Zemin Hardal & Mercan Gece Çiçekleri",
    "category": "cicekli-botanik",
    "category_name": "Çiçekli & Botanik",
    "print_type": "Emprime & Dijital Baskı",
    "separation_ready": true,
    "screen_count": 5,
    "base_price": 185.0,
    "rating": 5.0,
    "reviews_count": 38,
    "tags": [
      "Yeni",
      "İndigo",
      "Hardal",
      "Mercan",
      "Gece Çiçeği"
    ],
    "image": "/static/images/NT_073.jpg",
    "pattern_tile": "/static/images/NT_073.jpg",
    "description": "İndigo lacivert zemin üzerinde parlayan hardal ve mercan çiçekleri.",
    "colors": [
      "#f1b067",
      "#ec8763",
      "#645f69",
      "#404f65"
    ],
    "featured": true,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 56
  },
  {
    "id": "NT_072",
    "code": "NT_072",
    "title": "Leylak & Kiremit Pastel Çiçek Buketi",
    "category": "cicekli-botanik",
    "category_name": "Çiçekli & Botanik",
    "print_type": "Emprime & Dijital Baskı",
    "separation_ready": true,
    "screen_count": 5,
    "base_price": 175.0,
    "rating": 4.9,
    "reviews_count": 25,
    "tags": [
      "Yeni",
      "Leylak",
      "Kiremit",
      "Pastel",
      "Zarif"
    ],
    "image": "/static/images/NT_072.jpg",
    "pattern_tile": "/static/images/NT_072.jpg",
    "description": "Leylak ve kiremit tonlarının zarif uyumunu taşıyan çiçek buketi.",
    "colors": [
      "#b48ca0",
      "#637fb1",
      "#bc685d",
      "#655964"
    ],
    "featured": true,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 38
  },
  {
    "id": "NT_071",
    "code": "NT_071",
    "title": "Pudra & Eflatun Degrade Çiçek Bahçesi",
    "category": "cicekli-botanik",
    "category_name": "Çiçekli & Botanik",
    "print_type": "Emprime & Dijital Baskı",
    "separation_ready": true,
    "screen_count": 5,
    "base_price": 180.0,
    "rating": 5.0,
    "reviews_count": 33,
    "tags": [
      "Yeni",
      "Pudra",
      "Eflatun",
      "Degrade",
      "Pastel"
    ],
    "image": "/static/images/NT_071.jpg",
    "pattern_tile": "/static/images/NT_071.jpg",
    "description": "Pudra ve eflatun degrade geçişleriyle büyüleyen çiçek bahçesi.",
    "colors": [
      "#e5b7a3",
      "#8985ab",
      "#926063",
      "#515571"
    ],
    "featured": true,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 49
  },
  {
    "id": "NT_070",
    "code": "NT_070",
    "title": "Gül Kurusu & Terracotta Romantik Çiçekler",
    "category": "cicekli-botanik",
    "category_name": "Çiçekli & Botanik",
    "print_type": "Emprime & Dijital Baskı",
    "separation_ready": true,
    "screen_count": 5,
    "base_price": 175.0,
    "rating": 4.9,
    "reviews_count": 28,
    "tags": [
      "Yeni",
      "Gül Kurusu",
      "Terracotta",
      "Romantik",
      "Bahar"
    ],
    "image": "/static/images/NT_070.jpg",
    "pattern_tile": "/static/images/NT_070.jpg",
    "description": "Gül kurusu ve terracotta kırmızısı sıcak romantik kumaş deseni.",
    "colors": [
      "#c9a091",
      "#9b766c",
      "#e9686a",
      "#895e73"
    ],
    "featured": true,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 43
  },
  {
    "id": "NT_069",
    "code": "NT_069",
    "title": "İndigo & Karamel Sıcak Kontrast Botanik",
    "category": "cicekli-botanik",
    "category_name": "Çiçekli & Botanik",
    "print_type": "Emprime & Dijital Baskı",
    "separation_ready": true,
    "screen_count": 5,
    "base_price": 180.0,
    "rating": 5.0,
    "reviews_count": 35,
    "tags": [
      "Yeni",
      "İndigo",
      "Karamel",
      "Botanik",
      "Zarif"
    ],
    "image": "/static/images/NT_069.jpg",
    "pattern_tile": "/static/images/NT_069.jpg",
    "description": "İndigo mavi zemin üzerinde karamel ve bej yapraklı şık botanik desen.",
    "colors": [
      "#e7be98",
      "#b18b78",
      "#45567d",
      "#313945"
    ],
    "featured": true,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 52
  },
  {
    "id": "NT_068",
    "code": "NT_068",
    "title": "Antrasit & Platin Geometrik Doku Deseni",
    "category": "geometrik-soyut",
    "category_name": "Geometrik & Soyut",
    "print_type": "Emprime & Dijital Baskı",
    "separation_ready": true,
    "screen_count": 4,
    "base_price": 165.0,
    "rating": 4.9,
    "reviews_count": 27,
    "tags": [
      "Yeni",
      "Antrasit",
      "Platin",
      "Geometrik",
      "Modern"
    ],
    "image": "/static/images/NT_068.jpg",
    "pattern_tile": "/static/images/NT_068.jpg",
    "description": "Antrasit ve platin tonlarında sofistike geometrik tekstil dokusu.",
    "colors": [
      "#aaabb5",
      "#6f6575",
      "#454347",
      "#303029"
    ],
    "featured": true,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 45
  },
  {
    "id": "NT_067",
    "code": "NT_067",
    "title": "Hardal Sarısı & Füme Kontrast Çiçekler",
    "category": "cicekli-botanik",
    "category_name": "Çiçekli & Botanik",
    "print_type": "Emprime & Dijital Baskı",
    "separation_ready": true,
    "screen_count": 5,
    "base_price": 175.0,
    "rating": 4.9,
    "reviews_count": 26,
    "tags": [
      "Yeni",
      "Hardal",
      "Füme",
      "Kontrast",
      "Modern"
    ],
    "image": "/static/images/NT_067.jpg",
    "pattern_tile": "/static/images/NT_067.jpg",
    "description": "Hardal sarısı ve dumanlı füme tonlarının modern ve cesur birlikteliği.",
    "colors": [
      "#ecc98b",
      "#a27769",
      "#6a5256",
      "#3e3d45"
    ],
    "featured": true,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 41
  },
  {
    "id": "NT_066",
    "code": "NT_066",
    "title": "Krem & Şeftali Sıcak Pastel Bahar Buketi",
    "category": "cicekli-botanik",
    "category_name": "Çiçekli & Botanik",
    "print_type": "Emprime & Dijital Baskı",
    "separation_ready": true,
    "screen_count": 4,
    "base_price": 175.0,
    "rating": 5.0,
    "reviews_count": 32,
    "tags": [
      "Yeni",
      "Krem",
      "Şeftali",
      "Pastel",
      "Bahar"
    ],
    "image": "/static/images/NT_066.jpg",
    "pattern_tile": "/static/images/NT_066.jpg",
    "description": "Krem saten üstüne şeftali ve somon tonlarında sıcak bahar buketi.",
    "colors": [
      "#eecca2",
      "#dc8f72",
      "#c26b62",
      "#5c5b6a"
    ],
    "featured": true,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 48
  },
  {
    "id": "NT_065",
    "code": "NT_065",
    "title": "Kavun İçi & Mercan Güneş Çiçekleri",
    "category": "cicekli-botanik",
    "category_name": "Çiçekli & Botanik",
    "print_type": "Emprime & Dijital Baskı",
    "separation_ready": true,
    "screen_count": 5,
    "base_price": 170.0,
    "rating": 4.8,
    "reviews_count": 22,
    "tags": [
      "Yeni",
      "Kavun İçi",
      "Mercan",
      "Güneş",
      "Canlı"
    ],
    "image": "/static/images/NT_065.jpg",
    "pattern_tile": "/static/images/NT_065.jpg",
    "description": "Sıcak kavun içi ve mercan sarısı güneş ışıltılı yaz çiçekleri.",
    "colors": [
      "#eda777",
      "#e8766b",
      "#a66561",
      "#59525c"
    ],
    "featured": true,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 36
  },
  {
    "id": "NT_064",
    "code": "NT_064",
    "title": "Pudra Eflatun & Gül Tozu Vintage Buket",
    "category": "cicekli-botanik",
    "category_name": "Çiçekli & Botanik",
    "print_type": "Emprime & Dijital Baskı",
    "separation_ready": true,
    "screen_count": 5,
    "base_price": 175.0,
    "rating": 5.0,
    "reviews_count": 30,
    "tags": [
      "Yeni",
      "Eflatun",
      "Gül Tozu",
      "Vintage",
      "Pastel"
    ],
    "image": "/static/images/NT_064.jpg",
    "pattern_tile": "/static/images/NT_064.jpg",
    "description": "Eflatun ve gül tozu pastel geçişleriyle bezenmiş vintage çiçek buketi.",
    "colors": [
      "#e8e1ee",
      "#d1b4b7",
      "#c9a5a5",
      "#b08c8c"
    ],
    "featured": true,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 47
  },
  {
    "id": "NT_063",
    "code": "NT_063",
    "title": "Safir & Buz Mavisi Degrade Çiçek Deseni",
    "category": "cicekli-botanik",
    "category_name": "Çiçekli & Botanik",
    "print_type": "Emprime & Dijital Baskı",
    "separation_ready": true,
    "screen_count": 4,
    "base_price": 175.0,
    "rating": 4.9,
    "reviews_count": 29,
    "tags": [
      "Yeni",
      "Safir",
      "Buz Mavisi",
      "Degrade",
      "Asil"
    ],
    "image": "/static/images/NT_063.jpg",
    "pattern_tile": "/static/images/NT_063.jpg",
    "description": "Safir mavisi ve buz mavisi degrade geçişli asil kumaş deseni.",
    "colors": [
      "#dfdde9",
      "#8c95bd",
      "#4b5685",
      "#1b284f"
    ],
    "featured": true,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 44
  },
  {
    "id": "NT_062",
    "code": "NT_062",
    "title": "Gece Mavisi & Gül Kurusu Kontrast Çiçekler",
    "category": "cicekli-botanik",
    "category_name": "Çiçekli & Botanik",
    "print_type": "Emprime & Dijital Baskı",
    "separation_ready": true,
    "screen_count": 5,
    "base_price": 185.0,
    "rating": 5.0,
    "reviews_count": 39,
    "tags": [
      "Yeni",
      "Gece Mavisi",
      "Gül Kurusu",
      "Kontrast",
      "Zarif"
    ],
    "image": "/static/images/NT_062.jpg",
    "pattern_tile": "/static/images/NT_062.jpg",
    "description": "Derin mavi zemin ile gül kurusu çiçeklerin göz alıcı şık kontrastı.",
    "colors": [
      "#9c637c",
      "#2e5a86",
      "#1b5883",
      "#15435f"
    ],
    "featured": true,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 58
  },
  {
    "id": "NT_061",
    "code": "NT_061",
    "title": "Hardal & Mercan Canlı Çiçek Buketi",
    "category": "cicekli-botanik",
    "category_name": "Çiçekli & Botanik",
    "print_type": "Emprime & Dijital Baskı",
    "separation_ready": true,
    "screen_count": 5,
    "base_price": 175.0,
    "rating": 4.8,
    "reviews_count": 24,
    "tags": [
      "Yeni",
      "Hardal",
      "Mercan",
      "Canlı",
      "Yaz"
    ],
    "image": "/static/images/NT_061.jpg",
    "pattern_tile": "/static/images/NT_061.jpg",
    "description": "Sıcak hardal ve mercan renkleriyle enerjik ve neşeli çiçek buketi.",
    "colors": [
      "#e5a97c",
      "#bf7b6e",
      "#d56c78",
      "#60534a"
    ],
    "featured": true,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 39
  },
  {
    "id": "NT_060",
    "code": "NT_060",
    "title": "Pudra & Nar Çiçeği Romantik Bahçe",
    "category": "cicekli-botanik",
    "category_name": "Çiçekli & Botanik",
    "print_type": "Emprime & Dijital Baskı",
    "separation_ready": true,
    "screen_count": 5,
    "base_price": 180.0,
    "rating": 5.0,
    "reviews_count": 34,
    "tags": [
      "Yeni",
      "Pudra",
      "Nar Çiçeği",
      "Romantik",
      "Bahar"
    ],
    "image": "/static/images/NT_060.jpg",
    "pattern_tile": "/static/images/NT_060.jpg",
    "description": "Pudra pembe fon üzerine nar çiçeği kırmızısı ışıltılı romantik bahar deseni.",
    "colors": [
      "#d9d3d4",
      "#b98186",
      "#a96767",
      "#514442"
    ],
    "featured": true,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 53
  },
  {
    "id": "NT_059",
    "code": "NT_059",
    "title": "Vizon & Kiremit Rustik Çiçek Serisi",
    "category": "cicekli-botanik",
    "category_name": "Çiçekli & Botanik",
    "print_type": "Emprime & Dijital Baskı",
    "separation_ready": true,
    "screen_count": 5,
    "base_price": 175.0,
    "rating": 4.9,
    "reviews_count": 27,
    "tags": [
      "Yeni",
      "Vizon",
      "Kiremit",
      "Rustik",
      "Asil"
    ],
    "image": "/static/images/NT_059.jpg",
    "pattern_tile": "/static/images/NT_059.jpg",
    "description": "Vizon zemin üzerinde kiremit ve tarçın tonlarında zarif rustik çiçekler.",
    "colors": [
      "#c2a599",
      "#96716f",
      "#7a5c59",
      "#545059"
    ],
    "featured": false,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 40
  },
  {
    "id": "NT_058",
    "code": "NT_058",
    "title": "Kobalt & İndigo Çizgisel Geometrik Çiçekler",
    "category": "cicekli-botanik",
    "category_name": "Çiçekli & Botanik",
    "print_type": "Emprime & Dijital Baskı",
    "separation_ready": true,
    "screen_count": 4,
    "base_price": 170.0,
    "rating": 4.9,
    "reviews_count": 21,
    "tags": [
      "Yeni",
      "Kobalt",
      "İndigo",
      "Geometrik",
      "Modern"
    ],
    "image": "/static/images/NT_058.jpg",
    "pattern_tile": "/static/images/NT_058.jpg",
    "description": "Kobalt ve lacivert tonlarında modern çizgisel dinamik çiçek deseni.",
    "colors": [
      "#7a82af",
      "#6778aa",
      "#64617b",
      "#41424f"
    ],
    "featured": false,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 35
  },
  {
    "id": "NT_057",
    "code": "NT_057",
    "title": "Buz Mavisi & Fuşya Suluboya Çiçek Tarlası",
    "category": "cicekli-botanik",
    "category_name": "Çiçekli & Botanik",
    "print_type": "Emprime & Dijital Baskı",
    "separation_ready": true,
    "screen_count": 5,
    "base_price": 180.0,
    "rating": 5.0,
    "reviews_count": 36,
    "tags": [
      "Yeni",
      "Buz Mavisi",
      "Fuşya",
      "Suluboya",
      "Çiçek Tarlası"
    ],
    "image": "/static/images/NT_057.jpg",
    "pattern_tile": "/static/images/NT_057.jpg",
    "description": "Buz mavisi ferahlığı üzerinde fuşya ve pembe suluboya çiçek tarlası.",
    "colors": [
      "#d5e1f0",
      "#bac4d5",
      "#a38e8f",
      "#6d5f69"
    ],
    "featured": false,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 51
  },
  {
    "id": "NT_056",
    "code": "NT_056",
    "title": "Pastel Mavi & Gri Buket Çiçekleri",
    "category": "cicekli-botanik",
    "category_name": "Çiçekli & Botanik",
    "print_type": "Emprime & Dijital Baskı",
    "separation_ready": true,
    "screen_count": 4,
    "base_price": 165.0,
    "rating": 4.8,
    "reviews_count": 18,
    "tags": [
      "Yeni",
      "Pastel Mavi",
      "Gri",
      "Buket",
      "Sakin"
    ],
    "image": "/static/images/NT_056.jpg",
    "pattern_tile": "/static/images/NT_056.jpg",
    "description": "Sakin pastel mavi ve nötr gri tonlarında dingin çiçek buketi kompozisyonu.",
    "colors": [
      "#d2d4e2",
      "#b3bcd8",
      "#8a8ea5",
      "#4f4d57"
    ],
    "featured": false,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 30
  },
  {
    "id": "NT_055",
    "code": "NT_055",
    "title": "Gece Grisi & Gül Tozu Modern Çiçek Dokusu",
    "category": "cicekli-botanik",
    "category_name": "Çiçekli & Botanik",
    "print_type": "Emprime & Dijital Baskı",
    "separation_ready": true,
    "screen_count": 5,
    "base_price": 175.0,
    "rating": 4.9,
    "reviews_count": 23,
    "tags": [
      "Yeni",
      "Gri",
      "Gül Tozu",
      "Modern",
      "Doku"
    ],
    "image": "/static/images/NT_055.jpg",
    "pattern_tile": "/static/images/NT_055.jpg",
    "description": "Gece grisi ve gül tozu renklerinin dengeli uyumuyla modern tekstil deseni.",
    "colors": [
      "#cfab9f",
      "#726e88",
      "#54536c",
      "#3b4562"
    ],
    "featured": false,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 36
  },
  {
    "id": "NT_054",
    "code": "NT_054",
    "title": "Zümrüt Yeşili & Nil Yeşili Tropikal Yapraklar",
    "category": "cicekli-botanik",
    "category_name": "Çiçekli & Botanik",
    "print_type": "Emprime & Dijital Baskı",
    "separation_ready": true,
    "screen_count": 4,
    "base_price": 175.0,
    "rating": 5.0,
    "reviews_count": 28,
    "tags": [
      "Yeni",
      "Zümrüt",
      "Nil Yeşili",
      "Tropikal",
      "Yaprak"
    ],
    "image": "/static/images/NT_054.jpg",
    "pattern_tile": "/static/images/NT_054.jpg",
    "description": "Derin zümrüt ve canlı nil yeşili tonlarında ferahlatıcı tropikal yaprak deseni.",
    "colors": [
      "#8ebd5a",
      "#4a8956",
      "#1b5848",
      "#063230"
    ],
    "featured": false,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 43
  },
  {
    "id": "NT_053",
    "code": "NT_053",
    "title": "Krem Zemin Terracotta & Kiremit Kır Çiçekleri",
    "category": "cicekli-botanik",
    "category_name": "Çiçekli & Botanik",
    "print_type": "Emprime & Dijital Baskı",
    "separation_ready": true,
    "screen_count": 4,
    "base_price": 170.0,
    "rating": 4.9,
    "reviews_count": 20,
    "tags": [
      "Yeni",
      "Krem",
      "Terracotta",
      "Kiremit",
      "Kır Çiçeği"
    ],
    "image": "/static/images/NT_053.jpg",
    "pattern_tile": "/static/images/NT_053.jpg",
    "description": "Açık krem fon üzerine terracotta ve kiremit tonlarında zarif serpme çiçekler.",
    "colors": [
      "#fafaf9",
      "#d4d4d0",
      "#c1a79a",
      "#b57563"
    ],
    "featured": false,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 34
  },
  {
    "id": "NT_052",
    "code": "NT_052",
    "title": "Pudra & Gül Kurusu Asil Şakayık Bahçesi",
    "category": "cicekli-botanik",
    "category_name": "Çiçekli & Botanik",
    "print_type": "Emprime & Dijital Baskı",
    "separation_ready": true,
    "screen_count": 5,
    "base_price": 180.0,
    "rating": 5.0,
    "reviews_count": 31,
    "tags": [
      "Yeni",
      "Pudra",
      "Gül Kurusu",
      "Şakayık",
      "Zarif"
    ],
    "image": "/static/images/NT_052.jpg",
    "pattern_tile": "/static/images/NT_052.jpg",
    "description": "Yumuşak pudra zemin üzerinde asil gül kurusu ve mercan şakayıklar.",
    "colors": [
      "#f9ebd5",
      "#cfcecc",
      "#bd9c91",
      "#ad4e64"
    ],
    "featured": false,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 49
  },
  {
    "id": "NT_051",
    "code": "NT_051",
    "title": "Pastel Kiremit & Zeytin Yeşili Vintage Botanik",
    "category": "cicekli-botanik",
    "category_name": "Çiçekli & Botanik",
    "print_type": "Emprime & Dijital Baskı",
    "separation_ready": true,
    "screen_count": 5,
    "base_price": 175.0,
    "rating": 4.8,
    "reviews_count": 25,
    "tags": [
      "Yeni",
      "Kiremit",
      "Zeytin",
      "Vintage",
      "Botanik"
    ],
    "image": "/static/images/NT_051.jpg",
    "pattern_tile": "/static/images/NT_051.jpg",
    "description": "Kiremit ve zeytin yeşili uyumuyla harmanlanmış klasik vintage botanik.",
    "colors": [
      "#c8c8a6",
      "#aa8959",
      "#7d4737",
      "#33322f"
    ],
    "featured": false,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 38
  },
  {
    "id": "NT_050",
    "code": "NT_050",
    "title": "Gece Mavisi & İndigo Parlak Tropikal Flora",
    "category": "cicekli-botanik",
    "category_name": "Çiçekli & Botanik",
    "print_type": "Emprime & Dijital Baskı",
    "separation_ready": true,
    "screen_count": 5,
    "base_price": 185.0,
    "rating": 4.9,
    "reviews_count": 27,
    "tags": [
      "Yeni",
      "İndigo",
      "Gece Mavisi",
      "Tropikal",
      "Flora"
    ],
    "image": "/static/images/NT_050.jpg",
    "pattern_tile": "/static/images/NT_050.jpg",
    "description": "Koyu mavi zemin üzerinde parlak gök mavisi ve leylak tropikal flora.",
    "colors": [
      "#d4e9f0",
      "#a1abd4",
      "#7b74ba",
      "#373276"
    ],
    "featured": false,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 46
  },
  {
    "id": "NT_049",
    "code": "NT_049",
    "title": "Leylak & Mürdüm Romantik Suluboya Çiçekler",
    "category": "cicekli-botanik",
    "category_name": "Çiçekli & Botanik",
    "print_type": "Emprime & Dijital Baskı",
    "separation_ready": true,
    "screen_count": 5,
    "base_price": 180.0,
    "rating": 5.0,
    "reviews_count": 37,
    "tags": [
      "Yeni",
      "Leylak",
      "Mürdüm",
      "Suluboya",
      "Romantik"
    ],
    "image": "/static/images/NT_049.jpg",
    "pattern_tile": "/static/images/NT_049.jpg",
    "description": "Pastel leylak ve mürdüm tonlarında romantik degrade suluboya çiçekler.",
    "colors": [
      "#f1f1f0",
      "#d7d1d6",
      "#ada0ae",
      "#785b7d"
    ],
    "featured": false,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 54
  },
  {
    "id": "NT_048",
    "code": "NT_048",
    "title": "Krem & Altın Barok Vintage Bordürlü Buket",
    "category": "barok-etnik",
    "category_name": "Barok & Etnik",
    "print_type": "Emprime & Dijital Baskı",
    "separation_ready": true,
    "screen_count": 6,
    "base_price": 195.0,
    "rating": 5.0,
    "reviews_count": 33,
    "tags": [
      "Yeni",
      "Barok",
      "Krem",
      "Altın",
      "Vintage"
    ],
    "image": "/static/images/NT_048.jpg",
    "pattern_tile": "/static/images/NT_048.jpg",
    "description": "Krem saten zemin üzerinde altın sarısı vintage barok bordür ve çiçekler.",
    "colors": [
      "#ebe5dc",
      "#ac9f8b",
      "#776854",
      "#2d2519"
    ],
    "featured": false,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 50
  },
  {
    "id": "NT_047",
    "code": "NT_047",
    "title": "Toprak & Vizon Etnik Mozaik Desen",
    "category": "barok-etnik",
    "category_name": "Barok & Etnik",
    "print_type": "Emprime & Dijital Baskı",
    "separation_ready": true,
    "screen_count": 4,
    "base_price": 170.0,
    "rating": 4.9,
    "reviews_count": 19,
    "tags": [
      "Yeni",
      "Toprak",
      "Vizon",
      "Etnik",
      "Mozaik"
    ],
    "image": "/static/images/NT_047.jpg",
    "pattern_tile": "/static/images/NT_047.jpg",
    "description": "Doğal toprak tonlarında etnik ve geometrik geçişli sofistike kumaş deseni.",
    "colors": [
      "#c3b194",
      "#8a7a63",
      "#584a3a",
      "#261e15"
    ],
    "featured": false,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 33
  },
  {
    "id": "NT_046",
    "code": "NT_046",
    "title": "Siyah Beyaz Sanatsal Çizgisel Lilyum & Gül",
    "category": "cicekli-botanik",
    "category_name": "Çiçekli & Botanik",
    "print_type": "Emprime & Dijital Baskı",
    "separation_ready": true,
    "screen_count": 3,
    "base_price": 160.0,
    "rating": 4.9,
    "reviews_count": 40,
    "tags": [
      "Yeni",
      "Siyah-Beyaz",
      "Lilyum",
      "Gül",
      "Minimal"
    ],
    "image": "/static/images/NT_046.jpg",
    "pattern_tile": "/static/images/NT_046.jpg",
    "description": "Minimalist ve çarpıcı siyah beyaz illüstrasyon lilyum ve gül deseni.",
    "colors": [
      "#ffffff",
      "#edecea",
      "#9c9995",
      "#212224"
    ],
    "featured": false,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 68
  },
  {
    "id": "NT_045",
    "code": "NT_045",
    "title": "Limon Sarısı & Adaçayı Enerjik Kır Bahçesi",
    "category": "cicekli-botanik",
    "category_name": "Çiçekli & Botanik",
    "print_type": "Emprime & Dijital Baskı",
    "separation_ready": true,
    "screen_count": 5,
    "base_price": 170.0,
    "rating": 4.8,
    "reviews_count": 22,
    "tags": [
      "Yeni",
      "Sarı",
      "Adaçayı",
      "Bahar",
      "Canlı"
    ],
    "image": "/static/images/NT_045.jpg",
    "pattern_tile": "/static/images/NT_045.jpg",
    "description": "Limon sarısı ve adaçayı yeşiliyle bezeli taze bahar çiçekleri deseni.",
    "colors": [
      "#d4d898",
      "#b1b373",
      "#868750",
      "#494b28"
    ],
    "featured": false,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 37
  },
  {
    "id": "NT_044",
    "code": "NT_044",
    "title": "Siyah Zemin Karamel & Altın Varak Şakayık",
    "category": "barok-etnik",
    "category_name": "Barok & Etnik",
    "print_type": "Emprime & Dijital Baskı",
    "separation_ready": true,
    "screen_count": 6,
    "base_price": 190.0,
    "rating": 5.0,
    "reviews_count": 38,
    "tags": [
      "Yeni",
      "Siyah",
      "Karamel",
      "Şakayık",
      "Lüks"
    ],
    "image": "/static/images/NT_044.jpg",
    "pattern_tile": "/static/images/NT_044.jpg",
    "description": "Siyah zemin üzerinde karamel ve altın ışıltılı gösterişli şakayık çiçekleri.",
    "colors": [
      "#dcc1ac",
      "#9b7962",
      "#4e392b",
      "#0a0705"
    ],
    "featured": false,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 59
  },
  {
    "id": "NT_043",
    "code": "NT_043",
    "title": "Bordo & Terracotta Sıcak Çiçek Armonisi",
    "category": "cicekli-botanik",
    "category_name": "Çiçekli & Botanik",
    "print_type": "Emprime & Dijital Baskı",
    "separation_ready": true,
    "screen_count": 5,
    "base_price": 180.0,
    "rating": 4.9,
    "reviews_count": 26,
    "tags": [
      "Yeni",
      "Bordo",
      "Terracotta",
      "Sıcak",
      "Zarif"
    ],
    "image": "/static/images/NT_043.jpg",
    "pattern_tile": "/static/images/NT_043.jpg",
    "description": "Derin bordo ve terracotta tonlarında sıcak ve romantik çiçek kompozisyonu.",
    "colors": [
      "#e7e3df",
      "#64463d",
      "#45261d",
      "#341b13"
    ],
    "featured": false,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 41
  },
  {
    "id": "NT_042",
    "code": "NT_042",
    "title": "Krem Zemin Barok Bej & Varak Saray Çiçekleri",
    "category": "barok-etnik",
    "category_name": "Barok & Etnik",
    "print_type": "Emprime & Dijital Baskı",
    "separation_ready": true,
    "screen_count": 6,
    "base_price": 195.0,
    "rating": 5.0,
    "reviews_count": 44,
    "tags": [
      "Yeni",
      "Barok",
      "Varak",
      "Krem",
      "Lüks",
      "Saray"
    ],
    "image": "/static/images/NT_042.jpg",
    "pattern_tile": "/static/images/NT_042.jpg",
    "description": "Krem zemin üzerinde lüks barok altın varak ve bej tonlarında saray deseni.",
    "colors": [
      "#e3e0d2",
      "#cdc6b6",
      "#897c6a",
      "#2d2b28"
    ],
    "featured": false,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 63
  },
  {
    "id": "NT_041",
    "code": "NT_041",
    "title": "Haki & Zeytin Yeşili Rustik Bahçe Deseni",
    "category": "cicekli-botanik",
    "category_name": "Çiçekli & Botanik",
    "print_type": "Emprime & Dijital Baskı",
    "separation_ready": true,
    "screen_count": 5,
    "base_price": 175.0,
    "rating": 5.0,
    "reviews_count": 35,
    "tags": [
      "Yeni",
      "Haki",
      "Zeytin",
      "Rustik",
      "Doğal"
    ],
    "image": "/static/images/NT_041.jpg",
    "pattern_tile": "/static/images/NT_041.jpg",
    "description": "Toprak ve zeytin yeşili tonlarında zengin yapraklı rustik çiçek buketi.",
    "colors": [
      "#a5a08e",
      "#716855",
      "#544936",
      "#2d261a"
    ],
    "featured": false,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 52
  },
  {
    "id": "NT_040",
    "code": "NT_040",
    "title": "Monokrom Grafit & Antrasit Çizgisel Çiçekler",
    "category": "cicekli-botanik",
    "category_name": "Çiçekli & Botanik",
    "print_type": "Emprime & Dijital Baskı",
    "separation_ready": true,
    "screen_count": 4,
    "base_price": 170.0,
    "rating": 4.9,
    "reviews_count": 29,
    "tags": [
      "Yeni",
      "Monokrom",
      "Grafit",
      "Antrasit",
      "Modern"
    ],
    "image": "/static/images/NT_040.jpg",
    "pattern_tile": "/static/images/NT_040.jpg",
    "description": "Zarif antrasit ve grafit geçişli monokrom sanatsal çiçek kompozisyonu.",
    "colors": [
      "#d3d2d1",
      "#a3a0a0",
      "#5a5558",
      "#18141a"
    ],
    "featured": false,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 48
  },
  {
    "id": "NT_039",
    "code": "NT_039",
    "title": "Karamel & Kahve Tonları Zarif Kır Buketi",
    "category": "cicekli-botanik",
    "category_name": "Çiçekli & Botanik",
    "print_type": "Emprime & Dijital Baskı",
    "separation_ready": true,
    "screen_count": 5,
    "base_price": 180.0,
    "rating": 5.0,
    "reviews_count": 24,
    "tags": [
      "Yeni",
      "Karamel",
      "Toprak",
      "Vizon",
      "Kır Çiçeği"
    ],
    "image": "/static/images/NT_039.jpg",
    "pattern_tile": "/static/images/NT_039.jpg",
    "description": "Karamel, vizon ve kahve geçişleriyle sıcak sonbahar esintili kır çiçekleri.",
    "colors": [
      "#bcb0a1",
      "#85725f",
      "#564637",
      "#221c16"
    ],
    "featured": false,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 39
  },
  {
    "id": "NT_038",
    "code": "NT_038",
    "title": "Pastel Yeşil & Adaçayı Ferah Botanik Doku",
    "category": "cicekli-botanik",
    "category_name": "Çiçekli & Botanik",
    "print_type": "Emprime & Dijital Baskı",
    "separation_ready": true,
    "screen_count": 4,
    "base_price": 165.0,
    "rating": 4.9,
    "reviews_count": 31,
    "tags": [
      "Yeni",
      "Adaçayı",
      "Mint",
      "Botanik",
      "Doğal"
    ],
    "image": "/static/images/NT_038.jpg",
    "pattern_tile": "/static/images/NT_038.jpg",
    "description": "Ferah adaçayı ve mint yeşili tonlarında organik yaprak ve botanik doku deseni.",
    "colors": [
      "#cdd9cd",
      "#b8c5b9",
      "#9daa9f",
      "#59625c"
    ],
    "featured": false,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 55
  },
  {
    "id": "NT_037",
    "code": "NT_037",
    "title": "İndigo & Füme Zemin Pastel Adaçayı Çiçekler",
    "category": "cicekli-botanik",
    "category_name": "Çiçekli & Botanik",
    "print_type": "Emprime & Dijital Baskı",
    "separation_ready": true,
    "screen_count": 5,
    "base_price": 175.0,
    "rating": 5.0,
    "reviews_count": 28,
    "tags": [
      "Yeni",
      "İndigo",
      "Füme",
      "Adaçayı",
      "Pastel",
      "Zarif"
    ],
    "image": "/static/images/NT_037.jpg",
    "pattern_tile": "/static/images/NT_037.jpg",
    "description": "Füme ve indigo zemin üzerine pastel zeytin ve adaçayı tonlarında zarif dikişsiz çiçek deseni.",
    "colors": [
      "#a7a889",
      "#8a7066",
      "#3a4453",
      "#313f51"
    ],
    "featured": false,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 42
  },
  {
    "id": "NT_036",
    "code": "NT_036",
    "title": "Antrasit Zemin Adaçayı & Gül Kurusu Asil Çiçekler",
    "category": "cicekli-botanik",
    "category_name": "Çiçekli & Botanik",
    "print_type": "Emprime & Dijital Baskı",
    "separation_ready": true,
    "screen_count": 6,
    "base_price": 185.0,
    "rating": 5.0,
    "reviews_count": 32,
    "tags": [
      "Yeni",
      "Antrasit",
      "Adaçayı",
      "Gül Kurusu",
      "Asil",
      "Lüks"
    ],
    "image": "/static/images/NT_036.jpg",
    "pattern_tile": "/static/images/NT_036.jpg",
    "description": "Koyu antrasit ve gece mavisi zemin üzerinde adaçayı yeşili ve gül kurusu tonlarında zarif dikişsiz çiçek deseni.",
    "colors": [
      "#b2b78c",
      "#6e6670",
      "#512637",
      "#050f1a"
    ],
    "featured": true,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 45
  },
  {
    "id": "NT_035",
    "code": "NT_035",
    "title": "Siyah Zemin Zeytin Yeşili & Bordo Rustik Çiçekler",
    "category": "cicekli-botanik",
    "category_name": "Çiçekli & Botanik",
    "print_type": "Emprime & Dijital Baskı",
    "separation_ready": true,
    "screen_count": 5,
    "base_price": 185.0,
    "rating": 5.0,
    "reviews_count": 28,
    "tags": [
      "Yeni",
      "Zeytin Yeşili",
      "Bordo",
      "Rustik",
      "Siyah Zemin",
      "Sonbahar"
    ],
    "image": "/static/images/NT_035.jpg",
    "pattern_tile": "/static/images/NT_035.jpg",
    "description": "Siyah zemin üzerinde zeytin yeşili yapraklar ve derin bordo rustik çiçeklerle zenginleştirilmiş kumaş deseni.",
    "colors": [
      "#96a165",
      "#613d2e",
      "#461112",
      "#0e0e0d"
    ],
    "featured": true,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 39
  },
  {
    "id": "NT_034",
    "code": "NT_034",
    "title": "Koyu Mürdüm & Bordo Lüks Saray Çiçekleri",
    "category": "cicekli-botanik",
    "category_name": "Barok & Saray Çiçekleri",
    "print_type": "Emprime & Dijital Baskı",
    "separation_ready": true,
    "screen_count": 7,
    "base_price": 185.0,
    "rating": 5.0,
    "reviews_count": 55,
    "tags": [
      "Yeni",
      "Mürdüm",
      "Bordo",
      "Saray Çiçekleri",
      "Lüks",
      "Zengin Tonlar"
    ],
    "image": "/static/images/NT_034.jpg",
    "pattern_tile": "/static/images/NT_034.jpg",
    "description": "Koyu mürdüm ve bordo zemin üzerinde altın detaylı dev çiçeklerle abiye ve lüks giyim kumaş deseni.",
    "colors": [
      "#b79a6d",
      "#8d4c4f",
      "#7f1958",
      "#180b1f"
    ],
    "featured": true,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 81
  },
  {
    "id": "NT_033",
    "code": "NT_033",
    "title": "Toprak & Bronz Tonları Zarif Kır Çiçekleri",
    "category": "cicekli-botanik",
    "category_name": "Çiçekli & Botanik",
    "print_type": "Dijital & Emprime Baskı",
    "separation_ready": true,
    "screen_count": 5,
    "base_price": 185.0,
    "rating": 5.0,
    "reviews_count": 31,
    "tags": [
      "Yeni",
      "Toprak Tonları",
      "Bronz",
      "Kır Çiçekleri",
      "Pastel"
    ],
    "image": "/static/images/NT_033.jpg",
    "pattern_tile": "/static/images/NT_033.jpg",
    "description": "Toprak tonları ve doğal pastel renklerle hazırlanmış dikişsiz kır çiçeği kompozisyonu.",
    "colors": [
      "#b9a692",
      "#836c59",
      "#694635",
      "#373131"
    ],
    "featured": true,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 46
  },
  {
    "id": "NT_032",
    "code": "NT_032",
    "title": "Siyah Zemin Karamel & Altın Varak Şakayık",
    "category": "cicekli-botanik",
    "category_name": "Çiçekli & Botanik",
    "print_type": "Emprime & Dijital Baskı",
    "separation_ready": true,
    "screen_count": 6,
    "base_price": 185.0,
    "rating": 5.0,
    "reviews_count": 43,
    "tags": [
      "Yeni",
      "Siyah Zemin",
      "Karamel",
      "Altın Varak",
      "Şakayık",
      "Lüks"
    ],
    "image": "/static/images/NT_032.jpg",
    "pattern_tile": "/static/images/NT_032.jpg",
    "description": "Siyah saten zemin üzerinde sıcak karamel ve altın yaldız tonlu şakayık buketi.",
    "colors": [
      "#c5aa7c",
      "#864928",
      "#40170e",
      "#0a0302"
    ],
    "featured": true,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 63
  },
  {
    "id": "NT_031",
    "code": "NT_031",
    "title": "Pudra Zemin Canlı Mercan & Fuşya Şakayıklar",
    "category": "cicekli-botanik",
    "category_name": "Çiçekli & Botanik",
    "print_type": "Dijital Baskı",
    "separation_ready": true,
    "screen_count": 7,
    "base_price": 185.0,
    "rating": 5.0,
    "reviews_count": 49,
    "tags": [
      "Yeni",
      "Mercan",
      "Fuşya",
      "Şakayık",
      "Pudra",
      "Yazlık"
    ],
    "image": "/static/images/NT_031.jpg",
    "pattern_tile": "/static/images/NT_031.jpg",
    "description": "Büyük boy canlı mercan ve fuşya şakayık çiçekleriyle göz alıcı elbise ve etek kumaş deseni.",
    "colors": [
      "#f3e4e6",
      "#ec9861",
      "#e16446",
      "#cc3b67"
    ],
    "featured": true,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 72
  },
  {
    "id": "NT_030",
    "code": "NT_030",
    "title": "Krem Zemin Pastel Kır Çiçekleri & Papatyalar",
    "category": "cicekli-botanik",
    "category_name": "Çiçekli & Botanik",
    "print_type": "Dijital & Emprime Baskı",
    "separation_ready": true,
    "screen_count": 6,
    "base_price": 185.0,
    "rating": 5.0,
    "reviews_count": 38,
    "tags": [
      "Yeni",
      "Krem",
      "Papatya",
      "Kır Çiçekleri",
      "Pastel",
      "Bahar"
    ],
    "image": "/static/images/NT_030.jpg",
    "pattern_tile": "/static/images/NT_030.jpg",
    "description": "Krem zemin üzerinde sarı papatyalar ve kır çiçekleriyle bahar havası taşıyan ferah desen.",
    "colors": [
      "#f6f7e1",
      "#cfc29d",
      "#a07763",
      "#483232"
    ],
    "featured": true,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 56
  },
  {
    "id": "NT_029",
    "code": "NT_029",
    "title": "Kırmızı Gül & Bordo Gece Bahçesi",
    "category": "cicekli-botanik",
    "category_name": "Çiçekli & Botanik",
    "print_type": "Dijital & Emprime Baskı",
    "separation_ready": true,
    "screen_count": 5,
    "base_price": 185.0,
    "rating": 5.0,
    "reviews_count": 27,
    "tags": [
      "Yeni",
      "Kırmızı Gül",
      "Bordo",
      "Gece Bahçesi",
      "Romantik"
    ],
    "image": "/static/images/NT_029.jpg",
    "pattern_tile": "/static/images/NT_029.jpg",
    "description": "Klasik kırmızı güllerin bordo tonlarla birleştiği zamansız kadın giyim deseni.",
    "colors": [
      "#e1cec7",
      "#9a8587",
      "#932f37",
      "#1e1a1d"
    ],
    "featured": true,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 41
  },
  {
    "id": "NT_028",
    "code": "NT_028",
    "title": "Barok Altın & Kiremit Asil Saray Deseni",
    "category": "cicekli-botanik",
    "category_name": "Barok & Saray Çiçekleri",
    "print_type": "Emprime & Dijital Baskı",
    "separation_ready": true,
    "screen_count": 6,
    "base_price": 185.0,
    "rating": 5.0,
    "reviews_count": 45,
    "tags": [
      "Yeni",
      "Barok",
      "Altın Varak",
      "Kiremit",
      "Saray",
      "Lüks"
    ],
    "image": "/static/images/NT_028.jpg",
    "pattern_tile": "/static/images/NT_028.jpg",
    "description": "Zarif saray işlemeleri, altın sarısı kontürler ve zengin kiremit çiçeklerle lüks kumaş baskı deseni.",
    "colors": [
      "#d2c29a",
      "#ae9a61",
      "#84433e",
      "#2a312f"
    ],
    "featured": true,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 68
  },
  {
    "id": "NT_027",
    "code": "NT_027",
    "title": "Gece Mavisi Zemin Altın Varak & Hardal Çiçekler",
    "category": "cicekli-botanik",
    "category_name": "Çiçekli & Botanik",
    "print_type": "Emprime & Dijital Baskı",
    "separation_ready": true,
    "screen_count": 6,
    "base_price": 185.0,
    "rating": 5.0,
    "reviews_count": 37,
    "tags": [
      "Yeni",
      "Gece Mavisi",
      "Altın Varak",
      "Hardal",
      "Lüks",
      "Saray"
    ],
    "image": "/static/images/NT_027.jpg",
    "pattern_tile": "/static/images/NT_027.jpg",
    "description": "Koyu lacivert zemin üzerinde altın sarısı ve hardal çiçek desenleri.",
    "colors": [
      "#cac593",
      "#8f824f",
      "#504c39",
      "#080c24"
    ],
    "featured": true,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 54
  },
  {
    "id": "NT_026",
    "code": "NT_026",
    "title": "Adaçayı Yeşili & Bordo Rustik Botanik",
    "category": "cicekli-botanik",
    "category_name": "Çiçekli & Botanik",
    "print_type": "Dijital & Emprime Baskı",
    "separation_ready": true,
    "screen_count": 5,
    "base_price": 185.0,
    "rating": 5.0,
    "reviews_count": 33,
    "tags": [
      "Yeni",
      "Adaçayı",
      "Haki",
      "Bordo",
      "Rustik",
      "Botanik"
    ],
    "image": "/static/images/NT_026.jpg",
    "pattern_tile": "/static/images/NT_026.jpg",
    "description": "Adaçayı yeşili, zeytin yaprakları ve bordo çiçek detaylarıyla sakin ve seçkin bir tasarım.",
    "colors": [
      "#a1b69b",
      "#6b625b",
      "#4c2028",
      "#090d10"
    ],
    "featured": true,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 47
  },
  {
    "id": "NT_025",
    "code": "NT_025",
    "title": "Pudra Gül Kurusu & Kiremit Asil Buket",
    "category": "cicekli-botanik",
    "category_name": "Çiçekli & Botanik",
    "print_type": "Emprime & Dijital Baskı",
    "separation_ready": true,
    "screen_count": 5,
    "base_price": 185.0,
    "rating": 5.0,
    "reviews_count": 36,
    "tags": [
      "Yeni",
      "Gül Kurusu",
      "Kiremit",
      "Pudra",
      "Asil",
      "Lüks"
    ],
    "image": "/static/images/NT_025.jpg",
    "pattern_tile": "/static/images/NT_025.jpg",
    "description": "Pudra ve gül kurusu tonlarında kiremit dokunuşlu asil ve şık dikişsiz çiçek deseni.",
    "colors": [
      "#c79981",
      "#8e525a",
      "#47202e",
      "#0b0b0d"
    ],
    "featured": true,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 52
  },
  {
    "id": "NT_024",
    "code": "NT_024",
    "title": "Karamel & Bronz Toprak Tonları Etnik Çiçekler",
    "category": "cicekli-botanik",
    "category_name": "Çiçekli & Botanik",
    "print_type": "Dijital & Emprime Baskı",
    "separation_ready": true,
    "screen_count": 5,
    "base_price": 185.0,
    "rating": 5.0,
    "reviews_count": 29,
    "tags": [
      "Yeni",
      "Karamel",
      "Bronz",
      "Toprak Tonları",
      "Etnik",
      "Sonbahar"
    ],
    "image": "/static/images/NT_024.jpg",
    "pattern_tile": "/static/images/NT_024.jpg",
    "description": "Sıcak toprak tonları, karamel ve bronz yapraklarla sonbahar / kış modasına uygun şık desen.",
    "colors": [
      "#c7a586",
      "#925735",
      "#301915",
      "#040506"
    ],
    "featured": true,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 42
  },
  {
    "id": "NT_023",
    "code": "NT_023",
    "title": "Siyah Zemin Canlı Turuncu & Kırmızı Alev Çiçekleri",
    "category": "cicekli-botanik",
    "category_name": "Çiçekli & Botanik",
    "print_type": "Emprime & Dijital Baskı",
    "separation_ready": true,
    "screen_count": 5,
    "base_price": 185.0,
    "rating": 5.0,
    "reviews_count": 40,
    "tags": [
      "Yeni",
      "Siyah Zemin",
      "Turuncu",
      "Kırmızı",
      "Canlı",
      "Alev"
    ],
    "image": "/static/images/NT_023.jpg",
    "pattern_tile": "/static/images/NT_023.jpg",
    "description": "Siyah zemin üzerinde ateş kırmızısı ve parlak turuncu çiçeklerin enerjik dansı.",
    "colors": [
      "#df6919",
      "#a3352c",
      "#76151f",
      "#010201"
    ],
    "featured": true,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 65
  },
  {
    "id": "NT_022",
    "code": "NT_022",
    "title": "Siyah Zemin Karamel & Bordo Barok Çiçekler",
    "category": "cicekli-botanik",
    "category_name": "Çiçekli & Botanik",
    "print_type": "Emprime & Dijital Baskı",
    "separation_ready": true,
    "screen_count": 6,
    "base_price": 185.0,
    "rating": 5.0,
    "reviews_count": 35,
    "tags": [
      "Yeni",
      "Siyah Zemin",
      "Karamel",
      "Bordo",
      "Barok",
      "Lüks"
    ],
    "image": "/static/images/NT_022.jpg",
    "pattern_tile": "/static/images/NT_022.jpg",
    "description": "Siyah antrasit zemin üzerinde lüks karamel ve bordo tonlu barok çiçek desenleri.",
    "colors": [
      "#be9275",
      "#8d4f51",
      "#511c27",
      "#010101"
    ],
    "featured": true,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 58
  },
  {
    "id": "NT_021",
    "code": "NT_021",
    "title": "Krem Zemin Pastel Bordo Çiçek Bahçesi",
    "category": "cicekli-botanik",
    "category_name": "Çiçekli & Botanik",
    "print_type": "Dijital & Emprime Baskı",
    "separation_ready": true,
    "screen_count": 5,
    "base_price": 185.0,
    "rating": 5.0,
    "reviews_count": 21,
    "tags": [
      "Yeni",
      "Krem",
      "Bordo",
      "Pastel",
      "Kır Çiçekleri"
    ],
    "image": "/static/images/NT_021.jpg",
    "pattern_tile": "/static/images/NT_021.jpg",
    "description": "Doğal krem kumaş zeminine uyumlu bordo ve pastel pudra çiçek buketi.",
    "colors": [
      "#e7dfd5",
      "#dcd1c6",
      "#d0b3a0",
      "#8c5156"
    ],
    "featured": true,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 37
  },
  {
    "id": "NT_020",
    "code": "NT_020",
    "title": "Canlı Mor & Orkide Tropikal Buket",
    "category": "cicekli-botanik",
    "category_name": "Çiçekli & Botanik",
    "print_type": "Dijital & Emprime Baskı",
    "separation_ready": true,
    "screen_count": 6,
    "base_price": 185.0,
    "rating": 5.0,
    "reviews_count": 30,
    "tags": [
      "Yeni",
      "Orkide",
      "Mor",
      "Tropikal",
      "Canlı Renkler"
    ],
    "image": "/static/images/NT_020.jpg",
    "pattern_tile": "/static/images/NT_020.jpg",
    "description": "Derin mor ve orkide moru tonlarında göz alıcı çiçek kompozisyonu.",
    "colors": [
      "#cd93c5",
      "#c05fcc",
      "#b83dab",
      "#592664"
    ],
    "featured": true,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 48
  },
  {
    "id": "NT_019",
    "code": "NT_019",
    "title": "Leylak & Mor Degrade Suluboya Çiçekler",
    "category": "cicekli-botanik",
    "category_name": "Çiçekli & Botanik",
    "print_type": "Dijital Baskı",
    "separation_ready": true,
    "screen_count": 7,
    "base_price": 185.0,
    "rating": 5.0,
    "reviews_count": 26,
    "tags": [
      "Yeni",
      "Leylak",
      "Mor",
      "Degrade",
      "Suluboya",
      "Zarif"
    ],
    "image": "/static/images/NT_019.jpg",
    "pattern_tile": "/static/images/NT_019.jpg",
    "description": "Pastel lila ve mor tonlarında degrade suluboya dokularla harmanlanmış şık elbise deseni.",
    "colors": [
      "#eacbe7",
      "#e3bedc",
      "#c984aa",
      "#8e2b69"
    ],
    "featured": true,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 44
  },
  {
    "id": "NT_018",
    "code": "NT_018",
    "title": "Pudra Pembe & Fuşya Romantik Çiçekler",
    "category": "cicekli-botanik",
    "category_name": "Çiçekli & Botanik",
    "print_type": "Dijital Baskı",
    "separation_ready": true,
    "screen_count": 6,
    "base_price": 185.0,
    "rating": 5.0,
    "reviews_count": 32,
    "tags": [
      "Yeni",
      "Pudra Pembe",
      "Fuşya",
      "Romantik",
      "Çiçekli",
      "Yazlık"
    ],
    "image": "/static/images/NT_018.jpg",
    "pattern_tile": "/static/images/NT_018.jpg",
    "description": "Canlı pudra pembe, fuşya ve gül tonlarıyla yazlık elbise ve bluzlar için ideal dikişsiz kumaş deseni.",
    "colors": [
      "#fbaabb",
      "#f597ae",
      "#c86e93",
      "#9d2663"
    ],
    "featured": true,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 51
  },
  {
    "id": "NT_017",
    "code": "NT_017",
    "title": "Vintage Pastel Gül & Kır Bahçesi",
    "category": "cicekli-botanik",
    "category_name": "Çiçekli & Botanik",
    "print_type": "Dijital & Emprime Baskı",
    "separation_ready": true,
    "screen_count": 5,
    "base_price": 185.0,
    "rating": 5.0,
    "reviews_count": 24,
    "tags": [
      "Yeni",
      "Gül",
      "Vintage",
      "Pastel",
      "Kahve & Krem",
      "Romantik"
    ],
    "image": "/static/images/NT_017.jpg",
    "pattern_tile": "/static/images/NT_017.jpg",
    "description": "Romantik eskitme tonlarda pastel güller ve zarif dallarla tasarlanmış yüksek çözünürlüklü kumaş deseni.",
    "colors": [
      "#d0cbc1",
      "#9c8f7c",
      "#766552",
      "#413125"
    ],
    "featured": true,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 39
  },
  {
    "id": "NT_016",
    "code": "NT_016",
    "title": "Sıcak Pastel Bej & Terracotta Çiçek Bahçesi",
    "category": "cicekli-botanik",
    "category_name": "Çiçekli & Botanik",
    "print_type": "Dijital & Emprime Baskı",
    "separation_ready": true,
    "screen_count": 6,
    "base_price": 185.0,
    "rating": 5.0,
    "reviews_count": 28,
    "tags": [
      "Yeni",
      "Pastel",
      "Terracotta",
      "Bej",
      "Çiçek Bahçesi",
      "Dikişsiz Rapor"
    ],
    "image": "/static/images/NT_016.jpg",
    "pattern_tile": "/static/images/NT_016.jpg",
    "description": "Trenddesen yeni sezon özel tasarımı. Sıcak bej zemin üzerinde terracotta, karamel ve krem tonlarında dikişsiz çiçek deseni.",
    "colors": [
      "#e7d1bd",
      "#d9b89c",
      "#c79e7f",
      "#b76d4e"
    ],
    "featured": true,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 45
  },
  {
    "id": "NT_015",
    "code": "NT_015",
    "title": "Gece Mavisi Sulu Boya Sanatsal Çiçek Tablosu",
    "category": "soyut-mermer",
    "category_name": "Sulu Boya & Sanatsal Çiçekler",
    "print_type": "Dijital Baskı",
    "separation_ready": true,
    "screen_count": 8,
    "base_price": 185.0,
    "rating": 5.0,
    "reviews_count": 31,
    "tags": [
      "Yeni",
      "Sulu Boya",
      "Gece Mavisi",
      "Sarı Çiçek",
      "Sanatsal Tablo"
    ],
    "image": "/static/images/NT_015.jpg",
    "pattern_tile": "/static/images/NT_015.jpg",
    "description": "Derin gece mavisi ve çivit sulu boya akıntıları üzerinde sarı ve beyaz anemon çiçekleriyle galeri tablosu niteliğinde çarpıcı dijital baskı deseni.",
    "colors": [
      "#25295c",
      "#3d4b8f",
      "#f7bf46",
      "#f2efe9"
    ],
    "featured": true,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 49
  },
  {
    "id": "NT_014",
    "code": "NT_014",
    "title": "Siyah Beyaz Monokrom Çizgisel Şakayık & Lilyum",
    "category": "cicekli-botanik",
    "category_name": "Monokrom & Çizgisel Sanat",
    "print_type": "Emprime & Dijital Uyumlu",
    "separation_ready": true,
    "screen_count": 2,
    "base_price": 185.0,
    "rating": 5.0,
    "reviews_count": 25,
    "tags": [
      "Yeni",
      "Monokrom",
      "Siyah Beyaz",
      "Şakayık",
      "Çizgisel",
      "Asil"
    ],
    "image": "/static/images/NT_014.jpg",
    "pattern_tile": "/static/images/NT_014.jpg",
    "description": "Antrasit siyah zemin üzerinde yüksek kontrastlı beyaz gravür şakayık, zambak ve yaprak illüstrasyonları içeren şık ve lüks kumaş deseni.",
    "colors": [
      "#1c1d1f",
      "#ffffff",
      "#3b3c3e",
      "#e5e7eb"
    ],
    "featured": true,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 56
  },
  {
    "id": "NT_013",
    "code": "NT_013",
    "title": "Siyah Zemin Degrade Çizgisel Çiçekler & Kasımpatı",
    "category": "cicekli-botanik",
    "category_name": "Çizgisel Sanat & Etnik Çiçekler",
    "print_type": "Emprime & Dijital Uyumlu",
    "separation_ready": true,
    "screen_count": 5,
    "base_price": 185.0,
    "rating": 5.0,
    "reviews_count": 34,
    "tags": [
      "Yeni",
      "Siyah Zemin",
      "Degrade",
      "Kırmızı",
      "Mavi",
      "Kasımpatı",
      "Modern"
    ],
    "image": "/static/images/NT_013.jpg",
    "pattern_tile": "/static/images/NT_013.jpg",
    "description": "Siyah antrasit zemin üzerinde turuncu, kırmızı, mor ve elektrik mavisi degrade çizgisel kasımpatı ve papatya motifleriyle dinamik moda kumaş deseni.",
    "colors": [
      "#000000",
      "#ea580c",
      "#3b82f6",
      "#9333ea"
    ],
    "featured": true,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 63
  },
  {
    "id": "NT_012",
    "code": "NT_012",
    "title": "Romantik Pastel Mavi & Leylak Gül Buketi",
    "category": "cicekli-botanik",
    "category_name": "Çiçekli & Botanik",
    "print_type": "Emprime & Dijital Uyumlu",
    "separation_ready": true,
    "screen_count": 6,
    "base_price": 185.0,
    "rating": 5.0,
    "reviews_count": 18,
    "tags": [
      "Yeni",
      "Gül",
      "Pastel Mavi",
      "Leylak",
      "Romantik",
      "Vintage"
    ],
    "image": "/static/images/NT_012.jpg",
    "pattern_tile": "/static/images/NT_012.jpg",
    "description": "Trenddesen özel romantik koleksiyonu. Pudra zemin üzerinde pastel mavi katmerli güller, leylak goncalar ve zarafet dolu dikişsiz çiçek deseni.",
    "colors": [
      "#a4b2c6",
      "#c3a5bc",
      "#e8e1df",
      "#939ea0"
    ],
    "featured": true,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 38
  },
  {
    "id": "NT_011",
    "code": "NT_011",
    "title": "Pastel Gri Mavi & Gül Kurusu Vintage Çiçekler",
    "category": "cicekli-botanik",
    "category_name": "Çiçekli & Botanik",
    "print_type": "Dijital Baskı",
    "separation_ready": true,
    "screen_count": 6,
    "base_price": 185.0,
    "rating": 5.0,
    "reviews_count": 27,
    "tags": [
      "Yeni",
      "Gül Kurusu",
      "Pastel Mavi",
      "Vintage",
      "Çiçekli",
      "Dikişsiz Rapor"
    ],
    "image": "/static/images/NT_011.jpg",
    "pattern_tile": "/static/images/NT_011.jpg",
    "description": "Trenddesen yeni sezon özel tasarımı. Pastel mavi, gri ve gül kurusu tonlarında lüks dikişsiz çiçek deseni (4961x4961 HD).",
    "colors": [
      "#809fad",
      "#776f83",
      "#833c65",
      "#262827"
    ],
    "featured": true,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 52
  },
  {
    "id": "NT_010",
    "code": "NT_010",
    "title": "Soyut Dijital Anemon & Şakayık Bahçesi",
    "category": "cicekli-botanik",
    "category_name": "Çiçekli & Botanik",
    "print_type": "Emprime & Dijital Uyumlu",
    "separation_ready": true,
    "screen_count": 6,
    "base_price": 185.0,
    "rating": 5.0,
    "reviews_count": 16,
    "tags": [
      "Yeni",
      "Soyut",
      "Anemon",
      "Şakayık",
      "Degrade",
      "Canlı Renkler"
    ],
    "image": "/static/images/NT_010.jpg",
    "pattern_tile": "/static/images/NT_010.jpg",
    "description": "Trenddesen yeni sezon özel tasarımı. Degrade taç yapraklar, canlı anemon ve şakayık çiçekleriyle modern sanatsal dijital baskı kumaş deseni.",
    "colors": [
      "#dcd0d1",
      "#b09390",
      "#955446",
      "#3b3439"
    ],
    "featured": true,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 35
  },
  {
    "id": "NT_009",
    "code": "NT_009",
    "title": "Barok Altın Varak Saray Çiçeği Deseni",
    "category": "leopar-hayvan",
    "category_name": "Barok, Kemer, Zincir, Dekoratif Hayvan Desenleri",
    "print_type": "Emprime & Dijital Uyumlu",
    "separation_ready": true,
    "screen_count": 4,
    "base_price": 185.0,
    "rating": 5.0,
    "reviews_count": 29,
    "tags": [
      "Yeni",
      "Barok",
      "Altın Varak",
      "Saray",
      "Lüks",
      "Zengin Doku"
    ],
    "image": "/static/images/NT_009.jpg",
    "pattern_tile": "/static/images/NT_009.jpg",
    "description": "Trenddesen yeni sezon özel tasarımı. Siyah zemin üzerine lüks altın varak ve saray nakışı efektli dikişsiz kumaş deseni.",
    "colors": [
      "#fef08a",
      "#d97706",
      "#92400e",
      "#1c1917"
    ],
    "featured": true,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 58
  },
  {
    "id": "NT_008",
    "code": "NT_008",
    "title": "Pastel Çizgili Papatya & Boncuk Deseni",
    "category": "cicekli-botanik",
    "category_name": "Çizgili & Geometrik Çiçekler",
    "print_type": "Emprime & Dijital Uyumlu",
    "separation_ready": true,
    "screen_count": 5,
    "base_price": 185.0,
    "rating": 5.0,
    "reviews_count": 21,
    "tags": [
      "Yeni",
      "Papatya",
      "Çizgili",
      "Boncuk",
      "Pastel Pembe",
      "Bahar"
    ],
    "image": "/static/images/NT_008.jpg",
    "pattern_tile": "/static/images/NT_008.jpg",
    "description": "Trenddesen yeni sezon özel tasarımı. Pembe ve bej dikey çizgiler üzerinde papatyalar ve boncuklu motifler içeren dikişsiz yazlık elbise deseni.",
    "colors": [
      "#e7dad6",
      "#a19c96",
      "#695f57",
      "#3c3a38"
    ],
    "featured": true,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 42
  },
  {
    "id": "NT_007",
    "code": "NT_007",
    "title": "Vintage Çizgili Bordo Gül Deseni",
    "category": "cicekli-botanik",
    "category_name": "Çiçekli & Botanik",
    "print_type": "Emprime & Dijital Uyumlu",
    "separation_ready": true,
    "screen_count": 6,
    "base_price": 185.0,
    "rating": 5.0,
    "reviews_count": 16,
    "tags": [
      "Yeni",
      "Gül",
      "Çizgili",
      "Vintage",
      "Bordo",
      "Altın Kontür"
    ],
    "image": "/static/images/NT_007.jpg",
    "pattern_tile": "/static/images/NT_007.jpg",
    "description": "Trenddesen yeni sezon özel tasarımı. Çizgili zemin üzerinde lüks bordo güller, altın kontürlü yapraklar ve goncalar içeren yüksek çözünürlüklü dijital baskı kumaş deseni.",
    "colors": [
      "#d9d5c1",
      "#9f907b",
      "#7c5851",
      "#3f4040"
    ],
    "featured": true,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 35
  },
  {
    "id": "NT_006",
    "code": "NT_006",
    "title": "Leopar Zincir Deseni",
    "category": "leopar-hayvan",
    "category_name": "Barok, Kemer, Zincir, Dekoratif Hayvan Desenleri",
    "print_type": "Emprime & Dijital Uyumlu",
    "separation_ready": true,
    "screen_count": 6,
    "base_price": 185.0,
    "rating": 5.0,
    "reviews_count": 14,
    "tags": [
      "Yeni",
      "Leopar",
      "Zincir",
      "Barok",
      "Kemer"
    ],
    "image": "/static/images/NT_006.jpg",
    "pattern_tile": "/static/images/NT_006.jpg",
    "description": "Trenddesen yeni sezon özel dijital baskı deseni. Barok kemer, zincir ve vahşi doğa leopar motifli yüksek çözünürlüklü kumaş deseni.",
    "colors": [
      "#d97706",
      "#1e293b",
      "#047857",
      "#fef08a"
    ],
    "featured": true,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 48
  },
  {
    "id": "NT_005",
    "code": "NT_005",
    "title": "Kırık Cam Deseni",
    "category": "soyut-mermer",
    "category_name": "Batik, - Eskitme Değişik dokular",
    "print_type": "Dijital & Emprime Uyumlu",
    "separation_ready": true,
    "screen_count": 5,
    "base_price": 185.0,
    "rating": 5.0,
    "reviews_count": 19,
    "tags": [
      "Yeni",
      "Kırık Cam",
      "Soyut",
      "Mermer",
      "Batik"
    ],
    "image": "/static/images/NT_005.jpg",
    "pattern_tile": "/static/images/NT_005.jpg",
    "description": "Trenddesen yeni sezon özel dijital baskı deseni. Modern soyut kırık cam ve eskitme batik doku.",
    "colors": [
      "#f97316",
      "#06b6d4",
      "#64748b",
      "#f8fafc"
    ],
    "featured": true,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 41
  },
  {
    "id": "NT_004",
    "code": "NT_004",
    "title": "Bahar Çiçekleri",
    "category": "cicekli-botanik",
    "category_name": "Çiçekli & Botanik",
    "print_type": "Emprime & Dijital Uyumlu",
    "separation_ready": true,
    "screen_count": 5,
    "base_price": 185.0,
    "rating": 5.0,
    "reviews_count": 22,
    "tags": [
      "Yeni",
      "Çiçekli",
      "Bahar",
      "Pastel"
    ],
    "image": "/static/images/NT_004.jpg",
    "pattern_tile": "/static/images/NT_004.jpg",
    "description": "Trenddesen yeni sezon özel dijital baskı deseni. Bahar tazeliğinde renkli çiçek kompozisyonu.",
    "colors": [
      "#f43f5e",
      "#10b981",
      "#fbbf24",
      "#ffffff"
    ],
    "featured": true,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 38
  },
  {
    "id": "NT_003",
    "code": "NT_003",
    "title": "Mor Gül Bahçesi",
    "category": "cicekli-botanik",
    "category_name": "Çiçekli & Botanik",
    "print_type": "Emprime & Dijital Uyumlu",
    "separation_ready": true,
    "screen_count": 6,
    "base_price": 185.0,
    "rating": 5.0,
    "reviews_count": 31,
    "tags": [
      "Yeni",
      "Gül",
      "Mor",
      "Botanik"
    ],
    "image": "/static/images/NT_003.jpg",
    "pattern_tile": "/static/images/NT_003.jpg",
    "description": "Trenddesen yeni sezon özel dijital baskı deseni. Mor ve leylak tonlarında güller ve yapraklar.",
    "colors": [
      "#8b5cf6",
      "#ec4899",
      "#059669",
      "#1e293b"
    ],
    "featured": true,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 52
  },
  {
    "id": "NT_002",
    "code": "NT_002",
    "title": "Papatya Bahçesi",
    "category": "cicekli-botanik",
    "category_name": "Çiçekli & Botanik",
    "print_type": "Emprime & Dijital Uyumlu",
    "separation_ready": true,
    "screen_count": 5,
    "base_price": 185.0,
    "rating": 5.0,
    "reviews_count": 27,
    "tags": [
      "Yeni",
      "Papatya",
      "Sarı",
      "Bahar"
    ],
    "image": "/static/images/NT_002.jpg",
    "pattern_tile": "/static/images/NT_002.jpg",
    "description": "Trenddesen yeni sezon özel dijital baskı deseni. Neşeli sarı papatyalar ve kır çiçekleri.",
    "colors": [
      "#eab308",
      "#ffffff",
      "#15803d",
      "#3b82f6"
    ],
    "featured": true,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 64
  },
  {
    "id": "NT_001",
    "code": "NT_001",
    "title": "Sulu Boya Çiçek Bahçesi",
    "category": "cicekli-botanik",
    "category_name": "Çiçekli & Botanik",
    "print_type": "Emprime & Dijital Uyumlu",
    "separation_ready": true,
    "screen_count": 6,
    "base_price": 185.0,
    "rating": 5.0,
    "reviews_count": 45,
    "tags": [
      "Yeni",
      "Sulu Boya",
      "Çiçekli",
      "Bahar"
    ],
    "image": "/static/images/NT_001.jpg",
    "pattern_tile": "/static/images/NT_001.jpg",
    "description": "Trenddesen yeni sezon özel dijital baskı deseni. Canlı sulu boya tekniğiyle hazırlanmış çiçek buketi.",
    "colors": [
      "#ef4444",
      "#10b981",
      "#3b82f6",
      "#f59e0b"
    ],
    "featured": true,
    "is_new": true,
    "discount_pct": 0,
    "sales_count": 85
  }
]''')

def load_json(filename):
    if filename == "products.json":
        path = os.path.join(DATA_DIR, filename)
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list) and len(data) >= len(DEFAULT_PRODUCTS):
                        return data
            except Exception:
                pass
        try:
            save_json("products.json", DEFAULT_PRODUCTS)
        except Exception:
            pass
        return DEFAULT_PRODUCTS

    path = os.path.join(DATA_DIR, filename)
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if data:
                    return data
        except Exception:
            pass
    return []

def save_json(filename, data):
    os.makedirs(DATA_DIR, exist_ok=True)
    path = os.path.join(DATA_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

ADMIN_USERS = {
    "admin": os.getenv("ADMIN_PASSWORD", "nevartrend2026"),
    "moderator": os.getenv("MODERATOR_PASSWORD", "trend2026")
}
ADMIN_SESSION_TOKEN = "nevartrend_secret_admin_token_2026"

def is_admin(request: Request) -> bool:
    try:
        token = request.cookies.get("nevartrend_admin_auth")
        return token == ADMIN_SESSION_TOKEN
    except Exception:
        return False

def render(request: Request, template_name: str, context: dict = None):
    ctx = context or {}
    ctx["request"] = request
    ctx["is_admin"] = is_admin(request)
    return templates.TemplateResponse(request=request, name=template_name, context=ctx)


# --- Web Pages ---

@app.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    products = load_json("products.json")
    fabrics = load_json("fabric_types.json")
    categories = load_json("categories.json")
    featured_products = [p for p in products if p.get("featured", False)]
    new_products = [p for p in products if p.get("is_new", False)]
    return render(request, "index.html", {
        "products": products,
        "featured_products": featured_products,
        "new_products": new_products,
        "fabrics": fabrics,
        "categories": categories,
        "active_page": "home"
    })

@app.get("/emprime", response_class=HTMLResponse)
@app.get("/emprime-renk-ayrimi", response_class=HTMLResponse)
async def emprime_page(request: Request):
    return render(request, "emprime.html", {
        "active_page": "emprime"
    })

@app.get("/kumaslar", response_class=HTMLResponse)
async def kumaslar_page(request: Request):
    fabrics = load_json("fabric_types.json")
    return render(request, "kumaslar.html", {
        "fabrics": fabrics,
        "active_page": "kumaslar"
    })

@app.get("/dijital-baski", response_class=HTMLResponse)
async def dijital_baski_page(request: Request):
    return render(request, "dijital_baski.html", {
        "active_page": "dijital-baski"
    })

@app.get("/trend-urunler", response_class=HTMLResponse)
@app.get("/diger-trend-urunler", response_class=HTMLResponse)
async def trend_urunler_page(request: Request):
    return render(request, "trend_urunler.html", {
        "active_page": "trend-urunler"
    })

@app.get("/desenler", response_class=HTMLResponse)
@app.get("/fabrics", response_class=HTMLResponse)
async def fabrics_catalog(
    request: Request,
    category: Optional[str] = "all",
    fabric: Optional[str] = None,
    q: Optional[str] = None,
    sort: Optional[str] = "popular"
):
    products = load_json("products.json")
    fabrics = load_json("fabric_types.json")
    categories = load_json("categories.json")

    # Normalize category
    if category in [None, "", "desenler", "all"]:
        selected_cat = "all"
        filtered = products
    elif category == "emprime-desenleri":
        selected_cat = "emprime-desenleri"
        filtered = [p for p in products if p.get("separation_ready") or "emprime" in p.get("print_type", "").lower()]
    else:
        selected_cat = category
        filtered = [p for p in products if p.get("category") == category]

    if q:
        query = q.lower().strip()
        filtered = [
            p for p in filtered 
            if query in p.get("title", "").lower() 
            or query in p.get("code", "").lower() 
            or query in p.get("description", "").lower()
            or any(query in tag.lower() for tag in p.get("tags", []))
        ]

    if sort == "price_asc":
        filtered = sorted(filtered, key=lambda x: x.get("base_price", 0))
    elif sort == "price_desc":
        filtered = sorted(filtered, key=lambda x: x.get("base_price", 0), reverse=True)
    elif sort == "rating":
        filtered = sorted(filtered, key=lambda x: x.get("rating", 0), reverse=True)
    else:  # popular / default
        filtered = sorted(filtered, key=lambda x: x.get("sales_count", 0), reverse=True)

    for cat in categories:
        if cat["id"] == "all":
            cat["count"] = len(products)
        elif cat["id"] == "emprime-desenleri":
            cat["count"] = len([p for p in products if p.get("separation_ready") or "emprime" in p.get("print_type", "").lower()])
        else:
            cat["count"] = len([p for p in products if p.get("category") == cat["id"]])

    return render(request, "fabrics.html", {
        "products": filtered,
        "fabrics": fabrics,
        "categories": categories,
        "selected_category": selected_cat,
        "selected_fabric": fabric,
        "search_query": q or "",
        "selected_sort": sort,
        "active_page": "desenler"
    })

@app.get("/product/{product_id}", response_class=HTMLResponse)
async def product_detail(request: Request, product_id: str):
    products = load_json("products.json")
    fabrics = load_json("fabric_types.json")
    
    product = next((p for p in products if p["id"] == product_id or p["code"] == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Desen bulunamadı")

    related = [p for p in products if p["category"] == product["category"] and p["id"] != product["id"]][:4]
    if len(related) < 4:
        more = [p for p in products if p["id"] != product["id"] and p not in related]
        related.extend(more[: 4 - len(related)])

    return render(request, "product-detail.html", {
        "product": product,
        "fabrics": fabrics,
        "related_products": related,
        "active_page": "fabrics"
    })

@app.get("/cart", response_class=HTMLResponse)
async def cart_page(request: Request):
    return render(request, "cart.html", {"active_page": "cart"})

@app.get("/checkout", response_class=HTMLResponse)
async def checkout_page(request: Request):
    fabrics = load_json("fabric_types.json")
    return render(request, "checkout.html", {
        "fabrics": fabrics,
        "active_page": "checkout"
    })

@app.get("/order-success/{order_id}", response_class=HTMLResponse)
async def order_success_page(request: Request, order_id: str):
    orders = load_json("orders.json")
    order = next((o for o in orders if o["id"] == order_id), None)
    if not order:
        order = {
            "id": order_id,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "customer_name": "Değerli Müşterimiz",
            "customer_email": "bilgi@nevartrend.com",
            "cargo_company": "Yurtiçi Kargo",
            "total_amount": 0,
            "status": "Alındı"
        }
    return render(request, "order-success.html", {
        "order": order,
        "active_page": "home"
    })

@app.get("/admin/login", response_class=HTMLResponse)
async def admin_login_page(request: Request, error: Optional[str] = None):
    if is_admin(request):
        return RedirectResponse(url="/admin", status_code=302)
    return render(request, "admin-login.html", {"error": error})

@app.post("/admin/login")
async def admin_login_submit(request: Request, username: str = Form(...), password: str = Form(...)):
    u = username.strip().lower()
    if u in ADMIN_USERS and ADMIN_USERS[u] == password:
        response = RedirectResponse(url="/admin", status_code=302)
        response.set_cookie(
            key="nevartrend_admin_auth",
            value=ADMIN_SESSION_TOKEN,
            max_age=60 * 60 * 24 * 7,
            httponly=True,
            samesite="lax"
        )
        return response
    return render(request, "admin-login.html", {"error": "Yetkili kullanıcı adı veya şifre hatalı!"})


@app.get("/admin/logout")
async def admin_logout():
    response = RedirectResponse(url="/admin/login", status_code=302)
    response.delete_cookie("nevartrend_admin_auth")
    return response

@app.get("/admin", response_class=HTMLResponse)
async def admin_dashboard(request: Request, msg: Optional[str] = None):
    if not is_admin(request):
        return RedirectResponse(url="/admin/login", status_code=302)
    products = load_json("products.json")
    fabrics = load_json("fabric_types.json")
    orders = load_json("orders.json")
    categories = load_json("categories.json")

    total_sales = sum(float(o.get("total_amount", 0)) for o in orders)
    return render(request, "admin.html", {
        "products": products,
        "fabrics": fabrics,
        "orders": orders,
        "categories": categories,
        "total_sales": total_sales,
        "msg": msg,
        "active_page": "admin"
    })


# --- APIs ---

class OrderItem(BaseModel):
    product_id: str
    product_title: str
    product_code: Optional[str] = ""
    fabric_id: str
    fabric_name: str
    unit_price: float
    meters: float
    total_price: float
    image: Optional[str] = ""

class CreateOrderRequest(BaseModel):
    customer_name: str
    customer_email: str
    customer_phone: str
    city: str
    district: str
    address: str
    cargo_company: str
    payment_method: str
    items: List[OrderItem]
    subtotal: float
    discount: float
    shipping_fee: float
    total_amount: float

@app.post("/api/orders")
async def create_order(req: CreateOrderRequest):
    orders = load_json("orders.json")
    order_id = "NVT-" + uuid.uuid4().hex[:6].upper()
    new_order = {
        "id": order_id,
        "customer_name": req.customer_name,
        "customer_email": req.customer_email,
        "customer_phone": req.customer_phone,
        "address_full": f"{req.address} {req.district}/{req.city}",
        "cargo_company": req.cargo_company,
        "payment_method": req.payment_method,
        "items": [item.dict() for item in req.items],
        "subtotal": req.subtotal,
        "discount": req.discount,
        "shipping_fee": req.shipping_fee,
        "total_amount": req.total_amount,
        "status": "Baskı Sırasına Alındı",
        "cargo_code": "Hazırlanıyor",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    orders.insert(0, new_order)
    save_json("orders.json", orders)
    return {"success": True, "order_id": order_id}

def save_uploaded_pattern_file(upload_file: Optional[UploadFile]) -> Optional[str]:
    if not upload_file or not upload_file.filename:
        return None
    try:
        content = upload_file.file.read()
        if not content:
            return None
        orig_name = os.path.basename(upload_file.filename).replace(" ", "_")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = f"{timestamp}_{orig_name}"
        save_path = os.path.join(UPLOAD_DIR, safe_name)
        with open(save_path, "wb") as f:
            f.write(content)
        return f"/static/uploads/patterns/{safe_name}"
    except Exception as e:
        print(f"File upload error: {e}")
        return None

import re

def slugify(text: str) -> str:
    if not text:
        return "kategori"
    tr_map = {
        'ı': 'i', 'I': 'i', 'İ': 'i', 'ğ': 'g', 'Ğ': 'g',
        'ü': 'u', 'Ü': 'u', 'ş': 's', 'Ş': 's',
        'ö': 'o', 'Ö': 'o', 'ç': 'c', 'Ç': 'c'
    }
    for tr, en in tr_map.items():
        text = text.replace(tr, en)
    text = re.sub(r'[^a-zA-Z0-9\s-]', '', text).strip().lower()
    text = re.sub(r'[\s+]+', '-', text)
    return text or "kategori"

@app.post("/api/admin/products")
async def add_product(
    request: Request,
    title: str = Form(...),
    code: str = Form(...),
    category: str = Form(...),
    new_category_name: Optional[str] = Form(None),
    base_price: float = Form(...),
    image_url: Optional[str] = Form(None),
    image_file: Optional[UploadFile] = File(None),
    description: str = Form("")
):
    if not is_admin(request):
        return RedirectResponse(url="/admin/login", status_code=303)
    
    final_image = None
    if image_file and image_file.filename:
        saved_url = save_uploaded_pattern_file(image_file)
        if saved_url:
            final_image = saved_url
            
    if not final_image and image_url and image_url.strip():
        final_image = image_url.strip()
        
    if not final_image:
        final_image = "https://images.unsplash.com/photo-1550684848-fac1c5b4e853?w=800&auto=format&fit=crop&q=80"

    products = load_json("products.json")
    categories = load_json("categories.json")

    # Handle dynamic / new category
    if (category in ["__new__", "new", ""]) and new_category_name and new_category_name.strip():
        clean_cat = new_category_name.strip()
        cat_id = slugify(clean_cat)
        cat_obj = next((c for c in categories if c["id"] == cat_id), None)
        if not cat_obj:
            cat_obj = {
                "id": cat_id,
                "name": clean_cat,
                "short_title": clean_cat,
                "icon": "palette",
                "count": 1,
                "badge": "Yeni Kategori",
                "description": f"{clean_cat} desen ve kumaş koleksiyonu.",
                "image": final_image
            }
            categories.append(cat_obj)
            save_json("categories.json", categories)
        category = cat_id
    else:
        cat_obj = next((c for c in categories if c["id"] == category), {"name": category.title()})

    new_prod = {
        "id": code.upper().strip(),
        "code": code.upper().strip(),
        "title": title.strip(),
        "category": category,
        "category_name": cat_obj.get("name", category),
        "base_price": base_price,
        "rating": 5.0,
        "reviews_count": 1,
        "tags": ["Yeni", cat_obj.get("name", category)],
        "image": final_image,
        "mockup_dress": "https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=800&auto=format&fit=crop&q=80",
        "mockup_cushion": "https://images.unsplash.com/photo-1584100936595-c0654b55a2e2?w=800&auto=format&fit=crop&q=80",
        "pattern_tile": final_image,
        "description": description or f"Trenddesen {title} özel tasarım dijital kumaş baskı deseni.",
        "colors": ["#10b981", "#3b82f6", "#f59e0b", "#64748b"],
        "featured": True,
        "is_new": True,
        "discount_pct": 0,
        "sales_count": 0
    }
    products.insert(0, new_prod)
    save_json("products.json", products)
    return RedirectResponse(url="/admin?msg=added", status_code=303)

@app.post("/api/admin/products/edit")
async def edit_product(
    request: Request,
    product_id: str = Form(...),
    title: str = Form(...),
    code: str = Form(...),
    category: str = Form(...),
    new_category_name: Optional[str] = Form(None),
    base_price: float = Form(...),
    description: str = Form(""),
    image_url: Optional[str] = Form(None),
    image_file: Optional[UploadFile] = File(None)
):
    if not is_admin(request):
        return RedirectResponse(url="/admin/login", status_code=303)
    
    new_image = None
    if image_file and image_file.filename:
        saved_url = save_uploaded_pattern_file(image_file)
        if saved_url:
            new_image = saved_url
            
    if not new_image and image_url and image_url.strip():
        new_image = image_url.strip()

    products = load_json("products.json")
    categories = load_json("categories.json")

    # Handle dynamic / new category
    if (category in ["__new__", "new", ""]) and new_category_name and new_category_name.strip():
        clean_cat = new_category_name.strip()
        cat_id = slugify(clean_cat)
        cat_obj = next((c for c in categories if c["id"] == cat_id), None)
        if not cat_obj:
            cat_obj = {
                "id": cat_id,
                "name": clean_cat,
                "short_title": clean_cat,
                "icon": "palette",
                "count": 1,
                "badge": "Yeni Kategori",
                "description": f"{clean_cat} desen ve kumaş koleksiyonu.",
                "image": "https://images.unsplash.com/photo-1550684848-fac1c5b4e853?w=800"
            }
            categories.append(cat_obj)
            save_json("categories.json", categories)
        category = cat_id
    else:
        cat_obj = next((c for c in categories if c["id"] == category), {"name": category.title()})

    for p in products:
        if p["id"] == product_id:
            p["title"] = title.strip()
            p["code"] = code.upper().strip()
            p["category"] = category
            p["category_name"] = cat_obj.get("name", category)
            p["base_price"] = base_price
            p["description"] = description.strip()
            if new_image:
                p["image"] = new_image
                p["pattern_tile"] = new_image
            break

    save_json("products.json", products)
    return RedirectResponse(url="/admin?msg=edited", status_code=303)

@app.post("/api/admin/categories/add")
async def add_category(
    request: Request,
    name: str = Form(...),
    badge: Optional[str] = Form("Koleksiyon"),
    description: Optional[str] = Form("")
):
    if not is_admin(request):
        return RedirectResponse(url="/admin/login", status_code=303)
    categories = load_json("categories.json")
    clean_name = name.strip()
    cat_id = slugify(clean_name)
    if not any(c["id"] == cat_id for c in categories):
        categories.append({
            "id": cat_id,
            "name": clean_name,
            "short_title": clean_name,
            "icon": "folder",
            "count": 0,
            "badge": badge.strip() if badge else "Koleksiyon",
            "description": description.strip() if description else f"{clean_name} kategorisine ait desen ve kumaşlar.",
            "image": "https://images.unsplash.com/photo-1550684848-fac1c5b4e853?w=800"
        })
        save_json("categories.json", categories)
    return RedirectResponse(url="/admin?msg=cat_added", status_code=303)

@app.post("/api/admin/categories/delete")
async def delete_category(request: Request, category_id: str = Form(...)):
    if not is_admin(request):
        return RedirectResponse(url="/admin/login", status_code=303)
    categories = load_json("categories.json")
    categories = [c for c in categories if c["id"] != category_id]
    save_json("categories.json", categories)
    return RedirectResponse(url="/admin?msg=cat_deleted", status_code=303)

@app.post("/api/admin/products/delete")
async def delete_product(request: Request, product_id: str = Form(...)):
    if not is_admin(request):
        return RedirectResponse(url="/admin/login", status_code=303)
    products = load_json("products.json")
    products = [p for p in products if p["id"] != product_id]
    save_json("products.json", products)
    return RedirectResponse(url="/admin?msg=deleted", status_code=303)

@app.get("/api/admin/download-products")
async def download_products(request: Request):
    if not is_admin(request):
        return RedirectResponse(url="/admin/login", status_code=303)
    p_path = os.path.join(DATA_DIR, "products.json")
    return FileResponse(p_path, filename="products.json", media_type="application/json")

@app.get("/api/admin/download-categories")
async def download_categories(request: Request):
    if not is_admin(request):
        return RedirectResponse(url="/admin/login", status_code=303)
    c_path = os.path.join(DATA_DIR, "categories.json")
    return FileResponse(c_path, filename="categories.json", media_type="application/json")

@app.post("/api/admin/import-data")
async def import_json_data(
    request: Request,
    json_file: UploadFile = File(...)
):
    if not is_admin(request):
        return RedirectResponse(url="/admin/login", status_code=303)
    try:
        content = json_file.file.read()
        parsed = json.loads(content)
        fname = (json_file.filename or "").lower()
        if "product" in fname:
            save_json("products.json", parsed)
        elif "cat" in fname:
            save_json("categories.json", parsed)
        elif "fabric" in fname:
            save_json("fabric_types.json", parsed)
        else:
            save_json("products.json", parsed)
        return RedirectResponse(url="/admin?msg=imported", status_code=303)
    except Exception as e:
        print(f"Import error: {e}")
        return RedirectResponse(url="/admin?msg=import_error", status_code=303)

@app.post("/api/admin/fabrics/edit")
async def edit_fabric(
    request: Request,
    fabric_id: str = Form(...),
    name: str = Form(...),
    price_per_meter: float = Form(...),
    width: str = Form(...),
    weight: str = Form(...),
    composition: str = Form(...),
    description: str = Form("")
):
    if not is_admin(request):
        return RedirectResponse(url="/admin/login", status_code=303)
    fabrics = load_json("fabric_types.json")
    for f in fabrics:
        if f["id"] == fabric_id:
            f["name"] = name.strip()
            f["price_per_meter"] = price_per_meter
            f["width"] = width.strip()
            f["weight"] = weight.strip()
            f["composition"] = composition.strip()
            f["description"] = description.strip()
            break
    save_json("fabric_types.json", fabrics)
    return RedirectResponse(url="/admin?msg=fabric_updated", status_code=303)

@app.post("/api/admin/fix-turkish")
async def fix_turkish_characters(request: Request):
    if not is_admin(request):
        return RedirectResponse(url="/admin/login", status_code=303)

    fixes = {
        "?akay?k": "Şakayık",
        "?i?ek": "Çiçek",
        "?i?ekli": "Çiçekli",
        "Kuma?": "Kumaş",
        "Kuma??": "Kumaşı",
        "Kuma?lar": "Kumaşlar",
        "Kuma?lar?n?z": "Kumaşlarınız",
        "Kuma?lar?": "Kumaşları",
        "M??teri": "Müşteri",
        "Sipari?": "Sipariş",
        "Sipari?iniz": "Siparişiniz",
        "Sipari?ler": "Siparişler",
        "Al??veri?": "Alışveriş",
        "Al??veri?im": "Alışverişim",
        "?creti": "Ücreti",
        "?cretsiz": "Ücretsiz",
        "?zel": "Özel",
        "?deme": "Ödeme",
        "?demeye": "Ödemeye",
        "T?rk?e": "Türkçe",
        "T?rleri": "Türleri",
        "T?r?": "Türü",
        "?r?n": "Ürün",
        "?r?nler": "Ürünler",
        "??erik": "İçerik",
        "İİ": "İ",
        "ÇÇ": "Ç",
        "şş": "ş",
        "??": "ı",
    }

    def repair_obj(obj):
        if isinstance(obj, str):
            res = obj
            for bad, good in fixes.items():
                res = res.replace(bad, good)
            return res
        elif isinstance(obj, list):
            return [repair_obj(x) for x in obj]
        elif isinstance(obj, dict):
            return {k: repair_obj(v) for k, v in obj.items()}
        return obj

    for f_name in ["products.json", "fabric_types.json", "categories.json", "orders.json"]:
        data = load_json(f_name)
        repaired = repair_obj(data)
        save_json(f_name, repaired)
        
    return RedirectResponse(url="/admin?msg=turkish_fixed", status_code=303)

@app.post("/api/coupon/validate")
async def validate_coupon(coupon: dict):
    code = str(coupon.get("code", "")).strip().upper()
    if code == "TREND10":
        return {"valid": True, "discount_pct": 10, "message": "%10 Trenddesen İndirimi uygulandı!"}
    elif code == "NEVAR20":
        return {"valid": True, "discount_pct": 20, "message": "%20 Tanışma İndirimi uygulandı!"}
    elif code == "KARGO":
        return {"valid": True, "free_shipping": True, "message": "Ücretsiz Kargo kodu uygulandı!"}
    return {"valid": False, "message": "Geçersiz veya süresi dolmuş kupon kodu."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
