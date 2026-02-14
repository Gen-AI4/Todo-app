"""MCP Tool implementations for task management."""

import json
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field
from sqlmodel import Session, select

from app.database import engine
from app.models import Task
from app.mcp_server import mcp


# =============================================================================
# Input Schemas
# =============================================================================


class AddTaskInput(BaseModel):
    """Input schema for add_task tool."""

    user_id: str = Field(..., description="User identifier (required)")
    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(None, max_length=1000, description="Task description")


class ListTasksInput(BaseModel):
    """Input schema for list_tasks tool."""

    user_id: str = Field(..., description="User identifier (required)")


class TaskIdInput(BaseModel):
    """Input schema for tools requiring task_id."""

    user_id: str = Field(..., description="User identifier (required)")
    task_id: str = Field(..., description="Task UUID")


class UpdateTaskInput(BaseModel):
    """Input schema for update_task tool."""

    user_id: str = Field(..., description="User identifier (required)")
    task_id: str = Field(..., description="Task UUID")
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="New task title")
    description: Optional[str] = Field(None, max_length=1000, description="New task description")


# =============================================================================
# Response Helpers
# =============================================================================


def success_response(data: dict, message: str) -> str:
    """Create a JSON success response string."""
    return json.dumps({"success": True, "data": data, "message": message})


def error_response(error_code: str, message: str) -> str:
    """Create a JSON error response string."""
    return json.dumps({"success": False, "error": error_code, "message": message})


# =============================================================================
# Database Session Helper
# =============================================================================


def get_db_session() -> Session:
    """Get a synchronous database session for MCP tool operations."""
    return Session(engine)


# =============================================================================
# Tool Implementation Functions (for testing)
# =============================================================================


def _task_to_dict(task: Task) -> dict:
    """Convert a Task model to a dictionary for JSON serialization."""
    return {
        "id": str(task.id),
        "user_id": task.user_id,
        "title": task.title,
        "description": task.description,
        "status": "completed" if task.is_completed else "pending",
        "created_at": task.created_at.isoformat(),
        "updated_at": task.updated_at.isoformat(),
    }


def list_tasks_impl(session: Session, user_id: str) -> str:
    """Implementation of list_tasks tool."""
    statement = select(Task).where(Task.user_id == user_id)
    tasks = session.exec(statement).all()

    task_list = [_task_to_dict(task) for task in tasks]
    return success_response(
        {"tasks": task_list},
        f"Found {len(task_list)} tasks for user"
    )


def add_task_impl(session: Session, user_id: str, title: str, description: Optional[str]) -> str:
    """Implementation of add_task tool."""
    # Validate title
    if not title or not title.strip():
        return error_response("validation_error", "Title cannot be empty")

    task = Task(
        user_id=user_id,
        title=title.strip(),
        description=description,
        is_completed=False,
    )
    session.add(task)
    session.commit()
    session.refresh(task)

    return success_response(
        _task_to_dict(task),
        f"Task '{task.title}' created successfully"
    )


def complete_task_impl(session: Session, user_id: str, task_id: str) -> str:
    """Implementation of complete_task tool."""
    try:
        task_uuid = UUID(task_id)
    except ValueError:
        return error_response("validation_error", "Invalid task ID format")

    statement = select(Task).where(Task.id == task_uuid, Task.user_id == user_id)
    task = session.exec(statement).first()

    if not task:
        return error_response("not_found", "Task not found or access denied")

    task.is_completed = True
    task.updated_at = datetime.now(timezone.utc)
    session.add(task)
    session.commit()
    session.refresh(task)

    return success_response(
        _task_to_dict(task),
        f"Task '{task.title}' marked as completed"
    )


def delete_task_impl(session: Session, user_id: str, task_id: str) -> str:
    """Implementation of delete_task tool."""
    try:
        task_uuid = UUID(task_id)
    except ValueError:
        return error_response("validation_error", "Invalid task ID format")

    statement = select(Task).where(Task.id == task_uuid, Task.user_id == user_id)
    task = session.exec(statement).first()

    if not task:
        return error_response("not_found", "Task not found or access denied")

    task_title = task.title
    session.delete(task)
    session.commit()

    return success_response(
        {"deleted_id": str(task_uuid)},
        f"Task '{task_title}' deleted successfully"
    )


def update_task_impl(
    session: Session,
    user_id: str,
    task_id: str,
    title: Optional[str],
    description: Optional[str]
) -> str:
    """Implementation of update_task tool."""
    try:
        task_uuid = UUID(task_id)
    except ValueError:
        return error_response("validation_error", "Invalid task ID format")

    statement = select(Task).where(Task.id == task_uuid, Task.user_id == user_id)
    task = session.exec(statement).first()

    if not task:
        return error_response("not_found", "Task not found or access denied")

    # Update only provided fields
    if title is not None:
        if not title.strip():
            return error_response("validation_error", "Title cannot be empty")
        task.title = title.strip()

    if description is not None:
        task.description = description

    task.updated_at = datetime.now(timezone.utc)
    session.add(task)
    session.commit()
    session.refresh(task)

    return success_response(
        _task_to_dict(task),
        f"Task '{task.title}' updated successfully"
    )


# =============================================================================
# MCP Tool Decorators
# =============================================================================


@mcp.tool()
def list_tasks(user_id: str) -> str:
    """
    List all tasks for a specific user.

    Args:
        user_id: The user's unique identifier

    Returns:
        JSON string with list of tasks or error message
    """
    with get_db_session() as session:
        return list_tasks_impl(session, user_id)


@mcp.tool()
def add_task(user_id: str, title: str, description: str | None = None) -> str:
    """
    Create a new task for a user.

    Args:
        user_id: The user's unique identifier
        title: Task title (required, 1-200 characters)
        description: Optional task description (max 1000 characters)

    Returns:
        JSON string with created task details or error message
    """
    with get_db_session() as session:
        return add_task_impl(session, user_id, title, description)


@mcp.tool()
def complete_task(user_id: str, task_id: str) -> str:
    """
    Mark a task as completed.

    Args:
        user_id: The user's unique identifier
        task_id: The task's UUID

    Returns:
        JSON string with updated task details or error message
    """
    with get_db_session() as session:
        return complete_task_impl(session, user_id, task_id)


@mcp.tool()
def delete_task(user_id: str, task_id: str) -> str:
    """
    Delete a task.

    Args:
        user_id: The user's unique identifier
        task_id: The task's UUID

    Returns:
        JSON string confirming deletion or error message
    """
    with get_db_session() as session:
        return delete_task_impl(session, user_id, task_id)


@mcp.tool()
def update_task(
    user_id: str,
    task_id: str,
    title: str | None = None,
    description: str | None = None
) -> str:
    """
    Update a task's title and/or description.

    Args:
        user_id: The user's unique identifier
        task_id: The task's UUID
        title: New task title (optional)
        description: New task description (optional)

    Returns:
        JSON string with updated task details or error message
    """
    with get_db_session() as session:
        return update_task_impl(session, user_id, task_id, title, description)
