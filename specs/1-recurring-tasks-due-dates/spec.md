# Feature Specification: CLI To-Do App - Recurring Tasks & Due Dates

**Feature Branch**: `1-recurring-tasks-due-dates`
**Created**: 2026-01-01
**Status**: Draft
**Input**: User description: "Context: I am developing a CLI-based To-Do app and am currently in the \"Advanced Phase\" (Recurring Tasks & Due Dates). I need to lock down the technical specifications before implementation to avoid complexity creep.

Objective: Generate a detailed technical specification (sp.specify) that defines exactly how the system handles time, recurrence, and user input.

Topics to Specify:

Date/Time Handling:

What is the standard date format for storage (e.g., ISO 8601, UTC)?

How will the CLI parse user inputs like \"next Friday\" or \"tomorrow\"? (Library vs. Custom Regex).

Timezone strategy: Do we store in UTC and display in Local, or store Local?

Recurrence Logic:

Trigger Event: When is the next task created? (e.g., Immediately upon creation of the parent? Or only when the parent is marked 'Done'?)

Calculation: How do we calculate \"Weekly\"? Is it 7 days from the due date or 7 days from the completion date? (This is a crucial UX decision).

Storage: Do recurring tasks get a special flag or a \"frequency\" field (e.g., freq: \"weekly\")?

Notification Strategy (CLI Context):

Since a CLI isn't always running, define the \"Active Check\" mechanism.

Specification for a notify command that can be added to .bashrc or .zshrc to show pending tasks on terminal startup.

(Optional) Specification for integration with OS-level notifiers (notify-send, AppleScript).

Output Format:

Produce a structured list of Decisions and Rules.

Use \"Must\", \"Should\", and \"Could\" terminology (MoSCoW method).

Include a brief \"Data Schema Changes\" section outlining the exact JSON/Struct fields needed."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Set Due Dates for Tasks (Priority: P1)

As a CLI To-Do app user, I want to set due dates for my tasks so that I can track deadlines and manage my time effectively.

**Why this priority**: Due dates form the core functionality of the advanced phase and provide immediate value by helping users prioritize tasks.

**Independent Test**: Users can create tasks with due dates using natural language input (e.g., "task due tomorrow" or "task due next Friday") and view them in the task list with their due dates displayed.

**Acceptance Scenarios**:

1. **Given** a user has opened the CLI to-do app, **When** the user runs `todo add "Buy groceries due tomorrow"`, **Then** the task "Buy groceries" is created with tomorrow's date as the due date
2. **Given** a user has tasks with due dates, **When** the user runs `todo list`, **Then** the tasks are displayed with their due dates in a readable format

---

### User Story 2 - Create Recurring Tasks (Priority: P1)

As a CLI To-Do app user, I want to create recurring tasks so that I don't have to manually re-create regular tasks like weekly meetings or monthly bills.

**Why this priority**: Recurring tasks eliminate repetitive work and are essential for users with routine obligations.

**Independent Test**: Users can create a recurring task that automatically generates new instances based on the recurrence pattern when the previous instance is completed.

**Acceptance Scenarios**:

1. **Given** a user wants to create a recurring task, **When** the user runs `todo add "Weekly team meeting recurring weekly"`, **Then** the task is marked as recurring with a weekly frequency
2. **Given** a recurring task exists, **When** the user marks the task as done, **Then** a new instance of the same task is created according to the recurrence pattern

---

### User Story 3 - Receive Notifications for Due Tasks (Priority: P2)

As a CLI To-Do app user, I want to receive notifications for tasks that are due so that I don't miss important deadlines.

**Why this priority**: Notifications help ensure users stay on top of their tasks without needing to constantly check the app.

**Independent Test**: Users can see pending tasks when opening their terminal, and optionally receive system notifications for due tasks.

**Acceptance Scenarios**:

1. **Given** the user has pending tasks with due dates, **When** the user opens a new terminal session, **Then** a notification command displays pending tasks automatically
2. **Given** tasks are due today, **When** the system notification mechanism is active, **Then** users receive OS-level notifications about these tasks

---

### Edge Cases

- What happens when a recurring task is due but the user doesn't complete the previous instance?
- How does the system handle timezone changes when users travel across timezones?
- What happens when the same recurring task is created multiple times?
- How does the system handle invalid date inputs like "February 30th"?
- What happens when multiple recurring tasks are due simultaneously?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST store all dates and times in ISO 8601 format (UTC) for consistency and timezone handling
- **FR-002**: System MUST parse natural language date inputs (e.g., "tomorrow", "next Friday", "in 3 days") using a date parsing library
- **FR-003**: System MUST display dates and times in the user's local timezone when showing tasks to the user
- **FR-004**: System MUST create a new instance of a recurring task only when the parent task is marked as 'Done'
- **FR-005**: System MUST calculate recurring intervals based on completion date rather than due date for better user experience
- **FR-006**: System MUST add a 'frequency' field to recurring tasks (e.g., daily, weekly, monthly) to determine recurrence pattern
- **FR-007**: System MUST provide a 'notify' command that can be added to shell configuration files (.bashrc/.zshrc) to show pending tasks on terminal startup
- **FR-008**: System MUST integrate with OS-level notification systems (notify-send for Linux, AppleScript for macOS) to send desktop notifications
- **FR-009**: System MUST support common recurrence patterns: daily, weekly, monthly, yearly
- **FR-010**: System MUST allow users to create recurring tasks with due dates

### Key Entities

- **Task**: Represents a to-do item with title, status (completed/incomplete), optional due date, and recurrence information
- **RecurrencePattern**: Defines the frequency and rules for task repetition (e.g., weekly, monthly) with possible custom intervals
- **Notification**: Represents a reminder mechanism that can be triggered by due dates or system events

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can create tasks with due dates using natural language input with 95% accuracy in date interpretation
- **SC-002**: Recurring tasks are automatically generated within 1 second of marking the parent task as done
- **SC-003**: The notification system displays pending tasks on terminal startup in under 0.5 seconds
- **SC-004**: 90% of users successfully create recurring tasks without needing documentation
- **SC-005**: System correctly handles timezone conversions for 100% of international users