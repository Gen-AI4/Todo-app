# Tasks: OpenRouter Agent Integration & Chat Endpoint

**Input**: Design documents from `/specs/006-agent-chat-endpoint/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Tests**: Manual testing via Postman per plan.md testing strategy. No automated unit tests for this spec.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/app/`, `backend/tests/`
- Paths based on plan.md structure

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Add OpenAI SDK dependency and create file scaffolds

- [x] T001 Add `openai>=1.0.0` to backend/requirements.txt
- [x] T002 [P] Create empty backend/app/agent.py file
- [x] T003 [P] Create empty backend/app/schemas.py file
- [x] T004 [P] Create empty backend/app/routers/chat.py file

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: OpenRouter client config, schemas, and router registration that MUST be complete before any user story logic

**CRITICAL**: No agent logic can begin until this phase is complete

### OpenRouter Client Configuration (FR-002, FR-012)

- [x] T005 Define OPENROUTER_API_KEY, OPENROUTER_BASE_URL, and DEFAULT_MODEL constants in backend/app/agent.py
- [x] T006 Implement get_openrouter_client() function in backend/app/agent.py with base_url, api_key, and OpenRouter headers (HTTP-Referer, X-Title)
- [x] T007 Define SYSTEM_PROMPT constant in backend/app/agent.py describing the assistant role and available tools

### Request/Response Schemas

- [x] T008 [P] Define ChatRequest Pydantic model in backend/app/schemas.py with message (str) and conversation_id (Optional[UUID]) fields
- [x] T009 [P] Define ChatResponse Pydantic model in backend/app/schemas.py with response (str) and conversation_id (UUID) fields

### Tool Definitions (FR-003)

- [x] T010 Define TOOL_DEFINITIONS list in backend/app/agent.py with OpenAI function-calling schema for add_task (title, description params)
- [x] T011 Add list_tasks tool definition to TOOL_DEFINITIONS in backend/app/agent.py (no params)
- [x] T012 Add complete_task tool definition to TOOL_DEFINITIONS in backend/app/agent.py (task_id param)
- [x] T013 Add delete_task tool definition to TOOL_DEFINITIONS in backend/app/agent.py (task_id param)
- [x] T014 Add update_task tool definition to TOOL_DEFINITIONS in backend/app/agent.py (task_id, title, description params)

### Tool Dispatcher (FR-008)

- [x] T015 Import all _impl functions from backend/app/mcp_tools.py into backend/app/agent.py
- [x] T016 Define TOOL_DISPATCH dictionary mapping tool names to _impl functions in backend/app/agent.py
- [x] T017 Implement execute_tool() function in backend/app/agent.py that injects user_id server-side and dispatches to correct _impl function

### Chat Router Shell (FR-001)

- [x] T018 Create chat router with APIRouter(tags=["Chat"]) in backend/app/routers/chat.py
- [x] T019 Add POST /chat endpoint stub in backend/app/routers/chat.py with Depends(get_current_user) and Depends(get_session)
- [x] T020 Register chat router in backend/app/main.py with app.include_router(chat_router.router, prefix="/api")

**Checkpoint**: Foundation ready - OpenRouter client configured, schemas defined, tools mapped, router registered

---

## Phase 3: User Story 1 - User Sends Natural Language Task Command (Priority: P1) MVP

**Goal**: User sends "Add a task called Buy milk" and receives confirmation that the task was created

**Independent Test**: POST /api/chat with Bearer token and {"message": "Add a task called Buy milk"}, verify response confirms creation and task exists in DB

### Implementation for User Story 1

- [x] T021 [US1] Implement conversation fetch/create logic in run_agent() in backend/app/agent.py: create new Conversation if no conversation_id, else fetch existing with user_id validation
- [x] T022 [US1] Implement message history loading in run_agent() in backend/app/agent.py: select last 50 Messages ordered by created_at for the conversation
- [x] T023 [US1] Implement user message persistence in run_agent() in backend/app/agent.py: save Message with role="user" before calling LLM
- [x] T024 [US1] Implement API payload construction in run_agent() in backend/app/agent.py: system prompt + history + current user message
- [x] T025 [US1] Implement OpenRouter API call in run_agent() in backend/app/agent.py: client.chat.completions.create() with model, messages, and tools
- [x] T026 [US1] Implement tool-call loop in run_agent() in backend/app/agent.py: iterate on tool_calls, execute each via execute_tool(), append results, re-call LLM until no more tool_calls (max 5 iterations)
- [x] T027 [US1] Implement assistant response persistence in run_agent() in backend/app/agent.py: save Message with role="assistant" after final LLM response
- [x] T028 [US1] Wire chat router endpoint to call run_agent() in backend/app/routers/chat.py: pass session, user_id, message, conversation_id and return ChatResponse
- [ ] T029 [US1] Verify via Postman: POST /api/chat with "Add a task called Buy milk" returns success and task exists in DB

**Checkpoint**: Core agent loop functional - user can create tasks via natural language

---

## Phase 4: User Story 2 - User Asks About Their Tasks (Priority: P1)

**Goal**: User sends "What are my tasks?" and receives a formatted list

**Independent Test**: Create tasks for user, POST /api/chat with "What are my tasks?", verify response includes all task titles

### Implementation for User Story 2

- [x] T030 [US2] Verify list_tasks tool definition in TOOL_DEFINITIONS includes correct schema (no required params) in backend/app/agent.py
- [x] T031 [US2] Verify execute_tool() handles list_tasks dispatch correctly (only passes user_id) in backend/app/agent.py
- [ ] T032 [US2] Verify via Postman: POST /api/chat with "What are my tasks?" returns formatted task list for authenticated user

**Checkpoint**: Users can query their task list via natural language

---

## Phase 5: User Story 3 - Multi-Turn Conversation with Context (Priority: P1)

**Goal**: User can have a multi-turn conversation where the agent remembers prior context

**Independent Test**: Send "Add a task called Buy groceries", then send "Mark it as done" with same conversation_id, verify the correct task is completed

### Implementation for User Story 3

- [x] T033 [US3] Ensure ChatResponse includes conversation_id so client can pass it back in subsequent requests in backend/app/routers/chat.py
- [x] T034 [US3] Verify message history loading includes all prior messages (both user and assistant) for context in backend/app/agent.py
- [ ] T035 [US3] Verify via Postman: Send 2 sequential messages using returned conversation_id, confirm agent demonstrates context awareness in second response

**Checkpoint**: Multi-turn conversations work with persistent context

---

## Phase 6: User Story 4 - Agent Handles Non-Task Conversation (Priority: P2)

**Goal**: User sends "Hello" or "What can you do?" and gets a conversational response without tool invocation

**Independent Test**: POST /api/chat with "Hello", verify response is conversational and no tasks were created

### Implementation for User Story 4

- [x] T036 [US4] Verify SYSTEM_PROMPT instructs agent to respond conversationally to greetings and capability questions in backend/app/agent.py
- [x] T037 [US4] Verify run_agent() handles LLM response with no tool_calls (direct text response path) in backend/app/agent.py
- [ ] T038 [US4] Verify via Postman: POST /api/chat with "Hello" returns friendly greeting, no tools invoked

**Checkpoint**: Agent handles general conversation gracefully

---

## Phase 7: User Story 5 - Agent Handles Errors Gracefully (Priority: P2)

**Goal**: When OpenRouter is unavailable or tools fail, user receives friendly error messages

**Independent Test**: Temporarily invalidate API key, send message, verify friendly error returned

### Implementation for User Story 5

- [x] T039 [US5] Add try/except for openai.APIError and openai.APIConnectionError in chat endpoint in backend/app/routers/chat.py returning friendly "having trouble" message
- [x] T040 [US5] Add try/except for openai.RateLimitError in chat endpoint in backend/app/routers/chat.py returning friendly "too many requests" message
- [x] T041 [US5] Add generic Exception catch in chat endpoint in backend/app/routers/chat.py returning friendly "something went wrong" message
- [x] T042 [US5] Ensure run_agent() propagates exceptions cleanly for the router to catch in backend/app/agent.py
- [ ] T043 [US5] Verify via Postman: Set invalid OPENROUTER_API_KEY, send message, confirm friendly error response (not stack trace)

**Checkpoint**: Error scenarios return user-friendly messages

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T044 [P] Add max tool-call iteration guard (limit=5) to prevent infinite loops in backend/app/agent.py
- [x] T045 [P] Add request timeout (30s) to OpenRouter API calls in backend/app/agent.py
- [ ] T046 Verify user isolation: use 2 different JWT tokens via Postman, confirm no cross-access of conversations or tasks
- [ ] T047 Verify all messages (user + assistant) are persisted correctly by querying the Message table directly

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - US1 (task commands): Must complete first - establishes the core agent loop
  - US2 (task queries): Can start after US1 (reuses agent loop)
  - US3 (multi-turn): Can start after US1 (extends conversation handling)
  - US4 (general chat): Can start after US1 (tests no-tool path)
  - US5 (error handling): Can start after US1 (wraps agent in error handling)
- **Polish (Phase 8)**: Depends on all user stories being complete

### User Story Dependencies

| Story | Can Start After | Logical Prerequisites |
|-------|-----------------|----------------------|
| US1 (task commands) | Foundational | None - establishes core loop |
| US2 (task queries) | US1 | Agent loop must work |
| US3 (multi-turn) | US1 | Conversation persistence must work |
| US4 (general chat) | US1 | Agent response path must work |
| US5 (error handling) | US1 | Must have working flow to wrap |

### Within Each User Story

- Implementation before verification
- Postman verification after implementation

### Parallel Opportunities

- All Setup tasks T002-T004 marked [P] can run in parallel
- Foundational schemas T008-T009 can run in parallel
- Polish tasks T044-T045 can run in parallel
- US2, US3, US4, US5 can all start in parallel after US1 completes

---

## Parallel Example: Phase 1 (Setup)

```bash
# Launch all parallel setup tasks together:
Task T002: "Create empty backend/app/agent.py file"
Task T003: "Create empty backend/app/schemas.py file"
Task T004: "Create empty backend/app/routers/chat.py file"
```

## Parallel Example: After US1 Complete

```bash
# Launch US2, US3, US4, US5 verification in parallel:
Task T032: "Verify via Postman: list tasks query"
Task T035: "Verify via Postman: multi-turn context"
Task T038: "Verify via Postman: general conversation"
Task T043: "Verify via Postman: error handling"
```

---

## Implementation Strategy

### MVP First (US1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: US1 (core agent loop)
4. **STOP and VALIDATE**: Test with Postman - can user create a task via chat?
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational -> Foundation ready
2. Add US1 (task commands) -> Test independently -> MVP!
3. Add US2 (task queries) -> Test independently
4. Add US3 (multi-turn) -> Test independently
5. Add US4 (general chat) -> Test independently
6. Add US5 (error handling) -> Test independently
7. Polish -> Final validation

---

## Summary

| Metric | Value |
|--------|-------|
| Total Tasks | 47 |
| Setup Tasks | 4 |
| Foundational Tasks | 16 |
| US1 (task commands) Tasks | 9 |
| US2 (task queries) Tasks | 3 |
| US3 (multi-turn) Tasks | 3 |
| US4 (general chat) Tasks | 3 |
| US5 (error handling) Tasks | 5 |
| Polish Tasks | 4 |
| Parallel Opportunities | 8 tasks marked [P] |

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Testing is manual via Postman (no automated tests for this spec)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- user_id is NEVER exposed to the LLM - always injected server-side (ADR-004)
- Max 5 tool-call iterations to prevent infinite loops
