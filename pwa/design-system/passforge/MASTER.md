# Design System Master File

> **LOGIC:** When building a specific page, first check `design-system/pages/[page-name].md`.
> If that file exists, its rules **override** this Master file.
> If not, strictly follow the rules below.

---

**Project:** PassForge
**Generated:** 2026-02-10 20:34:31
**Category:** Cybersecurity Platform

---

## Global Rules

### Color Palette

| Role | Hex | CSS Variable |
|------|-----|--------------|
| Primary | `#0EA5E9` | `--color-primary` |
| Secondary | `#3B82F6` | `--color-secondary` |
| CTA/Accent | `#22C55E` | `--color-cta` |
| Background | `#020617` | `--color-background` |
| Text | `#F8FAFC` | `--color-text` |

**Color Notes:** Security blue + protected green

### Typography

- **Heading Font:** Inter
- **Body Font:** Inter
- **Mood:** spatial, legible, glass, system, clean, neutral
- **Google Fonts:** [Inter + Inter](https://fonts.google.com/share?selection.family=Inter:wght@300;400;500;600)

**CSS Import:**
```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
```

### Spacing Variables

| Token | Value | Usage |
|-------|-------|-------|
| `--space-xs` | `4px` / `0.25rem` | Tight gaps |
| `--space-sm` | `8px` / `0.5rem` | Icon gaps, inline spacing |
| `--space-md` | `16px` / `1rem` | Standard padding |
| `--space-lg` | `24px` / `1.5rem` | Section padding |
| `--space-xl` | `32px` / `2rem` | Large gaps |
| `--space-2xl` | `48px` / `3rem` | Section margins |
| `--space-3xl` | `64px` / `4rem` | Hero padding |

### Shadow Depths

| Level | Value | Usage |
|-------|-------|-------|
| `--shadow-sm` | `0 1px 2px rgba(0,0,0,0.05)` | Subtle lift |
| `--shadow-md` | `0 4px 6px rgba(0,0,0,0.1)` | Cards, buttons |
| `--shadow-lg` | `0 10px 15px rgba(0,0,0,0.1)` | Modals, dropdowns |
| `--shadow-xl` | `0 20px 25px rgba(0,0,0,0.15)` | Hero images, featured cards |

---

## Component Specs

### Buttons

```css
/* Primary Button */
.btn-primary {
  background: #22C55E;
  color: #052E16;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 700;
  box-shadow: 0 0 15px rgba(34, 197, 94, 0.2);
}

/* Glass Card */
.card {
  background: rgba(15, 23, 42, 0.7);
  backdrop-filter: blur(16px);
  border: 1px solid rgba(59, 130, 246, 0.1);
  border-radius: 16px;
  padding: 24px;
}

/* Cyber Input */
.input {
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(59, 130, 246, 0.2);
  color: #F8FAFC;
  padding: 12px 16px;
  border-radius: 8px;
}

.input:focus {
  border-color: #0EA5E9;
  box-shadow: 0 0 10px rgba(14, 165, 233, 0.3);
}
```

---

## Style Guidelines

**Style:** Cyberpunk UI

**Keywords:** Neon, dark mode, terminal, HUD, sci-fi, glitch, dystopian, futuristic, matrix, tech noir

**Best For:** Gaming platforms, tech products, crypto apps, sci-fi applications, developer tools, entertainment

**Key Effects:** Neon glow (text-shadow), glitch animations (skew/offset), scanlines (::before overlay), terminal fonts

### Page Pattern

**Pattern Name:** Horizontal Scroll Journey

- **Conversion Strategy:** Immersive product discovery. High engagement. Keep navigation visible.
- **CTA Placement:** Floating Sticky CTA or End of Horizontal Track
- **Section Order:** 1. Intro (Vertical), 2. The Journey (Horizontal Track), 3. Detail Reveal, 4. Vertical Footer

---

## Anti-Patterns (Do NOT Use)

- ❌ **Low-contrast themes** — Maintain AA accessibility on all modes.
- ❌ Poor data viz

**Note on Themes:** While Cyberpunk is primarily a dark aesthetic, high-contrast Light Themes are allowed if they maintain the 4.5:1 contrast requirement. Mixed-theme components that break visual hierarchy are forbidden.

### Additional Forbidden Patterns

- ❌ **Emojis as icons** — Use SVG icons (Heroicons, Lucide, Simple Icons)
- ❌ **Missing cursor:pointer** — All clickable elements must have cursor:pointer
- ❌ **Layout-shifting hovers** — Avoid scale transforms that shift layout
- ❌ **Low contrast text** — Maintain 4.5:1 minimum contrast ratio
- ❌ **Instant state changes** — Always use transitions (150-300ms)
- ❌ **Invisible focus states** — Focus states must be visible for a11y

---

## Pre-Delivery Checklist

Before delivering any UI code, verify:

- [ ] No emojis used as icons (use SVG instead)
- [ ] All icons from consistent icon set (Heroicons/Lucide)
- [ ] `cursor-pointer` on all clickable elements
- [ ] Hover states with smooth transitions (150-300ms)
- [ ] High-contrast themes: text contrast 4.5:1 minimum
- [ ] Focus states visible for keyboard navigation
- [ ] `prefers-reduced-motion` respected
- [ ] Responsive: 375px, 768px, 1024px, 1440px
- [ ] No content hidden behind fixed navbars
- [ ] No horizontal scroll on mobile
