---
id: 1
title: Kernel Todo App Spec
stage: spec
date: 2025-12-27
surface: agent
model: claude-opus-4-5-20251101
feature: kernel-todo-app
branch: 001-kernel-todo-app
user: user
command: sp.specify
labels: [specification, todo, console-app, kernel]
links:
  spec: specs/001-kernel-todo-app/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/001-kernel-todo-app/spec.md
 - specs/001-kernel-todo-app/checklists/requirements.md
tests:
 - none
---

## Prompt

```text
# Specification: Phase I - The Kernel
**Project:** The Evolution of Todo
**Phase:** I (In-Memory Python Console App)
**Reference:** `sp.constitution` (Section 2: Phase I)
**Language:** Python 3.10+

---

## 1. Architectural Overview
This phase requires a single-file Python application (`todo.py`) that runs in the terminal.
* **State Management:** An in-memory list of dictionaries or objects. Data is lost when the app exits.
* **Interface:** A Command Line Interface (CLI) utilizing a `while` loop to accept user commands.

## 2. Data Model
Define a `Task` class or structure with the following attributes:
* `id`: Integer (Auto-incrementing, starting at 1).
* `title`: String (The content of the todo item).
* `completed`: Boolean (Default: `False`).

## 3. Functional Requirements (Basic Tier)
The application must support the following commands. Input is case-insensitive regarding the command keyword.

### 3.1 Add Task
* **Command:** `add <task title>`
* **Logic:** Create a new Task, assign an ID, add to list.
* **Output:** Print "Task added: [ID] <Title>"

### 3.2 List Tasks
* **Command:** `list`
* **Logic:** Iterate through all tasks.
* **Output:** Display format: `[x] 1. Buy Milk` or `[ ] 2. Walk Dog`.
    * Use `[x]` for completed and `[ ]` for incomplete.
    * If list is empty, print "No tasks found."

### 3.3 Complete Task
* **Command:** `complete <id>`
* **Logic:** Find task by ID. Set `completed` to `True`.
* **Output:** Print "Task <ID> marked as completed."
* **Error Handling:** If ID not found, print "Error: Task ID not found."

### 3.4 Update Task
* **Command:** `update <id> <new title>`
* **Logic:** Find task by ID. Update `title` to new value. Keep status unchanged.
* **Output:** Print "Task <ID> updated."
* **Error Handling:** If ID not found, print "Error: Task ID not found."

### 3.5 Delete Task
* **Command:** `delete <id>`
* **Logic:** Remove the task with the corresponding ID from the list.
* **Output:** Print "Task <ID> deleted."
* **Error Handling:** If ID not found, print "Error: Task ID not found."
```

## Response snapshot

Created the feature specification for Phase I - The Kernel (001-kernel-todo-app). The specification includes user scenarios, functional requirements, and success criteria for a console-based todo application. The spec details the core functionality of adding, listing, completing, updating, and deleting tasks with proper error handling. Implementation details were removed to maintain technology-agnostic focus while preserving the essential functionality requirements.

## Outcome

- ✅ Impact: High - Created complete specification for kernel todo app feature
- 🧪 Tests: none
- 📁 Files: 2 files created (spec.md, requirements.md)
- 🔁 Next prompts: Ready for planning phase (`/sp.plan`)
- 🧠 Reflection: Specification successfully created with all required sections and quality validation

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): Feature specification creation
- Next experiment (smallest change to try): Plan the implementation of the kernel todo app