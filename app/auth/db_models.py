"""
SQLAlchemy models for User.

Replaces the in-memory User model with a proper database model.
"""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    """User model for database."""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    github_id = Column(Integer, unique=True, index=True, nullable=False)
    github_login = Column(String(255), nullable=False, index=True)
    name = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    html_url = Column(String(500), nullable=True)
    github_access_token = Column(String(500), nullable=True)  # SECURITY: Should be encrypted in production
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    last_login_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)





