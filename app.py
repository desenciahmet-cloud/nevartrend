import os
import json
import uuid
from datetime import datetime
from typing import Optional, List
from fastapi import FastAPI, Request, Form, HTTPException, Query
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI(title="nevartrend | Trenddesen E-Ticaret")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

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
        filtered = [p for p in filtered if q.lower() in p.get("title", "").lower() or q.lower() in p.get("code", "").lower()]
        
    if sort == "price_asc":
        filtered = sorted(filtered, key=lambda x: x.get("base_price", 0))
    elif sort == "price_desc":
        filtered = sorted(filtered, key=lambda x: x.get("base_price", 0), reverse=True)
    elif sort == "rating":
        filtered = sorted(filtered, key=lambda x: x.get("rating", 0), reverse=True)
    else:
        filtered = sorted(filtered, key=lambda x: x.get("sales_count", 0), reverse=True)
        
    return render(request, "fabrics.html", {
        "products": filtered,
        "all_products_count": len(products),
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
        raise HTTPException(status_code=404, detail="?r?n veya desen bulunamad?")
        
    related = [p for p in products if p["id"] != product["id"] and (p.get("category") == product.get("category"))][:4]
    if len(related) < 4:
        related = [p for p in products if p["id"] != product["id"]][:4]

    return render(request, "product-detail.html", {
        "product": product,
        "fabrics": fabrics,
        "related_products": related,
        "active_page": "fabrics"
    })

@app.get("/cart", response_class=HTMLResponse)
async def cart_page(request: Request):
    fabrics = load_json("fabric_types.json")
    return render(request, "cart.html", {
        "fabrics": fabrics,
        "active_page": "cart"
    })

@app.get("/checkout", response_class=HTMLResponse)
async def checkout_page(request: Request):
    return render(request, "checkout.html", {
        "active_page": "checkout"
    })

@app.get("/order-success/{order_id}", response_class=HTMLResponse)
async def order_success_page(request: Request, order_id: str):
    orders = load_json("orders.json")
    order = next((o for o in orders if o["id"] == order_id), None)
    if not order:
        order = {
            "id": order_id,
            "customer_name": "De?erli M??terimiz",
            "customer_email": "musteri@example.com",
            "total_amount": 750.0,
            "status": "Sipari? Al?nd? & Onayland?",
            "cargo_company": "Yurti?i Kargo (?cretsiz)",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
    return render(request, "order-success.html", {
        "order": order,
        "active_page": "checkout"
    })

@app.get("/admin", response_class=HTMLResponse)
async def admin_page(request: Request, msg: Optional[str] = None):
    products = load_json("products.json")
    fabrics = load_json("fabric_types.json")
    categories = load_json("categories.json")
    orders = load_json("orders.json")
    
    total_sales = sum(o.get("total_amount", 0) for o in orders)
    return render(request, "admin.html", {
        "products": products,
        "fabrics": fabrics,
        "categories": categories,
        "orders": orders,
        "total_sales": total_sales,
        "active_page": "admin",
        "msg": msg
    })

# --- JSON API Endpoints ---

class OrderItem(BaseModel):
    product_id: str
    product_title: str
    fabric_id: str
    fabric_name: str
    meters: float
    unit_price: float
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
    notes: Optional[str] = ""

@app.post("/api/orders")
async def create_order(req: CreateOrderRequest):
    orders = load_json("orders.json")
    order_id = f"NVT-{str(uuid.uuid4().hex[:6]).upper()}"
    
    new_order = {
        "id": order_id,
        "customer_name": req.customer_name,
        "customer_email": req.customer_email,
        "customer_phone": req.customer_phone,
        "address_full": f"{req.address} {req.district}/{req.city}",
        "cargo_company": req.cargo_company,
        "payment_method": req.payment_method,
        "items": [item.model_dump() for item in req.items],
        "subtotal": req.subtotal,
        "discount": req.discount,
        "shipping_fee": req.shipping_fee,
        "total_amount": req.total_amount,
        "status": "Bask? S?ras?na Al?nd?",
        "cargo_code": "Haz?rlan?yor",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    orders.insert(0, new_order)
    save_json("orders.json", orders)
    return {"success": True, "order_id": order_id, "message": "Sipari? ba?ar?yla olu?turuldu."}

@app.post("/api/admin/products")
async def add_product(
    title: str = Form(...),
    code: str = Form(...),
    category: str = Form(...),
    base_price: float = Form(...),
    description: str = Form(...),
    image_url: str = Form(...)
):
    products = load_json("products.json")
    categories = load_json("categories.json")
    cat_name = next((c["name"] for c in categories if c["id"] == category), "Genel")
    
    new_p = {
        "id": code.upper().strip() if code else f"TD-{len(products)+101}",
        "code": code.upper().strip() if code else f"TD-{len(products)+101}",
        "title": title.strip(),
        "category": category,
        "category_name": cat_name,
        "base_price": base_price,
        "rating": 5.0,
        "reviews_count": 1,
        "tags": ["Yeni", "Trenddesen ?zel"],
        "image": image_url.strip() or "https://images.unsplash.com/photo-1550684848-fac1c5b4e853?w=800&auto=format&fit=crop&q=80",
        "mockup_dress": image_url.strip() or "https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=800&auto=format&fit=crop&q=80",
        "mockup_cushion": image_url.strip() or "https://images.unsplash.com/photo-1584100936595-c0654b55a2e2?w=800&auto=format&fit=crop&q=80",
        "pattern_tile": image_url.strip() or "https://images.unsplash.com/photo-1550684848-fac1c5b4e853?w=500&auto=format&fit=crop&q=80",
        "description": description.strip(),
        "colors": ["#2a9d8f", "#e76f51", "#264653"],
        "featured": True,
        "is_new": True,
        "discount_pct": 0,
        "sales_count": 0
    }
    products.insert(0, new_p)
    save_json("products.json", products)
    return RedirectResponse(url="/admin?msg=added", status_code=303)

@app.post("/api/admin/products/edit")
async def edit_product(
    product_id: str = Form(...),
    title: str = Form(...),
    code: str = Form(...),
    category: str = Form(...),
    base_price: float = Form(...),
    description: str = Form(...),
    image_url: str = Form(...)
):
    products = load_json("products.json")
    categories = load_json("categories.json")
    cat_name = next((c["name"] for c in categories if c["id"] == category), "Genel")
    
    for p in products:
        if p["id"] == product_id or p["code"] == product_id:
            p["title"] = title.strip()
            p["code"] = code.strip().upper()
            p["category"] = category
            p["category_name"] = cat_name
            p["base_price"] = base_price
            p["description"] = description.strip()
            if image_url.strip():
                p["image"] = image_url.strip()
                p["mockup_dress"] = image_url.strip()
                p["mockup_cushion"] = image_url.strip()
                p["pattern_tile"] = image_url.strip()
            break
            
    save_json("products.json", products)
    return RedirectResponse(url="/admin?msg=edited", status_code=303)

@app.post("/api/admin/products/delete")
async def delete_product(product_id: str = Form(...)):
    products = load_json("products.json")
    products = [p for p in products if p["id"] != product_id and p["code"] != product_id]
    save_json("products.json", products)
    return RedirectResponse(url="/admin?msg=deleted", status_code=303)

@app.post("/api/admin/fabrics/edit")
async def edit_fabric(
    fabric_id: str = Form(...),
    name: str = Form(...),
    price_per_meter: float = Form(...),
    composition: str = Form(...),
    width: str = Form(...),
    weight: str = Form(...),
    description: str = Form(...)
):
    fabrics = load_json("fabric_types.json")
    for f in fabrics:
        if f["id"] == fabric_id:
            f["name"] = name.strip()
            f["price_per_meter"] = price_per_meter
            f["composition"] = composition.strip()
            f["width"] = width.strip()
            f["weight"] = weight.strip()
            f["description"] = description.strip()
            break
    save_json("fabric_types.json", fabrics)
    return RedirectResponse(url="/admin?msg=fabric_updated", status_code=303)

@app.post("/api/admin/fix-turkish")
async def fix_turkish_characters():
    """Otomatik T?rk?e Karakter Onar?m Fonksiyonu"""
    fixes = {
        "??": "?", "??": "?",
        "??": "?", "??": "?",
        "??": "?", "??": "?",
        "??": "?", "??": "?",
        "??": "?", "??": "?",
        "??": "?", "??": "?"
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
        return {"valid": True, "discount_pct": 10, "message": "%10 Trenddesen ?ndirimi uyguland?!"}
    elif code == "NEVAR20":
        return {"valid": True, "discount_pct": 20, "message": "%20 Tan??ma ?ndirimi uyguland?!"}
    elif code == "KARGO":
        return {"valid": True, "free_shipping": True, "message": "?cretsiz Kargo kodu uyguland?!"}
    return {"valid": False, "message": "Ge?ersiz veya s?resi dolmu? kupon kodu."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
