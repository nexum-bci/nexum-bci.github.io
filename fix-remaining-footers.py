#!/usr/bin/env python3
"""Fix remaining footer replacements that the first script missed."""

import os
import re

REPO = "/Users/ziruizhao/Desktop/EXO/repos/nexum"

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

# These files have an inline footer with text-align:left
# The exact old footer HTML varies slightly between files
# We'll read each file, find the footer, and replace it

files_to_fix = [
    "product.html",
    "technology.html",
    "index.html",
    "clinical-protocol.html",
    "app.html",
    "app-ui-mockups.html",
]

for fname in files_to_fix:
    fpath = os.path.join(REPO, fname)
    print(f"Processing {fname}...")

    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the footer block - it starts with <footer style="border-top:...
    # And ends with </footer>
    footer_start_marker = '<footer style="border-top:1px solid var(--border);padding:64px 24px 32px;margin-top:48px;background:var(--bg-card)'
    footer_start_idx = content.find(footer_start_marker)

    if footer_start_idx < 0:
        print(f"  -> Footer not found!")
        continue

    footer_end_idx = content.find('</footer>', footer_start_idx)
    if footer_end_idx < 0:
        print(f"  -> Footer end not found!")
        continue

    old_footer = content[footer_start_idx:footer_end_idx + 9]
    print(f"  -> Found footer at {footer_start_idx}-{footer_end_idx + 9}")

    # Check if this footer is already the new one
    if 'footer-inner' in old_footer:
        print(f"  -> Already updated, skipping")
        continue

    content = content.replace(old_footer, FOOTER_HTML)

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  -> Replaced footer")

print("\nDone!")
