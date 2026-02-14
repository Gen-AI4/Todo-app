# Feature Specification: OpenRouter Agent Integration & Chat Endpoint

**Feature Branch**: `006-agent-chat-endpoint`
**Created**: 2026-02-10
**Status**: Draft
**Input**: User description: "Spec 6: OpenRouter Agent Integration & Chat Endpoint - Target System: FastAPI Backend. Focus: Agentic Logic, OpenRouter Configuration, and API Endpoint."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - User Sends a Natural Language Task Command (Priority: P1)

A user sends a plain-text message like "Add a task called Buy milk" to the chat endpoint. The system routes the message to an AI agent configured via OpenRouter. The agent interprets the intent, invokes the appropriate MCP tool (e.g., `add_task`), and returns a conversational response confirming the action.

**Why this priority**: This is the core interaction loop - without it the chatbot has no functionality. Every other feature depends on this working end-to-end.

**Independent Test**: Send a POST request with a user message, verify the response contains a confirmation of the tool action and the message is persisted.

**Acceptance Scenarios**:

1. **Given** an authenticated user with user_id "user-123", **When** they POST `{"message": "Add a task called Buy milk"}` to the chat endpoint, **Then** the system returns a response confirming the task was created, and a new task "Buy milk" exists for that user.
2. **Given** a user sends a message, **When** the agent processes it, **Then** both the user message and the agent response are saved as Message records linked to a Conversation.
3. **Given** a user sends a task-related command, **When** the agent invokes an MCP tool, **Then** the tool result is incorporated into the agent's response to the user.

---

### User Story 2 - User Asks About Their Tasks (Priority: P1)

A user asks "What are my tasks?" or "Show me my todo list." The agent invokes the `list_tasks` tool and returns a formatted summary of the user's current tasks.

**Why this priority**: Reading tasks is as fundamental as creating them - users need to see their data to manage it.

**Independent Test**: Send a list request, verify the response includes all tasks for that user.

**Acceptance Scenarios**:

1. **Given** a user with 3 existing tasks, **When** they send "What are my tasks?", **Then** the response includes all 3 task titles and their statuses.
2. **Given** a user with no tasks, **When** they send "Show my tasks", **Then** the response indicates the user has no tasks and suggests creating one.

---

### User Story 3 - Multi-Turn Conversation with Context (Priority: P1)

A user has a conversation spanning multiple messages. The system loads prior messages from the database to provide context to the agent, enabling coherent multi-turn interactions.

**Why this priority**: Stateless AI architecture requires context hydration from the database - without this, every message would be treated as a fresh conversation with no memory.

**Independent Test**: Send two sequential messages where the second depends on context from the first, verify the agent response demonstrates awareness of both.

**Acceptance Scenarios**:

1. **Given** a user who previously said "Add a task called Buy groceries", **When** they follow up with "Mark it as done", **Then** the agent identifies the correct task from context and marks "Buy groceries" as completed.
2. **Given** an existing conversation with 5 messages, **When** a new message arrives, **Then** the system loads all prior messages to hydrate the agent's context before processing.
3. **Given** a user starting fresh, **When** they send their first message, **Then** a new Conversation record is created and associated with their user_id.

---

### User Story 4 - Agent Handles Non-Task Conversation (Priority: P2)

A user sends a message that is not a task command, such as "Hello" or "What can you do?" The agent responds conversationally without invoking any tools.

**Why this priority**: Users expect a chatbot to handle general conversation gracefully, not just tool commands.

**Independent Test**: Send a non-task message and verify the response is conversational and no tools were invoked.

**Acceptance Scenarios**:

1. **Given** a user sends "Hello", **When** the agent processes the message, **Then** the response is a friendly greeting that describes the chatbot's capabilities.
2. **Given** a user sends "What can you help me with?", **When** the agent responds, **Then** it lists the available task operations (add, list, complete, update, delete).

---

### User Story 5 - Agent Handles Errors Gracefully (Priority: P2)

When the AI provider is unavailable, a tool fails, or the user's request is ambiguous, the system returns a meaningful error message rather than crashing or returning raw errors.

**Why this priority**: Error resilience is critical for user trust - users should never see stack traces or raw API errors.

**Independent Test**: Simulate a failure scenario and verify the response is a user-friendly error message.

**Acceptance Scenarios**:

1. **Given** the AI provider returns an error, **When** the system processes the request, **Then** the user receives a friendly message like "I'm having trouble right now. Please try again."
2. **Given** a tool invocation fails (e.g., task not found), **When** the agent receives the error, **Then** it translates the error into a user-friendly response like "I couldn't find that task."
3. **Given** the user's message is ambiguous (e.g., "Delete it" with no prior context), **When** the agent processes it, **Then** it asks the user for clarification rather than guessing.

---

### Edge Cases

- What happens when the conversation history is very long (100+ messages)? The system should use a reasonable context window limit or summarization strategy.
- What happens if the user sends concurrent requests? The system should handle race conditions on conversation state.
- What happens if the AI provider rate-limits requests? The system should return a retry-friendly error.
- How does the system handle tool calls that take longer than expected? A timeout mechanism should prevent hanging requests.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST expose a chat endpoint that accepts a user identifier and a text message, routes the message through an AI agent, and returns the agent's response.
- **FR-002**: System MUST configure the AI provider client with the OpenRouter base URL and API key from environment variables.
- **FR-003**: System MUST make MCP tools (add_task, list_tasks, complete_task, delete_task, update_task) available to the agent for invocation during message processing.
- **FR-004**: System MUST persist every user message as a Message record with role "user" before sending to the agent.
- **FR-005**: System MUST persist every agent response as a Message record with role "assistant" after receiving from the agent.
- **FR-006**: System MUST load all prior messages for the active conversation to hydrate agent context on each request.
- **FR-007**: System MUST create a new Conversation record when a user initiates their first chat or starts a new conversation.
- **FR-008**: System MUST pass the authenticated user's user_id to all MCP tool invocations for user isolation.
- **FR-009**: System MUST return user-friendly error messages when the AI provider is unavailable or returns an error.
- **FR-010**: System MUST enforce that each user can only access their own conversations and tasks through the endpoint.
- **FR-011**: System MUST include a system prompt that instructs the agent about its role as a task management assistant and the available tools.
- **FR-012**: System MUST support configurable model selection, defaulting to a standard model if none is specified.

### Key Entities

- **ChatRequest**: Represents an incoming user message to the chat endpoint. Contains the message text and optionally a conversation_id for continuing an existing conversation.
- **ChatResponse**: Represents the agent's reply to the user. Contains the response text, conversation_id, and optionally metadata about tool invocations.
- **Conversation**: (from Spec 5) Represents a chat session. Used to group messages and hydrate context.
- **Message**: (from Spec 5) Represents a single message. Used to persist user inputs and agent responses.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can create, list, complete, update, and delete tasks purely through natural language messages sent to the chat endpoint.
- **SC-002**: Conversation context is maintained across multiple messages - the agent demonstrates awareness of prior exchanges within the same conversation.
- **SC-003**: All user messages and agent responses are persisted, allowing full conversation replay from the database.
- **SC-004**: Chat responses are returned within 10 seconds under normal conditions for single-tool operations.
- **SC-005**: When the AI provider is unavailable, users receive a clear, non-technical error message within 5 seconds.
- **SC-006**: No user can access or modify another user's conversations or tasks through the chat endpoint.

## Assumptions

- MCP tools from Spec 5 (add_task, list_tasks, complete_task, delete_task, update_task) are implemented and functional.
- The Conversation and Message models from Spec 5 are available in the database.
- User authentication is handled by existing JWT middleware (from Spec 2) - the chat endpoint receives a validated user_id.
- The OPENROUTER_API_KEY environment variable is configured and valid.
- A single active conversation per user is sufficient for the initial implementation. Multi-conversation support can be added later.
- The system prompt for the agent is a static string that describes the assistant's role and capabilities.
- Message history loaded for context is limited to a reasonable window (e.g., last 50 messages) to stay within model token limits.

## Out of Scope

- Visual UI components (Spec 7)
- Streaming/Server-Sent Events responses (future enhancement)
- Conversation management (rename, delete, archive conversations)
- File or image attachments in messages
- Multiple concurrent conversations per user
- Agent memory beyond database-persisted message history
