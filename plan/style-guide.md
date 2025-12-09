# Guessme Design Style Guide

Based on MotherDuck design system. Use this guide to maintain visual consistency.

## Color Palette

```css
:root {
  --bg: #F4EFEA;          /* Warm cream - page background */
  --text: #383838;        /* Dark charcoal - text, borders */
  --primary: #6FC2FF;     /* Light blue - primary buttons */
  --primary-hover: #2BA5FF; /* Medium blue - button hover */
  --accent: #FFDE00;      /* Yellow - highlights, timer */
  --success: #53DBC9;     /* Teal - success states */
  --error: #FF7169;       /* Coral - error, warning */
  --white: #FFFFFF;       /* White - cards, inputs */
  --gray: #A1A1A1;        /* Gray - secondary text */
}
```

| Color | Hex | Usage |
|-------|-----|-------|
| Background | `#F4EFEA` | Page bg |
| Text | `#383838` | All text, borders, shadows |
| Primary | `#6FC2FF` | Primary buttons |
| Accent | `#FFDE00` | Highlights, top items |
| Success | `#53DBC9` | Correct, win states |
| Error | `#FF7169` | Wrong, timer warning |

---

## Typography

### Fonts

```css
/* Headlines, labels, buttons */
font-family: 'Space Mono', monospace;

/* Body text */
font-family: 'Inter', Arial, sans-serif;
```

**Google Fonts import:**
```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
```

### Heading Scale (h1)

```css
h1 {
  font-family: 'Space Mono', monospace;
  font-weight: 400;
  text-transform: uppercase;
  letter-spacing: 0.02em;
  line-height: 140%;
  font-size: 30px;  /* mobile */
}

@media (min-width: 728px) {
  h1 { font-size: 56px; line-height: 120%; }
}

@media (min-width: 960px) {
  h1 { font-size: 80px; }
}
```

### Body Text

```css
body {
  font-family: 'Inter', Arial, sans-serif;
  font-weight: 300;
  font-size: 16px;
  line-height: 140%;
  letter-spacing: 0.02em;
}
```

### Labels

```css
.label {
  font-family: 'Space Mono', monospace;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.02em;
  color: var(--gray);
}
```

---

## Components

### Buttons

**Primary Button (Blue)**
```css
.btn-primary {
  font-family: 'Space Mono', monospace;
  font-size: 14px;
  font-weight: 400;
  text-transform: uppercase;
  letter-spacing: 0.02em;
  padding: 16.5px 22px;
  border: 2px solid var(--text);
  border-radius: 2px;
  background-color: var(--primary);
  color: var(--text);
  cursor: pointer;
  transition: transform 120ms ease-in-out, background-color 120ms ease-in-out;
}

.btn-primary:hover {
  transform: translate(7px, -7px);
  background-color: var(--primary-hover);
}

.btn-primary:active {
  transform: translate(2px, -2px);
}
```

**Outline Button**
```css
.btn-outline {
  /* Same base as primary */
  background-color: transparent;
  color: var(--text);
}

.btn-outline:hover {
  background-color: var(--white);
}
```

**Success Button**
```css
.btn-success {
  background-color: var(--success);
  color: var(--text);
}
```

**Example:**
```html
<button class="btn btn-primary">Submit</button>
<button class="btn btn-outline">Clear</button>
<button class="btn btn-success">New Game</button>
```

---

### Cards

```css
.card {
  background-color: var(--white);
  border: 2px solid var(--text);
  box-shadow: -8px 8px 0px 0px var(--text);
  padding: 24px;
}
```

**Shadow sizes:**
| Size | Value | Usage |
|------|-------|-------|
| Small | `-4px 4px 0px 0px` | Badges, small elements |
| Medium | `-6px 6px 0px 0px` | Cards, panels |
| Large | `-8px 8px 0px 0px` | Main content cards |

**Example:**
```html
<div class="card">
  <h2>Card Title</h2>
  <p>Card content goes here.</p>
</div>
```

---

### Badges / Tags

```css
.badge {
  display: inline-flex;
  align-items: center;
  background-color: var(--accent);
  border: 2px solid var(--text);
  padding: 8px 16px;
  font-family: 'Space Mono', monospace;
  font-size: 14px;
  box-shadow: -4px 4px 0px 0px var(--text);
}

.badge--warning {
  background-color: var(--error);
  color: var(--white);
}
```

**Example:**
```html
<span class="badge">30s</span>
<span class="badge badge--warning">10s</span>
```

---

### List Items

```css
.list-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 12px;
  background-color: var(--bg);
  border: 1px solid var(--text);
  transition: all 150ms ease;
}

/* First item (highlighted) */
.list-item:first-child {
  background-color: var(--accent);
  border-width: 2px;
}

/* Correct state */
.list-item.correct:first-child {
  background-color: var(--success);
}
```

---

### Progress Bars

```css
.progress-bar {
  width: 100px;
  height: 8px;
  background-color: var(--white);
  border: 1px solid var(--text);
  overflow: hidden;
}

.progress-bar__fill {
  height: 100%;
  background-color: var(--primary);
  transition: width 200ms ease;
}

/* Highlighted variant */
.list-item:first-child .progress-bar__fill {
  background-color: var(--text);
}
```

**Example:**
```html
<div class="progress-bar">
  <div class="progress-bar__fill" style="width: 75%"></div>
</div>
```

---

## Layout

### Container

```css
.container {
  max-width: 1302px;
  margin: 0 auto;
  padding: 0 24px;
}

@media (min-width: 1302px) {
  .container {
    padding: 0 30px;
  }
}
```

### Breakpoints

| Name | Width | Usage |
|------|-------|-------|
| Mobile | < 728px | Base styles |
| Tablet | ≥ 728px | Medium adjustments |
| Desktop | ≥ 960px | Large typography |
| Wide | ≥ 1302px | Max container width |

---

## Animations

### Hover Transform (Buttons)

```css
transition: transform 120ms ease-in-out;

/* Hover */
transform: translate(7px, -7px);

/* Active/Click */
transform: translate(2px, -2px);
```

### Fade In

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

### Smooth Transitions

```css
/* UI state changes */
transition: all 150ms ease;

/* Progress bars */
transition: width 200ms ease;
```

---

## States

### Disabled

```css
.btn:disabled {
  color: var(--gray);
  background-color: var(--bg);
  border-color: var(--gray);
  cursor: not-allowed;
  transform: none;
}
```

### Game Over

```css
.game-over .canvas-card {
  opacity: 0.7;
  pointer-events: none;
}
```

### Score Display

```css
.score {
  font-family: 'Space Mono', monospace;
  font-size: 48px;
  color: var(--success);  /* Win */
}

.score--fail {
  color: var(--error);    /* Lose */
}
```

---

## Mobile / Responsive

### Breakpoints

| Name | Width | Usage |
|------|-------|-------|
| Mobile | < 728px | Base styles (mobile-first) |
| Tablet | ≥ 728px | Larger padding, wider elements |
| Desktop | ≥ 960px | Full typography scale |
| Wide | ≥ 1302px | Max container width |

### Touch Targets

**Minimum size: 48px** (iOS/Android recommendation)

```css
.btn {
  min-height: 48px;
  padding: 14px 20px;  /* mobile */
}

@media (min-width: 728px) {
  .btn {
    padding: 16.5px 22px;  /* desktop */
  }
}
```

### Hover Effects (Touch vs Mouse)

Use `@media (hover: hover)` to only apply hover effects on devices with mouse/trackpad:

```css
/* Base active state for all devices */
.btn:active {
  transform: translate(2px, -2px);
}

/* Hover only for non-touch devices */
@media (hover: hover) {
  .btn:hover {
    transform: translate(7px, -7px);
  }
}
```

### Responsive Canvas

Canvas maintains internal resolution but scales visually:

```css
#canvas {
  width: 100%;
  height: auto;
  max-width: 400px;
  touch-action: none;  /* prevents scroll while drawing */
}
```

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
body {
  padding: env(safe-area-inset-top) env(safe-area-inset-right) env(safe-area-inset-bottom) env(safe-area-inset-left);
}
```

### Mobile Meta Tags

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<meta name="theme-color" content="#F4EFEA">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
```

### Touch Event Handling

Use `{ passive: false }` to prevent page scroll while drawing:

```js
canvas.addEventListener('touchstart', handler, { passive: false });
canvas.addEventListener('touchmove', handler, { passive: false });
```

### Responsive Spacing

```css
/* Mobile-first spacing */
main {
  padding: 24px 0;
  gap: 20px;
}

/* Desktop spacing */
@media (min-width: 728px) {
  main {
    padding: 48px 0;
    gap: 32px;
  }
}
```

### Card Shadows (Responsive)

```css
/* Smaller shadow on mobile */
.card {
  box-shadow: -6px 6px 0px 0px var(--text);
}

/* Full shadow on desktop */
@media (min-width: 728px) {
  .card {
    box-shadow: -8px 8px 0px 0px var(--text);
  }
}
```

---

## Quick Reference

### Do's ✓
- Use `Space Mono` for all UI text (buttons, labels, headings)
- Use `Inter` for body/paragraph text only
- Always uppercase UI text (`text-transform: uppercase`)
- Use offset shadows (`-Xpx Xpx 0px 0px var(--text)`)
- Use `2px solid var(--text)` borders
- Apply hover transform on interactive elements

### Don'ts ✗
- Don't use rounded corners (except `border-radius: 2px` on buttons)
- Don't use drop shadows (only offset shadows)
- Don't use gradients
- Don't mix fonts within UI elements
- Don't use colors outside the palette

---

## Example Components

### Prediction Item (Live Stream)

```html
<div class="prediction-item">
  <span class="prediction-name">CAT</span>
  <div class="prediction-bar">
    <div class="prediction-bar-fill" style="width: 87%"></div>
  </div>
  <span class="prediction-confidence">87%</span>
</div>
```

```css
.prediction-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 12px;
  background-color: #F4EFEA;
  border: 1px solid #383838;
}

/* First item (top prediction) highlighted */
.prediction-item:first-child {
  background-color: #FFDE00;
  border-width: 2px;
}

.prediction-name {
  font-family: 'Space Mono', monospace;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 0.02em;
  flex: 1;
}

.prediction-bar {
  width: 60px;  /* mobile */
  height: 8px;
  background-color: #FFFFFF;
  border: 1px solid #383838;
  overflow: hidden;
}

@media (min-width: 728px) {
  .prediction-bar { width: 100px; }
}

.prediction-bar-fill {
  height: 100%;
  background-color: #6FC2FF;
  transition: width 200ms ease;
}

.prediction-confidence {
  font-family: 'Space Mono', monospace;
  font-size: 12px;
  color: #A1A1A1;
  min-width: 40px;
  text-align: right;
}
```

---

### Final Result Card

Two-row layout with label/value pairs:

```html
<div class="final-result">
  <div class="final-result-row">
    <span class="final-result-label">Result</span>
    <span class="final-result-value success">CAT</span>
  </div>
  <div class="final-result-row">
    <span class="final-result-label">Confidence</span>
    <span class="final-result-value success">87%</span>
  </div>
</div>
```

```css
.final-result {
  padding: 20px;
  background-color: var(--white);
  border: 2px solid var(--text);
  box-shadow: -6px 6px 0px 0px var(--text);
  width: calc(100% - 12px);
  max-width: 400px;
}

.final-result-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
}

.final-result-row:first-child {
  border-bottom: 1px solid var(--text);
}

.final-result-label {
  font-family: 'Space Mono', monospace;
  font-size: 14px;
  text-transform: uppercase;
  color: var(--gray);
  letter-spacing: 0.02em;
}

.final-result-value {
  font-family: 'Space Mono', monospace;
  font-size: 24px;
  text-transform: uppercase;
  color: var(--text);
  letter-spacing: 0.02em;
}

.final-result-value.success {
  color: var(--success);
}

.final-result-value.fail {
  color: var(--error);
}

@media (min-width: 728px) {
  .final-result { padding: 24px; }
  .final-result-value { font-size: 28px; }
}
```

---

### Prompt Examples

Display suggested drawing options:

```html
<div class="prompt-section">
  <p class="prompt-label">Draw something like:</p>
  <p class="prompt-examples">Cat, House, Tree, Car, Sun, Flower...</p>
</div>
```

```css
.prompt-label {
  font-family: 'Space Mono', monospace;
  font-size: 14px;
  text-transform: uppercase;
  color: var(--gray);
  margin-bottom: 8px;
  letter-spacing: 0.02em;
}

.prompt-examples {
  font-family: 'Space Mono', monospace;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 0.02em;
  color: var(--text);
  max-width: 400px;
  line-height: 160%;
}

@media (min-width: 728px) {
  .prompt-examples { font-size: 16px; }
}
```
