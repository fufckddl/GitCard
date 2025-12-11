"""
FastAPI application entry point.

Main application setup with CORS configuration and router includes.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.auth.router import router as auth_router
from app.users.router import router as users_router
from app.profiles.router import router as profiles_router
from app.config import settings
from app.database import init_db
# Import models to ensure they are registered with Base
from app.auth import db_models  # noqa: F401
from app.profiles import db_models  # noqa: F401

app = FastAPI(
    title="GitCard API",
    description="Backend API for GitCard application with GitHub OAuth",
    version="1.0.0",
)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    init_db()

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

