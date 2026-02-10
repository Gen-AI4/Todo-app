# Todo Service API Contract

## Overview
This contract defines the interface for the TodoService that manages in-memory todo tasks. This is an internal service contract for the console application.

## Data Types

### Task
```python
class Task:
    id: int
    description: str
    completed: bool
```

## Service Interface

### Methods

#### `add_task(description: str) -> int`
- **Purpose**: Add a new task to the todo list
- **Input**: Task description (non-empty string)
- **Output**: Unique task ID (positive integer)
- **Errors**: ValueError if description is empty

#### `get_task(task_id: int) -> Task`
- **Purpose**: Retrieve a task by its ID
- **Input**: Task ID (positive integer)
- **Output**: Task object
- **Errors**: KeyError if task ID doesn't exist

#### `get_all_tasks() -> List[Task]`
- **Purpose**: Retrieve all tasks in the list
- **Input**: None
- **Output**: List of all Task objects (empty list if no tasks)

#### `update_task(task_id: int, description: str) -> bool`
- **Purpose**: Update the description of an existing task
- **Input**: Task ID and new description
- **Output**: True if successful, False if task doesn't exist
- **Errors**: ValueError if description is empty

#### `mark_complete(task_id: int) -> bool`
- **Purpose**: Mark a task as complete
- **Input**: Task ID
- **Output**: True if successful, False if task doesn't exist

#### `mark_incomplete(task_id: int) -> bool`
- **Purpose**: Mark a task as incomplete
- **Input**: Task ID
- **Output**: True if successful, False if task doesn't exist

#### `delete_task(task_id: int) -> bool`
- **Purpose**: Remove a task from the list
- **Input**: Task ID
- **Output**: True if successful, False if task doesn't exist

#### `toggle_task_status(task_id: int) -> bool`
- **Purpose**: Toggle the completion status of a task
- **Input**: Task ID
- **Output**: True if successful, False if task doesn't exist