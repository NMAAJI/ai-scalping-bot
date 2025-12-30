# Design System - Quick Reference Card

## 🎯 Quick Start

### 1. Link CSS in HTML Head
```html
<link rel="stylesheet" href="/static/design-system.css">
```

### 2. Use Design System Classes
```html
<!-- Cards -->
<div class="card">Content here</div>

<!-- Buttons -->
<button class="btn-primary">Click me</button>
<button class="btn-success">Success</button>
<button class="btn-danger">Danger</button>
<button class="btn-secondary">Secondary</button>

<!-- Stat Cards -->
<div class="stat-card">
    <div class="stat-label">Title</div>
    <div class="stat-value">123</div>
    <div class="stat-change positive">↑ 5%</div>
</div>

<!-- Status Indicators -->
<div class="status-indicator">
    <div class="status-dot online"></div>
    <span>API Status</span>
</div>

<!-- Badges -->
<span class="badge badge-success">✓ Active</span>
<span class="badge badge-danger">✗ Offline</span>
<span class="badge badge-warning">⚠ Pending</span>

<!-- Alerts -->
<div class="alert alert-success">Success message</div>
<div class="alert alert-danger">Error message</div>
<div class="alert alert-warning">Warning message</div>

<!-- Confidence Meter -->
<div class="confidence-meter">
    <div class="confidence-fill" style="width: 75%">75%</div>
</div>

<!-- Toggle Switch -->
<label class="toggle-switch">
    <input type="checkbox" checked>
    <span class="toggle-slider"></span>
</label>

<!-- Table -->
<table class="data-table">
    <thead><tr><th>Column 1</th><th>Column 2</th></tr></thead>
    <tbody><tr><td>Data 1</td><td>Data 2</td></tr></tbody>
</table>

<!-- Grid Layouts -->
<div class="grid-2">
    <div class="card">Item 1</div>
    <div class="card">Item 2</div>
</div>

<div class="grid-3">Item 1</div><div class="grid-3">Item 2</div><div class="grid-3">Item 3</div>

<div class="grid-4">Item 1</div><!-- repeat 4 items -->

<!-- Forms -->
<label>Field Label</label>
<input type="text" placeholder="Enter text">
<select><option>Select option</option></select>
<textarea placeholder="Enter text"></textarea>
```

---

## 🎨 Color Reference

### Variables (Use in CSS)
```css
--primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%)
--success: #00cc66
--danger: #ff4444
--warning: #ffaa00
--neutral-dark: #333333
--neutral-medium: #666666
--neutral-light: #ddd
--neutral-lighter: #eee
--neutral-lightest: #f9f9f9
```

### Hex Values (Direct Use)
| Color | Hex | Class | Usage |
|-------|-----|-------|-------|
| Primary Purple | #667eea | `.btn-primary` | Main actions |
| Dark Purple | #764ba2 | Gradient | Accents |
| Success | #00cc66 | `.badge-success`, `.text-success` | Positive states |
| Danger | #ff4444 | `.badge-danger`, `.text-danger` | Errors/losses |
| Warning | #ffaa00 | `.badge-warning` | Cautions |

---

## 📐 Spacing Scale

```css
--spacing-xs: 8px
--spacing-sm: 12px
--spacing-md: 16px
--spacing-lg: 20px
--spacing-xl: 25px
--spacing-2xl: 30px
```

**Utility Classes:**
```html
<!-- Margin Top -->
<div class="mt-1">8px margin-top</div>
<div class="mt-2">12px margin-top</div>
<div class="mt-3">16px margin-top</div>
<div class="mt-4">20px margin-top</div>
<div class="mt-5">25px margin-top</div>

<!-- Margin Bottom (same scale: mb-1 to mb-5) -->
<!-- Padding (same scale: p-1 to p-5) -->
```

---

## 🔤 Typography

### Font Families
```css
font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
```

### Font Weights
- **Normal**: 400 - Body text
- **Medium**: 500 - Secondary headings
- **Semibold**: 600 - Labels, badges
- **Bold**: 700 - Main headings

### Font Sizes
```html
<h1>Heading 1</h1>  <!-- 2.5em (40px) -->
<h2>Heading 2</h2>  <!-- 2em (32px) -->
<h3>Heading 3</h3>  <!-- 1.5em (24px) -->
<h4>Heading 4</h4>  <!-- 1.25em (20px) -->
<p>Paragraph</p>    <!-- 1em (16px) -->

<!-- Size Utilities -->
<span class="text-sm">Small (0.85em)</span>
<span class="text-lg">Large (1.15em)</span>
<span class="text-xl">Extra Large (1.35em)</span>
```

### Text Utilities
```html
<div class="text-center">Centered text</div>
<div class="text-right">Right-aligned text</div>
<div class="text-left">Left-aligned text</div>

<div class="text-success">Green text</div>
<div class="text-danger">Red text</div>
<div class="text-warning">Orange text</div>
<div class="text-muted">Gray text</div>

<div class="font-bold">Bold text</div>
<div class="font-semibold">Semibold text</div>
<div class="font-medium">Medium text</div>
```

---

## ✨ Animations

| Name | Duration | Use Case |
|------|----------|----------|
| `pulse` | 2s | Status indicators |
| `blink` | 1s | Activity badges |
| `spin` | 1s | Loading spinner |
| `slideIn` | 0.3s | Notifications, modals |
| `slideOut` | 0.3s | Dismiss animations |

---

## 🛠️ Flex Utilities

```html
<!-- Center all items -->
<div class="flex-center">
    <icon></icon>
    <span>Loading</span>
</div>

<!-- Space between (justify-content: space-between) -->
<div class="flex-between">
    <h2>Title</h2>
    <button>Action</button>
</div>
```

---

## 📱 Responsive Breakpoints

| Breakpoint | Width | Usage |
|-----------|-------|-------|
| Desktop | > 1200px | 4-column grids |
| Tablet | 768-1200px | 2-column grids |
| Mobile | < 768px | 1-column grids |
| Small Mobile | < 480px | Full width, condensed |

**Auto-responsive grids:**
```html
<!-- Automatically adjusts columns -->
<div class="grid-2">Items auto-fit</div>
<div class="grid-3">Items auto-fit</div>
<div class="grid-4">Items auto-fit</div>
```

---

## 🔘 Button States

### Normal State
```html
<button class="btn-primary">Click me</button>
```

### Hover State
- Transform: `translateY(-2px)`
- Shadow: Enhanced
- Opacity: 100%

### Disabled State
```html
<button class="btn-primary" disabled>Disabled</button>
```
- Opacity: 50%
- Cursor: not-allowed

---

## 🎯 Component Anatomy

### Card Structure
```html
<div class="card">
    <h3>Card Title</h3>
    <p>Card content</p>
</div>
```
- **Background**: Glass effect (rgba(255, 255, 255, 0.95))
- **Backdrop Filter**: blur(10px)
- **Border Radius**: 15px
- **Padding**: 25px
- **Shadow**: 0 8px 32px rgba(0, 0, 0, 0.1)

### Stat Card Structure
```html
<div class="stat-card">
    <div class="stat-label">Label</div>
    <div class="stat-value">123</div>
    <div class="stat-change positive">↑ 5%</div>
    <div class="stat-subtext">Additional info</div>
</div>
```

### Status Indicator Structure
```html
<div class="status-indicator">
    <div class="status-dot online"></div>
    <span>Status Text</span>
</div>
```

### Badge Structure
```html
<span class="badge badge-success">Label</span>
```

### Alert Structure
```html
<div class="alert alert-success">
    <strong>Title</strong><br>
    Message text
</div>
```

### Table Structure
```html
<table class="data-table">
    <thead>
        <tr><th>Header 1</th><th>Header 2</th></tr>
    </thead>
    <tbody>
        <tr><td>Data 1</td><td>Data 2</td></tr>
    </tbody>
</table>
```

---

## 🎨 Custom Styling Tips

### Override Variables
```css
:root {
    --primary-purple: #your-color;
    --success: #your-color;
    /* etc */
}
```

### Combining Classes
```html
<!-- Multiple utilities work together -->
<div class="card mt-4 mb-3 p-5">Content</div>

<!-- Grid + Utilities -->
<div class="grid-2 mb-4">
    <div class="stat-card">Item 1</div>
    <div class="stat-card">Item 2</div>
</div>
```

### Add Custom Styles
```html
<style>
    .my-custom-class {
        background: var(--primary-gradient);
        padding: var(--spacing-lg);
        border-radius: var(--radius-md);
    }
</style>
```

---

## ✅ Common Patterns

### Header Section
```html
<div class="header">
    <div class="header-content">
        <div>
            <h1>Page Title</h1>
            <p>Subtitle or description</p>
        </div>
        <div class="header-actions">
            <button class="btn-primary">Action 1</button>
            <button class="btn-secondary">Action 2</button>
        </div>
    </div>
</div>
```

### Statistics Dashboard
```html
<div class="stats-grid">
    <div class="stat-card">
        <div class="stat-label">Metric 1</div>
        <div class="stat-value">123</div>
        <div class="stat-change positive">↑ 5%</div>
    </div>
    <!-- Repeat for more stats -->
</div>
```

### Status Section
```html
<div class="grid-3">
    <div class="status-indicator">
        <div class="status-dot online"></div>
        <span>System 1</span>
    </div>
    <!-- Repeat for more statuses -->
</div>
```

### Data Table with Badges
```html
<table class="data-table">
    <thead>
        <tr>
            <th>Name</th>
            <th>Status</th>
            <th>Action</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Item Name</td>
            <td><span class="badge badge-success">Active</span></td>
            <td><button class="btn-secondary">Edit</button></td>
        </tr>
    </tbody>
</table>
```

### Form Section
```html
<div class="card">
    <h3>Form Title</h3>
    <form>
        <label>Field 1</label>
        <input type="text" placeholder="Enter text">
        
        <label>Field 2</label>
        <input type="number" placeholder="Enter number">
        
        <button class="btn-primary mt-4">Submit</button>
    </form>
</div>
```

---

## 🚀 Performance Tips

1. **Use CSS variables** for consistent theming
2. **Minimize custom CSS** by leveraging utilities
3. **Use grid system** for responsive layouts
4. **Leverage backdrop-filter** for glass effect (hardware accelerated)
5. **Use animations sparingly** on interactive elements
6. **Apply transforms** instead of position changes (better performance)

---

## 📚 Component Showcase

Visit `/design-showcase` to see all components in action.

---

## 🔗 File Structure

```
web/
├── static/
│   └── design-system.css          ← Main CSS file (import this)
├── templates/
│   ├── dashboard_v3.html          ← Main dashboard
│   └── design-showcase.html       ← Component showcase
└── README.md

Root/
└── DESIGN_SYSTEM_GUIDE.md         ← Full documentation
```

---

## 💡 Pro Tips

1. **Responsive by Default**: Grid layouts automatically adjust
2. **Dark Mode Ready**: Supports `prefers-color-scheme: dark`
3. **Accessibility Built-in**: WCAG AA compliance
4. **No Frameworks**: Pure CSS + HTML (no React, Vue, etc)
5. **Easy Customization**: All colors/spacing as CSS variables
6. **Mobile Optimized**: Automatic font/spacing adjustments

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Colors look off | Ensure CSS file is linked |
| Buttons not styled | Check class names (btn-primary, etc) |
| Grid not responsive | Grid classes auto-adjust (no media queries needed) |
| Animations slow | Check browser performance, reduce simultaneous animations |
| Text hard to read | Check contrast ratio meets WCAG AA (4.5:1) |

---

## 📞 Need Help?

1. Check `DESIGN_SYSTEM_GUIDE.md` for detailed documentation
2. Visit `/design-showcase` for visual examples
3. Review component anatomy section above
4. Check CSS variables in `design-system.css`

---

**Last Updated:** December 2025  
**Version:** 1.0.0  
**Status:** Production Ready ✅
