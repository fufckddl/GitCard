"""
ProfileCard 모델에 대한 CRUD 작업.

인메모리 저장소 함수를 데이터베이스 작업으로 대체합니다.
"""
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime
from typing import Optional, List, Dict
from app.profiles.db_models import ProfileCard


def create_profile_card(
    db: Session,
    user_id: int,
    card_title: str,
    name: str,
    title: str,
    tagline: str,
    primary_color: str,
    gradient: str,
    show_stacks: bool,
    show_contact: bool,
    show_github_stats: bool,
    show_baekjoon: bool,
    baekjoon_id: str,
    stack_label_lang: str,
    stacks: List[Dict],
    contacts: List[Dict],
    stack_alignment: str = "center",
    repositories: Optional[List[Dict]] = None,
) -> ProfileCard:
    """새 프로필 카드를 생성합니다."""
    print(f"[CREATE_CARD] stack_alignment={stack_alignment}")  # 디버그 로그
    card = ProfileCard(
        user_id=user_id,
        card_title=card_title,
        name=name,
        title=title,
        tagline=tagline,
        primary_color=primary_color,
        gradient=gradient,
        show_stacks=show_stacks,
        show_contact=show_contact,
        show_github_stats=show_github_stats,
        show_baekjoon=show_baekjoon,
        baekjoon_id=baekjoon_id,
        stack_label_lang=stack_label_lang,
        stack_alignment=stack_alignment,
        stacks=stacks,
        contacts=contacts,
        repositories=repositories or [],
    )
    db.add(card)
    db.commit()
    db.refresh(card)
    print(f"[CREATE_CARD] Saved card_id={card.id}, stack_alignment={card.stack_alignment}")  # 디버그 로그
    return card


def get_profile_cards_by_user_id(db: Session, user_id: int) -> List[ProfileCard]:
    """사용자의 모든 프로필 카드를 가져옵니다."""
    stmt = select(ProfileCard).where(ProfileCard.user_id == user_id).order_by(ProfileCard.created_at.desc())
    result = db.execute(stmt)
    return list(result.scalars().all())


def get_profile_card_by_id(db: Session, card_id: int, user_id: int) -> Optional[ProfileCard]:
    """ID로 프로필 카드를 가져옵니다 (사용자에게 속한 경우에만)."""
    stmt = select(ProfileCard).where(
        ProfileCard.id == card_id,
        ProfileCard.user_id == user_id
    )
    result = db.execute(stmt)
    return result.scalar_one_or_none()


def update_profile_card(
    db: Session,
    card_id: int,
    user_id: int,
    card_title: Optional[str] = None,
    name: Optional[str] = None,
    title: Optional[str] = None,
    tagline: Optional[str] = None,
    primary_color: Optional[str] = None,
    gradient: Optional[str] = None,
    show_stacks: Optional[bool] = None,
    show_contact: Optional[bool] = None,
    show_github_stats: Optional[bool] = None,
    show_baekjoon: Optional[bool] = None,
    baekjoon_id: Optional[str] = None,
    stack_label_lang: Optional[str] = None,
    stack_alignment: Optional[str] = None,
    stacks: Optional[List[Dict]] = None,
    contacts: Optional[List[Dict]] = None,
    repositories: Optional[List[Dict]] = None,
) -> Optional[ProfileCard]:
    """프로필 카드를 업데이트합니다."""
    card = get_profile_card_by_id(db, card_id, user_id)
    if not card:
        return None
    
    if card_title is not None:
        card.card_title = card_title
    if name is not None:
        card.name = name
    if title is not None:
        card.title = title
    if tagline is not None:
        card.tagline = tagline
    if primary_color is not None:
        card.primary_color = primary_color
    if gradient is not None:
        card.gradient = gradient
    if show_stacks is not None:
        card.show_stacks = show_stacks
    if show_contact is not None:
        card.show_contact = show_contact
    if show_github_stats is not None:
        card.show_github_stats = show_github_stats
    if show_baekjoon is not None:
        card.show_baekjoon = show_baekjoon
    if baekjoon_id is not None:
        card.baekjoon_id = baekjoon_id
    if stack_label_lang is not None:
        card.stack_label_lang = stack_label_lang
    if stack_alignment is not None:
        print(f"[UPDATE_CARD] Updating stack_alignment from '{card.stack_alignment}' to '{stack_alignment}'")  # 디버그 로그
        card.stack_alignment = stack_alignment
    if stacks is not None:
        card.stacks = stacks
    if contacts is not None:
        card.contacts = contacts
    if repositories is not None:
        card.repositories = repositories
    
    card.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(card)
    return card


def delete_profile_card(db: Session, card_id: int, user_id: int) -> bool:
    """프로필 카드를 삭제합니다."""
    card = get_profile_card_by_id(db, card_id, user_id)
    if card:
        db.delete(card)
        db.commit()
        return True
    return False


def get_public_profile_card_by_github_login_and_card_id(
    db: Session,
    github_login: str,
    card_id: int
) -> Optional[ProfileCard]:
    """
    GitHub 로그인 및 카드 ID로 공개 프로필 카드를 가져옵니다.
    인증 없이 공개 보기를 위해 사용됩니다.
    """
    from app.auth.db_models import User
    from sqlalchemy import select
    
    # 먼저 github_login으로 사용자 찾기
    user_stmt = select(User).where(User.github_login == github_login)
    user_result = db.execute(user_stmt)
    user = user_result.scalar_one_or_none()
    
    if not user:
        return None
    
    # 그런 다음 card_id와 user_id로 카드 찾기
    card_stmt = select(ProfileCard).where(
        ProfileCard.id == card_id,
        ProfileCard.user_id == user.id
    )
    card_result = db.execute(card_stmt)
    return card_result.scalar_one_or_none()


