# Tasks: Database Schema & MCP Tool Server

**Input**: Design documents from `/specs/005-db-mcp-tools/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Tests**: Unit tests included per plan.md testing strategy.

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

**Purpose**: Add MCP SDK dependency and prepare project structure

- [x] T001 Add `mcp` package to backend/requirements.txt
- [x] T002 [P] Create empty backend/app/mcp_server.py file
- [x] T003 [P] Create empty backend/app/mcp_tools.py file
- [x] T004 [P] Create empty backend/tests/test_mcp_tools.py file
- [x] T005 [P] Create empty backend/tests/test_models.py file

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core models and MCP server infrastructure that MUST be complete before ANY tool can be implemented

### Data Models (FR-001, FR-002)

- [x] T006 Add Conversation model to backend/app/models.py with fields: id (UUID), user_id (str), title (Optional[str]), created_at, updated_at
- [x] T007 Add Message model to backend/app/models.py with fields: id (UUID), conversation_id (UUID FK), role (str), content (str), created_at

### MCP Server Infrastructure (FR-004)

- [x] T008 Initialize FastMCP server instance in backend/app/mcp_server.py with name "todo-ai-chatbot"
- [x] T009 Define Pydantic input schemas in backend/app/mcp_tools.py: AddTaskInput, ListTasksInput, TaskIdInput, UpdateTaskInput
- [x] T010 Create JSON response helper functions in backend/app/mcp_tools.py: success_response(), error_response()
- [x] T011 Create database session helper in backend/app/mcp_tools.py: get_db_session()

**Checkpoint**: Foundation ready - MCP tools can now be implemented in parallel

---

## Phase 3: User Story 6 - Chat History Persistence (Priority: P1)

**Goal**: Enable chat context to persist across sessions via Conversation/Message tables

**Independent Test**: Create conversation, add messages, verify retrieval in new request

### Tests for User Story 6

- [x] T012 [P] [US6] Write test_create_conversation in backend/tests/test_models.py
- [x] T013 [P] [US6] Write test_create_message_with_conversation in backend/tests/test_models.py
- [x] T014 [P] [US6] Write test_message_foreign_key_constraint in backend/tests/test_models.py

### Implementation for User Story 6

- [x] T015 [US6] Verify Conversation and Message tables are created via create_db_and_tables() in backend/app/main.py lifespan
- [x] T016 [US6] Run pytest backend/tests/test_models.py to validate model tests pass

**Checkpoint**: Chat persistence models functional and tested

---

## Phase 4: User Story 1 - AI Lists User Tasks (Priority: P1)

**Goal**: AI can retrieve all tasks for a specific user via `list_tasks` tool

**Independent Test**: Invoke list_tasks with user_id, verify JSON response contains only that user's tasks

### Tests for User Story 1

- [x] T017 [P] [US1] Write test_list_tasks_returns_user_tasks_only in backend/tests/test_mcp_tools.py
- [x] T018 [P] [US1] Write test_list_tasks_empty_for_new_user in backend/tests/test_mcp_tools.py
- [x] T019 [P] [US1] Write test_list_tasks_json_format in backend/tests/test_mcp_tools.py

### Implementation for User Story 1

- [x] T020 [US1] Implement list_tasks tool function in backend/app/mcp_tools.py with @mcp.tool() decorator
- [x] T021 [US1] Add user_id filtering logic to list_tasks in backend/app/mcp_tools.py
- [x] T022 [US1] Register list_tasks tool with MCP server in backend/app/mcp_tools.py
- [x] T023 [US1] Run pytest backend/tests/test_mcp_tools.py::TestListTasks to validate

**Checkpoint**: list_tasks tool functional and tested

---

## Phase 5: User Story 2 - AI Creates a New Task (Priority: P1)

**Goal**: AI can create new tasks for a user via `add_task` tool

**Independent Test**: Invoke add_task with user_id and title, verify task created and JSON confirmation returned

### Tests for User Story 2

- [x] T024 [P] [US2] Write test_add_task_success in backend/tests/test_mcp_tools.py
- [x] T025 [P] [US2] Write test_add_task_with_description in backend/tests/test_mcp_tools.py
- [x] T026 [P] [US2] Write test_add_task_empty_title_fails in backend/tests/test_mcp_tools.py
- [x] T027 [P] [US2] Write test_add_task_json_format in backend/tests/test_mcp_tools.py

### Implementation for User Story 2

- [x] T028 [US2] Implement add_task tool function in backend/app/mcp_tools.py with @mcp.tool() decorator
- [x] T029 [US2] Add task creation logic with user_id in backend/app/mcp_tools.py
- [x] T030 [US2] Add title validation (non-empty) in backend/app/mcp_tools.py
- [x] T031 [US2] Register add_task tool with MCP server in backend/app/mcp_tools.py
- [x] T032 [US2] Run pytest backend/tests/test_mcp_tools.py::TestAddTask to validate

**Checkpoint**: add_task tool functional and tested

---

## Phase 6: User Story 3 - AI Marks Task Complete (Priority: P2)

**Goal**: AI can mark a task as completed via `complete_task` tool

**Independent Test**: Create task, invoke complete_task, verify status changes to completed

### Tests for User Story 3

- [x] T033 [P] [US3] Write test_complete_task_success in backend/tests/test_mcp_tools.py
- [x] T034 [P] [US3] Write test_complete_task_not_found in backend/tests/test_mcp_tools.py
- [x] T035 [P] [US3] Write test_complete_task_wrong_user in backend/tests/test_mcp_tools.py
- [x] T036 [P] [US3] Write test_complete_task_json_format in backend/tests/test_mcp_tools.py

### Implementation for User Story 3

- [x] T037 [US3] Implement complete_task tool function in backend/app/mcp_tools.py with @mcp.tool() decorator
- [x] T038 [US3] Add task lookup with user_id validation in backend/app/mcp_tools.py
- [x] T039 [US3] Add is_completed=True update logic in backend/app/mcp_tools.py
- [x] T040 [US3] Add error handling for not_found and unauthorized cases in backend/app/mcp_tools.py
- [x] T041 [US3] Register complete_task tool with MCP server in backend/app/mcp_tools.py
- [x] T042 [US3] Run pytest backend/tests/test_mcp_tools.py::TestCompleteTask to validate

**Checkpoint**: complete_task tool functional and tested

---

## Phase 7: User Story 4 - AI Updates Task Details (Priority: P2)

**Goal**: AI can update task title/description via `update_task` tool

**Independent Test**: Create task, invoke update_task with new values, verify changes persist

### Tests for User Story 4

- [x] T043 [P] [US4] Write test_update_task_title in backend/tests/test_mcp_tools.py
- [x] T044 [P] [US4] Write test_update_task_description_only in backend/tests/test_mcp_tools.py
- [x] T045 [P] [US4] Write test_update_task_not_found in backend/tests/test_mcp_tools.py
- [x] T046 [P] [US4] Write test_update_task_wrong_user in backend/tests/test_mcp_tools.py
- [x] T047 [P] [US4] Write test_update_task_json_format in backend/tests/test_mcp_tools.py

### Implementation for User Story 4

- [x] T048 [US4] Implement update_task tool function in backend/app/mcp_tools.py with @mcp.tool() decorator
- [x] T049 [US4] Add task lookup with user_id validation in backend/app/mcp_tools.py
- [x] T050 [US4] Add partial update logic (only update provided fields) in backend/app/mcp_tools.py
- [x] T051 [US4] Add updated_at timestamp update in backend/app/mcp_tools.py
- [x] T052 [US4] Register update_task tool with MCP server in backend/app/mcp_tools.py
- [x] T053 [US4] Run pytest backend/tests/test_mcp_tools.py::TestUpdateTask to validate

**Checkpoint**: update_task tool functional and tested

---

## Phase 8: User Story 5 - AI Deletes a Task (Priority: P3)

**Goal**: AI can permanently remove a task via `delete_task` tool

**Independent Test**: Create task, invoke delete_task, verify task no longer exists

### Tests for User Story 5

- [x] T054 [P] [US5] Write test_delete_task_success in backend/tests/test_mcp_tools.py
- [x] T055 [P] [US5] Write test_delete_task_not_found in backend/tests/test_mcp_tools.py
- [x] T056 [P] [US5] Write test_delete_task_wrong_user in backend/tests/test_mcp_tools.py
- [x] T057 [P] [US5] Write test_delete_task_json_format in backend/tests/test_mcp_tools.py

### Implementation for User Story 5

- [x] T058 [US5] Implement delete_task tool function in backend/app/mcp_tools.py with @mcp.tool() decorator
- [x] T059 [US5] Add task lookup with user_id validation in backend/app/mcp_tools.py
- [x] T060 [US5] Add session.delete() logic in backend/app/mcp_tools.py
- [x] T061 [US5] Add error handling for not_found and unauthorized cases in backend/app/mcp_tools.py
- [x] T062 [US5] Register delete_task tool with MCP server in backend/app/mcp_tools.py
- [x] T063 [US5] Run pytest backend/tests/test_mcp_tools.py::TestDeleteTask to validate

**Checkpoint**: delete_task tool functional and tested

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T064 [P] Add docstrings to all tool functions in backend/app/mcp_tools.py
- [x] T065 [P] Add type hints validation with mypy for backend/app/mcp_tools.py
- [x] T066 Run full test suite: pytest backend/tests/ -v
- [x] T067 Verify all 5 tools return consistent JSON format per plan.md ADR-001
- [x] T068 Manual verification: Test tool operations complete within 500ms (SC-005)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-8)**: All depend on Foundational phase completion
- **Polish (Phase 9)**: Depends on all user stories being complete

### User Story Dependencies

| Story | Can Start After | Logical Prerequisites |
|-------|-----------------|----------------------|
| US6 (Chat) | Foundational | None |
| US1 (list) | Foundational | None |
| US2 (add) | Foundational | None |
| US3 (complete) | Foundational | Tasks must exist (add_task) |
| US4 (update) | Foundational | Tasks must exist (add_task) |
| US5 (delete) | Foundational | Tasks must exist (add_task) |

---

## Summary

| Metric | Value |
|--------|-------|
| Total Tasks | 68 |
| All Tasks | COMPLETE |
