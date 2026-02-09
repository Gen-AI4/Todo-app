"""JWT authentication module for the Todo App.

This module provides JWT token verification and user authentication
using Better Auth's JWT tokens with HS256 signing.
"""

import os
from typing import Optional

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

# =============================================================================
# Configuration
# =============================================================================

ALGORITHM = "HS256"
CLOCK_LEEWAY_SECONDS = 30  # Tolerance for clock skew

# Load and validate secret from environment
BETTER_AUTH_SECRET: Optional[str] = os.getenv("BETTER_AUTH_SECRET")

if not BETTER_AUTH_SECRET:
    raise ValueError(
        "BETTER_AUTH_SECRET environment variable is required. "
        "Please set it in your .env file."
    )

if len(BETTER_AUTH_SECRET) < 32:
    raise ValueError(
        "BETTER_AUTH_SECRET must be at least 32 characters for security. "
        f"Current length: {len(BETTER_AUTH_SECRET)}"
    )


# =============================================================================
# Data Models
# =============================================================================


class CurrentUser(BaseModel):
    """Authenticated user context from JWT token."""

    user_id: str
    email: Optional[str] = None

    @classmethod
    def from_token(cls, payload: dict) -> "CurrentUser":
        """Create CurrentUser from decoded JWT payload.

        Args:
            payload: Decoded JWT token payload

        Returns:
            CurrentUser instance with user_id and optional email
        """
        # Better Auth stores user_id in 'sub' claim
        # Also check nested 'user' object for compatibility
        user_id = payload.get("sub") or payload.get("user", {}).get("id")
        email = payload.get("user", {}).get("email")

        return cls(user_id=user_id, email=email)


# =============================================================================
# Token Verification
# =============================================================================

# HTTPBearer extracts token from Authorization: Bearer <token> header
security = HTTPBearer()


def verify_token(token: str) -> dict:
    """Verify and decode a JWT token.

    Args:
        token: JWT token string to verify

    Returns:
        Decoded token payload as dictionary

    Raises:
        HTTPException: If token is invalid, expired, or malformed
    """
    try:
        payload = jwt.decode(
            token,
            BETTER_AUTH_SECRET,
            algorithms=[ALGORITHM],
            options={
                "require": ["sub", "exp"],
                "verify_exp": True,
                "verify_iat": True,
            },
            leeway=CLOCK_LEEWAY_SECONDS,
        )
        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

    except jwt.InvalidSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token signature",
            headers={"WWW-Authenticate": "Bearer"},
        )

    except jwt.DecodeError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not decode token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


# =============================================================================
# FastAPI Dependency
# =============================================================================


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> CurrentUser:
    """FastAPI dependency to extract and validate current user from JWT.

    This dependency:
    1. Extracts the Bearer token from the Authorization header
    2. Verifies the token signature and expiration
    3. Returns a CurrentUser object with user_id

    Args:
        credentials: HTTP Authorization credentials from request header

    Returns:
        CurrentUser instance with authenticated user's information

    Raises:
        HTTPException: 401 if token is missing, invalid, or expired
    """
    token = credentials.credentials
    payload = verify_token(token)

    # Extract user_id from token
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: missing user ID",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return CurrentUser.from_token(payload)
