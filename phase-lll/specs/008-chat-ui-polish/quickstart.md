# Quickstart: Chat UI Responsiveness & Modern Polish

**Feature**: 008-chat-ui-polish
**Prerequisites**: Frontend running (`npm run dev` in `frontend/`), Backend running (`uvicorn` in `backend/`)

## Setup

No new packages to install. All dependencies are already in `package.json`:
- `next-themes` — dark mode (installed, not yet wired)
- `swr` — data fetching for tasks panel (installed, not yet used)
- `clsx` — conditional class names (installed, already used)

## Development

```bash
cd frontend
npm run dev
```

## Testing Devices (Chrome DevTools)

1. Open Chrome DevTools → Toggle Device Toolbar (Ctrl+Shift+M)
2. Test with:
   - **iPhone SE** (375 x 667) — mobile layout, tabs
   - **Pixel 7** (412 x 915) — mobile, touch targets
   - **iPad Air** (820 x 1180) — breakpoint transition
   - **Responsive** (1280 x 800) — desktop split view

## Dark Mode Testing

- **macOS**: System Preferences → Appearance → Dark
- **Windows**: Settings → Personalization → Colors → Dark
- **Chrome DevTools**: Rendering → Emulate CSS media feature `prefers-color-scheme: dark`

## Key Files to Watch

| File | What changes |
|------|-------------|
| `app/globals.css` | Dark mode variant declaration |
| `app/layout.tsx` | ThemeProvider wrapper |
| `app/dashboard/page.tsx` | Split layout + mobile tabs |
| `components/ChatInterface.tsx` | Dark mode + tool feedback |
| `components/TasksPanel.tsx` | New task list component |
| `lib/tool-feedback.ts` | New pattern matching utility |
