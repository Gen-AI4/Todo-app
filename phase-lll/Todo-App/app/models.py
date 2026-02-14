"""Task and User models and schemas for the Todo App."""

from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4

from pydantic import field_validator, EmailStr
from sqlmodel import Field, SQLModel


# =============================================================================
# User Models
# =============================================================================


class User(SQLModel, table=True):
    """User database model."""

    id: UUID = Field(default_factory=uuid4, primary_key=True, description="Unique user identifier")
    email: str = Field(unique=True, index=True, description="User email address")
    password_hash: str = Field(description="Hashed password")
    name: Optional[str] = Field(default=None, max_length=200, description="User display name")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Account creation timestamp (UTC)",
    )


class UserCreate(SQLModel):
    """Schema for user registration."""

    email: str = Field(description="User email address")
    password: str = Field(min_length=8, description="User password (min 8 chars)")
    name: Optional[str] = Field(default=None, max_length=200, description="User display name")


class UserLogin(SQLModel):
    """Schema for user login."""

    email: str = Field(description="User email address")
    password: str = Field(description="User password")


class UserResponse(SQLModel):
    """Schema for user API responses."""

    id: UUID
    email: str
    name: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(SQLModel):
    """Schema for authentication token response."""

    token: str
    user: UserResponse


# =============================================================================
# Task Models
# =============================================================================


class TaskBase(SQLModel):
    """Base model with shared Task fields."""

    title: str = Field(max_length=200, description="Task title (required, max 200 chars)")
    description: Optional[str] = Field(
        default=None, max_length=1000, description="Task description (optional, max 1000 chars)"
    )
    is_completed: bool = Field(default=False, description="Task completion status")


class Task(TaskBase, table=True):
    """Task database model."""

    id: UUID = Field(default_factory=uuid4, primary_key=True, description="Unique task identifier")
    user_id: str = Field(index=True, description="Owner's user identifier")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Task creation timestamp (UTC)",
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Last modification timestamp (UTC)",
    )


class TaskCreate(SQLModel):
    """Schema for creating a new task."""

    title: str = Field(min_length=1, max_length=200, description="Task title (required, 1-200 chars)")
    description: Optional[str] = Field(
        default=None, max_length=1000, description="Task description (optional)"
    )
    is_completed: bool = Field(default=False, description="Initial completion status")

    @field_validator("title")
    @classmethod
    def title_must_not_be_empty(cls, v: str) -> str:
        """Validate that title is not empty or whitespace only."""
        if not v or not v.strip():
            raise ValueError("Title cannot be empty or whitespace only")
        return v.strip()


class TaskUpdate(SQLModel):
    """Schema for full task update (PUT) - all fields required."""

    title: str = Field(min_length=1, max_length=200, description="Task title (required)")
    description: Optional[str] = Field(default=None, max_length=1000, description="Task description")
    is_completed: bool = Field(description="Completion status")

    @field_validator("title")
    @classmethod
    def title_must_not_be_empty(cls, v: str) -> str:
        """Validate that title is not empty or whitespace only."""
        if not v or not v.strip():
            raise ValueError("Title cannot be empty or whitespace only")
        return v.strip()


class TaskPatch(SQLModel):
    """Schema for partial task update (PATCH) - all fields optional."""

    title: Optional[str] = Field(default=None, min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(default=None, max_length=1000, description="Task description")
    is_completed: Optional[bool] = Field(default=None, description="Completion status")

    @field_validator("title")
    @classmethod
    def title_must_not_be_empty(cls, v: Optional[str]) -> Optional[str]:
        """Validate that title is not empty or whitespace only if provided."""
        if v is not None and (not v or not v.strip()):
            raise ValueError("Title cannot be empty or whitespace only")
        return v.strip() if v else v


class TaskResponse(TaskBase):
    """Schema for task API responses."""

    id: UUID
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config for ORM mode."""

        from_attributes = True


# =============================================================================
# Conversation Models (Chat Persistence)
# =============================================================================


class Conversation(SQLModel, table=True):
    """Conversation database model for chat history."""

    id: UUID = Field(default_factory=uuid4, primary_key=True, description="Unique conversation identifier")
    user_id: str = Field(index=True, description="Owner's user identifier")
    title: Optional[str] = Field(default=None, max_length=200, description="Conversation title")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Conversation creation timestamp (UTC)",
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Last modification timestamp (UTC)",
    )


class Message(SQLModel, table=True):
    """Message database model for conversation messages."""

    id: UUID = Field(default_factory=uuid4, primary_key=True, description="Unique message identifier")
    conversation_id: UUID = Field(foreign_key="conversation.id", index=True, description="Parent conversation")
    role: str = Field(description="Message role: user, assistant, or tool")
    content: str = Field(description="Message content")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Message creation timestamp (UTC)",
    )
