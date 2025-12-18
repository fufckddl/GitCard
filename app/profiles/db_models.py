"""
SQLAlchemy models for ProfileCard.

Replaces the in-memory ProfileCard model with a proper database model.
"""
from sqlalchemy import Column, Integer, String, Boolean, JSON, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class ProfileCard(Base):
    """Profile card model for database."""
    
    __tablename__ = "profile_cards"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    card_title = Column(String(255), nullable=False)  # 카드 목록에서 보이는 제목
    name = Column(String(255), nullable=False)
    title = Column(String(255), nullable=False)  # 프로필 카드에 표시되는 제목
    tagline = Column(String(500), nullable=True)
    primary_color = Column(String(7), nullable=False, default="#667eea")  # hex color
    gradient = Column(String(500), nullable=False)  # 그라데이션 문자열
    show_stacks = Column(Boolean, default=True, nullable=False)
    show_contact = Column(Boolean, default=True, nullable=False)
    show_github_stats = Column(Boolean, default=True, nullable=False)
    # Baekjoon tier display (Solved.ac badge)
    show_baekjoon = Column(Boolean, default=False, nullable=False)
    baekjoon_id = Column(String(255), nullable=True)
    stack_alignment = Column(String(10), nullable=False, default="center")  # "left", "center", "right"
    stacks = Column(JSON, nullable=False, default=list)
    contacts = Column(JSON, nullable=False, default=list)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationship (optional, for future use)
    # user = relationship("User", back_populates="profile_cards")

