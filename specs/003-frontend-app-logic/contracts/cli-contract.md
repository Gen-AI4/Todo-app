# CLI API Contract: Task Organization Feature

**Feature**: 1-task-organization
**Created**: 2026-01-01
**Status**: Draft

## Command Extensions

### Add Command
**Current**: `add <task title>`
**Extended**: `add <task title> [OPTIONS]`

**New Options**:
- `--priority, -p <level>`: Set priority level (high|medium|low)
- `--tag, -t <tag>`: Add tag to task (can be used multiple times)
- `--due-date, -d <YYYY-MM-DD>`: Set due date for task

**Examples**:
- `add "Buy Milk" --priority high --tag home`
- `add "Team Meeting" --priority medium --tag work --due-date 2026-01-15`

**Validation**:
- Priority must be one of: high, medium, low (case-insensitive)
- Tag must be a non-empty string
- Due date must be in YYYY-MM-DD format and a valid date

### List Command
**Current**: `list`
**Extended**: `list [OPTIONS]`

**New Options**:
- `--status <status>`: Filter by status (pending|completed)
- `--priority <level>`: Filter by priority (high|medium|low)
- `--tag <tag>`: Filter by tag
- `--search <term>`: Search by keyword (case-insensitive)
- `--sort <method>`: Sort by method (date|priority|alpha)
- `--all`: Show all tasks (including completed)

**Examples**:
- `list --status pending --priority high`
- `list --search "meeting" --sort alpha`
- `list --tag work --sort date`

**Validation**:
- Status must be one of: pending, completed
- Priority must be one of: high, medium, low
- Sort method must be one of: date, priority, alpha

## Data Model Contract

### Task Object
```
{
  "id": integer,
  "title": string,
  "description": string | null,
  "status": "pending" | "completed",
  "priority": "high" | "medium" | "low",
  "tags": string[],
  "due_date": string | null,  // ISO 8601 format: YYYY-MM-DD
  "created_at": string,       // ISO 8601 format
  "completed_at": string | null  // ISO 8601 format
}
```

### Filter Object
```
{
  "status": "pending" | "completed" | null,
  "priority": "high" | "medium" | "low" | null,
  "tags": string[] | null,
  "search_term": string | null,
  "due_date": string | null  // YYYY-MM-DD format
}
```

### Sort Criteria
```
{
  "method": "date" | "priority" | "alpha",
  "direction": "asc" | "desc"  // default: asc
}
```

## Response Formats

### Add Command Response
**Success**:
```
Task added: {id} {title}
  Priority: {priority}
  Tags: {tags}
  Due Date: {due_date}
```

**Error**:
```
Error: {error_message}
```

### List Command Response
**Success** (formatted as ASCII table):
```
┌─────┬─────────────────────┬──────────┬──────────────┬──────────────┐
│ ID  │ Title               │ Priority │ Status       │ Tags         │
├─────┼─────────────────────┼──────────┼──────────────┼──────────────┤
│ 1   │ Buy Milk            │ high     │ pending      │ home         │
│ 2   │ Team Meeting        │ medium   │ completed    │ work         │
└─────┴─────────────────────┴──────────┴──────────────┴──────────────┘
```

### Error Responses
- Invalid command format: "Error: {specific error message}"
- Invalid argument: "Error: Invalid {argument_name}. {help_text}"
- Task not found: "Error: Task ID {id} not found"

## Validation Rules

### Input Validation
1. All string inputs must be trimmed of leading/trailing whitespace
2. Priority values are case-insensitive
3. Date format must be YYYY-MM-DD
4. Task titles must not be empty after trimming

### Business Logic Validation
1. A task cannot have an empty title
2. Priority must be one of the defined values (high, medium, low)
3. Due date cannot be in the past for new tasks
4. Multiple tags can be added to a single task
5. Search is case-insensitive substring matching

## Backward Compatibility
- All existing commands must continue to work without modification
- Existing task data without priority/tags must be handled gracefully
- Default priority should be "medium" for tasks without explicit priority
- Default tags list should be empty for tasks without tags