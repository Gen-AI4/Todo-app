# Data Model: CLI To-Do App - Recurring Tasks & Due Dates

## Task Entity

**Fields:**
- `id` (string/UUID): Unique identifier for the task
- `title` (string): The task description/text
- `status` (enum): "pending" | "completed"
- `due_date` (string): ISO 8601 formatted date/time in UTC (optional)
- `completed_at` (string): ISO 8601 formatted date/time in UTC (optional)
- `recurrence_pattern` (object): Recurrence configuration (optional)
- `created_at` (string): ISO 8601 formatted date/time in UTC
- `updated_at` (string): ISO 8601 formatted date/time in UTC

**Validation Rules:**
- `title` is required and non-empty
- `status` must be one of the allowed values
- `due_date` must be a valid ISO 8601 date if present
- `recurrence_pattern` must follow the RecurrencePattern schema if present

## RecurrencePattern Entity

**Fields:**
- `frequency` (enum): "daily" | "weekly" | "monthly" | "yearly"
- `interval` (integer): How many periods between occurrences (default: 1)
- `end_date` (string): Optional ISO 8601 date when recurrence ends (optional)
- `occurrence_count` (integer): Optional maximum number of occurrences (optional)

**Validation Rules:**
- `frequency` is required and must be one of the allowed values
- `interval` must be a positive integer
- `end_date` and `occurrence_count` are mutually exclusive optional fields
- If both are absent, the recurrence continues indefinitely

## State Transitions

**Task Status Transitions:**
- `pending` → `completed` (when user marks task as done)
- `completed` → `pending` (when user unmarks task as done)

**Recurrence Logic:**
- When a recurring task transitions from `pending` to `completed`, a new task is created with the next occurrence date calculated based on the recurrence pattern
- The new task inherits all properties from the parent task except the due date and ID

## Relationships

- Each Task may have one RecurrencePattern (optional)
- RecurrencePattern is embedded within the Task entity (no separate table/structure needed)