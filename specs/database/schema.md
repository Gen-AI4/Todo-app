# Database Schema Specification

**Project**: hackathon-todo
**Phase**: II - Full-Stack Web Application
**Created**: 2026-01-19
**Status**: Active

## Overview

The database schema consists of two main areas:
1. **Users**: Managed by Better Auth (external to our direct control)
2. **Tasks**: Managed by our application using SQLModel

## User Management (Handled by Better Auth)

Better Auth manages the user authentication layer and provides user identities. Our application receives user_id through JWT tokens and uses this to isolate data.

### Better Auth Integration Points
- **User Registration**: Handled by Better Auth frontend components
- **Login/Session**: Managed by Better Auth
- **User Identification**: User ID extracted from JWT token for data isolation
- **User Profile**: Basic user information managed by Better Auth

## Task Entity Schema

Our application manages the Tasks entity with the following structure:

### Tasks Table

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | Integer | PRIMARY KEY, AUTO_INCREMENT | Unique identifier for each task |
| user_id | String | NOT NULL, Foreign Key Reference | ID of the user who owns this task (extracted from JWT) |
| title | String(255) | NOT NULL | Title of the task |
| description | Text | NULL | Detailed description of the task |
| completed | Boolean | DEFAULT FALSE | Whether the task is completed |
| created_at | DateTime | NOT NULL, DEFAULT NOW | Timestamp when task was created |
| updated_at | DateTime | NOT NULL, DEFAULT NOW | Timestamp when task was last updated |
| due_date | DateTime | NULL | Optional due date for the task |

### Indexes
- **Primary Index**: id (automatically created)
- **User Isolation Index**: user_id (to optimize queries filtered by user)
- **Completed Tasks Index**: completed (to optimize queries for completed/incomplete tasks)
- **Due Date Index**: due_date (to optimize queries for upcoming tasks)

### Constraints
- **Foreign Key**: user_id references the user identified in the JWT token (enforced at application level)
- **Data Isolation**: All queries MUST be filtered by user_id to prevent unauthorized access
- **Required Fields**: title is required for all tasks
- **Default Values**: completed defaults to FALSE, timestamps default to current time

## Data Access Patterns

### Mandatory User Filtering
All database queries involving tasks MUST include a WHERE clause filtering by user_id extracted from the JWT token. This is critical for maintaining user data isolation.

### Common Queries
1. **Get User's Tasks**: SELECT * FROM tasks WHERE user_id = [extracted_from_jwt]
2. **Get Specific Task**: SELECT * FROM tasks WHERE id = [task_id] AND user_id = [extracted_from_jwt]
3. **Create Task**: INSERT INTO tasks (user_id, title, ...) VALUES ([extracted_from_jwt], ...)
4. **Update Task**: UPDATE tasks SET ... WHERE id = [task_id] AND user_id = [extracted_from_jwt]
5. **Delete Task**: DELETE FROM tasks WHERE id = [task_id] AND user_id = [extracted_from_jwt]

## Security Considerations

### User Isolation Enforcement
- The application layer MUST verify that all operations are scoped to the authenticated user
- No direct access to tasks belonging to other users is permitted
- All API endpoints must validate that the requesting user owns the data being accessed
- Database-level foreign key constraints reference the user identified in the JWT

### Audit Trail
- Creation and modification timestamps are automatically maintained
- User association is maintained through the user_id field
- No deletion of user records occurs (soft deletes may be implemented if needed)

## Migration Strategy

### Initial Setup
1. Create the tasks table with the specified schema
2. Ensure proper indexing for performance
3. Implement application-level checks for user_id filtering
4. Test data isolation between users

### Future Considerations
- Additional indexes may be added based on query patterns
- Archive/soft-delete functionality may be added if needed
- Additional metadata fields may be added to tasks if required