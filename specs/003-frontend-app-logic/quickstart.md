# Quickstart Guide: Task Organization Features

**Feature**: 1-task-organization
**Created**: 2026-01-01

## Overview
This guide provides a quick introduction to the new task organization features in the Todo application. These features allow you to prioritize tasks, categorize them with tags, search through your tasks, filter them based on criteria, and sort them in various ways.

## New Features

### 1. Task Priorities
Assign priority levels (High, Medium, Low) to your tasks to indicate their importance.

**Adding a task with priority:**
```
add "Complete project proposal" --priority high
```

**List tasks with high priority:**
```
list --priority high
```

### 2. Task Tags
Add tags to categorize your tasks (e.g., work, home, personal).

**Adding a task with tags:**
```
add "Buy groceries" --tag home --tag shopping
```

**List tasks with specific tags:**
```
list --tag work
```

### 3. Search Functionality
Search for tasks containing specific keywords.

**Search for tasks:**
```
list --search "meeting"
```

### 4. Advanced Filtering
Filter tasks based on multiple criteria.

**Filter by status and priority:**
```
list --status pending --priority high
```

**Combine search and tags:**
```
list --search "report" --tag work
```

### 5. Sorting Options
Sort tasks in different ways to organize your view.

**Sort by due date:**
```
list --sort date
```

**Sort by priority (High to Low):**
```
list --sort priority
```

**Sort alphabetically:**
```
list --sort alpha
```

## Complete Examples

### Add a task with multiple attributes:
```
add "Prepare quarterly report" --priority high --tag work --due-date 2026-01-15
```

### List high priority work tasks:
```
list --priority high --tag work
```

### Search and sort results:
```
list --search "client" --sort priority
```

### Filter by multiple criteria:
```
list --status pending --priority medium --tag home
```

## Available Options

### Add Command Options:
- `--priority, -p`: Priority level (high, medium, low)
- `--tag, -t`: Category tag (can be used multiple times)
- `--due-date, -d`: Due date in YYYY-MM-DD format

### List Command Options:
- `--status`: Filter by status (pending, completed)
- `--priority`: Filter by priority (high, medium, low)
- `--tag`: Filter by tag
- `--search`: Search term for filtering
- `--sort`: Sort method (date, priority, alpha)
- `--all`: Show all tasks (including completed)

## Tips
1. Use multiple tags to categorize tasks in different contexts
2. Combine search and filter options for precise results
3. Sort by priority to focus on important tasks first
4. Use due dates to organize tasks by timeline
5. Remember that all existing commands continue to work as before