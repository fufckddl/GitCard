"""
Profile card data models.

For production, replace the in-memory store with a proper database.
"""
from datetime import datetime
from typing import Optional, Dict, List
from dataclasses import dataclass, field
from typing_extensions import TypedDict


class ProfileCardDict(TypedDict):
    """Profile card data structure."""
    id: int
    user_id: int
    card_title: str      # 카드 목록에서 보이는 제목
    name: str
    title: str           # 프로필 카드에 표시되는 제목
    tagline: str
    primary_color: str   # 카드의 주요 색상 (hex color) - UI에서 선택용
    gradient: str        # 배너에 사용할 그라데이션 문자열
    show_stacks: bool
    show_contact: bool
    show_github_stats: bool
    stacks: List[Dict]
    contacts: List[Dict]
    created_at: datetime
    updated_at: datetime


@dataclass
class ProfileCard:
    """
    Profile card model.
    
    In production, use SQLAlchemy:
    
    from sqlalchemy import Column, Integer, String, Boolean, JSON, DateTime, ForeignKey
    from sqlalchemy.ext.declarative import declarative_base
    
    Base = declarative_base()
    
    class ProfileCard(Base):
        __tablename__ = "profile_cards"
        
        id = Column(Integer, primary_key=True, index=True)
        user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
        name = Column(String, nullable=False)
        title = Column(String, nullable=False)
        tagline = Column(String, nullable=True)
        show_stacks = Column(Boolean, default=True)
        show_contact = Column(Boolean, default=True)
        show_github_stats = Column(Boolean, default=True)
        stacks = Column(JSON, default=list)
        contacts = Column(JSON, default=list)
        created_at = Column(DateTime, default=datetime.utcnow)
        updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    """
    
    id: int
    user_id: int
    card_title: str      # 카드 목록에서 보이는 제목
    name: str
    title: str           # 프로필 카드에 표시되는 제목
    tagline: str
    primary_color: str   # 카드의 주요 색상 (hex color) - UI에서 선택용
    gradient: str        # 배너에 사용할 그라데이션 문자열
    show_stacks: bool
    show_contact: bool
    show_github_stats: bool
    stacks: List[Dict]
    contacts: List[Dict]
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> ProfileCardDict:
        """Convert ProfileCard to dictionary."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "card_title": self.card_title,
            "name": self.name,
            "title": self.title,
            "tagline": self.tagline,
            "primary_color": self.primary_color,
            "gradient": self.gradient,
            "show_stacks": self.show_stacks,
            "show_contact": self.show_contact,
            "show_github_stats": self.show_github_stats,
            "stacks": self.stacks,
            "contacts": self.contacts,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


# In-memory profile card store (replace with database in production)
# Key: card_id, Value: ProfileCard
_profile_cards_store: Dict[int, ProfileCard] = {}
_next_card_id = 1


def create_profile_card(
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
    stacks: List[Dict],
    contacts: List[Dict],
) -> ProfileCard:
    """Create a new profile card."""
    global _next_card_id
    
    card = ProfileCard(
        id=_next_card_id,
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
        stacks=stacks,
        contacts=contacts,
    )
    _profile_cards_store[_next_card_id] = card
    _next_card_id += 1
    
    return card


def get_profile_cards_by_user_id(user_id: int) -> List[ProfileCard]:
    """Get all profile cards for a user."""
    return [
        card for card in _profile_cards_store.values()
        if card.user_id == user_id
    ]


def get_profile_card_by_id(card_id: int, user_id: int) -> Optional[ProfileCard]:
    """Get a profile card by ID (only if it belongs to the user)."""
    card = _profile_cards_store.get(card_id)
    if card and card.user_id == user_id:
        return card
    return None


def update_profile_card(
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
    stacks: Optional[List[Dict]] = None,
    contacts: Optional[List[Dict]] = None,
) -> Optional[ProfileCard]:
    """Update a profile card."""
    card = get_profile_card_by_id(card_id, user_id)
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
    if stacks is not None:
        card.stacks = stacks
    if contacts is not None:
        card.contacts = contacts
    
    card.updated_at = datetime.utcnow()
    return card


def delete_profile_card(card_id: int, user_id: int) -> bool:
    """Delete a profile card."""
    card = get_profile_card_by_id(card_id, user_id)
    if not card:
        return False
    
    del _profile_cards_store[card_id]
    return True

