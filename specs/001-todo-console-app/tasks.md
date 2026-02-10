# Development Tasks: Todo In-Memory Python Console App

**Feature**: Todo In-Memory Python Console App
**Branch**: 001-todo-console-app
**Generated**: 2026-02-05
**Based on**: specs/001-todo-console-app/spec.md, plan.md, data-model.md

## Implementation Strategy

Build the application in priority order following the user stories. Start with core functionality (adding and viewing tasks) before implementing update, delete, and completion features. Each user story should be independently testable and deliver value.

## Phase 1: Project Setup

Goal: Establish project foundation with proper structure and dependencies.

- [X] T001 Create project directory structure (src/models/, src/services/, src/cli/, tests/unit/, tests/integration/)
- [X] T002 Initialize Python project with `uv init` and create pyproject.toml
- [X] T003 Configure pytest in pyproject.toml with proper test paths
- [X] T004 Set up basic project configuration files (.gitignore, README.md)

## Phase 2: Foundational Components

Goal: Create core data structures and service foundation needed by all user stories.

- [X] T005 [P] Create Task dataclass in src/models/task.py with id, description, and completed fields
- [X] T006 [P] Create TodoList class in src/services/todo_service.py with in-memory storage
- [X] T007 [P] Implement ID generation logic with auto-increment in TodoList class
- [X] T008 [P] Create basic CLI structure in src/cli/main.py with menu display
- [X] T009 Implement validation for task descriptions in models

## Phase 3: User Story 1 - Add New Todo Task (Priority: P1)

Goal: Enable users to add new tasks to their todo list.

**Independent Test Criteria**: User can run the application, select the add task option, enter a task description, and verify that the task appears in the list.

- [X] T010 [P] [US1] Implement add_task method in TodoService that validates description and assigns unique ID
- [X] T011 [P] [US1] Create CLI function to handle add task user input and validation
- [X] T012 [P] [US1] Add menu option for adding tasks in main CLI loop
- [X] T013 [US1] Test add task functionality with valid and invalid inputs
- [X] T014 [US1] Handle empty description error case with user-friendly message

## Phase 4: User Story 2 - View All Todo Tasks (Priority: P1)

Goal: Allow users to view all their tasks with completion status.

**Independent Test Criteria**: User can add several tasks and then select the view option to confirm all tasks are displayed with their status.

- [X] T015 [P] [US2] Implement get_all_tasks method in TodoService to return all tasks
- [X] T016 [P] [US2] Create CLI function to display tasks in a formatted list
- [X] T017 [P] [US2] Add menu option for viewing tasks in main CLI loop
- [X] T018 [US2] Handle empty list case with appropriate message
- [X] T019 [US2] Test view functionality with various task sets and completion statuses

## Phase 5: User Story 3 - Mark Tasks Complete (Priority: P2)

Goal: Enable users to mark tasks as complete to track progress.

**Independent Test Criteria**: User can add a task, select it to mark as complete, and verify its status changes in the system.

- [X] T020 [P] [US3] Implement mark_complete and mark_incomplete methods in TodoService
- [X] T021 [P] [US3] Create CLI function to handle mark complete/incomplete user input
- [X] T022 [P] [US3] Add menu option for marking tasks in main CLI loop
- [X] T023 [US3] Test marking tasks with valid and invalid IDs
- [X] T024 [US3] Handle invalid task ID error case with user-friendly message

## Phase 6: User Story 4 - Update Task Description (Priority: P2)

Goal: Allow users to modify task descriptions as needed.

**Independent Test Criteria**: User can add a task, update its description, and verify the change is saved and displayed correctly.

- [X] T025 [P] [US4] Implement update_task method in TodoService with validation
- [X] T026 [P] [US4] Create CLI function to handle update task user input
- [X] T027 [P] [US4] Add menu option for updating tasks in main CLI loop
- [X] T028 [US4] Test updating tasks with valid and invalid inputs
- [X] T029 [US4] Handle invalid task ID and empty description error cases

## Phase 7: User Story 5 - Delete Tasks (Priority: P3)

Goal: Enable users to remove irrelevant tasks to maintain organized lists.

**Independent Test Criteria**: User can add a task, delete it, and verify it no longer appears in the list.

- [X] T030 [P] [US5] Implement delete_task method in TodoService
- [X] T031 [P] [US5] Create CLI function to handle delete task user input with confirmation
- [X] T032 [P] [US5] Add menu option for deleting tasks in main CLI loop
- [X] T033 [US5] Test deleting tasks with valid and invalid IDs
- [X] T034 [US5] Handle invalid task ID error case with user-friendly message

## Phase 8: Error Handling and Edge Cases

Goal: Implement comprehensive error handling for all user inputs and edge cases.

- [X] T035 [P] Implement input validation for all CLI functions to handle non-numeric IDs
- [X] T036 [P] Add error handling for accessing non-existent task IDs
- [X] T037 Handle extremely long task descriptions with appropriate limits
- [X] T038 Add error handling for operations on empty lists
- [X] T039 Test all error scenarios and edge cases

## Phase 9: Polish & Cross-Cutting Concerns

Goal: Complete the application with proper documentation, testing, and final touches.

- [X] T040 [P] Add docstrings to all classes and methods following Python standards
- [X] T041 [P] Create comprehensive unit tests for all service methods
- [X] T042 [P] Create integration tests for CLI flows
- [X] T043 [P] Add type hints to all function signatures
- [X] T044 [P] Improve user interface with better formatting and messages
- [X] T045 [P] Update README.md with usage instructions
- [X] T046 Run complete application test to verify all functionality works together

## Dependencies

User stories can be developed in parallel after Phase 2 foundational components are complete. Each story builds upon the shared data models and service foundation.

## Parallel Execution Opportunities

- Tasks within each user story phase can be developed in parallel (marked with [P])
- Model and service development can happen simultaneously with CLI development
- Testing can be done in parallel with implementation
- Documentation can be updated throughout development