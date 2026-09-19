import os
import json
import uuid
from datetime import datetime
from typing import Optional, List
from fastapi import FastAPI, Request, Form, HTTPException, Query
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI(title="nevartrend | Trenddesen E-Ticaret")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    fav_path = os.path.join(BASE_DIR, "static", "img", "favicon.svg")
    return FileResponse(fav_path, media_type="image/svg+xml")


def load_json(filename):
    path = os.path.join(DATA_DIR, filename)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_json(filename, data):
    path = os.path.join(DATA_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def render(request: Request, template_name: str, context: dict = None):
    ctx = context or {}
    ctx["request"] = request
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

@app.get("/admin", response_class=HTMLResponse)
async def admin_dashboard(request: Request, msg: Optional[str] = None):
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

@app.post("/api/admin/products")
async def add_product(
    title: str = Form(...),
    code: str = Form(...),
    category: str = Form(...),
    base_price: float = Form(...),
    image_url: str = Form(...),
    description: str = Form("")
):
    products = load_json("products.json")
    categories = load_json("categories.json")
    cat_obj = next((c for c in categories if c["id"] == category), {"name": "Genel"})

    new_prod = {
        "id": code.upper().strip(),
        "code": code.upper().strip(),
        "title": title.strip(),
        "category": category,
        "category_name": cat_obj["name"],
        "base_price": base_price,
        "rating": 5.0,
        "reviews_count": 1,
        "tags": ["Yeni", cat_obj["name"]],
        "image": image_url,
        "mockup_dress": "https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=800&auto=format&fit=crop&q=80",
        "mockup_cushion": "https://images.unsplash.com/photo-1584100936595-c0654b55a2e2?w=800&auto=format&fit=crop&q=80",
        "pattern_tile": image_url,
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
    product_id: str = Form(...),
    title: str = Form(...),
    code: str = Form(...),
    category: str = Form(...),
    base_price: float = Form(...),
    description: str = Form(""),
    image_url: Optional[str] = Form(None)
):
    products = load_json("products.json")
    categories = load_json("categories.json")
    cat_obj = next((c for c in categories if c["id"] == category), {"name": "Genel"})

    for p in products:
        if p["id"] == product_id:
            p["title"] = title.strip()
            p["code"] = code.upper().strip()
            p["category"] = category
            p["category_name"] = cat_obj["name"]
            p["base_price"] = base_price
            p["description"] = description.strip()
            if image_url:
                p["image"] = image_url
                p["pattern_tile"] = image_url
            break

    save_json("products.json", products)
    return RedirectResponse(url="/admin?msg=edited", status_code=303)

@app.post("/api/admin/products/delete")
async def delete_product(product_id: str = Form(...)):
    products = load_json("products.json")
    products = [p for p in products if p["id"] != product_id]
    save_json("products.json", products)
    return RedirectResponse(url="/admin?msg=deleted", status_code=303)

@app.post("/api/admin/fabrics/edit")
async def edit_fabric(
    fabric_id: str = Form(...),
    name: str = Form(...),
    price_per_meter: float = Form(...),
    width: str = Form(...),
    weight: str = Form(...),
    composition: str = Form(...),
    description: str = Form("")
):
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
async def fix_turkish_characters():
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
