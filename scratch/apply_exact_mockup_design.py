import os
import re

app_dir = r"C:\Users\user\Desktop\nevartrend_ev"

# ==========================================
# 1. UPDATE templates/base.html
# ==========================================
base_path = os.path.join(app_dir, "templates", "base.html")
with open(base_path, "r", encoding="utf-8") as f:
    base_html = f.read()

# Replace Header with the exact header from user's image:
# Left: Logo
# Center: Search bar
# Right: WhatsApp | Giriş Yap | Favorilerim | Sepetim
new_header_code = """  <!-- Main Sticky Header -->
  <header class="sticky top-0 z-40 bg-white border-b border-slate-200/80 shadow-2xs transition-all duration-300">
    <div class="max-w-[1600px] mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-20 gap-4">
        
        <!-- Left: Logo -->
        <div class="flex items-center flex-shrink-0">
          <a href="/" class="flex items-center gap-2">
            <img src="/static/img/logo.png" alt="nevartrend by Trenddesen" class="h-10 sm:h-12 w-auto object-contain">
          </a>
        </div>

        <!-- Center: Search Bar -->
        <div class="flex-1 max-w-xl mx-2 sm:mx-6">
          <form action="/" method="GET" class="w-full relative flex items-center">
            <input 
              type="text" 
              name="q" 
              value="{{ search_query if search_query else '' }}"
              placeholder="Hazır ürün ara (örnek: Kimono, Kırlent, Çanta)..." 
              class="w-full pl-10 pr-20 py-2.5 bg-slate-50 border border-slate-200 rounded-full text-xs font-medium focus:outline-none focus:ring-2 focus:ring-[#183c2c] focus:bg-white transition"
            >
            <i data-lucide="search" class="w-4 h-4 text-slate-400 absolute left-3.5"></i>
            <button type="submit" class="absolute right-1 px-4 py-1.5 bg-[#183c2c] text-white rounded-full text-xs font-bold hover:bg-[#0f281d] transition">
              Ara
            </button>
          </form>
        </div>

        <!-- Right: Actions (WhatsApp, Giriş Yap, Favorilerim, Sepetim) -->
        <div class="flex items-center gap-3 sm:gap-4 flex-shrink-0">
          <!-- WhatsApp Button -->
          <a href="https://wa.me/908503000000?text=Merhaba,%20nevartrend%20hazır%20butik%20ürünleriniz%20hakkında%20bilgi%20almak%20istiyorum." target="_blank" rel="noopener noreferrer" class="hidden sm:inline-flex items-center gap-1.5 px-3.5 py-2 bg-emerald-50 hover:bg-emerald-100 text-emerald-800 rounded-full text-xs font-bold border border-emerald-300 transition shadow-2xs">
            <i data-lucide="message-circle" class="w-3.5 h-3.5 text-emerald-600"></i>
            <span>WhatsApp</span>
          </a>

          <!-- Giriş Yap -->
          <a href="/admin" class="hidden md:inline-flex items-center gap-1.5 text-xs font-bold text-slate-700 hover:text-[#183c2c] transition px-2 py-1">
            <i data-lucide="user" class="w-4 h-4 text-slate-600"></i>
            <span>Giriş Yap</span>
          </a>

          <!-- Favorilerim -->
          <button type="button" onclick="alert('Favorileriniz yakında aktif olacaktır!')" class="hidden md:inline-flex items-center gap-1.5 text-xs font-bold text-slate-700 hover:text-[#183c2c] transition px-2 py-1">
            <i data-lucide="heart" class="w-4 h-4 text-slate-600"></i>
            <span>Favorilerim</span>
          </button>

          <!-- Sepetim -->
          <button onclick="CartEngine.openDrawer()" class="inline-flex items-center gap-2 text-xs font-bold text-slate-700 hover:text-[#183c2c] transition px-2.5 py-1.5 rounded-lg hover:bg-slate-100 relative">
            <div class="relative">
              <i data-lucide="shopping-cart" class="w-4 h-4 text-slate-700"></i>
              <span class="cart-count-badge absolute -top-2 -right-2 bg-emerald-700 text-white text-[9px] font-bold rounded-full w-4 h-4 flex items-center justify-center border-2 border-white" style="display:none;">0</span>
            </div>
            <span class="font-bold text-slate-800">Sepetim</span>
          </button>
        </div>

      </div>
    </div>

    <!-- Centered Category Navigation Pills Bar -->
    <div class="bg-[#FAF9F6] border-t border-b border-slate-200/80 py-2.5 px-4 shadow-2xs">
      <div class="max-w-7xl mx-auto flex items-center justify-center gap-2 sm:gap-3 flex-wrap text-xs font-bold">
        <a href="/?category=giyim-butik" class="px-3.5 py-1.5 bg-white hover:bg-emerald-50 text-slate-700 hover:text-[#183c2c] border border-slate-200 rounded-lg transition flex items-center gap-1.5 shadow-2xs">
          <span>👗</span> <span>Fular, Kimono & Giyim</span>
        </a>
        <a href="/?category=canta-aksesuar" class="px-3.5 py-1.5 bg-white hover:bg-emerald-50 text-slate-700 hover:text-[#183c2c] border border-slate-200 rounded-lg transition flex items-center gap-1.5 shadow-2xs">
          <span>🛍️</span> <span>Kanvas Bez Çanta</span>
        </a>
        <a href="/?category=ev-tekstili" class="px-3.5 py-1.5 bg-white hover:bg-emerald-50 text-slate-700 hover:text-[#183c2c] border border-slate-200 rounded-lg transition flex items-center gap-1.5 shadow-2xs">
          <span>🛋️</span> <span>Kırlent & Yastık Kılıfı</span>
        </a>
        <a href="/?category=runner-setler" class="px-3.5 py-1.5 bg-white hover:bg-emerald-50 text-slate-700 hover:text-[#183c2c] border border-slate-200 rounded-lg transition flex items-center gap-1.5 shadow-2xs">
          <span>🍽️</span> <span>Pofuduk Minder & Runner</span>
        </a>
        <a href="/?category=sal-esarp" class="px-3.5 py-1.5 bg-white hover:bg-emerald-50 text-slate-700 hover:text-[#183c2c] border border-slate-200 rounded-lg transition flex items-center gap-1.5 shadow-2xs">
          <span>🧣</span> <span>Şal & Eşarp</span>
        </a>
      </div>
    </div>
  </header>"""

# Replace existing header in base.html
pattern_header = re.compile(r'<!-- Main Sticky Header -->.*?<!-- Page Body Content -->', re.DOTALL)
base_html = pattern_header.sub(new_header_code + '\n\n  <!-- Page Body Content -->', base_html)

with open(base_path, "w", encoding="utf-8") as f:
    f.write(base_html)

print("Updated templates/base.html header & category sub-bar successfully!")


# ==========================================
# 2. UPDATE templates/index.html & index.html
# ==========================================
index_template = """{% extends "base.html" %}

{% block title %}nevartrend | Özel Tasarım Hazır Giyim & Butik Koleksiyonu{% endblock %}

{% block content %}
<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8 space-y-8">

  <!-- Hero Header Banner (Compact, Elegant, Matching User Mockup) -->
  <div class="relative bg-gradient-to-r from-[#143325] via-[#1a4432] to-[#143325] text-white rounded-2xl sm:rounded-3xl p-8 sm:p-12 overflow-hidden shadow-xl border border-emerald-800/40 text-center">
    <div class="relative z-10 max-w-3xl mx-auto space-y-3.5">
      <div class="inline-flex items-center gap-2 px-3.5 py-1 bg-amber-500/20 text-amber-300 rounded-full text-xs font-extrabold uppercase tracking-wider border border-amber-500/30">
        <i data-lucide="sparkles" class="w-3.5 h-3.5 text-amber-400"></i>
        <span>ÖZGÜN BUTİK KOLEKSİYON</span>
      </div>

      <h1 class="font-serif-title text-3xl sm:text-5xl lg:text-5xl font-extrabold tracking-tight text-white leading-tight">
        Özel Tasarım Hazır Giyim & Butik Ürünler
      </h1>
    </div>
  </div>

  <!-- Product Grid (Matching exact card design from mockup) -->
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 sm:gap-8">
    {% for p in products %}
    <div class="bg-white rounded-2xl sm:rounded-3xl border border-slate-200 overflow-hidden shadow-xs hover:shadow-xl transition-all duration-300 flex flex-col justify-between group">
      <div>
        <!-- Image Box with Badges -->
        <div class="h-64 sm:h-72 bg-slate-100 relative overflow-hidden">
          <img src="{{ p.image }}" alt="{{ p.title }}" loading="lazy" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700">
          
          <!-- Top Left Badges -->
          <div class="absolute top-3.5 left-3.5 flex flex-col gap-1.5 z-10">
            <span class="px-2.5 py-1 bg-[#183c2c] text-white font-extrabold text-[10px] sm:text-[11px] rounded-md shadow uppercase tracking-wider">
              {{ p.badge }}
            </span>
            <span class="px-2 py-0.5 bg-slate-900/80 backdrop-blur-xs text-white font-semibold text-[10px] rounded-md">
              {{ p.fabric_type }}
            </span>
          </div>

          <!-- Top Right İndirim Badge -->
          {% if p.old_price %}
          <span class="absolute top-3.5 right-3.5 px-2.5 py-1 bg-rose-600 text-white font-extrabold text-[11px] rounded-md shadow z-10">
            İndirim
          </span>
          {% endif %}
        </div>

        <!-- Details -->
        <div class="p-5 sm:p-6 space-y-3.5">
          <!-- Category & Title -->
          <div>
            <span class="text-[10px] font-extrabold text-emerald-800 uppercase tracking-widest block">{{ p.category_name }}</span>
            <h3 class="font-extrabold text-slate-900 text-base group-hover:text-emerald-800 transition leading-snug mt-1">
              {{ p.title }}
            </h3>
          </div>

          <!-- Description -->
          <p class="text-xs text-slate-500 leading-relaxed line-clamp-2">
            {{ p.description }}
          </p>

          <!-- Feature Bullets with Teal Checks -->
          <div class="space-y-1 pt-1 border-t border-slate-100 text-xs text-slate-600">
            {% for feat in p.features[:3] %}
            <div class="flex items-center gap-2">
              <i data-lucide="check-circle" class="w-3.5 h-3.5 text-emerald-600 flex-shrink-0"></i>
              <span>{{ feat }}</span>
            </div>
            {% endfor %}
          </div>

          <!-- Size Options -->
          <div class="pt-1">
            <span class="text-[11px] font-bold text-slate-700 block mb-1.5">Mevcut Ölçü / Beden:</span>
            <div class="flex flex-wrap gap-1.5">
              {% for s in p.size_options %}
              <span class="px-2.5 py-1 bg-slate-50 text-slate-700 rounded-lg text-[10px] sm:text-[11px] font-semibold border border-slate-200">
                {{ s }}
              </span>
              {% endfor %}
            </div>
          </div>
        </div>
      </div>

      <!-- Price & Actions Row -->
      <div class="p-5 sm:p-6 pt-0 border-t border-slate-100 mt-1">
        <div class="flex items-center justify-between mb-3.5 pt-3">
          <div>
            {% if p.old_price %}
            <span class="text-xs text-slate-400 line-through block">{{ p.old_price }} TL</span>
            {% endif %}
            <span class="text-2xl font-extrabold text-slate-900">{{ p.price }} TL</span>
            <span class="text-[10px] text-slate-400 block font-medium">KDV Dahil</span>
          </div>
          
          <span class="px-2.5 py-1 bg-emerald-50 text-emerald-800 text-xs font-bold rounded-lg border border-emerald-200 flex items-center gap-1">
            <i data-lucide="check" class="w-3.5 h-3.5"></i> Stokta Var
          </span>
        </div>

        <div class="grid grid-cols-2 gap-2">
          <button onclick="CartEngine.addItem({
            id: '{{ p.id }}',
            title: '{{ p.title|e }}',
            price: {{ p.price }},
            image: '{{ p.image }}',
            type: 'trend-product',
            details: '{{ p.fabric_type }} • {{ p.size_options[0] if p.size_options else "Standart" }}'
          })" class="py-2.5 px-3 bg-[#183c2c] hover:bg-[#0f281d] text-white rounded-xl text-xs font-bold transition flex items-center justify-center gap-1.5 shadow-sm">
            <i data-lucide="shopping-bag" class="w-4 h-4"></i>
            <span>Sepete Ekle</span>
          </button>
          
          <a href="https://wa.me/908503000000?text=Merhaba,%20{{ p.title|urlencode }}%20({{ p.price }}%20TL)%20ürününü%20sipariş%20etmek%20istiyorum." target="_blank" rel="noopener noreferrer" class="py-2.5 px-3 bg-emerald-50 hover:bg-emerald-100 text-emerald-800 rounded-xl text-xs font-bold transition flex items-center justify-center gap-1 border border-emerald-200">
            <i data-lucide="message-circle" class="w-4 h-4 text-emerald-600"></i>
            <span>WhatsApp</span>
          </a>
        </div>
      </div>
    </div>
    {% endfor %}
  </div>

</div>
{% endblock %}
"""

with open(os.path.join(app_dir, "templates", "index.html"), "w", encoding="utf-8") as f:
    f.write(index_template)

with open(os.path.join(app_dir, "index.html"), "w", encoding="utf-8") as f:
    f.write(index_template)

with open(os.path.join(app_dir, "templates", "trend_urunler.html"), "w", encoding="utf-8") as f:
    f.write(index_template)

print("Updated index templates successfully!")
