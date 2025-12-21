"""
사용자 데이터 모델.

프로덕션에서는 인메모리 저장소를 적절한 데이터베이스(예: SQLAlchemy를 사용한 PostgreSQL)로 교체하세요.
"""
from datetime import datetime
from typing import Optional, Dict
from dataclasses import dataclass, field
from typing_extensions import TypedDict


class UserDict(TypedDict):
    """사용자 데이터 구조."""
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
    시스템의 사용자를 나타내는 User 모델.
    
    프로덕션에서는 이를 SQLAlchemy 모델로 교체하세요:
    
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
        github_access_token = Column(String, nullable=True)  # 보안: 프로덕션에서는 암호화해야 함
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
    github_access_token: Optional[str] = None  # 보안: 프로덕션에서는 암호화해야 함
    created_at: datetime = field(default_factory=datetime.utcnow)
    last_login_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> UserDict:
        """User를 딕셔너리로 변환합니다."""
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


# 인메모리 사용자 저장소 (프로덕션에서는 데이터베이스로 교체)
# 키: github_id, 값: User
_users_store: Dict[int, User] = {}
_next_user_id = 1


def get_user_by_github_id(github_id: int) -> Optional[User]:
    """GitHub ID로 사용자를 가져옵니다."""
    return _users_store.get(github_id)


def get_user_by_id(user_id: int) -> Optional[User]:
    """내부 사용자 ID로 사용자를 가져옵니다."""
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
    새 사용자를 생성하거나 기존 사용자의 last_login_at을 업데이트합니다.
    
    프로덕션에서는 SQLAlchemy를 사용하세요:
    
    from sqlalchemy.orm import Session
    
    def create_or_update_user(db: Session, github_id: int, ...):
        user = db.query(User).filter(User.github_id == github_id).first()
        if user:
            user.last_login_at = datetime.utcnow()
            # 필요시 다른 필드 업데이트
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
        # 마지막 로그인 시간 업데이트
        user.last_login_at = datetime.utcnow()
        # 선택적으로 다른 필드 업데이트
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
        # 새 사용자 생성
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

