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

Font: Plus Jakarta Sans (Google Fonts), fallback: system-ui
Mono: JetBrains Mono

| Level | Size | Weight | Use |
|---|---|---|---|
| Display | 24px | 700 | Page titles |
| Heading | 15px | 700 | Brand, section titles |
| Subheading | 13px | 600 | Card titles |
| Body | 13px | 400 | Default text |
| Caption | 12px | 500 | Timestamps |
| Micro | 11px | 500 | Uppercase labels |

## Layout

```
┌─────────────────────────────────────────────────┐
│              HEADER (56px, full width)           │
├────────────┬───────────────────┬────────────────┤
│ LEFT       │                   │ RIGHT PANEL    │
│ SIDEBAR    │   MAIN CONTENT    │ (360px)        │
│ 240px/68px │                   │ [Activity|Chat]│
└────────────┴───────────────────┴────────────────┘
```

- Header: 56px, full width, flex row
- Left Sidebar: 240px expanded / 68px collapsed
- Main Content: flex-1, scrollable
- Right Panel: 360px, always visible, tabbed (Activity + Chat)

## Components

### Header
- Full width, white bg, bottom border
- Left: sidebar toggle + breadcrumb
- Center: search bar (gray bg, amber focus ring)
- Right: bell icon with badge + user avatar/name/role

### Left Sidebar
- Expanded (240px): icon + label text, logo + brand name
- Collapsed (68px): icon only, tooltip on hover
- Active: amber left bar + amber icon + light amber bg
- Bottom: settings, logout, user avatar with name/role

### Right Panel
- 360px wide, two tabs: Activity and AI Copilot
- Activity: quick stats grid + activity feed
- Chat: message list + input + quick prompts

### Chat Messages
- Assistant: left-aligned, gray bubble, bot avatar
- User: right-aligned, navy bubble, user avatar
- Quick prompts appear below first message

## Animations

| Element | Duration | Easing |
|---|---|---|
| Sidebar width | 300ms | ease |
| Nav active bar | 250ms | spring |
| Stat cards entrance | 350ms | ease, staggered |
| Chat slide-in | 350ms | ease |
| Badge pulse | 2s | infinite |
