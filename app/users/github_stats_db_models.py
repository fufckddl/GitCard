"""
SQLAlchemy model for storing cached GitHub statistics per user.

이 테이블은 GitHub API 호출 결과를 주기적으로 저장해 두고,
SVG 카드 생성 시 DB에 저장된 값을 사용하도록 하기 위한 용도입니다.
"""
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.database import Base


class GitHubStats(Base):
    """Cached GitHub statistics for a user."""

    __tablename__ = "github_stats"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)

    repositories = Column(Integer, nullable=True)
    stars = Column(Integer, nullable=True)
    followers = Column(Integer, nullable=True)
    following = Column(Integer, nullable=True)
    contributions = Column(Integer, nullable=True)

    last_synced_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

