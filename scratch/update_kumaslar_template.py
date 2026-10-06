import os

file_path = r'C:\Users\user\Desktop\nevartrend_ev\templates\kumaslar.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the fabric card top section to include the fabric thumbnail image
old_card_top = '''      <div class="bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-sm hover:shadow-md transition-all flex flex-col justify-between group">
        <div>
          <!-- Fabric Header -->
          <div class="p-6 pb-4 border-b border-slate-100 bg-gradient-to-b from-slate-50 to-white">
            <div class="flex items-start justify-between gap-2 mb-2">
              <span class="px-2.5 py-1 bg-emerald-100 text-emerald-800 text-[11px] font-extrabold rounded-lg">
                {{ f.badge }}
              </span>
              <div class="text-right">
                <span class="text-xl font-extrabold text-slate-900">{{ f.price_per_meter }} TL</span>
                <span class="text-[10px] text-slate-400 block font-medium">/ Metre (KDV Dahil)</span>
              </div>
            </div>
            <h3 class="text-lg font-bold text-slate-900 group-hover:text-emerald-700 transition">
              {{ f.name }}
            </h3>
            <p class="text-xs text-slate-500 mt-1 font-medium">{{ f.composition }}</p>
          </div>'''

new_card_top = '''      <div class="bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-sm hover:shadow-md transition-all flex flex-col justify-between group">
        <div>
          <!-- Fabric Image Thumbnail -->
          {% if f.image %}
          <div class="h-44 w-full bg-slate-100 overflow-hidden relative border-b border-slate-100">
            <img src="{{ f.image }}" alt="{{ f.name }}" class="w-full h-full object-cover group-hover:scale-105 transition duration-500">
            <span class="absolute top-3 left-3 px-2.5 py-1 bg-slate-950/80 backdrop-blur-md text-white text-[10px] font-extrabold rounded-lg border border-white/10">
              {{ f.badge }}
            </span>
          </div>
          {% endif %}

          <!-- Fabric Header -->
          <div class="p-6 pb-4 border-b border-slate-100 bg-gradient-to-b from-slate-50 to-white">
            <div class="flex items-start justify-between gap-2 mb-2">
              <span class="px-2.5 py-1 bg-emerald-100 text-emerald-800 text-[11px] font-extrabold rounded-lg">
                {{ f.weight }} • {{ f.width }}
              </span>
              <div class="text-right">
                <span class="text-xl font-extrabold text-slate-900">{{ f.price_per_meter }} TL</span>
                <span class="text-[10px] text-slate-400 block font-medium">/ Metre (KDV Dahil)</span>
              </div>
            </div>
            <h3 class="text-lg font-bold text-slate-900 group-hover:text-emerald-700 transition">
              {{ f.name }}
            </h3>
            <p class="text-xs text-slate-500 mt-1 font-medium">{{ f.composition }}</p>
          </div>'''

if old_card_top in content:
    content = content.replace(old_card_top, new_card_top)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated templates/kumaslar.html successfully!")
else:
    print("Template target section not found, checking fallback...")
