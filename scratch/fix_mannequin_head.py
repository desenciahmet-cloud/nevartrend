import os

def fix_head(filepath):
    if not os.path.exists(filepath):
        print("Not found:", filepath)
        return
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Update .runway-stage and #catwalkCanvas CSS
    old_css = '''  .runway-stage {
    position: sticky;
    top: 96px;
    overflow: hidden;
    border-radius: 20px;
    background: #e5e3dd;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.06);
    aspect-ratio: 2 / 3;
    max-height: calc(100vh - 120px);
    width: 100%;
  }
  #catwalkCanvas {
    display: block;
    width: 100%;
    height: 100%;
    object-fit: cover;
  }'''

    new_css = '''  .runway-stage {
    position: sticky;
    top: 96px;
    overflow: hidden;
    border-radius: 20px;
    background: #e5e3dd;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.06);
    aspect-ratio: 2 / 3;
    max-height: calc(100vh - 120px);
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  #catwalkCanvas {
    display: block;
    width: 100%;
    height: 100%;
    object-fit: contain;
    object-position: center center;
  }'''

    if old_css in content:
        content = content.replace(old_css, new_css)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Updated CSS in", filepath)
    else:
        # Fallback replacement for #catwalkCanvas object-fit
        content = content.replace('object-fit: cover;', 'object-fit: contain;\n    object-position: center center;')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Fallback updated in", filepath)

fix_head('index.html')
fix_head('templates/index.html')
