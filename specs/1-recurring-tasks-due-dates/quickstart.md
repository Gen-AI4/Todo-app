# Quickstart Guide: CLI To-Do App - Recurring Tasks & Due Dates

## Setup

1. Ensure you have Python 3.11+ installed
2. Install required dependencies:
   ```bash
   pip install python-dateutil colorama
   ```

## Basic Usage

### Adding Tasks with Due Dates
```bash
# Add a task with a due date using natural language
todo add "Buy groceries --due tomorrow"
todo add "Team meeting --due next Friday"
todo add "Pay rent --due 2024-02-01"
```

### Adding Recurring Tasks
```bash
# Add a recurring task
todo add "Weekly team meeting --recur weekly"
todo add "Daily workout --recur daily"
todo add "Monthly report --recur monthly"
```

### Listing Tasks
```bash
# List all tasks with due date indicators
todo list

# Tasks due soon will be highlighted with color coding:
# - Red: Overdue tasks
# - Yellow: Due today
# - Orange: Due within 24 hours
# - Green: Due within 7 days
```

### Completing Tasks
```bash
# Complete a task
todo complete 1

# If the task is recurring, a new instance will be automatically created
# based on the recurrence pattern
```

## Notification Setup

### Passive Notifications
To see pending tasks on terminal startup, add this to your `.bashrc` or `.zshrc`:
```bash
# Add to your shell config file
todo notify
```

This will show a summary of due tasks each time you open a new terminal session.

### Active Notifications (Optional)
For desktop notifications, the system will attempt to use:
- `notify-send` on Linux
- `osascript` on macOS
- `powershell` on Windows

## Advanced Features

### Natural Language Examples
```bash
todo add "Meeting --due tomorrow at 3pm"
todo add "Call mom --due next Thursday"
todo add "Dentist appointment --due in 2 days"
todo add "Project deadline --due January 15th"
```

### Recurrence Patterns
- `--recur daily`: Every day
- `--recur weekly`: Every week
- `--recur monthly`: Every month
- `--recur yearly`: Every year

## Troubleshooting

### Date Parsing Issues
If natural language parsing fails, use ISO 8601 format:
```bash
todo add "Task --due 2024-01-15T14:30:00"
```

### Notification Not Working
- On Linux: Ensure `libnotify` is installed (`sudo apt-get install libnotify-bin`)
- On macOS: Notification system should work by default
- On Windows: Ensure PowerShell is available