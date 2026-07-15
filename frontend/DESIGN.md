# CrimeMatrix Design System

## Brand Identity

A law enforcement intelligence platform — authoritative, trustworthy, precise.

| Token | Value | Hex |
|---|---|---|
| Primary | Deep Navy | `#0f172a` |
| Accent | Badge Gold | `#f59e0b` |
| Accent Light | Gold Glow | `#fef3c7` |
| Accent Dark | Deep Gold | `#d97706` |
| Surface | Cool Gray | `#f8fafc` |
| Card | White | `#ffffff` |
| Text Primary | Near Black | `#0f172a` |
| Text Secondary | Slate | `#475569` |
| Text Muted | Light Slate | `#94a3b8` |
| Border | Subtle | `#e2e8f0` |
| Success | Emerald | `#10b981` |
| Warning | Amber | `#f59e0b` |
| Danger | Red | `#ef4444` |
| Info | Blue | `#3b82f6` |

## Typography

| Level | Size | Weight | Line Height | Use |
|---|---|---|---|---|
| Display | 28px | 700 | 1.2 | Page titles |
| Heading | 20px | 600 | 1.3 | Section headings |
| Subheading | 14px | 600 | 1.4 | Card titles |
| Body | 14px | 400 | 1.5 | Default text |
| Caption | 12px | 500 | 1.4 | Timestamps |
| Overline | 11px | 600 | 1.2 | Uppercase labels |

Font: Inter (Google Fonts), fallback: system-ui
Mono: JetBrains Mono

## Layout

- Sidebar: 68px fixed left
- Header: 60px fixed top
- Right Panel: 340px fixed right (visible on >= 1280px)
- Main Content: flex fill, padded 24px

## Components

### Sidebar
- White bg, right border
- Logo: 40px dark rounded square
- Nav: 48px wide items, 44px tall
- Active: 3px amber left bar + amber icon + amber bg tint
- Avatar: 36px circle with initials

### Header
- 60px height, white bg, bottom border
- Search: rounded-lg, gray bg, focus amber ring
- Bell: badge with count, pulse animation
- User: avatar + name + role + chevron

### Right Panel
- 340px, always visible on wide screens
- Sections: Quick Stats, Activity, Notifications
- Cards: icon + title + time, hover bg

### Cards
- White bg, rounded-xl, shadow-sm
- Hover: shadow-md, slight translateY(-1px)
- Padding: 20px

### Stat Cards
- Icon (colored bg) + value (28px bold) + label (12px muted)
- Grid: 4 columns on desktop, 2 on tablet

## Animations

| Element | Duration | Easing |
|---|---|---|
| Sidebar hover | 150ms | ease |
| Panel slide | 300ms | cubic-bezier(0.4, 0, 0.2, 1) |
| Card hover | 200ms | ease |
| Search focus | 200ms | ease |
| Badge pulse | 2s | ease infinite |
