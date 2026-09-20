# TravelPilot Brand Guidelines v1.0

> Last updated: September 19, 2026
> Status: Active

## Quick Reference

| Element | Value |
|---------|-------|
| Primary Color | #171717 (Near-Black) |
| Accent Color | #A16207 (Gold) |
| Primary Font | Fira Sans |
| Mono Font | Fira Code |
| Voice | Confident, Precise, Trustworthy |
| Style | Trust & Authority |

---

## 1. Color Palette

### Primary Colors

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| Primary | #171717 | rgb(23,23,23) | Headers, buttons, text, primary actions |
| On Primary | #FFFFFF | rgb(255,255,255) | Text on primary backgrounds |
| Secondary | #404040 | rgb(64,64,64) | Hover states, secondary emphasis |

### Accent Colors

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| Accent Gold | #A16207 | rgb(161,98,7) | CTAs, highlights, active states |
| Accent Light | #D4A843 | rgb(212,168,67) | Lighter gold for subtle accents |
| Accent Background | #FDF8EE | rgb(253,248,238) | Gold-tinted backgrounds, badges |
| Accent Border | #E8D5A8 | rgb(232,213,168) | Gold borders, tag outlines |

### Neutral Palette

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| Background | #FFFFFF | rgb(255,255,255) | Page backgrounds |
| Muted | #E8ECF0 | rgb(232,236,240) | Card backgrounds, subtle fills |
| Muted Foreground | #6B7280 | rgb(107,114,128) | Captions, labels, secondary text |
| Border | #E5E5E5 | rgb(229,229,229) | Dividers, input borders |
| Foreground | #171717 | rgb(23,23,23) | Body text, headings |

### Semantic Colors

| State | Hex | Usage |
|-------|-----|-------|
| Success | #16A34A | Positive states, resilience "Strong" |
| Warning | #A16207 | Caution, resilience "Fragile" |
| Error | #DC2626 | Errors, destructive actions, Chaos Mode, resilience "Critical" |
| Info | #404040 | Informational, neutral feedback |

### Accessibility

- Primary on white: 18.1:1 contrast ratio (AAA)
- Muted Foreground on white: 4.7:1 contrast ratio (AA)
- Gold Accent on white: 4.6:1 contrast ratio (AA)
- All interactive elements meet WCAG 2.1 AA standards

---

## 2. Typography

### Font Stack

```css
--font-sans: 'Fira Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
--font-mono: 'Fira Code', 'SF Mono', Consolas, monospace;
```

### Type Scale

| Element | Size (Desktop) | Size (Mobile) | Weight | Line Height |
|---------|----------------|---------------|--------|-------------|
| H1 | 40px | 28px | 700 | 1.1 |
| H2 | 24px | 20px | 600 | 1.3 |
| H3 | 18px | 16px | 600 | 1.3 |
| Body | 16px | 15px | 400 | 1.6 |
| Body Small | 14px | 13px | 400 | 1.5 |
| Caption | 12px | 11px | 500 | 1.4 |
| Mono | 11-13px | 10-12px | 400-500 | 1.4 |

### Font Loading

```html
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600&family=Fira+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet" />
```

---

## 3. Voice & Tone

### Brand Personality

| Trait | Description |
|-------|-------------|
| **Confident** | Algorithmic rigor, not guesswork — we show our work |
| **Precise** | Specific numbers, real distances, actual times — never vague |
| **Trustworthy** | We surface risk proactively, not just pretty itineraries |

### Voice Chart

| Trait | We Are | We Are Not |
|-------|--------|------------|
| Confident | "The scheduler runs greedy nearest-neighbor with time-window pruning" | "Our AI plans your perfect trip!" |
| Precise | "8.49km, ~17min travel from Senso-ji to Gyoen" | "A short ride away" |
| Trustworthy | "Resilience: 55/100 — Fragile. Key risks: Buffer Time, Single-Point Failures." | "Your trip is ready!" |

### Tone by Context

| Context | Tone | Example |
|---------|------|---------|
| Dashboard headline | Bold, minimal | "Tokyo" (not "Your Amazing Tokyo Adventure") |
| Resilience score | Factual, specific | "55 — Fragile. Buffer Time: 80, Single-Point Failures: 67" |
| Chaos Mode button | Urgent, action-oriented | "CHAOS MODE" (uppercase, red, with intent) |
| Diff explanation | Analytical, structured | "Replaced Tokyo National Museum with Senso-ji Temple. Travel time: 3min. Cost difference: $10." |
| Chat responses | Concise, data-backed | "Total estimated cost: $115. Day 1: $115 across 6 activities." |

### Prohibited Terms

| Avoid | Reason |
|-------|--------|
| "AI-powered" (in body copy) | Overused — show intelligence through output, not labels |
| "Seamless" | Corporate jargon |
| "Leverage" | Use "use" instead |
| "Revolutionary" | Overused |
| "Best-in-class" | Vague claim |
| Emoji as UI elements | Use SVG icons instead |
| Exclamation marks (more than 1 per page) | Undermines precision tone |

---

## 4. Visual Identity

### Design Style: Trust & Authority

- Minimal black + gold accent
- Lots of whitespace
- No playful gradients or shadows
- Data-dense, not decorative
- Certificates/badges displayed, expert credentials visible

### Iconography

- **Library:** Lucide (via better-icons)
- **Style:** Outline, 24px base grid
- **Stroke:** 2px consistent
- **Color:** `currentColor` (inherits from parent)
- **Never use emojis as icons**

### Component Standards

| Element | Style |
|---------|-------|
| Buttons | 8px radius, 600 weight, 16px font |
| Cards | 12px radius, 1px solid border, shadow-sm |
| Inputs | 8px radius, 1px solid border, focus ring |
| Tags/Pills | 100px radius (pill shape) |
| Charts | Chart.js with Fira Code labels |

### Spacing Scale

| Token | Value | Usage |
|-------|-------|-------|
| --space-1 | 4px | Tight inline spacing |
| --space-2 | 8px | Compact element gaps |
| --space-3 | 12px | Standard small gaps |
| --space-4 | 16px | Standard spacing |
| --space-5 | 20px | Medium gaps |
| --space-6 | 24px | Section padding |
| --space-8 | 32px | Large gaps |
| --space-10 | 40px | Section dividers |
| --space-12 | 48px | Major section breaks |

---

## 5. Imagery & Data Visualization

### Photography Style

- **None** — TravelPilot uses data visualization, not photography
- If photography is ever needed: natural lighting, real places, no stock-photo feel

### Data Visualization

- **Library:** Chart.js (Doughnut, Bar)
- **Colors:** Primary (#171717), Accent (#A16207), Neutral (#E8ECF0)
- **Fonts:** Fira Code for axis labels, Fira Sans for legends
- **Style:** Minimal — no grid lines on x-axis, subtle y-axis grid
- **Tooltips:** Dark background (#171717), white text, 6px radius

### Diff Visualization

| Change Type | Color | Badge |
|-------------|-------|-------|
| Removed | #DC2626 (red) | White on red |
| Added | #16A34A (green) | White on green |
| Modified | #7C3AED (purple) | White on purple |
| Shifted | #A16207 (gold) | White on gold |

---

## 6. AI Image Generation

### Base Prompt Template

```
Minimalist data dashboard, black (#171717) and gold (#A16207) color scheme,
clean white background, Fira Sans typography, professional travel planning
interface, trust and authority aesthetic, no gradients, sharp edges
```

### Style Keywords

| Category | Keywords |
|----------|----------|
| **Lighting** | Even, flat, no dramatic shadows |
| **Mood** | Professional, precise, trustworthy |
| **Composition** | Grid-based, data-dense, structured |
| **Treatment** | High contrast, minimal color |
| **Aesthetic** | Swiss design, data-first, no decoration |

### Visual Don'ts

| Avoid | Reason |
|-------|--------|
| Colorful gradients | Undermines Trust & Authority |
| Emoji as icons | Inconsistent across platforms |
| Playful illustrations | Wrong tone for precision product |
| Drop shadows on cards | Use borders instead |
| Centered single-column forms | Use grid layout |

---

## 7. Brand Sync

### Source of Truth

This file (`docs/brand-guidelines.md`) is the canonical brand reference.

### Design Tokens

Tokens are synced to:
- `assets/design-tokens.json` — structured token definitions
- `assets/design-tokens.css` — CSS custom properties
- `frontend/src/index.css` — actual implementation

### Sync Command

```bash
node scripts/sync-brand-to-tokens.cjs
```

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-09-19 | Initial guidelines — Trust & Authority, black/gold palette |
