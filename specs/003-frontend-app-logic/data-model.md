# Data Model: Task Organization Feature

**Feature**: 1-task-organization
**Created**: 2026-01-01
**Status**: Complete

## Entities

### Task Entity

**Description**: Represents a todo item with attributes for title, description, priority level, categories/tags, due date, and status

**Fields**:
- `id` (int): Unique identifier for the task
- `title` (str): The main description of the task
- `description` (str, optional): Detailed description of the task
- `status` (str): Current status of the task ("pending", "completed")
- `priority` (Priority): Priority level of the task (High, Medium, Low)
- `tags` (List[str]): List of category tags associated with the task
- `due_date` (datetime, optional): Optional due date for the task
- `created_at` (datetime): Timestamp when the task was created
- `completed_at` (datetime, optional): Timestamp when the task was completed

**Validation Rules**:
- `title` must not be empty
- `status` must be one of ["pending", "completed"]
- `priority` must be a valid Priority enum value
- `tags` must be a list of non-empty strings
- `due_date` must be a valid date in the future (if provided)

### Priority Enum

**Description**: Represents the importance level of a task

**Values**:
- `HIGH` ("high"): High priority task
- `MEDIUM` ("medium"): Medium priority task
- `LOW` ("low"): Low priority task

**Ordering**: HIGH > MEDIUM > LOW

### FilterCriteria

**Description**: Represents search criteria that can be applied to task lists

**Fields**:
- `status` (str, optional): Filter by task status
- `priority` (Priority, optional): Filter by task priority
- `tags` (List[str], optional): Filter by specific tags
- `search_term` (str, optional): Search term for substring matching
- `due_date` (datetime, optional): Filter by specific due date

### SortCriteria

**Description**: Represents sorting options for task lists

**Values**:
- `DATE` ("date"): Sort by due date (ascending)
- `PRIORITY` ("priority"): Sort by priority (High > Medium > Low)
- `ALPHA` ("alpha"): Sort alphabetically by title

## Relationships

### Task to Tags
- One Task can have many Tags (one-to-many relationship)
- Tags are stored as a list within each Task object

## State Transitions

### Task Status Transitions
- `pending` → `completed` (when task is marked as done)
- `completed` → `pending` (when task is marked as undone)

## Constraints

1. A task must always have a valid priority level
2. A task can have zero or more tags
3. Due date cannot be in the past for new tasks
4. Task title must be unique within the system (optional constraint)
5. Priority values are restricted to the defined enum values