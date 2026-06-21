#!/usr/bin/env python3
"""Convert Nexum One markdown docs to styled HTML pages."""

import markdown
import re
import os

DOCS_DIR = "/Users/ziruizhao/Desktop/EXO/repos/nexum/docs"

CONFIG = [
    {
        "md": "Nexum_One_Engineering_Architecture_v0.1.md",
        "html": "Nexum_One_Engineering_Architecture.html",
        "title": "Nexum One — Engineering Architecture v0.1",
    },
    {
        "md": "Nexum_One_PRD_v1.0.md",
        "html": "Nexum_One_PRD.html",
        "title": "Nexum One — Product Requirements Document v1.0",
    },
    {
        "md": "Nexum_One_Production_BOM_v0.1.md",
        "html": "Nexum_One_Production_BOM.html",
        "title": "Nexum One — Production BOM & Supplier Guide v0.1",
    },
    {
        "md": "Nexum_One_Clinical_Protocol_v0.1.md",
        "html": "Nexum_One_Clinical_Protocol.html",
        "title": "Nexum One — Clinical Protocol v0.1",
    },
    {
        "md": "Nexum_One_Regulatory_Strategy_v0.1.md",
        "html": "Nexum_One_Regulatory_Strategy.html",
        "title": "Nexum One — NMPA Regulatory Strategy v0.1",
    },
]

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

*, *::before, *::after {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

html {{
    scroll-behavior: smooth;
}}

body {{
    font-family: 'Inter', 'PingFang SC', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Noto Sans SC', 'Microsoft YaHei', sans-serif;
    background: #0a0f1a;
    color: #e5e7eb;
    font-size: 16px;
    line-height: 1.8;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}}

/* Nav */
.navbar {{
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 56px;
    background: rgba(10, 15, 26, 0.92);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-bottom: 1px solid rgba(0, 150, 240, 0.15);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 24px;
    z-index: 1000;
}}

.navbar .logo {{
    font-size: 18px;
    font-weight: 700;
    color: #0096f0;
    text-decoration: none;
    letter-spacing: 0.5px;
    display: flex;
    align-items: center;
    gap: 10px;
}}

.navbar .logo::before {{
    content: '';
    display: inline-block;
    width: 24px;
    height: 24px;
    background: linear-gradient(135deg, #0096f0, #00d4ff);
    border-radius: 6px;
}}

.navbar .nav-link {{
    font-size: 14px;
    color: #94a3b8;
    text-decoration: none;
    padding: 6px 14px;
    border-radius: 6px;
    transition: all 0.2s;
    border: 1px solid rgba(0, 150, 240, 0.2);
    font-weight: 500;
}}

.navbar .nav-link:hover {{
    background: rgba(0, 150, 240, 0.1);
    color: #0096f0;
    border-color: rgba(0, 150, 240, 0.4);
}}

/* Main content */
.container {{
    max-width: 960px;
    margin: 0 auto;
    padding: 80px 32px 40px;
}}

/* Typography */
h1, h2, h3, h4, h5, h6 {{
    color: #f1f5f9;
    font-weight: 600;
    line-height: 1.4;
    margin-top: 2em;
    margin-bottom: 0.6em;
    letter-spacing: -0.01em;
}}

h1 {{
    font-size: 2.2em;
    font-weight: 800;
    margin-top: 0.5em;
    margin-bottom: 0.3em;
    background: linear-gradient(135deg, #f1f5f9 0%, #94a3b8 60%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.02em;
}}

h2 {{
    font-size: 1.5em;
    font-weight: 700;
    padding-bottom: 0.3em;
    border-bottom: 1px solid rgba(0, 150, 240, 0.2);
    color: #0096f0;
    margin-top: 2.5em;
}}

h3 {{
    font-size: 1.2em;
    font-weight: 600;
    color: #e2e8f0;
    margin-top: 1.8em;
}}

h4 {{
    font-size: 1.05em;
    font-weight: 600;
    color: #cbd5e1;
    margin-top: 1.5em;
}}

p {{
    margin-bottom: 1em;
    color: #e5e7eb;
}}

a {{
    color: #0096f0;
    text-decoration: none;
    transition: color 0.2s;
}}

a:hover {{
    color: #00b4ff;
    text-decoration: underline;
}}

strong {{
    color: #f1f5f9;
    font-weight: 600;
}}

em {{
    color: #94a3b8;
    font-style: italic;
}}

/* Horizontal rule */
hr {{
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0, 150, 240, 0.3), transparent);
    margin: 2.5em 0;
}}

/* Code blocks */
pre {{
    background: #0d1525;
    border: 1px solid rgba(0, 150, 240, 0.12);
    border-radius: 10px;
    padding: 20px 24px;
    overflow-x: auto;
    margin: 1.2em 0;
    font-size: 13.5px;
    line-height: 1.6;
    position: relative;
}}

code {{
    font-family: 'JetBrains Mono', 'SF Mono', 'Fira Code', Consolas, monospace;
    font-size: 0.92em;
    background: rgba(0, 150, 240, 0.08);
    color: #7dd3fc;
    padding: 2px 6px;
    border-radius: 4px;
}}

pre code {{
    background: none;
    padding: 0;
    border-radius: 0;
    color: #e2e8f0;
    font-size: 13.5px;
}}

/* Blockquotes */
blockquote {{
    border-left: 4px solid #0096f0;
    background: rgba(0, 150, 240, 0.04);
    padding: 12px 20px;
    margin: 1.2em 0;
    border-radius: 0 8px 8px 0;
    color: #94a3b8;
}}

blockquote p {{
    margin-bottom: 0.3em;
    color: #94a3b8;
}}

blockquote strong {{
    color: #cbd5e1;
}}

/* Lists */
ul, ol {{
    padding-left: 1.5em;
    margin-bottom: 1em;
}}

li {{
    margin-bottom: 0.4em;
}}

li > ul, li > ol {{
    margin-top: 0.3em;
    margin-bottom: 0.3em;
}}

/* Tables */
.table-wrapper {{
    overflow-x: auto;
    margin: 1.2em 0;
    border-radius: 10px;
    border: 1px solid rgba(0, 150, 240, 0.1);
}}

table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 14px;
    line-height: 1.6;
}}

thead {{
    background: linear-gradient(135deg, rgba(0, 150, 240, 0.15), rgba(0, 150, 240, 0.08));
}}

th {{
    color: #0096f0;
    font-weight: 600;
    text-align: left;
    padding: 12px 16px;
    border-bottom: 1px solid rgba(0, 150, 240, 0.2);
    font-size: 13.5px;
    letter-spacing: 0.03em;
    white-space: nowrap;
}}

td {{
    padding: 10px 16px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.04);
    color: #e5e7eb;
    vertical-align: top;
}}

tbody tr:nth-child(odd) {{
    background: rgba(255, 255, 255, 0.015);
}}

tbody tr:nth-child(even) {{
    background: rgba(0, 150, 240, 0.025);
}}

tbody tr:hover {{
    background: rgba(0, 150, 240, 0.06);
}}

/* Sub / sup for footnotes */
sub, sup {{
    font-size: 0.75em;
}}

/* Footnotes / meta text */
.meta {{
    color: #94a3b8;
    font-size: 14px;
    margin-bottom: 0.5em;
}}

/* Alert / note boxes */
.alert {{
    background: rgba(0, 150, 240, 0.06);
    border: 1px solid rgba(0, 150, 240, 0.15);
    border-radius: 8px;
    padding: 16px 20px;
    margin: 1.2em 0;
    color: #94a3b8;
}}

/* Footer */
.footer {{
    text-align: center;
    padding: 32px 24px;
    margin-top: 48px;
    color: #475569;
    font-size: 13px;
    border-top: 1px solid rgba(255, 255, 255, 0.05);
    letter-spacing: 1px;
}}

.footer span {{
    color: #0096f0;
}}

/* Print styles */
@media print {{
    body {{
        background: #fff;
        color: #1a1a2e;
        font-size: 12pt;
    }}
    .navbar {{
        display: none;
    }}
    .container {{
        max-width: 100%;
        padding: 20px;
    }}
    h1, h2, h3, h4 {{
        color: #1a1a2e;
    }}
    h1 {{
        -webkit-text-fill-color: #1a1a2e;
        background: none;
    }}
    h2 {{
        color: #005fa3;
        border-bottom-color: rgba(0, 0, 0, 0.1);
    }}
    a {{
        color: #005fa3;
    }}
    pre {{
        background: #f5f5f5;
        border-color: #ddd;
    }}
    pre code {{
        color: #333;
    }}
    code {{
        background: #f0f0f0;
        color: #333;
    }}
    blockquote {{
        border-left-color: #005fa3;
        background: #f8f8f8;
        color: #555;
    }}
    table {{
        font-size: 10pt;
    }}
    th {{
        color: #005fa3;
        background: #e8f0f8;
    }}
    tbody tr:nth-child(odd) {{
        background: #fafafa;
    }}
    tbody tr:nth-child(even) {{
        background: #f0f5fa;
    }}
    .footer {{
        color: #999;
        border-top-color: #ddd;
    }}
    .table-wrapper {{
        border-color: #ddd;
    }}
    hr {{
        background: #ddd;
    }}
}}

/* Responsive */
@media (max-width: 768px) {{
    .container {{
        padding: 72px 16px 32px;
    }}
    h1 {{ font-size: 1.6em; }}
    h2 {{ font-size: 1.3em; }}
    h3 {{ font-size: 1.1em; }}
    table {{ font-size: 13px; }}
    th, td {{ padding: 8px 10px; }}
    pre {{ padding: 14px 16px; font-size: 12.5px; }}
}}
</style>
</head>
<body>
<nav class="navbar">
    <a href="../index.html" class="logo">Nexum One</a>
    <a href="../index.html" class="nav-link">Portal</a>
</nav>
<div class="container">
{content}
<div class="footer">逐念而行 &middot; Nexum One &middot; Confidential</div>
</div>
</body>
</html>"""

# Extensions for markdown conversion
MD_EXTENSIONS = [
    'tables',
    'fenced_code',
    'codehilite',
    'nl2br',
    'sane_lists',
]

def convert_table_delimiters(content):
    """Fix markdown tables that use === separators."""
    lines = content.split('\n')
    result = []
    in_table = False
    for line in lines:
        result.append(line)
    return '\n'.join(result)

def post_process_tables(html):
    """Wrap tables in a div for horizontal scrolling."""
    html = re.sub(
        r'<table>',
        '<div class="table-wrapper"><table>',
        html
    )
    html = re.sub(
        r'</table>',
        '</table></div>',
        html
    )
    return html

def post_process_images(html):
    """Convert image markers in code blocks back to ascii art."""
    return html

def fix_links(html):
    """Convert .md links to .html links for internal cross-references."""
    html = re.sub(
        r'href="([^"]+)\.md"',
        lambda m: f'href="{m.group(1)}.html"',
        html
    )
    return html

def convert_md_to_html(md_content):
    """Convert markdown to HTML with proper extensions."""
    html = markdown.markdown(
        md_content,
        extensions=MD_EXTENSIONS
    )
    html = post_process_tables(html)
    html = fix_links(html)
    return html

def process_file(md_path, html_path, title):
    """Read markdown, convert to HTML, write file."""
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Check for ASCII art diagrams and protect them from markdown parsing
    # The markdown library might mess with ascii art in code blocks
    html_body = convert_md_to_html(md_content)

    full_html = HTML_TEMPLATE.format(
        title=title,
        content=html_body
    )

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(full_html)

    print(f"  -> {html_path}  ({len(full_html):,} bytes)")

def main():
    for cfg in CONFIG:
        md_path = os.path.join(DOCS_DIR, cfg["md"])
        html_path = os.path.join(DOCS_DIR, cfg["html"])
        print(f"Converting: {cfg['md']}")
        process_file(md_path, html_path, cfg["title"])

    print(f"\nDone. {len(CONFIG)} files converted.")

if __name__ == "__main__":
    main()
