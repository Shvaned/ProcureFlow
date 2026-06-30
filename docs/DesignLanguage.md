# ProcureFlow AI — Design Language

**Version:** 1.0.0
**Date:** 2026-06-30

---

## 1. Design Philosophy

ProcureFlow AI should feel like a premium enterprise SaaS product. The design draws inspiration from Linear, Stripe, and Vercel — minimal, professional, fast, and accessible. Every screen should appear designed by a single team with consistent spacing, typography, colors, and interaction patterns.

### Core Principles
- **Clarity over decoration**: Every element should serve a purpose
- **Content-first**: The data is the hero; chrome recedes
- **Fast feels premium**: Optimistic updates, skeleton loading, snappy transitions
- **Dark by default**: Professionally dark with a polished light mode
- **Keyboard-first**: Every action reachable via keyboard

---

## 2. Color Palette

### Dark Mode (Default)

| Token | Value | Usage |
|-------|-------|-------|
| `--background` | `#0A0A0A` | Page background |
| `--foreground` | `#FAFAFA` | Primary text |
| `--muted` | `#1A1A1A` | Card background, hover states |
| `--muted-foreground` | `#A1A1A1` | Secondary text, descriptions |
| `--border` | `#2A2A2A` | Borders, dividers |
| `--accent` | `#3B82F6` | Primary actions, links, focus rings |
| `--accent-foreground` | `#FFFFFF` | Text on accent |
| `--success` | `#22C55E` | Positive metrics, confirmed status |
| `--warning` | `#F59E0B` | Warnings, pending status |
| `--destructive` | `#EF4444` | Errors, delete actions, declined |
| `--info` | `#6366F1` | Informational, AI features |

### Light Mode

| Token | Value | Usage |
|-------|-------|-------|
| `--background` | `#FFFFFF` | Page background |
| `--foreground` | `#0A0A0A` | Primary text |
| `--muted` | `#F5F5F5` | Card background |
| `--muted-foreground` | `#737373` | Secondary text |
| `--border` | `#E5E5E5` | Borders, dividers |
| `--accent` | `#2563EB` | Primary actions, links |
| `--accent-foreground` | `#FFFFFF` | Text on accent |

### Chart Palette

For accessible data visualization:
```
#3B82F6 #22C55E #F59E0B #EF4444 #8B5CF6 #EC4899 #06B6D4 #F97316
```

---

## 3. Typography

### Font Stack

```css
--font-sans: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
--font-mono: "JetBrains Mono", "Fira Code", "Cascadia Code", monospace;
```

### Scale

| Token | Size | Line Height | Usage |
|-------|------|-------------|-------|
| `text-xs` | 0.75rem | 1rem | Labels, badges, captions |
| `text-sm` | 0.875rem | 1.25rem | Body, table cells, descriptions |
| `text-base` | 1rem | 1.5rem | Default body, form inputs |
| `text-lg` | 1.125rem | 1.75rem | Card titles, emphasized text |
| `text-xl` | 1.25rem | 1.75rem | Section headers |
| `text-2xl` | 1.5rem | 2rem | Page titles |
| `text-3xl` | 1.875rem | 2.25rem | Dashboard hero metrics |
| `text-4xl` | 2.25rem | 2.5rem | Landing page headings |

### Weights
- Regular (400): Body text
- Medium (500): Emphasized text, labels, buttons
- Semibold (600): Headings, card titles
- Bold (700): Page titles, hero metrics

---

## 4. Spacing System

| Token | Value | Usage |
|-------|-------|-------|
| `space-1` | 4px | Icon padding, tight groups |
| `space-2` | 8px | Inline spacing, badge padding |
| `space-3` | 12px | Between related elements |
| `space-4` | 16px | Card padding, form groups |
| `space-5` | 20px | Between sections |
| `space-6` | 24px | Page padding, section gaps |
| `space-8` | 32px | Major section separation |
| `space-10` | 40px | Page top/bottom padding |
| `space-12` | 48px | Hero section spacing |

---

## 5. Component Patterns

### Cards
- Background: `--muted` (dark) / `--background` with border (light)
- Border: 1px solid `--border`
- Border radius: 8px (default), 12px (dashboard overview cards)
- Padding: 16px (default), 24px (dashboard)
- Hover: subtle border color change, no scale transform
- Shadow: none by default; subtle shadow on hover for interactive cards

### Buttons
- Primary: `--accent` background, white text, 8px border radius
- Secondary: transparent background with `--border` border
- Destructive: `--destructive` background
- Ghost: transparent, hover shows `--muted` background
- Sizes: sm (32px), default (40px), lg (48px)
- Loading state: spinner replaces text, button disabled
- Focus: 2px `--accent` ring with 2px offset

### Tables
- Header: `--muted` background, `--foreground` text, medium weight
- Rows: alternating subtle backgrounds (muted / background)
- Hover: slightly lighter/darker muted background
- Selected: `--accent` with 10% opacity background
- Border: `--border` horizontal dividers only
- Cell padding: 12px 16px
- Responsive: horizontal scroll on mobile, priority columns visible

### Forms
- Inputs: `--muted` background, `--border` border, 8px radius
- Focus: 2px `--accent` ring
- Error: `--destructive` border + subtle red background
- Labels: `--foreground` text, medium weight, 8px below input
- Helper text: `--muted-foreground`, `text-sm`
- Error text: `--destructive`, `text-sm`

### Modals
- Backdrop: rgba(0, 0, 0, 0.6) blur
- Panel: `--muted` background, 12px radius, max 90vw, max 90vh
- Close: X button top-right, Esc key
- Animation: fade + scale (0.97 → 1) on enter

### Navigation
- Sidebar: fixed left, 240px width, `--muted` background
- Collapsible: 56px width when collapsed (icons only)
- Active item: `--accent` with 10% opacity background
- Navbar: 56px height, bottom border, breadcrumbs + actions
- Command Palette: ⌘K / Ctrl+K, modal overlay with search

---

## 6. Iconography

- **Lucide Icons**: Primary icon set (consistent with shadcn/ui)
- **Size**: 16px (inline), 20px (buttons), 24px (feature icons)
- **Stroke width**: 1.5px default, 2px for emphasis
- **Color**: inherit from text color

---

## 7. Animation

### Principles
- Subtle and purposeful — never decorative
- Duration: 150ms (micro), 200ms (standard), 300ms (page transitions)
- Easing: ease-out (enter), ease-in (exit)
- Respect `prefers-reduced-motion`

### Examples
- Page transitions: fade in (150ms)
- Modals: fade + scale (200ms)
- Dropdowns: expand with height animation (150ms)
- Hover states: color/border transition (150ms)
- Loading skeletons: shimmer animation
- Toast notifications: slide in from top-right (300ms), auto-dismiss (5s)
- Number changes: subtle count-up animation

---

## 8. State Patterns

### Loading
- **Skeleton**: Pulsing placeholder matching content shape (cards, table rows, text lines)
- **Spinner**: For buttons and inline loading (16px-24px)
- **Progress**: For multi-step operations (file uploads, data generation)
- **Streaming cursor**: For AI responses (blinking cursor while tokens stream)

### Empty
- Icon + title + description + CTA
- Examples: "No products yet" → "Create your first product"
- Never show blank tables or empty charts

### Error
- Icon + title + error message + retry button
- Distinguish: 404 (not found), 403 (forbidden), 500 (server error)
- AI errors: "AI is unavailable right now. You can still access all ERP features."

### Permission Denied
- Lock icon + "You don't have access to this page"
- Contact admin message + return to dashboard CTA

---

## 9. Dashboard Layout

```
┌──────────────────────────────────────────────────────┐
│ [Sidebar] │ Navbar: Breadcrumbs │ [Search] [Avatar]   │
│           ├───────────────────────────────────────────┤
│ [Nav]     │                                           │
│           │  ┌─────────┐ ┌─────────┐ ┌─────────┐     │
│ [Dash]    │  │ KPI 1   │ │ KPI 2   │ │ KPI 3   │     │
│           │  │ $12.4M  │ │ 94.2%   │ │ 2,341   │     │
│ [Products]│  └─────────┘ └─────────┘ └─────────┘     │
│           │                                           │
│ [Inventory]│  ┌──────────────────────┐ ┌───────────┐  │
│           │  │     Revenue Chart    │ │ Top       │  │
│ [Warehouse]│  │                      │ │ Products  │  │
│           │  └──────────────────────┘ └───────────┘  │
│ [Suppliers]│                                           │
│           │  ┌──────────────────────────────────────┐  │
│ [Procure] │  │         Recent Activity Feed         │  │
│           │  └──────────────────────────────────────┘  │
│ [AI]      │                                           │
│ [Analytics]│                                           │
│ [Settings]│                                           │
└───────────┴───────────────────────────────────────────┘
```

---

## 10. Responsive Breakpoints

| Breakpoint | Width | Layout Changes |
|------------|-------|---------------|
| Mobile | < 640px | Sidebar hidden (hamburger), single column, stacked cards |
| Tablet | 640-1024px | Sidebar collapsible, 2-column card grid, tables scroll horizontally |
| Desktop | 1024-1440px | Full sidebar, 3-4 column card grid |
| Wide | > 1440px | Expanded content area, 4+ column card grid |

---

## 11. Accessibility

- **WCAG AA** minimum for all components
- **Keyboard**: Tab order logical, focus visible (2px ring), skip-to-content link
- **Screen readers**: ARIA labels on interactive elements, live regions for dynamic content
- **Color**: 4.5:1 minimum contrast ratio for text, charts use patterns in addition to color
- **Motion**: Respect `prefers-reduced-motion`, no auto-playing animations
- **Forms**: Every input has a visible label, errors linked via `aria-describedby`

---

## 12. AI Interface Patterns

### AI Chat Panel
- Messages aligned left (AI) / right (user)
- AI messages: structured cards with expandable evidence sections
- Streaming: text appears progressively with typing cursor
- Citations: numbered references linking to ERP data
- Action chips: "Create PO", "View Supplier", "Open Analytics"

### AI Insight Cards
- Severity badge (Critical/High/Medium/Low) with color coding
- Confidence percentage with progress bar
- Evidence section with specific metric references
- Action button linking to relevant ERP module

### AI Recommendation Panel
- Summary at top
- Supporting evidence (KPIs, trends, comparisons)
- Confidence score
- Recommended actions (linked to ERP workflows)
- "Why this recommendation?" expandable section
