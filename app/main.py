"""
FastAPI application entry point.

Main application setup with CORS configuration, routers, and background tasks.
"""
import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.auth.router import router as auth_router
from app.users.router import router as users_router
from app.profiles.router import router as profiles_router
from app.dashboard.router import router as dashboard_router
from app.config import settings
from app.database import init_db
# Import models to ensure they are registered with Base
from app.auth import db_models  # noqa: F401
from app.profiles import db_models  # noqa: F401
from app.users import github_stats_db_models  # noqa: F401
from app.dashboard import db_models  # noqa: F401
from app.users.github_stats_service import github_stats_background_loop

app = FastAPI(
    title="GitCard API",
    description="Backend API for GitCard application with GitHub OAuth",
    version="1.0.0",
)


@app.on_event("startup")
async def startup_event():
    """Initialize database and start background tasks on startup."""
    init_db()
    # GitHub 통계 주기적 동기화 백그라운드 태스크 시작 (기본 1시간 간격)
    asyncio.create_task(github_stats_background_loop())

# CORS configuration
# In production, restrict origins to your frontend domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.frontend_base_url,
        "http://localhost:5173",  # Vite default dev server
        "http://localhost:3000",   # Common React dev server
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(profiles_router)
app.include_router(dashboard_router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "GitCard API",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}

