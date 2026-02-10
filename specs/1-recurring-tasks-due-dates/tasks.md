# Tasks: CLI To-Do App - Recurring Tasks & Due Dates

**Feature**: CLI To-Do App - Recurring Tasks & Due Dates
**Branch**: `1-recurring-tasks-due-dates`
**Spec**: [specs/1-recurring-tasks-due-dates/spec.md](../specs/1-recurring-tasks-due-dates/spec.md)
**Plan**: [specs/1-recurring-tasks-due-dates/plan.md](../specs/1-recurring-tasks-due-dates/plan.md)

## Implementation Strategy

The tasks are organized by user story priority to enable independent implementation and testing. User Story 1 (due dates) is implemented first as the foundation, followed by User Story 2 (recurring tasks), and finally User Story 3 (notifications).

## Dependencies

- User Story 1 must be completed before User Story 2
- User Story 2 must be completed before User Story 3
- Core data model changes are prerequisites for all stories

## Parallel Execution Opportunities

- Date parsing and timezone utilities can be developed in parallel with model updates
- CLI command updates can be developed in parallel after model changes
- Unit tests can be written in parallel with implementation

---

## Phase 1: Setup & Infrastructure

- [ ] T001 Create models directory: `mkdir -p src/models`
- [ ] T002 Create services directory: `mkdir -p src/services`
- [ ] T003 Create cli directory: `mkdir -p src/cli/commands`
- [ ] T004 Create lib directory: `mkdir -p src/lib`
- [ ] T005 [P] Install required dependencies: `pip install python-dateutil colorama`

---

## Phase 2: Foundational Components

- [ ] T006 [P] Create RecurrencePattern class in src/models/recurrence.py with fields: frequency, interval, end_date, occurrence_count
- [ ] T007 [P] Update Task class in src/models/task.py to include due_date, recurrence_pattern, created_at, updated_at, completed_at fields
- [ ] T008 [P] Create date_parser.py in src/lib/ for natural language date parsing using dateutil
- [ ] T009 [P] Create timezone_utils.py in src/lib/ for timezone handling
- [ ] T010 [P] Create date_parser_service.py in src/services/ with parse_natural_date function
- [ ] T011 [P] Create notification_service.py in src/services/ with check_due_tasks and send_notification functions
- [ ] T012 [P] Create recurrence_service.py in src/services/ with generate_next_occurrence function

---

## Phase 3: User Story 1 - Set Due Dates for Tasks (Priority: P1)

**Story Goal**: Users can create tasks with due dates using natural language input and view them in the task list with their due dates displayed.

**Independent Test**: Users can create tasks with due dates using natural language input (e.g., "task due tomorrow" or "task due next Friday") and view them in the task list with their due dates displayed.

- [ ] T013 [P] [US1] Update CLI add command to accept --due flag in src/cli/commands/add.py
- [ ] T014 [P] [US1] Implement natural language date parsing in add command using dateutil
- [ ] T015 [US1] Update CLI list command to sort tasks by due date in src/cli/commands/list.py
- [ ] T016 [US1] Implement color coding for due date urgency (Red=Overdue, Yellow=Today, Orange=Soon, Green=Future) in list command
- [ ] T017 [US1] Update task display format to show due dates in human-readable format
- [ ] T018 [US1] Add unit test for natural language date parsing in tests/unit/test_date_parser.py
- [ ] T019 [US1] Add integration test for add command with due dates in tests/integration/test_cli_commands.py
- [ ] T020 [US1] Add integration test for list command with due date sorting and color coding in tests/integration/test_cli_commands.py

---

## Phase 4: User Story 2 - Create Recurring Tasks (Priority: P1)

**Story Goal**: Users can create recurring tasks that automatically generate new instances based on the recurrence pattern when the previous instance is completed.

**Independent Test**: Users can create a recurring task that automatically generates new instances based on the recurrence pattern when the previous instance is completed.

- [ ] T021 [P] [US2] Update CLI add command to accept --recur flag with frequency options in src/cli/commands/add.py
- [ ] T022 [US2] Implement recurrence pattern validation in add command
- [ ] T023 [US2] Update CLI complete command to check for recurring tasks in src/cli/commands/complete.py
- [ ] T024 [US2] Implement next date calculator in recurrence_service.py for generating next occurrence
- [ ] T025 [US2] Implement lazy generation logic that creates new task instance when parent is marked complete
- [ ] T026 [US2] Handle recurrence end conditions (end_date, occurrence_count, indefinite)
- [ ] T027 [US2] Add unit test for recurrence calculation in tests/unit/test_recurrence.py
- [ ] T028 [US2] Add integration test for recurring task creation and completion in tests/integration/test_cli_commands.py

---

## Phase 5: User Story 3 - Receive Notifications for Due Tasks (Priority: P2)

**Story Goal**: Users can see pending tasks when opening their terminal, and optionally receive system notifications for due tasks.

**Independent Test**: Users can see pending tasks when opening their terminal, and optionally receive system notifications for due tasks.

- [ ] T029 [P] [US3] Create notify command in src/cli/commands/notify.py that summarizes urgent tasks
- [ ] T030 [US3] Implement logic to identify overdue and due-today tasks in notification_service.py
- [ ] T031 [US3] Implement OS-level notification integration (notify-send for Linux, osascript for macOS, PowerShell for Windows)
- [ ] T032 [US3] Add command to show pending tasks on terminal startup
- [ ] T033 [US3] Add unit test for notification service in tests/unit/test_notification.py
- [ ] T034 [US3] Add integration test for notify command in tests/integration/test_cli_commands.py

---

## Phase 6: Polish & Cross-Cutting Concerns

- [ ] T035 Update main CLI entry point in src/cli/main.py to include new commands
- [ ] T036 Update help documentation to include new --due and --recur options
- [ ] T037 Add error handling for invalid date formats and recurrence patterns
- [ ] T038 Implement data migration for existing JSON data to support new schema
- [ ] T039 Add comprehensive error messages for date parsing failures
- [ ] T040 Add edge case handling for "February 30th" and other invalid dates
- [ ] T041 Update README with examples of new due date and recurring task features
- [ ] T042 Write contract tests for all new API endpoints in tests/contract/test_api_contracts.py
- [ ] T043 Perform end-to-end testing of all user stories
- [ ] T044 Update quickstart guide with new feature examples