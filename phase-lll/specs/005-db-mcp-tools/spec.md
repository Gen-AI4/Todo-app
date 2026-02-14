# Feature Specification: Database Schema & MCP Tool Server

**Feature Branch**: `005-db-mcp-tools`
**Created**: 2026-02-09
**Status**: Draft
**Input**: User description: "Spec 5: Database Schema & MCP Tool Server - Target System: FastAPI Backend & Neon Database. Focus: Data Models for Chat and MCP Tool Implementation."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - AI Lists User Tasks (Priority: P1)

A user engages the AI chatbot and asks to see their tasks. The AI invokes the `list_tasks` tool, which retrieves all tasks belonging to that specific user from the database and returns them as a structured response.

**Why this priority**: Listing tasks is the foundation of all task management - users must be able to see what they have before they can manage it. This enables the chatbot's core value proposition.

**Independent Test**: Can be tested by invoking the `list_tasks` tool with a valid `user_id` and verifying the returned JSON contains only tasks belonging to that user.

**Acceptance Scenarios**:

1. **Given** a user with 3 existing tasks, **When** the AI invokes `list_tasks` with their `user_id`, **Then** the tool returns a JSON string containing exactly those 3 tasks with id, title, description, status, and timestamps.
2. **Given** a user with no tasks, **When** the AI invokes `list_tasks`, **Then** the tool returns a JSON string indicating an empty task list.
3. **Given** a `user_id` that doesn't exist, **When** the AI invokes `list_tasks`, **Then** the tool returns an empty list (not an error).

---

### User Story 2 - AI Creates a New Task (Priority: P1)

A user tells the AI chatbot to create a new task. The AI extracts the task details and invokes the `add_task` tool, which persists the task in the database associated with the user.

**Why this priority**: Task creation is essential - users cannot manage tasks that don't exist. This is equally critical as listing for the MVP.

**Independent Test**: Can be tested by invoking `add_task` with valid parameters and verifying the task appears in subsequent `list_tasks` calls.

**Acceptance Scenarios**:

1. **Given** a valid `user_id` and task title "Buy groceries", **When** the AI invokes `add_task`, **Then** the tool creates the task and returns a JSON string confirming creation with the new task's id.
2. **Given** a task title and optional description, **When** the AI invokes `add_task`, **Then** the task is stored with status "pending" and creation timestamp.
3. **Given** an empty task title, **When** the AI invokes `add_task`, **Then** the tool returns a JSON error message indicating title is required.

---

### User Story 3 - AI Marks Task Complete (Priority: P2)

A user tells the AI chatbot they finished a task. The AI invokes `complete_task` with the task identifier, which updates the task's status to "completed" in the database.

**Why this priority**: Completing tasks is the primary workflow after creation - users need to track progress. Slightly lower than create/list since those must exist first.

**Independent Test**: Can be tested by creating a task, then invoking `complete_task`, and verifying the status change via `list_tasks`.

**Acceptance Scenarios**:

1. **Given** an existing task with id=5 belonging to user_id=1, **When** the AI invokes `complete_task` with task_id=5 and user_id=1, **Then** the task status changes to "completed" and completion timestamp is set.
2. **Given** a task_id that doesn't exist, **When** the AI invokes `complete_task`, **Then** the tool returns a JSON error message indicating task not found.
3. **Given** a task_id belonging to a different user, **When** the AI invokes `complete_task`, **Then** the tool returns a JSON error message indicating unauthorized access.

---

### User Story 4 - AI Updates Task Details (Priority: P2)

A user wants to modify a task's title or description. The AI invokes `update_task` with the new values, which updates the task in the database.

**Why this priority**: Task modification is a common workflow but secondary to core create/complete cycle.

**Independent Test**: Can be tested by creating a task, invoking `update_task` with new values, and verifying changes via `list_tasks`.

**Acceptance Scenarios**:

1. **Given** an existing task with title "Buy groceries", **When** the AI invokes `update_task` with new title "Buy organic groceries", **Then** the task title is updated and update timestamp is set.
2. **Given** a task_id and user_id, **When** the AI invokes `update_task` with only description changes, **Then** only the description is updated, title remains unchanged.
3. **Given** a task belonging to a different user, **When** the AI invokes `update_task`, **Then** the tool returns a JSON error message indicating unauthorized access.

---

### User Story 5 - AI Deletes a Task (Priority: P3)

A user wants to remove a task entirely. The AI invokes `delete_task`, which removes the task from the database.

**Why this priority**: Deletion is less frequent than other operations and can be worked around by completing tasks.

**Independent Test**: Can be tested by creating a task, invoking `delete_task`, and verifying it no longer appears in `list_tasks`.

**Acceptance Scenarios**:

1. **Given** an existing task belonging to the user, **When** the AI invokes `delete_task`, **Then** the task is permanently removed and a success JSON is returned.
2. **Given** a task_id that doesn't exist, **When** the AI invokes `delete_task`, **Then** the tool returns a JSON error indicating task not found.
3. **Given** a task belonging to a different user, **When** the AI invokes `delete_task`, **Then** the tool returns a JSON error indicating unauthorized access.

---

### User Story 6 - Chat History Persistence (Priority: P1)

When a user starts a conversation with the chatbot, the system loads previous conversation context from the database. New messages are persisted so context is maintained across sessions.

**Why this priority**: Stateless AI architecture requires database-backed context hydration - this enables coherent multi-turn conversations.

**Independent Test**: Can be tested by creating a conversation, adding messages, then loading the conversation in a new request and verifying context is restored.

**Acceptance Scenarios**:

1. **Given** a new user starting their first chat, **When** the system initializes, **Then** a new Conversation record is created and associated with the user_id.
2. **Given** an existing conversation with 5 messages, **When** a new request arrives, **Then** all 5 messages are loaded to hydrate context.
3. **Given** a user sends a new message, **When** the system processes it, **Then** both the user message and AI response are persisted as Message records.

---

### Edge Cases

- What happens when a user has thousands of tasks? The `list_tasks` tool should handle pagination or return a reasonable default limit.
- How does the system handle concurrent task modifications? The database should use appropriate locking/transactions.
- What happens if the database connection fails during a tool operation? Tools should return a JSON error indicating service unavailable.
- How are task IDs generated? IDs must be unique and not expose sensitive information.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a `Conversation` data model with fields: id, user_id, title, created_at, updated_at.
- **FR-002**: System MUST provide a `Message` data model with fields: id, conversation_id, role (user/assistant/tool), content, created_at.
- **FR-003**: System MUST provide a `Task` data model with fields: id, user_id, title, description (optional), status (pending/completed), created_at, updated_at, completed_at.
- **FR-004**: System MUST initialize an MCP Server instance using the official MCP SDK.
- **FR-005**: System MUST implement `add_task` tool that accepts user_id, title, and optional description, creates a Task, and returns JSON confirmation.
- **FR-006**: System MUST implement `list_tasks` tool that accepts user_id and returns JSON array of all tasks for that user.
- **FR-007**: System MUST implement `complete_task` tool that accepts user_id and task_id, updates status to "completed", and returns JSON confirmation.
- **FR-008**: System MUST implement `delete_task` tool that accepts user_id and task_id, removes the task, and returns JSON confirmation.
- **FR-009**: System MUST implement `update_task` tool that accepts user_id, task_id, and optional title/description updates, and returns JSON confirmation.
- **FR-010**: Every MCP tool MUST validate that the `user_id` parameter is provided and that the user owns the target resource.
- **FR-011**: All MCP tools MUST return results as JSON-formatted strings.
- **FR-012**: Tools MUST return appropriate error messages in JSON format when operations fail (not found, unauthorized, validation error).

### Key Entities

- **Conversation**: Represents a chat session between a user and the AI. Contains metadata about the conversation and links to the user. Has many Messages.
- **Message**: Represents a single message in a conversation. Contains role (user, assistant, or tool), content, and timestamps. Belongs to a Conversation.
- **Task**: Represents a user's todo item. Contains title, optional description, status, and timestamps. Belongs to a user via user_id. All CRUD operations filter by user_id for security.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All 5 MCP tools (add, list, complete, delete, update) successfully execute when invoked with valid parameters.
- **SC-002**: Each tool returns properly formatted JSON strings (parseable by standard JSON parsers).
- **SC-003**: Tools correctly enforce user isolation - no tool operation can access or modify another user's tasks.
- **SC-004**: Conversation and Message records persist correctly, allowing context reconstruction across requests.
- **SC-005**: Tool operations complete within 500ms under normal database load.
- **SC-006**: Error scenarios return informative JSON error messages rather than exceptions or stack traces.

## Assumptions

- User authentication and `user_id` extraction is handled by upstream middleware (defined in earlier specs).
- The Neon database connection is already configured and accessible.
- Task status is limited to "pending" and "completed" states for this iteration.
- Conversation title can be auto-generated or left empty initially.
- Message content is stored as plain text (no special formatting requirements).

## Out of Scope

- Chat API endpoint implementation (Spec 6)
- Frontend UI components (Spec 7)
- Task due dates, priorities, or tags
- Task sharing between users
- Conversation search or filtering
- Message editing or deletion
