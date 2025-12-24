"""
ProfileCard용 SQLAlchemy 모델.

인메모리 ProfileCard 모델을 적절한 데이터베이스 모델로 대체합니다.
"""
from sqlalchemy import Column, Integer, String, Boolean, JSON, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class ProfileCard(Base):
    """데이터베이스용 프로필 카드 모델."""
    
    __tablename__ = "profile_cards"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    card_title = Column(String(255), nullable=False)  # 카드 목록에서 보이는 제목
    name = Column(String(255), nullable=False)
    title = Column(String(255), nullable=False)  # 프로필 카드에 표시되는 제목
    tagline = Column(String(500), nullable=True)
    primary_color = Column(String(7), nullable=False, default="#667eea")  # hex 색상
    gradient = Column(String(500), nullable=False)  # 그라데이션 문자열
    show_stacks = Column(Boolean, default=True, nullable=False)
    show_contact = Column(Boolean, default=True, nullable=False)
    show_github_stats = Column(Boolean, default=True, nullable=False)
    # 백준 티어 표시 (Solved.ac 배지)
    show_baekjoon = Column(Boolean, default=False, nullable=False)
    baekjoon_id = Column(String(255), nullable=True)
    # 기술 스택 카테고리 라벨 언어: 'ko' 또는 'en'
    stack_label_lang = Column(String(2), nullable=False, default="en")
    stack_alignment = Column(String(10), nullable=False, default="center")  # "left", "center", "right"
    stacks = Column(JSON, nullable=False, default=list)
    contacts = Column(JSON, nullable=False, default=list)
    repositories = Column(JSON, nullable=False, default=list)  # 선택된 레포지토리 목록
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # 관계 (선택사항, 향후 사용)
    # user = relationship("User", back_populates="profile_cards")

