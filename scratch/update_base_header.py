import os

def update_base(filepath):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Define the new consolidated single-row header
    new_header = '''  <!-- Main Sticky Header -->
  <header class="sticky top-0 z-40 bg-white/95 backdrop-blur-md border-b border-slate-200/80 shadow-xs transition-all duration-300">
    <div class="max-w-[1600px] mx-auto px-4 sm:px-6 lg:px-8">
      
      <!-- Single Row Header: Menu, Logo, Anasayfa, History Nav, Search & Fast Actions -->
      <div class="flex items-center justify-between h-16 sm:h-20 gap-3">
        
        <!-- Left Controls: Menu, Logo, Anasayfa, Geri/İleri -->
        <div class="flex items-center gap-2.5 flex-shrink-0">
          <button type="button" onclick="toggleSidebarMenu()" class="inline-flex items-center gap-2 px-3.5 py-2 bg-[#183c2c] hover:bg-[#0f281d] text-white rounded-full text-xs font-extrabold transition shadow-2xs" aria-label="Menüyü Aç" title="Kategoriler ve Menü">
            <div class="flex flex-col gap-1 w-3.5 justify-center items-center">
              <span class="w-3.5 h-0.5 bg-white rounded-full block"></span>
              <span class="w-3.5 h-0.5 bg-white rounded-full block"></span>
              <span class="w-3.5 h-0.5 bg-white rounded-full block"></span>
            </div>
            <span class="hidden sm:inline tracking-tight">MENÜ</span>
          </button>

          <a href="/" class="flex items-center gap-2 flex-shrink-0 ml-1">
            <img src="/static/img/logo.png" alt="nevartrend by Trenddesen" class="h-8 sm:h-10 w-auto object-contain">
          </a>

          <a href="/" class="hidden md:inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-full bg-[#183c2c] text-white text-xs font-extrabold shadow-2xs">
            <i data-lucide="home" class="w-3.5 h-3.5"></i>
            <span>ANASAYFA</span>
          </a>

          <div class="hidden lg:flex items-center gap-1">
            <button type="button" onclick="window.history.back()" class="px-2.5 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold text-xs transition" title="Önceki Sayfa">
              ← Geri
            </button>
            <button type="button" onclick="window.history.forward()" class="px-2.5 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold text-xs transition" title="Sonraki Sayfa">
              İleri →
            </button>
          </div>
        </div>

        <!-- Center Search Bar -->
        <div class="flex-1 max-w-xl mx-2 sm:mx-4">
          <form action="/fabrics" method="GET" class="w-full relative flex items-center">
            <input 
              type="text" 
              name="q" 
              placeholder="Desen, kumaş veya hizmet ara (örnek: Şakayık, Poplin)..." 
              class="w-full pl-9 pr-16 py-2 bg-slate-100/90 border border-slate-200/80 rounded-full text-xs font-medium focus:outline-none focus:ring-2 focus:ring-emerald-600 focus:bg-white transition"
            >
            <i data-lucide="search" class="w-4 h-4 text-slate-400 absolute left-3"></i>
            <button type="submit" class="absolute right-1 px-3.5 py-1.5 bg-[#183c2c] text-white rounded-full text-[11px] font-bold hover:bg-[#0f281d] transition">
              Ara
            </button>
          </form>
        </div>

        <!-- Right Quick Action Controls -->
        <div class="flex items-center gap-2 flex-shrink-0">
          <a href="/studyo" class="inline-flex items-center gap-1.5 px-3.5 py-2 bg-emerald-50 hover:bg-emerald-100 text-emerald-800 rounded-full text-xs font-bold border border-emerald-200/80 transition shadow-2xs">
            <i data-lucide="sparkles" class="w-3.5 h-3.5 text-emerald-600"></i>
            <span class="hidden sm:inline">Canlı Stüdyo</span>
          </a>

          <button onclick="CartEngine.openDrawer()" class="relative px-3.5 py-2 text-slate-700 hover:text-emerald-800 hover:bg-slate-100 rounded-full transition flex items-center gap-2 border border-slate-200 bg-white shadow-2xs text-xs font-bold">
            <i data-lucide="shopping-bag" class="w-4 h-4"></i>
            <span class="cart-count-badge absolute -top-1 -right-1 bg-emerald-700 text-white text-[9px] font-bold rounded-full w-4 h-4 flex items-center justify-center border-2 border-white" style="display:none;">0</span>
            <span class="hidden sm:inline summary-subtotal">0 TL</span>
          </button>
        </div>

      </div>
    </div>
  </header>'''

    # Replace header section in base.html
    import re
    pattern = re.compile(r'<!-- Main Sticky Header -->.*?<!-- Page Body Content -->', re.DOTALL)
    new_content = pattern.sub(new_header + '\n\n  <!-- Page Body Content -->', content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Updated {filepath}")

update_base("base.html")
update_base("templates/base.html")
