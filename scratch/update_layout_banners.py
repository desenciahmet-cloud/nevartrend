import re

def update_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Replace Left Column section (from <!-- 1. LEFT COLUMN to <!-- 2. CENTER COLUMN)
    new_left = '''      <!-- 1. LEFT COLUMN (col-span-3): KATEGORİLER SIDEBAR (DESENLER MAIN + SUB-LAYERS) -->
      <div class="lg:col-span-3 space-y-2.5 sticky top-24">
        <div class="flex items-center gap-2 px-1 mb-1">
          <span class="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></span>
          <span class="text-[10px] font-extrabold text-slate-700 uppercase tracking-widest block">KATEGORİLER</span>
        </div>

        <!-- MAIN DESENLER ACCORDION CARD (COLLAPSED / CLOSED BY DEFAULT WITH ARROW ICON) -->
        <div class="bg-emerald-900/90 rounded-2xl p-1.5 border border-emerald-700/60 shadow-md">
          <button type="button" onclick="toggleLeftDesenlerMenu()" class="w-full h-11 px-3.5 bg-emerald-800 hover:bg-emerald-950 text-white rounded-xl text-xs font-extrabold flex items-center justify-between transition shadow-2xs group">
            <div class="flex items-center gap-2">
              <i data-lucide="palette" class="w-4 h-4 text-emerald-300"></i>
              <span>DESENLER (74 DESEN)</span>
            </div>
            <div class="flex items-center gap-2">
              <span class="px-2 py-0.5 bg-emerald-950 text-emerald-300 font-mono font-extrabold text-[10px] rounded-md">74</span>
              <i data-lucide="chevron-down" id="desenlerMenuChevron" class="w-4 h-4 text-emerald-300 transform transition-transform duration-300"></i>
            </div>
          </button>

          <!-- SUB-LAYERS (CLOSED BY DEFAULT, EXPANDS ON CLICK) -->
          <div id="desenlerSubMenu" class="pl-1 pr-1 space-y-1 pt-1.5 border-t border-emerald-800/80 mt-1.5" style="display: none;">
            <a href="/studyo" class="w-full px-3 py-1.5 bg-emerald-700 hover:bg-emerald-600 text-white rounded-lg text-[11px] font-extrabold flex items-center justify-between transition border border-emerald-500/40 shadow-2xs mb-1.5">
              <div class="flex items-center gap-2">
                <i data-lucide="sparkles" class="w-3.5 h-3.5 text-emerald-200"></i>
                <span>3D CANLI STÜDYO</span>
              </div>
              <span class="px-1.5 py-0.5 bg-emerald-950 text-emerald-300 font-mono font-extrabold text-[9px] rounded">3D GÖR</span>
            </a>

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

        <div class="space-y-2.5 pt-1">
          <a href="/kumaslar" class="w-full h-11 px-3.5 bg-slate-900 hover:bg-slate-800 text-white rounded-xl text-xs font-extrabold shadow-2xs flex items-center justify-between transition hover:translate-x-1">
            <div class="flex items-center gap-2">
              <i data-lucide="layers" class="w-4 h-4 text-emerald-300"></i>
              <span>KUMAŞ KARTELASI</span>
            </div>
            <span class="px-2 py-0.5 bg-slate-950 text-emerald-300 font-mono font-extrabold text-[10px] rounded-md">7 Tür</span>
          </a>

          <a href="/dijital-baski" class="w-full h-11 px-3.5 bg-slate-900 hover:bg-slate-800 text-white rounded-xl text-xs font-extrabold shadow-2xs flex items-center justify-between transition hover:translate-x-1">
            <div class="flex items-center gap-2">
              <i data-lucide="printer" class="w-4 h-4 text-emerald-300"></i>
              <span>DİJİTAL BASKI</span>
            </div>
            <i data-lucide="chevron-right" class="w-4 h-4 text-emerald-300"></i>
          </a>

          <a href="/emprime" class="w-full h-11 px-3.5 bg-slate-900 hover:bg-slate-800 text-white rounded-xl text-xs font-extrabold shadow-2xs flex items-center justify-between transition hover:translate-x-1">
            <div class="flex items-center gap-2">
              <i data-lucide="split" class="w-4 h-4 text-emerald-300"></i>
              <span>EMPRİME FİLM</span>
            </div>
            <span class="px-2 py-0.5 bg-slate-950 text-emerald-300 font-mono font-extrabold text-[10px] rounded-md">4.0 Dmax</span>
          </a>

          <a href="/trend-urunler" class="w-full h-11 px-3.5 bg-amber-700 hover:bg-amber-800 text-white rounded-xl text-xs font-extrabold shadow-2xs flex items-center justify-between transition hover:translate-x-1">
            <div class="flex items-center gap-2">
              <i data-lucide="shopping-bag" class="w-4 h-4 text-amber-300"></i>
              <span>BUTİK TREND ÜRÜNLER</span>
            </div>
            <span class="px-2 py-0.5 bg-amber-950 text-amber-300 font-mono font-extrabold text-[10px] rounded-md">Hazır</span>
          </a>
        </div>
      </div>'''

    # Replace Right Column section (from <!-- 3. RIGHT COLUMN to <!-- SEAMLESS PATTERN CATALOG)
    new_right = '''      <!-- 3. RIGHT COLUMN (col-span-4): HERO & MAŞET CARD -->
      <div class="lg:col-span-4 space-y-4">
        <div class="bg-white p-5 sm:p-6 rounded-2xl border border-slate-200 shadow-xs space-y-3.5">
          
          <!-- Badge -->
          <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-sage-100/90 text-sage-900 border border-sage-200 text-[11px] font-extrabold tracking-wide shadow-2xs">
            <span class="w-2 h-2 rounded-full bg-emerald-600 animate-pulse"></span>
            <span>TRENDDESEN KOLEKSİYONU & METRAJ BASKI</span>
          </div>

          <!-- Main Heading -->
          <h1 class="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight font-serif-title leading-snug">
            Deseni seç.<br>
            <span class="text-emerald-700 italic font-normal">Üzerinde gör.</span>
          </h1>

          <!-- Subtitle -->
          <p class="text-xs sm:text-sm text-slate-600 font-normal leading-relaxed">
            Koleksiyonundan bir desen seç, üründe nasıl duracağını keşfet. 74 dikişsiz desenimizi ortadaki canlı model üzerinde ve 3D stüdyomuzda 9 farklı anatomik modelde anında canlı giydirin.
          </p>

          <!-- CTA Buttons -->
          <div class="flex flex-col gap-2.5 pt-1">
            <a href="/studyo" class="w-full px-4 py-2.5 bg-emerald-800 hover:bg-emerald-900 text-white rounded-xl text-xs font-extrabold shadow-md hover:scale-[1.01] transition-all flex items-center justify-center gap-2">
              <i data-lucide="sparkles" class="w-4 h-4 text-emerald-300"></i>
              <span>3D Canlı Stüdyoda Dene</span>
              <i data-lucide="arrow-right" class="w-4 h-4"></i>
            </a>

            <a href="/fabrics?category=all" class="w-full px-4 py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-800 rounded-xl text-xs font-bold border border-slate-200/80 transition-all flex items-center justify-center gap-2">
              <i data-lucide="grid" class="w-4 h-4 text-slate-600"></i>
              <span>74 Desen Kataloğunu İncele</span>
            </a>
          </div>

          <!-- Trust Badges -->
          <div class="pt-3 border-t border-slate-100 flex flex-wrap items-center gap-3 text-[11px] text-slate-500 font-medium">
            <span class="flex items-center gap-1"><i data-lucide="check-circle" class="w-3.5 h-3.5 text-emerald-600"></i> Min. 1 Metre Sipariş</span>
            <span class="flex items-center gap-1"><i data-lucide="check-circle" class="w-3.5 h-3.5 text-emerald-600"></i> OEKO-TEX Sertifikalı</span>
            <span class="flex items-center gap-1"><i data-lucide="check-circle" class="w-3.5 h-3.5 text-emerald-600"></i> 48 Saatte Kargo</span>
          </div>

        </div>
      </div>'''

    pattern_left = re.compile(r'<!-- 1\. LEFT COLUMN.*?<!-- 2\. CENTER COLUMN', re.DOTALL)
    html = pattern_left.sub(new_left + '\n\n      <!-- 2. CENTER COLUMN', html)

    pattern_right = re.compile(r'<!-- 3\. RIGHT COLUMN.*?<!-- SEAMLESS PATTERN CATALOG', re.DOTALL)
    html = pattern_right.sub(new_right + '\n\n    </div>\n\n  </div>\n</section>\n\n<!-- SEAMLESS PATTERN CATALOG', html)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print('Updated', path)

update_file('index.html')
update_file('templates/index.html')
