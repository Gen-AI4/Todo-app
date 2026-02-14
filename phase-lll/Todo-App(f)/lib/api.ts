/**
 * Chat API helper with JWT injection.
 *
 * Sends messages to the FastAPI backend chat endpoint
 * and returns the agent's response.
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface ChatApiResponse {
  response: string;
  conversation_id: string;
}

/**
 * Send a chat message to the backend agent endpoint.
 *
 * @param message - The user's message text
 * @param conversationId - Optional conversation ID to continue an existing conversation
 * @param token - JWT token for authentication
 * @returns The agent's response and conversation ID
 */
export interface TaskItem {
  id: string;
  user_id: string;
  title: string;
  description: string | null;
  is_completed: boolean;
  created_at: string;
  updated_at: string;
}

export async function fetchTasks(token: string): Promise<TaskItem[]> {
  const res = await fetch(`${API_URL}/api/tasks`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error(`Failed to fetch tasks: ${res.status}`);
  return res.json();
}

export async function sendChatMessage(
  message: string,
  conversationId: string | null,
  token: string
): Promise<ChatApiResponse> {
  const res = await fetch(`${API_URL}/api/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({
      message,
      conversation_id: conversationId,
    }),
  });

  if (!res.ok) {
    const errorText = await res.text().catch(() => "Unknown error");
    throw new Error(`Chat request failed (${res.status}): ${errorText}`);
  }

  return res.json();
}

export async function toggleTaskComplete(
  taskId: string,
  isCompleted: boolean,
  token: string
): Promise<TaskItem> {
  const res = await fetch(`${API_URL}/api/tasks/${taskId}`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ is_completed: !isCompleted }),
  });
  if (!res.ok) throw new Error(`Failed to update task: ${res.status}`);
  return res.json();
}

export async function deleteTask(taskId: string, token: string): Promise<void> {
  const res = await fetch(`${API_URL}/api/tasks/${taskId}`, {
    method: "DELETE",
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error(`Failed to delete task: ${res.status}`);
}

export async function createTask(
  title: string,
  description: string | null,
  token: string
): Promise<TaskItem> {
  const res = await fetch(`${API_URL}/api/tasks`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ title, description }),
  });
  if (!res.ok) throw new Error(`Failed to create task: ${res.status}`);
  return res.json();
}

export async function updateTask(
  taskId: string,
  title: string,
  description: string | null,
  token: string
): Promise<TaskItem> {
  const res = await fetch(`${API_URL}/api/tasks/${taskId}`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ title, description }),
  });
  if (!res.ok) throw new Error(`Failed to update task: ${res.status}`);
  return res.json();
}
