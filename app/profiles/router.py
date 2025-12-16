"""
Profile cards router.

Endpoints:
- POST /api/profiles: Create a new profile card
- GET /api/profiles: Get all profile cards for current user
- GET /api/profiles/{card_id}: Get a specific profile card
- PUT /api/profiles/{card_id}: Update a profile card
- DELETE /api/profiles/{card_id}: Delete a profile card
"""
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import PlainTextResponse, StreamingResponse
from pydantic import BaseModel
from typing import List, Optional, Dict
from io import BytesIO
from sqlalchemy.orm import Session
from app.auth.dependencies import get_current_user
from app.auth.db_models import User
from app.profiles import crud as profile_crud
from app.users.github_stats_db_models import GitHubStats
from app.profiles.db_models import ProfileCard
from app.profiles import exporters
from app.database import get_db

router = APIRouter(prefix="/profiles", tags=["profiles"])


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


# Export endpoints (no authentication required)
@router.get("/public/{github_login}/cards/{card_id}/markdown/card")
async def get_profile_card_markdown_card(
    github_login: str,
    card_id: int,
    db: Session = Depends(get_db),
):
    """
    GitHub README에서 바로 카드 전체 디자인을 볼 수 있는
    이미지 기반 마크다운 코드를 반환합니다.

    예시:
      [![GitCard](image_url)](card_url)
    """
    card = profile_crud.get_public_profile_card_by_github_login_and_card_id(
        db, github_login, card_id
    )

    if not card:
        raise HTTPException(status_code=404, detail="Profile card not found")

    markdown = exporters.generate_svg_markdown(card, github_login)

    return PlainTextResponse(
        content=markdown,
        media_type="text/markdown"
    )


@router.get("/public/{github_login}/cards/{card_id}/readme")
async def get_profile_card_readme_template(
    github_login: str,
    card_id: int,
    db: Session = Depends(get_db),
):
    """
    GitHub README-safe 마크다운 템플릿을 반환합니다.
    
    이 템플릿은 GitHub README에서 안정적으로 렌더링되도록 설계되었습니다:
    - capsule-render를 사용한 배너
    - shields.io 배지를 사용한 스택/연락처
    - github-readme-stats를 사용한 GitHub 통계
    - GitCard 이미지 엔드포인트를 사용한 커스텀 카드
    
    복잡한 HTML/CSS나 인라인 스타일을 사용하지 않으며,
    GitHub가 안정적으로 지원하는 마크다운과 외부 이미지 서비스만 사용합니다.
    """
    card = profile_crud.get_public_profile_card_by_github_login_and_card_id(
        db, github_login, card_id
    )

    if not card:
        raise HTTPException(status_code=404, detail="Profile card not found")
    
    # Get GitHub stats if available
    stats_row = (
        db.query(GitHubStats)
        .filter(GitHubStats.user_id == card.user_id)
        .one_or_none()
    )
    
    stats = None
    if stats_row:
        stats = {
            "repositories": stats_row.repositories,
            "stars": stats_row.stars,
            "followers": stats_row.followers,
            "following": stats_row.following,
            "contributions": stats_row.contributions,
        }
    
    readme_template = exporters.generate_readme_template(card, github_login, stats=stats)

    return PlainTextResponse(
        content=readme_template,
        media_type="text/markdown"
    )


@router.get("/public/{github_login}/cards/{card_id}/image-url")
async def get_profile_card_image_url(
    github_login: str,
    card_id: int,
    db: Session = Depends(get_db),
):
    """
    Get profile card image URL and markdown formats.
    Returns URLs and markdown that can be used in GitHub README.
    This endpoint does not require authentication.
    
    Returns:
    - image_url: URL to the profile card page
    - markdown_badge: Markdown badge code
    - html_img: HTML img tag
    """
    card = profile_crud.get_public_profile_card_by_github_login_and_card_id(
        db, github_login, card_id
    )
    
    if not card:
        raise HTTPException(status_code=404, detail="Profile card not found")
    
    image_url = await exporters.generate_image_url(card, github_login)
    
    return {
        "image_url": image_url,
        "markdown_badge": f"[![GitCard]({image_url})]({image_url})",
        "html_img": f'<img src="{image_url}" alt="GitCard" />',
        "markdown_link": f"[내 GitCard 보기]({image_url})"
    }


@router.get("/public/{github_login}/cards/{card_id}/image")
async def get_profile_card_image(
    github_login: str,
    card_id: int,
    format: str = "png",
    v: Optional[str] = None,  # Cache busting parameter
    db: Session = Depends(get_db),
):
    """
    Get profile card as PNG or WebP image.
    Uses Playwright to take a screenshot of the actual web card UI.
    The image matches the web design exactly (gradient, shadows, layout, fonts).
    This endpoint does not require authentication.
    
    Args:
        github_login: GitHub username
        card_id: Profile card ID
        format: Image format ("png" or "webp", default: "png")
        v: Cache busting parameter (ignored but accepted for URL versioning)
        
    Returns:
        PNG or WebP image
    """
    card = profile_crud.get_public_profile_card_by_github_login_and_card_id(
        db, github_login, card_id
    )
    
    if not card:
        raise HTTPException(status_code=404, detail="Profile card not found")
    
    # Validate format
    if format not in ("png", "webp"):
        format = "png"
    
    screenshot = await exporters.generate_image_screenshot(
        card, github_login, format=format
    )
    
    if screenshot is None:
        raise HTTPException(
            status_code=503, 
            detail="Image generation is not available. Playwright may not be installed."
        )
    
    # Set appropriate media type
    media_type = "image/png" if format == "png" else "image/webp"
    file_ext = format
    
    return StreamingResponse(
        BytesIO(screenshot),
        media_type=media_type,
        headers={
            "Content-Type": media_type,  # Explicit Content-Type header
            "Content-Disposition": f'inline; filename="gitcard-{github_login}-{card_id}.{file_ext}"',
            "Cache-Control": "public, max-age=86400",  # 24 hours
            "X-Content-Type-Options": "nosniff",  # Prevent MIME type sniffing
        }
    )


@router.get("/public/{github_login}/cards/{card_id}/svg")
async def get_profile_card_svg(
    github_login: str,
    card_id: int,
    db: Session = Depends(get_db),
):
    """
    SVG 형식의 프로필 카드를 반환합니다.
    - GitHub README에서 그대로 렌더링 가능
    - 별도 CSS 없이 카드와 유사한 디자인 유지
    """
    card = profile_crud.get_public_profile_card_by_github_login_and_card_id(
        db, github_login, card_id
    )

    if not card:
        raise HTTPException(status_code=404, detail="Profile card not found")

    # 해당 카드의 소유자(user_id)에 대한 GitHub stats 조회 (없으면 None)
    stats_row = (
        db.query(GitHubStats)
        .filter(GitHubStats.user_id == card.user_id)
        .one_or_none()
    )

    stats = None
    if stats_row:
        stats = {
            "repositories": stats_row.repositories,
            "stars": stats_row.stars,
            "followers": stats_row.followers,
            "following": stats_row.following,
            "contributions": stats_row.contributions,
        }

    svg = exporters.generate_svg(card, github_login, stats=stats)

    return Response(
        content=svg,
        media_type="image/svg+xml",
        headers={
            "Content-Disposition": f'inline; filename=\"gitcard-{github_login}-{card_id}.svg\"'
        },
    )

