"""
CRUD operations for User model.

Replaces the in-memory store functions with database operations.
"""
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime
from typing import Optional
from app.auth.db_models import User


def get_user_by_github_id(db: Session, github_id: int) -> Optional[User]:
    """Get user by GitHub ID."""
    stmt = select(User).where(User.github_id == github_id)
    result = db.execute(stmt)
    return result.scalar_one_or_none()


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """Get user by internal user ID."""
    stmt = select(User).where(User.id == user_id)
    result = db.execute(stmt)
    return result.scalar_one_or_none()


def create_or_update_user(
    db: Session,
    github_id: int,
    github_login: str,
    name: Optional[str] = None,
    email: Optional[str] = None,
    avatar_url: Optional[str] = None,
    html_url: Optional[str] = None,
    github_access_token: Optional[str] = None,
) -> User:
    """
    Create a new user or update existing user's last_login_at.
    """
    user = get_user_by_github_id(db, github_id)
    
    if user:
        # Update existing user
        user.last_login_at = datetime.utcnow()
        if name:
            user.name = name
        if email:
            user.email = email
        if avatar_url:
            user.avatar_url = avatar_url
        if html_url:
            user.html_url = html_url
        if github_access_token:
            user.github_access_token = github_access_token
    else:
        # Create new user
        user = User(
            github_id=github_id,
            github_login=github_login,
            name=name,
            email=email,
            avatar_url=avatar_url,
            html_url=html_url,
            github_access_token=github_access_token,
        )
        db.add(user)
    
    db.commit()
    db.refresh(user)
    return user





