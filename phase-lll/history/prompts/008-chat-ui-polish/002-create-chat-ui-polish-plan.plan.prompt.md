---
id: 002
title: Create Chat UI Polish Implementation Plan
stage: plan
date: 2026-02-11
surface: agent
model: claude-sonnet-4-5-20250929
feature: 008-chat-ui-polish
branch: 008-chat-ui-polish
user: Adi
command: /sp.plan
labels: ["plan", "responsive", "dark-mode", "split-view", "mobile", "tailwind"]
links:
  spec: specs/008-chat-ui-polish/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/008-chat-ui-polish/plan.md
  - specs/008-chat-ui-polish/research.md
  - specs/008-chat-ui-polish/data-model.md
  - specs/008-chat-ui-polish/quickstart.md
  - specs/008-chat-ui-polish/contracts/tasks-api.md
tests:
  - null
---

## Prompt

/sp.plan

Create: Responsive Layout Wrapper, Mobile Toggle (Chat/Tasks), Loading Skeletons.
Decisions needing documentation: Desktop split-screen ratio vs. Floating modal.
Testing strategy: Chrome DevTools Device Mode (iPhone SE, Pixel 7, iPad Air).

Technical details:
- Phase 1: Implement a Sidebar/Drawer layout for the Chat on mobile.
- Phase 2: Design the Desktop split-pane layout.
- Phase 3: Style the ChatKit components to match the specific "Todo App" branding (colors/fonts).
- Phase 4: Add "Thinking..." indicators for better perceived performance.

## Response snapshot

Created 4-phase implementation plan with 6 research decisions, data model, API contract, and quickstart guide.

**Phases:**
1. Phase 1: Mobile-First Foundation & Dark Mode Infrastructure — globals.css @custom-variant, ThemeProvider wrapper, dark: classes on all existing pages
2. Phase 2: Desktop Split-Pane Layout — TasksPanel component (SWR + GET /api/tasks), 1/3 + 2/3 split, independent scrolling, refreshKey for task updates
3. Phase 3: Mobile Tab Navigation — bottom tab bar (Chat/Tasks), conditional panel rendering, dvh units for keyboard, CSS-only show/hide to preserve state
4. Phase 4: Tool Execution Feedback — client-side pattern matching utility, contextual messages ("Adding task...", "Fetching tasks...")

**Key decisions:**
- R1: Fixed 1/3+2/3 split over floating modal (keeps both panels visible)
- R2: next-themes + @custom-variant dark for Tailwind v4 class-based dark mode
- R3: Bottom tab bar for mobile navigation (thumb-friendly)
- R4: SWR re-fetch after each chat response (no WebSockets needed)
- R5: Client-side regex matching for tool feedback
- R6: dvh units + sticky positioning for mobile keyboard handling

**Files:** 7 modified, 2 new (9 total)

## Outcome

- Impact: Complete architectural plan for responsive mobile/desktop UI with dark mode and UX polish
- Tests: Chrome DevTools device mode testing matrix (4 devices x 8 scenarios x 2 themes)
- Files: 5 design artifacts created (plan, research, data-model, quickstart, contract)
- Next prompts: /sp.tasks to generate implementation tasks, then /sp.implement
- Reflection: Leveraged existing installed-but-unused dependencies (next-themes, swr) to avoid new package installs
