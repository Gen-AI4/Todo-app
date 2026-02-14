"""Request and response schemas for the Chat endpoint."""

from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Incoming chat message from user."""

    message: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="User's message text",
    )
    conversation_id: Optional[UUID] = Field(
        None,
        description="Continue existing conversation (omit to start new)",
    )


class ChatResponse(BaseModel):
    """Agent's reply to the user."""

    response: str = Field(..., description="Agent's response text")
    conversation_id: UUID = Field(
        ...,
        description="Conversation ID for follow-up messages",
    )
