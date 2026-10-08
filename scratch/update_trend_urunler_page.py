import os

file_path = r'C:\Users\user\Desktop\nevartrend_ev\templates\trend_urunler.html'

template_html = '''{% extends "base.html" %}

{% block title %}Trend Hazır Tekstil & Butik Ürünler | nevartrend{% endblock %}

{% block content %}
<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-10">

  <!-- Breadcrumb -->
  <nav class="flex text-xs text-slate-500 gap-2 items-center">
    <a href="/" class="hover:text-emerald-700">Ana Sayfa</a>
    <span>/</span>
    <span class="font-bold text-slate-800">Diğer Trend Ürünler</span>
  </nav>

  <!-- Hero Header Banner -->
  <div class="relative bg-gradient-to-r from-amber-950 via-slate-900 to-amber-950 text-white rounded-3xl p-8 sm:p-12 overflow-hidden shadow-xl border border-amber-800/40">
    <div class="relative z-10 max-w-3xl space-y-4">
      <div class="inline-flex items-center gap-2 px-3.5 py-1 bg-amber-500/20 text-amber-300 rounded-full text-xs font-bold uppercase tracking-wider border border-amber-500/30">
        <i data-lucide="sparkles" class="w-4 h-4 text-amber-400"></i> Butik Üretim & Hazır Koleksiyon
      </div>
      <h1 class="font-serif-title text-3xl sm:text-5xl font-extrabold tracking-tight">
        Özel Tasarım Hazır Trend Ürünler
      </h1>
      <p class="text-sm sm:text-base text-slate-300 leading-relaxed">
        Nevartrend / Trenddesen atölyelerinde kendi ürettiğimiz ve özenle diktiğimiz <strong>kırlent, fular, kimono, masa örtüsü ve kanvas çantalar</strong>. Birinci sınıf kumaş ve garantili solmaz dijital baskı kalitesi.
      </p>
      <div class="flex flex-wrap items-center gap-4 pt-2">
        <a href="#koleksiyon-grid" class="px-6 py-3 bg-amber-600 hover:bg-amber-500 text-white rounded-xl text-sm font-bold shadow-lg transition flex items-center gap-2">
          <i data-lucide="shopping-bag" class="w-4 h-4"></i> Ürünleri İncele
        </a>
        <a href="https://wa.me/908503000000?text=Toptan%20veya%20özel%20üretim%20hazır%20ürün%20hakkında%20bilgi%20almak%20istiyorum." target="_blank" class="px-6 py-3 bg-white/10 hover:bg-white/20 text-white rounded-xl text-sm font-bold backdrop-blur-sm border border-white/20 transition flex items-center gap-2">
          <i data-lucide="message-circle" class="w-4 h-4 text-emerald-400"></i> Toptan / Özel Dikim Talebi
        </a>
      </div>
    </div>
  </div>

  <!-- Category Filter Pills -->
  <div id="koleksiyon-grid" class="flex flex-wrap items-center justify-between gap-4 border-b border-slate-200 pb-4">
    <div class="flex flex-wrap items-center gap-2">
      <a href="/trend-urunler?category=all" class="px-4 py-2 rounded-xl text-xs font-bold transition {% if selected_category == 'all' or not selected_category %}bg-slate-900 text-white shadow-sm{% else %}bg-slate-100 text-slate-600 hover:bg-slate-200{% endif %}">
        Tüm Hazır Ürünler ({{ total_count }})
      </a>
      <a href="/trend-urunler?category=giyim-butik" class="px-4 py-2 rounded-xl text-xs font-bold transition {% if selected_category == 'giyim-butik' %}bg-amber-700 text-white shadow-sm{% else %}bg-slate-100 text-slate-600 hover:bg-slate-200{% endif %}">
        👗 Fular, Kimono & Giyim
      </a>
      <a href="/trend-urunler?category=canta-aksesuar" class="px-4 py-2 rounded-xl text-xs font-bold transition {% if selected_category == 'canta-aksesuar' %}bg-amber-700 text-white shadow-sm{% else %}bg-slate-100 text-slate-600 hover:bg-slate-200{% endif %}">
        🛍️ Kanvas Bez Çanta
      </a>
      <a href="/trend-urunler?category=ev-tekstili" class="px-4 py-2 rounded-xl text-xs font-bold transition {% if selected_category == 'ev-tekstili' %}bg-amber-700 text-white shadow-sm{% else %}bg-slate-100 text-slate-600 hover:bg-slate-200{% endif %}">
        🛋️ Kırlent & Yastık Kılıfı
      </a>
      <a href="/trend-urunler?category=runner-setler" class="px-4 py-2 rounded-xl text-xs font-bold transition {% if selected_category == 'runner-setler' %}bg-amber-700 text-white shadow-sm{% else %}bg-slate-100 text-slate-600 hover:bg-slate-200{% endif %}">
        🍽️ Pofuduk Minder & Runner Setler
      </a>
      <a href="/trend-urunler?category=sal-esarp" class="px-4 py-2 rounded-xl text-xs font-bold transition {% if selected_category == 'sal-esarp' %}bg-amber-700 text-white shadow-sm{% else %}bg-slate-100 text-slate-600 hover:bg-slate-200{% endif %}">
        🧣 Şal & Eşarp
      </a>
      <a href="/trend-urunler?category=tayt-pantolon" class="px-4 py-2 rounded-xl text-xs font-bold transition {% if selected_category == 'tayt-pantolon' %}bg-amber-700 text-white shadow-sm{% else %}bg-slate-100 text-slate-600 hover:bg-slate-200{% endif %}">
        👖 Tayt & Pantolon
      </a>
    </div>

    <span class="text-xs text-slate-500 font-medium">
      Toplam <strong class="text-slate-800">{{ products|length }}</strong> ürün listeleniyor
    </span>
  </div>

  <!-- Product Grid -->
  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
    {% for p in products %}
    <div class="bg-white rounded-3xl border border-slate-200 overflow-hidden shadow-sm hover:shadow-xl transition-all duration-300 flex flex-col justify-between group">
      <div>
        <!-- Image Box -->
        <div class="h-64 sm:h-72 bg-slate-100 relative overflow-hidden">
          <img src="{{ p.image }}" alt="{{ p.title }}" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700">
          
          <!-- Badges -->
          <div class="absolute top-4 left-4 flex flex-col gap-1.5 z-10">
            <span class="px-3 py-1 bg-amber-600 text-white font-extrabold text-[11px] rounded-lg shadow-md uppercase tracking-wider">
              {{ p.badge }}
            </span>
            <span class="px-2.5 py-0.5 bg-slate-900/80 backdrop-blur-sm text-white font-semibold text-[10px] rounded-md">
              {{ p.fabric_type }}
            </span>
          </div>

          {% if p.old_price %}
          <span class="absolute top-4 right-4 px-2.5 py-1 bg-rose-600 text-white font-bold text-xs rounded-lg shadow-md z-10">
            İndirim
          </span>
          {% endif %}
        </div>

        <!-- Details -->
        <div class="p-6 space-y-4">
          <div>
            <span class="text-[10px] font-bold text-amber-700 uppercase tracking-widest block">{{ p.category_name }}</span>
            <h3 class="font-bold text-slate-900 text-base group-hover:text-amber-700 transition leading-snug mt-1">
              {{ p.title }}
            </h3>
          </div>

          <p class="text-xs text-slate-600 leading-relaxed line-clamp-2">
            {{ p.description }}
          </p>

          <!-- Features -->
          <div class="space-y-1.5 pt-2 border-t border-slate-100">
            {% for feat in p.features[:3] %}
            <div class="flex items-center gap-2 text-xs text-slate-500">
              <i data-lucide="check-circle-2" class="w-3.5 h-3.5 text-emerald-600 flex-shrink-0"></i>
              <span>{{ feat }}</span>
            </div>
            {% endfor %}
          </div>

          <!-- Size Options -->
          <div class="pt-2">
            <span class="text-[11px] font-bold text-slate-700 block mb-1.5">Mevcut Ölçü / Beden:</span>
            <div class="flex flex-wrap gap-1.5">
              {% for s in p.size_options %}
              <span class="px-2.5 py-1 bg-slate-100 text-slate-700 rounded-lg text-[11px] font-semibold border border-slate-200">
                {{ s }}
              </span>
              {% endfor %}
            </div>
          </div>
        </div>
      </div>

      <!-- Price & Actions -->
      <div class="p-6 pt-0 border-t border-slate-100 mt-2">
        <div class="flex items-center justify-between mb-4 pt-3">
          <div>
            {% if p.old_price %}
            <span class="text-xs text-slate-400 line-through block">{{ p.old_price }} TL</span>
            {% endif %}
            <span class="text-2xl font-extrabold text-slate-900">{{ p.price }} TL</span>
            <span class="text-[10px] text-slate-400 block font-medium">KDV Dahil</span>
          </div>
          
          <span class="px-2.5 py-1 bg-emerald-50 text-emerald-700 text-xs font-bold rounded-lg border border-emerald-200 flex items-center gap-1">
            <i data-lucide="check" class="w-3 h-3"></i> Stokta Var
          </span>
        </div>

        <div class="grid grid-cols-2 gap-2">
          <button onclick="CartEngine.addItem({
            id: '{{ p.id }}',
            title: '{{ p.title }}',
            code: '{{ p.code }}',
            category: 'Trend Ürünler',
            unit_price: {{ p.price }},
            quantity: 1,
            image: '{{ p.image }}',
            options: { fabric: '{{ p.fabric_type }}', size: '{{ p.size_options[0] }}' }
          })" class="w-full py-3 bg-amber-600 hover:bg-amber-700 text-white rounded-xl text-xs font-bold transition flex items-center justify-center gap-1.5 shadow-sm">
            <i data-lucide="shopping-cart" class="w-4 h-4"></i> Sepete Ekle
          </button>

          <a href="https://wa.me/908503000000?text=Merhaba,%20{{ p.title|urlencode }}%20ürünü%20hakkında%20bilgi%20veya%20özel%20sipariş%20vermek%20istiyorum." target="_blank" class="w-full py-3 bg-emerald-800 hover:bg-emerald-900 text-white rounded-xl text-xs font-bold transition flex items-center justify-center gap-1.5 shadow-sm">
            <i data-lucide="message-circle" class="w-4 h-4 text-emerald-300"></i> WhatsApp
          </a>
        </div>
      </div>
    </div>
    {% endfor %}
  </div>

</div>
{% endblock %}
'''

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(template_html)

print("Updated templates/trend_urunler.html successfully!")
