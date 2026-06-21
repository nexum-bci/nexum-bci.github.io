#!/usr/bin/env python3
"""Nexum One — 逐念而行 投资人路演PPT (Professional Investor Grade)"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu, Cm
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn, nsmap
from pptx.oxml import parse_xml
import os, copy

# ═══════════════════════════════════════════
# DESIGN SYSTEM — Nexum Brand
# ═══════════════════════════════════════════
N  = RGBColor(0x00, 0x96, 0xF0)  # Nexum Blue
ND = RGBColor(0x00, 0x56, 0x90)  # Dark Blue
NB = RGBColor(0x0A, 0x0F, 0x1A)  # Near Black BG
W  = RGBColor(0xFF, 0xFF, 0xFF)
B  = RGBColor(0x15, 0x1D, 0x2E)  # Card BG
G1 = RGBColor(0x94, 0xA3, 0xB8)  # Secondary text
G2 = RGBColor(0x64, 0x74, 0x8B)  # Tertiary text
G3 = RGBColor(0xF1, 0xF5, 0xF9)  # Light BG
A  = RGBColor(0x7D, 0xD3, 0xFC)  # Accent light
GL = RGBColor(0xE8, 0xF4, 0xFD)  # Highlight BG
GR = RGBColor(0x22, 0x26, 0x34)   # Dark card

WH = Inches(13.333)
HH = Inches(7.5)
MG = Inches(0.65)  # margin
DOCS = os.path.dirname(os.path.abspath(__file__)) + '/docs'

prs = Presentation()
prs.slide_width = WH; prs.slide_height = HH
BLANK = prs.slide_layouts[6]  # blank layout

# ═══════════════════════════════════════════
# UTILITY FUNCTIONS
# ═══════════════════════════════════════════
def tb(slide, l, t, w, h):
    """Add textbox, return textframe"""
    box = slide.shapes.add_textbox(l, t, w, h)
    tf = box.text_frame; tf.word_wrap = True
    return tf

def p_add(tf, text, size=Pt(13), color=G1, bold=False, align=PP_ALIGN.LEFT, name='Arial', space_after=Pt(6), space_before=Pt(0), first=False):
    """Add paragraph to textframe. If first=True, use first paragraph."""
    if first:
        p = tf.paragraphs[0]
    else:
        p = tf.add_paragraph()
    p.text = text
    p.font.size = size; p.font.color.rgb = color; p.font.bold = bold
    p.font.name = name; p.alignment = align
    p.space_after = space_after; p.space_before = space_before
    return p

def text(slide, l, t, w, h, text, size=Pt(13), color=G1, bold=False, align=PP_ALIGN.LEFT):
    """Simple single-paragraph text"""
    tff = tb(slide, l, t, w, h)
    p_add(tff, text, size, color, bold, align, first=True)
    return tff

def rect(slide, l, t, w, h, color, radius=None):
    """Add filled rectangle, optionally rounded"""
    if radius:
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, l, t, w, h)
        shape.adjustments[0] = radius
    else:
        shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, l, t, w, h)
    shape.fill.solid(); shape.fill.fore_color.rgb = color; shape.line.fill.background()
    return shape

def gradient(slide, l, t, w, h, c1, c2, angle=90.0):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, l, t, w, h)
    shape.line.fill.background()
    f = shape.fill; f.gradient(); f.gradient_angle = angle
    f.gradient_stops[0].color.rgb = c1; f.gradient_stops[1].color.rgb = c2
    return shape

def line(slide, l, t, w, color, thickness=Pt(2)):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, l, t, w, thickness)
    shape.fill.solid(); shape.fill.fore_color.rgb = color; shape.line.fill.background()
    return shape

def circle(slide, l, t, d, color):
    shape = slide.shapes.add_shape(MSO_SHAPE.OVAL, l, t, d, d)
    shape.fill.solid(); shape.fill.fore_color.rgb = color; shape.line.fill.background()
    return shape

def img(slide, path, l, t, w, h=None):
    if h and os.path.exists(path) and os.path.getsize(path) > 1000:
        slide.shapes.add_picture(path, l, t, w, h)
        return True
    return False

def card(slide, l, t, w, h, bg=B, accent=N, accent_top=True):
    """Standard card with optional accent bar"""
    r = rect(slide, l, t, w, h, bg, radius=0.03)
    if accent and accent_top:
        line(slide, l, t, w, accent, Pt(3))
    return r

def metric_card(slide, l, t, w, h, value, label):
    card(slide, l, t, w, h, B)
    text(slide, l+Inches(0.15), t+Inches(0.15), w-Inches(0.3), Inches(0.6), value, Pt(28), N, bold=True, align=PP_ALIGN.CENTER)
    text(slide, l+Inches(0.15), t+Inches(0.85), w-Inches(0.3), Inches(0.5), label, Pt(9), G1, align=PP_ALIGN.CENTER)

def table(slide, l, t, w, h, headers, rows, col_widths, header_bg=N, font_size=Pt(9)):
    """Professional table"""
    n_rows = len(rows) + 1; n_cols = len(headers)
    tbl_shape = slide.shapes.add_table(n_rows, n_cols, l, t, w, h)
    tbl = tbl_shape.table
    for i, cw in enumerate(col_widths): tbl.columns[i].width = cw
    # Header
    for j, hdr in enumerate(headers):
        cell = tbl.cell(0, j); cell.text = hdr
        for p in cell.text_frame.paragraphs:
            p.font.size = Pt(10); p.font.bold = True; p.font.color.rgb = W; p.font.name = 'Inter'
        cell.fill.solid(); cell.fill.fore_color.rgb = header_bg
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
    # Data rows
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            cell = tbl.cell(i+1, j); cell.text = str(val)
            for p in cell.text_frame.paragraphs:
                p.font.size = font_size; p.font.color.rgb = G1; p.font.name = 'Inter'
            if i % 2 == 0:
                cell.fill.solid(); cell.fill.fore_color.rgb = RGBColor(0xF8, 0xFA, 0xFC)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
    return tbl

# ═══════════════════════════════════════════
# UTILITY: Rich text paragraph
# ═══════════════════════════════════════════
def rich_text(slide, l, t, w, h, segments_list):
    """segments_list = [(text, size, color, bold), ...]"""
    tff = tb(slide, l, t, w, h)
    p = tff.paragraphs[0]
    for i, seg in enumerate(segments_list):
        txt, sz, clr, bd = seg
        if i == 0:
            p.text = txt; p.font.size = sz; p.font.color.rgb = clr; p.font.bold = bd; p.font.name = 'Inter'
        else:
            run = p.add_run(); run.text = txt; run.font.size = sz; run.font.color.rgb = clr; run.font.bold = bd; run.font.name = 'Inter'
    return tff


# ═══════════════════════════════════════════
# SLIDE 1 — TITLE (Dark Hero)
# ═══════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
gradient(s, 0, 0, WH, HH, NB, RGBColor(0x00, 0x1A, 0x3A))
line(s, 0, 0, WH, N, Pt(4))
# Subtle radial glow
circle(s, Inches(4.5), Inches(-2), Inches(18), RGBColor(0x00, 0x96, 0xF0))
s.shapes[-1].fill.fore_color.rgb = N
# Make last circle semi-transparent via XML
sp = s.shapes[-1]._element
spPr = sp.find(qn('a:spPr'))
if spPr is not None:
    sf = spPr.find(qn('a:solidFill'))
    if sf is not None:
        srgb = sf.find(qn('a:srgbClr'))
        if srgb is not None:
            alpha_elem = parse_xml(f'<a:alpha val="8000" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"/>')
            srgb.append(alpha_elem)

text(s, MG, Inches(1.8), Inches(11.5), Inches(1.8), '逐念而行', Pt(60), W, bold=True)
text(s, MG, Inches(3.5), Inches(11.5), Inches(0.7), '神经重连AI系统', Pt(28), A)
line(s, MG, Inches(4.3), Inches(1.8), N, Pt(3))
text(s, MG, Inches(4.8), Inches(10), Inches(0.6), '人机共生  ·  从大脑到肌肉的AI  ·  赛道定义者', Pt(16), G1)
text(s, MG, Inches(5.5), Inches(10), Inches(0.5), '赵子睿  创始人 & CEO  |  2026年6月  |  种子轮', Pt(12), G2)
text(s, Inches(9), HH-Inches(0.5), Inches(4), Inches(0.35), 'Confidential — For Investor Use Only', Pt(8), G2, align=PP_ALIGN.RIGHT)

# ═══════════════════════════════════════════
# SLIDE 2 — PROBLEM (Dark BG)
# ═══════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
gradient(s, 0, 0, WH, HH, NB, RGBColor(0x00, 0x14, 0x28))
line(s, 0, 0, WH, N, Pt(4))

text(s, MG, Inches(0.35), Inches(3), Inches(0.4), '01', Pt(14), N, bold=True)
text(s, MG, Inches(0.7), Inches(11), Inches(0.7), '9400万人被困在神经损伤里', Pt(36), W, bold=True)
line(s, MG, Inches(1.55), Inches(1.8), N, Pt(3))

# Left: problem description
tf = tb(s, MG, Inches(1.9), Inches(8.5), Inches(4.5))
p_add(tf, '全球9400万中风幸存者，年新发1200万。其中66%存在步行功能障碍。', Pt(16), W, bold=True, first=True, space_after=Pt(16))
p_add(tf, '问题的本质：大脑还记得怎么走，但指令传不到肌肉。这不是机械问题，是神经连接问题。', Pt(14), G1, space_after=Pt(14))
p_add(tf, '现有方案二十年停滞不前：', Pt(14), N, bold=True, space_after=Pt(10))
p_add(tf, '• 外骨骼太重（12–25kg），穿戴痛苦，患者拒绝长期使用', Pt(12), G1)
p_add(tf, '• 康复机器人依赖治疗师手动调参，中国每10万人仅3.6名康复治疗师', Pt(12), G1)
p_add(tf, '• SCIRE荟萃分析（2022）：现有外骨骼 vs 传统物理治疗，"证据尚不充分"', Pt(12), G1)
p_add(tf, '• Ekso FY2025收入$12.8M，SG&A占134%，连续两年下滑——硬件差异化已触天花板', Pt(12), G1, space_after=Pt(14))
p_add(tf, '根本原因：所有竞品都在把神经损伤当成机械问题来解决。这是一个范式错误。', Pt(14), N, bold=True)

# Right: stat cards
for i, (num, label, desc) in enumerate([
    ('9400万', '全球中风幸存者', 'GBD 2021'),
    ('66%', '步行功能障碍率', 'World Stroke Org'),
    ('3.6/10万', '康复治疗师密度', '中国 vs 高收入国家10-30'),
]):
    y = Inches(2.0) + i * Inches(1.6)
    card(s, Inches(9.8), y, Inches(3.0), Inches(1.4), B)
    text(s, Inches(10.0), y+Inches(0.1), Inches(2.6), Inches(0.6), num, Pt(30), N, bold=True, align=PP_ALIGN.CENTER)
    text(s, Inches(10.0), y+Inches(0.7), Inches(2.6), Inches(0.35), label, Pt(11), W, align=PP_ALIGN.CENTER)
    text(s, Inches(10.0), y+Inches(1.05), Inches(2.6), Inches(0.25), desc, Pt(7), G2, align=PP_ALIGN.CENTER)

# ═══════════════════════════════════════════
# SLIDE 3 — SOLUTION (Dark BG)
# ═══════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
gradient(s, 0, 0, WH, HH, NB, RGBColor(0x00, 0x16, 0x30))
line(s, 0, 0, WH, N, Pt(4))

text(s, MG, Inches(0.35), Inches(3), Inches(0.35), '02', Pt(14), N, bold=True)
text(s, MG, Inches(0.7), Inches(11), Inches(0.65), 'Nexum One：从大脑到肌肉的AI', Pt(36), W, bold=True)
text(s, MG, Inches(1.35), Inches(11), Inches(0.4), '不卖硬件参数。卖的是AI对"你"的理解能力。', Pt(14), A)

# 4-step diagram
steps = [
    ('❶', '读取意图', 'EEG-Sense\n8ch干电极头带(80g)\n检测运动准备电位\n非侵入，像运动头带', True),
    ('❷', '生成策略', '个性化AI引擎\n416肌肉+206骨骼\n数字孪生+RL策略\n每患者独立模型', True),
    ('❸', '执行动作', 'NeuroSuit混合架构\n碳纤维锚定+线缆驱动\n<1.5kg, 8Nm持续\n穿戴<3分钟', True),
    ('❹', '持续进化', '传感器反馈闭环\n策略每周自适应\n联邦学习隐私保护\n越多人用AI越强', True),
]
for i, (num, title, desc, active) in enumerate(steps):
    x = MG + i * Inches(3.05)
    y = Inches(2.0)
    card(s, x, y, Inches(2.8), Inches(4.8), B if not active else RGBColor(0x1A, 0x2A, 0x42), N)
    circle(s, x+Inches(0.15), y+Inches(0.15), Inches(0.45), N)
    text(s, x+Inches(0.15), y+Inches(0.18), Inches(0.45), Inches(0.4), num, Pt(18), W, bold=True, align=PP_ALIGN.CENTER)
    text(s, x+Inches(0.15), y+Inches(0.8), Inches(2.5), Inches(0.4), title, Pt(16), W, bold=True)
    tf2 = tb(s, x+Inches(0.15), y+Inches(1.35), Inches(2.5), Inches(3.0))
    for j, line_text in enumerate(desc.split('\n')):
        p_add(tf2, line_text, Pt(10), G1, first=(j==0), space_after=Pt(2))

# Bottom quote
text(s, MG, HH-Inches(0.65), Inches(11.5), Inches(0.4), '1960年，Licklider预言"人机共生"。等了66年，2026年四个前提全部就绪——9400万人的问题从科学问题变成了工程问题。', Pt(11), A, align=PP_ALIGN.CENTER)

# ═══════════════════════════════════════════
# SLIDE 4 — WHY NOW (Light BG)
# ═══════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
rect(s, 0, 0, WH, HH, W)

text(s, MG, Inches(0.35), Inches(3), Inches(0.35), '03', Pt(14), G2, bold=True)
text(s, MG, Inches(0.7), Inches(11), Inches(0.65), '为什么是现在？四个条件同时就绪', Pt(32), B, bold=True)
line(s, MG, Inches(1.4), Inches(1.8), N, Pt(3))

conds = [
    ('非侵入BCI\n达到可用精度', 'CMU Bin He Lab 2025 Nature Comms发表非侵入EEG解码精细运动意图的突破性成果。下肢步态离散意图（走/停）已被Gwin, Wagner, Sburlea等多篇独立研究验证。中国2025年3月发布非侵入BCI医疗服务定价¥960-966/次（湖北/江苏/浙江）。', '🧠'),
    ('可穿戴硬件\n工程成熟', '学术界已验证的混合架构（碳纤维锚定+织物包裹+线缆驱动）：力传输效率>70%，总重<1.5kg。线缆驱动临床安全性经20年积累。柔性织物和轻量化材料不再是瓶颈。', '🦾'),
    ('个性化AI\n工程化条件成熟', '肌骨模型（416肌肉+206骨骼+Hill型柔顺肌腱）+ GPU并行强化学习（2048仿真世界，日产53亿步态样本，零人工标注）。"为每个患者生成专属康复策略"从学术论文变为可部署软件。', '🧬'),
    ('政策框架\n全面到位', '中国2025年脑机接口列入国家未来产业、写入政府工作报告。美国Medicare 2024年建立个人外骨骼支付标准$91,032/台。日本HAL纳入医保。德国裁定扩大外骨骼覆盖。中美日德已建立支付框架。', '⚖️'),
]
for i, (title, desc, icon) in enumerate(conds):
    x = MG + i * Inches(3.05)
    y = Inches(1.8)
    card(s, x, y, Inches(2.8), Inches(5.0), G3, N)
    text(s, x+Inches(0.15), y+Inches(0.1), Inches(2.5), Inches(0.3), icon, Pt(24), align=PP_ALIGN.CENTER)
    text(s, x+Inches(0.15), y+Inches(0.6), Inches(2.5), Inches(0.55), title, Pt(13), B, bold=True, align=PP_ALIGN.CENTER)
    line(s, x+Inches(0.7), y+Inches(1.25), Inches(1.1), N, Pt(1))
    tf3 = tb(s, x+Inches(0.1), y+Inches(1.4), Inches(2.6), Inches(3.3))
    p_add(tf3, desc, Pt(9), G2, first=True)

text(s, MG, HH-Inches(0.65), Inches(11.5), Inches(0.4), '这四个条件——感知精度、硬件成熟度、AI工程化、政策框架——缺任何一个，人机共生都是科幻。2026年，四个条件全部就绪。', Pt(12), N, bold=True, align=PP_ALIGN.CENTER)

# ═══════════════════════════════════════════
# SLIDE 5 — PRODUCT (Dark BG)
# ═══════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
gradient(s, 0, 0, WH, HH, NB, RGBColor(0x00, 0x18, 0x34))

text(s, MG, Inches(0.35), Inches(3), Inches(0.35), '04', Pt(14), N, bold=True)
text(s, MG, Inches(0.7), Inches(11), Inches(0.65), 'Nexum One：首款神经重连AI系统', Pt(36), W, bold=True)

modules = [
    ('EEG-Sense 头带', '8通道干电极 · 80g\nBLE 5.0 · ADS1299\n250SPS · 24-bit\n外观像运动头带', 'ppt_render_2_headband.png'),
    ('NeuroSuit 穿戴界面', '碳纤维锚定\n鲍登线缆驱动\n<1.5kg 总重\n8Nm持续 / 15Nm峰值', 'ppt_render_3_suit.png'),
    ('Nexum One 完整系统', 'EEG头带 + NeuroSuit\n+ 控制盒 + App\nClinical $18,000\nHome $3,999+$499/年', 'ppt_render_1_system.png'),
]
for i, (name, spec, rpath) in enumerate(modules):
    x = MG + i * Inches(4.05)
    y = Inches(1.6)
    card(s, x, y, Inches(3.8), Inches(4.2), B, N)
    if not img(s, f'{DOCS}/{rpath}', x+Inches(0.15), y+Inches(0.15), Inches(3.5), Inches(2.0)):
        rect(s, x+Inches(0.15), y+Inches(0.15), Inches(3.5), Inches(2.0), GR)
        text(s, x+Inches(0.3), y+Inches(0.9), Inches(3.2), Inches(0.4), name, Pt(14), G2, align=PP_ALIGN.CENTER)
    text(s, x+Inches(0.15), y+Inches(2.35), Inches(3.5), Inches(0.4), name, Pt(15), W, bold=True, align=PP_ALIGN.CENTER)
    line(s, x+Inches(0.8), y+Inches(2.85), Inches(2.2), N, Pt(1))
    text(s, x+Inches(0.15), y+Inches(3.0), Inches(3.5), Inches(1.1), spec, Pt(10), G1, align=PP_ALIGN.CENTER)

# Specs bar at bottom
specs_bar = [('8ch', '干电极'), ('80g', '头带重量'), ('<1.5kg', '系统总重'), ('<185ms', '端到端延迟'), ('8/15Nm', '持续/峰值扭矩'), ('48Wh', '电池续航>4h')]
for i, (val, label) in enumerate(specs_bar):
    x = MG + i * Inches(2.0)
    text(s, x, Inches(6.1), Inches(1.8), Inches(0.4), val, Pt(20), N, bold=True, align=PP_ALIGN.CENTER)
    text(s, x, Inches(6.5), Inches(1.8), Inches(0.3), label, Pt(9), G2, align=PP_ALIGN.CENTER)

text(s, MG, Inches(7.05), Inches(11.5), Inches(0.35), '同一套AI系统，两个版本，一条数据链：Clinical版$18K（医院）+ Home版$3,999+$499/年（家用）——数据不中断', Pt(11), A, align=PP_ALIGN.CENTER)

# ═══════════════════════════════════════════
# SLIDE 6 — MARKET (Light BG)
# ═══════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
rect(s, 0, 0, WH, HH, W)

text(s, MG, Inches(0.35), Inches(3), Inches(0.35), '05', Pt(14), G2, bold=True)
text(s, MG, Inches(0.7), Inches(11), Inches(0.65), '市场：TAM随每阶段指数级扩大', Pt(32), B, bold=True)
line(s, MG, Inches(1.4), Inches(1.8), N, Pt(3))

phases = [
    ('Phase 1  2028–2030', '$6.6B', '全球神经康复', '9400万中风×66%障碍×30%适配\n×5%渗透×$3,999 + 8000家医院\n×10%×$18K\n\n中国院内首轮TAM $43-65M\n程天已验证: 800+医院, 92万人次'),
    ('Phase 2  2030–2033', '$15B', '全球老年行动力', '中国3亿60+人口(国家统计局2025)\n×20%肌少症×3%渗透×¥5,000\n+美日欧老龄化市场\n(日本29% 65+, 欧盟21% 65+)'),
    ('Phase 3  2033+', '$33.7B+', '全人群行动增强', '全球可穿戴外骨骼市场$33.7B\nCAGR 32% (Research & Markets)\n户外/通勤/职业防护\n人机共生新品类: 增量远超已有\n市场报告(如手机>>手机+MP3)'),
]
for i, (phase, tam, title, desc) in enumerate(phases):
    x = MG + i * Inches(4.05)
    bg_c = G3 if i < 2 else GL
    card(s, x, Inches(1.8), Inches(3.8), Inches(5.0), bg_c, N)
    text(s, x+Inches(0.15), Inches(1.9), Inches(3.5), Inches(0.55), phase, Pt(11), G1, bold=True, align=PP_ALIGN.CENTER)
    text(s, x+Inches(0.15), Inches(2.5), Inches(3.5), Inches(0.7), tam, Pt(44), N, bold=True, align=PP_ALIGN.CENTER)
    line(s, x+Inches(0.7), Inches(3.3), Inches(2.4), N, Pt(1))
    text(s, x+Inches(0.15), Inches(3.4), Inches(3.5), Inches(0.4), title, Pt(14), B, bold=True, align=PP_ALIGN.CENTER)
    tf3 = tb(s, x+Inches(0.15), Inches(3.9), Inches(3.5), Inches(2.7))
    p_add(tf3, desc, Pt(9), G2, first=True)

# Bottom context bar
rect(s, MG, Inches(7.0), Inches(11.5), Inches(0.4), G3)
text(s, MG, Inches(7.05), Inches(5.7), Inches(0.3), '已有市场: BCI $2.4B(15% CAGR) + 康复机器人 $1.8B(22%) + 外骨骼 $33.7B(32%)', Pt(10), N, bold=True)
text(s, Inches(7), Inches(7.05), Inches(5.7), Inches(0.3), '全球支付: Medicare $91,032/台 · 中国BCI ¥960-966/次 · 日本医保 · 德国裁定', Pt(10), G2, align=PP_ALIGN.RIGHT)

# ═══════════════════════════════════════════
# SLIDE 7 — TECHNOLOGY (Dark BG)
# ═══════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
gradient(s, 0, 0, WH, HH, NB, RGBColor(0x00, 0x14, 0x28))

text(s, MG, Inches(0.35), Inches(3), Inches(0.35), '06', Pt(14), N, bold=True)
text(s, MG, Inches(0.7), Inches(11), Inches(0.65), '技术架构：AI驱动的神经重连闭环', Pt(32), W, bold=True)
text(s, MG, Inches(1.35), Inches(11), Inches(0.4), '四层架构，每层技术均已独立验证。逐念而行的贡献是把它们整合成完整的AI系统。', Pt(13), G1)

layers = [
    ('感知层', 'EEG + sEMG 双模态神经接口', 'N',
     'EEG-Sense: 8ch干电极，检测运动准备电位(MRCP)\nCMU Bin He 2025 Nature Comms验证非侵入EEG解码可行性\nsEMG: 多通道织物电极，<100ms精细力矩解码\n三级降级安全: EEG+sEMG → sEMG+IMU → 无助力被动支撑'),
    ('决策层', '个性化AI引擎', 'N',
     'DL提取EEG特征(CNN/TCN) → MSK数字孪生(416肌肉+206骨骼+Hill肌腱)\n→ 2048仿真世界并行RL训练 → 日产53亿步态 → 每患者独立策略\n→ 传统控制(PID/MPC)毫秒级安全执行\n本周策略与上周不同——因为这个患者的身体已经不同'),
    ('执行层', '混合式机械架构', 'N',
     '碳纤维髋部锚定 → 力传输效率>70%\n鲍登线缆驱动 → 电机位于腰部(重心附近)，关节处仅轻量锚点\n标准化关节电机 → 扭矩密度40-50Nm/kg，双电机+驱动器+线缆<1.5kg\n织物包裹穿戴界面 → 外观像压缩裤，解决穿戴耻感'),
    ('进化层', '联邦学习数据飞轮', 'A',
     '原始生理信号本地处理 → 仅脱敏模型改善数据上传\n联邦学习架构(pFedAC) → 隐私保护\n每多一个患者使用 → AI就更理解人 → 产品更强\n这是硬件公司无法复制的数据网络效应'),
]
for i, (label, title, accent_color, desc) in enumerate(layers):
    y = Inches(1.9) + i * Inches(1.35)
    accent_clr = N if accent_color == 'N' else A
    card(s, MG, y, Inches(2.0), Inches(1.2), B, accent_clr)
    text(s, MG+Inches(0.15), y+Inches(0.08), Inches(1.7), Inches(0.3), label, Pt(14), accent_clr, bold=True)
    text(s, MG+Inches(0.15), y+Inches(0.4), Inches(1.7), Inches(0.5), title, Pt(9), W, bold=True)

    text(s, Inches(2.9), y+Inches(0.1), Inches(9.8), Inches(1.1), desc, Pt(10), G1)

# ═══════════════════════════════════════════
# SLIDE 8 — COMPETITION (Light BG)
# ═══════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
rect(s, 0, 0, WH, HH, W)

text(s, MG, Inches(0.35), Inches(3), Inches(0.35), '07', Pt(14), G2, bold=True)
text(s, MG, Inches(0.7), Inches(11), Inches(0.65), '竞争：我们在AI理解人的维度上', Pt(32), B, bold=True)
line(s, MG, Inches(1.4), Inches(1.8), N, Pt(3))

headers = ['竞争维度', '逐念而行 Nexum', 'Ekso / ReWalk', 'HAL (Cyberdyne)', '程天科技 UGO']
rows = [
    ['EEG运动意图解码', '✅ 8ch干电极', '❌', '❌ (仅EMG)', '✅ 多模态融合'],
    ['sEMG神经接口', '✅ 织物电极', '❌', '✅', '✅'],
    ['EEG+sEMG双模态融合', '✅ 独家', '❌', '❌', '❌'],
    ['MSK数字孪生建模', '✅ 416肌肉+Hill肌腱', '❌', '❌', '❌'],
    ['RL个性化康复策略', '✅ 每患者独立策略', '❌', '❌', '❌'],
    ['联邦学习隐私保护', '✅ pFedAC架构', '❌', '❌', '❌'],
    ['产品价格', '$18K / $3,999', '$75K–100K', '$60K–80K', '¥10万+(医院)'],
    ['核心定位', 'AI公司', '硬件公司', '硬件公司', '硬件集成'],
]
col_w = [Inches(2.5), Inches(2.6), Inches(2.1), Inches(2.1), Inches(2.2)]
table(s, MG, Inches(1.7), Inches(11.5), Inches(4.3), headers, rows, col_w, N, Pt(8.5))

# Key insight
card(s, MG, Inches(6.3), Inches(11.5), Inches(1.0), GL, N)
text(s, MG+Inches(0.2), Inches(6.4), Inches(11.1), Inches(0.8),
     '核心差异：Ekso/ReWalk/HAL卖硬件参数——第一万台和第一台没有本质区别。逐念而行卖AI对人的理解——每多一个患者，AI就更强一分。范式竞争，不是参数竞争。',
     Pt(11), B, bold=True)

# ═══════════════════════════════════════════
# SLIDE 9 — FINANCIALS (Dark BG)
# ═══════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
gradient(s, 0, 0, WH, HH, NB, RGBColor(0x00, 0x18, 0x34))

text(s, MG, Inches(0.35), Inches(3), Inches(0.35), '08', Pt(14), N, bold=True)
text(s, MG, Inches(0.7), Inches(11), Inches(0.65), '商业模式与五年财务预测', Pt(32), W, bold=True)

# Revenue table
fin_headers = ['', '2027', '2028', '2029', '2030', '2031']
fin_rows = [
    ['Clinical交付(台)', '—（预临床）', '150×$16K', '400×$15K', '1,000×$14K', '2,500×$13K'],
    ['Home交付(台)', '—', '100×$4K', '500×$3.8K', '2,000×$3.5K', '8,000×$3.2K'],
    ['总收入', '$0', '$2.8M', '$7.9M', '$21.0M', '$58.1M'],
    ['毛利率', '—', '52%', '58%', '63%', '68%'],
    ['净利润', '-$2.5M', '-$2.0M', '-$0.5M', '$3.0M', '$15.0M'],
]
fin_col_w = [Inches(2.5), Inches(1.7), Inches(2.0), Inches(2.0), Inches(2.0), Inches(2.3)]
table(s, MG, Inches(1.5), Inches(12.1), Inches(2.8), fin_headers, fin_rows, fin_col_w, N, Pt(9))

# Right: key metrics
bx = MG; by = Inches(4.6)
for i, (label, val) in enumerate([
    ('盈亏平衡点', '~700台/年 (2029 Q4–2030 Q1)'),
    ('Home版BOM成本', '¥2,980 (量产@100台) → ¥2,080 (@1000台)'),
    ('Clinical版BOM成本', '¥3,280 (量产@100台) → ¥2,280 (@1000台)'),
    ('S&M占比', '30% (vs 竞品40–70%，因差异化在软件)'),
    ('Home订阅收入(额外)', '2031年8,000台×50%续订×$499 = +$2M高毛利'),
]):
    text(s, bx + i%2 * Inches(6.2), by + i//2 * Inches(0.65), Inches(6.0), Inches(0.55), f'{label}: {val}', Pt(10), G1)

# ═══════════════════════════════════════════
# SLIDE 10 — TEAM (Dark BG)
# ═══════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
gradient(s, 0, 0, WH, HH, NB, RGBColor(0x00, 0x14, 0x28))

text(s, MG, Inches(0.35), Inches(3), Inches(0.35), '09', Pt(14), N, bold=True)
text(s, MG, Inches(0.7), Inches(11), Inches(0.65), '团队：六人核心', Pt(32), W, bold=True)
text(s, MG, Inches(1.35), Inches(11), Inches(0.4), '优先级：临床决定NMPA · EEG决定量产 · 注册决定审评速度 · 设计决定用户留存', Pt(12), A)

team = [
    ('赵子睿', '创始人 & CEO\n产品/架构/技术方向', 'Columbia EE MSc (ML)\n华为美国研究院Futurewei IoT Lab\n欣网/智擎CTO 8年\nFAI患者——产品原动力', True),
    ('汪牧星', '算法\n联邦学习', 'NEU PhD Candidate\nEdinburgh MSc Distinction\npFedAC第一作者', True),
    ('临床负责人', '招募中\n优先级最高', '康复医学主任医师\n临床试验设计\nNMPA方案撰写', False),
    ('EEG硬件负责人', '招募中', '脑电采集系统设计\nTI ADS1299经验\n干电极优化+产品化', False),
    ('NMPA注册负责人', '招募中', '二类创新器械注册\nISO 13485体系\n创新器械申报', False),
    ('产品设计师', '招募中', '可穿戴设备工业设计\n用户体验\n穿戴体验=留存关键', False),
]
for i, (name, role, bio, active) in enumerate(team):
    x = MG + i * Inches(2.05)
    card(s, x, Inches(1.8), Inches(1.85), Inches(3.6), B if active else GR, N if active else G2)
    circle(s, x+Inches(0.6), Inches(1.9), Inches(0.6), N if active else G2)
    text(s, x+Inches(0.62), Inches(1.95), Inches(0.56), Inches(0.4), name[0], Pt(18), W, bold=True, align=PP_ALIGN.CENTER)
    text(s, x+Inches(0.1), Inches(2.6), Inches(1.65), Inches(0.45), name, Pt(15), W if active else G1, bold=True, align=PP_ALIGN.CENTER)
    text(s, x+Inches(0.1), Inches(3.1), Inches(1.65), Inches(0.6), role, Pt(8), N if active else G2, align=PP_ALIGN.CENTER)
    text(s, x+Inches(0.1), Inches(3.8), Inches(1.65), Inches(1.4), bio, Pt(7), G1 if active else G2, align=PP_ALIGN.CENTER)

# Academic
text(s, MG, Inches(5.7), Inches(11.5), Inches(0.35), '学术合作', Pt(13), A, bold=True)
text(s, MG, Inches(6.15), Inches(11.5), Inches(0.3), 'CMU Bin He Lab (非侵入EEG运动解码) · NEU NeuMove Lab (肌骨仿真) · 清华/浙大/西湖大学 (BCI与神经工程)', Pt(9), G1)
text(s, MG, Inches(6.5), Inches(11.5), Inches(0.3), '杨朋昆 (清华统计系副教授, pFedAC共同作者) · 苏丽丽 (NEU助理教授, NSF CAREER, 联邦学习)', Pt(9), G1)

# ═══════════════════════════════════════════
# SLIDE 11 — FUNDING (Light BG)
# ═══════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
rect(s, 0, 0, WH, HH, W)

text(s, MG, Inches(0.35), Inches(3), Inches(0.35), '10', Pt(14), G2, bold=True)
text(s, MG, Inches(0.7), Inches(11), Inches(0.65), '融资路线：每轮对应可验证里程碑', Pt(32), B, bold=True)
line(s, MG, Inches(1.4), Inches(1.8), N, Pt(3))

rounds = [
    ('种子轮', '2026 Q3', '¥800万',
     '原型2台(¥200万) + 团队8人12月(¥300万)\n+ 预临床启动(¥200万) + 运营储备(¥100万)',
     '可演示原型 · 3家医院预临床协议 · NMPA分类界定申请', False),
    ('天使轮', '2027 Q1', '¥2,500万',
     '10台样机(¥500万) + 团队12人18月(¥800万)\n+ 30例预临床(¥600万) + NMPA申报(¥300万)\n+ 运营储备(¥300万)',
     '预临床数据发表 · NMPA创新器械正式受理', False),
    ('Pre-A', '2028 Q1', '$7M (≈¥5,000万)',
     '量产备货(¥2,000万) + 50家医院渠道(¥1,500万)\n+ Home版发布(¥1,000万) + 团队30人(¥500万)',
     'NMPA获批 · 首批商业化交付 · 年收入$2.8M', False),
    ('A轮', '2029 H2', '$20M',
     'FDA 510(k) + CE申报 + 海外渠道建设\n+ 规模化生产 + 团队50人',
     '海外准入 · 年销过千台 · 盈亏平衡', True),
]
for i, (name, time, amount, use, milestone, is_last) in enumerate(rounds):
    x = MG + i * Inches(3.05)
    bg_c = GL if is_last else G3
    card(s, x, Inches(1.8), Inches(2.8), Inches(5.0), bg_c, N)
    text(s, x+Inches(0.15), Inches(1.9), Inches(2.5), Inches(0.35), name, Pt(18), N, bold=True)
    text(s, x+Inches(0.15), Inches(2.3), Inches(2.5), Inches(0.3), time, Pt(10), G1)
    text(s, x+Inches(0.15), Inches(2.65), Inches(2.5), Inches(0.5), amount, Pt(28), B, bold=True)
    line(s, x+Inches(0.3), Inches(3.2), Inches(2.2), N, Pt(1))
    text(s, x+Inches(0.15), Inches(3.35), Inches(2.5), Inches(0.35), '用途', Pt(9), N, bold=True)
    text(s, x+Inches(0.15), Inches(3.7), Inches(2.5), Inches(1.4), use, Pt(8), G2)
    text(s, x+Inches(0.15), Inches(5.2), Inches(2.5), Inches(0.35), '产出', Pt(9), N, bold=True)
    milestone_bg = B if is_last else RGBColor(0xF8, 0xFA, 0xFC)
    milestone_color = A if is_last else G1
    rect(s, x+Inches(0.1), Inches(5.55), Inches(2.6), Inches(1.05), milestone_bg)
    text(s, x+Inches(0.2), Inches(5.6), Inches(2.4), Inches(0.9), milestone, Pt(8), milestone_color, bold=is_last)

text(s, MG, Inches(7.05), Inches(11.5), Inches(0.35), '当前：种子轮¥800万寻找领投方。12个月可验证的技术里程碑 → 原型可演示 → 预临床数据 → 为天使轮¥2,500万建立定价基础。', Pt(12), N, bold=True, align=PP_ALIGN.CENTER)

# ═══════════════════════════════════════════
# SLIDE 12 — VISION + CLOSE (Dark BG)
# ═══════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
gradient(s, 0, 0, WH, HH, NB, RGBColor(0x00, 0x20, 0x50))
line(s, 0, 0, WH, N, Pt(4))

text(s, MG, Inches(1.2), Inches(11.5), Inches(1.5),
     '2026年，AI从数字世界进入了物理世界。\n逐念而行专注于其中尚未被充分探索的方向——\n让AI理解人的身体，而不只是造AI的机器身体。',
     Pt(24), W, align=PP_ALIGN.CENTER)

line(s, Inches(5.5), Inches(3.2), Inches(2.3), N, Pt(2))

vision_items = [
    ('2026–2028', '定义品类', '100家医院 · 30例预临床 → 200例上市后研究\n临床论文 → 进入康复指南\n让"人机共生"出现在顶级期刊和政策文件中'),
    ('2029–2030', '品类扩展', '医院→家庭闭环 · 从神经重连到通用意图驱动助力\n中国3亿60+老人，老年行动力市场\n启动FDA + CE，海外准入'),
    ('2031+', '成为基础设施', '百万用户 · 从修复到增强\n户外运动 · 都市通勤 · 职业防护\n人机共生像智能手机一样成为日常生活一部分'),
]
for i, (year, title, desc) in enumerate(vision_items):
    y = Inches(3.6) + i * Inches(1.15)
    text(s, MG+Inches(0.5), y, Inches(2.0), Inches(0.4), year, Pt(16), N, bold=True)
    text(s, MG+Inches(2.5), y, Inches(2.0), Inches(0.4), title, Pt(16), W, bold=True)
    text(s, MG+Inches(5.0), y, Inches(7.0), Inches(0.9), desc, Pt(10), G1)

# Contact card
y = Inches(6.25)
rect(s, Inches(2.5), y, Inches(8.3), Inches(0.95), B)
text(s, Inches(2.7), y+Inches(0.1), Inches(7.9), Inches(0.35), '逐念而行 · Nexum  |  人机共生赛道定义者', Pt(18), W, bold=True, align=PP_ALIGN.CENTER)
text(s, Inches(2.7), y+Inches(0.55), Inches(7.9), Inches(0.3), '赵子睿  ·  zirui@nexum.ai  ·  Columbia EE MSc  ·  种子轮 ¥800万', Pt(11), A, align=PP_ALIGN.CENTER)

# ═══════════════════════════════════════════
# SAVE
# ═══════════════════════════════════════════
output = f'{DOCS}/Nexum_Pitch_Deck.pptx'
prs.save(output)
print(f'✅ PPTX saved: {output}')
print(f'📊 Size: {os.path.getsize(output)/1024:.0f} KB  |  Slides: {len(prs.slides)}')
