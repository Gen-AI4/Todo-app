"""Unit tests for MCP tools."""

import json
import pytest
from sqlmodel import Session, SQLModel, create_engine, select
from sqlmodel.pool import StaticPool
from uuid import uuid4

from app.models import Task
from app.mcp_tools import (
    AddTaskInput,
    ListTasksInput,
    TaskIdInput,
    UpdateTaskInput,
    success_response,
    error_response,
)


@pytest.fixture(name="session")
def session_fixture():
    """Create an in-memory SQLite database session for testing."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture
def sample_task(session: Session) -> Task:
    """Create a sample task for testing."""
    task = Task(
        user_id="user-123",
        title="Test Task",
        description="Test description",
        is_completed=False,
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


# =============================================================================
# Test Helper Functions
# =============================================================================


class TestResponseHelpers:
    """Tests for JSON response helper functions."""

    def test_success_response_format(self):
        """Test success_response creates valid JSON."""
        result = success_response({"id": "123"}, "Task created")
        parsed = json.loads(result)

        assert parsed["success"] is True
        assert parsed["data"] == {"id": "123"}
        assert parsed["message"] == "Task created"

    def test_error_response_format(self):
        """Test error_response creates valid JSON."""
        result = error_response("not_found", "Task not found")
        parsed = json.loads(result)

        assert parsed["success"] is False
        assert parsed["error"] == "not_found"
        assert parsed["message"] == "Task not found"


# =============================================================================
# Test list_tasks Tool (US1)
# =============================================================================


class TestListTasks:
    """Tests for the list_tasks MCP tool."""

    def test_list_tasks_returns_user_tasks_only(self, session: Session):
        """Test that list_tasks only returns tasks for the specified user."""
        # Create tasks for two different users
        task1 = Task(user_id="user-123", title="Task 1")
        task2 = Task(user_id="user-123", title="Task 2")
        task3 = Task(user_id="user-456", title="Other user task")
        session.add_all([task1, task2, task3])
        session.commit()

        # Import and call the tool
        from app.mcp_tools import list_tasks_impl

        result = list_tasks_impl(session, "user-123")
        parsed = json.loads(result)

        assert parsed["success"] is True
        assert len(parsed["data"]["tasks"]) == 2
        for task in parsed["data"]["tasks"]:
            assert task["user_id"] == "user-123"

    def test_list_tasks_empty_for_new_user(self, session: Session):
        """Test that list_tasks returns empty list for user with no tasks."""
        from app.mcp_tools import list_tasks_impl

        result = list_tasks_impl(session, "nonexistent-user")
        parsed = json.loads(result)

        assert parsed["success"] is True
        assert parsed["data"]["tasks"] == []
        assert "0 tasks" in parsed["message"]

    def test_list_tasks_json_format(self, session: Session, sample_task: Task):
        """Test that list_tasks returns properly formatted JSON."""
        from app.mcp_tools import list_tasks_impl

        result = list_tasks_impl(session, "user-123")
        parsed = json.loads(result)

        assert "success" in parsed
        assert "data" in parsed
        assert "message" in parsed
        assert "tasks" in parsed["data"]

        task = parsed["data"]["tasks"][0]
        assert "id" in task
        assert "title" in task
        assert "description" in task
        assert "status" in task


# =============================================================================
# Test add_task Tool (US2)
# =============================================================================


class TestAddTask:
    """Tests for the add_task MCP tool."""

    def test_add_task_success(self, session: Session):
        """Test successful task creation."""
        from app.mcp_tools import add_task_impl

        result = add_task_impl(session, "user-123", "New Task", None)
        parsed = json.loads(result)

        assert parsed["success"] is True
        assert "id" in parsed["data"]
        assert parsed["data"]["title"] == "New Task"

        # Verify task exists in database
        statement = select(Task).where(Task.user_id == "user-123")
        tasks = session.exec(statement).all()
        assert len(tasks) == 1
        assert tasks[0].title == "New Task"

    def test_add_task_with_description(self, session: Session):
        """Test task creation with description."""
        from app.mcp_tools import add_task_impl

        result = add_task_impl(session, "user-123", "Task Title", "Task Description")
        parsed = json.loads(result)

        assert parsed["success"] is True
        assert parsed["data"]["description"] == "Task Description"

    def test_add_task_empty_title_fails(self, session: Session):
        """Test that empty title returns validation error."""
        from app.mcp_tools import add_task_impl

        result = add_task_impl(session, "user-123", "", None)
        parsed = json.loads(result)

        assert parsed["success"] is False
        assert parsed["error"] == "validation_error"

    def test_add_task_json_format(self, session: Session):
        """Test that add_task returns properly formatted JSON."""
        from app.mcp_tools import add_task_impl

        result = add_task_impl(session, "user-123", "Test Task", None)
        parsed = json.loads(result)

        assert "success" in parsed
        assert "data" in parsed
        assert "message" in parsed


# =============================================================================
# Test complete_task Tool (US3)
# =============================================================================


class TestCompleteTask:
    """Tests for the complete_task MCP tool."""

    def test_complete_task_success(self, session: Session, sample_task: Task):
        """Test successfully marking a task as completed."""
        from app.mcp_tools import complete_task_impl

        result = complete_task_impl(session, "user-123", str(sample_task.id))
        parsed = json.loads(result)

        assert parsed["success"] is True

        # Verify task is completed in database
        session.refresh(sample_task)
        assert sample_task.is_completed is True

    def test_complete_task_not_found(self, session: Session):
        """Test error when task doesn't exist."""
        from app.mcp_tools import complete_task_impl

        fake_id = str(uuid4())
        result = complete_task_impl(session, "user-123", fake_id)
        parsed = json.loads(result)

        assert parsed["success"] is False
        assert parsed["error"] == "not_found"

    def test_complete_task_wrong_user(self, session: Session, sample_task: Task):
        """Test error when user doesn't own the task."""
        from app.mcp_tools import complete_task_impl

        result = complete_task_impl(session, "wrong-user", str(sample_task.id))
        parsed = json.loads(result)

        assert parsed["success"] is False
        assert parsed["error"] == "not_found"

    def test_complete_task_json_format(self, session: Session, sample_task: Task):
        """Test that complete_task returns properly formatted JSON."""
        from app.mcp_tools import complete_task_impl

        result = complete_task_impl(session, "user-123", str(sample_task.id))
        parsed = json.loads(result)

        assert "success" in parsed
        assert "data" in parsed
        assert "message" in parsed


# =============================================================================
# Test update_task Tool (US4)
# =============================================================================


class TestUpdateTask:
    """Tests for the update_task MCP tool."""

    def test_update_task_title(self, session: Session, sample_task: Task):
        """Test updating task title."""
        from app.mcp_tools import update_task_impl

        result = update_task_impl(
            session, "user-123", str(sample_task.id), "Updated Title", None
        )
        parsed = json.loads(result)

        assert parsed["success"] is True

        session.refresh(sample_task)
        assert sample_task.title == "Updated Title"

    def test_update_task_description_only(self, session: Session, sample_task: Task):
        """Test updating only description (title unchanged)."""
        from app.mcp_tools import update_task_impl

        original_title = sample_task.title
        result = update_task_impl(
            session, "user-123", str(sample_task.id), None, "New Description"
        )
        parsed = json.loads(result)

        assert parsed["success"] is True

        session.refresh(sample_task)
        assert sample_task.title == original_title
        assert sample_task.description == "New Description"

    def test_update_task_not_found(self, session: Session):
        """Test error when task doesn't exist."""
        from app.mcp_tools import update_task_impl

        fake_id = str(uuid4())
        result = update_task_impl(session, "user-123", fake_id, "Title", None)
        parsed = json.loads(result)

        assert parsed["success"] is False
        assert parsed["error"] == "not_found"

    def test_update_task_wrong_user(self, session: Session, sample_task: Task):
        """Test error when user doesn't own the task."""
        from app.mcp_tools import update_task_impl

        result = update_task_impl(
            session, "wrong-user", str(sample_task.id), "Title", None
        )
        parsed = json.loads(result)

        assert parsed["success"] is False
        assert parsed["error"] == "not_found"

    def test_update_task_json_format(self, session: Session, sample_task: Task):
        """Test that update_task returns properly formatted JSON."""
        from app.mcp_tools import update_task_impl

        result = update_task_impl(
            session, "user-123", str(sample_task.id), "Title", None
        )
        parsed = json.loads(result)

        assert "success" in parsed
        assert "data" in parsed
        assert "message" in parsed


# =============================================================================
# Test delete_task Tool (US5)
# =============================================================================


class TestDeleteTask:
    """Tests for the delete_task MCP tool."""

    def test_delete_task_success(self, session: Session, sample_task: Task):
        """Test successfully deleting a task."""
        from app.mcp_tools import delete_task_impl

        task_id = str(sample_task.id)
        result = delete_task_impl(session, "user-123", task_id)
        parsed = json.loads(result)

        assert parsed["success"] is True

        # Verify task is deleted from database
        statement = select(Task).where(Task.id == sample_task.id)
        deleted_task = session.exec(statement).first()
        assert deleted_task is None

    def test_delete_task_not_found(self, session: Session):
        """Test error when task doesn't exist."""
        from app.mcp_tools import delete_task_impl

        fake_id = str(uuid4())
        result = delete_task_impl(session, "user-123", fake_id)
        parsed = json.loads(result)

        assert parsed["success"] is False
        assert parsed["error"] == "not_found"

    def test_delete_task_wrong_user(self, session: Session, sample_task: Task):
        """Test error when user doesn't own the task."""
        from app.mcp_tools import delete_task_impl

        result = delete_task_impl(session, "wrong-user", str(sample_task.id))
        parsed = json.loads(result)

        assert parsed["success"] is False
        assert parsed["error"] == "not_found"

    def test_delete_task_json_format(self, session: Session, sample_task: Task):
        """Test that delete_task returns properly formatted JSON."""
        from app.mcp_tools import delete_task_impl

        result = delete_task_impl(session, "user-123", str(sample_task.id))
        parsed = json.loads(result)

        assert "success" in parsed
        assert "data" in parsed
        assert "message" in parsed
