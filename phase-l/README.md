# Todo In-Memory Python Console App

A command-line interface (CLI) todo application using Python 3.13+ with in-memory data structures. The application provides five core functions: Add, View, Update, Delete, and Mark Complete tasks.

## Features

- Add new todo tasks
- View all tasks with completion status
- Update task descriptions
- Mark tasks as complete/incomplete
- Delete tasks
- Error handling for invalid user inputs

## Prerequisites

- Python 3.13+
- `uv` package manager

## Setup

1. Clone the repository
2. Navigate to the project directory
3. Run `uv sync` to install dependencies
4. Run `uv run python -m src.cli.main` to start the application

## Usage

Once the application starts, you'll see a menu with the following options:
1. Add a new task
2. View all tasks
3. Update a task
4. Mark task as complete/incomplete
5. Delete a task
6. Exit

Follow the on-screen prompts to interact with the application. The application maintains state in-memory during the session.

## Development

- Source code is located in the `src/` directory
- Models are in `src/models/`
- Business logic is in `src/services/`
- CLI interface is in `src/cli/`
- Tests are in the `tests/` directory

Run tests with: `uv run pytest`

## Project Structure

```
todo-app/
├── src/
│   ├── models/
│   │   └── task.py
│   ├── services/
│   │   └── todo_service.py
│   └── cli/
│       └── main.py
├── tests/
│   ├── unit/
│   └── integration/
├── pyproject.toml
└── README.md
```