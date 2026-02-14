"""Chat endpoint for the Todo AI Chatbot.

Routes user messages through the OpenRouter agent and returns responses.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from openai import APIConnectionError, APIError, RateLimitError
from sqlmodel import Session

from app.agent import run_agent
from app.auth import CurrentUser, get_current_user
from app.database import get_session
from app.schemas import ChatRequest, ChatResponse

router = APIRouter(tags=["Chat"])


@router.post(
    "/chat",
    response_model=ChatResponse,
    summary="Send a message to the AI assistant",
    responses={
        401: {"description": "Authentication required"},
        500: {"description": "Server error"},
    },
)
def chat(
    request: ChatRequest,
    current_user: CurrentUser = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> ChatResponse:
    """Process a user message through the AI agent.

    - **message**: Natural language message (e.g., "Add a task called Buy milk")
    - **conversation_id**: Optional UUID to continue an existing conversation

    The agent can invoke task management tools (add, list, complete, delete, update)
    on behalf of the authenticated user.
    """
    try:
        response_text, conversation_id = run_agent(
            session=session,
            user_id=current_user.user_id,
            user_message=request.message,
            conversation_id=request.conversation_id,
        )
        return ChatResponse(
            response=response_text,
            conversation_id=conversation_id,
        )

    except ValueError as e:
        # Conversation not found or validation error
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )

    except (APIError, APIConnectionError):
        return ChatResponse(
            response="I'm having trouble connecting right now. Please try again in a moment.",
            conversation_id=request.conversation_id or _create_fallback_conversation(session, current_user.user_id),
        )

    except RateLimitError:
        return ChatResponse(
            response="I'm receiving too many requests right now. Please wait a moment and try again.",
            conversation_id=request.conversation_id or _create_fallback_conversation(session, current_user.user_id),
        )

    except Exception:
        return ChatResponse(
            response="Something went wrong. Please try again.",
            conversation_id=request.conversation_id or _create_fallback_conversation(session, current_user.user_id),
        )


def _create_fallback_conversation(session: Session, user_id: str):
    """Create a conversation for error responses when none exists."""
    from app.models import Conversation

    conversation = Conversation(user_id=user_id)
    session.add(conversation)
    session.commit()
    session.refresh(conversation)
    return conversation.id
