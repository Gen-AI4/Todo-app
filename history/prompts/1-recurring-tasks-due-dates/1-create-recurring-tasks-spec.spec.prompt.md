---
id: 1
title: "Create Recurring Tasks Spec"
stage: "spec"
date_iso: "2026-01-01"
surface: "agent"
model: "claude-opus-4-5-20251101"
feature: "recurring-tasks-due-dates"
branch: "1-recurring-tasks-due-dates"
user: "user"
command: "sp.specify"
labels: ["spec", "recurring-tasks", "due-dates", "cli"]
links:
  spec: "specs/1-recurring-tasks-due-dates/spec.md"
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - specs/1-recurring-tasks-due-dates/spec.md
  - specs/1-recurring-tasks-due-dates/checklists/requirements.md
tests_yaml: |
  - spec validation
  - requirement completeness check
prompt_text: |
  Context: I am developing a CLI-based To-Do app and am currently in the "Advanced Phase" (Recurring Tasks & Due Dates). I need to lock down the technical specifications before implementation to avoid complexity creep.

  Objective: Generate a detailed technical specification (sp.specify) that defines exactly how the system handles time, recurrence, and user input.

  Topics to Specify:

  Date/Time Handling:

  What is the standard date format for storage (e.g., ISO 8601, UTC)?

  How will the CLI parse user inputs like "next Friday" or "tomorrow"? (Library vs. Custom Regex).

  Timezone strategy: Do we store in UTC and display in Local, or store Local?

  Recurrence Logic:

  Trigger Event: When is the next task created? (e.g., Immediately upon creation of the parent? Or only when the parent is marked 'Done'?)

  Calculation: How do we calculate "Weekly"? Is it 7 days from the due date or 7 days from the completion date? (This is a crucial UX decision).

  Storage: Do recurring tasks get a special flag or a "frequency" field (e.g., freq: "weekly")?

  Notification Strategy (CLI Context):

  Since a CLI isn't always running, define the "Active Check" mechanism.

  Specification for a notify command that can be added to .bashrc or .zshrc to show pending tasks on terminal startup.

  (Optional) Specification for integration with OS-level notifiers (notify-send, AppleScript).

  Output Format:

  Produce a structured list of Decisions and Rules.

  Use "Must", "Should", and "Could" terminology (MoSCoW method).

  Include a brief "Data Schema Changes" section outlining the exact JSON/Struct fields needed.
response_text: |
  Created comprehensive specification for recurring tasks and due dates in CLI To-Do app. The specification includes:

  - Date/Time Handling: All dates stored in ISO 8601 format (UTC) with local timezone display
  - Natural Language Parsing: Support for inputs like "tomorrow", "next Friday" using date parsing library
  - Recurrence Logic: New instances created only when parent task is marked 'Done', with intervals calculated from completion date
  - Notification Strategy: 'notify' command for terminal startup integration and OS-level notifications
  - Data Schema: Defined Task, RecurrencePattern, and Notification entities

  The spec includes user scenarios, functional requirements with MoSCoW priorities, and measurable success criteria.
outcome: "Specification successfully created with all requirements defined"
evaluation: "All requested topics covered with clear technical decisions and rules"
---
# Create Recurring Tasks Spec

## User Prompt
```
Context: I am developing a CLI-based To-Do app and am currently in the "Advanced Phase" (Recurring Tasks & Due Dates). I need to lock down the technical specifications before implementation to avoid complexity creep.

Objective: Generate a detailed technical specification (sp.specify) that defines exactly how the system handles time, recurrence, and user input.

Topics to Specify:

Date/Time Handling:

What is the standard date format for storage (e.g., ISO 8601, UTC)?

How will the CLI parse user inputs like "next Friday" or "tomorrow"? (Library vs. Custom Regex).

Timezone strategy: Do we store in UTC and display in Local, or store Local?

Recurrence Logic:

Trigger Event: When is the next task created? (e.g., Immediately upon creation of the parent? Or only when the parent is marked 'Done'?)

Calculation: How do we calculate "Weekly"? Is it 7 days from the due date or 7 days from the completion date? (This is a crucial UX decision).

Storage: Do recurring tasks get a special flag or a "frequency" field (e.g., freq: "weekly")?

Notification Strategy (CLI Context):

Since a CLI isn't always running, define the "Active Check" mechanism.

Specification for a notify command that can be added to .bashrc or .zshrc to show pending tasks on terminal startup.

(Optional) Specification for integration with OS-level notifiers (notify-send, AppleScript).

Output Format:

Produce a structured list of Decisions and Rules.

Use "Must", "Should", and "Could" terminology (MoSCoW method).

Include a brief "Data Schema Changes" section outlining the exact JSON/Struct fields needed.
```

## Assistant Response
Created comprehensive specification for recurring tasks and due dates in CLI To-Do app. The specification includes:

- Date/Time Handling: All dates stored in ISO 8601 format (UTC) with local timezone display
- Natural Language Parsing: Support for inputs like "tomorrow", "next Friday" using date parsing library
- Recurrence Logic: New instances created only when parent task is marked 'Done', with intervals calculated from completion date
- Notification Strategy: 'notify' command for terminal startup integration and OS-level notifications
- Data Schema: Defined Task, RecurrencePattern, and Notification entities

The spec includes user scenarios, functional requirements with MoSCoW priorities, and measurable success criteria.