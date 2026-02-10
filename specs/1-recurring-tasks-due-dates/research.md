# Research: CLI To-Do App - Recurring Tasks & Due Dates

## Decision: Date Storage Format
**Rationale**: ISO 8601 format provides universal compatibility and proper timezone handling
**Alternatives considered**: Unix timestamps, custom formats, local date strings
**Choice**: Store all dates in ISO 8601 format (UTC) to ensure consistency across timezones

## Decision: Natural Language Date Parsing
**Rationale**: dateutil.parser is a well-established library with good natural language support
**Alternatives considered**: Custom regex implementation, other parsing libraries
**Choice**: Use python-dateutil library for parsing natural language inputs like "tomorrow", "next Friday"

## Decision: Recurrence Strategy
**Rationale**: Lazy generation (triggered when task is completed) is simpler and more reliable than background cron jobs
**Alternatives considered**: Cron-based generation, background daemon processes
**Choice**: Implement lazy generation where new instances are created only when parent task is marked 'Done'

## Decision: Timezone Handling
**Rationale**: Store in UTC for consistency, display in local timezone for user experience
**Alternatives considered**: Store in local timezone, convert at runtime
**Choice**: Store all dates in UTC, convert to local timezone for display only

## Decision: Notification Mechanism
**Rationale**: CLI environment limitations require passive notification system
**Alternatives considered**: Background notification service, email notifications
**Choice**: Implement passive notifications via shell startup integration and optional OS-level notifications

## Decision: Color Coding for Urgency
**Rationale**: Visual indicators improve user experience in CLI environment
**Alternatives considered**: No visual indicators, only text-based warnings
**Choice**: Use colorama library for terminal color coding based on due date proximity