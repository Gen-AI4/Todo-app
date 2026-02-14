# API Contract: Tasks List (Existing Endpoint)

**Status**: Already implemented in backend (Spec 5)
**Used by**: New `TasksPanel` component

---

## GET /api/tasks

Fetches all tasks for the authenticated user.

### Request

```
GET /api/tasks
Authorization: Bearer <jwt_token>
```

### Response (200 OK)

```json
[
  {
    "id": "uuid-string",
    "user_id": "user-id-string",
    "title": "Buy milk",
    "description": null,
    "is_completed": false,
    "created_at": "2026-02-11T10:00:00Z",
    "updated_at": "2026-02-11T10:00:00Z"
  }
]
```

### Response (401 Unauthorized)

```json
{
  "detail": "Not authenticated"
}
```

### TypeScript Interface

```typescript
export interface TaskItem {
  id: string;
  user_id: string;
  title: string;
  description: string | null;
  is_completed: boolean;
  created_at: string;
  updated_at: string;
}
```

### Frontend Usage

```typescript
// In lib/api.ts
export async function fetchTasks(token: string): Promise<TaskItem[]> {
  const res = await fetch(`${API_URL}/api/tasks`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error(`Failed to fetch tasks: ${res.status}`);
  return res.json();
}
```
