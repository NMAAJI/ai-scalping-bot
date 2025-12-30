# AI Trading Bot - Design System Guide v1.0

**Complete Design System Reference for Professional Dashboard**

---

## 📋 Table of Contents

1. [Color Palette](#color-palette)
2. [Typography](#typography)
3. [Component Library](#component-library)
4. [Animations](#animations)
5. [Layout & Spacing](#layout--spacing)
6. [Responsive Design](#responsive-design)
7. [Accessibility](#accessibility)
8. [Usage Examples](#usage-examples)
9. [Implementation Checklist](#implementation-checklist)

---

## 🎨 Color Palette

### Primary Gradient
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```
- **Start Color**: `#667eea` (Primary Purple)
- **End Color**: `#764ba2` (Dark Purple)
- **Usage**: Headers, buttons, primary CTAs

### Semantic Colors

| Color | Value | Usage |
|-------|-------|-------|
| **Success** | `#00cc66` | Positive states, online status, gains |
| **Danger** | `#ff4444` | Errors, offline status, losses |
| **Warning** | `#ffaa00` | Caution, pending, neutral signals |

### Neutral Palette

| Level | Value | Usage |
|-------|-------|-------|
| **Dark** | `#333333` | Primary text, dark backgrounds |
| **Medium** | `#666666` | Secondary text, labels |
| **Light** | `#ddd` | Borders, dividers |
| **Lighter** | `#eee` | Background accents |
| **Lightest** | `#f9f9f9` | Subtle backgrounds |

### Glassmorphism Colors
```css
--glass-light: rgba(255, 255, 255, 0.95);    /* Light frosted glass */
--glass-dark: rgba(255, 255, 255, 0.1);      /* Dark frosted glass */
--glass-blur: blur(10px);                     /* Backdrop filter */
```

---

## 🔤 Typography

### Font Family
```css
font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
```

### Font Weights
| Weight | Value | Usage |
|--------|-------|-------|
| Normal | 400 | Body text, descriptions |
| Medium | 500 | Secondary headings |
| Semibold | 600 | Labels, badges, subheadings |
| Bold | 700 | Primary headings, emphasis |

### Font Sizes

#### Headings
```html
<h1>Page Title</h1>        /* 2.5em / 40px */
<h2>Section Title</h2>     /* 2em / 32px */
<h3>Subsection</h3>        /* 1.5em / 24px */
<h4>Component Title</h4>   /* 1.25em / 20px */
```

#### Body Text
```html
<p>Standard text</p>       /* 1em / 16px - 400 weight */
<span class="text-lg">Large</span>    /* 1.15em / 18px */
<span class="text-sm">Small</span>    /* 0.85em / 14px */
```

#### Special Cases
- **Stat Values**: `2em / 700 weight` (High contrast)
- **Labels**: `0.85em / 600 weight / uppercase`
- **Captions**: `0.8em / 400 weight` (Subtle)

---

## 🧩 Component Library

### 1. Cards
Basic container for content with glassmorphic styling.

```html
<div class="card">
    <h3>Card Title</h3>
    <p>Card content goes here.</p>
</div>
```

**CSS Classes:**
- `.card` - Standard card
- `.card:hover` - Lift effect on hover
- `.card-dark` - Dark variant

**Styling:**
- Background: `rgba(255, 255, 255, 0.95)`
- Backdrop Filter: `blur(10px)`
- Border: `1px solid rgba(255, 255, 255, 0.2)`
- Border Radius: `15px`
- Padding: `25px`
- Shadow: `0 8px 32px rgba(0, 0, 0, 0.1)`

---

### 2. Buttons

#### Primary Button
```html
<button class="btn-primary">Start Trading</button>
```
- **Color**: Purple gradient
- **State On Hover**: Lift effect (`translateY(-2px)`)
- **Shadow**: `0 5px 15px rgba(0, 0, 0, 0.2)`

#### Success Button
```html
<button class="btn-success">Confirm</button>
```
- **Color**: `#00cc66`
- **State On Hover**: Lift + Green shadow

#### Danger Button
```html
<button class="btn-danger">Delete</button>
```
- **Color**: `#ff4444`
- **State On Hover**: Lift + Red shadow

#### Secondary Button
```html
<button class="btn-secondary">Cancel</button>
```
- **Background**: `rgba(255, 255, 255, 0.1)`
- **Border**: `2px solid rgba(255, 255, 255, 0.2)`
- **State On Hover**: Border turns purple

**Button Properties:**
- Padding: `12px 20px`
- Border Radius: `10px`
- Font Weight: `600`
- Text Transform: `uppercase`
- Letter Spacing: `0.5px`
- Transition: `0.2s ease`

---

### 3. Stat Cards
Display important metrics with value and change indicator.

```html
<div class="stat-card">
    <div class="stat-label">Total Trades</div>
    <div class="stat-value">48</div>
    <div class="stat-change positive">↑ 12% This Week</div>
</div>
```

**Components:**
- `.stat-label` - Uppercase label (0.85em, 600 weight, muted color)
- `.stat-value` - Large bold value (2em, gradient color)
- `.stat-change` - Change indicator
  - `.positive` - Green text
  - `.negative` - Red text
- `.stat-subtext` - Additional info (optional)

---

### 4. Badges
Small labeled indicators for status or categorization.

```html
<span class="badge badge-success">Active</span>
<span class="badge badge-danger">Offline</span>
<span class="badge badge-warning">Pending</span>
```

**Variants:**
- `.badge-success` - Green with checkmark
- `.badge-danger` - Red with X
- `.badge-warning` - Orange with alert
- `.badge-status` - With animated dot

**Properties:**
- Padding: `12px 20px`
- Border Radius: `20px` (Pill shape)
- Font Size: `0.85em`
- Text Transform: `uppercase`

---

### 5. Status Indicators
Show API/Service health status with animated dot.

```html
<div class="status-indicator">
    <div class="status-dot online"></div>
    <span>Binance API: Online</span>
</div>
```

**States:**
- `.online` - Green, pulsing animation
- `.offline` - Red, no animation

**CSS:**
```css
animation: pulse 2s infinite;
box-shadow: 0 0 10px rgba(0, 204, 102, 1);
```

---

### 6. Toggle Switch
Enable/disable feature with smooth animation.

```html
<label class="toggle-switch">
    <input type="checkbox" checked>
    <span class="toggle-slider"></span>
</label>
```

**Properties:**
- Width: `50px`
- Height: `26px`
- Checked Color: `#00cc66`
- Animation: `0.2s ease`

---

### 7. Confidence Meter
Visual representation of confidence level (0-100%).

```html
<div class="confidence-meter">
    <div class="confidence-fill" style="width: 75%">75%</div>
</div>
```

**Gradient:**
```
Red (#ff4444) → Orange (#ffaa00) → Green (#00cc66)
```

**Height:** `30px`
**Border Radius:** `15px`

---

### 8. Data Tables

```html
<table class="data-table">
    <thead>
        <tr>
            <th>Symbol</th>
            <th>Price</th>
            <th>Change</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>BTCUSDT</td>
            <td>$67,500</td>
            <td class="text-success">+2.5%</td>
        </tr>
    </tbody>
</table>
```

**Styling:**
- **Header**: Gradient background, white text, uppercase labels
- **Rows**: Border-bottom separator, hover background change
- **Padding**: `20px` per cell
- **Font Size**: `0.9em`

---

### 9. Alerts/Messages

```html
<div class="alert alert-success">✓ Trade executed successfully</div>
<div class="alert alert-danger">✗ API connection failed</div>
<div class="alert alert-warning">⚠ Unusual market movement</div>
```

**Properties:**
- Padding: `20px 25px`
- Border Left: `4px solid` (color-specific)
- Border Radius: `10px`
- Background: Light tint of color

---

### 10. Tab System

```html
<div class="tabs">
    <button class="tab-button active" onclick="switchTab('overview')">Overview</button>
    <button class="tab-button" onclick="switchTab('trades')">Trades</button>
</div>

<div id="overview" class="tab-content active">
    <!-- Content -->
</div>
```

**Active Tab Styling:**
- Border Bottom: `3px solid #667eea`
- Color: White
- No background color

---

### 11. Forms
Input fields with focus states and validation.

```html
<label>Trading Symbol</label>
<input type="text" placeholder="e.g., BTCUSDT">
```

**Styling:**
- Border: `1px solid #ddd`
- Border Radius: `10px`
- Padding: `16px`
- Focus Border Color: `#667eea`
- Focus Shadow: `0 0 0 3px rgba(102, 126, 234, 0.1)`

---

## ✨ Animations

### 1. Pulse
Used for status indicators.

```css
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.7; }
}
```
**Duration:** `2s`
**Use Case:** Live status dots

---

### 2. Blink
Used for badge indicators.

```css
@keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}
```
**Duration:** `1s`
**Use Case:** Activity indicators

---

### 3. Spin
Used for loading spinners.

```css
@keyframes spin {
    to { transform: rotate(360deg); }
}
```
**Duration:** `1s`
**Direction:** Linear infinite
**Use Case:** Loading states

---

### 4. Slide In
Used for notifications and tab content.

```css
@keyframes slideIn {
    from {
        transform: translateY(-20px);
        opacity: 0;
    }
    to {
        transform: translateY(0);
        opacity: 1;
    }
}
```
**Duration:** `0.3s`
**Use Case:** Page transitions, alerts

---

### 5. Slide Out
Used for dismissed notifications.

```css
@keyframes slideOut {
    from {
        transform: translateY(0);
        opacity: 1;
    }
    to {
        transform: translateX(400px);
        opacity: 0;
    }
}
```
**Duration:** `0.3s`
**Use Case:** Notification dismissal

---

## 📐 Layout & Spacing

### Spacing Scale
```css
--spacing-xs: 8px;      /* Small gaps */
--spacing-sm: 12px;     /* Labels to elements */
--spacing-md: 16px;     /* Standard padding */
--spacing-lg: 20px;     /* Card padding */
--spacing-xl: 25px;     /* Section padding */
--spacing-2xl: 30px;    /* Header/footer */
```

### Grid Systems

#### 2-Column Grid
```html
<div class="grid-2">
    <div class="card">Column 1</div>
    <div class="card">Column 2</div>
</div>
```

#### 3-Column Grid
```html
<div class="grid-3">
    <div class="stat-card">Stat 1</div>
    <div class="stat-card">Stat 2</div>
    <div class="stat-card">Stat 3</div>
</div>
```

#### 4-Column Grid (Desktop)
```html
<div class="grid-4">
    <div class="card">Item 1</div>
    <div class="card">Item 2</div>
    <div class="card">Item 3</div>
    <div class="card">Item 4</div>
</div>
```

**Note:** Grids automatically adjust on smaller screens.

---

### Flex Utilities

```html
<!-- Center content -->
<div class="flex-center">
    <spinner></spinner>
    <span>Loading...</span>
</div>

<!-- Space between items -->
<div class="flex-between">
    <h2>Dashboard</h2>
    <button>Settings</button>
</div>
```

---

## 📱 Responsive Design

### Breakpoints
- **Desktop**: > 1200px (4-column grids)
- **Tablet**: 768px - 1200px (2-column grids)
- **Mobile**: < 768px (1-column grids)
- **Small Mobile**: < 480px (Full width, condensed)

### Implementation Example

```html
<div class="stats-grid">  <!-- Auto-fit: repeat(auto-fit, minmax(250px, 1fr)) -->
    <div class="stat-card">...responsive by default</div>
</div>
```

### Mobile Optimizations
- Body Padding: Reduced from `20px` to `12px`
- Font Sizes: Scaled down (heading: 1.25em)
- Buttons: Full width on mobile
- Tables: Reduced font size (0.9em)

---

## ♿ Accessibility Standards

### WCAG AA Compliance

#### Color Contrast
| Element | Contrast Ratio |
|---------|---|
| Heading on Background | 7:1 |
| Body Text on Background | 4.5:1 |
| Interactive Elements | 3:1 minimum |

#### Keyboard Navigation
- All buttons: Keyboard accessible
- Focus states: Visible outline or underline
- Tab order: Logical flow

#### Screen Readers
```html
<!-- Good -->
<button aria-label="Start trading">▶</button>

<!-- Label associations -->
<label for="symbol">Trading Symbol</label>
<input id="symbol" type="text">
```

#### Color Not Sole Indicator
```html
<!-- Good - combines color + text -->
<span class="badge badge-success">✓ Active</span>

<!-- Avoid - color only -->
<div style="color: green"></div>
```

---

## 💻 Usage Examples

### Example 1: Dashboard Header
```html
<div class="header">
    <div class="header-content">
        <div>
            <h1>Trading Dashboard</h1>
            <p>Real-time autonomous trading</p>
        </div>
        <div class="header-actions">
            <button class="btn-primary">Start Trading</button>
            <button class="btn-secondary">Settings</button>
        </div>
    </div>
</div>
```

### Example 2: Statistics Section
```html
<div class="stats-grid">
    <div class="stat-card">
        <div class="stat-label">Total Trades</div>
        <div class="stat-value">157</div>
        <div class="stat-change positive">↑ 8% Today</div>
    </div>
    
    <div class="stat-card">
        <div class="stat-label">Win Rate</div>
        <div class="stat-value">62%</div>
        <div class="stat-change positive">↑ 3% This Week</div>
    </div>
</div>
```

### Example 3: API Health Status
```html
<div class="grid-3 mb-4">
    <div class="status-indicator">
        <div class="status-dot online"></div>
        <span>Binance API</span>
    </div>
    
    <div class="status-indicator">
        <div class="status-dot online"></div>
        <span>Gemini AI</span>
    </div>
    
    <div class="status-indicator">
        <div class="status-dot offline"></div>
        <span>Market Data</span>
    </div>
</div>
```

### Example 4: Trade Notification
```html
<div class="alert alert-success">
    <strong>✓ Trade Executed</strong><br>
    Sold 0.5 BTC at $67,500 | Profit: $1,250
</div>
```

### Example 5: Form Section
```html
<div class="card">
    <h3>Trade Parameters</h3>
    
    <label>Take Profit (%)</label>
    <input type="number" value="2.5" min="0.1" max="10">
    
    <label>Stop Loss (%)</label>
    <input type="number" value="1.5" min="0.1" max="5">
    
    <button class="btn-primary mt-4">Update Settings</button>
</div>
```

---

## ✅ Implementation Checklist

- [ ] Link `design-system.css` in HTML head
- [ ] Use semantic HTML with proper structure
- [ ] Apply design system classes (not inline styles)
- [ ] Test responsiveness at breakpoints
- [ ] Verify color contrast (WCAG AA)
- [ ] Test keyboard navigation
- [ ] Verify animations work smoothly
- [ ] Check mobile layout (< 768px)
- [ ] Test dark mode (prefers-color-scheme)
- [ ] Verify all components match spec
- [ ] Test in multiple browsers
- [ ] Check loading states
- [ ] Verify error states
- [ ] Test interactive elements
- [ ] Run accessibility audit

---

## 📚 Quick Reference

### CSS Variables
All design tokens are defined as CSS variables for easy customization:

```css
/* Colors */
--primary-gradient
--success
--danger
--warning

/* Spacing */
--spacing-xs to --spacing-2xl

/* Typography */
--font-family
--font-weight-*

/* Effects */
--shadow-sm to --shadow-lg
--transition-*
```

### Utility Classes
```
.flex-center          Center flex items
.flex-between         Space-between flex
.text-center          Center text
.text-success         Green text
.text-danger          Red text
.mt-/mb-/p-1-5        Margin/padding utilities
.grid-2/3/4           Grid layouts
.text-sm/lg/xl        Font size variants
```

---

## 🔄 Maintenance & Updates

**Version:** 1.0.0  
**Last Updated:** December 2025  
**Status:** Production Ready

### Future Enhancements
- [ ] Dark mode theme variants
- [ ] Additional animation presets
- [ ] Extended component library
- [ ] Accessibility improvements
- [ ] Performance optimizations

---

## 📞 Support

For questions or customizations, refer to:
1. CSS variables in `:root`
2. Component examples in this guide
3. Dashboard implementation in `dashboard_v3.html`
4. Responsive breakpoints section

---

**This design system ensures consistency, accessibility, and professional presentation across the entire AI Trading Bot platform.**
