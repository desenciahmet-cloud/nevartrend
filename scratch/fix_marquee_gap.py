import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace hardcoded marquee cards with 12 items duplicated in Jinja2 loop for continuous seamless ticker
old_marquee = """    <div class="animate-marquee-left flex gap-4 items-center">
      
      <a href="/studyo?pattern=NT_015" onclick="selectCatwalkPatternByCode('NT_015'); return false;" class="flex-shrink-0 bg-[#F4F6F4] hover:bg-[#EAEFEA] border border-emerald-900/10 hover:border-emerald-600/60 rounded-2xl p-2.5 flex items-center gap-3.5 transition group shadow-2xs min-w-[290px]">
        <img src="/static/images/NT_015.jpg" class="w-20 h-20 rounded-xl object-cover border border-slate-300/80 group-hover:scale-105 transition shadow-2xs flex-shrink-0" alt="NT_015">
        <div>
          <span class="px-2 py-0.5 bg-emerald-100 text-emerald-900 font-mono font-extrabold text-[10px] rounded-md inline-block mb-1 border border-emerald-200">NT_015</span>
          <h4 class="text-xs sm:text-sm font-extrabold text-slate-900 group-hover:text-emerald-800 transition line-clamp-1">Tropikal Gece Palmiye</h4>
          <span class="text-xs text-slate-600 font-medium block mt-0.5">185 TL/mt • Vintage & Etnik</span>
        </div>
      </a>

      <a href="/studyo?pattern=NT_001" onclick="selectCatwalkPatternByCode('NT_001'); return false;" class="flex-shrink-0 bg-[#F4F6F4] hover:bg-[#EAEFEA] border border-emerald-900/10 hover:border-amber-600/60 rounded-2xl p-2.5 flex items-center gap-3.5 transition group shadow-2xs min-w-[290px]">
        <img src="/static/images/NT_001.jpg" class="w-20 h-20 rounded-xl object-cover border border-slate-300/80 group-hover:scale-105 transition shadow-2xs flex-shrink-0" alt="NT_001">
        <div>
          <span class="px-2 py-0.5 bg-amber-100 text-amber-900 font-mono font-extrabold text-[10px] rounded-md inline-block mb-1 border border-amber-200">NT_001</span>
          <h4 class="text-xs sm:text-sm font-extrabold text-slate-900 group-hover:text-amber-800 transition line-clamp-1">Zümrüt Şakayık Çiçeği</h4>
          <span class="text-xs text-slate-600 font-medium block mt-0.5">195 TL/mt • Çiçekli & Botanik</span>
        </div>
      </a>

      <a href="/studyo?pattern=NT_074" onclick="selectCatwalkPatternByCode('NT_074'); return false;" class="flex-shrink-0 bg-[#F4F6F4] hover:bg-[#EAEFEA] border border-emerald-900/10 hover:border-emerald-600/60 rounded-2xl p-2.5 flex items-center gap-3.5 transition group shadow-2xs min-w-[290px]">
        <img src="/static/images/NT_074.jpg" class="w-20 h-20 rounded-xl object-cover border border-slate-300/80 group-hover:scale-105 transition shadow-2xs flex-shrink-0" alt="NT_074">
        <div>
          <span class="px-2 py-0.5 bg-emerald-100 text-emerald-900 font-mono font-extrabold text-[10px] rounded-md inline-block mb-1 border border-emerald-200">NT_074</span>
          <h4 class="text-xs sm:text-sm font-extrabold text-slate-900 group-hover:text-emerald-800 transition line-clamp-1">Gece Siyahı Botanik</h4>
          <span class="text-xs text-slate-600 font-medium block mt-0.5">195 TL/mt • Çiçekli & Botanik</span>
        </div>
      </a>

      <a href="/studyo?pattern=NT_042" onclick="selectCatwalkPatternByCode('NT_042'); return false;" class="flex-shrink-0 bg-[#F4F6F4] hover:bg-[#EAEFEA] border border-emerald-900/10 hover:border-amber-600/60 rounded-2xl p-2.5 flex items-center gap-3.5 transition group shadow-2xs min-w-[290px]">
        <img src="/static/images/NT_042.jpg" class="w-20 h-20 rounded-xl object-cover border border-slate-300/80 group-hover:scale-105 transition shadow-2xs flex-shrink-0" alt="NT_042">
        <div>
          <span class="px-2 py-0.5 bg-amber-100 text-amber-900 font-mono font-extrabold text-[10px] rounded-md inline-block mb-1 border border-amber-200">NT_042</span>
          <h4 class="text-xs sm:text-sm font-extrabold text-slate-900 group-hover:text-amber-800 transition line-clamp-1">Krem Barok Saray</h4>
          <span class="text-xs text-slate-600 font-medium block mt-0.5">195 TL/mt • Barok & Saray</span>
        </div>
      </a>

      <a href="/studyo?pattern=NT_036" onclick="selectCatwalkPatternByCode('NT_036'); return false;" class="flex-shrink-0 bg-[#F4F6F4] hover:bg-[#EAEFEA] border border-emerald-900/10 hover:border-emerald-600/60 rounded-2xl p-2.5 flex items-center gap-3.5 transition group shadow-2xs min-w-[290px]">
        <img src="/static/images/NT_036.jpg" class="w-20 h-20 rounded-xl object-cover border border-slate-300/80 group-hover:scale-105 transition shadow-2xs flex-shrink-0" alt="NT_036">
        <div>
          <span class="px-2 py-0.5 bg-emerald-100 text-emerald-900 font-mono font-extrabold text-[10px] rounded-md inline-block mb-1 border border-emerald-200">NT_036</span>
          <h4 class="text-xs sm:text-sm font-extrabold text-slate-900 group-hover:text-emerald-800 transition line-clamp-1">Antrasit Gül Kurusu</h4>
          <span class="text-xs text-slate-600 font-medium block mt-0.5">185 TL/mt • Çiçekli & Botanik</span>
        </div>
      </a>

      <a href="/studyo?pattern=NT_011" onclick="selectCatwalkPatternByCode('NT_011'); return false;" class="flex-shrink-0 bg-[#F4F6F4] hover:bg-[#EAEFEA] border border-emerald-900/10 hover:border-slate-400/60 rounded-2xl p-2.5 flex items-center gap-3.5 transition group shadow-2xs min-w-[290px]">
        <img src="/static/images/NT_011.jpg" class="w-20 h-20 rounded-xl object-cover border border-slate-300/80 group-hover:scale-105 transition shadow-2xs flex-shrink-0" alt="NT_011">
        <div>
          <span class="px-2 py-0.5 bg-slate-200 text-slate-800 font-mono font-extrabold text-[10px] rounded-md inline-block mb-1 border border-slate-300">NT_011</span>
          <h4 class="text-xs sm:text-sm font-extrabold text-slate-900 group-hover:text-emerald-800 transition line-clamp-1">Pastel Gri Vintage</h4>
          <span class="text-xs text-slate-600 font-medium block mt-0.5">185 TL/mt • Vintage & Etnik</span>
        </div>
      </a>

      <!-- Duplicate Set for Infinite Scroll Loop -->
      <a href="/studyo?pattern=NT_015" onclick="selectCatwalkPatternByCode('NT_015'); return false;" class="flex-shrink-0 bg-[#F4F6F4] hover:bg-[#EAEFEA] border border-emerald-900/10 hover:border-emerald-600/60 rounded-2xl p-2.5 flex items-center gap-3.5 transition group shadow-2xs min-w-[290px]">
        <img src="/static/images/NT_015.jpg" class="w-20 h-20 rounded-xl object-cover border border-slate-300/80 group-hover:scale-105 transition shadow-2xs flex-shrink-0" alt="NT_015">
        <div>
          <span class="px-2 py-0.5 bg-emerald-100 text-emerald-900 font-mono font-extrabold text-[10px] rounded-md inline-block mb-1 border border-emerald-200">NT_015</span>
          <h4 class="text-xs sm:text-sm font-extrabold text-slate-900 group-hover:text-emerald-800 transition line-clamp-1">Tropikal Gece Palmiye</h4>
          <span class="text-xs text-slate-600 font-medium block mt-0.5">185 TL/mt • Vintage & Etnik</span>
        </div>
      </a>

    </div>"""

new_marquee = """    <div class="animate-marquee-left flex gap-4 items-center">
      {% for p in products[:15] %}
      <a href="/studyo?pattern={{ p.code }}" onclick="selectCatwalkPatternByCode('{{ p.code }}'); return false;" class="flex-shrink-0 bg-[#F4F6F4] hover:bg-[#EAEFEA] border border-emerald-900/10 hover:border-emerald-600/60 rounded-2xl p-2.5 flex items-center gap-3.5 transition group shadow-2xs min-w-[290px]">
        <img src="{{ p.image }}" class="w-20 h-20 rounded-xl object-cover border border-slate-300/80 group-hover:scale-105 transition shadow-2xs flex-shrink-0" alt="{{ p.code }}">
        <div>
          <span class="px-2 py-0.5 bg-emerald-100 text-emerald-900 font-mono font-extrabold text-[10px] rounded-md inline-block mb-1 border border-emerald-200">{{ p.code }}</span>
          <h4 class="text-xs sm:text-sm font-extrabold text-slate-900 group-hover:text-emerald-800 transition line-clamp-1">{{ p.title }}</h4>
          <span class="text-xs text-slate-600 font-medium block mt-0.5">{{ p.base_price }} TL/mt • {{ p.category_name }}</span>
        </div>
      </a>
      {% endfor %}

      <!-- Seamless Loop Set (No empty gap) -->
      {% for p in products[:15] %}
      <a href="/studyo?pattern={{ p.code }}" onclick="selectCatwalkPatternByCode('{{ p.code }}'); return false;" class="flex-shrink-0 bg-[#F4F6F4] hover:bg-[#EAEFEA] border border-emerald-900/10 hover:border-emerald-600/60 rounded-2xl p-2.5 flex items-center gap-3.5 transition group shadow-2xs min-w-[290px]">
        <img src="{{ p.image }}" class="w-20 h-20 rounded-xl object-cover border border-slate-300/80 group-hover:scale-105 transition shadow-2xs flex-shrink-0" alt="{{ p.code }}">
        <div>
          <span class="px-2 py-0.5 bg-emerald-100 text-emerald-900 font-mono font-extrabold text-[10px] rounded-md inline-block mb-1 border border-emerald-200">{{ p.code }}</span>
          <h4 class="text-xs sm:text-sm font-extrabold text-slate-900 group-hover:text-emerald-800 transition line-clamp-1">{{ p.title }}</h4>
          <span class="text-xs text-slate-600 font-medium block mt-0.5">{{ p.base_price }} TL/mt • {{ p.category_name }}</span>
        </div>
      </a>
      {% endfor %}
    </div>"""

content = content.replace(old_marquee, new_marquee)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed marquee gap: added 30 items total with seamless loop!")
