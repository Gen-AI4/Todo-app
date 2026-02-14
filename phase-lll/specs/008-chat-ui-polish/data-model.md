# Data Model: Chat UI Responsiveness & Modern Polish

**Date**: 2026-02-11
**Feature**: 008-chat-ui-polish

---

This feature is frontend-only. No new database tables or backend models are created. All state is local React component state or derived from existing backend responses.

## Frontend State Entities

### TabState (mobile only)

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| activeTab | `"chat" \| "tasks"` | `"chat"` | Currently visible panel on mobile |

**Scope**: Local state in `DashboardPage` component.
**Lifecycle**: Created on mount, lost on unmount (no persistence needed).

### TaskItem (fetched from backend)

Maps to existing backend `Task` model via `GET /api/tasks`:

| Field | Type | Description |
|-------|------|-------------|
| id | `string` (UUID) | Task identifier |
| title | `string` | Task title |
| description | `string \| null` | Optional task description |
| is_completed | `boolean` | Completion status |
| created_at | `string` (ISO date) | Creation timestamp |
| updated_at | `string` (ISO date) | Last update timestamp |

### ToolFeedback (transient)

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| message | `string \| null` | `null` | Contextual feedback text (e.g., "Adding task...") |

**Scope**: Derived inside `ChatInterface` from the last user message text using pattern matching.
**Lifecycle**: Set when `loading` becomes `true`, cleared when `loading` becomes `false`.

### ThemeMode (derived from OS)

| Field | Type | Source | Description |
|-------|------|--------|-------------|
| theme | `"light" \| "dark" \| "system"` | `next-themes` | Active color theme |
| resolvedTheme | `"light" \| "dark"` | `next-themes` | Resolved theme (system -> actual) |

**Scope**: Provided by `next-themes` ThemeProvider. No custom state needed.

## Existing Entities (unchanged)

- **Message** (`{ role: "user" | "assistant", content: string }`) — already in `ChatInterface.tsx`
- **ChatApiResponse** (`{ response: string, conversation_id: string }`) — already in `lib/api.ts`
