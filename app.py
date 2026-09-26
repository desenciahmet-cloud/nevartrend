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




DEFAULT_PRODUCTS = [
  {
    "id": "NT_011",
    "code": "NT_011",
    "title": "Neon Işıltılı Şeffaf Lale & Nilüfer Bahçesi",
    "category": "soyut-mermer",
    "category_name": "Modern Sanat & Neon Çiçekler",
    "print_type": "Dijital Baskı",
    "separation_ready": True,
    "screen_count": 8,
    "base_price": 185.0,
    "rating": 5.0,
    "reviews_count": 27,
    "tags": ["Yeni", "Neon", "Fuşya", "Turkuaz", "Şeffaf Çiçek", "Lale", "Sanatsal"],
    "image": "/static/images/NT_011.jpg",
    "pattern_tile": "/static/images/NT_011.jpg",
    "description": "Trenddesen yeni sezon özel fütüristik tasarımı. Canlı fuşya, turkuaz ve mor neon ışık huzmeleriyle transparan katmerli nilüfer ve anemon çiçekleri içeren yüksek çözünürlüklü dijital baskı deseni.",
    "colors": ["#d946ef", "#06b6d4", "#a855f7", "#1e1b4b"],
    "featured": True,
    "is_new": True,
    "discount_pct": 0,
    "sales_count": 52
  },
  {
    "id": "NT_013",
    "code": "NT_013",
    "title": "Siyah Zemin Degrade Çizgisel Çiçekler & Kasımpatı",
    "category": "cicekli-botanik",
    "category_name": "Çizgisel Sanat & Etnik Çiçekler",
    "print_type": "Emprime & Dijital Uyumlu",
    "separation_ready": True,
    "screen_count": 5,
    "base_price": 185.0,
    "rating": 5.0,
    "reviews_count": 34,
    "tags": ["Yeni", "Siyah Zemin", "Degrade", "Kırmızı", "Mavi", "Kasımpatı", "Modern"],
    "image": "/static/images/NT_013.jpg",
    "pattern_tile": "/static/images/NT_013.jpg",
    "description": "Siyah antrasit zemin üzerinde turuncu, kırmızı, mor ve elektrik mavisi degrade çizgisel kasımpatı ve papatya motifleriyle dinamik moda kumaş deseni.",
    "colors": ["#000000", "#ea580c", "#3b82f6", "#9333ea"],
    "featured": True,
    "is_new": True,
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
    "separation_ready": True,
    "screen_count": 6,
    "base_price": 185.0,
    "rating": 5.0,
    "reviews_count": 18,
    "tags": ["Yeni", "Gül", "Pastel Mavi", "Leylak", "Romantik", "Vintage"],
    "image": "/static/images/NT_012.jpg",
    "pattern_tile": "/static/images/NT_012.jpg",
    "description": "Trenddesen özel romantik koleksiyonu. Pudra zemin üzerinde pastel mavi katmerli güller, leylak goncalar ve zarafet dolu dikişsiz çiçek deseni.",
    "colors": ["#a4b2c6", "#c3a5bc", "#e8e1df", "#939ea0"],
    "featured": True,
    "is_new": True,
    "discount_pct": 0,
    "sales_count": 38
  },
  {
    "id": "NT_014",
    "code": "NT_014",
    "title": "Siyah Beyaz Monokrom Çizgisel Şakayık & Lilyum",
    "category": "cicekli-botanik",
    "category_name": "Monokrom & Çizgisel Sanat",
    "print_type": "Emprime & Dijital Uyumlu",
    "separation_ready": True,
    "screen_count": 2,
    "base_price": 185.0,
    "rating": 5.0,
    "reviews_count": 25,
    "tags": ["Yeni", "Monokrom", "Siyah Beyaz", "Şakayık", "Çizgisel", "Asil"],
    "image": "/static/images/NT_014.jpg",
    "pattern_tile": "/static/images/NT_014.jpg",
    "description": "Antrasit siyah zemin üzerinde yüksek kontrastlı beyaz gravür şakayık, zambak ve yaprak illüstrasyonları içeren şık ve lüks kumaş deseni.",
    "colors": ["#1c1d1f", "#ffffff", "#3b3c3e", "#e5e7eb"],
    "featured": True,
    "is_new": True,
    "discount_pct": 0,
    "sales_count": 56
  },
  {
    "id": "NT_015",
    "code": "NT_015",
    "title": "Gece Mavisi Sulu Boya Sanatsal Çiçek Tablosu",
    "category": "soyut-mermer",
    "category_name": "Sulu Boya & Sanatsal Çiçekler",
    "print_type": "Dijital Baskı",
    "separation_ready": True,
    "screen_count": 8,
    "base_price": 185.0,
    "rating": 5.0,
    "reviews_count": 31,
    "tags": ["Yeni", "Sulu Boya", "Gece Mavisi", "Sarı Çiçek", "Sanatsal Tablo"],
    "image": "/static/images/NT_015.jpg",
    "pattern_tile": "/static/images/NT_015.jpg",
    "description": "Derin gece mavisi ve çivit sulu boya akıntıları üzerinde sarı ve beyaz anemon çiçekleriyle galeri tablosu niteliğinde çarpıcı dijital baskı deseni.",
    "colors": ["#25295c", "#3d4b8f", "#f7bf46", "#f2efe9"],
    "featured": True,
    "is_new": True,
    "discount_pct": 0,
    "sales_count": 49
  },
  {
    "id": "NT_007",
    "code": "NT_007",
    "title": "Vintage Çizgili Bordo Gül Deseni",
    "category": "cicekli-botanik",
    "category_name": "Çiçekli & Botanik",
    "print_type": "Emprime & Dijital Uyumlu",
    "separation_ready": True,
    "screen_count": 6,
    "base_price": 185.0,
    "rating": 5.0,
    "reviews_count": 16,
    "tags": ["Yeni", "Gül", "Çizgili", "Vintage", "Bordo", "Altın Kontür"],
    "image": "/static/images/NT_007.jpg",
    "pattern_tile": "/static/images/NT_007.jpg",
    "description": "Trenddesen yeni sezon özel tasarımı. Çizgili zemin üzerinde lüks bordo güller, altın kontürlü yapraklar ve goncalar içeren yüksek çözünürlüklü dijital baskı kumaş deseni.",
    "colors": ["#d9d5c1", "#9f907b", "#7c5851", "#3f4040"],
    "featured": True,
    "is_new": True,
    "discount_pct": 0,
    "sales_count": 35
  },
  {
    "id": "NT_008",
    "code": "NT_008",
    "title": "Pastel Çizgili Papatya & Boncuk Deseni",
    "category": "cicekli-botanik",
    "category_name": "Çiçekli & Botanik",
    "print_type": "Emprime & Dijital Uyumlu",
    "separation_ready": True,
    "screen_count": 6,
    "base_price": 185.0,
    "rating": 5.0,
    "reviews_count": 16,
    "tags": ["Yeni", "Pastel", "Papatya", "Çizgili", "Pembe & Mint", "Yazlık"],
    "image": "/static/images/NT_008.jpg",
    "pattern_tile": "/static/images/NT_008.jpg",
    "description": "Trenddesen yeni sezon özel tasarımı. Pastel pembe ve nane yeşili dikey çizgiler, boncuk dizileri ve stilize papatya motifleriyle bezenmiş ferah kumaş deseni.",
    "colors": ["#fcfefe", "#f2efe9", "#ddcbc1", "#bc9d8d"],
    "featured": True,
    "is_new": True,
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
    "separation_ready": True,
    "screen_count": 6,
    "base_price": 185.0,
    "rating": 5.0,
    "reviews_count": 16,
    "tags": ["Yeni", "Barok", "Altın Varak", "Gold", "Saray Çiçeği", "Lüks"],
    "image": "/static/images/NT_009.jpg",
    "pattern_tile": "/static/images/NT_009.jpg",
    "description": "Trenddesen yeni sezon özel tasarımı. Siyah zemin üzerine lüks altın yaldız işlemeli Barok saray motifi ve lotus detaylarıyla zenginleştirilmiş kumaş deseni.",
    "colors": ["#ebdd73", "#c1a957", "#816537", "#23120b"],
    "featured": True,
    "is_new": True,
    "discount_pct": 0,
    "sales_count": 35
  },
  {
    "id": "NT_010",
    "code": "NT_010",
    "title": "Soyut Dijital Anemon & Şakayık Bahçesi",
    "category": "cicekli-botanik",
    "category_name": "Çiçekli & Botanik",
    "print_type": "Emprime & Dijital Uyumlu",
    "separation_ready": True,
    "screen_count": 6,
    "base_price": 185.0,
    "rating": 5.0,
    "reviews_count": 16,
    "tags": ["Yeni", "Soyut", "Anemon", "Şakayık", "Degrade", "Canlı Renkler"],
    "image": "/static/images/NT_010.jpg",
    "pattern_tile": "/static/images/NT_010.jpg",
    "description": "Trenddesen yeni sezon özel tasarımı. Degrade taç yapraklar, canlı anemon ve şakayık çiçekleriyle modern sanatsal dijital baskı kumaş deseni.",
    "colors": ["#dcd0d1", "#b09390", "#955446", "#3b3439"],
    "featured": True,
    "is_new": True,
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
    "separation_ready": True,
    "screen_count": 6,
    "base_price": 185.0,
    "rating": 5.0,
    "reviews_count": 14,
    "tags": ["Yeni", "Leopar", "Zincir", "Barok", "Kemer"],
    "image": "/static/images/NT_006.jpg",
    "pattern_tile": "/static/images/NT_006.jpg",
    "description": "Trenddesen yeni sezon özel dijital baskı deseni. Barok kemer, zincir ve vahşi doğa leopar motifli yüksek çözünürlüklü kumaş deseni.",
    "colors": ["#d97706", "#1e293b", "#047857", "#fef08a"],
    "featured": True,
    "is_new": True,
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
    "separation_ready": True,
    "screen_count": 5,
    "base_price": 185.0,
    "rating": 5.0,
    "reviews_count": 19,
    "tags": ["Yeni", "Kırık Cam", "Soyut", "Mermer", "Batik"],
    "image": "/static/images/NT_005.jpg",
    "pattern_tile": "/static/images/NT_005.jpg",
    "description": "Trenddesen yeni sezon özel dijital baskı deseni. Modern soyut kırık cam ve eskitme batik doku.",
    "colors": ["#f97316", "#06b6d4", "#64748b", "#f8fafc"],
    "featured": True,
    "is_new": True,
    "discount_pct": 0,
    "sales_count": 62
  },
  {
    "id": "NT_004",
    "code": "NT_004_60980536",
    "title": "Bahar Çiçekleri",
    "category": "desenler",
    "category_name": "Çiçekli & Botanik",
    "print_type": "Dijital & Emprime Uyumlu",
    "separation_ready": True,
    "screen_count": 6,
    "base_price": 185.0,
    "rating": 5.0,
    "reviews_count": 28,
    "tags": ["Yeni", "Bahar Çiçekleri", "Botanik", "Çiçekli"],
    "image": "/static/images/NT_004.jpg",
    "pattern_tile": "/static/images/NT_004.jpg",
    "description": "Trenddesen yeni sezon özel dijital baskı deseni. Bahar çiçekleri ve pastel yaprak tonları.",
    "colors": ["#ec4899", "#10b981", "#f59e0b", "#38bdf8"],
    "featured": True,
    "is_new": True,
    "discount_pct": 0,
    "sales_count": 84
  },
  {
    "id": "NT_003",
    "code": "NT_003_85328767",
    "title": "Mor Gül Bahçesi",
    "category": "desenler",
    "category_name": "Çiçekli & Botanik",
    "print_type": "Dijital & Emprime Uyumlu",
    "separation_ready": True,
    "screen_count": 5,
    "base_price": 185.0,
    "rating": 5.0,
    "reviews_count": 31,
    "tags": ["Yeni", "Mor Gül", "Çiçekli", "Zarif"],
    "image": "/static/images/NT_003.jpg",
    "pattern_tile": "/static/images/NT_003.jpg",
    "description": "Trenddesen yeni sezon özel dijital baskı deseni. Siyah zemin üzerinde koyu ve açık mor güller.",
    "colors": ["#a855f7", "#0f172a", "#22c55e", "#f43f5e"],
    "featured": True,
    "is_new": True,
    "discount_pct": 0,
    "sales_count": 95
  },
  {
    "id": "NT_002",
    "code": "NT_002_60980536",
    "title": "Papatya Bahçesi",
    "category": "desenler",
    "category_name": "Çiçekli & Botanik",
    "print_type": "Dijital & Emprime Uyumlu",
    "separation_ready": True,
    "screen_count": 4,
    "base_price": 185.0,
    "rating": 5.0,
    "reviews_count": 42,
    "tags": ["Yeni", "Papatya", "Çiçekli", "Sarı", "Beyaz"],
    "image": "/static/images/NT_002.jpg",
    "pattern_tile": "/static/images/NT_002.jpg",
    "description": "Trenddesen yeni sezon özel dijital baskı deseni. Sarı ve beyaz papatyalarla dolu canlı bahçe deseni.",
    "colors": ["#eab308", "#ffffff", "#15803d", "#78350f"],
    "featured": True,
    "is_new": True,
    "discount_pct": 0,
    "sales_count": 110
  },
  {
    "id": "NT_001",
    "code": "NT_001",
    "title": "Sulu Boya Çiçek Bahçesi",
    "category": "desenler",
    "category_name": "Çiçekli & Botanik",
    "print_type": "Dijital & Emprime Uyumlu",
    "separation_ready": True,
    "screen_count": 5,
    "base_price": 185.0,
    "rating": 5.0,
    "reviews_count": 37,
    "tags": ["Yeni", "Suluboya", "Kırmızı Gül", "Çiçekli"],
    "image": "/static/images/NT_001.jpg",
    "pattern_tile": "/static/images/NT_001.jpg",
    "description": "Trenddesen yeni sezon özel dijital baskı deseni. Krem zemin üzerine sulu boya tekniğiyle hazırlanmış kırmızı ve pembe çiçekler.",
    "colors": ["#ef4444", "#fef08a", "#16a34a", "#f43f5e"],
    "featured": True,
    "is_new": True,
    "discount_pct": 0,
    "sales_count": 125
  }
]

def load_json(filename):
    path = os.path.join(DATA_DIR, filename)
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if filename == "products.json" and isinstance(data, list) and len(data) >= 10:
                    return data
                elif filename != "products.json" and data:
                    return data
        except Exception:
            pass
    if filename == "products.json":
        try:
            save_json("products.json", DEFAULT_PRODUCTS)
        except Exception:
            pass
        return DEFAULT_PRODUCTS
    return []

def save_json(filename, data):
    os.makedirs(DATA_DIR, exist_ok=True)
    path = os.path.join(DATA_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

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

    filtered = products

    if category and category != "all":
        filtered = [p for p in filtered if p.get("category") == category]

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
        else:
            cat["count"] = len([p for p in products if p.get("category") == cat["id"]])

    return render(request, "fabrics.html", {
        "products": filtered,
        "fabrics": fabrics,
        "categories": categories,
        "selected_category": category,
        "selected_fabric": fabric,
        "search_query": q or "",
        "selected_sort": sort,
        "active_page": "fabrics"
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

ADMIN_USERS = {
    "admin": os.getenv("ADMIN_PASSWORD", "nevartrend2026"),
    "moderator": os.getenv("MODERATOR_PASSWORD", "trend2026")
}
ADMIN_SESSION_TOKEN = "nevartrend_secret_admin_token_2026"

def is_admin(request: Request) -> bool:
    token = request.cookies.get("nevartrend_admin_auth")
    return token == ADMIN_SESSION_TOKEN

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
