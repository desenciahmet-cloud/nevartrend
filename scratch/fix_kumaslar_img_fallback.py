import os

file_path = r'C:\Users\user\Desktop\nevartrend_ev\templates\kumaslar.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Update subtitle to dynamic count
content = content.replace(
    'Metraj dijital ve emprime baskı için hazır 7 özel kumaş türü',
    'Metraj dijital ve emprime baskı için hazır {{ fabrics|length }} özel kumaş türü'
)

# Update img tag with onerror fallback
old_img = '<img src="{{ f.image }}" alt="{{ f.name }}" class="w-full h-full object-cover group-hover:scale-105 transition duration-500">'
new_img = '<img src="{{ f.image }}" alt="{{ f.name }}" onerror="this.onerror=null; this.src=\'/static/images/fabrics/queen-krep-112.jpg\';" class="w-full h-full object-cover group-hover:scale-105 transition duration-500">'

content = content.replace(old_img, new_img)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated templates/kumaslar.html with fallback and dynamic count")
