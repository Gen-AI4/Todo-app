"""FastAPI application entry point for Todo App Backend."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import create_db_and_tables
from app.routers import tasks
from app.routers import auth as auth_router

# Import auth module to validate BETTER_AUTH_SECRET on startup
# This will raise ValueError if secret is missing or too short
from app import auth as auth_utils  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Lifespan context manager for startup and shutdown events.

    On startup: Creates database tables if they don't exist.
    On shutdown: Cleanup (currently none required).
    """
    # Startup: Create database tables
    create_db_and_tables()
    yield
    # Shutdown: Add cleanup here if needed


app = FastAPI(
    title="Todo App Backend API",
    description="CRUD API for managing tasks in the Todo application",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS middleware
# T037: Explicitly allow Authorization header for JWT auth
# Allow all origins for Hugging Face Spaces and development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for Spaces compatibility
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept"],
    expose_headers=["Authorization"],
)


# Include routers
app.include_router(auth_router.router)  # Auth routes at /api/auth
app.include_router(tasks.router, prefix="/api")  # Task routes at /api/tasks



@app.get("/", include_in_schema=False)
def root() -> dict[str, str]:
    """Root endpoint used by hosting health checks.

    Returns a simple 200 OK JSON so platforms that probe `/` see the app is alive.
    """
    return {"status": "running", "info": "Todo App Backend - visit /docs or /health"}


@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}
