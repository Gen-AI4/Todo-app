# Feature Specification: Chat UI Responsiveness & Modern Polish

**Feature Branch**: `008-chat-ui-polish`
**Created**: 2026-02-11
**Status**: Draft
**Input**: User description: "Spec 8: Chat UI Responsiveness & Modern Polish — Mobile Layout, Theme Consistency, and UX micro-interactions"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - User Accesses Chat on a Mobile Device (Priority: P1)

A user opens the Todo AI Chatbot on their phone. The chat interface fills the screen without horizontal scrolling, the input bar stays above the on-screen keyboard, and messages are readable without zooming. The user can type, send, and read responses comfortably on a 375px-wide screen.

**Why this priority**: Mobile is the most constrained surface. If the chat is unusable on phones, a significant portion of users cannot interact with the app at all.

**Independent Test**: Open the application on a 375px viewport (or real mobile device), send 3 messages, verify no horizontal scroll, input stays visible above keyboard, and messages wrap correctly.

**Acceptance Scenarios**:

1. **Given** a user opens the app on a 375px-wide screen, **When** the dashboard loads, **Then** the chat interface fits within the viewport with no horizontal scrollbar.
2. **Given** a user taps the chat input on mobile, **When** the on-screen keyboard appears, **Then** the input bar remains visible above the keyboard and the latest messages stay in view.
3. **Given** a conversation with long messages, **When** viewed on a small screen, **Then** message text wraps naturally within bubbles and remains readable without zooming.
4. **Given** a user on mobile, **When** they type and press Send, **Then** the send button is large enough to tap comfortably (minimum 44x44px touch target).

---

### User Story 2 - User Sees a Split View on Desktop (Priority: P1)

On desktop (screens wider than 768px), the interface shows a two-panel layout: a tasks list on the left and the chat on the right. This lets users see their task state while conversing with the AI assistant.

**Why this priority**: The split view is the core desktop experience that differentiates this app from a simple chat. It provides productivity context alongside the conversation.

**Independent Test**: Open the application at 1280px width, verify the tasks panel is visible on the left and the chat panel on the right, both usable simultaneously.

**Acceptance Scenarios**:

1. **Given** a desktop viewport (>768px), **When** the dashboard loads, **Then** the layout shows a tasks panel on the left and the chat panel on the right.
2. **Given** the split view, **When** the user sends a chat message that creates a task, **Then** the tasks panel updates to reflect the new task without a full page reload.
3. **Given** a desktop viewport, **When** the user resizes the browser below 768px, **Then** the layout switches from split view to single-panel (chat-only or tab view).

---

### User Story 3 - User Switches Between Tabs on Mobile (Priority: P1)

On mobile (screens narrower than 768px), the user can switch between a "Chat" tab and a "Tasks" tab. Only one panel is visible at a time, maximizing screen real estate. The active tab is clearly highlighted.

**Why this priority**: On small screens, a split view is impractical. Tabs provide access to both features without cramming them together.

**Independent Test**: Open on a 375px viewport, verify tabs for "Chat" and "Tasks" are visible, switching tabs shows the correct panel, and the active tab is visually distinct.

**Acceptance Scenarios**:

1. **Given** a mobile viewport (<768px), **When** the dashboard loads, **Then** the user sees tab controls for "Chat" and "Tasks" with "Chat" active by default.
2. **Given** the mobile tab view, **When** the user taps the "Tasks" tab, **Then** the tasks list is displayed and the chat panel is hidden.
3. **Given** the mobile tab view, **When** the user switches back to "Chat", **Then** the chat state (messages, input text) is preserved.

---

### User Story 4 - User Experiences Consistent Dark/Light Theme (Priority: P2)

The chat interface respects the user's OS-level color scheme preference (or an explicit toggle). Chat bubbles, backgrounds, input fields, headers, and error messages all adapt to the current theme without hardcoded colors breaking the appearance.

**Why this priority**: Visual consistency builds trust and reduces eye strain. Hardcoded light-mode colors on a dark-mode OS feel broken.

**Independent Test**: Switch OS to dark mode (or toggle the theme if a toggle exists), verify all chat elements — bubbles, input, header, error messages — use appropriate dark-mode colors.

**Acceptance Scenarios**:

1. **Given** the user's OS is set to dark mode, **When** the app loads, **Then** the background, text, input fields, and chat bubbles use dark-theme colors.
2. **Given** dark mode, **When** the user sends a message, **Then** user bubbles and assistant bubbles remain visually distinct (different shades or accent colors appropriate for dark backgrounds).
3. **Given** theme transitions, **When** the user changes their OS theme while the app is open, **Then** the interface updates to the new theme without requiring a page refresh.
4. **Given** any theme, **When** an error message is displayed, **Then** the error styling is legible and contrasts with the current background.

---

### User Story 5 - User Sees Tool Execution Feedback (Priority: P2)

When the AI assistant is executing a tool (e.g., adding a task, listing tasks), the user sees a specific status message like "Adding task..." instead of generic loading dots. This gives the user confidence that their request is being processed correctly.

**Why this priority**: Generic loading gives no insight into what's happening. Specific feedback ("Adding task...") reduces uncertainty and makes the app feel intelligent.

**Independent Test**: Send "Add a task called Buy milk", verify the loading indicator shows "Adding task..." (or similar tool-specific text) before the final response appears.

**Acceptance Scenarios**:

1. **Given** the user sends a command like "Add a task called Buy milk", **When** the backend is executing the tool, **Then** the chat displays a contextual status like "Adding task..." instead of generic dots.
2. **Given** the user sends "What are my tasks?", **When** the backend queries, **Then** the status shows "Fetching tasks..." or similar.
3. **Given** a tool execution completes, **When** the response arrives, **Then** the status indicator is replaced by the actual AI response.
4. **Given** the backend does not provide tool execution metadata, **When** waiting for a response, **Then** the system falls back to the existing generic loading dots.

**Resolved**: The backend does not return tool execution metadata. Tool-specific feedback uses client-side heuristics — the frontend pattern-matches the user's message text (e.g., "add a task" maps to "Adding task...", "what are my tasks" maps to "Fetching tasks...") to display contextual status. When no pattern matches, the existing generic loading dots are shown.

---

### Edge Cases

- What happens when the user rotates their phone between portrait and landscape? The layout should re-adapt without losing chat state.
- What happens if the tasks panel is empty? Show an empty-state message like "No tasks yet. Chat with the assistant to create some!"
- What happens if the user has a very long task list on desktop split view? The tasks panel should scroll independently from the chat panel.
- What happens with system-level font size scaling (accessibility)? Text should remain readable and layout should not break.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST render a single-panel chat layout on viewports narrower than 768px.
- **FR-002**: System MUST render a two-panel split layout (tasks left, chat right) on viewports 768px or wider.
- **FR-003**: System MUST display tab controls ("Chat" / "Tasks") on mobile viewports, defaulting to the Chat tab.
- **FR-004**: System MUST preserve chat state (messages, input, conversation_id) when switching between tabs on mobile.
- **FR-005**: System MUST keep the chat input bar visible above the on-screen keyboard on mobile devices.
- **FR-006**: System MUST ensure all interactive elements (send button, tab controls) meet a minimum 44x44px touch target on mobile.
- **FR-007**: System MUST support dark and light color themes, adapting all UI elements (backgrounds, text, bubbles, inputs, headers, errors) to the active theme.
- **FR-008**: System MUST detect the user's OS-level color scheme via `prefers-color-scheme` media query and apply the corresponding theme by default.
- **FR-009**: System MUST display contextual tool-execution feedback (e.g., "Adding task...") when a recognizable tool action is in progress, falling back to generic loading dots when no specific action is identified.
- **FR-010**: System MUST update the tasks panel in real-time (or on next render cycle) when the chat assistant creates, completes, or deletes a task, without requiring a full page refresh.
- **FR-011**: System MUST allow both panels in the desktop split view to scroll independently.
- **FR-012**: System MUST transition smoothly between mobile and desktop layouts when the viewport is resized across the 768px breakpoint.

### Key Entities

- **TabState**: Tracks the active tab on mobile ("chat" or "tasks"). Exists only in local component state.
- **ThemeMode**: The active color theme ("light" or "dark"). Derived from OS preference or explicit user toggle.
- **ToolFeedback**: A transient display state showing a contextual message (e.g., "Adding task...") during tool execution. Derived from the user's last message or backend metadata.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Chat interface is fully usable (send, receive, scroll) on a 375px-wide viewport with no horizontal scrollbar.
- **SC-002**: Desktop users at 1280px see a split layout with tasks on the left and chat on the right, both independently scrollable.
- **SC-003**: Mobile tab switching between Chat and Tasks preserves all chat state (messages, input text, scroll position).
- **SC-004**: All UI elements render correctly in both dark and light themes with no hardcoded colors visible in the wrong theme.
- **SC-005**: Tool-specific feedback is shown for at least 3 recognized actions (add, list, complete) instead of generic loading.
- **SC-006**: Layout transitions between mobile and desktop happen without page reload or state loss when resizing the browser.

## Assumptions

- The existing backend `POST /api/chat` endpoint (Spec 6) does not return tool execution metadata. Tool-specific feedback uses client-side heuristics (message pattern matching on the user's input) to display contextual status messages.
- The tasks panel will call an existing backend endpoint to fetch the user's task list. If no such endpoint exists yet, the tasks panel will show a placeholder until one is available.
- Tailwind CSS 4 is the only CSS framework used. No additional UI libraries will be introduced.
- The dark/light theme uses CSS custom properties or Tailwind's `dark:` variant driven by `prefers-color-scheme`. No explicit theme toggle is required for v1 (OS preference only).
- The 768px breakpoint is the standard Tailwind `md` breakpoint and is appropriate for this app's layout needs.

## Dependencies

- **Spec 7** (ChatKit Frontend Integration): The existing `ChatInterface.tsx`, `dashboard/page.tsx`, `login/page.tsx`, `register/page.tsx`, `globals.css`, and `layout.tsx` files are the starting point.
- **Spec 5** (Database Schema & MCP Tools): The tasks data model and MCP tools must be functional for the tasks panel to display real data.
- **Spec 6** (Agent Chat Endpoint): `POST /api/chat` must be operational for the chat to function.

## Out of Scope

- New backend features or API changes (all work is frontend-only).
- Complex animations or page transitions beyond CSS transitions.
- Offline support or service workers.
- User-configurable theme toggle (v1 follows OS preference only).
- Markdown rendering in AI messages.
- Desktop task drag-and-drop or inline task editing.
- Chat history persistence across browser sessions.
