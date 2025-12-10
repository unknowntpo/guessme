# Guessme Design Style Guide (Tailwind CSS)

Based on MotherDuck design system. Use this guide to maintain visual consistency.

**Framework:** Tailwind CSS 4 with `@theme` variables in `main.css`

---

## Color Palette

**Theme Definition (`main.css`):**
```css
@theme {
  --color-bg: #F4EFEA;          /* Warm cream - page background */
  --color-text: #383838;        /* Dark charcoal - text, borders */
  --color-primary: #6FC2FF;     /* Light blue - primary buttons */
  --color-primary-hover: #2BA5FF; /* Medium blue - button hover */
  --color-accent: #FFDE00;      /* Yellow - highlights, timer */
  --color-success: #53DBC9;     /* Teal - success states */
  --color-error: #FF7169;       /* Coral - error, warning */
  --color-gray: #A1A1A1;        /* Gray - secondary text */
}
```

**Tailwind Classes:**
| Color | Hex | Background | Text |
|-------|-----|------------|------|
| Background | `#F4EFEA` | `bg-bg` | `text-bg` |
| Text | `#383838` | `bg-text` | `text-text` |
| Primary | `#6FC2FF` | `bg-primary` | `text-primary` |
| Primary Hover | `#2BA5FF` | `hover:bg-primary-hover` | - |
| Accent | `#FFDE00` | `bg-accent` | `text-accent` |
| Success | `#53DBC9` | `bg-success` | `text-success` |
| Error | `#FF7169` | `bg-error` | `text-error` |
| Gray | `#A1A1A1` | `bg-gray` | `text-gray` |
| White | `#FFFFFF` | `bg-white` | `text-white` |

---

## Typography

### Fonts

**Theme Definition (`main.css`):**
```css
@theme {
  --font-mono: "Space Mono", monospace;
  --font-sans: "Inter", Arial, sans-serif;
}
```

**Tailwind Classes:**
| Font | Usage | Tailwind |
|------|-------|----------|
| Space Mono | Headlines, labels, buttons | `font-mono` |
| Inter | Body text | `font-sans` |

**Google Fonts import:**
```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
```

### Heading Scale (h1)

```html
<h1 class="font-mono font-normal uppercase tracking-wide leading-[140%] text-[30px] md:text-[56px] md:leading-[120%] lg:text-[80px]">
  Heading
</h1>
```

| Breakpoint | Font Size | Line Height |
|------------|-----------|-------------|
| Mobile (default) | `text-[30px]` | `leading-[140%]` |
| Tablet (≥728px) | `md:text-[56px]` | `md:leading-[120%]` |
| Desktop (≥960px) | `lg:text-[80px]` | - |

### Body Text

```html
<body class="font-sans font-light text-base leading-[140%] tracking-wide bg-bg text-text">
```

**Classes:** `font-sans font-light text-base leading-[140%] tracking-wide`

### Labels

```html
<span class="font-mono text-xs uppercase tracking-wide text-gray">
  Label text
</span>
```

**Classes:** `font-mono text-xs uppercase tracking-wide text-gray`

---

## Components

### Buttons

Buttons use utility classes defined in `main.css`. The `.btn` base class handles:
- Font, padding, border, transition
- Hover transform with shadow
- Active state
- Touch-friendly sizing (min-height 48px)

**Primary Button (Blue)**
```html
<button class="btn btn-primary">Submit</button>
```

**Tailwind equivalent (if not using utility):**
```html
<button class="font-mono text-sm font-normal uppercase tracking-wide
  py-[14px] px-5 md:py-[16.5px] md:px-[22px] min-h-12
  border-2 border-text rounded-sm
  bg-primary text-text cursor-pointer
  transition-all duration-[120ms] ease-in-out
  hover:translate-x-[7px] hover:-translate-y-[7px] hover:shadow-offset-hover hover:bg-primary-hover
  active:translate-x-[2px] active:-translate-y-[2px]">
  Submit
</button>
```

**Outline Button**
```html
<button class="btn btn-outline">Clear</button>
```

**Classes:** Same as primary, but `bg-transparent hover:bg-white`

**Success Button**
```html
<button class="btn btn-success">New Game</button>
```

**Classes:** Same as primary, but `bg-success`

**Disabled State**
```html
<button class="btn btn-primary" disabled>
  <!-- Automatically styled via CSS -->
</button>
```

```css
/* In main.css */
.btn:disabled {
  color: var(--color-gray);
  background-color: var(--color-bg);
  border-color: var(--color-gray);
  cursor: not-allowed;
  transform: none;
}
```

---

### Cards

**Theme Definition (`main.css`):**
```css
@theme {
  --shadow-offset-sm: -4px 4px 0px 0px #383838;
  --shadow-offset-md: -6px 6px 0px 0px #383838;
  --shadow-offset-lg: -8px 8px 0px 0px #383838;
}
```

**Tailwind Classes:**
```html
<div class="bg-white border-2 border-text shadow-offset-lg p-6">
  <h2>Card Title</h2>
  <p>Card content goes here.</p>
</div>
```

**Shadow sizes:**
| Size | Tailwind Class | Usage |
|------|----------------|-------|
| Small | `shadow-offset-sm` | Badges, small elements |
| Medium | `shadow-offset-md` | Cards, panels |
| Large | `shadow-offset-lg` | Main content cards |
| Hover | `shadow-offset-hover` | Button hover state |

**Responsive Shadow:**
```html
<!-- Smaller shadow on mobile, larger on desktop -->
<div class="shadow-offset-md md:shadow-offset-lg">
```

---

### Badges / Tags

```html
<span class="inline-flex items-center bg-accent border-2 border-text
  py-2 px-4 font-mono text-sm shadow-offset-sm">
  30s
</span>
```

**Warning variant:**
```html
<span class="inline-flex items-center bg-error border-2 border-text
  py-2 px-4 font-mono text-sm shadow-offset-sm text-white">
  10s
</span>
```

---

### List Items

```html
<div class="flex items-center gap-3 py-2 px-3 bg-bg border border-text transition-all duration-150">
  <!-- Content -->
</div>
```

**First item (highlighted):**
```html
<div class="flex items-center gap-3 py-2 px-3 bg-accent border-2 border-text transition-all duration-150">
  <!-- Top prediction -->
</div>
```

**Correct state (first item):**
```html
<div class="flex items-center gap-3 py-2 px-3 bg-success border-2 border-text">
  <!-- Correct answer -->
</div>
```

---

### Progress Bars

```html
<div class="w-[100px] h-2 bg-white border border-text overflow-hidden">
  <div class="h-full bg-primary transition-[width] duration-200 ease-out"
    style="width: 75%">
  </div>
</div>
```

**Responsive width:**
```html
<div class="w-[60px] md:w-[100px] h-2 bg-white border border-text overflow-hidden">
```

**Highlighted variant (first item):**
```html
<div class="h-full bg-text transition-[width] duration-200 ease-out">
```

---

## Layout

### Container

```html
<div class="max-w-[1302px] mx-auto px-6 xl:px-[30px]">
  <!-- Content -->
</div>
```

### Breakpoints

Tailwind defaults + custom:
| Name | Width | Tailwind Prefix |
|------|-------|-----------------|
| Mobile | < 728px | (default) |
| Tablet | ≥ 728px | `md:` |
| Desktop | ≥ 960px | `lg:` |
| Wide | ≥ 1302px | `xl:` |

**Note:** Configure custom breakpoints in `tailwind.config.js` if needed:
```js
theme: {
  screens: {
    'md': '728px',
    'lg': '960px',
    'xl': '1302px',
  }
}
```

---

## Animations

### Fade In (defined in `main.css`)

```css
@keyframes fadeIn {
  0% {
    opacity: 0;
    transform: translateY(1rem);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

.fade-in {
  animation: fadeIn 0.3s ease forwards;
}
```

**Usage:**
```html
<div class="fade-in">Animated content</div>
```

### Smooth Transitions

```html
<!-- UI state changes -->
<div class="transition-all duration-150 ease-out">

<!-- Progress bars -->
<div class="transition-[width] duration-200 ease-out">
```

### Hover Transform (Buttons)

```html
<button class="transition-transform duration-[120ms] ease-in-out
  hover:translate-x-[7px] hover:-translate-y-[7px]
  active:translate-x-[2px] active:-translate-y-[2px]">
```

---

## States

### Disabled

Defined in `.btn:disabled` in `main.css`:
```css
.btn:disabled {
  color: var(--color-gray);
  background-color: var(--color-bg);
  border-color: var(--color-gray);
  cursor: not-allowed;
  transform: none;
}
```

**Tailwind equivalent:**
```html
<button disabled class="disabled:text-gray disabled:bg-bg disabled:border-gray
  disabled:cursor-not-allowed disabled:transform-none">
```

### Game Over

```html
<div class="opacity-70 pointer-events-none">
  <!-- Canvas card when game is over -->
</div>
```

### Score Display

```html
<!-- Win -->
<span class="font-mono text-5xl text-success">87%</span>

<!-- Lose -->
<span class="font-mono text-5xl text-error">12%</span>
```

---

## Mobile / Responsive

### Touch Targets

**Minimum size: 48px** (iOS/Android recommendation)

```html
<button class="min-h-12 py-[14px] px-5 md:py-[16.5px] md:px-[22px]">
```

### Hover Effects (Touch vs Mouse)

Use `@media (hover: hover)` in CSS to apply hover only on mouse devices:

```css
/* In main.css */
@media (hover: hover) {
  .btn:hover {
    transform: translate(7px, -7px);
    box-shadow: var(--shadow-offset-hover);
  }
}

.btn:active {
  transform: translate(2px, -2px);
}
```

**Note:** Tailwind's `hover:` modifier applies to all devices. For touch-friendly hover, define in CSS.

### Responsive Canvas

```html
<canvas class="w-full h-auto max-w-[400px] touch-none">
</canvas>
```

`touch-none` = `touch-action: none` (prevents scroll while drawing)

**JavaScript coordinate scaling:**
```js
function getPos(e) {
  const rect = canvas.getBoundingClientRect();
  const scaleX = canvas.width / rect.width;
  const scaleY = canvas.height / rect.height;
  const x = (clientX - rect.left) * scaleX;
  const y = (clientY - rect.top) * scaleY;
  return { x, y };
}
```

### Safe Area Insets (Notched Phones)

```css
/* In main.css */
body {
  padding: env(safe-area-inset-top) env(safe-area-inset-right)
           env(safe-area-inset-bottom) env(safe-area-inset-left);
}
```

### Mobile Meta Tags

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<meta name="theme-color" content="#F4EFEA">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
```

### Responsive Spacing

```html
<!-- Mobile-first spacing -->
<main class="py-6 gap-5 md:py-12 md:gap-8">
```

---

## Quick Reference

### Tailwind Class Mapping

| Pure CSS | Tailwind |
|----------|----------|
| `background-color: #F4EFEA` | `bg-bg` |
| `color: #383838` | `text-text` |
| `font-family: 'Space Mono'` | `font-mono` |
| `font-family: 'Inter'` | `font-sans` |
| `box-shadow: -6px 6px...` | `shadow-offset-md` |
| `padding: 24px` | `p-6` |
| `border: 2px solid` | `border-2 border-text` |
| `text-transform: uppercase` | `uppercase` |
| `letter-spacing: 0.02em` | `tracking-wide` |
| `font-size: 14px` | `text-sm` |
| `max-width: 400px` | `max-w-[400px]` |
| `gap: 12px` | `gap-3` |
| `min-height: 48px` | `min-h-12` |

### Do's ✓
- Use `font-mono` for all UI text (buttons, labels, headings)
- Use `font-sans` for body/paragraph text only
- Always `uppercase` UI text
- Use `shadow-offset-*` for offset shadows
- Use `border-2 border-text` borders
- Use `.btn` utility from `main.css` for buttons

### Don'ts ✗
- Don't use `rounded-*` (except `rounded-sm` on buttons)
- Don't use Tailwind's default shadows (only `shadow-offset-*`)
- Don't use gradients
- Don't mix fonts within UI elements
- Don't use colors outside the theme palette

---

## Example Components

### Prediction Item (Live Stream)

```html
<div class="flex items-center gap-3 py-2 px-3 bg-bg border border-text
  first:bg-accent first:border-2 transition-all duration-150">

  <span class="font-mono text-sm uppercase tracking-wide flex-1">
    CAT
  </span>

  <div class="w-[60px] md:w-[100px] h-2 bg-white border border-text overflow-hidden">
    <div class="h-full bg-primary first:bg-text transition-[width] duration-200 ease-out"
      style="width: 87%">
    </div>
  </div>

  <span class="font-mono text-xs text-gray min-w-[40px] text-right">
    87%
  </span>
</div>
```

---

### Final Result Card

```html
<div class="p-5 md:p-6 bg-white border-2 border-text shadow-offset-md
  w-[calc(100%-12px)] max-w-[400px]">

  <div class="flex justify-between items-center py-3 border-b border-text">
    <span class="font-mono text-sm uppercase text-gray tracking-wide">Result</span>
    <span class="font-mono text-2xl md:text-[28px] uppercase tracking-wide text-success">
      CAT
    </span>
  </div>

  <div class="flex justify-between items-center py-3">
    <span class="font-mono text-sm uppercase text-gray tracking-wide">Confidence</span>
    <span class="font-mono text-2xl md:text-[28px] uppercase tracking-wide text-success">
      87%
    </span>
  </div>
</div>
```

**Fail variant:** Replace `text-success` with `text-error`

---

### Prompt Examples

```html
<div class="space-y-2">
  <p class="font-mono text-sm uppercase text-gray tracking-wide">
    Draw something like:
  </p>
  <p class="font-mono text-sm md:text-base uppercase tracking-wide text-text
    max-w-[400px] leading-[160%]">
    Cat, House, Tree, Car, Sun, Flower...
  </p>
</div>
```

---

## Theme Files

All custom theme values are defined in `frontend/src/styles/main.css`:

```css
@import "tailwindcss";

@theme {
  /* Colors */
  --color-bg: #F4EFEA;
  --color-text: #383838;
  --color-primary: #6FC2FF;
  --color-primary-hover: #2BA5FF;
  --color-accent: #FFDE00;
  --color-success: #53DBC9;
  --color-error: #FF7169;
  --color-gray: #A1A1A1;

  /* Fonts */
  --font-mono: "Space Mono", monospace;
  --font-sans: "Inter", Arial, sans-serif;

  /* Offset Shadows */
  --shadow-offset-sm: -4px 4px 0px 0px #383838;
  --shadow-offset-md: -6px 6px 0px 0px #383838;
  --shadow-offset-lg: -8px 8px 0px 0px #383838;
  --shadow-offset-hover: -7px 7px 0px 0px #383838;
}
```
