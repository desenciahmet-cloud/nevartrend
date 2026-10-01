import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace staticPose script with smooth 4-pose walking animation engine script + fitting controls
old_script = """<!-- SCRIPT: CLEAN STATIC MODEL CANVAS ENGINE WITH DYNAMIC PATTERN & FITTING CONTROLS -->
<script>
(function() {
  // Ultra-clean studio standing model pose (No crowd in background)
  const staticPose = {
    bg: '/static/images/catwalk/clean_catwalk_1_bg.jpg',
    mask: '/static/images/catwalk/catwalk_1_mask.png',
    shade: '/static/images/catwalk/catwalk_1_shade.png'
  };

  const patternsDict = {
    {% for p in products %}
    "{{ p.code }}": { code: "{{ p.code }}", title: "{{ p.code }} • {{ p.title|e }}", url: "{{ p.image }}", category: "{{ p.category }}" },
    {% endfor %}
  };
  const patternKeysList = Object.keys(patternsDict);

  let currentPattern = patternsDict['NT_021'] || (patternKeysList.length > 0 ? patternsDict[patternKeysList[0]] : { code: 'NT_021', title: 'NT_021', url: '/static/images/NT_021.jpg' });
  let currentScaleMode = 'normal'; // 'narrow', 'normal', 'wide'
  let currentLengthMode = 'normal'; // 'short', 'normal', 'long'

  const canvas = document.getElementById('catwalkCanvas');
  const ctx = canvas ? canvas.getContext('2d') : null;
  const imageCache = {};

  function loadImage(src) {
    if (!src) return Promise.resolve(null);
    if (imageCache[src]) return Promise.resolve(imageCache[src]);
    return new Promise((resolve) => {
      const img = new Image();
      img.crossOrigin = 'anonymous';
      img.onload = () => { imageCache[src] = img; resolve(img); };
      img.onerror = () => resolve(null);
      img.src = src;
    });
  }

  function renderStaticModelFrame() {
    if (!ctx) return;

    // UI Label Updates
    const pTitle = document.getElementById('catwalkPatternTitle');
    const avatar = document.getElementById('catwalkAvatarThumb');
    const goBtn = document.getElementById('catwalkGoStudioBtnTop');

    if (pTitle) pTitle.textContent = currentPattern.title;
    if (avatar) avatar.src = currentPattern.url;
    if (goBtn) goBtn.href = `/studyo?pattern=${currentPattern.code}`;

    Promise.all([
      loadImage(staticPose.bg),
      loadImage(staticPose.mask),
      loadImage(staticPose.shade),
      loadImage(currentPattern.url)
    ]).then(([bgImg, maskImg, shadeImg, patImg]) => {
      ctx.clearRect(0, 0, 699, 1536);

      // 1. Draw Clean Backdrop & Standing Model Base
      if (bgImg) ctx.drawImage(bgImg, 0, 0, 699, 1536);

      // 2. Tile Pattern & Mask onto Dress
      if (patImg && maskImg) {
        const patCanvas = document.createElement('canvas');
        patCanvas.width = 699;
        patCanvas.height = 1536;
        const pCtx = patCanvas.getContext('2d');

        // Fitting Scale Calculation (Daralt / Normal / Genişlet)
        let tileW = 450;
        if (currentScaleMode === 'narrow') tileW = 280;
        else if (currentScaleMode === 'wide') tileW = 680;

        // Fitting Length Calculation (Kısalt / Normal / Uzat)
        let tileH = tileW;
        if (currentLengthMode === 'short') tileH = Math.round(tileW * 0.7);
        else if (currentLengthMode === 'long') tileH = Math.round(tileW * 1.35);

        const tileCanvas = document.createElement('canvas');
        tileCanvas.width = tileW;
        tileCanvas.height = tileH;
        const tctx = tileCanvas.getContext('2d');
        tctx.drawImage(patImg, 0, 0, tileW, tileH);

        const ptrn = pCtx.createPattern(tileCanvas, 'repeat');
        pCtx.fillStyle = ptrn;
        pCtx.fillRect(0, 0, 699, 1536);

        pCtx.globalCompositeOperation = 'destination-in';
        pCtx.drawImage(maskImg, 0, 0, 699, 1536);
        pCtx.globalCompositeOperation = 'source-over';

        ctx.globalCompositeOperation = 'multiply';
        ctx.drawImage(patCanvas, 0, 0, 699, 1536);
        ctx.globalCompositeOperation = 'source-over';
      }

      // 3. Draw Lighting Shade
      if (shadeImg) {
        ctx.globalCompositeOperation = 'multiply';
        ctx.drawImage(shadeImg, 0, 0, 699, 1536);
        ctx.globalCompositeOperation = 'source-over';
      }
    });
  }

  // Scale Mode Trigger (Daralt / Normal / Genişlet)
  window.setCatwalkScaleMode = function(mode) {
    currentScaleMode = mode;
    ['Narrow', 'Normal', 'Wide'].forEach(m => {
      const btn = document.getElementById('scaleBtn' + m);
      if (btn) {
        if (m.toLowerCase() === mode) {
          btn.className = 'px-2 py-1 bg-emerald-800 text-white font-bold rounded-lg text-[10px] transition shadow-xs';
        } else {
          btn.className = 'px-2 py-1 bg-white hover:bg-emerald-50 text-slate-700 font-bold rounded-lg border border-slate-200 text-[10px] transition';
        }
      }
    });
    renderStaticModelFrame();
  };

  // Length Mode Trigger (Kısalt / Normal / Uzat)
  window.setCatwalkLengthMode = function(mode) {
    currentLengthMode = mode;
    ['Short', 'Normal', 'Long'].forEach(m => {
      const btn = document.getElementById('lenBtn' + m);
      if (btn) {
        if (m.toLowerCase() === mode) {
          btn.className = 'px-2 py-1 bg-emerald-800 text-white font-bold rounded-lg text-[10px] transition shadow-xs';
        } else {
          btn.className = 'px-2 py-1 bg-white hover:bg-emerald-50 text-slate-700 font-bold rounded-lg border border-slate-200 text-[10px] transition';
        }
      }
    });
    renderStaticModelFrame();
  };

  // Pattern Selection Trigger
  window.selectCatwalkPatternByCode = function(code, title, url) {
    if (!patternsDict[code]) {
      patternsDict[code] = {
        code: code,
        title: title || `${code} • Özel Desen`,
        url: url || `/static/images/${code}.jpg`
      };
    }
    currentPattern = patternsDict[code];
    renderStaticModelFrame();

    const stage = document.getElementById('catwalkCanvas');
    if (stage) {
      stage.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  };

  // Left Sidebar Category Click -> Filter patterns & Update model with category pattern
  window.selectCategoryLeft = function(cat) {
    filterPatterns(cat);
    const catPats = patternKeysList.filter(k => patternsDict[k] && patternsDict[k].category === cat);
    if (catPats.length > 0) {
      const p = patternsDict[catPats[0]];
      selectCatwalkPatternByCode(p.code, p.title, p.url);
    }
  };

  window.filterPatterns = function(cat) {
    document.querySelectorAll('.cat-filter-btn').forEach(b => {
      b.className = 'cat-filter-btn px-4 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 transition font-bold';
    });
    const activeBtn = document.getElementById(`tab-${cat}`);
    if (activeBtn) {
      activeBtn.className = 'cat-filter-btn px-4 py-2 rounded-xl bg-slate-900 text-white shadow-xs transition font-bold';
    }

    document.querySelectorAll('.pattern-card').forEach(card => {
      if (cat === 'all' || card.getAttribute('data-category') === cat) {
        card.style.display = 'block';
      } else {
        card.style.display = 'none';
      }
    });
  };

  // Smooth automatic pattern switching every 3.5 seconds on static mannequin
  let patternCycleIdx = 0;
  setInterval(() => {
    if (patternKeysList.length > 0) {
      patternCycleIdx = (patternCycleIdx + 1) % patternKeysList.length;
      const nextCode = patternKeysList[patternCycleIdx];
      if (patternsDict[nextCode]) {
        currentPattern = patternsDict[nextCode];
        renderStaticModelFrame();
      }
    }
  }, 3500);

  // Preload images
  loadImage(staticPose.bg);
  loadImage(staticPose.mask);
  loadImage(staticPose.shade);

  document.addEventListener('DOMContentLoaded', () => {
    renderStaticModelFrame();
  });

  if (document.readyState === 'complete' || document.readyState === 'interactive') {
    setTimeout(() => {
      renderStaticModelFrame();
    }, 150);
  }
})();
</script>"""

new_script = """<!-- SCRIPT: SMOOTH CONTINUOUS RUNWAY CATWALK WALKING MANNEQUIN ENGINE -->
<script>
(function() {
  const catwalkPoses = [
    { bg: '/static/images/catwalk/clean_catwalk_1_bg.jpg', mask: '/static/images/catwalk/catwalk_1_mask.png', shade: '/static/images/catwalk/catwalk_1_shade.png' },
    { bg: '/static/images/catwalk/clean_catwalk_2_bg.jpg', mask: '/static/images/catwalk/catwalk_2_mask.png', shade: '/static/images/catwalk/catwalk_2_shade.png' },
    { bg: '/static/images/catwalk/clean_catwalk_3_bg.jpg', mask: '/static/images/catwalk/catwalk_3_mask.png', shade: '/static/images/catwalk/catwalk_3_shade.png' },
    { bg: '/static/images/catwalk/clean_catwalk_4_bg.jpg', mask: '/static/images/catwalk/catwalk_4_mask.png', shade: '/static/images/catwalk/catwalk_4_shade.png' }
  ];

  const patternsDict = {
    {% for p in products %}
    "{{ p.code }}": { code: "{{ p.code }}", title: "{{ p.code }} • {{ p.title|e }}", url: "{{ p.image }}", category: "{{ p.category }}" },
    {% endfor %}
  };
  const patternKeysList = Object.keys(patternsDict);

  let currentPoseIdx = 0;
  let nextPoseIdx = 1;
  let transitionProgress = 1.0;
  let isTransitioning = false;
  let currentPattern = patternsDict['NT_021'] || (patternKeysList.length > 0 ? patternsDict[patternKeysList[0]] : { code: 'NT_021', title: 'NT_021', url: '/static/images/NT_021.jpg' });
  let currentScaleMode = 'normal'; // 'narrow', 'normal', 'wide'
  let currentLengthMode = 'normal'; // 'short', 'normal', 'long'
  let isPlaying = true;
  let timerId = null;
  let animFrameId = null;
  let stepCounter = 0;

  const canvas = document.getElementById('catwalkCanvas');
  const ctx = canvas ? canvas.getContext('2d') : null;
  const imageCache = {};

  function loadImage(src) {
    if (!src) return Promise.resolve(null);
    if (imageCache[src]) return Promise.resolve(imageCache[src]);
    return new Promise((resolve) => {
      const img = new Image();
      img.crossOrigin = 'anonymous';
      img.onload = () => { imageCache[src] = img; resolve(img); };
      img.onerror = () => resolve(null);
      img.src = src;
    });
  }

  function createPoseCanvas(poseIdx, patternObj) {
    const pose = catwalkPoses[poseIdx];
    const offCanvas = document.createElement('canvas');
    offCanvas.width = 699;
    offCanvas.height = 1536;
    const offCtx = offCanvas.getContext('2d');

    return Promise.all([
      loadImage(pose.bg),
      loadImage(pose.mask),
      loadImage(pose.shade),
      loadImage(patternObj.url)
    ]).then(([bgImg, maskImg, shadeImg, patImg]) => {
      offCtx.clearRect(0, 0, 699, 1536);

      if (bgImg) offCtx.drawImage(bgImg, 0, 0, 699, 1536);

      if (patImg && maskImg) {
        const patCanvas = document.createElement('canvas');
        patCanvas.width = 699;
        patCanvas.height = 1536;
        const pCtx = patCanvas.getContext('2d');

        let tileW = 450;
        if (currentScaleMode === 'narrow') tileW = 280;
        else if (currentScaleMode === 'wide') tileW = 680;

        let tileH = tileW;
        if (currentLengthMode === 'short') tileH = Math.round(tileW * 0.7);
        else if (currentLengthMode === 'long') tileH = Math.round(tileW * 1.35);

        const tileCanvas = document.createElement('canvas');
        tileCanvas.width = tileW;
        tileCanvas.height = tileH;
        const tctx = tileCanvas.getContext('2d');
        tctx.drawImage(patImg, 0, 0, tileW, tileH);

        const ptrn = pCtx.createPattern(tileCanvas, 'repeat');
        pCtx.fillStyle = ptrn;
        pCtx.fillRect(0, 0, 699, 1536);

        pCtx.globalCompositeOperation = 'destination-in';
        pCtx.drawImage(maskImg, 0, 0, 699, 1536);
        pCtx.globalCompositeOperation = 'source-over';

        offCtx.globalCompositeOperation = 'multiply';
        offCtx.drawImage(patCanvas, 0, 0, 699, 1536);
        offCtx.globalCompositeOperation = 'source-over';
      }

      if (shadeImg) {
        offCtx.globalCompositeOperation = 'multiply';
        offCtx.drawImage(shadeImg, 0, 0, 699, 1536);
        offCtx.globalCompositeOperation = 'source-over';
      }

      return offCanvas;
    });
  }

  function renderFrame() {
    if (!ctx) return;

    const pTitle = document.getElementById('catwalkPatternTitle');
    const avatar = document.getElementById('catwalkAvatarThumb');
    const goBtn = document.getElementById('catwalkGoStudioBtnTop');

    if (pTitle) pTitle.textContent = currentPattern.title;
    if (avatar) avatar.src = currentPattern.url;
    if (goBtn) goBtn.href = `/studyo?pattern=${currentPattern.code}`;

    if (transitionProgress >= 1.0) {
      createPoseCanvas(currentPoseIdx, currentPattern).then(c => {
        ctx.clearRect(0, 0, 699, 1536);
        ctx.drawImage(c, 0, 0, 699, 1536);
      });
    } else {
      Promise.all([
        createPoseCanvas(currentPoseIdx, currentPattern),
        createPoseCanvas(nextPoseIdx, currentPattern)
      ]).then(([currC, nextC]) => {
        ctx.clearRect(0, 0, 699, 1536);
        ctx.globalAlpha = 1.0;
        ctx.drawImage(currC, 0, 0, 699, 1536);

        ctx.globalAlpha = transitionProgress;
        ctx.drawImage(nextC, 0, 0, 699, 1536);
        ctx.globalAlpha = 1.0;
      });
    }
  }

  function advanceStepSmoothly() {
    if (isTransitioning) return;
    isTransitioning = true;
    nextPoseIdx = (currentPoseIdx + 1) % catwalkPoses.length;

    // Pattern auto-cycling on mannequin walk every 3 strides
    stepCounter++;
    if (stepCounter % 3 === 0 && patternKeysList.length > 0) {
      const currIdx = patternKeysList.indexOf(currentPattern.code);
      const nextIdx = (currIdx + 1) % patternKeysList.length;
      if (patternsDict[patternKeysList[nextIdx]]) {
        currentPattern = patternsDict[patternKeysList[nextIdx]];
      }
    }
    
    let startTime = null;
    const duration = 650;

    function animateCrossfade(timestamp) {
      if (!startTime) startTime = timestamp;
      const elapsed = timestamp - startTime;
      transitionProgress = Math.min(elapsed / duration, 1.0);

      renderFrame();

      if (transitionProgress < 1.0) {
        animFrameId = requestAnimationFrame(animateCrossfade);
      } else {
        currentPoseIdx = nextPoseIdx;
        isTransitioning = false;
      }
    }

    animFrameId = requestAnimationFrame(animateCrossfade);
  }

  window.setCatwalkScaleMode = function(mode) {
    currentScaleMode = mode;
    ['Narrow', 'Normal', 'Wide'].forEach(m => {
      const btn = document.getElementById('scaleBtn' + m);
      if (btn) {
        if (m.toLowerCase() === mode) {
          btn.className = 'px-2 py-1 bg-emerald-800 text-white font-bold rounded-lg text-[10px] transition shadow-xs';
        } else {
          btn.className = 'px-2 py-1 bg-white hover:bg-emerald-50 text-slate-700 font-bold rounded-lg border border-slate-200 text-[10px] transition';
        }
      }
    });
    renderFrame();
  };

  window.setCatwalkLengthMode = function(mode) {
    currentLengthMode = mode;
    ['Short', 'Normal', 'Long'].forEach(m => {
      const btn = document.getElementById('lenBtn' + m);
      if (btn) {
        if (m.toLowerCase() === mode) {
          btn.className = 'px-2 py-1 bg-emerald-800 text-white font-bold rounded-lg text-[10px] transition shadow-xs';
        } else {
          btn.className = 'px-2 py-1 bg-white hover:bg-emerald-50 text-slate-700 font-bold rounded-lg border border-slate-200 text-[10px] transition';
        }
      }
    });
    renderFrame();
  };

  window.selectCatwalkPatternByCode = function(code, title, url) {
    if (!patternsDict[code]) {
      patternsDict[code] = {
        code: code,
        title: title || `${code} • Özel Desen`,
        url: url || `/static/images/${code}.jpg`
      };
    }
    currentPattern = patternsDict[code];
    transitionProgress = 1.0;
    renderFrame();

    const stage = document.getElementById('catwalkCanvas');
    if (stage) {
      stage.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  };

  window.selectCategoryLeft = function(cat) {
    filterPatterns(cat);
    const catPats = patternKeysList.filter(k => patternsDict[k] && patternsDict[k].category === cat);
    if (catPats.length > 0) {
      const p = patternsDict[catPats[0]];
      selectCatwalkPatternByCode(p.code, p.title, p.url);
    }
  };

  window.filterPatterns = function(cat) {
    document.querySelectorAll('.cat-filter-btn').forEach(b => {
      b.className = 'cat-filter-btn px-4 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 transition font-bold';
    });
    const activeBtn = document.getElementById(`tab-${cat}`);
    if (activeBtn) {
      activeBtn.className = 'cat-filter-btn px-4 py-2 rounded-xl bg-slate-900 text-white shadow-xs transition font-bold';
    }

    document.querySelectorAll('.pattern-card').forEach(card => {
      if (cat === 'all' || card.getAttribute('data-category') === cat) {
        card.style.display = 'block';
      } else {
        card.style.display = 'none';
      }
    });
  };

  function startCycle() {
    stopCycle();
    timerId = setInterval(() => {
      advanceStepSmoothly();
    }, 1100);
  }

  function stopCycle() {
    if (timerId) clearInterval(timerId);
    if (animFrameId) cancelAnimationFrame(animFrameId);
    timerId = null;
  }

  catwalkPoses.forEach(pose => {
    loadImage(pose.bg);
    loadImage(pose.mask);
    loadImage(pose.shade);
  });

  document.addEventListener('DOMContentLoaded', () => {
    renderFrame();
    startCycle();
  });

  if (document.readyState === 'complete' || document.readyState === 'interactive') {
    setTimeout(() => {
      renderFrame();
      startCycle();
    }, 150);
  }
})();
</script>"""

content = content.replace(old_script, new_script)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Restored smooth runway catwalk walking animation on mannequin!")
