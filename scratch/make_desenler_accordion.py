import re

# Update templates/index.html & index.html
with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_desenler_card = """        <!-- MAIN DESENLER MENU CARD WITH NESTED SUB-LAYERS (ALT KATMANLAR) -->
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
        </div>"""

new_desenler_card = """        <!-- MAIN DESENLER ACCORDION CARD (COLLAPSED / CLOSED BY DEFAULT WITH ARROW ICON) -->
        <div class="bg-emerald-900/90 rounded-2xl p-2 border border-emerald-700/60 shadow-md">
          <button type="button" onclick="toggleLeftDesenlerMenu()" class="w-full px-3.5 py-2.5 bg-emerald-800 hover:bg-emerald-950 text-white rounded-xl text-xs font-extrabold flex items-center justify-between transition shadow-2xs group">
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
        </div>"""

content = content.replace(old_desenler_card, new_desenler_card)

# Add toggleLeftDesenlerMenu JS function
toggle_js = """  window.toggleLeftDesenlerMenu = function() {
    const subMenu = document.getElementById('desenlerSubMenu');
    const chevron = document.getElementById('desenlerMenuChevron');
    if (!subMenu) return;
    const isHidden = subMenu.style.display === 'none';
    if (isHidden) {
      subMenu.style.display = 'block';
      if (chevron) chevron.style.transform = 'rotate(180deg)';
    } else {
      subMenu.style.display = 'none';
      if (chevron) chevron.style.transform = 'rotate(0deg)';
    }
  };

  // Left Sidebar Category Click -> Filter patterns & Update model with category pattern"""

content = content.replace("// Left Sidebar Category Click -> Filter patterns & Update model with category pattern", toggle_js)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated templates/index.html and index.html: DESENLER menu is now closed by default and opens/closes with chevron arrow!")
