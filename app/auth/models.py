"""
User data models.

For production, replace the in-memory store with a proper database (e.g., PostgreSQL with SQLAlchemy).
"""
from datetime import datetime
from typing import Optional, Dict
from dataclasses import dataclass, field
from typing_extensions import TypedDict


class UserDict(TypedDict):
    """User data structure."""
    id: int
    github_id: int
    github_login: str
    name: Optional[str]
    email: Optional[str]
    avatar_url: Optional[str]
    html_url: Optional[str]
    created_at: datetime
    last_login_at: datetime


@dataclass
class User:
    """
    User model representing a user in our system.
    
    In production, replace this with a SQLAlchemy model:
    
    from sqlalchemy import Column, Integer, String, DateTime
    from sqlalchemy.ext.declarative import declarative_base
    
    Base = declarative_base()
    
    class User(Base):
        __tablename__ = "users"
        
        id = Column(Integer, primary_key=True, index=True)
        github_id = Column(Integer, unique=True, index=True, nullable=False)
        github_login = Column(String, nullable=False)
        name = Column(String, nullable=True)
        email = Column(String, nullable=True)
        avatar_url = Column(String, nullable=True)
        html_url = Column(String, nullable=True)
        github_access_token = Column(String, nullable=True)  # SECURITY: Should be encrypted in production
        created_at = Column(DateTime, default=datetime.utcnow)
        last_login_at = Column(DateTime, default=datetime.utcnow)
    """
    
    id: int
    github_id: int
    github_login: str
    name: Optional[str] = None
    email: Optional[str] = None
    avatar_url: Optional[str] = None
    html_url: Optional[str] = None
    github_access_token: Optional[str] = None  # SECURITY: Should be encrypted in production
    created_at: datetime = field(default_factory=datetime.utcnow)
    last_login_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> UserDict:
        """Convert User to dictionary."""
        return {
            "id": self.id,
            "github_id": self.github_id,
            "github_login": self.github_login,
            "name": self.name,
            "email": self.email,
            "avatar_url": self.avatar_url,
            "html_url": self.html_url,
            "created_at": self.created_at,
            "last_login_at": self.last_login_at,
        }


# In-memory user store (replace with database in production)
# Key: github_id, Value: User
_users_store: Dict[int, User] = {}
_next_user_id = 1


def get_user_by_github_id(github_id: int) -> Optional[User]:
    """Get user by GitHub ID."""
    return _users_store.get(github_id)


def get_user_by_id(user_id: int) -> Optional[User]:
    """Get user by internal user ID."""
    for user in _users_store.values():
        if user.id == user_id:
            return user
    return None


def create_or_update_user(
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
    
    In production, use SQLAlchemy:
    
    from sqlalchemy.orm import Session
    
    def create_or_update_user(db: Session, github_id: int, ...):
        user = db.query(User).filter(User.github_id == github_id).first()
        if user:
            user.last_login_at = datetime.utcnow()
            # Update other fields if needed
        else:
            user = User(github_id=github_id, ...)
            db.add(user)
        db.commit()
        db.refresh(user)
        return user
    """
    global _next_user_id
    
    user = _users_store.get(github_id)
    
    if user:
        # Update last login time
        user.last_login_at = datetime.utcnow()
        # Optionally update other fields
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
            id=_next_user_id,
            github_id=github_id,
            github_login=github_login,
            name=name,
            email=email,
            avatar_url=avatar_url,
            html_url=html_url,
            github_access_token=github_access_token,
        )
        _users_store[github_id] = user
        _next_user_id += 1
    
    return user

