"""
Profile cards router.

Endpoints:
- POST /api/profiles: Create a new profile card
- GET /api/profiles: Get all profile cards for current user
- GET /api/profiles/{card_id}: Get a specific profile card
- PUT /api/profiles/{card_id}: Update a profile card
- DELETE /api/profiles/{card_id}: Delete a profile card
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from app.auth.dependencies import get_current_user
from app.auth.db_models import User
from app.profiles import crud as profile_crud
from app.profiles.db_models import ProfileCard
from app.database import get_db

router = APIRouter(prefix="/api/profiles", tags=["profiles"])


class ProfileCardCreate(BaseModel):
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


class ProfileCardUpdate(BaseModel):
    card_title: Optional[str] = None
    name: Optional[str] = None
    title: Optional[str] = None
    tagline: Optional[str] = None
    primary_color: Optional[str] = None
    gradient: Optional[str] = None
    show_stacks: Optional[bool] = None
    show_contact: Optional[bool] = None
    show_github_stats: Optional[bool] = None
    stacks: Optional[List[Dict]] = None
    contacts: Optional[List[Dict]] = None


@router.post("")
async def create_profile_card(
    card_data: ProfileCardCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new profile card."""
    card = profile_crud.create_profile_card(
        db=db,
        user_id=current_user.id,
        card_title=card_data.card_title,
        name=card_data.name,
        title=card_data.title,
        tagline=card_data.tagline,
        primary_color=card_data.primary_color,
        gradient=card_data.gradient,
        show_stacks=card_data.show_stacks,
        show_contact=card_data.show_contact,
        show_github_stats=card_data.show_github_stats,
        stacks=card_data.stacks,
        contacts=card_data.contacts,
    )
    
    return {
        "id": card.id,
        "user_id": card.user_id,
        "card_title": card.card_title,
        "name": card.name,
        "title": card.title,
        "tagline": card.tagline,
        "primary_color": card.primary_color,
        "gradient": card.gradient,
        "show_stacks": card.show_stacks,
        "show_contact": card.show_contact,
        "show_github_stats": card.show_github_stats,
        "stacks": card.stacks,
        "contacts": card.contacts,
        "created_at": card.created_at.isoformat() if card.created_at else None,
        "updated_at": card.updated_at.isoformat() if card.updated_at else None,
    }


@router.get("")
async def get_profile_cards(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get all profile cards for current user."""
    cards = profile_crud.get_profile_cards_by_user_id(db, current_user.id)
    
    return [
        {
            "id": card.id,
            "user_id": card.user_id,
            "card_title": card.card_title,
            "name": card.name,
            "title": card.title,
            "tagline": card.tagline,
            "primary_color": card.primary_color,
            "gradient": card.gradient,
            "show_stacks": card.show_stacks,
            "show_contact": card.show_contact,
            "show_github_stats": card.show_github_stats,
            "stacks": card.stacks,
            "contacts": card.contacts,
            "created_at": card.created_at.isoformat() if card.created_at else None,
            "updated_at": card.updated_at.isoformat() if card.updated_at else None,
        }
        for card in cards
    ]


@router.get("/{card_id}")
async def get_profile_card(
    card_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get a specific profile card."""
    card = profile_crud.get_profile_card_by_id(db, card_id, current_user.id)
    
    if not card:
        raise HTTPException(status_code=404, detail="Profile card not found")
    
    return {
        "id": card.id,
        "user_id": card.user_id,
        "card_title": card.card_title,
        "name": card.name,
        "title": card.title,
        "tagline": card.tagline,
        "primary_color": card.primary_color,
        "gradient": card.gradient,
        "show_stacks": card.show_stacks,
        "show_contact": card.show_contact,
        "show_github_stats": card.show_github_stats,
        "stacks": card.stacks,
        "contacts": card.contacts,
        "created_at": card.created_at.isoformat() if card.created_at else None,
        "updated_at": card.updated_at.isoformat() if card.updated_at else None,
    }


@router.put("/{card_id}")
async def update_profile_card(
    card_id: int,
    card_data: ProfileCardUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update a profile card."""
    card = profile_crud.update_profile_card(
        db=db,
        card_id=card_id,
        user_id=current_user.id,
        card_title=card_data.card_title,
        name=card_data.name,
        title=card_data.title,
        tagline=card_data.tagline,
        primary_color=card_data.primary_color,
        gradient=card_data.gradient,
        show_stacks=card_data.show_stacks,
        show_contact=card_data.show_contact,
        show_github_stats=card_data.show_github_stats,
        stacks=card_data.stacks,
        contacts=card_data.contacts,
    )
    
    if not card:
        raise HTTPException(status_code=404, detail="Profile card not found")
    
    return {
        "id": card.id,
        "user_id": card.user_id,
        "card_title": card.card_title,
        "name": card.name,
        "title": card.title,
        "tagline": card.tagline,
        "primary_color": card.primary_color,
        "gradient": card.gradient,
        "show_stacks": card.show_stacks,
        "show_contact": card.show_contact,
        "show_github_stats": card.show_github_stats,
        "stacks": card.stacks,
        "contacts": card.contacts,
        "created_at": card.created_at.isoformat() if card.created_at else None,
        "updated_at": card.updated_at.isoformat() if card.updated_at else None,
    }


@router.delete("/{card_id}")
async def delete_profile_card(
    card_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a profile card."""
    success = profile_crud.delete_profile_card(db, card_id, current_user.id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Profile card not found")
    
    return {"message": "Profile card deleted successfully"}


# Public endpoint (no authentication required)
@router.get("/public/{github_login}/cards/{card_id}")
async def get_public_profile_card(
    github_login: str,
    card_id: int,
    db: Session = Depends(get_db),
):
    """
    Get a public profile card by GitHub login and card ID.
    This endpoint does not require authentication.
    """
    card = profile_crud.get_public_profile_card_by_github_login_and_card_id(
        db, github_login, card_id
    )
    
    if not card:
        raise HTTPException(status_code=404, detail="Profile card not found")
    
    return {
        "id": card.id,
        "user_id": card.user_id,
        "card_title": card.card_title,
        "name": card.name,
        "title": card.title,
        "tagline": card.tagline,
        "primary_color": card.primary_color,
        "gradient": card.gradient,
        "show_stacks": card.show_stacks,
        "show_contact": card.show_contact,
        "show_github_stats": card.show_github_stats,
        "stacks": card.stacks,
        "contacts": card.contacts,
        "created_at": card.created_at.isoformat() if card.created_at else None,
        "updated_at": card.updated_at.isoformat() if card.updated_at else None,
    }

