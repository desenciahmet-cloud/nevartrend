import os

index_content = '''{% extends "base.html" %}
{% block title %}Nevartrend by Trenddesen | Beğendiğin desene dokun, model üzerine gör{% endblock %}

{% block content %}
<style>
  .showcase {
    padding: 16px 20px;
    background: #FAF9F6;
    min-height: calc(100vh - 80px);
  }
  .showcase-layout {
    max-width: 1600px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: minmax(0, 1.15fr) minmax(0, 1fr);
    gap: 24px;
    align-items: start;
  }
  .runway-stage {
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
  }
  .pattern-panel {
    min-width: 0;
    display: flex;
    flex-direction: column;
    gap: 16px;
  }
  .panel-title {
    font-size: clamp(20px, 2vw, 26px);
    font-weight: 800;
    color: #183c2c;
    text-align: center;
    letter-spacing: -0.02em;
    margin-bottom: 4px;
  }
  #patternGrid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 14px;
    max-height: calc(100vh - 180px);
    overflow-y: auto;
    padding-right: 6px;
    scrollbar-width: thin;
    scrollbar-color: #cbd5e1 transparent;
  }
  .pattern-card {
    display: block;
    width: 100%;
    text-align: left;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    background: white;
    overflow: hidden;
    cursor: pointer;
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03);
  }
  .pattern-card:hover {
    border-color: #183c2c;
    transform: translateY(-2px);
    box-shadow: 0 8px 18px rgba(24, 60, 44, 0.12);
  }
  .pattern-card[aria-pressed="true"] {
    border-color: #183c2c;
    box-shadow: 0 0 0 2px #183c2c;
  }
  .pattern-swatch {
    position: relative;
    aspect-ratio: 1;
    overflow: hidden;
    background: #f1f5f9;
  }
  .pattern-swatch img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.3s ease;
  }
  .pattern-card:hover img {
    transform: scale(1.06);
  }
  .pattern-code {
    position: absolute;
    bottom: 6px;
    left: 6px;
    padding: 2px 6px;
    border-radius: 5px;
    background: rgba(255, 255, 255, 0.92);
    backdrop-filter: blur(4px);
    color: #183c2c;
    font-size: 9px;
    font-weight: 800;
    font-family: monospace;
    border: 1px solid rgba(24, 60, 44, 0.1);
  }
  .pattern-info {
    padding: 8px 10px;
  }
  .pattern-title {
    display: block;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    font-size: 11px;
    font-weight: 700;
    color: #1e293b;
  }
  .pattern-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 4px;
    font-size: 10px;
    color: #64748b;
    font-weight: 500;
  }
  .pattern-rating {
    color: #d97706;
    font-weight: 700;
  }
  @media (max-width: 1023px) {
    .showcase-layout {
      grid-template-columns: 1fr;
      gap: 20px;
    }
    .runway-stage {
      position: relative;
      top: 0;
      max-height: 520px;
    }
    #patternGrid {
      max-height: none;
    }
  }
  @media (max-width: 639px) {
    #patternGrid {
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 10px;
    }
  }
</style>

<section class="showcase">
  <div class="showcase-layout">
    
    <!-- LEFT COLUMN: CATWALK MODEL STAGE -->
    <div class="runway-stage">
      <canvas id="catwalkCanvas" width="1024" height="1536" role="img" aria-label="Canlı model üzerinde desen denemesi"></canvas>
    </div>

    <!-- RIGHT COLUMN: PATTERN SELECTION GRID -->
    <div class="pattern-panel">
      <h2 class="panel-title font-serif-title">
        Beğendiğin desene dokun, model üzerine gör.
      </h2>

      <div id="patternGrid">
        {% for p in products %}
        <button type="button" class="pattern-card" data-category="{{ p.category }}" data-code="{{ p.code }}" aria-pressed="false" onclick='selectCatwalkPatternByCode({{ p.code|tojson }}, {{ p.title|tojson }}, {{ p.image|tojson }})'>
          <div class="pattern-swatch">
            <img src="/static/images/thumbs/{{ p.code }}.webp" data-fallback="{{ p.image }}" onerror="this.onerror=null; this.src=this.dataset.fallback;" loading="lazy" decoding="async" width="300" height="300" alt="{{ p.title }}">
            <span class="pattern-code">{{ p.code }}</span>
          </div>
          <div class="pattern-info">
            <span class="pattern-title">{{ p.title }}</span>
            <div class="pattern-meta">
              <span>{{ p.base_price }} TL/mt</span>
              <span class="pattern-rating">★ {{ p.rating }}</span>
            </div>
          </div>
        </button>
        {% endfor %}
      </div>
    </div>

  </div>
</section>

<!-- SCRIPT: SMOOTH CONTINUOUS RUNWAY CATWALK WALKING MANNEQUIN ENGINE -->
<script>
(function() {
  const CANVAS_W = 1024;
  const CANVAS_H = 1536;

  const canvas = document.getElementById('catwalkCanvas');
  const ctx = canvas ? canvas.getContext('2d') : null;

  const posesData = [
    { bgSrc: '/static/images/catwalk/catwalk_1_bg.jpg?v=6.0', maskSrc: '/static/images/catwalk/catwalk_1_mask.png?v=6.0', shadeSrc: '/static/images/catwalk/catwalk_1_shade.png?v=6.0', bg: null, mask: null, shade: null },
    { bgSrc: '/static/images/catwalk/catwalk_2_bg.jpg?v=6.0', maskSrc: '/static/images/catwalk/catwalk_2_mask.png?v=6.0', shadeSrc: '/static/images/catwalk/catwalk_2_shade.png?v=6.0', bg: null, mask: null, shade: null },
    { bgSrc: '/static/images/catwalk/catwalk_3_bg.jpg?v=6.0', maskSrc: '/static/images/catwalk/catwalk_3_mask.png?v=6.0', shadeSrc: '/static/images/catwalk/catwalk_3_shade.png?v=6.0', bg: null, mask: null, shade: null },
    { bgSrc: '/static/images/catwalk/catwalk_4_bg.jpg?v=6.0', maskSrc: '/static/images/catwalk/catwalk_4_mask.png?v=6.0', shadeSrc: '/static/images/catwalk/catwalk_4_shade.png?v=6.0', bg: null, mask: null, shade: null },
    { bgSrc: '/static/images/catwalk/catwalk_5_bg.jpg?v=6.0', maskSrc: '/static/images/catwalk/catwalk_5_mask.png?v=6.0', shadeSrc: '/static/images/catwalk/catwalk_5_shade.png?v=6.0', bg: null, mask: null, shade: null },
    { bgSrc: '/static/images/catwalk/catwalk_6_bg.jpg?v=6.0', maskSrc: '/static/images/catwalk/catwalk_6_mask.png?v=6.0', shadeSrc: '/static/images/catwalk/catwalk_6_shade.png?v=6.0', bg: null, mask: null, shade: null }
  ];

  const patternsDict = {
    {% for p in products %}
    "{{ p.code }}": { code: "{{ p.code }}", title: "{{ p.code }} • {{ p.title|e }}", url: "{{ p.image }}", category: "{{ p.category }}" },
    {% endfor %}
  };
  const patternKeysList = Object.keys(patternsDict);

  let currentPattern = patternsDict['NT_074'] || patternsDict['NT_021'] || (patternKeysList.length > 0 ? patternsDict[patternKeysList[0]] : { code: 'NT_074', title: 'NT_074', url: '/static/images/NT_074.jpg' });
  let currentScaleMode = 'normal';
  let currentLengthMode = 'normal';
  let isPlaying = true;
  let isAssetsLoaded = false;
  let currentFrameIndex = 0;
  let lastFrameTime = performance.now();
  let lastPatternSwitchTime = performance.now();
  const FRAME_DURATION = 320;
  const PATTERN_CHANGE_INTERVAL = 7000;

  const compositedCanvases = [
    document.createElement('canvas'),
    document.createElement('canvas'),
    document.createElement('canvas'),
    document.createElement('canvas'),
    document.createElement('canvas'),
    document.createElement('canvas')
  ];

  compositedCanvases.forEach(c => {
    c.width = CANVAS_W;
    c.height = CANVAS_H;
  });

  function loadImageAsync(src) {
    return new Promise(resolve => {
      const img = new Image();
      img.onload = () => resolve(img);
      img.onerror = () => {
        console.warn('Failed to load asset:', src);
        resolve(null);
      };
      img.src = src;
    });
  }

  const loadPromises = [];
  posesData.forEach(p => {
    loadPromises.push(loadImageAsync(p.bgSrc).then(img => p.bg = img));
    loadPromises.push(loadImageAsync(p.maskSrc).then(img => p.mask = img));
    loadPromises.push(loadImageAsync(p.shadeSrc).then(img => p.shade = img));
  });

  Promise.all(loadPromises).then(() => {
    isAssetsLoaded = true;
    renderAllPosesWithCurrentPattern();
  });

  let patternImgObj = null;

  function renderAllPosesWithCurrentPattern() {
    if (!isAssetsLoaded) return;

    if (!patternImgObj || patternImgObj.src !== currentPattern.url) {
      patternImgObj = new Image();
      patternImgObj.onload = () => renderAllPosesWithCurrentPattern();
      patternImgObj.src = currentPattern.url;
      if (!patternImgObj.complete) return;
    }

    let tileW = 380;
    let tileH = tileW;

    const tileCanvas = document.createElement('canvas');
    tileCanvas.width = tileW;
    tileCanvas.height = tileH;
    const tctx = tileCanvas.getContext('2d');
    tctx.drawImage(patternImgObj, 0, 0, tileW, tileH);

    for (let i = 0; i < 6; i++) {
      const p = posesData[i];
      const targetCanvas = compositedCanvases[i];
      const tCtx = targetCanvas.getContext('2d');

      tCtx.clearRect(0, 0, CANVAS_W, CANVAS_H);

      if (p.bg) {
        tCtx.drawImage(p.bg, 0, 0, CANVAS_W, CANVAS_H);
      }

      if (p.mask) {
        const patCanvas = document.createElement('canvas');
        patCanvas.width = CANVAS_W;
        patCanvas.height = CANVAS_H;
        const pCtx = patCanvas.getContext('2d');

        const ptrn = pCtx.createPattern(tileCanvas, 'repeat');
        pCtx.fillStyle = ptrn;
        pCtx.fillRect(0, 0, CANVAS_W, CANVAS_H);

        pCtx.globalCompositeOperation = 'destination-in';
        pCtx.drawImage(p.mask, 0, 0, CANVAS_W, CANVAS_H);

        if (p.shade) {
          pCtx.globalCompositeOperation = 'multiply';
          pCtx.globalAlpha = 0.18;
          pCtx.drawImage(p.shade, 0, 0, CANVAS_W, CANVAS_H);
          pCtx.globalAlpha = 1.0;

          pCtx.globalCompositeOperation = 'destination-in';
          pCtx.drawImage(p.mask, 0, 0, CANVAS_W, CANVAS_H);
        }

        tCtx.globalCompositeOperation = 'source-over';
        tCtx.drawImage(patCanvas, 0, 0, CANVAS_W, CANVAS_H);
      }
    }

    drawActiveFrame();
  }

  function drawActiveFrame() {
    if (ctx && isAssetsLoaded && compositedCanvases[currentFrameIndex]) {
      ctx.clearRect(0, 0, CANVAS_W, CANVAS_H);
      ctx.drawImage(compositedCanvases[currentFrameIndex], 0, 0, CANVAS_W, CANVAS_H);
    }
  }

  let isCanvasInView = true;
  let rafId = null;

  if ('IntersectionObserver' in window && canvas) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        isCanvasInView = entry.isIntersecting;
        if (isCanvasInView && !rafId) {
          lastFrameTime = performance.now();
          rafId = requestAnimationFrame(animationLoop);
        }
      });
    }, { threshold: 0.05 });
    observer.observe(canvas);
  }

  function animationLoop(now) {
    if (!isCanvasInView) {
      rafId = null;
      return;
    }

    if (isPlaying && isAssetsLoaded) {
      if (now - lastFrameTime >= FRAME_DURATION) {
        currentFrameIndex = (currentFrameIndex + 1) % 6;
        lastFrameTime = now;
        drawActiveFrame();
      }

      if (now - lastPatternSwitchTime >= PATTERN_CHANGE_INTERVAL) {
        const currIdx = patternKeysList.indexOf(currentPattern.code);
        const nextIdx = (currIdx + 1) % patternKeysList.length;
        if (patternsDict[patternKeysList[nextIdx]]) {
          currentPattern = patternsDict[patternKeysList[nextIdx]];
          updatePatternSelection();
          renderAllPosesWithCurrentPattern();
        }
        lastPatternSwitchTime = now;
      }
    }

    rafId = requestAnimationFrame(animationLoop);
  }

  rafId = requestAnimationFrame(animationLoop);

  window.selectCatwalkPatternByCode = function(code, title, url) {
    if (!patternsDict[code]) {
      patternsDict[code] = {
        code: code,
        title: title || `${code} • Özel Desen`,
        url: url || `/static/images/${code}.jpg`
      };
    }
    currentPattern = patternsDict[code];
    updatePatternSelection();
    lastPatternSwitchTime = performance.now();
    renderAllPosesWithCurrentPattern();

    const stage = document.getElementById('catwalkCanvas');
    if (stage && window.matchMedia('(max-width: 767px)').matches) {
      stage.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  };

  function updatePatternSelection() {
    document.querySelectorAll('#patternGrid .pattern-card').forEach(card => {
      card.setAttribute('aria-pressed', String(card.dataset.code === currentPattern.code));
    });
  }
  updatePatternSelection();

})();
</script>
{% endblock %}
'''

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(index_content)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(index_content)

print("Updated index.html and templates/index.html successfully!")
