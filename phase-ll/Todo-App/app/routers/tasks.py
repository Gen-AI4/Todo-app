"""Task CRUD endpoints for the Todo App with JWT authentication.

All endpoints require a valid JWT token in the Authorization header.
User identity is extracted from the token, not from URL parameters.
"""

from datetime import datetime, timezone
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.auth import CurrentUser, get_current_user
from app.database import get_session
from app.models import Task, TaskCreate, TaskPatch, TaskResponse, TaskUpdate

router = APIRouter(tags=["Tasks"])


# ============================================================================
# User Story 1: Create a Task (P1)
# T025, T031, T038: Route migration + auth dependency + user isolation
# ============================================================================


@router.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    responses={
        400: {"description": "Validation error - title is required"},
        401: {"description": "Authentication required"},
        500: {"description": "Server error"},
    },
)
def create_task(
    task_data: TaskCreate,
    current_user: CurrentUser = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> Task:
    """
    Create a new task for the authenticated user.

    - **title**: Task title (required, 1-200 characters)
    - **description**: Task description (optional, max 1000 characters)
    - **is_completed**: Initial completion status (default: false)

    User ID is automatically extracted from the JWT token.
    """
    # T038: Use current_user.user_id from token instead of path parameter
    task = Task(
        title=task_data.title,
        description=task_data.description,
        is_completed=task_data.is_completed,
        user_id=current_user.user_id,
    )

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


# ============================================================================
# User Story 2: View Tasks (P1)
# T026, T027, T032, T033, T039, T040: Route migration + auth + isolation
# ============================================================================


@router.get(
    "/tasks",
    response_model=List[TaskResponse],
    summary="List all tasks for authenticated user",
    responses={
        401: {"description": "Authentication required"},
        500: {"description": "Server error"},
    },
)
def list_tasks(
    current_user: CurrentUser = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> List[Task]:
    """
    Retrieve all tasks for the authenticated user.

    Tasks are filtered by the user_id from the JWT token.
    """
    # T039: Filter by current_user.user_id from token
    statement = select(Task).where(Task.user_id == current_user.user_id)
    tasks = session.exec(statement).all()
    return list(tasks)


@router.get(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    summary="Get a specific task",
    responses={
        401: {"description": "Authentication required"},
        404: {"description": "Task not found"},
        500: {"description": "Server error"},
    },
)
def get_task(
    task_id: UUID,
    current_user: CurrentUser = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> Task:
    """
    Retrieve a specific task by ID.

    - **task_id**: Unique task identifier (UUID)

    Only returns the task if it belongs to the authenticated user.
    """
    # T040: Verify ownership with current_user.user_id
    statement = select(Task).where(
        Task.id == task_id, Task.user_id == current_user.user_id
    )
    task = session.exec(statement).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found",
        )

    return task


# ============================================================================
# User Story 3: Update a Task (P2)
# T028, T029, T034, T035, T041, T042: Route migration + auth + isolation
# ============================================================================


@router.put(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    summary="Full update of a task",
    responses={
        400: {"description": "Validation error"},
        401: {"description": "Authentication required"},
        404: {"description": "Task not found"},
        500: {"description": "Server error"},
    },
)
def update_task(
    task_id: UUID,
    task_data: TaskUpdate,
    current_user: CurrentUser = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> Task:
    """
    Fully update an existing task (all fields required).

    - **task_id**: Unique task identifier (UUID)
    - **title**: New task title (required)
    - **description**: New task description
    - **is_completed**: New completion status

    Only updates the task if it belongs to the authenticated user.
    """
    # T041: Verify ownership with current_user.user_id
    statement = select(Task).where(
        Task.id == task_id, Task.user_id == current_user.user_id
    )
    task = session.exec(statement).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found",
        )

    # Update all fields
    task.title = task_data.title
    task.description = task_data.description
    task.is_completed = task_data.is_completed
    task.updated_at = datetime.now(timezone.utc)

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


@router.patch(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    summary="Partial update of a task",
    responses={
        400: {"description": "Validation error"},
        401: {"description": "Authentication required"},
        404: {"description": "Task not found"},
        500: {"description": "Server error"},
    },
)
def patch_task(
    task_id: UUID,
    task_data: TaskPatch,
    current_user: CurrentUser = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> Task:
    """
    Partially update an existing task (only provided fields are updated).

    - **task_id**: Unique task identifier (UUID)
    - **title**: New task title (optional)
    - **description**: New task description (optional)
    - **is_completed**: New completion status (optional)

    Only updates the task if it belongs to the authenticated user.
    """
    # T042: Verify ownership with current_user.user_id
    statement = select(Task).where(
        Task.id == task_id, Task.user_id == current_user.user_id
    )
    task = session.exec(statement).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found",
        )

    # Update only provided fields
    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description
    if task_data.is_completed is not None:
        task.is_completed = task_data.is_completed

    task.updated_at = datetime.now(timezone.utc)

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


# ============================================================================
# User Story 4: Delete a Task (P2)
# T030, T036, T043: Route migration + auth + isolation
# ============================================================================


@router.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
    responses={
        401: {"description": "Authentication required"},
        404: {"description": "Task not found"},
        500: {"description": "Server error"},
    },
)
def delete_task(
    task_id: UUID,
    current_user: CurrentUser = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> None:
    """
    Delete a specific task.

    - **task_id**: Unique task identifier (UUID)

    Only deletes the task if it belongs to the authenticated user.
    """
    # T043: Verify ownership with current_user.user_id
    statement = select(Task).where(
        Task.id == task_id, Task.user_id == current_user.user_id
    )
    task = session.exec(statement).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found",
        )

    session.delete(task)
    session.commit()
