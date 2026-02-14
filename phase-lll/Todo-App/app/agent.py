"""OpenRouter agent service for the Todo AI Chatbot.

Handles OpenRouter client configuration, tool definitions,
tool dispatch, and the core agent execution loop.
"""

import json
import os
from typing import Optional
from uuid import UUID

from dotenv import load_dotenv
from openai import OpenAI
from sqlmodel import Session, select

from app.mcp_tools import (
    add_task_impl,
    list_tasks_impl,
    complete_task_impl,
    delete_task_impl,
    update_task_impl,
    error_response,
)
from app.models import Conversation, Message

load_dotenv()

# =============================================================================
# OpenRouter Configuration
# =============================================================================

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_MODEL = "arcee-ai/trinity-large-preview:free"

MAX_TOOL_ITERATIONS = 5
REQUEST_TIMEOUT = 30


def get_openrouter_client() -> OpenAI:
    """Create OpenAI client configured for OpenRouter."""
    if not OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY environment variable is required")
    return OpenAI(
        api_key=OPENROUTER_API_KEY,
        base_url=OPENROUTER_BASE_URL,
        timeout=REQUEST_TIMEOUT,
        default_headers={
            "HTTP-Referer": "https://todo-ai-chatbot.app",
            "X-Title": "Todo AI Chatbot",
        },
    )


# =============================================================================
# System Prompt
# =============================================================================

SYSTEM_PROMPT = """You are a helpful task management assistant. You help users \
manage their todo list through natural language conversation.

You have access to the following tools:
- add_task: Create a new task with a title and optional description
- list_tasks: Show all tasks for the current user
- complete_task: Mark a task as completed
- delete_task: Remove a task permanently
- update_task: Update a task's title or description

When a user asks you to do something with their tasks, use the appropriate tool. \
Always confirm the action you took. If the user's request is ambiguous, ask for \
clarification.

Important: The user_id is automatically provided to all tools. You do not need \
to ask users for their ID."""


# =============================================================================
# Tool Definitions (OpenAI Function Calling Format)
# =============================================================================

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Create a new task for the user",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Task title (required)",
                    },
                    "description": {
                        "type": "string",
                        "description": "Optional task description",
                    },
                },
                "required": ["title"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "List all tasks for the current user",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "complete_task",
            "description": "Mark a task as completed by its ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "The UUID of the task to complete",
                    },
                },
                "required": ["task_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": "Permanently delete a task by its ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "The UUID of the task to delete",
                    },
                },
                "required": ["task_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "update_task",
            "description": "Update a task's title and/or description",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "The UUID of the task to update",
                    },
                    "title": {
                        "type": "string",
                        "description": "New task title (optional)",
                    },
                    "description": {
                        "type": "string",
                        "description": "New task description (optional)",
                    },
                },
                "required": ["task_id"],
            },
        },
    },
]


# =============================================================================
# Tool Dispatcher
# =============================================================================

TOOL_DISPATCH = {
    "add_task": add_task_impl,
    "list_tasks": list_tasks_impl,
    "complete_task": complete_task_impl,
    "delete_task": delete_task_impl,
    "update_task": update_task_impl,
}


def execute_tool(
    session: Session, user_id: str, tool_name: str, arguments: dict
) -> str:
    """Execute an MCP tool with server-side user_id injection.

    The user_id is never exposed to the LLM. It is injected here
    from the authenticated user context (ADR-004).
    """
    fn = TOOL_DISPATCH.get(tool_name)
    if not fn:
        return error_response("not_found", f"Unknown tool: {tool_name}")

    if tool_name == "add_task":
        return fn(
            session,
            user_id,
            arguments.get("title", ""),
            arguments.get("description"),
        )
    elif tool_name == "list_tasks":
        return fn(session, user_id)
    elif tool_name in ("complete_task", "delete_task"):
        return fn(session, user_id, arguments.get("task_id", ""))
    elif tool_name == "update_task":
        return fn(
            session,
            user_id,
            arguments.get("task_id", ""),
            arguments.get("title"),
            arguments.get("description"),
        )

    return error_response("internal_error", "Unhandled tool dispatch")


# =============================================================================
# Agent Execution Loop
# =============================================================================


def run_agent(
    session: Session,
    user_id: str,
    user_message: str,
    conversation_id: Optional[UUID] = None,
) -> tuple[str, UUID]:
    """Full agent execution flow.

    1. Fetch or create Conversation
    2. Load Message history
    3. Save user message to DB
    4. Construct payload (system prompt + history + tools)
    5. Call OpenRouter API
    6. Handle tool calls (loop until no more, max iterations)
    7. Save assistant response to DB
    8. Return (response_text, conversation_id)
    """
    # Step 1: Fetch or create Conversation
    if conversation_id:
        conversation = session.exec(
            select(Conversation).where(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id,
            )
        ).first()
        if not conversation:
            raise ValueError("Conversation not found or access denied")
    else:
        conversation = Conversation(user_id=user_id)
        session.add(conversation)
        session.commit()
        session.refresh(conversation)

    # Step 2: Load message history (last 50 for context window)
    statement = (
        select(Message)
        .where(Message.conversation_id == conversation.id)
        .order_by(Message.created_at)
        .limit(50)
    )
    history = session.exec(statement).all()

    # Step 3: Save user message to DB
    user_msg = Message(
        conversation_id=conversation.id,
        role="user",
        content=user_message,
    )
    session.add(user_msg)
    session.commit()

    # Step 4: Construct API payload
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for msg in history:
        messages.append({"role": msg.role, "content": msg.content})
    messages.append({"role": "user", "content": user_message})

    # Step 5: Call OpenRouter API
    client = get_openrouter_client()
    response = client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=messages,
        tools=TOOL_DEFINITIONS,
    )
    assistant_message = response.choices[0].message

    # Step 6: Tool-call loop (max iterations to prevent infinite cycling)
    iterations = 0
    while assistant_message.tool_calls and iterations < MAX_TOOL_ITERATIONS:
        iterations += 1

        # Add assistant message with tool calls to conversation
        messages.append(assistant_message.model_dump())

        # Execute each tool call
        for tool_call in assistant_message.tool_calls:
            try:
                args = json.loads(tool_call.function.arguments)
            except json.JSONDecodeError:
                args = {}

            result = execute_tool(
                session, user_id, tool_call.function.name, args
            )
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result,
                }
            )

        # Get next response from LLM
        response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=messages,
            tools=TOOL_DEFINITIONS,
        )
        assistant_message = response.choices[0].message

    # Step 7: Save assistant response to DB
    response_text = assistant_message.content or ""
    assistant_msg = Message(
        conversation_id=conversation.id,
        role="assistant",
        content=response_text,
    )
    session.add(assistant_msg)
    session.commit()

    # Step 8: Return
    return response_text, conversation.id
