import re

# Update templates/index.html and index.html
with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_left_sidebar = """      <!-- 1. LEFT COLUMN (col-span-3): KATEGORİLER SIDEBAR (EXACT 5 CATEGORIES + SERVICES) -->
      <div class="lg:col-span-3 space-y-2 sticky top-24">
        <div class="flex items-center gap-2 px-1 mb-1">
          <span class="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></span>
          <span class="text-[10px] font-extrabold text-slate-700 uppercase tracking-widest block">KATEGORİLER</span>
        </div>

        <!-- 5 Exact Category Filters -->
        <button type="button" onclick="selectCategoryLeft('cicekli-botanik')" class="left-cat-btn w-full px-3.5 py-2 bg-emerald-800 hover:bg-emerald-900 text-white rounded-xl text-[11px] font-extrabold shadow-2xs flex items-center justify-between transition hover:translate-x-1">
          <div class="flex items-center gap-2">
            <i data-lucide="flower-2" class="w-3.5 h-3.5 text-emerald-300"></i>
            <span>1. ÇİÇEKLİ & BOTANİK</span>
          </div>
          <span class="px-2 py-0.5 bg-emerald-950 text-emerald-300 font-mono font-extrabold text-[9px] rounded-md">15</span>
        </button>

        <button type="button" onclick="selectCategoryLeft('barok-saray')" class="left-cat-btn w-full px-3.5 py-2 bg-emerald-800 hover:bg-emerald-900 text-white rounded-xl text-[11px] font-extrabold shadow-2xs flex items-center justify-between transition hover:translate-x-1">
          <div class="flex items-center gap-2">
            <i data-lucide="crown" class="w-3.5 h-3.5 text-emerald-300"></i>
            <span>2. BAROK & SARAY</span>
          </div>
          <span class="px-2 py-0.5 bg-emerald-950 text-emerald-300 font-mono font-extrabold text-[9px] rounded-md">14</span>
        </button>

        <button type="button" onclick="selectCategoryLeft('geometrik')" class="left-cat-btn w-full px-3.5 py-2 bg-emerald-800 hover:bg-emerald-900 text-white rounded-xl text-[11px] font-extrabold shadow-2xs flex items-center justify-between transition hover:translate-x-1">
          <div class="flex items-center gap-2">
            <i data-lucide="shapes" class="w-3.5 h-3.5 text-emerald-300"></i>
            <span>3. GEOMETRİK</span>
          </div>
          <span class="px-2 py-0.5 bg-emerald-950 text-emerald-300 font-mono font-extrabold text-[9px] rounded-md">15</span>
        </button>

        <button type="button" onclick="selectCategoryLeft('dokular-fircalar')" class="left-cat-btn w-full px-3.5 py-2 bg-emerald-800 hover:bg-emerald-900 text-white rounded-xl text-[11px] font-extrabold shadow-2xs flex items-center justify-between transition hover:translate-x-1">
          <div class="flex items-center gap-2">
            <i data-lucide="brush" class="w-3.5 h-3.5 text-emerald-300"></i>
            <span>4. DOKULAR - FIRÇALAR</span>
          </div>
          <span class="px-2 py-0.5 bg-emerald-950 text-emerald-300 font-mono font-extrabold text-[9px] rounded-md">15</span>
        </button>

        <button type="button" onclick="selectCategoryLeft('vintage-etnik')" class="left-cat-btn w-full px-3.5 py-2 bg-emerald-800 hover:bg-emerald-900 text-white rounded-xl text-[11px] font-extrabold shadow-2xs flex items-center justify-between transition hover:translate-x-1">
          <div class="flex items-center gap-2">
            <i data-lucide="sparkles" class="w-3.5 h-3.5 text-emerald-300"></i>
            <span>5. VİNTAGE & ETNİK</span>
          </div>
          <span class="px-2 py-0.5 bg-emerald-950 text-emerald-300 font-mono font-extrabold text-[9px] rounded-md">15</span>
        </button>

        <div class="pt-2 border-t border-slate-200/70 space-y-2">
          <a href="/kumaslar" class="w-full px-3.5 py-2 bg-slate-900 hover:bg-slate-800 text-white rounded-xl text-[11px] font-extrabold shadow-2xs flex items-center justify-between transition hover:translate-x-1">
            <div class="flex items-center gap-2">
              <i data-lucide="layers" class="w-3.5 h-3.5 text-emerald-300"></i>
              <span>KUMAŞ KARTELASI</span>
            </div>
            <span class="px-2 py-0.5 bg-slate-950 text-emerald-300 font-mono font-extrabold text-[9px] rounded-md">7 Tür</span>
          </a>

          <a href="/dijital-baski" class="w-full px-3.5 py-2 bg-slate-900 hover:bg-slate-800 text-white rounded-xl text-[11px] font-extrabold shadow-2xs flex items-center justify-between transition hover:translate-x-1">
            <div class="flex items-center gap-2">
              <i data-lucide="printer" class="w-3.5 h-3.5 text-emerald-300"></i>
              <span>DİJİTAL BASKI</span>
            </div>
            <i data-lucide="chevron-right" class="w-3.5 h-3.5 text-emerald-300"></i>
          </a>

          <a href="/emprime" class="w-full px-3.5 py-2 bg-slate-900 hover:bg-slate-800 text-white rounded-xl text-[11px] font-extrabold shadow-2xs flex items-center justify-between transition hover:translate-x-1">
            <div class="flex items-center gap-2">
              <i data-lucide="split" class="w-3.5 h-3.5 text-emerald-300"></i>
              <span>EMPRİME FİLM</span>
            </div>
            <span class="px-2 py-0.5 bg-slate-950 text-emerald-300 font-mono font-extrabold text-[9px] rounded-md">4.0 Dmax</span>
          </a>

          <a href="/trend-urunler" class="w-full px-3.5 py-2 bg-amber-700 hover:bg-amber-800 text-white rounded-xl text-[11px] font-extrabold shadow-2xs flex items-center justify-between transition hover:translate-x-1">
            <div class="flex items-center gap-2">
              <i data-lucide="shopping-bag" class="w-3.5 h-3.5 text-amber-300"></i>
              <span>BUTİK TREND ÜRÜNLER</span>
            </div>
            <span class="px-2 py-0.5 bg-amber-950 text-amber-300 font-mono font-extrabold text-[9px] rounded-md">Hazır</span>
          </a>
        </div>
      </div>"""

new_left_sidebar = """      <!-- 1. LEFT COLUMN (col-span-3): KATEGORİLER SIDEBAR (DESENLER MAIN + 5 SUB-LAYERS) -->
      <div class="lg:col-span-3 space-y-2.5 sticky top-24">
        <div class="flex items-center gap-2 px-1 mb-1">
          <span class="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></span>
          <span class="text-[10px] font-extrabold text-slate-700 uppercase tracking-widest block">KATEGORİLER</span>
        </div>

        <!-- MAIN DESENLER MENU CARD WITH NESTED SUB-LAYERS (ALT KATMANLAR) -->
        <div class="bg-emerald-900/90 rounded-2xl p-2 space-y-1.5 border border-emerald-700/60 shadow-md">
          <a href="/fabrics?category=all" class="w-full px-3.5 py-2.5 bg-emerald-800 hover:bg-emerald-950 text-white rounded-xl text-xs font-extrabold flex items-center justify-between transition shadow-2xs">
            <div class="flex items-center gap-2">
              <i data-lucide="palette" class="w-4 h-4 text-emerald-300"></i>
              <span>DESENLER (74 DESEN)</span>
            </div>
            <span class="px-2 py-0.5 bg-emerald-950 text-emerald-300 font-mono font-extrabold text-[10px] rounded-md">74</span>
          </a>

          <!-- SUB-LAYERS (ALT KATMANLAR: 5 EXACT CATEGORIES) -->
          <div class="pl-1 pr-1 space-y-1 pt-1.5 border-t border-emerald-800/80">
            <button type="button" onclick="selectCategoryLeft('cicekli-botanik')" class="sub-cat-btn w-full px-3 py-1.5 bg-emerald-800/80 hover:bg-emerald-700 text-white rounded-lg text-[11px] font-bold flex items-center justify-between transition hover:translate-x-1 border border-emerald-600/30">
              <div class="flex items-center gap-2">
                <span class="w-1.5 h-1.5 rounded-full bg-emerald-300"></span>
                <span>1. ÇİÇEKLİ & BOTANİK</span>
              </div>
              <span class="px-1.5 py-0.5 bg-emerald-950/80 text-emerald-300 font-mono font-extrabold text-[9px] rounded">15</span>
            </button>

            <button type="button" onclick="selectCategoryLeft('barok-saray')" class="sub-cat-btn w-full px-3 py-1.5 bg-emerald-800/80 hover:bg-emerald-700 text-white rounded-lg text-[11px] font-bold flex items-center justify-between transition hover:translate-x-1 border border-emerald-600/30">
              <div class="flex items-center gap-2">
                <span class="w-1.5 h-1.5 rounded-full bg-emerald-300"></span>
                <span>2. BAROK & SARAY</span>
              </div>
              <span class="px-1.5 py-0.5 bg-emerald-950/80 text-emerald-300 font-mono font-extrabold text-[9px] rounded">14</span>
            </button>

            <button type="button" onclick="selectCategoryLeft('geometrik')" class="sub-cat-btn w-full px-3 py-1.5 bg-emerald-800/80 hover:bg-emerald-700 text-white rounded-lg text-[11px] font-bold flex items-center justify-between transition hover:translate-x-1 border border-emerald-600/30">
              <div class="flex items-center gap-2">
                <span class="w-1.5 h-1.5 rounded-full bg-emerald-300"></span>
                <span>3. GEOMETRİK</span>
              </div>
              <span class="px-1.5 py-0.5 bg-emerald-950/80 text-emerald-300 font-mono font-extrabold text-[9px] rounded">15</span>
            </button>

            <button type="button" onclick="selectCategoryLeft('dokular-fircalar')" class="sub-cat-btn w-full px-3 py-1.5 bg-emerald-800/80 hover:bg-emerald-700 text-white rounded-lg text-[11px] font-bold flex items-center justify-between transition hover:translate-x-1 border border-emerald-600/30">
              <div class="flex items-center gap-2">
                <span class="w-1.5 h-1.5 rounded-full bg-emerald-300"></span>
                <span>4. DOKULAR - FIRÇALAR</span>
              </div>
              <span class="px-1.5 py-0.5 bg-emerald-950/80 text-emerald-300 font-mono font-extrabold text-[9px] rounded">15</span>
            </button>

            <button type="button" onclick="selectCategoryLeft('vintage-etnik')" class="sub-cat-btn w-full px-3 py-1.5 bg-emerald-800/80 hover:bg-emerald-700 text-white rounded-lg text-[11px] font-bold flex items-center justify-between transition hover:translate-x-1 border border-emerald-600/30">
              <div class="flex items-center gap-2">
                <span class="w-1.5 h-1.5 rounded-full bg-emerald-300"></span>
                <span>5. VİNTAGE & ETNİK</span>
              </div>
              <span class="px-1.5 py-0.5 bg-emerald-950/80 text-emerald-300 font-mono font-extrabold text-[9px] rounded">15</span>
            </button>
          </div>
        </div>

        <div class="space-y-2 pt-1">
          <a href="/studyo" class="w-full px-3.5 py-2.5 bg-emerald-800 hover:bg-emerald-900 text-white rounded-xl text-xs font-extrabold shadow-2xs flex items-center justify-between transition hover:translate-x-1">
            <div class="flex items-center gap-2">
              <i data-lucide="sparkles" class="w-4 h-4 text-emerald-300"></i>
              <span>CANLI STÜDYO</span>
            </div>
            <span class="px-2 py-0.5 bg-emerald-950 text-emerald-300 font-mono font-extrabold text-[10px] rounded-md">3D</span>
          </a>

          <a href="/kumaslar" class="w-full px-3.5 py-2 bg-slate-900 hover:bg-slate-800 text-white rounded-xl text-[11px] font-extrabold shadow-2xs flex items-center justify-between transition hover:translate-x-1">
            <div class="flex items-center gap-2">
              <i data-lucide="layers" class="w-3.5 h-3.5 text-emerald-300"></i>
              <span>KUMAŞ KARTELASI</span>
            </div>
            <span class="px-2 py-0.5 bg-slate-950 text-emerald-300 font-mono font-extrabold text-[9px] rounded-md">7 Tür</span>
          </a>

          <a href="/dijital-baski" class="w-full px-3.5 py-2 bg-slate-900 hover:bg-slate-800 text-white rounded-xl text-[11px] font-extrabold shadow-2xs flex items-center justify-between transition hover:translate-x-1">
            <div class="flex items-center gap-2">
              <i data-lucide="printer" class="w-3.5 h-3.5 text-emerald-300"></i>
              <span>DİJİTAL BASKI</span>
            </div>
            <i data-lucide="chevron-right" class="w-3.5 h-3.5 text-emerald-300"></i>
          </a>

          <a href="/emprime" class="w-full px-3.5 py-2 bg-slate-900 hover:bg-slate-800 text-white rounded-xl text-[11px] font-extrabold shadow-2xs flex items-center justify-between transition hover:translate-x-1">
            <div class="flex items-center gap-2">
              <i data-lucide="split" class="w-3.5 h-3.5 text-emerald-300"></i>
              <span>EMPRİME FİLM</span>
            </div>
            <span class="px-2 py-0.5 bg-slate-950 text-emerald-300 font-mono font-extrabold text-[9px] rounded-md">4.0 Dmax</span>
          </a>

          <a href="/trend-urunler" class="w-full px-3.5 py-2 bg-amber-700 hover:bg-amber-800 text-white rounded-xl text-[11px] font-extrabold shadow-2xs flex items-center justify-between transition hover:translate-x-1">
            <div class="flex items-center gap-2">
              <i data-lucide="shopping-bag" class="w-3.5 h-3.5 text-amber-300"></i>
              <span>BUTİK TREND ÜRÜNLER</span>
            </div>
            <span class="px-2 py-0.5 bg-amber-950 text-amber-300 font-mono font-extrabold text-[9px] rounded-md">Hazır</span>
          </a>
        </div>
      </div>"""

content = content.replace(old_left_sidebar, new_left_sidebar)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated templates/index.html and index.html with DESENLER main section + 5 sub-layers (alt katmanlar)!")
