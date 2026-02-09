"""Authentication tests for the Todo App API.

Tests JWT token verification and data isolation.
"""

import os
from datetime import datetime, timedelta, timezone

import jwt
import pytest
from fastapi.testclient import TestClient

# Set test secret before importing app
os.environ["BETTER_AUTH_SECRET"] = "test-secret-key-for-testing-min-32-chars"
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

from app.main import app  # noqa: E402


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


@pytest.fixture
def secret():
    """Get the test secret."""
    return os.environ["BETTER_AUTH_SECRET"]


def create_test_token(user_id: str, secret: str, expired: bool = False) -> str:
    """Create a test JWT token."""
    now = datetime.now(timezone.utc)
    if expired:
        exp = now - timedelta(hours=1)  # Already expired
    else:
        exp = now + timedelta(hours=1)  # Valid for 1 hour

    payload = {
        "sub": user_id,
        "iat": now,
        "exp": exp,
        "user": {
            "id": user_id,
            "email": f"{user_id}@test.com",
        },
    }
    return jwt.encode(payload, secret, algorithm="HS256")


# =============================================================================
# T052: Test request without token returns 401
# =============================================================================


def test_request_without_token_returns_401(client):
    """Request without Authorization header should return 401."""
    response = client.get("/api/tasks")
    assert response.status_code == 401


# =============================================================================
# T053: Test request with invalid token returns 401
# =============================================================================


def test_request_with_invalid_token_returns_401(client):
    """Request with invalid token should return 401."""
    response = client.get(
        "/api/tasks",
        headers={"Authorization": "Bearer invalid_token_here"},
    )
    assert response.status_code == 401


def test_request_with_wrong_secret_returns_401(client, secret):
    """Token signed with wrong secret should return 401."""
    # Create token with different secret
    token = create_test_token("user1", "wrong-secret-key-definitely-not-the-same")
    response = client.get(
        "/api/tasks",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 401


# =============================================================================
# T054: Test request with expired token returns 401
# =============================================================================


def test_request_with_expired_token_returns_401(client, secret):
    """Request with expired token should return 401."""
    token = create_test_token("user1", secret, expired=True)
    response = client.get(
        "/api/tasks",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 401
    assert "expired" in response.json()["detail"].lower()


# =============================================================================
# T055: Test request with valid token returns 200
# =============================================================================


def test_request_with_valid_token_returns_200(client, secret):
    """Request with valid token should succeed."""
    token = create_test_token("user1", secret)
    response = client.get(
        "/api/tasks",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_task_with_valid_token(client, secret):
    """Creating a task with valid token should succeed."""
    token = create_test_token("user1", secret)
    response = client.post(
        "/api/tasks",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": "Test Task"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["user_id"] == "user1"


# =============================================================================
# T056: Test User A cannot access User B's tasks
# =============================================================================


def test_user_cannot_access_other_users_tasks(client, secret):
    """User A should not see tasks created by User B."""
    # Create a task as user A
    token_a = create_test_token("user_a", secret)
    create_response = client.post(
        "/api/tasks",
        headers={"Authorization": f"Bearer {token_a}"},
        json={"title": "User A's Task"},
    )
    assert create_response.status_code == 201
    task_id = create_response.json()["id"]

    # Try to access that task as user B
    token_b = create_test_token("user_b", secret)
    get_response = client.get(
        f"/api/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token_b}"},
    )
    # User B should get 404 (task not found for them)
    assert get_response.status_code == 404


def test_user_only_sees_own_tasks(client, secret):
    """User should only see their own tasks in list."""
    # Create tasks as user A
    token_a = create_test_token("list_user_a", secret)
    for i in range(3):
        client.post(
            "/api/tasks",
            headers={"Authorization": f"Bearer {token_a}"},
            json={"title": f"User A Task {i}"},
        )

    # Create tasks as user B
    token_b = create_test_token("list_user_b", secret)
    for i in range(2):
        client.post(
            "/api/tasks",
            headers={"Authorization": f"Bearer {token_b}"},
            json={"title": f"User B Task {i}"},
        )

    # User A should only see their 3 tasks
    response_a = client.get(
        "/api/tasks",
        headers={"Authorization": f"Bearer {token_a}"},
    )
    assert response_a.status_code == 200
    tasks_a = response_a.json()
    assert all(t["user_id"] == "list_user_a" for t in tasks_a)
    assert len(tasks_a) >= 3  # At least 3 tasks

    # User B should only see their 2 tasks
    response_b = client.get(
        "/api/tasks",
        headers={"Authorization": f"Bearer {token_b}"},
    )
    assert response_b.status_code == 200
    tasks_b = response_b.json()
    assert all(t["user_id"] == "list_user_b" for t in tasks_b)
    assert len(tasks_b) >= 2  # At least 2 tasks


def test_user_cannot_delete_other_users_task(client, secret):
    """User should not be able to delete another user's task."""
    # Create task as user A
    token_a = create_test_token("delete_user_a", secret)
    create_response = client.post(
        "/api/tasks",
        headers={"Authorization": f"Bearer {token_a}"},
        json={"title": "User A's Protected Task"},
    )
    task_id = create_response.json()["id"]

    # Try to delete as user B
    token_b = create_test_token("delete_user_b", secret)
    delete_response = client.delete(
        f"/api/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token_b}"},
    )
    # Should return 404 (not found for user B)
    assert delete_response.status_code == 404

    # Verify task still exists for user A
    get_response = client.get(
        f"/api/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token_a}"},
    )
    assert get_response.status_code == 200
