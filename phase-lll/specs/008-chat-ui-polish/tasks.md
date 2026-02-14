# Tasks: Chat UI Responsiveness & Modern Polish

**Input**: Design documents from `/specs/008-chat-ui-polish/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Tests**: End-to-end manual testing via Chrome DevTools Device Mode (iPhone SE 375px, Pixel 7 412px, iPad Air 820px, Desktop 1280px). No automated tests.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Frontend**: `frontend/app/`, `frontend/components/`, `frontend/lib/`
- Paths based on plan.md structure

---

## Phase 1: Setup (Dark Mode Infrastructure)

**Purpose**: Configure Tailwind CSS 4 dark variant and next-themes ThemeProvider. This is the cross-cutting foundation that BLOCKS all user story work.

- [x] T001 Add `@custom-variant dark (&:where(.dark, .dark *));` directive to frontend/app/globals.css after the `@import "tailwindcss"` line
- [x] T002 Update frontend/app/layout.tsx: import ThemeProvider from next-themes, wrap children in `<ThemeProvider attribute="class" defaultTheme="system" enableSystem>`, add `suppressHydrationWarning` to `<html>`, add `dark:bg-gray-900 dark:text-gray-100` to `<body>`

**Checkpoint**: Dark mode infrastructure ready — `dark:` Tailwind classes respond to OS preference via next-themes

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: API helper for tasks and the TasksPanel component that all layout stories depend on.

**CRITICAL**: No layout or tab work can begin until this phase is complete.

### API Layer

- [x] T003 Add `TaskItem` interface (id, user_id, title, description, is_completed, created_at, updated_at) to frontend/lib/api.ts
- [x] T004 Add `fetchTasks(token: string): Promise<TaskItem[]>` function to frontend/lib/api.ts that GETs `/api/tasks` with JWT Authorization header

### TasksPanel Component

- [x] T005 Create frontend/components/TasksPanel.tsx with "use client" directive, accepting props `{ token: string; refreshKey: number }`
- [x] T006 Implement SWR data fetching in frontend/components/TasksPanel.tsx: call `fetchTasks(token)` with `refreshKey` in the SWR key to trigger revalidation
- [x] T007 Render task list in frontend/components/TasksPanel.tsx: checkbox icon (filled/empty), title (strikethrough if completed), truncated description, sorted by created_at descending
- [x] T008 Add loading skeleton state (3 animated gray placeholder rows) to frontend/components/TasksPanel.tsx
- [x] T009 Add empty state ("No tasks yet. Chat with the assistant to create some!") to frontend/components/TasksPanel.tsx
- [x] T010 Add error state (friendly message with retry) to frontend/components/TasksPanel.tsx
- [x] T011 Style TasksPanel with dark mode classes in frontend/components/TasksPanel.tsx: bg-white/dark:bg-gray-800, text-gray-900/dark:text-gray-100, border colors, checkbox colors

**Checkpoint**: TasksPanel renders tasks from backend, handles loading/empty/error states, supports dark mode

---

## Phase 3: User Story 4 — Dark/Light Theme Consistency (Priority: P2)

**Goal**: All existing pages render correctly in both dark and light themes with no hardcoded light-only colors.

**Independent Test**: Toggle OS to dark mode (or use Chrome DevTools → Rendering → prefers-color-scheme: dark), verify all pages — login, register, dashboard, chat — use dark-appropriate colors.

### Implementation for User Story 4

- [x] T012 [P] [US4] Add dark mode classes to frontend/app/login/page.tsx: page bg (dark:bg-gray-900), heading (dark:text-gray-100), labels (dark:text-gray-300), inputs (dark:border-gray-600 dark:bg-gray-800 dark:text-gray-100), error (dark:bg-red-900/30 dark:text-red-400), button hover, footer text (dark:text-gray-400), link (dark:text-blue-400)
- [x] T013 [P] [US4] Add dark mode classes to frontend/app/register/page.tsx: same color mapping as login page — page bg, heading, labels, inputs, error, button, footer, link
- [x] T014 [US4] Add dark mode classes to dashboard header in frontend/app/dashboard/page.tsx: header bg (dark:bg-gray-800 dark:border-gray-700), title (dark:text-gray-100), sign-out (dark:text-gray-400 dark:hover:text-gray-200), not-auth section (dark:bg-gray-900, dark:text-gray-300)
- [x] T015 [US4] Add dark mode classes to ChatInterface welcome text in frontend/components/ChatInterface.tsx: dark:text-gray-500
- [x] T016 [US4] Add dark mode classes to ChatInterface message bubbles in frontend/components/ChatInterface.tsx: user bubble (dark:bg-blue-600), assistant bubble (dark:bg-gray-700 dark:text-gray-100), labels (dark:text-gray-400)
- [x] T017 [US4] Add dark mode classes to ChatInterface loading dots in frontend/components/ChatInterface.tsx: dots (dark:bg-gray-500), loading bubble bg (dark:bg-gray-700)
- [x] T018 [US4] Add dark mode classes to ChatInterface error banner in frontend/components/ChatInterface.tsx: dark:bg-red-900/30 dark:text-red-400 dark:border-red-800
- [x] T019 [US4] Add dark mode classes to ChatInterface input bar in frontend/components/ChatInterface.tsx: bar bg (dark:bg-gray-800 dark:border-gray-700), input field (dark:border-gray-600 dark:bg-gray-700 dark:text-gray-100 dark:placeholder-gray-400), send button (dark:bg-blue-600)
- [ ] T020 [US4] Verify in browser (Chrome DevTools prefers-color-scheme toggle): all pages render correctly in dark mode — login, register, dashboard header, chat bubbles, input, error, loading

**Checkpoint**: All UI elements are theme-aware with no hardcoded light-only colors (SC-004)

---

## Phase 4: User Story 2 — Desktop Split View (Priority: P1)

**Goal**: On desktop (>768px), show tasks panel on the left (1/3) and chat on the right (2/3) with independent scrolling.

**Independent Test**: Open at 1280px width, verify tasks panel visible on left, chat on right, both scrollable independently. Send a chat message that creates a task, verify tasks panel updates.

### Implementation for User Story 2

- [x] T021 [US2] Add `onMessageComplete` optional callback prop to ChatInterface interface in frontend/components/ChatInterface.tsx
- [x] T022 [US2] Call `onMessageComplete?.()` in ChatInterface handleSend() after successful response (inside try block, after setting assistant message) in frontend/components/ChatInterface.tsx
- [x] T023 [US2] Add `refreshKey` state (number, default 0) to frontend/app/dashboard/page.tsx, create `handleChatComplete` callback that increments refreshKey
- [x] T024 [US2] Restructure frontend/app/dashboard/page.tsx main area: wrap TasksPanel and ChatInterface in a flex container with `md:flex md:flex-row` for side-by-side on desktop
- [x] T025 [US2] Set tasks panel container in frontend/app/dashboard/page.tsx: `hidden md:flex md:flex-col md:w-1/3 md:border-r border-gray-200 dark:border-gray-700 overflow-y-auto`
- [x] T026 [US2] Set chat panel container in frontend/app/dashboard/page.tsx: `w-full md:w-2/3 overflow-hidden` wrapping ChatInterface
- [x] T027 [US2] Pass `token`, `refreshKey` to TasksPanel and `token`, `onMessageComplete={handleChatComplete}` to ChatInterface in frontend/app/dashboard/page.tsx
- [ ] T028 [US2] Verify in browser at 1280px: tasks panel on left (1/3), chat on right (2/3), both scroll independently, task panel updates after chat creates a task

**Checkpoint**: Desktop split view functional with real-time task updates (SC-002, FR-002, FR-010, FR-011)

---

## Phase 5: User Story 1 — Mobile Chat Usability (Priority: P1)

**Goal**: Chat interface is fully usable on 375px mobile viewport with no horizontal scroll, proper keyboard handling, and adequate touch targets.

**Independent Test**: Open at 375px (iPhone SE), send 3 messages, verify no horizontal scroll, input stays visible above keyboard simulation, messages wrap correctly, send button is easily tappable.

### Implementation for User Story 1

- [x] T029 [US1] Ensure ChatInterface input bar uses sticky bottom-0 positioning for mobile keyboard compatibility in frontend/components/ChatInterface.tsx
- [x] T030 [US1] Ensure send button meets 44x44px minimum touch target (min-h-[44px] min-w-[44px]) in frontend/components/ChatInterface.tsx
- [x] T031 [US1] Ensure message bubbles use max-w-[85%] on mobile (sm:max-w-[75%] on larger) for better readability in frontend/components/ChatInterface.tsx
- [x] T032 [US1] Add responsive padding to ChatInterface: smaller padding on mobile (px-3 py-4) vs desktop (px-4 py-6) in frontend/components/ChatInterface.tsx
- [ ] T033 [US1] Verify in Chrome DevTools (iPhone SE 375x667): no horizontal scroll, messages wrap in bubbles, send button tappable, input visible above simulated keyboard

**Checkpoint**: Mobile chat fully usable at 375px (SC-001, FR-005, FR-006)

---

## Phase 6: User Story 3 — Mobile Tab Navigation (Priority: P1)

**Goal**: On mobile (<768px), user can switch between "Chat" and "Tasks" tabs. Chat state is preserved when switching.

**Independent Test**: Open at 375px, verify tab bar visible with "Chat" active, tap "Tasks" to see task list, tap "Chat" to return with all messages preserved.

### Implementation for User Story 3

- [x] T034 [US3] Add `activeTab` state (`"chat" | "tasks"`, default `"chat"`) to frontend/app/dashboard/page.tsx
- [x] T035 [US3] Render bottom tab bar (md:hidden) in frontend/app/dashboard/page.tsx: two buttons "Chat" and "Tasks", min-h-[44px] touch targets, border-t, dark mode colors
- [x] T036 [US3] Style active tab button (bold text, blue underline/bg-blue-50 dark:bg-blue-900/20) and inactive tab (text-gray-500 dark:text-gray-400) in frontend/app/dashboard/page.tsx
- [x] T037 [US3] Implement conditional panel visibility in frontend/app/dashboard/page.tsx: chat panel uses `clsx("flex-1 overflow-hidden", activeTab === "tasks" && "hidden md:flex")`, tasks panel uses `clsx("flex-1 overflow-y-auto", activeTab === "chat" && "hidden md:flex")`
- [x] T038 [US3] Ensure both ChatInterface and TasksPanel remain mounted (not unmounted) when hidden — use CSS display/visibility, not conditional rendering — in frontend/app/dashboard/page.tsx
- [x] T039 [US3] Ensure layout transitions smoothly when resizing browser across 768px breakpoint: tab bar appears/disappears, panels rearrange without state loss in frontend/app/dashboard/page.tsx
- [ ] T040 [US3] Verify in Chrome DevTools (375px): tab bar visible, switching tabs shows correct panel, chat state (messages, input) preserved after switching, tab bar hidden at 820px+

**Checkpoint**: Mobile tab navigation functional with state preservation (SC-003, FR-001, FR-003, FR-004, FR-012)

---

## Phase 7: User Story 5 — Tool Execution Feedback (Priority: P2)

**Goal**: Contextual loading messages ("Adding task...", "Fetching tasks...") replace generic dots when recognizable tool actions are detected.

**Independent Test**: Send "Add a task called Buy milk", verify "Adding task..." appears instead of dots. Send "What are my tasks?", verify "Fetching tasks..." appears. Send "Hello", verify generic dots appear.

### Implementation for User Story 5

- [x] T041 [P] [US5] Create frontend/lib/tool-feedback.ts with `getToolFeedback(message: string): string | null` function containing regex pattern map: add/create/new task → "Adding task...", list/show/what tasks → "Fetching tasks...", complete/finish/done/mark → "Completing task...", delete/remove → "Deleting task...", update/change/rename/edit → "Updating task...", no match → null
- [x] T042 [US5] Add `toolFeedback` state (string | null, default null) to ChatInterface in frontend/components/ChatInterface.tsx
- [x] T043 [US5] Import `getToolFeedback` and call it in handleSend() before setLoading(true), store result in toolFeedback state in frontend/components/ChatInterface.tsx
- [x] T044 [US5] Update loading indicator in frontend/components/ChatInterface.tsx: if toolFeedback is set, show `<p className="text-sm text-gray-500 dark:text-gray-400 animate-pulse">{toolFeedback}</p>` instead of bouncing dots
- [x] T045 [US5] Clear toolFeedback in the finally block of handleSend() (alongside setLoading(false)) in frontend/components/ChatInterface.tsx
- [ ] T046 [US5] Verify in browser: "Add a task called Buy milk" shows "Adding task...", "What are my tasks?" shows "Fetching tasks...", "Complete the milk task" shows "Completing task...", "Hello" shows generic dots

**Checkpoint**: Tool-specific feedback for at least 3 recognized actions (SC-005, FR-009)

---

## Phase 8: Polish & Verification

**Purpose**: Cross-cutting verification and edge cases

- [ ] T047 Verify tasks panel empty state shows "No tasks yet. Chat with the assistant to create some!" when user has no tasks in frontend/components/TasksPanel.tsx
- [ ] T048 Verify tasks panel scrolls independently from chat panel on desktop (1280px) when task list is long in frontend/app/dashboard/page.tsx
- [ ] T049 Verify device rotation (portrait ↔ landscape) preserves chat state and re-adapts layout in Chrome DevTools
- [ ] T050 Verify full E2E flow: register → login → see dark mode correct → desktop split view with tasks → mobile tab switching → send chat "Add a task called Buy milk" → see "Adding task..." feedback → see task appear in panel

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately
- **Foundational (Phase 2)**: Depends on Setup — BLOCKS all user stories
- **US4 Dark Mode (Phase 3)**: Depends on Setup (Phase 1) — can start as soon as ThemeProvider is wired
- **US2 Split View (Phase 4)**: Depends on Foundational (Phase 2) — needs TasksPanel
- **US1 Mobile Usability (Phase 5)**: Depends on Setup (Phase 1) — adjustments to ChatInterface
- **US3 Mobile Tabs (Phase 6)**: Depends on US2 Split View (Phase 4) — tabs switch between panels
- **US5 Tool Feedback (Phase 7)**: Depends on Setup (Phase 1) — modifies ChatInterface loading
- **Polish (Phase 8)**: Depends on all user stories complete

### User Story Dependencies

| Story | Can Start After | Logical Prerequisites |
|-------|-----------------|----------------------|
| US4 (dark/light theme) | Phase 1 Setup | ThemeProvider and @custom-variant ready |
| US2 (desktop split view) | Phase 2 Foundational | TasksPanel and fetchTasks() ready |
| US1 (mobile usability) | Phase 1 Setup | ChatInterface exists (already does) |
| US3 (mobile tabs) | US2 | Both panels exist to switch between |
| US5 (tool feedback) | Phase 1 Setup | ChatInterface loading state exists |

### Parallel Opportunities

- Phase 1: T001 and T002 are sequential (T002 depends on T001)
- Phase 2: T003 and T004 are sequential; T005-T011 are sequential
- Phase 3 (US4): T012 and T013 can run in parallel (different files)
- Phase 3 (US4) and Phase 7 (US5) can run in parallel after Phase 1
- Phase 5 (US1) can run in parallel with Phase 4 (US2) after Phase 1

---

## Implementation Strategy

### MVP First (US4 + US2 + US1)

1. Complete Phase 1: Setup (dark mode infrastructure)
2. Complete Phase 2: Foundational (TasksPanel, fetchTasks)
3. Complete Phase 3: US4 (all pages dark-mode-aware)
4. Complete Phase 4: US2 (desktop split view working)
5. Complete Phase 5: US1 (mobile chat usable)
6. **STOP and VALIDATE**: Does desktop show split view? Does mobile work at 375px? Does dark mode look correct?

### Incremental Delivery

1. Setup + Foundational → Infrastructure ready
2. US4 → Dark mode everywhere → Testable
3. US2 → Desktop split view → Major visual upgrade
4. US1 → Mobile polish → Mobile-ready
5. US3 → Tab navigation → Full mobile experience
6. US5 → Tool feedback → UX polish
7. Polish → E2E verification → Ship!

---

## Summary

| Metric | Value |
|--------|-------|
| Total Tasks | 50 |
| Setup Tasks | 2 |
| Foundational Tasks | 9 |
| US4 (dark/light theme) Tasks | 9 |
| US2 (desktop split view) Tasks | 8 |
| US1 (mobile usability) Tasks | 5 |
| US3 (mobile tabs) Tasks | 7 |
| US5 (tool feedback) Tasks | 6 |
| Polish & Verification Tasks | 4 |
| Parallel Opportunities | 4 tasks marked [P] |

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story
- All changes are frontend-only — no backend modifications
- Testing is E2E manual via Chrome DevTools Device Mode
- Dependencies: next-themes and swr are already installed but unused — this feature activates them
- Dark mode uses class-based toggling via @custom-variant (Tailwind CSS 4) + next-themes
- Both panels stay mounted in DOM when hidden on mobile (CSS visibility, not React conditional rendering) to preserve state
