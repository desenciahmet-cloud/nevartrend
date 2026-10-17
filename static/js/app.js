// nevartrend Client State & Cart Engine

const CartEngine = {
  getCart: function() {
    try {
      const cart = localStorage.getItem('nevartrend_cart');
      if (!cart) return [];
      let parsed = JSON.parse(cart);
      if (!Array.isArray(parsed)) return [];
      
      // Clean and sanitize any corrupt/legacy items
      const cleaned = [];
      for (let i = 0; i < parsed.length; i++) {
        const item = parsed[i];
        if (!item) continue;
        const pId = String(item.product_id || item.id || ('PROD-' + (Date.now() + i)));
        const pTitle = String(item.product_title || item.title || 'Nevartrend Ürünü');
        const pCode = String(item.product_code || item.code || pId);
        const fId = String(item.fabric_id || item.fabric || item.type || 'hazir-urun');
        const fName = String(item.fabric_name || item.details || item.category || 'Hazır Giyim & Ev Tekstili');
        const uPrice = Number(item.unit_price != null ? item.unit_price : item.price) || 0;
        const qty = Number(item.meters != null ? item.meters : (item.quantity != null ? item.quantity : 1)) || 1;
        const img = item.image || '/static/img/hero-kimono.jpg';
        const tPrice = (Number(item.total_price) && !isNaN(item.total_price)) ? Number(item.total_price) : Math.round(qty * uPrice);
        
        cleaned.push({
          id: item.id || ('ITEM-' + (Date.now() + i)),
          product_id: pId,
          product_title: pTitle,
          product_code: pCode,
          fabric_id: fId,
          fabric_name: fName,
          unit_price: uPrice,
          meters: qty,
          total_price: tPrice,
          image: img
        });
      }
      return cleaned;
    } catch (e) {
      return [];
    }
  },

  saveCart: function(cart) {
    try {
      localStorage.setItem('nevartrend_cart', JSON.stringify(cart));
    } catch (e) {
      console.warn('Cart save error:', e);
    }
    this.updateUI();
  },

  addItem: function(item) {
    if (!item) return;
    const cart = this.getCart();

    // Normalize incoming item parameters
    const pId = String(item.product_id || item.id || ('PROD-' + Date.now()));
    const pTitle = String(item.product_title || item.title || 'Nevartrend Ürünü');
    const pCode = String(item.product_code || item.code || pId);
    const fId = String(item.fabric_id || item.fabric || item.type || 'hazir-urun');
    const fName = String(item.fabric_name || item.details || item.category || 'Hazır Giyim & Ev Tekstili');
    const uPrice = Number(item.unit_price != null ? item.unit_price : item.price) || 0;
    const qty = Number(item.meters != null ? item.meters : (item.quantity != null ? item.quantity : 1)) || 1;
    const img = item.image || '/static/img/hero-kimono.jpg';

    const isPiece = fId === 'hazir-urun' || fId === 'trend-product' || fId === 'emprime-service' || fId === 'emprime-catalog' || pId.startsWith('prod_') || pId.startsWith('EMP-');

    const existingIndex = cart.findIndex(function(i) {
      return String(i.product_id) === pId && String(i.fabric_id) === fId;
    });

    if (existingIndex > -1) {
      const newQty = cart[existingIndex].meters + qty;
      cart[existingIndex].meters = isPiece ? Math.round(newQty) : parseFloat(newQty.toFixed(1));
      cart[existingIndex].total_price = Math.round(cart[existingIndex].meters * cart[existingIndex].unit_price);
    } else {
      cart.push({
        id: 'ITEM-' + Date.now(),
        product_id: pId,
        product_title: pTitle,
        product_code: pCode,
        fabric_id: fId,
        fabric_name: fName,
        unit_price: uPrice,
        meters: isPiece ? Math.round(qty) : parseFloat(qty.toFixed(1)),
        total_price: Math.round(qty * uPrice),
        image: img
      });
    }

    this.saveCart(cart);
    this.openDrawer();
    this.showToast('Ürün sepetinize eklendi!', 'success');
  },

  removeItem: function(index) {
    const cart = this.getCart();
    if (index >= 0 && index < cart.length) {
      cart.splice(index, 1);
      this.saveCart(cart);
      this.showToast('Ürün sepetten çıkarıldı.', 'info');
    }
  },

  updateMeters: function(index, meters) {
    const cart = this.getCart();
    if (cart[index]) {
      const isPiece = cart[index].fabric_id === 'hazir-urun' || cart[index].fabric_id === 'trend-product' || cart[index].fabric_id === 'emprime-service' || cart[index].fabric_id === 'emprime-catalog' || String(cart[index].product_id).startsWith('prod_') || String(cart[index].product_id).startsWith('EMP-');
      const minVal = isPiece ? 1 : 0.5;
      let m = parseFloat(meters);
      if (isNaN(m) || m < minVal) {
        this.removeItem(index);
        return;
      }
      cart[index].meters = isPiece ? Math.round(m) : parseFloat(m.toFixed(1));
      cart[index].total_price = Math.round(cart[index].meters * cart[index].unit_price);
      this.saveCart(cart);
    }
  },

  clearCart: function() {
    localStorage.removeItem('nevartrend_cart');
    this.updateUI();
  },

  getSubtotal: function() {
    const cart = this.getCart();
    return cart.reduce(function(sum, item) { 
      const price = Number(item.total_price);
      return sum + (isNaN(price) ? 0 : price); 
    }, 0);
  },

  getDiscount: function() {
    const coupon = this.getCoupon();
    if (!coupon) return 0;
    const subtotal = this.getSubtotal();
    if (coupon.discount_pct) {
      return Math.round(subtotal * (coupon.discount_pct / 100));
    }
    return 0;
  },

  getShippingFee: function() {
    const subtotal = this.getSubtotal();
    const coupon = this.getCoupon();
    if (coupon && coupon.free_shipping) return 0;
    if (subtotal >= 1000 || subtotal === 0) return 0;
    return 79.90;
  },

  getTotal: function() {
    return Math.max(0, this.getSubtotal() - this.getDiscount() + this.getShippingFee());
  },

  getCoupon: function() {
    try {
      const c = localStorage.getItem('nevartrend_coupon');
      return c ? JSON.parse(c) : null;
    } catch(e) { return null; }
  },

  applyCoupon: function(couponObj) {
    localStorage.setItem('nevartrend_coupon', JSON.stringify(couponObj));
    this.updateUI();
  },

  removeCoupon: function() {
    localStorage.removeItem('nevartrend_coupon');
    this.updateUI();
  },

  updateUI: function() {
    const cart = this.getCart();
    const totalCount = cart.length;
    const subtotal = this.getSubtotal();
    const discount = this.getDiscount();
    const shipping = this.getShippingFee();
    const grandTotal = this.getTotal();

    // 1. Badges
    document.querySelectorAll('.cart-count-badge').forEach(function(el) {
      el.textContent = totalCount;
      el.style.display = totalCount > 0 ? 'flex' : 'none';
    });

    // 2. Drawer Items Container
    const drawerList = document.getElementById('cart-items-container') || document.getElementById('cart-drawer-items');
    if (drawerList) {
      if (cart.length === 0) {
        drawerList.innerHTML = `
          <div class="text-center py-16 px-4">
            <div class="w-16 h-16 bg-slate-100 rounded-full flex items-center justify-center mx-auto mb-3 text-slate-400">
              <i data-lucide="shopping-bag" class="w-8 h-8"></i>
            </div>
            <p class="font-extrabold text-slate-700 text-sm">Sepetiniz Boş</p>
            <p class="text-xs text-slate-500 mt-1">Beğendiğiniz butik ürün veya kumaşları sepetinize ekleyebilirsiniz.</p>
            <button onclick="CartEngine.closeDrawer()" class="inline-flex items-center gap-1.5 mt-4 px-4 py-2 bg-[#183c2c] text-white rounded-xl text-xs font-bold hover:bg-[#0f281d] transition">
              Alışverişe Devam Et
            </button>
          </div>
        `;
      } else {
        drawerList.innerHTML = cart.map(function(item, idx) {
          const isPiece = item.fabric_id === 'hazir-urun' || item.fabric_id === 'trend-product' || item.fabric_id === 'emprime-service' || item.fabric_id === 'emprime-catalog' || String(item.product_id).startsWith('prod_') || String(item.product_id).startsWith('EMP-');
          const unitLabel = isPiece ? 'Adet' : 'm';
          const nextDown = isPiece ? (item.meters - 1) : parseFloat((item.meters - 0.5).toFixed(1));
          const nextUp = isPiece ? (item.meters + 1) : parseFloat((item.meters + 0.5).toFixed(1));

          return `
            <div class="flex items-center gap-3 p-3 bg-white border border-slate-200/90 rounded-2xl shadow-xs mb-3 hover:border-slate-300 transition">
              <img src="${item.image}" class="w-16 h-16 object-cover rounded-xl flex-shrink-0 border border-slate-200" alt="${item.product_title}">
              <div class="flex-1 min-w-0">
                <div class="flex justify-between items-start gap-1">
                  <h4 class="text-xs font-bold text-slate-900 truncate leading-snug">${item.product_title}</h4>
                  <button onclick="CartEngine.removeItem(${idx})" class="text-slate-400 hover:text-red-500 transition p-1 flex-shrink-0" title="Ürünü Sil">
                    <i data-lucide="trash-2" class="w-3.5 h-3.5"></i>
                  </button>
                </div>
                <p class="text-[11px] text-emerald-800 font-semibold mt-0.5 truncate">${item.fabric_name}</p>
                <div class="flex items-center justify-between mt-2 pt-1 border-t border-slate-100">
                  <div class="flex items-center border border-slate-200 rounded-lg overflow-hidden bg-slate-50">
                    <button onclick="CartEngine.updateMeters(${idx}, ${nextDown})" class="px-2 py-0.5 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-extrabold">-</button>
                    <span class="px-2 py-0.5 text-xs font-bold text-slate-800 min-w-[36px] text-center">${item.meters} ${unitLabel}</span>
                    <button onclick="CartEngine.updateMeters(${idx}, ${nextUp})" class="px-2 py-0.5 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-extrabold">+</button>
                  </div>
                  <span class="text-xs font-black text-slate-900">${item.total_price.toLocaleString('tr-TR')} TL</span>
                </div>
              </div>
            </div>
          `;
        }).join('');
      }
    }

    // 3. Free shipping bar & text
    const freeShippingThreshold = 1000;
    const remainingForFree = Math.max(0, freeShippingThreshold - subtotal);
    const freeShippingProgress = Math.min(100, (subtotal / freeShippingThreshold) * 100);

    const progressBar = document.getElementById('free-shipping-bar') || document.getElementById('free-shipping-progress');
    const freeShippingText = document.getElementById('free-shipping-text');
    if (progressBar) progressBar.style.width = freeShippingProgress + '%';
    if (freeShippingText) {
      if (subtotal >= freeShippingThreshold && subtotal > 0) {
        freeShippingText.innerHTML = '<span class="text-emerald-700 font-bold flex items-center gap-1"><i data-lucide="check-circle-2" class="w-4 h-4"></i> Harika! Ücretsiz Kargo Kazandınız!</span>';
      } else {
        freeShippingText.innerHTML = 'Ücretsiz Kargo için <strong class="text-emerald-800 font-black">' + Math.round(remainingForFree).toLocaleString('tr-TR') + ' TL</strong> daha ekleyin!';
      }
    }

    // 4. Cart page table (/cart)
    const cartTableBody = document.getElementById('cart-page-items');
    if (cartTableBody) {
      if (cart.length === 0) {
        cartTableBody.innerHTML = '<tr><td colspan="6" class="text-center py-12 text-slate-500 font-medium">Sepetinizde ürün bulunmamaktadır.</td></tr>';
      } else {
        cartTableBody.innerHTML = cart.map(function(item, idx) {
          const isPiece = item.fabric_id === 'hazir-urun' || item.fabric_id === 'trend-product' || item.fabric_id === 'emprime-service' || item.fabric_id === 'emprime-catalog' || String(item.product_id).startsWith('prod_') || String(item.product_id).startsWith('EMP-');
          const unitLabel = isPiece ? 'Adet' : 'm';
          const nextDown = isPiece ? (item.meters - 1) : parseFloat((item.meters - 0.5).toFixed(1));
          const nextUp = isPiece ? (item.meters + 1) : parseFloat((item.meters + 0.5).toFixed(1));

          return `
            <tr class="border-b border-slate-100 hover:bg-slate-50/50">
              <td class="py-4 px-4">
                <div class="flex items-center gap-3">
                  <img src="${item.image}" class="w-16 h-16 rounded-xl object-cover border border-slate-200" alt="${item.product_title}">
                  <div>
                    <span class="font-bold text-slate-900 text-sm block">${item.product_title}</span>
                    <span class="text-xs text-slate-400">Kod: ${item.product_code}</span>
                  </div>
                </div>
              </td>
              <td class="py-4 px-4 text-sm font-medium text-slate-700">
                <span class="px-2.5 py-1 bg-emerald-50 text-emerald-800 rounded-md text-xs font-bold border border-emerald-100">${item.fabric_name}</span>
              </td>
              <td class="py-4 px-4 text-sm text-slate-700 font-bold">${item.unit_price.toLocaleString('tr-TR')} TL</td>
              <td class="py-4 px-4">
                <div class="inline-flex items-center border border-slate-200 rounded-lg bg-white overflow-hidden">
                  <button onclick="CartEngine.updateMeters(${idx}, ${nextDown})" class="px-3 py-1 text-slate-600 hover:bg-slate-100 font-bold">-</button>
                  <span class="w-16 text-center text-xs font-bold text-slate-900">${item.meters} ${unitLabel}</span>
                  <button onclick="CartEngine.updateMeters(${idx}, ${nextUp})" class="px-3 py-1 text-slate-600 hover:bg-slate-100 font-bold">+</button>
                </div>
              </td>
              <td class="py-4 px-4 font-black text-slate-900 text-base">${item.total_price.toLocaleString('tr-TR')} TL</td>
              <td class="py-4 px-4 text-right">
                <button onclick="CartEngine.removeItem(${idx})" class="text-slate-400 hover:text-red-600 p-2 rounded-lg hover:bg-red-50 transition">
                  <i data-lucide="trash-2" class="w-4 h-4"></i>
                </button>
              </td>
            </tr>
          `;
        }).join('');
      }
    }

    // 5. Summary elements
    document.querySelectorAll('.summary-subtotal').forEach(function(el) { el.textContent = subtotal.toLocaleString('tr-TR') + ' TL'; });
    document.querySelectorAll('.summary-discount').forEach(function(el) { el.textContent = discount > 0 ? '-' + discount.toLocaleString('tr-TR') + ' TL' : '0 TL'; });
    document.querySelectorAll('.summary-shipping').forEach(function(el) { el.textContent = shipping === 0 ? 'Ücretsiz' : shipping.toFixed(2) + ' TL'; });
    document.querySelectorAll('.summary-grandtotal, .summary-total').forEach(function(el) { el.textContent = grandTotal.toLocaleString('tr-TR') + ' TL'; });

    // 6. Refresh icons
    if (window.lucide) {
      lucide.createIcons();
    }
  },

  openDrawer: function() {
    this.updateUI();
    const drawer = document.getElementById('cart-drawer');
    const overlay = document.getElementById('cart-drawer-overlay');
    if (drawer && overlay) {
      drawer.classList.remove('invisible', 'pointer-events-none');
      drawer.style.visibility = 'visible';
      drawer.style.pointerEvents = 'auto';
      drawer.style.zIndex = '9999';

      overlay.classList.remove('hidden');
      overlay.style.display = 'block';
      overlay.style.zIndex = '9998';

      requestAnimationFrame(function() {
        overlay.classList.remove('opacity-0');
        overlay.style.opacity = '1';
        drawer.classList.remove('translate-x-full');
        drawer.style.transform = 'translateX(0)';
      });
      document.body.style.overflow = 'hidden';
    }
  },

  closeDrawer: function() {
    const drawer = document.getElementById('cart-drawer');
    const overlay = document.getElementById('cart-drawer-overlay');
    if (drawer && overlay) {
      drawer.classList.add('translate-x-full');
      drawer.style.transform = 'translateX(100%)';
      overlay.classList.add('opacity-0');
      overlay.style.opacity = '0';
      setTimeout(function() { 
        overlay.classList.add('hidden'); 
        overlay.style.display = 'none';
        drawer.classList.add('invisible', 'pointer-events-none');
        drawer.style.visibility = 'hidden';
        drawer.style.pointerEvents = 'none';
        document.body.style.overflow = '';
      }, 300);
    }
  },

  showToast: function(message, type) {
    type = type || 'info';
    let container = document.getElementById('toast-container');
    if (!container) {
      container = document.createElement('div');
      container.id = 'toast-container';
      container.className = 'fixed top-20 right-4 sm:top-24 sm:right-6 z-[99999] flex flex-col gap-2 pointer-events-none max-w-sm';
      document.body.appendChild(container);
    }
    const toast = document.createElement('div');
    toast.className = 'flex items-center gap-2.5 px-4 py-3 rounded-2xl shadow-2xl text-xs text-white font-bold transform transition-all duration-300 translate-y-3 opacity-0 pointer-events-auto ' + (type === 'success' ? 'bg-[#183c2c]' : 'bg-slate-900');
    toast.innerHTML = '<i data-lucide="' + (type === 'success' ? 'check-circle' : 'info') + '" class="w-4 h-4 text-emerald-400"></i> <span>' + message + '</span>';
    container.appendChild(toast);
    if (window.lucide) lucide.createIcons();
    
    setTimeout(function() {
      toast.classList.remove('translate-y-3', 'opacity-0');
    }, 20);

    setTimeout(function() {
      toast.classList.add('opacity-0', 'translate-y-3');
      setTimeout(function() { toast.remove(); }, 300);
    }, 3000);
  }
};

document.addEventListener('DOMContentLoaded', function() {
  CartEngine.updateUI();
});

// Close drawer on Escape key
document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape') {
    CartEngine.closeDrawer();
  }
});
