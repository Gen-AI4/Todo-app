# API Contracts: CLI To-Do App - Recurring Tasks & Due Dates

## Command Interface Contracts

### Add Command
**Command**: `todo add "<task_title>" [--due <date>] [--recur <frequency>]`

**Input Parameters**:
- `task_title` (required): String containing the task description
- `--due <date>` (optional): Date specification in natural language or ISO 8601 format
- `--recur <frequency>` (optional): Recurrence frequency (daily|weekly|monthly|yearly)

**Success Response**:
- Status: Success
- Output: "Task added successfully with ID: <id>"

**Error Responses**:
- Invalid date format: "Error: Invalid date format specified"
- Invalid recurrence: "Error: Invalid recurrence frequency specified"

### List Command
**Command**: `todo list`

**Input Parameters**: None

**Success Response**:
- Status: Success
- Output: Formatted list of tasks with due dates and color coding based on urgency

**Output Format**:
```
ID | Title | Status | Due Date | Recurrence
-- | ----- | ------ | -------- | ----------
1  | Task  | PENDING| 2024-01-02 (RED - OVERDUE) | none
2  | Task  | PENDING| 2024-01-01 (YELLOW - TODAY) | weekly
```

### Complete Command
**Command**: `todo complete <task_id>`

**Input Parameters**:
- `task_id` (required): ID of the task to mark as complete

**Success Response**:
- Status: Success
- Output: "Task marked as complete"
- If recurring: "New instance of recurring task created with ID: <new_id>"

**Error Responses**:
- Task not found: "Error: Task with ID <id> not found"

### Notify Command
**Command**: `todo notify`

**Input Parameters**: None

**Success Response**:
- Status: Success
- Output: Summary of pending tasks due today and overdue tasks
- If OS notifications enabled: Sends desktop notification for urgent tasks

## Internal Service Contracts

### Date Parser Service
**Function**: `parse_natural_date(input: str) -> datetime | None`

**Input**: Natural language date string (e.g., "tomorrow", "next Friday")
**Output**: Parsed datetime object in UTC, or None if parsing fails

### Recurrence Service
**Function**: `generate_next_occurrence(task: Task) -> Task | None`

**Input**: Completed recurring task object
**Output**: New task object with updated due date based on recurrence pattern, or None if recurrence should end

### Notification Service
**Function**: `check_due_tasks() -> List[Task]`

**Input**: None
**Output**: List of tasks that are due today or overdue

**Function**: `send_notification(task: Task) -> bool`

**Input**: Task object requiring notification
**Output**: Boolean indicating if notification was sent successfully