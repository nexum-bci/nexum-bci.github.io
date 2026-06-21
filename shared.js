// Nexum Shared Components — single source of truth for nav + footer
(function() {
  'use strict';

  var path = window.location.pathname;
  var page = path.split('/').pop() || 'index.html';
  if (page === '') page = 'index.html';
  var isIndex = (page === 'index.html' || page === '');

  // SVG icons for theme toggle
  var sunSVG = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>';
  var moonSVG = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';

  // ===== NAV =====
  var navHTML = '<nav>'+
    '<div class="nav-inner">'+
      '<a href="'+(isIndex?'':'index.html')+'" class="nav-logo">'+
        '<img src="'+(isIndex?'':'')+'favicon.svg" width="24" height="24" alt="Nexum"> Nexum 逐念而行'+
      '</a>'+
      '<div class="nav-links">'+
        '<a href="'+(isIndex?'#product':'product.html')+'" class="nav-link">产品</a>'+
        '<a href="'+(isIndex?'#technology':'technology.html')+'" class="nav-link">技术</a>'+
        '<a href="'+(isIndex?'#app':'app.html')+'" class="nav-link">App</a>'+
        '<a href="'+(isIndex?'#team':'index.html#team')+'" class="nav-link">团队</a>'+
      '</div>'+
      '<div class="nav-actions">'+
        '<button class="theme-btn" id="themeToggle" aria-label="切换主题"></button>'+
        '<a href="'+(isIndex?'':'')+'逐念而行_Nexum_BP.html" class="nav-cta">'+
          'BP <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"/></svg>'+
        '</a>'+
      '</div>'+
      '<button class="nav-toggle" id="navToggle" aria-label="菜单">'+
        '<span></span><span></span><span></span>'+
      '</button>'+
    '</div>'+
  '</nav>';

  // ===== FOOTER =====
  var footerHTML = '<footer>'+
    '<div class="footer-inner">'+
      '<div class="footer-brand">'+
        '<a href="'+(isIndex?'':'index.html')+'" class="footer-logo">'+
          '<img src="'+(isIndex?'':'')+'favicon.svg" width="28" height="28" alt="Nexum">'+
          '<span>逐念而行 Nexum</span>'+
        '</a>'+
        '<p class="footer-tagline">从大脑到肌肉的AI。读取运动意图，AI生成策略，驱动穿戴式外骨骼。定义人机共生赛道。</p>'+
        '<div class="footer-social">'+
          '<a href="https://github.com/nexum-bci" target="_blank" rel="noopener" aria-label="GitHub">'+
            '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/></svg>'+
          '</a>'+
          '<a href="mailto:hello@nexum.ai" aria-label="Email">'+
            '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="M22 4L12 13 2 4"/></svg>'+
          '</a>'+
        '</div>'+
      '</div>'+
      '<div class="footer-col">'+
        '<h5>了解 Nexum</h5>'+
        '<a href="'+(isIndex?'product.html':'product.html')+'">产品概览</a>'+
        '<a href="'+(isIndex?'technology.html':'technology.html')+'">技术架构</a>'+
        '<a href="'+(isIndex?'app.html':'app.html')+'">App 设计</a>'+
        '<a href="'+(isIndex?'product-renders.html':'product-renders.html')+'">产品渲染</a>'+
      '</div>'+
      '<div class="footer-col">'+
        '<h5>深度</h5>'+
        '<a href="'+(isIndex?'engineering.html':'engineering.html')+'">工程架构</a>'+
        '<a href="'+(isIndex?'clinical-protocol.html':'clinical-protocol.html')+'">临床方案</a>'+
        '<a href="'+(isIndex?'regulatory-strategy.html':'regulatory-strategy.html')+'">注册策略</a>'+
        '<a href="'+(isIndex?'prd.html':'prd.html')+'">产品需求</a>'+
      '</div>'+
      '<div class="footer-col">'+
        '<h5>更多</h5>'+
        '<a href="'+(isIndex?'production-bom.html':'production-bom.html')+'">生产 BOM</a>'+
        '<a href="'+(isIndex?'':'')+'逐念而行_Nexum_BP.html">商业计划书</a>'+
        '<a href="https://github.com/nexum-bci" target="_blank" rel="noopener">GitHub</a>'+
        '<a href="mailto:hello@nexum.ai">hello@nexum.ai</a>'+
      '</div>'+
    '</div>'+
    '<div class="footer-bottom">'+
      '<p>&copy; 2026 逐念而行 Nexum · 人机共生 · 上海</p>'+
    '</div>'+
  '</footer>';

  document.body.insertAdjacentHTML('afterbegin', navHTML);
  document.body.insertAdjacentHTML('beforeend', footerHTML);

  // ===== THEME TOGGLE =====
  // Restore theme from localStorage on load
  (function() {
    var savedTheme = localStorage.getItem('nexum-theme');
    if (savedTheme === 'dark') {
      document.documentElement.setAttribute('data-theme', 'dark');
    }
  })();

  var toggle = document.getElementById('themeToggle');
  if (toggle) {
    var isDark = document.documentElement.hasAttribute('data-theme');
    toggle.innerHTML = isDark ? sunSVG : moonSVG;
    toggle.addEventListener('click', function() {
      var isDark = document.documentElement.hasAttribute('data-theme');
      toggle.classList.add('rotating');
      var myToggle = toggle;
      setTimeout(function() { myToggle.classList.remove('rotating'); }, 400);
      if (isDark) {
        document.documentElement.removeAttribute('data-theme');
        localStorage.setItem('nexum-theme', 'light');
        toggle.innerHTML = moonSVG;
      } else {
        document.documentElement.setAttribute('data-theme', 'dark');
        localStorage.setItem('nexum-theme', 'dark');
        toggle.innerHTML = sunSVG;
      }
    });
  }

  // ===== MOBILE NAV TOGGLE =====
  (function() {
    var navToggleBtn = document.getElementById('navToggle');
    var navEl = document.querySelector('nav');
    if (navToggleBtn && navEl) {
      navToggleBtn.addEventListener('click', function() {
        navEl.classList.toggle('nav-open');
      });
      document.querySelectorAll('.nav-link').forEach(function(link) {
        link.addEventListener('click', function() {
          navEl.classList.remove('nav-open');
        });
      });
      window.addEventListener('scroll', function() {
        navEl.classList.remove('nav-open');
      }, { passive: true });
    }
  })();

  // ===== ACTIVE NAV LINK =====
  (function() {
    var curPage = window.location.pathname.split('/').pop() || 'index.html';
    document.querySelectorAll('.nav-link').forEach(function(link) {
      var href = link.getAttribute('href');
      if (href === curPage || href === '#' + curPage.replace('.html', '')) {
        link.classList.add('active');
      }
    });
  })();

  // ===== NAV SCROLL BEHAVIOR =====
  // Adds .nav-scrolled for opacity change and .nav-shrink for height reduction
  (function() {
    var navEl = document.querySelector('nav');
    var lastScrollY = window.scrollY;
    var ticking = false;

    if (!navEl) return;

    function updateNav() {
      var scrollY = window.scrollY;

      // Scrolled state — intensify glass blur when past threshold
      if (scrollY > 20) {
        navEl.classList.add('nav-scrolled');
      } else {
        navEl.classList.remove('nav-scrolled');
      }

      // Shrink nav height on scroll down, restore on scroll up
      if (scrollY > 80 && scrollY > lastScrollY + 5) {
        navEl.classList.add('nav-shrink');
      } else if (scrollY < lastScrollY - 5 || scrollY < 80) {
        navEl.classList.remove('nav-shrink');
      }

      lastScrollY = scrollY;
    }

    // Set initial state (handles page load with existing scroll position)
    updateNav();

    window.addEventListener('scroll', function() {
      if (!ticking) {
        window.requestAnimationFrame(function() {
          updateNav();
          ticking = false;
        });
        ticking = true;
      }
    }, { passive: true });
  })();

  // ===== PAGE TRANSITION =====
  var style = document.createElement('style');
  style.textContent = 'body{opacity:0;animation:fadeIn .4s cubic-bezier(0.16,1,0.3,1) forwards}@keyframes fadeIn{to{opacity:1}}';
  document.head.appendChild(style);

  // Smooth fade-out on internal navigation
  document.addEventListener('click', function(e) {
    var link = e.target.closest('a');
    if (!link) return;
    var href = link.getAttribute('href');
    // Only intercept relative internal links (no protocol, no hash, no mailto)
    if (!href || href.startsWith('#') || href.startsWith('//') || href.indexOf(':') !== -1) return;

    e.preventDefault();
    document.body.style.transition = 'opacity .2s ease';
    document.body.style.opacity = '0';
    setTimeout(function() {
      window.location.href = href;
    }, 200);
  });

  // Handle bfcache — restore opacity when navigating back
  window.addEventListener('pageshow', function(e) {
    if (e.persisted) {
      document.body.style.opacity = '1';
      document.body.style.transition = 'none';
    }
  });

  // ===== BACK-TO-TOP BUTTON =====
  var btt = document.createElement('button');
  btt.className = 'btt-btn';
  btt.innerHTML = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="18 15 12 9 6 15"/></svg>';
  btt.setAttribute('aria-label', '回到顶部');
  btt.style.cssText = 'position:fixed;bottom:28px;right:28px;z-index:999;width:44px;height:44px;border-radius:50%;border:1px solid var(--border);cursor:pointer;display:flex;align-items:center;justify-content:center;color:var(--text-secondary);box-shadow:0 4px 16px rgba(0,0,0,0.1);transition:all 0.3s cubic-bezier(.16,1,.3,1);opacity:0;pointer-events:none';
  btt.addEventListener('click',function(){window.scrollTo({top:0,behavior:'smooth'})});
  btt.addEventListener('mouseenter',function(){this.style.transform='translateY(-3px)';this.style.boxShadow='0 8px 28px rgba(0,0,0,0.15)'});
  btt.addEventListener('mouseleave',function(){this.style.transform='translateY(0)';this.style.boxShadow='0 4px 16px rgba(0,0,0,0.1)'});
  document.body.appendChild(btt);
  window.addEventListener('scroll',function(){
    if(window.scrollY>400){btt.style.opacity='1';btt.style.pointerEvents='auto'}
    else{btt.style.opacity='0';btt.style.pointerEvents='none'}
  });

})();
