# Nexum Website Redesign — Design Spec

**Date:** 2026-06-21 | **Status:** Approved

## 1. Design System

### 1.1 Colors
| Token | Value | Usage | WCAG |
|-------|-------|-------|------|
| `--bg` | `#000000` | Page background | — |
| `--bg-elevated` | `rgba(255,255,255,0.03)` | Card background | — |
| `--bg-elevated-hover` | `rgba(255,255,255,0.05)` | Card hover | — |
| `--border` | `rgba(255,255,255,0.06)` | Card borders | — |
| `--border-hover` | `rgba(255,255,255,0.12)` | Card hover borders | — |
| `--text-primary` | `#FFFFFF` | H1/H2/H3 titles | 21:1 AAA |
| `--text-body` | `#CCCCCC` | Paragraph text | 13:1 AAA |
| `--text-secondary` | `#999999` | Descriptions, labels | 7.5:1 AAA |
| `--text-tertiary` | `#777777` | Footnotes, copyright | 4.5:1 AA |
| `--text-disabled` | `#555555` | Decorative only | — |
| `--accent` | `#0096F0` | Links, highlights, data | 4.5:1 AA |
| `--accent-glow` | `rgba(0,150,240,0.08)` | Glow effects | — |

### 1.2 Typography
- **Font:** Inter (headings + body) + PingFang SC (Chinese fallback)
- **H1:** 72-120px, 900 weight, letter-spacing -3px, line-height 0.95
- **H2:** 36-48px, 800 weight, letter-spacing -0.5px, line-height 1.1
- **H3:** 18-24px, 700 weight, line-height 1.2
- **Body:** 15px, 400 weight, #CCC, line-height 1.7
- **Secondary:** 13px, #999, line-height 1.6
- **Tertiary:** 11px, #777, line-height 1.5
- **Minimum readable size:** 10px (footnotes only)
- **Rule:** No font-weight below 400 on black background

### 1.3 Spacing
- Section vertical padding: 120px (desktop), 80px (mobile)
- Card padding: 28-40px
- Grid gaps: 16-24px (cards), 40-64px (sections)
- Max content width: 1200px

## 2. Page Architecture — Hub & Spoke

```
nexum/
├── index.html              L1: Homepage (investor teaser, ~10 sections)
├── product.html             L2: Product detail (3 components + renders + specs)
├── technology.html          L2: Technology deep-dive (loop + architecture + diagrams)
├── app.html                 L2: App UI showcase (patient + therapist screens)
├── 逐念而行_Nexum_BP.html   Independent: Investor BP (existing, sync theme)
└── docs/                    L3: Document center (PRD, clinical, BOM, etc.)
    ├── prd.html
    ├── clinical-protocol.html
    ├── engineering-architecture.html
    ├── production-bom.html
    ├── regulatory-strategy.html
    ├── product-renders.html
    ├── engineering-diagrams.html
    └── app-ui-mockups.html
```

## 3. Homepage Sections (index.html)

| # | Section | Content | Visual Technique |
|---|---------|---------|------------------|
| 1 | Nav | Logo + 产品/技术/App/团队 + 投资者入口 CTA | Fixed, glass blur, 1px bottom border |
| 2 | Hero | Full-screen: 2-line title 120px, subtitle, 2 CTAs, 5 metrics | Glow orbs, product silhouette watermark, fade-in |
| 3 | Problem | Left text + right 3 stat cards | Number impact, minimal |
| 4 | Product | 3 cards with render images on top → click to product.html | Image-top cards, tilt on hover (JS 3D parallax) |
| 5 | Tech Loop | 4-step SVG (already built) + latency bar | Step cards with glow, animated arrows |
| 6 | Gallery | 4-5 render images horizontal scroll | Full-width sticky carousel, dot indicators |
| 7 | App Preview | 3 phone-frame mockups | Centered, side-by-side phones |
| 8 | Market + Why Now | 3 phase cards + 4 why-now cards | Hover lift + border glow |
| 9 | Team | 2 core + 2 advisor cards + "Join us" | Minimal avatar circles |
| 10 | Contact + Footer | Email, Shanghai, 4-column footer | Clean divider, low-key |

## 4. Sub-Page Designs

### 4.1 product.html
- Hero: large product render background
- Section 1: 3-component detail (expanded cards from homepage)
- Section 2: Full render gallery (grid + lightbox)
- Section 3: Engineering architecture diagram (SVG)
- Section 4: Full spec table

### 4.2 technology.html
- Hero: tech loop animation
- Section 1: 4-step expanded explanation
- Section 2: Latency breakdown with interactive bar
- Section 3: Engineering diagrams (system block, power tree, firmware)
- Section 4: AI architecture (data flow, training pipeline)

### 4.3 app.html
- Hero: phones in 3D-ish arrangement
- Section 1: Patient app screens (training, biofeedback, progress)
- Section 2: Therapist app screens (patient management, reports)
- Section 3: Design system (colors, components, typography)

## 5. Navigation System
- **Desktop:** Fixed top bar, glass blur bg, 1px bottom border
- **Nav items:** 产品 | 技术 | App | 团队 | 投资者入口(CTA button)
- **Mobile:** Hamburger → full-screen overlay menu
- **Page transitions:** View Transitions API where supported, CSS fade fallback
- **Active state:** White text + subtle bottom indicator

## 6. Animation & Interaction
- Scroll-triggered fade-up (Intersection Observer, already built)
- Product cards: 3D tilt on mouse move (vanilla JS, ~50 lines)
- Gallery carousel: horizontal scroll snap + dot indicators
- Tech loop: SVG step-by-step reveal on scroll
- Latency bar: segment animation on view (already built)
- Hero: subtle particle/grain animation (CSS only, no JS dep)
- Hover: all cards lift 4-8px + border glow transition

## 7. Technical Constraints
- **No framework dependencies** — vanilla HTML/CSS/JS only
- **No build step** — files served directly
- **Single shared CSS** for all pages (copy or shared include)
- **Responsive:** 3 breakpoints (1024px, 768px, 480px)
- **Performance:** all images optimized, no blocking JS
- **Print styles:** keep existing print CSS

## 8. Files to Create/Modify

### Create:
- `product.html` — new L2 product page
- `technology.html` — new L2 technology page  
- `app.html` — new L2 app showcase page

### Complete Rewrite:
- `index.html` — full redesign with new theme, layout, animations

### Theme Sync (CSS-only update):
- `docs/prd.html`
- `docs/clinical-protocol.html`
- `docs/engineering-architecture.html`
- `docs/production-bom.html`
- `docs/regulatory-strategy.html`
- `docs/product-visualization.html`
- `docs/product-renders.html`
- `docs/engineering-diagrams.html`
- `docs/app-ui-mockups.html`
- `逐念而行_Nexum_BP.html`

## 9. Text Clarity Checklist (per page)
- [ ] Body text ≥ 15px, #CCCCCC
- [ ] No font-weight below 400
- [ ] No text color dimmer than #777 for readable content
- [ ] Line-height ≥ 1.5 for all body text
- [ ] All Chinese text uses PingFang SC fallback
- [ ] WCAG AA minimum (4.5:1) for all content text
