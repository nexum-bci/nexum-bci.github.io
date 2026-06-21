#!/usr/bin/env python3
"""Nexum One — 逐念而行 投资人路演PPT 生成脚本"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
import os

# ── Design System ──
NEXUM_BLUE  = RGBColor(0x00, 0x96, 0xF0)
DARK_BLUE   = RGBColor(0x00, 0x50, 0xA0)
DARK_BG     = RGBColor(0x0A, 0x0F, 0x1A)
WHITE       = RGBColor(0xFF, 0xFF, 0xFF)
BLACK       = RGBColor(0x11, 0x11, 0x11)
GRAY        = RGBColor(0x66, 0x66, 0x66)
LIGHT_BG    = RGBColor(0xF5, 0xF8, 0xFC)
ACCENT      = RGBColor(0x80, 0xD0, 0xFF)
DARK_CARD   = RGBColor(0x15, 0x1D, 0x2E)

W = Inches(13.333)
H = Inches(7.5)
M = Inches(0.7)
DOCS = os.path.dirname(os.path.abspath(__file__)) + '/docs'

def add_text(slide, l, t, w, h, text, size=Pt(14), color=BLACK, bold=False, align=PP_ALIGN.LEFT, font='Inter'):
    tb = slide.shapes.add_textbox(l, t, w, h)
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = text
    p.font.size = size; p.font.color.rgb = color; p.font.bold = bold; p.font.name = font; p.alignment = align
    return tf

def add_rect(slide, l, t, w, h, color, shape=MSO_SHAPE.RECTANGLE):
    s = slide.shapes.add_shape(shape, l, t, w, h)
    s.fill.solid(); s.fill.fore_color.rgb = color; s.line.fill.background()
    return s

def add_gradient(slide, l, t, w, h, c1, c2):
    s = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, l, t, w, h)
    s.line.fill.background(); f = s.fill; f.gradient(); f.gradient_angle = 90.0
    f.gradient_stops[0].color.rgb = c1; f.gradient_stops[1].color.rgb = c2
    return s

def add_img(slide, path, l, t, w, h=None):
    if h: slide.shapes.add_picture(path, l, t, w, h)
    else: slide.shapes.add_picture(path, l, t, w)

def add_rich_box(slide, l, t, w, h, lines, font_size=Pt(13), color=GRAY, line_spacing=Pt(24)):
    """lines = [(text, bold, color_override), ...]"""
    tb = slide.shapes.add_textbox(l, t, w, h)
    tf = tb.text_frame; tf.word_wrap = True
    for i, item in enumerate(lines):
        text, bold, clr = item[0], item[1] if len(item) > 1 else False, item[2] if len(item) > 2 else color
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = text; p.font.size = font_size; p.font.color.rgb = clr
        p.font.bold = bold; p.font.name = 'Inter'; p.space_after = Pt(8)
    return tf

prs = Presentation()
prs.slide_width = W; prs.slide_height = H

# ═══════════════════════════════════════════
# SLIDE 1: TITLE
# ═══════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6])
add_gradient(s, 0, 0, W, H, DARK_BG, RGBColor(0x00, 0x30, 0x60))
# Accent line top
add_rect(s, 0, 0, W, Pt(4), NEXUM_BLUE)
# Big title
add_text(s, M, Inches(1.5), Inches(11.5), Inches(1.8), '逐念而行', Pt(56), WHITE, bold=True)
add_text(s, M, Inches(3.2), Inches(11.5), Inches(0.8), '神经重连AI系统', Pt(28), ACCENT)
# Divider
add_rect(s, M, Inches(4.2), Inches(1.5), Pt(3), NEXUM_BLUE)
# Subtitle
add_text(s, M, Inches(4.6), Inches(11.5), Inches(0.7), '人机共生 · 从大脑到肌肉的AI', Pt(18), RGBColor(0xAA, 0xCC, 0xEE))
add_text(s, M, Inches(5.6), Inches(11.5), Inches(0.5), '赵子睿 · 创始人 & CEO · 2026年6月', Pt(12), GRAY)
add_text(s, Inches(9.5), Inches(6.8), Inches(3.5), Inches(0.4), 'Confidential — For Investor Use Only', Pt(8), RGBColor(0x55, 0x66, 0x77))

# ═══════════════════════════════════════════
# SLIDE 2: THE PROBLEM
# ═══════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6])
add_rect(s, 0, 0, W, Pt(4), NEXUM_BLUE)
add_text(s, M, Inches(0.3), Inches(11.5), Inches(0.6), '问题：9400万人被困在神经损伤里', Pt(28), BLACK, bold=True)
add_rect(s, M, Inches(1.1), Inches(1.5), Pt(2), NEXUM_BLUE)

add_rich_box(s, M, Inches(1.5), Inches(8.5), Inches(5.0), [
    ('全球9400万中风幸存者，年新发1200万', True, BLACK),
    ('', False, BLACK),
    ('其中66%存在步行功能障碍——大脑还记得怎么走，但指令传不到肌肉', False, GRAY),
    ('', False, BLACK),
    ('现有方案的困境：', True, BLACK),
    ('外骨骼太重（12–25kg），穿戴痛苦，患者不愿使用', False, GRAY),
    ('康复机器人依赖治疗师手动调参，中国每10万人仅3.6名康复治疗师', False, GRAY),
    ('二十年硬件迭代未带来显著临床效果提升（SCIRE荟萃分析证实）', False, GRAY),
    ('Ekso FY2025收入$12.8M，SG&A占134%，连续两年下滑——硬件差异化已到尽头', False, GRAY),
    ('', False, BLACK),
    ('根本原因：所有人都在把神经损伤当成机械问题解决', True, NEXUM_BLUE),
])

# Metric cards
for i, (num, label) in enumerate([('9400万', '全球中风\n幸存者'), ('66%', '步行功能\n障碍率'), ('3.6/10万', '中国康复\n治疗师密度')]):
    x = Inches(10.0) + i * Inches(1.1)
    add_rect(s, x, Inches(1.5), Inches(1.0), Inches(2.2), LIGHT_BG)
    add_text(s, x, Inches(1.7), Inches(1.0), Inches(1.0), num, Pt(24), NEXUM_BLUE, bold=True, align=PP_ALIGN.CENTER)
    add_text(s, x, Inches(2.8), Inches(1.0), Inches(0.8), label, Pt(8), GRAY, align=PP_ALIGN.CENTER)

# ═══════════════════════════════════════════
# SLIDE 3: SOLUTION
# ═══════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6])
add_gradient(s, 0, 0, W, H, DARK_BG, RGBColor(0x00, 0x20, 0x40))
add_text(s, M, Inches(0.5), Inches(11.5), Inches(0.8), 'Nexum One：从大脑到肌肉的AI', Pt(32), WHITE, bold=True)
add_rect(s, M, Inches(1.4), Inches(1.5), Pt(3), NEXUM_BLUE)

# 4 numbered steps
steps = [
    ('1', '读取意图', 'EEG-Sense 8通道干电极头带\n检测运动准备电位\n非侵入，像运动头带'),
    ('2', '生成策略', '个性化AI引擎\n416肌肉+206骨骼数字孪生\n每患者独立RL策略'),
    ('3', '执行动作', 'NeuroSuit混合架构\n碳纤维锚定+鲍登线缆驱动\n<1.5kg，穿戴<3分钟'),
    ('4', '持续进化', '实时传感器反馈闭环\n策略每周自适应调整\n数据飞轮：越用越强'),
]
for i, (num, title, desc) in enumerate(steps):
    x = M + i * Inches(3.0)
    add_rect(s, x, Inches(2.0), Inches(2.7), Inches(4.8), DARK_CARD)
    add_rect(s, x, Inches(2.0), Inches(2.7), Pt(3), NEXUM_BLUE)
    add_text(s, x + Inches(0.2), Inches(2.2), Inches(0.5), Inches(0.5), num, Pt(28), NEXUM_BLUE, bold=True)
    add_text(s, x + Inches(0.2), Inches(2.9), Inches(2.3), Inches(0.5), title, Pt(16), WHITE, bold=True)
    add_text(s, x + Inches(0.2), Inches(3.5), Inches(2.3), Inches(2.5), desc, Pt(11), RGBColor(0xAA, 0xBB, 0xCC))

# Key message
add_text(s, M, Inches(7.0), Inches(11.5), Inches(0.4), '不卖硬件参数。卖的是AI对"你"的理解能力。', Pt(12), ACCENT, bold=True, align=PP_ALIGN.CENTER)

# ═══════════════════════════════════════════
# SLIDE 4: WHY NOW
# ═══════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6])
add_rect(s, 0, 0, W, Pt(4), NEXUM_BLUE)
add_text(s, M, Inches(0.3), Inches(11.5), Inches(0.6), '为什么是现在？四个条件同时就绪', Pt(28), BLACK, bold=True)
add_rect(s, M, Inches(1.1), Inches(1.5), Pt(2), NEXUM_BLUE)

conds = [
    ('🧠', '非侵入BCI\n达到可用精度', 'CMU Bin He 2025 Nature Comms\n步态意图检测多篇独立验证\n湖北/江苏/浙江已定价¥960-966/次'),
    ('🤖', '可穿戴硬件\n工程成熟', '混合架构经十多年研发积累\n力传输效率>70%，总重<1.5kg\n线缆驱动临床安全性20年数据'),
    ('⚡', '个性化AI\n具备工程化条件', '416肌肉+206骨骼+Hill柔顺肌腱\n2048仿真世界并行，日产53亿步态\n零人工标注'),
    ('📋', '政策框架\n全面到位', '中国脑机接口列入国家未来产业\nMedicare K1007 $91,032/台\n中美日德均已建立支付标准'),
]
for i, (icon, title, desc) in enumerate(conds):
    x = M + i * Inches(3.0)
    add_rect(s, x, Inches(1.6), Inches(2.7), Inches(5.2), LIGHT_BG)
    add_text(s, x + Inches(0.2), Inches(1.8), Inches(2.3), Inches(0.5), icon + '  ' + title, Pt(12), NEXUM_BLUE, bold=True)
    add_text(s, x + Inches(0.2), Inches(3.0), Inches(2.3), Inches(3.5), desc, Pt(10), GRAY)

# Quote
add_text(s, M, Inches(7.0), Inches(11.5), Inches(0.4), '2026年，9400万人的问题从科学问题变成了工程问题。', Pt(12), NEXUM_BLUE, bold=True, align=PP_ALIGN.CENTER)

# ═══════════════════════════════════════════
# SLIDE 5: PRODUCT
# ═══════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6])
add_rect(s, 0, 0, W, Pt(4), NEXUM_BLUE)
add_text(s, M, Inches(0.3), Inches(11.5), Inches(0.6), 'Nexum One：首款神经重连AI系统', Pt(28), BLACK, bold=True)

# Try to add renders
render_paths = [
    f'{DOCS}/ppt_render_2_headband.png',
    f'{DOCS}/ppt_render_3_suit.png',
    f'{DOCS}/ppt_render_1_system.png',
]
modules = ['EEG-Sense 头带', 'NeuroSuit 穿戴界面', 'Nexum One 完整系统']
specs = ['8ch干电极 · 80g · BLE 5.0\n250SPS · 24-bit · ADS1299', '碳纤维锚定 · 鲍登线缆\n<1.5kg · 8Nm持续/15Nm峰值', 'Clinical $18,000\nHome $3,999+$499/年']
for i in range(3):
    x = M + i * Inches(4.0)
    rpath = render_paths[i]
    if os.path.exists(rpath) and os.path.getsize(rpath) > 1000:
        add_img(s, rpath, x, Inches(1.3), Inches(3.7), Inches(2.8))
    else:
        add_rect(s, x, Inches(1.3), Inches(3.7), Inches(2.8), LIGHT_BG)
        add_text(s, x, Inches(2.5), Inches(3.7), Inches(0.5), modules[i], Pt(14), GRAY, align=PP_ALIGN.CENTER)
    add_text(s, x, Inches(4.3), Inches(3.7), Inches(0.4), modules[i], Pt(13), BLACK, bold=True, align=PP_ALIGN.CENTER)
    add_text(s, x, Inches(4.8), Inches(3.7), Inches(1.0), specs[i], Pt(9), GRAY, align=PP_ALIGN.CENTER)

add_text(s, M, Inches(6.2), Inches(11.5), Inches(0.8), '两个版本，同一条数据链：Clinical版$18K（医院）+ Home版$3,999+$499/年（家用）', Pt(12), NEXUM_BLUE, bold=True, align=PP_ALIGN.CENTER)

# ═══════════════════════════════════════════
# SLIDE 6: MARKET
# ═══════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6])
add_rect(s, 0, 0, W, Pt(4), NEXUM_BLUE)
add_text(s, M, Inches(0.3), Inches(11.5), Inches(0.6), '市场：三阶段TAM指数级扩大', Pt(28), BLACK, bold=True)
add_rect(s, M, Inches(1.1), Inches(1.5), Pt(2), NEXUM_BLUE)

phases = [
    ('Phase 1\n2028-2030', '$6.6B', '全球神经康复', '9400万中风×66%障碍\n×30%适配×5%渗透×$3,999\n+8000家医院×10%×$18K'),
    ('Phase 2\n2030-2033', '$15B', '全球老年行动力', '中国3亿60+人口\n×20%肌少症×3%渗透×¥5,000\n+美日欧老龄化市场'),
    ('Phase 3\n2033+', '$33.7B+', '全人群行动增强', '全球可穿戴外骨骼市场\nCAGR 32%\n户外/通勤/职业防护'),
]
for i, (phase, tam, title, desc) in enumerate(phases):
    x = M + i * Inches(4.0)
    # Card
    add_rect(s, x, Inches(1.5), Inches(3.7), Inches(5.2), LIGHT_BG if i < 2 else RGBColor(0xE8, 0xF4, 0xFD))
    add_rect(s, x, Inches(1.5), Inches(3.7), Pt(3), NEXUM_BLUE)
    add_text(s, x + Inches(0.2), Inches(1.7), Inches(3.3), Inches(0.7), phase, Pt(11), GRAY, bold=True, align=PP_ALIGN.CENTER)
    add_text(s, x + Inches(0.2), Inches(2.4), Inches(3.3), Inches(0.8), tam, Pt(36), NEXUM_BLUE, bold=True, align=PP_ALIGN.CENTER)
    add_text(s, x + Inches(0.2), Inches(3.4), Inches(3.3), Inches(0.4), title, Pt(14), BLACK, bold=True, align=PP_ALIGN.CENTER)
    add_text(s, x + Inches(0.2), Inches(4.0), Inches(3.3), Inches(2.5), desc, Pt(10), GRAY, align=PP_ALIGN.CENTER)

# Bottom
add_text(s, M, Inches(7.0), Inches(5.5), Inches(0.4), '已有市场：BCI $2.4B(15%) + 康复机器人 $1.8B(22%) + 外骨骼 $33.7B(32%)', Pt(12), NEXUM_BLUE, bold=True)
add_text(s, Inches(7.0), Inches(7.0), Inches(5.5), Inches(0.4), '医保已建立：Medicare $91K/台 · 中国BCI定价¥960-966/次 · HAL纳入日本医保', Pt(10), GRAY)

# ═══════════════════════════════════════════
# SLIDE 7: TECHNOLOGY
# ═══════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6])
add_gradient(s, 0, 0, W, H, DARK_BG, RGBColor(0x00, 0x20, 0x40))
add_text(s, M, Inches(0.5), Inches(11.5), Inches(0.6), '技术架构：四层闭环', Pt(32), WHITE, bold=True)
add_rect(s, M, Inches(1.2), Inches(1.5), Pt(3), NEXUM_BLUE)

layers = [
    ('感知层', 'EEG + sEMG双模态', '8ch干电极头带 + 织物sEMG电极\nEEG覆盖肌力0-1级，sEMG逐步接管\n三级降级安全冗余'),
    ('决策层', '个性化AI引擎', 'DL提取EEG特征 → MSK数字孪生建模\n→ RL训练最优策略 → 传统控制保安全\n每患者独立模型，每周自适应更新'),
    ('执行层', '混合式机械架构', '碳纤维髋部锚定(力传输>70%)\n鲍登线缆驱动(关节处轻量化)\n标准化关节电机(扭矩密度40-50Nm/kg)'),
    ('进化层', '联邦学习数据飞轮', '原始生理数据本地处理\n仅脱敏模型改善数据上传\n隐私保护+数据网络效应'),
]
for i, (label, title, desc) in enumerate(layers):
    y = Inches(1.6) + i * Inches(1.4)
    add_rect(s, M, y, Inches(1.8), Inches(1.2), DARK_CARD)
    add_text(s, M + Inches(0.1), y + Inches(0.1), Inches(1.6), Inches(0.4), label, Pt(14), NEXUM_BLUE, bold=True)
    add_text(s, M + Inches(0.1), y + Inches(0.5), Inches(1.6), Inches(0.5), title, Pt(10), WHITE, bold=True)

    add_text(s, Inches(2.8), y + Inches(0.1), Inches(9.5), Inches(1.1), desc, Pt(11), RGBColor(0xAA, 0xBB, 0xCC))

# ═══════════════════════════════════════════
# SLIDE 8: COMPETITION
# ═══════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6])
add_rect(s, 0, 0, W, Pt(4), NEXUM_BLUE)
add_text(s, M, Inches(0.3), Inches(11.5), Inches(0.6), '竞争：我们在AI理解人的维度上', Pt(28), BLACK, bold=True)
add_rect(s, M, Inches(1.1), Inches(1.5), Pt(2), NEXUM_BLUE)

# Comparison table
tbl = slide = s
n_rows, n_cols = 6, 5
tbl_shape = s.shapes.add_table(n_rows, n_cols, M, Inches(1.5), Inches(11.5), Inches(4.5))
table = tbl_shape.table
col_widths = [Inches(3.0), Inches(2.2), Inches(2.1), Inches(2.1), Inches(2.1)]
for i, w in enumerate(col_widths):
    table.columns[i].width = w

headers = ['能力', '逐念而行 Nexum', 'Ekso/ReWalk', 'HAL (Cyberdyne)', '程天科技']
rows = [
    ['EEG意图解码', '✅ 8ch干电极', '❌', '❌ (仅EMG)', '✅ 多模态融合'],
    ['MSK数字孪生+RL', '✅ 416肌肉模型', '❌', '❌', '❌'],
    ['联邦学习隐私保护', '✅', '❌', '❌', '❌'],
    ['价格', '$18K / $3,999', '$75K–100K', '$60K–80K', '¥10万+(医院)'],
    ['核心差异', 'AI理解人', '卖硬件参数', 'EMG灵敏度', '硬件集成'],
]

for j, h in enumerate(headers):
    cell = table.cell(0, j); cell.text = h
    for p in cell.text_frame.paragraphs: p.font.size = Pt(11); p.font.bold = True; p.font.color.rgb = WHITE
    cell.fill.solid(); cell.fill.fore_color.rgb = NEXUM_BLUE

for i, row in enumerate(rows):
    for j, val in enumerate(row):
        cell = table.cell(i+1, j); cell.text = val
        for p in cell.text_frame.paragraphs: p.font.size = Pt(10); p.font.color.rgb = GRAY
        if j == 0:
            for p in cell.text_frame.paragraphs: p.font.bold = True; p.font.color.rgb = BLACK
        if i % 2 == 0:
            cell.fill.solid(); cell.fill.fore_color.rgb = LIGHT_BG

add_text(s, M, Inches(6.3), Inches(11.5), Inches(0.8), '关键差异：Ekso/ReWalk/HAL是硬件公司——每多卖一台，不会变得更聪明。逐念而行每多一个患者，AI就更强一分。', Pt(12), NEXUM_BLUE, bold=True)

# ═══════════════════════════════════════════
# SLIDE 9: BUSINESS MODEL + FINANCIALS
# ═══════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6])
add_rect(s, 0, 0, W, Pt(4), NEXUM_BLUE)
add_text(s, M, Inches(0.3), Inches(11.5), Inches(0.6), '商业模式与财务预测', Pt(28), BLACK, bold=True)
add_rect(s, M, Inches(1.1), Inches(1.5), Pt(2), NEXUM_BLUE)

# Revenue table
rev_tbl = s.shapes.add_table(6, 6, M, Inches(1.5), Inches(7.0), Inches(3.0))
rt = rev_tbl.table
for i, w in enumerate([Inches(0.8), Inches(1.5), Inches(1.2), Inches(1.2), Inches(1.2), Inches(1.1)]):
    rt.columns[i].width = w

for j, h in enumerate(['年', 'Clinical(台)', 'Home(台)', '总收入', '毛利率', '净利润']):
    c = rt.cell(0, j); c.text = h
    for p in c.text_frame.paragraphs: p.font.size = Pt(9); p.font.bold = True; p.font.color.rgb = WHITE
    c.fill.solid(); c.fill.fore_color.rgb = NEXUM_BLUE

fin_data = [
    ('2027', '—（预临床）', '—', '$0', '—', '-$2.5M'),
    ('2028', '150×$16K', '100×$4K', '$2.8M', '52%', '-$2.0M'),
    ('2029', '400×$15K', '500×$3.8K', '$7.9M', '58%', '-$0.5M'),
    ('2030', '1,000×$14K', '2,000×$3.5K', '$21.0M', '63%', '$3.0M'),
    ('2031', '2,500×$13K', '8,000×$3.2K', '$58.1M', '68%', '$15.0M'),
]
for i, row in enumerate(fin_data):
    for j, v in enumerate(row):
        c = rt.cell(i+1, j); c.text = v
        for p in c.text_frame.paragraphs: p.font.size = Pt(8); p.font.color.rgb = GRAY
        if i % 2 == 0: c.fill.solid(); c.fill.fore_color.rgb = LIGHT_BG
        if j == 3 or j == 5:
            for p in c.text_frame.paragraphs: p.font.bold = True

# Right side highlights
bx = Inches(8.5)
add_rect(s, bx, Inches(1.5), Inches(4.3), Inches(5.5), LIGHT_BG)
add_text(s, bx + Inches(0.2), Inches(1.7), Inches(3.9), Inches(0.4), '商业里程碑', Pt(14), NEXUM_BLUE, bold=True)

milestones = [
    ('2026 Q3', '种子轮 ¥800万'),
    ('2027 Q1', '天使轮 ¥2,500万'),
    ('2028 Q1', 'Pre-A $7M'),
    ('2028', 'NMPA获批 · 首批交付'),
    ('2029', '盈亏平衡 · ~700台/年'),
    ('2030', 'A轮$20M · FDA+CE'),
]
for i, (yr, ms) in enumerate(milestones):
    add_text(s, bx + Inches(0.2), Inches(2.3) + i * Inches(0.5), Inches(1.2), Inches(0.4), yr, Pt(9), NEXUM_BLUE, bold=True)
    add_text(s, bx + Inches(1.5), Inches(2.3) + i * Inches(0.5), Inches(2.6), Inches(0.4), ms, Pt(9), GRAY)

add_text(s, M, Inches(5.0), Inches(7.0), Inches(1.0), '盈亏平衡：~700台/年（2029 Q4–2030 Q1）\nHome版BOM约¥3,000，毛利与Ekso(53%)可比但S&M仅30%(vs 40-70%)', Pt(9), GRAY)

# ═══════════════════════════════════════════
# SLIDE 10: TEAM
# ═══════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6])
add_gradient(s, 0, 0, W, H, DARK_BG, RGBColor(0x00, 0x20, 0x40))
add_text(s, M, Inches(0.5), Inches(11.5), Inches(0.8), '团队', Pt(32), WHITE, bold=True)
add_rect(s, M, Inches(1.3), Inches(1.5), Pt(3), NEXUM_BLUE)

# Core team
team = [
    ('赵子睿', '创始人 & CEO', 'Columbia EE MSc (ML)\n华为美国Futurewei IoT Lab\n8年CTO (欣网/智擎机器人)\nFAI患者——产品原动力'),
    ('汪牧星', '算法', 'NEU PhD Candidate\nEdinburgh MSc Distinction\npFedAC第一作者\n联邦学习/个性化AI'),
    ('临床负责人', '招募中 · 优先级最高', '康复医学主任医师\n临床试验设计与执行\nNMPA方案撰写经验'),
    ('EEG硬件负责人', '招募中', '脑电采集系统设计\nTI ADS1299方案经验\n干电极优化+产品化'),
]
for i, (name, role, bio) in enumerate(team):
    x = M + i * Inches(3.0)
    add_rect(s, x, Inches(1.7), Inches(2.7), Inches(3.6), DARK_CARD)
    add_rect(s, x, Inches(1.7), Inches(2.7), Pt(3), NEXUM_BLUE if i < 2 else RGBColor(0x55, 0x55, 0x55))
    add_text(s, x + Inches(0.2), Inches(1.9), Inches(2.3), Inches(0.5), name, Pt(18), WHITE if i < 2 else GRAY, bold=True)
    add_text(s, x + Inches(0.2), Inches(2.5), Inches(2.3), Inches(0.3), role, Pt(11), NEXUM_BLUE if i < 2 else GRAY)
    add_text(s, x + Inches(0.2), Inches(3.0), Inches(2.3), Inches(2.0), bio, Pt(9), RGBColor(0xAA, 0xBB, 0xCC))

# Academic partners
add_text(s, M, Inches(5.6), Inches(11.5), Inches(0.4), '学术合作', Pt(14), ACCENT, bold=True)
add_text(s, M, Inches(6.1), Inches(11.5), Inches(0.8), 'CMU Bin He Lab (非侵入EEG) · NEU NeuMove Lab (肌骨仿真) · 清华/浙大/西湖大学 (BCI与神经工程)', Pt(10), RGBColor(0xAA, 0xBB, 0xCC))

# ═══════════════════════════════════════════
# SLIDE 11: FUNDING
# ═══════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6])
add_rect(s, 0, 0, W, Pt(4), NEXUM_BLUE)
add_text(s, M, Inches(0.3), Inches(11.5), Inches(0.6), '融资路线：每轮对应可验证里程碑', Pt(28), BLACK, bold=True)
add_rect(s, M, Inches(1.1), Inches(1.5), Pt(2), NEXUM_BLUE)

rounds = [
    ('种子轮', '2026 Q3', '¥800万', '原型2台 + 团队8人12月\n3家医院预临床协议\n可演示原型'),
    ('天使轮', '2027 Q1', '¥2,500万', '10台样机 + 30例预临床\nNMPA正式受理\n预临床数据发表'),
    ('Pre-A', '2028 Q1', '$7M', 'NMPA获批 + 首批商业化\n50家医院渠道\nHome版发布'),
    ('A轮', '2029 H2', '$20M', 'FDA 510(k) + CE\n海外渠道 + 规模化\n年销过千台'),
]
for i, (name, time, amount, use) in enumerate(rounds):
    x = M + i * Inches(3.0)
    add_rect(s, x, Inches(1.5), Inches(2.7), Inches(5.2), LIGHT_BG if i < 3 else RGBColor(0xE8, 0xF4, 0xFD))
    add_rect(s, x, Inches(1.5), Inches(2.7), Pt(3), NEXUM_BLUE)
    add_text(s, x + Inches(0.2), Inches(1.7), Inches(2.3), Inches(0.4), name, Pt(16), NEXUM_BLUE, bold=True)
    add_text(s, x + Inches(0.2), Inches(2.2), Inches(2.3), Inches(0.4), time, Pt(11), GRAY)
    add_text(s, x + Inches(0.2), Inches(2.6), Inches(2.3), Inches(0.6), amount, Pt(24), BLACK, bold=True)
    add_text(s, x + Inches(0.2), Inches(3.4), Inches(2.3), Inches(3.0), use, Pt(10), GRAY)

add_text(s, M, Inches(7.0), Inches(11.5), Inches(0.4), '种子轮¥800万寻找领投方。资金用于原型验证和预临床启动——12个月可验证的技术里程碑。', Pt(12), NEXUM_BLUE, bold=True, align=PP_ALIGN.CENTER)

# ═══════════════════════════════════════════
# SLIDE 12: VISION
# ═══════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6])
add_gradient(s, 0, 0, W, H, DARK_BG, RGBColor(0x00, 0x30, 0x60))
add_rect(s, 0, 0, W, Pt(4), NEXUM_BLUE)

add_text(s, M, Inches(1.0), Inches(11.5), Inches(1.5), '2026年，AI从数字世界进入了物理世界。\n逐念而行专注于其中尚未被充分探索的方向——\n让AI理解人的身体，而不只是造AI的机器身体。', Pt(22), WHITE, align=PP_ALIGN.CENTER)

add_rect(s, Inches(5.5), Inches(3.0), Inches(2.3), Pt(2), NEXUM_BLUE)

vision_steps = [
    '2026-2028：定义品类，从最难的地方开始。Nexum One进入100家康复医院。',
    '2029-2030：品类扩展，从患者到老人。从神经重连到通用意图驱动助力。',
    '2031+：人机共生成为基础设施。百万用户。从修复到增强，从患者到每一个人。',
]
for i, step in enumerate(vision_steps):
    add_text(s, M + Inches(1.0), Inches(3.5) + i * Inches(0.8), Inches(11.0), Inches(0.6), f'{i+1}. {step}', Pt(14), ACCENT if i == 0 else RGBColor(0xAA, 0xCC, 0xEE))

# Contact
add_rect(s, Inches(3.5), Inches(6.3), Inches(6.3), Inches(0.9), DARK_CARD)
add_text(s, Inches(3.7), Inches(6.4), Inches(5.9), Inches(0.3), '逐念而行 · Nexum', Pt(16), WHITE, bold=True, align=PP_ALIGN.CENTER)
add_text(s, Inches(3.7), Inches(6.8), Inches(5.9), Inches(0.3), '赵子睿 · zirui@nexum.ai · 人机共生赛道', Pt(11), ACCENT, align=PP_ALIGN.CENTER)

# ── SAVE ──
output_path = f'{DOCS}/Nexum_Pitch_Deck.pptx'
prs.save(output_path)
print(f'PPTX saved: {output_path}')
print(f'Size: {os.path.getsize(output_path)/1024:.0f} KB')
