"""Authentication routes for user registration and login."""

import hashlib
import os
from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.database import get_session
from app.models import User, UserCreate, UserLogin, UserResponse, TokenResponse

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

# JWT Configuration
ALGORITHM = "HS256"
TOKEN_EXPIRE_HOURS = 24
BETTER_AUTH_SECRET = os.getenv("BETTER_AUTH_SECRET")


def hash_password(password: str) -> str:
    """Hash a password using SHA-256 with salt."""
    # Simple hash for demo - in production use bcrypt or argon2
    salt = BETTER_AUTH_SECRET[:16] if BETTER_AUTH_SECRET else "default_salt_123"
    return hashlib.sha256(f"{salt}{password}".encode()).hexdigest()


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a password against its hash."""
    return hash_password(password) == password_hash


def create_access_token(user_id: str, email: str) -> str:
    """Create a JWT access token."""
    expire = datetime.now(timezone.utc) + timedelta(hours=TOKEN_EXPIRE_HOURS)
    payload = {
        "sub": user_id,
        "email": email,
        "exp": expire,
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, BETTER_AUTH_SECRET, algorithm=ALGORITHM)


@router.post("/sign-up/email", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register_user(
    user_data: UserCreate,
    session: Session = Depends(get_session),
) -> TokenResponse:
    """
    Register a new user account.

    Returns a JWT token and user data on success.
    """
    # Check if email already exists
    existing_user = session.exec(
        select(User).where(User.email == user_data.email)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email already exists",
        )

    # Create new user
    user = User(
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        name=user_data.name,
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    # Generate token
    token = create_access_token(str(user.id), user.email)

    return TokenResponse(
        token=token,
        user=UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            created_at=user.created_at,
        ),
    )


@router.post("/sign-in/email", response_model=TokenResponse)
def login_user(
    credentials: UserLogin,
    session: Session = Depends(get_session),
) -> TokenResponse:
    """
    Login with email and password.

    Returns a JWT token and user data on success.
    """
    # Find user by email
    user = session.exec(
        select(User).where(User.email == credentials.email)
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # Verify password
    if not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # Generate token
    token = create_access_token(str(user.id), user.email)

    return TokenResponse(
        token=token,
        user=UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            created_at=user.created_at,
        ),
    )
