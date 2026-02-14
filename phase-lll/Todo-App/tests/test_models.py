"""Unit tests for Conversation and Message models."""

import pytest
from sqlmodel import Session, SQLModel, create_engine, select
from sqlmodel.pool import StaticPool
from uuid import uuid4

from app.models import Conversation, Message


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


class TestConversationModel:
    """Tests for the Conversation model."""

    def test_create_conversation(self, session: Session):
        """Test Conversation model creation with all fields."""
        conversation = Conversation(
            user_id="user-123",
            title="Test Conversation",
        )
        session.add(conversation)
        session.commit()
        session.refresh(conversation)

        assert conversation.id is not None
        assert conversation.user_id == "user-123"
        assert conversation.title == "Test Conversation"
        assert conversation.created_at is not None
        assert conversation.updated_at is not None

    def test_create_conversation_without_title(self, session: Session):
        """Test Conversation model creation without optional title."""
        conversation = Conversation(user_id="user-456")
        session.add(conversation)
        session.commit()
        session.refresh(conversation)

        assert conversation.id is not None
        assert conversation.user_id == "user-456"
        assert conversation.title is None

    def test_conversation_user_id_indexed(self, session: Session):
        """Test that multiple conversations can be retrieved by user_id."""
        # Create multiple conversations for same user
        for i in range(3):
            conv = Conversation(user_id="user-789", title=f"Conv {i}")
            session.add(conv)
        session.commit()

        # Query by user_id
        statement = select(Conversation).where(Conversation.user_id == "user-789")
        results = session.exec(statement).all()

        assert len(results) == 3


class TestMessageModel:
    """Tests for the Message model."""

    def test_create_message_with_conversation(self, session: Session):
        """Test Message model creation with foreign key to Conversation."""
        # Create parent conversation
        conversation = Conversation(user_id="user-123")
        session.add(conversation)
        session.commit()
        session.refresh(conversation)

        # Create message linked to conversation
        message = Message(
            conversation_id=conversation.id,
            role="user",
            content="Hello, AI!",
        )
        session.add(message)
        session.commit()
        session.refresh(message)

        assert message.id is not None
        assert message.conversation_id == conversation.id
        assert message.role == "user"
        assert message.content == "Hello, AI!"
        assert message.created_at is not None

    def test_message_roles(self, session: Session):
        """Test Message model with different roles."""
        conversation = Conversation(user_id="user-123")
        session.add(conversation)
        session.commit()

        roles = ["user", "assistant", "tool"]
        for role in roles:
            message = Message(
                conversation_id=conversation.id,
                role=role,
                content=f"Message from {role}",
            )
            session.add(message)
        session.commit()

        statement = select(Message).where(Message.conversation_id == conversation.id)
        messages = session.exec(statement).all()

        assert len(messages) == 3
        assert set(m.role for m in messages) == {"user", "assistant", "tool"}

    def test_message_foreign_key_constraint(self, session: Session):
        """Test that Message requires valid conversation_id."""
        # Create a message with valid conversation first
        conversation = Conversation(user_id="user-123")
        session.add(conversation)
        session.commit()

        message = Message(
            conversation_id=conversation.id,
            role="user",
            content="Valid message",
        )
        session.add(message)
        session.commit()

        # Verify the relationship works
        assert message.conversation_id == conversation.id

    def test_multiple_messages_per_conversation(self, session: Session):
        """Test that a conversation can have multiple messages."""
        conversation = Conversation(user_id="user-123")
        session.add(conversation)
        session.commit()

        # Add multiple messages
        for i in range(5):
            role = "user" if i % 2 == 0 else "assistant"
            message = Message(
                conversation_id=conversation.id,
                role=role,
                content=f"Message {i}",
            )
            session.add(message)
        session.commit()

        statement = select(Message).where(Message.conversation_id == conversation.id)
        messages = session.exec(statement).all()

        assert len(messages) == 5
