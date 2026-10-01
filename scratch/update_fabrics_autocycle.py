import re

with open('templates/fabrics.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace patternsDict definition with Jinja2 loop for all products
old_dict = """  const patternsDict = {
    'NT_021': { code: 'NT_021', title: 'NT_021 • Krem Zemin Pastel Bordo Çiçek Bahçesi', url: '/static/images/NT_021.jpg' },
    'NT_074': { code: 'NT_074', title: 'NT_074 • Gece Siyahı Botanik', url: '/static/images/NT_074.jpg' },
    'NT_042': { code: 'NT_042', title: 'NT_042 • Krem Barok Saray', url: '/static/images/NT_042.jpg' },
    'NT_036': { code: 'NT_036', title: 'NT_036 • Antrasit Gül Kurusu', url: '/static/images/NT_036.jpg' },
    'NT_011': { code: 'NT_011', title: 'NT_011 • Pastel Gri Vintage', url: '/static/images/NT_011.jpg' },
    'NT_015': { code: 'NT_015', title: 'NT_015 • Tropikal Gece Palmiye', url: '/static/images/NT_015.jpg' },
    'NT_001': { code: 'NT_001', title: 'NT_001 • Zümrüt Şakayık Çiçeği', url: '/static/images/NT_001.jpg' }
  };"""

new_dict = """  const patternsDict = {
    {% for p in products %}
    "{{ p.code }}": { code: "{{ p.code }}", title: "{{ p.code }} • {{ p.title|e }}", url: "{{ p.image }}" },
    {% endfor %}
  };
  const patternKeysList = Object.keys(patternsDict);
  let patternCycleStep = 0;"""

content = content.replace(old_dict, new_dict)

# Update advanceStepSmoothly to auto-cycle patterns
old_advance = """  function advanceStepSmoothly() {
    if (isTransitioning) return;
    isTransitioning = true;
    nextPoseIdx = (currentPoseIdx + 1) % catwalkPoses.length;
    
    let startTime = null;
    const duration = 700;"""

new_advance = """  function advanceStepSmoothly() {
    if (isTransitioning) return;
    isTransitioning = true;
    nextPoseIdx = (currentPoseIdx + 1) % catwalkPoses.length;
    
    // Automatic continuous pattern rotation on mannequin walk
    patternCycleStep++;
    if (patternCycleStep % 3 === 0 && patternKeysList.length > 0) {
      const currIdx = patternKeysList.indexOf(currentPattern.code);
      const nextIdx = (currIdx + 1) % patternKeysList.length;
      if (patternsDict[patternKeysList[nextIdx]]) {
        currentPattern = patternsDict[patternKeysList[nextIdx]];
      }
    }

    let startTime = null;
    const duration = 700;"""

content = content.replace(old_advance, new_advance)

with open('templates/fabrics.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated templates/fabrics.html with dynamic 74 patterns and automatic continuous pattern cycling!")
