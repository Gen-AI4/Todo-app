# Research: Chat UI Responsiveness & Modern Polish

**Date**: 2026-02-11
**Feature**: 008-chat-ui-polish

---

## R1: Desktop Split-Screen Ratio vs. Floating Modal

**Decision**: Fixed split-pane layout with 1/3 tasks + 2/3 chat ratio.

**Rationale**: A floating modal would overlay the chat and block interaction with it. The split-pane keeps both panels visible and independently usable. The 1/3 + 2/3 ratio gives the chat (the primary interaction surface) more space while still showing a meaningful task list.

**Alternatives considered**:
- **50/50 split**: Equal space, but chat needs more room for message bubbles. Task titles are short and don't need half the screen.
- **Resizable splitter**: Adds complexity (drag handle, persistence of width). Not justified for v1.
- **Floating modal for tasks**: Blocks chat, requires open/close gesture, breaks the "see tasks update in real-time" requirement (FR-010).
- **Sidebar drawer (collapsible)**: Reasonable alternative but adds animation complexity and a toggle button. Could be a v2 enhancement.

---

## R2: Tailwind CSS 4 Dark Mode Strategy

**Decision**: Use `@custom-variant dark (&:where(.dark, .dark *))` in globals.css with `next-themes` ThemeProvider (`attribute="class"`, `defaultTheme="system"`, `enableSystem`).

**Rationale**: Tailwind CSS v4 defaults to `prefers-color-scheme` media queries for the `dark:` variant — which works without any config. However, using `next-themes` with class-based toggling gives us:
1. OS preference detection out of the box (`defaultTheme="system"`)
2. Future-proofing for an explicit toggle (v2)
3. No flash of wrong theme on page load (next-themes handles SSR)
4. `suppressHydrationWarning` on `<html>` avoids React hydration mismatch

**Alternatives considered**:
- **Pure media query (Tailwind default)**: Simpler, but no path to user toggle and no SSR flash prevention.
- **CSS custom properties only**: More manual work, loses Tailwind's `dark:` utility classes.
- **next-themes with `attribute="data-theme"`**: Works but `class` is the Tailwind convention.

---

## R3: Mobile Tab Navigation Pattern

**Decision**: Bottom tab bar with "Chat" and "Tasks" tabs, visible only on mobile (<768px / `md` breakpoint).

**Rationale**: Bottom tabs are the standard mobile navigation pattern (iOS tab bar, Material bottom navigation). They're reachable with thumbs on large phones. The tab bar sits above the chat input bar on the Chat tab and at the bottom of the screen on the Tasks tab.

**Alternatives considered**:
- **Top tabs**: Less thumb-friendly on tall phones. Competes with the header for vertical space.
- **Swipe between panels**: Discoverable only for experienced users. Conflicts with horizontal scroll gestures.
- **Hamburger menu / drawer**: Hides navigation, adds an extra tap. Overkill for 2 panels.

---

## R4: Task Panel Data Fetching

**Decision**: Fetch tasks via `GET /api/tasks` with JWT header. Re-fetch after each chat response using a `refreshKey` counter.

**Rationale**: The backend already has a REST endpoint for task listing (`GET /api/tasks` in `backend/app/routers/tasks.py`). We don't need WebSockets or polling — we know tasks may change after a chat message, so we re-fetch the task list after every chat response arrives. The `swr` library (already installed) handles caching and revalidation.

**Alternatives considered**:
- **SWR with `mutate()` on interval**: Wasteful polling when user isn't chatting.
- **WebSocket push**: Requires backend changes (out of scope).
- **Optimistic UI update**: Complex to map chat response text to task mutations. Re-fetch is simpler and guaranteed correct.

---

## R5: Tool Execution Feedback (Client-Side Heuristics)

**Decision**: Pattern-match the user's message text against a map of keywords to feedback messages. Display the matched feedback instead of generic loading dots.

**Rationale**: The backend does not return tool metadata. Client-side pattern matching is simple, zero-dependency, and covers the common cases. The patterns are case-insensitive substring matches.

**Pattern map**:

| User Message Contains | Feedback Displayed |
|-----------------------|-------------------|
| "add a task", "create a task", "new task" | "Adding task..." |
| "list", "show", "what are my tasks", "my tasks" | "Fetching tasks..." |
| "complete", "finish", "done", "mark" | "Completing task..." |
| "delete", "remove" | "Deleting task..." |
| "update", "change", "rename", "edit" | "Updating task..." |
| (no match) | Generic pulsing dots (existing behavior) |

**Alternatives considered**:
- **Backend streaming with tool events**: Accurate but requires backend changes (out of scope).
- **No feedback (keep dots)**: Simpler but spec requires it (FR-009, SC-005).

---

## R6: Mobile Keyboard Handling

**Decision**: Use `position: sticky` on the input bar with `bottom: 0` plus `dvh` (dynamic viewport height) units on the chat container.

**Rationale**: On mobile, the virtual keyboard reduces the viewport. Using `100dvh` instead of `100vh` makes the container respect the keyboard. The sticky input bar stays above the keyboard. This is a CSS-only approach with no JavaScript keyboard detection needed.

**Alternatives considered**:
- **`visualViewport` API**: More precise but requires JavaScript listeners and has inconsistent support.
- **Fixed positioning**: Can cause issues with iOS Safari scroll behavior.
- **`env(safe-area-inset-bottom)`**: Useful for notch devices but doesn't solve keyboard issue alone.
