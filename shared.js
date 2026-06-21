// Nexum Shared Components — single source of truth for nav + footer
(function() {
  'use strict';

  // Determine current page for active state
  var path = window.location.pathname;
  var page = path.split('/').pop() || 'index.html';
  if (page === '') page = 'index.html';

  var isIndex = (page === 'index.html' || page === '');

  function active(pageName) {
    return page === pageName ? ' active' : '';
  }

  // ===== NAV =====
  var navHTML = '<nav>'+
    '<div class="nav-inner">'+
      '<a href="'+(isIndex?'':'index.html')+'" class="nav-logo">'+
        '<img src="'+(isIndex?'':'')+'favicon.svg" width="24" height="24" alt="Nexum"> Nexum 逐念而行'+
      '</a>'+
      '<div class="nav-links">'+
        '<a href="'+(isIndex?'#product':'product.html')+'" class="nav-link'+(page==='product.html'?' active':'')+'">产品</a>'+
        '<a href="'+(isIndex?'#technology':'technology.html')+'" class="nav-link'+(page==='technology.html'?' active':'')+'">技术</a>'+
        '<a href="'+(isIndex?'#app':'app.html')+'" class="nav-link'+(page==='app.html'?' active':'')+'">App</a>'+
        '<a href="'+(isIndex?'#team':'index.html#team')+'" class="nav-link">团队</a>'+
      '</div>'+
      '<div class="nav-actions">'+
        '<button class="theme-btn" id="themeToggle" aria-label="切换主题">'+
          '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>'+
        '</button>'+
        '<a href="'+(isIndex?'#contact':'index.html#contact')+'" class="nav-cta">投资者入口</a>'+
      '</div>'+
    '</div>'+
  '</nav>';

  // ===== FOOTER =====
  var footerHTML = '<footer>'+
    '<div class="footer-inner">'+
      '<div class="footer-brand">'+
        '<a href="'+(isIndex?'':'index.html')+'" class="nav-logo">'+
          '<img src="'+(isIndex?'':'')+'favicon.svg" width="24" height="24" alt="Nexum"> Nexum 逐念而行'+
        '</a>'+
        '<p>定义人机共生赛道</p>'+
        '<p style="font-size:12px;color:var(--text-tertiary);margin-top:16px">&copy; 2026 逐念而行 Nexum</p>'+
      '</div>'+
      '<div>'+
        '<h5>页面</h5>'+
        '<a href="'+(isIndex?'':'index.html')+'">首页</a>'+
        '<a href="'+(isIndex?'product.html':'product.html')+'">产品</a>'+
        '<a href="'+(isIndex?'technology.html':'technology.html')+'">技术</a>'+
        '<a href="'+(isIndex?'app.html':'app.html')+'">App</a>'+
      '</div>'+
      '<div>'+
        '<h5>更多</h5>'+
        '<a href="'+(isIndex?'':'')+'逐念而行_Nexum_BP.html">商业计划书</a>'+
        '<a href="'+(isIndex?'prd.html':'prd.html')+'">产品需求</a>'+
        '<a href="'+(isIndex?'clinical-protocol.html':'clinical-protocol.html')+'">临床方案</a>'+
        '<a href="'+(isIndex?'engineering-architecture.html':'engineering-architecture.html')+'">工程架构</a>'+
      '</div>'+
      '<div>'+
        '<h5>联系</h5>'+
        '<a href="mailto:hello@nexum.ai">hello@nexum.ai</a>'+
        '<p>中国 &middot; 上海</p>'+
        '<a href="https://github.com/nexum-bci" target="_blank" rel="noopener">GitHub</a>'+
      '</div>'+
    '</div>'+
    '<div class="footer-bottom">'+
      '<p>Confidential &mdash; For Investor Use Only</p>'+
    '</div>'+
  '</footer>';

  // Inject nav at body start
  document.body.insertAdjacentHTML('afterbegin', navHTML);

  // Inject footer at body end
  document.body.insertAdjacentHTML('beforeend', footerHTML);

  // Theme toggle logic
  var toggle = document.getElementById('themeToggle');
  if (toggle) {
    function setTheme(t) {
      if (t === 'dark') {
        document.documentElement.setAttribute('data-theme', 'dark');
        localStorage.setItem('nexum-theme', 'dark');
      } else {
        document.documentElement.removeAttribute('data-theme');
        localStorage.setItem('nexum-theme', 'light');
      }
    }
    toggle.addEventListener('click', function() {
      var isDark = document.documentElement.hasAttribute('data-theme');
      setTheme(isDark ? 'light' : 'dark');
    });
  }

  // Add page transition
  var style = document.createElement('style');
  style.textContent = 'body{opacity:0;animation:fadeIn .25s ease forwards}@keyframes fadeIn{to{opacity:1}}';
  document.head.appendChild(style);

})();
