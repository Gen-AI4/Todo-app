# Data Model: Todo In-Memory Python Console App

## Entity: Task

### Fields
- **id**: `int` - Unique identifier for the task (auto-incrementing integer)
- **description**: `str` - Text content describing the task
- **completed**: `bool` - Boolean indicating completion status (default: False)

### Relationships
- Belongs to a single TodoList (collection of tasks)

### Validation Rules
- `id` must be a positive integer
- `description` must not be empty or consist only of whitespace
- `completed` must be a boolean value

### State Transitions
- `incomplete` → `completed`: When user marks task as complete
- `completed` → `incomplete`: When user marks task as incomplete (optional functionality)

## Entity: TodoList

### Fields
- **tasks**: `List[Task]` - Collection of Task objects
- **next_id**: `int` - Counter for generating unique task IDs (starts at 1)

### Relationships
- Contains multiple Task entities
- Singleton instance for this console application

### Operations
- Add a new Task to the list
- Retrieve a Task by ID
- Update a Task's properties
- Delete a Task from the list
- List all Tasks
- Validate ID uniqueness before assignment

### Validation Rules
- Task IDs must be unique within the list
- Task descriptions must meet minimum length requirements
- Access to non-existent Task IDs must raise appropriate errors