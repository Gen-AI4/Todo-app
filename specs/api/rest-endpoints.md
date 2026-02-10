# REST API Endpoints Specification

**Project**: hackathon-todo
**Phase**: II - Full-Stack Web Application
**Created**: 2026-01-19
**Status**: Active

## Security Requirements

All endpoints require JWT authentication unless explicitly noted otherwise. The authentication mechanism follows these rules:

- **Token Format**: Bearer token in Authorization header: `Authorization: Bearer <jwt_token>`
- **Token Source**: Issued by Better Auth frontend integration
- **Verification**: Stateless verification using shared BETTER_AUTH_SECRET
- **User Extraction**: User ID extracted from JWT claims for data isolation
- **Access Control**: All operations restricted to authenticated user's data only

## Base URL
`/api/v1` (version may change in future releases)

## Endpoint Definitions

### 1. List User's Tasks
- **Method**: GET
- **Endpoint**: `/api/tasks`
- **Authentication Required**: Yes (JWT)
- **Description**: Retrieve all tasks belonging to the authenticated user
- **Request Headers**:
  - `Authorization: Bearer <jwt_token>`
- **Query Parameters**:
  - `completed` (optional): Filter by completion status (true/false)
  - `limit` (optional): Limit number of results
  - `offset` (optional): Offset for pagination
- **Response Codes**:
  - `200 OK`: Successfully retrieved tasks
  - `401 Unauthorized`: Invalid or missing JWT token
- **Response Body** (200):
```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Sample task",
      "description": "Detailed description of the task",
      "completed": false,
      "created_at": "2026-01-19T10:00:00Z",
      "updated_at": "2026-01-19T10:00:00Z",
      "due_date": "2026-01-20T12:00:00Z"
    }
  ],
  "total_count": 1
}
```

### 2. Create Task
- **Method**: POST
- **Endpoint**: `/api/tasks`
- **Authentication Required**: Yes (JWT)
- **Description**: Create a new task for the authenticated user
- **Request Headers**:
  - `Authorization: Bearer <jwt_token>`
- **Request Body**:
```json
{
  "title": "New task title",
  "description": "Detailed description of the task (optional)",
  "due_date": "2026-01-20T12:00:00Z (optional)"
}
```
- **Validation**:
  - Title is required and must not exceed 255 characters
  - Description, if provided, must not exceed 10000 characters
  - Due date, if provided, must be a valid datetime
- **Response Codes**:
  - `201 Created`: Task successfully created
  - `400 Bad Request`: Invalid request data
  - `401 Unauthorized`: Invalid or missing JWT token
- **Response Body** (201):
```json
{
  "id": 1,
  "title": "New task title",
  "description": "Detailed description of the task",
  "completed": false,
  "created_at": "2026-01-19T10:00:00Z",
  "updated_at": "2026-01-19T10:00:00Z",
  "due_date": "2026-01-20T12:00:00Z"
}
```

### 3. Get Task Details
- **Method**: GET
- **Endpoint**: `/api/tasks/{id}`
- **Authentication Required**: Yes (JWT)
- **Description**: Retrieve details of a specific task owned by the authenticated user
- **Path Parameter**:
  - `id` (required): Task ID
- **Request Headers**:
  - `Authorization: Bearer <jwt_token>`
- **Response Codes**:
  - `200 OK`: Task successfully retrieved
  - `401 Unauthorized`: Invalid or missing JWT token
  - `403 Forbidden`: User does not own the requested task
  - `404 Not Found`: Task does not exist
- **Response Body** (200):
```json
{
  "id": 1,
  "title": "Sample task",
  "description": "Detailed description of the task",
  "completed": false,
  "created_at": "2026-01-19T10:00:00Z",
  "updated_at": "2026-01-19T10:00:00Z",
  "due_date": "2026-01-20T12:00:00Z"
}
```

### 4. Update Task
- **Method**: PUT
- **Endpoint**: `/api/tasks/{id}`
- **Authentication Required**: Yes (JWT)
- **Description**: Update details of a specific task owned by the authenticated user
- **Path Parameter**:
  - `id` (required): Task ID
- **Request Headers**:
  - `Authorization: Bearer <jwt_token>`
- **Request Body**:
```json
{
  "title": "Updated task title",
  "description": "Updated description of the task",
  "due_date": "2026-01-20T12:00:00Z",
  "completed": false
}
```
- **Validation**:
  - At least one field must be provided for update
  - Title must not exceed 255 characters if provided
  - Description, if provided, must not exceed 10000 characters
  - Due date, if provided, must be a valid datetime
- **Response Codes**:
  - `200 OK`: Task successfully updated
  - `400 Bad Request`: Invalid request data
  - `401 Unauthorized`: Invalid or missing JWT token
  - `403 Forbidden`: User does not own the requested task
  - `404 Not Found`: Task does not exist
- **Response Body** (200):
```json
{
  "id": 1,
  "title": "Updated task title",
  "description": "Updated description of the task",
  "completed": false,
  "created_at": "2026-01-19T10:00:00Z",
  "updated_at": "2026-01-19T11:00:00Z",
  "due_date": "2026-01-20T12:00:00Z"
}
```

### 5. Delete Task
- **Method**: DELETE
- **Endpoint**: `/api/tasks/{id}`
- **Authentication Required**: Yes (JWT)
- **Description**: Delete a specific task owned by the authenticated user
- **Path Parameter**:
  - `id` (required): Task ID
- **Request Headers**:
  - `Authorization: Bearer <jwt_token>`
- **Response Codes**:
  - `204 No Content`: Task successfully deleted
  - `401 Unauthorized`: Invalid or missing JWT token
  - `403 Forbidden`: User does not own the requested task
  - `404 Not Found`: Task does not exist
- **Response Body**: Empty

### 6. Toggle Task Completion
- **Method**: PATCH
- **Endpoint**: `/api/tasks/{id}/complete`
- **Authentication Required**: Yes (JWT)
- **Description**: Toggle the completion status of a specific task owned by the authenticated user
- **Path Parameter**:
  - `id` (required): Task ID
- **Request Headers**:
  - `Authorization: Bearer <jwt_token>`
- **Request Body**: Empty or with optional update to completion status
```json
{
  "completed": true
}
```
- **Response Codes**:
  - `200 OK`: Task completion status successfully toggled
  - `400 Bad Request`: Invalid request data
  - `401 Unauthorized`: Invalid or missing JWT token
  - `403 Forbidden`: User does not own the requested task
  - `404 Not Found`: Task does not exist
- **Response Body** (200):
```json
{
  "id": 1,
  "title": "Sample task",
  "description": "Detailed description of the task",
  "completed": true,
  "created_at": "2026-01-19T10:00:00Z",
  "updated_at": "2026-01-19T11:30:00Z",
  "due_date": "2026-01-20T12:00:00Z"
}
```

## Common Error Responses

### 401 Unauthorized
```json
{
  "error": "Unauthorized",
  "message": "Invalid or missing authentication token"
}
```

### 403 Forbidden
```json
{
  "error": "Forbidden",
  "message": "You do not have permission to access this resource"
}
```

### 404 Not Found
```json
{
  "error": "Not Found",
  "message": "The requested resource was not found"
}
```

### 400 Bad Request
```json
{
  "error": "Bad Request",
  "message": "The request data is invalid",
  "details": {
    "field_name": ["Validation error message"]
  }
}
```

## Authentication Flow

1. User authenticates through Better Auth frontend components
2. Better Auth issues JWT token
3. Frontend stores token securely
4. For each API request, frontend attaches `Authorization: Bearer <token>` header
5. Backend verifies JWT signature using BETTER_AUTH_SECRET
6. Backend extracts user_id from JWT claims
7. Backend filters all database operations by user_id to ensure data isolation