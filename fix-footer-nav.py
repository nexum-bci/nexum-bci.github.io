#!/usr/bin/env python3
"""Fix footer and nav across all Nexum website HTML files."""

import os
import re

REPO = "/Users/ziruizhao/Desktop/EXO/repos/nexum"

# ===================================================================
# STANDARD NAV HTML
# ===================================================================
NAV_HTML = """<nav>
  <div class="nav-inner">
    <a href="index.html" class="nav-logo">
      <img src="favicon.svg" width="24" height="24" alt="Nexum"> Nexum 逐念而行
    </a>
    <div class="nav-links">
      <a href="index.html">首页</a>
      <a href="product.html">产品</a>
      <a href="technology.html">技术</a>
      <a href="app.html">App</a>
      <a href="index.html#documents">文档</a>
      <a href="index.html#team">团队</a>
    </div>
    <div class="nav-actions">
      <button class="theme-btn" id="themeToggle" aria-label="切换主题"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg></button>
      <a href="index.html#contact" class="nav-cta">投资者入口</a>
      <button class="nav-toggle" id="navToggle" aria-label="菜单">
        <span></span><span></span><span></span>
      </button>
    </div>
  </div>
</nav>"""

# ===================================================================
# STANDARD FOOTER HTML
# ===================================================================
FOOTER_HTML = """<footer>
  <div class="footer-inner">
    <div class="footer-brand">
      <a href="index.html" class="nav-logo">
        <img src="favicon.svg" width="24" height="24" alt="Nexum"> Nexum 逐念而行
      </a>
      <p>定义人机共生赛道</p>
      <p style="font-size:12px;color:var(--text-tertiary);margin-top:16px">&copy; 2026 逐念而行 Nexum</p>
    </div>
    <div>
      <h5>页面</h5>
      <a href="index.html">首页</a>
      <a href="product.html">产品</a>
      <a href="technology.html">技术</a>
      <a href="app.html">App</a>
    </div>
    <div>
      <h5>文档</h5>
      <a href="逐念而行_Nexum_BP.html">商业计划书</a>
      <a href="prd.html">产品需求文档</a>
      <a href="clinical-protocol.html">临床方案</a>
      <a href="engineering-architecture.html">工程架构</a>
    </div>
    <div>
      <h5>联系</h5>
      <a href="mailto:hello@nexum.ai">hello@nexum.ai</a>
      <p>中国 · 上海</p>
      <a href="https://github.com/nexum-bci" target="_blank">GitHub</a>
    </div>
  </div>
  <div class="footer-bottom">
    &copy; 2026 逐念而行 Nexum. All rights reserved.
  </div>
</footer>"""

# ===================================================================
# NAV CSS (for files that don't have class-based nav CSS)
# ===================================================================
NAV_CSS = """
/* ===== NAV ===== */
nav{position:fixed;top:0;left:0;right:0;z-index:1000;backdrop-filter:blur(20px) saturate(180%);-webkit-backdrop-filter:blur(20px) saturate(180%);background:var(--nav-bg,rgba(255,255,255,0.8));border-bottom:1px solid var(--border);height:64px;transition:background .35s ease,border-color .35s ease}
[data-theme="dark"] nav{background:rgba(0,0,0,0.8)}
.nav-inner{max-width:1100px;margin:0 auto;padding:0 24px;display:flex;align-items:center;height:64px;gap:24px}
.nav-logo{display:flex;align-items:center;gap:8px;font-weight:700;font-size:16px;color:var(--text);text-decoration:none;flex-shrink:0}
.nav-logo img{width:24px;height:24px;display:block}
.nav-links{display:flex;gap:20px;flex:1}
.nav-links a{font-size:14px;font-weight:500;color:var(--text-secondary);text-decoration:none;position:relative;transition:color .2s}
.nav-links a:hover{color:var(--text)}
.nav-links a::after{content:'';position:absolute;bottom:-4px;left:0;right:0;height:2px;background:var(--accent);transform:scaleX(0);transition:transform .2s}
.nav-links a:hover::after{transform:scaleX(1)}
.nav-actions{display:flex;align-items:center;gap:12px;flex-shrink:0}
.theme-btn{width:36px;height:36px;border:1px solid var(--border);border-radius:8px;background:var(--bg-card);cursor:pointer;font-size:16px;color:var(--text);display:flex;align-items:center;justify-content:center}
.theme-btn:hover{background:var(--accent-subtle)}
.nav-cta{display:inline-flex;align-items:center;gap:6px;background:var(--accent);color:#fff!important;padding:6px 16px;border-radius:20px;font-size:13px;font-weight:600;text-decoration:none}
.nav-cta:hover{opacity:.9}
.nav-toggle{display:none;background:none;border:none;cursor:pointer;padding:4px}
.nav-toggle span{display:block;width:22px;height:2px;background:var(--text);margin:4px 0;border-radius:1px;transition:all .3s cubic-bezier(.16,1,.3,1)}
.nav-open .nav-toggle span:nth-child(1){transform:rotate(45deg) translate(4px,4px)}
.nav-open .nav-toggle span:nth-child(2){opacity:0}
.nav-open .nav-toggle span:nth-child(3){transform:rotate(-45deg) translate(4px,-4px)}
@media(max-width:768px){.nav-toggle{display:block}.nav-links{position:fixed;top:64px;left:0;right:0;background:var(--bg-card);flex-direction:column;padding:16px 24px;gap:4px;border-bottom:1px solid var(--border);transform:translateY(-120%);opacity:0;pointer-events:none;transition:all .3s cubic-bezier(.16,1,.3,1)}.nav-open .nav-links{transform:translateY(0);opacity:1;pointer-events:auto}.nav-links a{padding:12px 0;display:block;font-size:15px}.nav-cta{font-size:12px;padding:6px 14px}}
"""

# ===================================================================
# FOOTER CSS
# ===================================================================
FOOTER_CSS = """
/* ===== FOOTER ===== */
footer{background:var(--bg-card);border-top:1px solid var(--border);padding:80px 24px 40px}
.footer-inner{max-width:1100px;margin:0 auto;display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:48px}
footer h5{font-size:12px;font-weight:600;letter-spacing:.5px;text-transform:uppercase;color:var(--text-secondary);margin-bottom:16px}
footer a{font-size:13px;color:var(--text-tertiary);text-decoration:none;line-height:2.2;transition:color .2s;display:block}
footer a:hover{color:var(--accent)}
footer p{font-size:13px;color:var(--text-tertiary);line-height:2.2}
.footer-brand p{line-height:1.6;margin-top:8px}
.footer-bottom{border-top:1px solid var(--border);padding-top:24px;margin-top:48px;text-align:center;font-size:12px;color:var(--text-tertiary);max-width:1100px;margin-left:auto;margin-right:auto}
@media(max-width:768px){.footer-inner{grid-template-columns:1fr 1fr;gap:32px}.footer-inner>div:first-child{grid-column:1/-1}footer{padding:60px 20px 32px}}
@media(max-width:480px){.footer-inner{grid-template-columns:1fr}}
"""

# ===================================================================
# STANDARD THEME TOGGLE + MOBILE NAV SCRIPT
# ===================================================================
STANDARD_SCRIPT = """<script>
(function(){
  var toggle = document.getElementById('themeToggle');
  function setTheme(t){
    if(t==='dark') document.documentElement.setAttribute('data-theme','dark');
    else document.documentElement.removeAttribute('data-theme');
    localStorage.setItem('nexum-theme',t);
  }
  var saved = localStorage.getItem('nexum-theme');
  if(saved==='dark') setTheme('dark');
  if(document.documentElement.hasAttribute('data-theme')) toggle.innerHTML = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>';
  else toggle.innerHTML = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';
  toggle.addEventListener('click',function(){
    var isDark = document.documentElement.hasAttribute('data-theme');
    setTheme(isDark?'light':'dark');
    toggle.innerHTML = isDark?'<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>':'<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>';
  });
  var navToggle = document.getElementById('navToggle');
  if(navToggle) {
    var nav = document.querySelector('nav');
    navToggle.addEventListener('click',function(){ nav.classList.toggle('nav-open'); });
    document.querySelectorAll('.nav-links a').forEach(function(a){
      a.addEventListener('click',function(){ nav.classList.remove('nav-open'); });
    });
  }
})();
</script>"""

# ===================================================================
# OLD INLINE NAV (exact match for Group A "doc" files)
# ===================================================================
OLD_INLINE_NAV = """<nav>
  <div style="max-width:1100px;margin:0 auto;padding:0 24px;display:flex;align-items:center;height:64px;gap:24px">
    <a href="index.html" style="display:flex;align-items:center;gap:8px;font-weight:700;color:var(--text);text-decoration:none">
      <img src="favicon.svg" width="24" height="24"> Nexum 逐念而行
    </a>
    <div style="flex:1;display:flex;gap:20px">
      <a href="product.html" style="color:var(--text-secondary);text-decoration:none;font-size:14px">产品</a>
      <a href="technology.html" style="color:var(--text-secondary);text-decoration:none;font-size:14px">技术</a>
      <a href="app.html" style="color:var(--text-secondary);text-decoration:none;font-size:14px">App</a>
      <a href="index.html#documents" style="color:var(--text-secondary);text-decoration:none;font-size:14px">文档</a>
      <a href="index.html#team" style="color:var(--text-secondary);text-decoration:none;font-size:14px">团队</a>
    </div>
    <div style="display:flex;align-items:center;gap:12px">
      <button id="themeToggle" style="width:36px;height:36px;border:1px solid var(--border);border-radius:8px;background:var(--bg-card);cursor:pointer;font-size:16px;color:var(--text)"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg></button>
      <a href="index.html#contact" style="display:inline-flex;align-items:center;gap:6px;background:var(--accent);color:#fff!important;padding:6px 16px;border-radius:20px;font-size:13px;font-weight:600;text-decoration:none">投资者入口</a>
    </div>
  </div>
</nav>"""

# ===================================================================
# OLD INLINE FOOTER (exact match for Group A "doc" files)
# ===================================================================
OLD_INLINE_FOOTER_PATTERN = r'<footer style="border-top:1px solid var\(--border\);padding:64px 24px 32px;margin-top:48px;background:var\(--bg-card\)"[^>]*>.*?</footer>'

# ===================================================================
# OLD SIMPLE THEME TOGGLE SCRIPT
# ===================================================================
OLD_SIMPLE_SCRIPT_PATTERN = r'<script>\s*document\.getElementById\([\'"]themeToggle[\'"]\)\.addEventListener\([\'"]click[\'"],function\(\)\{[^}]+if\(isDark\)[^}]+[^}]+}[^}]+}[^}]+</script>'


def fix_group_a_files():
    """Fix the 8 doc files that share the same inline nav/footer pattern."""
    files = [
        "prd.html", "clinical-protocol.html", "engineering-architecture.html",
        "engineering-diagrams.html", "production-bom.html", "regulatory-strategy.html",
        "product-visualization.html", "product-renders.html"
    ]

    for fname in files:
        fpath = os.path.join(REPO, fname)
        print(f"Processing {fname}...")

        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()

        # 1. Replace inline nav with standard nav
        if OLD_INLINE_NAV in content:
            content = content.replace(OLD_INLINE_NAV, NAV_HTML)
            print(f"  -> Replaced nav")
        else:
            print(f"  -> WARNING: Old nav not found!")
            # Debug: try to find the nav
            nav_start = content.find('<nav>')
            if nav_start >= 0:
                nav_end = content.find('</nav>', nav_start)
                print(f"  -> Found nav at {nav_start}-{nav_end}")
                print(f"  -> Nav preview: {content[nav_start:nav_start+200]}")

        # 2. Replace inline footer with standard footer
        footer_match = re.search(OLD_INLINE_FOOTER_PATTERN, content, re.DOTALL)
        if footer_match:
            old_footer = footer_match.group(0)
            content = content.replace(old_footer, FOOTER_HTML)
            print(f"  -> Replaced footer")
        else:
            print(f"  -> WARNING: Old footer not found!")

        # 3. Replace simple theme toggle script with standard one
        # Find the simple theme toggle script pattern
        simple_script = 'document.getElementById(\'themeToggle\')'
        if simple_script in content:
            # Find the exact script block
            script_start = content.rfind('<script>', 0, content.find(simple_script))
            if script_start < 0:
                script_start = content.rfind('<script>\n', 0, content.find(simple_script))
            script_end = content.find('</script>', script_start)

            if script_start >= 0 and script_end >= 0:
                old_script = content[script_start:script_end + 9]
                # Check if this is a simple theme toggle (not the big one with scroll reveal)
                if 'document.getElementById(\'themeToggle\')' in old_script and 'navToggle' not in old_script:
                    content = content.replace(old_script, STANDARD_SCRIPT)
                    print(f"  -> Replaced theme toggle script")
                else:
                    print(f"  -> Skipped script (may already have navToggle)")

        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)

    print("Group A done.\n")


def fix_app_html():
    """Fix app.html - similar to group A but with slight differences."""
    fpath = os.path.join(REPO, "app.html")
    print(f"Processing app.html...")

    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace nav - app.html has a slightly different inline nav
    old_app_nav = """<nav>
  <div style="max-width:1100px;margin:0 auto;padding:0 24px;display:flex;align-items:center;height:64px;gap:24px">
    <a href="index.html" style="display:flex;align-items:center;gap:8px;font-weight:700;color:var(--text);text-decoration:none">
      <img src="favicon.svg" width="24" height="24"> Nexum 逐念而行
    </a>
    <div style="flex:1;display:flex;gap:20px">
      <a href="product.html" style="color:var(--text-secondary);text-decoration:none;font-size:14px">产品</a>
      <a href="technology.html" style="color:var(--text-secondary);text-decoration:none;font-size:14px">技术</a>
      <a href="app.html" style="color:var(--text-secondary);text-decoration:none;font-size:14px">App</a>
      <a href="index.html#documents" style="color:var(--text-secondary);text-decoration:none;font-size:14px">文档</a>
      <a href="index.html#team" style="color:var(--text-secondary);text-decoration:none;font-size:14px">团队</a>
    </div>
    <div style="display:flex;align-items:center;gap:12px">
      <button id="themeToggle" style="width:36px;height:36px;border:1px solid var(--border);border-radius:8px;background:var(--bg-card);cursor:pointer;font-size:16px;color:var(--text)"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg></button>
      <a href="index.html#contact" style="display:inline-flex;align-items:center;gap:6px;background:var(--accent);color:#fff!important;padding:6px 16px;border-radius:20px;font-size:13px;font-weight:600;text-decoration:none">投资者入口</a>
    </div>
  </div>
</nav>"""

    if old_app_nav in content:
        content = content.replace(old_app_nav, NAV_HTML)
        print(f"  -> Replaced nav")
    else:
        print(f"  -> WARNING: Old nav not found!")

    # Replace footer (same pattern as group A)
    footer_match = re.search(OLD_INLINE_FOOTER_PATTERN, content, re.DOTALL)
    if footer_match:
        content = content.replace(footer_match.group(0), FOOTER_HTML)
        print(f"  -> Replaced footer")
    else:
        print(f"  -> WARNING: Old footer not found!")

    # Replace theme toggle script
    simple_script = 'document.getElementById(\'themeToggle\')'
    if simple_script in content:
        script_start = content.rfind('<script>', 0, content.find(simple_script))
        if script_start < 0:
            script_start = content.rfind('<script>\n', 0, content.find(simple_script))
        script_end = content.find('</script>', script_start)

        if script_start >= 0 and script_end >= 0:
            old_script = content[script_start:script_end + 9]
            if 'document.getElementById(\'themeToggle\')' in old_script and 'navToggle' not in old_script:
                content = content.replace(old_script, STANDARD_SCRIPT)
                print(f"  -> Replaced theme toggle script")

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)

    print("app.html done.\n")


def fix_app_ui_mockups():
    """Fix app-ui-mockups.html."""
    fpath = os.path.join(REPO, "app-ui-mockups.html")
    print(f"Processing app-ui-mockups.html...")

    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Nav - app-ui-mockups has a slightly different nav (no 团队 link, no CTA)
    old_nav = """<nav>
  <div style="max-width:1100px;margin:0 auto;padding:0 24px;display:flex;align-items:center;height:64px;gap:24px">
    <a href="index.html" style="display:flex;align-items:center;gap:8px;font-weight:700;color:var(--text);text-decoration:none">
      <img src="favicon.svg" width="24" height="24"> Nexum 逐念而行
    </a>
    <div style="flex:1;display:flex;gap:20px">
      <a href="product.html" style="color:var(--text-secondary);text-decoration:none;font-size:14px">产品</a>
      <a href="technology.html" style="color:var(--text-secondary);text-decoration:none;font-size:14px">技术</a>
      <a href="app.html" style="color:var(--text-secondary);text-decoration:none;font-size:14px">App</a>
      <a href="index.html#documents" style="color:var(--text-secondary);text-decoration:none;font-size:14px">文档</a>
    </div>
    <button id="themeToggle" style="width:36px;height:36px;border:1px solid var(--border);border-radius:8px;background:var(--bg-card);cursor:pointer;font-size:16px;color:var(--text)"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg></button>
  </div>
</nav>"""

    if old_nav in content:
        content = content.replace(old_nav, NAV_HTML)
        print(f"  -> Replaced nav")
    else:
        print(f"  -> WARNING: Old nav not found!")

    # Replace footer (same pattern)
    footer_match = re.search(OLD_INLINE_FOOTER_PATTERN, content, re.DOTALL)
    if footer_match:
        content = content.replace(footer_match.group(0), FOOTER_HTML)
        print(f"  -> Replaced footer")
    else:
        print(f"  -> WARNING: Old footer not found!")

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)

    print("app-ui-mockups.html done.\n")


def fix_product_and_technology():
    """Fix product.html and technology.html - already have nav CSS, need footer HTML update."""
    files = ["product.html", "technology.html"]

    for fname in files:
        fpath = os.path.join(REPO, fname)
        print(f"Processing {fname}...")

        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Replace the footer HTML block
        # The old footer in product/technology starts with <footer class="footer">
        old_footer_start = """<footer class="footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <a href="index.html" class="nav-logo" style="margin-bottom:8px;display:inline-flex;">
          <img src="favicon.svg" width="24" height="24" alt="Nexum">Nexum 逐念而行
        </a>
        <p>从大脑到肌肉的AI。读取大脑运动意图，AI生成个性化策略，驱动轻量穿戴式外骨骼，持续进化——定义人机共生。</p>
      </div>
      <div class="footer-col">
        <h4>导航</h4>
        <a href="index.html">首页</a>
        <a href="product.html">产品</a>
        <a href="technology.html">技术</a>
        <a href="app.html">App</a>
        <a href="index.html#team">团队</a>
      </div>
      <div class="footer-col">
        <h4>文档</h4>
        <a href="逐念而行_Nexum_BP.html">商业计划书</a>
        <a href="prd.html">产品需求文档</a>
        <a href="clinical-protocol.html">临床方案</a>
        <a href="engineering-architecture.html">工程架构</a>
        <a href="docs/README.md">文档索引</a>
      </div>
      <div class="footer-col">
        <h4>联系</h4>
        <a href="mailto:hello@nexum.ai">hello@nexum.ai</a>
        <p>中国 · 上海</p>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; 2026 逐念而行 Nexum. All rights reserved.</span>
      <span>Confidential — For Investor Use Only</span>
    </div>
  </div>
</footer>"""

        if old_footer_start in content:
            content = content.replace(old_footer_start, FOOTER_HTML)
            print(f"  -> Replaced footer")
        else:
            print(f"  -> WARNING: Old footer not found! Trying alternate check...")
            # Maybe there's a slightly different version
            if '<footer class="footer">' in content:
                print(f"  -> Found <footer class='footer'> tag")

        # Also update the footer CSS section to match new design
        old_footer_css = """/* ===== FOOTER ===== */
.footer{
  border-top:1px solid var(--border);padding:80px 0 48px;
  margin-top:0;
}
.footer-grid{display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:40px;}
.footer-brand p{font-size:13px;color:var(--text-tertiary);margin-top:8px;max-width:280px;}
.footer-col h4{font-size:12px;font-weight:600;text-transform:uppercase;letter-spacing:1px;
  color:var(--text);margin-bottom:16px;}
.footer-col a{display:block;font-size:13px;color:var(--text-secondary);padding:4px 0;}
.footer-col a:hover{color:var(--accent);}
.footer-bottom{margin-top:40px;padding-top:20px;border-top:1px solid var(--border);
  font-size:12px;color:var(--text-tertiary);display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px;}
@media(max-width:768px){.footer-grid{grid-template-columns:1fr 1fr;}}"""

        # Replace with new footer CSS
        if old_footer_css in content:
            # Keep the existing footer CSS mostly, just enhance it
            new_footer_css = """/* ===== FOOTER ===== */
footer{background:var(--bg-card);border-top:1px solid var(--border);padding:80px 0 48px}
.footer-grid{display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:48px}
.footer-brand p{font-size:13px;color:var(--text-tertiary);margin-top:8px;max-width:280px;line-height:1.6}
footer h4{font-size:12px;font-weight:600;letter-spacing:.5px;text-transform:uppercase;color:var(--text-secondary);margin-bottom:16px}
footer a{font-size:13px;color:var(--text-tertiary);text-decoration:none;line-height:2.2;transition:color .2s;display:block}
footer a:hover{color:var(--accent)}
footer p{font-size:13px;color:var(--text-tertiary);line-height:2.2}
.footer-bottom{margin-top:48px;padding-top:24px;border-top:1px solid var(--border);text-align:center;font-size:12px;color:var(--text-tertiary)}
@media(max-width:768px){.footer-grid{grid-template-columns:1fr 1fr;gap:32px}.footer-grid>div:first-child{grid-column:1/-1}footer{padding:60px 20px 32px}}"""
            content = content.replace(old_footer_css, new_footer_css)
            print(f"  -> Updated footer CSS")
        else:
            print(f"  -> WARNING: Old footer CSS not found!")

        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)

    print("product.html and technology.html done.\n")


def fix_index():
    """Fix index.html - has its own nav already, needs footer updated."""
    fpath = os.path.join(REPO, "index.html")
    print(f"Processing index.html...")

    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace the footer HTML block
    # index.html has a unique footer structure
    old_index_footer_start = """<footer><div><img src="logo.png" alt="" style="height:32px"><p style="font-size:14px;font-weight:500;margin-top:8px">Neuromusculoskeletal AI for Consumer Exoskeletons</p><p style="font-size:11px;color:rgba(255,255,255,.4);margin-top:4px">Nanjing · Boston</p></div><div class="links"><dl><dt>Projects</dt><dd><a href="https://github.com/bones-manifold/bones">bones</a></dd><dd><a href="https://github.com/bones-manifold/myowarp">myowarp</a></dd></dl><dl><dt>Resources</dt><dd><a href="https://github.com/bones-manifold">GitHub</a></dd><dd><a href="mailto:sayhi@bones-manifold.com">Contact</a></dd></dl><dl><dt>Language</dt><dd><a href="index-zh.html">中文</a></dd></dl></div><div class="btm">&copy;&nbsp;2026 Bones &amp; Manifold</div></footer>"""

    if old_index_footer_start in content:
        content = content.replace(old_index_footer_start, FOOTER_HTML)
        print(f"  -> Replaced footer")
    else:
        print(f"  -> WARNING: Old index footer not found! Checking pattern...")
        if '<footer>' in content:
            start = content.find('<footer>')
            end = content.find('</footer>', start) + 9
            print(f"  -> Found footer at {start}-{end}")
            print(f"  -> Preview: {content[start:start+150]}")

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)

    print("index.html done.\n")


def add_css_to_group_a():
    """Add nav and footer CSS to the 8 doc files that lack them."""
    files = [
        "prd.html", "clinical-protocol.html", "engineering-architecture.html",
        "engineering-diagrams.html", "production-bom.html", "regulatory-strategy.html",
        "product-visualization.html", "product-renders.html"
    ]

    for fname in files:
        fpath = os.path.join(REPO, fname)
        print(f"Adding CSS to {fname}...")

        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if nav CSS already exists
        if '.nav-inner' in content:
            print(f"  -> Nav CSS already exists, skipping")
        else:
            # Add nav CSS before </style>
            if NAV_CSS in content:
                print(f"  -> Nav CSS already added")
            else:
                content = content.replace('</style>', NAV_CSS + '\n</style>')
                print(f"  -> Added nav CSS")

        # Check if footer CSS already exists
        if 'footer{' in content.lower().replace(' ', '') or '.footer-inner' in content:
            print(f"  -> Footer CSS already exists, skipping")
        elif FOOTER_CSS in content:
            print(f"  -> Footer CSS already added")
        else:
            content = content.replace('</style>', FOOTER_CSS + '\n</style>')
            print(f"  -> Added footer CSS")

        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)

    print("CSS added to Group A.\n")


def add_css_to_app():
    """Add nav and footer CSS to app.html."""
    fpath = os.path.join(REPO, "app.html")
    print(f"Adding CSS to app.html...")

    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    if '.nav-inner' not in content:
        content = content.replace('</style>', NAV_CSS + '\n</style>')
        print(f"  -> Added nav CSS")

    if 'footer{' not in content.lower().replace(' ', '') and '.footer-inner' not in content:
        content = content.replace('</style>', FOOTER_CSS + '\n</style>')
        print(f"  -> Added footer CSS")

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)

    print("CSS added to app.html.\n")


def add_css_to_app_ui():
    """Add nav and footer CSS to app-ui-mockups.html."""
    fpath = os.path.join(REPO, "app-ui-mockups.html")
    print(f"Adding CSS to app-ui-mockups.html...")

    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    if '.nav-inner' not in content:
        content = content.replace('</style>', NAV_CSS + '\n</style>')
        print(f"  -> Added nav CSS")

    if 'footer{' not in content.lower().replace(' ', '') and '.footer-inner' not in content:
        content = content.replace('</style>', FOOTER_CSS + '\n</style>')
        print(f"  -> Added footer CSS")

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)

    print("CSS added to app-ui-mockups.html.\n")


def update_index_css():
    """Update index.html nav references to match standard classes."""
    fpath = os.path.join(REPO, "index.html")
    print(f"Updating index.html CSS...")

    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if footer CSS needs to be added
    if 'footer {' not in content:
        # Add footer CSS before the responsive section
        content = content.replace('/* === RESPONSIVE === */', FOOTER_CSS + '\n\n/* === RESPONSIVE === */')
        print(f"  -> Added footer CSS")

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)

    print("index.html CSS updated.\n")


if __name__ == "__main__":
    print("=" * 60)
    print("FIXING NAV AND FOOTER ACROSS NEXUM WEBSITE")
    print("=" * 60)
    print()

    # Step 1: Fix nav and footer HTML for all files
    print("--- Step 1: Replace nav/footer HTML ---")
    fix_group_a_files()
    fix_app_html()
    fix_app_ui_mockups()
    fix_product_and_technology()
    fix_index()

    # Step 2: Add CSS to files that lack it
    print("--- Step 2: Add CSS ---")
    add_css_to_group_a()
    add_css_to_app()
    add_css_to_app_ui()
    update_index_css()

    print("=" * 60)
    print("ALL DONE!")
    print("=" * 60)
