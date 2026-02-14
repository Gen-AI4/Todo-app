---
id: 003
title: Generate Chat UI Polish Implementation Tasks
stage: tasks
date: 2026-02-11
surface: agent
model: claude-sonnet-4-5-20250929
feature: 008-chat-ui-polish
branch: 008-chat-ui-polish
user: Adi
command: /sp.tasks
labels: ["tasks", "responsive", "dark-mode", "split-view", "mobile-tabs", "tool-feedback"]
links:
  spec: specs/008-chat-ui-polish/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/008-chat-ui-polish/tasks.md
tests:
  - null
---

## Prompt

/sp.tasks

## Response snapshot

Generated 50 tasks across 8 phases from 5 design documents (spec, plan, research, data-model, contracts).

**Phase breakdown:**
- Phase 1 (Setup): 2 tasks — @custom-variant dark, ThemeProvider wrapper
- Phase 2 (Foundational): 9 tasks — TaskItem type, fetchTasks(), TasksPanel component with SWR, loading/empty/error states
- Phase 3 (US4 Dark Mode): 9 tasks — dark: classes on login, register, dashboard, ChatInterface (bubbles, input, error, loading)
- Phase 4 (US2 Split View): 8 tasks — onMessageComplete callback, refreshKey, flex layout, 1/3+2/3 split, independent scroll
- Phase 5 (US1 Mobile): 5 tasks — sticky input, 44px touch targets, responsive bubble widths, padding
- Phase 6 (US3 Tabs): 7 tasks — activeTab state, bottom tab bar, conditional visibility, CSS mount/hide
- Phase 7 (US5 Feedback): 6 tasks — tool-feedback.ts utility, toolFeedback state, conditional loading indicator
- Phase 8 (Polish): 4 tasks — empty state, scroll verification, rotation, full E2E

**Parallel opportunities:** T012+T013 (login+register dark mode), US4+US5 after Phase 1, US1+US2 after Phase 1

## Outcome

- Impact: Complete task checklist for responsive UI, dark mode, split view, mobile tabs, and tool feedback
- Tests: Manual E2E via Chrome DevTools (4 devices, 8 scenarios, 2 themes)
- Files: 1 file created (tasks.md)
- Next prompts: /sp.implement to execute all 50 tasks
- Reflection: Tasks organized by user story with clear file paths; both panels stay DOM-mounted on mobile for state preservation
