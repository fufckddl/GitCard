"""
프로필 카드 라우터.

엔드포인트:
- POST /api/profiles: 새 프로필 카드 생성
- GET /api/profiles: 현재 사용자의 모든 프로필 카드 가져오기
- GET /api/profiles/{card_id}: 특정 프로필 카드 가져오기
- PUT /api/profiles/{card_id}: 프로필 카드 업데이트
- DELETE /api/profiles/{card_id}: 프로필 카드 삭제
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
    show_baekjoon: bool = False
    baekjoon_id: Optional[str] = None
    stack_label_lang: str = "en"  # 'ko' or 'en'
    stack_alignment: str = "center"  # "left", "center", "right"
    stacks: List[Dict]
    contacts: List[Dict]
    repositories: Optional[List[Dict]] = None  # 선택된 레포지토리 목록


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
    show_baekjoon: Optional[bool] = None
    baekjoon_id: Optional[str] = None
    stack_alignment: Optional[str] = None  # "left", "center", "right"
    stack_label_lang: Optional[str] = None  # 'ko' or 'en'
    stacks: Optional[List[Dict]] = None
    contacts: Optional[List[Dict]] = None
    repositories: Optional[List[Dict]] = None  # 선택된 레포지토리 목록


@router.post("")
async def create_profile_card(
    card_data: ProfileCardCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """새 프로필 카드를 생성합니다."""
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
        show_baekjoon=card_data.show_baekjoon,
        baekjoon_id=card_data.baekjoon_id or "",
        stack_label_lang=card_data.stack_label_lang,
        stacks=card_data.stacks,
        contacts=card_data.contacts,
        stack_alignment=card_data.stack_alignment,
        repositories=card_data.repositories or [],
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
        "show_baekjoon": getattr(card, "show_baekjoon", False),
        "baekjoon_id": getattr(card, "baekjoon_id", None),
        "stack_label_lang": getattr(card, "stack_label_lang", "en"),
        "stack_alignment": card.stack_alignment,
        "stacks": card.stacks,
        "contacts": card.contacts,
        "repositories": getattr(card, "repositories", []),
        "created_at": card.created_at.isoformat() if card.created_at else None,
        "updated_at": card.updated_at.isoformat() if card.updated_at else None,
    }


@router.get("")
async def get_profile_cards(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """현재 사용자의 모든 프로필 카드를 가져옵니다."""
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
            "show_baekjoon": getattr(card, "show_baekjoon", False),
            "baekjoon_id": getattr(card, "baekjoon_id", None),
            "stack_label_lang": getattr(card, "stack_label_lang", "en"),
            "stack_alignment": card.stack_alignment,
            "stacks": card.stacks,
            "contacts": card.contacts,
            "repositories": getattr(card, "repositories", []),
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
    """특정 프로필 카드를 가져옵니다."""
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
        "show_baekjoon": getattr(card, "show_baekjoon", False),
        "baekjoon_id": getattr(card, "baekjoon_id", None),
        "stack_label_lang": getattr(card, "stack_label_lang", "en"),
        "stack_alignment": getattr(card, "stack_alignment", "center"),
        "stacks": card.stacks,
        "contacts": card.contacts,
        "repositories": getattr(card, "repositories", []),
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
    """프로필 카드를 업데이트합니다."""
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
        show_baekjoon=card_data.show_baekjoon,
        baekjoon_id=card_data.baekjoon_id,
        stack_label_lang=card_data.stack_label_lang,
        stack_alignment=card_data.stack_alignment,
        stacks=card_data.stacks,
        contacts=card_data.contacts,
        repositories=card_data.repositories,
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
        "show_baekjoon": getattr(card, "show_baekjoon", False),
        "baekjoon_id": getattr(card, "baekjoon_id", None),
        "stack_label_lang": getattr(card, "stack_label_lang", "en"),
        "stack_alignment": card.stack_alignment,
        "stacks": card.stacks,
        "contacts": card.contacts,
        "repositories": getattr(card, "repositories", []),
        "created_at": card.created_at.isoformat() if card.created_at else None,
        "updated_at": card.updated_at.isoformat() if card.updated_at else None,
    }


@router.delete("/{card_id}")
async def delete_profile_card(
    card_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """프로필 카드를 삭제합니다."""
    success = profile_crud.delete_profile_card(db, card_id, current_user.id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Profile card not found")
    
    return {"message": "Profile card deleted successfully"}


# 공개 엔드포인트 (인증 불필요)
@router.get("/public/{github_login}/cards/{card_id}")
async def get_public_profile_card(
    github_login: str,
    card_id: int,
    db: Session = Depends(get_db),
):
    """
    GitHub 로그인 및 카드 ID로 공개 프로필 카드를 가져옵니다.
    이 엔드포인트는 인증이 필요하지 않습니다.
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
        "show_baekjoon": getattr(card, "show_baekjoon", False),
        "baekjoon_id": getattr(card, "baekjoon_id", None),
        "stack_label_lang": getattr(card, "stack_label_lang", "en"),
        "stack_alignment": card.stack_alignment,
        "stacks": card.stacks,
        "contacts": card.contacts,
        "repositories": getattr(card, "repositories", []),
        "created_at": card.created_at.isoformat() if card.created_at else None,
        "updated_at": card.updated_at.isoformat() if card.updated_at else None,
    }


# 내보내기 엔드포인트 (인증 불필요)
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
    
    # 사용 가능한 경우 GitHub 통계 가져오기
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
    프로필 카드 이미지 URL 및 마크다운 형식을 가져옵니다.
    GitHub README에서 사용할 수 있는 URL 및 마크다운을 반환합니다.
    이 엔드포인트는 인증이 필요하지 않습니다.
    
    Returns:
    - image_url: 프로필 카드 페이지 URL
    - markdown_badge: 마크다운 배지 코드
    - html_img: HTML img 태그
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
    v: Optional[str] = None,  # 캐시 무효화 매개변수
    db: Session = Depends(get_db),
):
    """
    프로필 카드를 PNG 또는 WebP 이미지로 가져옵니다.
    Playwright를 사용하여 실제 웹 카드 UI의 스크린샷을 찍습니다.
    이미지는 웹 디자인과 정확히 일치합니다 (그라데이션, 그림자, 레이아웃, 폰트).
    이 엔드포인트는 인증이 필요하지 않습니다.
    
    Args:
        github_login: GitHub 사용자명
        card_id: 프로필 카드 ID
        format: 이미지 형식 ("png" 또는 "webp", 기본값: "png")
        v: 캐시 무효화 매개변수 (URL 버전 관리를 위해 무시되지만 허용됨)
        
    Returns:
        PNG 또는 WebP 이미지
    """
    card = profile_crud.get_public_profile_card_by_github_login_and_card_id(
        db, github_login, card_id
    )
    
    if not card:
        raise HTTPException(status_code=404, detail="Profile card not found")
    
    # 형식 검증
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
    
    # 적절한 미디어 타입 설정
    media_type = "image/png" if format == "png" else "image/webp"
    file_ext = format
    
    return StreamingResponse(
        BytesIO(screenshot),
        media_type=media_type,
        headers={
            "Content-Type": media_type,  # 명시적 Content-Type 헤더
            "Content-Disposition": f'inline; filename="gitcard-{github_login}-{card_id}.{file_ext}"',
            "Cache-Control": "public, max-age=86400",  # 24시간
            "X-Content-Type-Options": "nosniff",  # MIME 타입 스니핑 방지
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

    # 해당 카드의 소유자(user_id)에 대한 GitHub 통계 조회 (없으면 None)
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


@router.get("/public/{github_login}/cards/{card_id}/banner")
async def get_profile_card_banner(
    github_login: str,
    card_id: int,
    db: Session = Depends(get_db),
):
    """
    SVG 형식의 배너만 반환합니다.
    - GitHub README에서 이미지로 참조 가능 (capsule-render 방식)
    - 그라데이션 배경과 텍스트 포함
    - 프론트엔드의 PublicProfileCardPage와 동일한 색상을 사용합니다.
    """
    card = profile_crud.get_public_profile_card_by_github_login_and_card_id(
        db, github_login, card_id
    )

    if not card:
        raise HTTPException(status_code=404, detail="Profile card not found")

    # 디버그: 콘솔에 출력 (systemd 로그에 나타남)
    print(f"[BANNER DEBUG] card_id={card_id}, gradient={card.gradient}, primary_color={card.primary_color}")
    
    # 디버깅을 위한 색상 추출
    primary, secondary = exporters._extract_gradient_colors(card)
    print(f"[BANNER DEBUG] Extracted colors - primary={primary}, secondary={secondary}")

    svg_banner = exporters.generate_svg_banner(card)

    return Response(
        content=svg_banner,
        media_type="image/svg+xml",
        headers={
            "Content-Disposition": f'inline; filename="gitcard-banner-{github_login}-{card_id}.svg"',
            "Cache-Control": "public, max-age=86400",  # 24시간
        },
    )


@router.get("/public/{github_login}/cards/{card_id}/contact")
async def get_profile_card_contact(
    github_login: str,
    card_id: int,
    db: Session = Depends(get_db),
):
    """
    SVG 형식의 연락처 섹션만 반환합니다.
    - GitHub README에서 이미지로 참조 가능 (capsule-render 방식)
    - 연락처 카드들을 그리드 형태로 배치
    - 아이콘, 라벨, 값이 포함된 카드 형태
    """
    card = profile_crud.get_public_profile_card_by_github_login_and_card_id(
        db, github_login, card_id
    )

    if not card:
        raise HTTPException(status_code=404, detail="Profile card not found")

    svg_contact = exporters.generate_svg_contact(card)

    if not svg_contact:
        raise HTTPException(status_code=404, detail="Contact section not available")

    return Response(
        content=svg_contact,
        media_type="image/svg+xml",
        headers={
            "Content-Disposition": f'inline; filename="gitcard-contact-{github_login}-{card_id}.svg"',
            "Cache-Control": "public, max-age=86400",  # 24시간
        },
    )


@router.get("/public/{github_login}/cards/{card_id}/banner/debug")
async def get_profile_card_banner_debug(
    github_login: str,
    card_id: int,
    db: Session = Depends(get_db),
):
    """
    배너 색상 추출 디버깅 정보를 반환합니다.
    실제 데이터베이스의 gradient 값과 추출된 색상을 확인할 수 있습니다.
    """
    card = profile_crud.get_public_profile_card_by_github_login_and_card_id(
        db, github_login, card_id
    )

    if not card:
        raise HTTPException(status_code=404, detail="Profile card not found")

    # 색상 추출
    primary, secondary = exporters._extract_gradient_colors(card)
    
    return {
        "card_id": card.id,
        "gradient": card.gradient,
        "primary_color": card.primary_color,
        "extracted_primary": primary,
        "extracted_secondary": secondary,
    }


@router.get("/public/{github_login}/cards/{card_id}/repositories/{repo_index}/banner")
async def get_repository_banner(
    github_login: str,
    card_id: int,
    repo_index: int,
    db: Session = Depends(get_db),
):
    """
    레포지토리 정보를 SVG 배너 이미지로 반환합니다.
    - GitHub README에서 이미지로 참조 가능
    - 카드 형태의 레이아웃: 레포지토리 이름, 언어 배지, 설명, Stars/Forks 통계
    - 인증 불필요 (공개 엔드포인트)
    
    Args:
        github_login: GitHub 사용자명
        card_id: 프로필 카드 ID
        repo_index: 레포지토리 인덱스 (0부터 시작)
    
    Returns:
        SVG 형식의 레포지토리 배너
    """
    card = profile_crud.get_public_profile_card_by_github_login_and_card_id(
        db, github_login, card_id
    )
    
    if not card:
        raise HTTPException(status_code=404, detail="Profile card not found")
    
    repositories = getattr(card, "repositories", [])
    
    # 디버깅: repositories 데이터 확인
    print(f"[REPO BANNER DEBUG] card_id={card_id}, github_login={github_login}, repo_index={repo_index}")
    print(f"[REPO BANNER DEBUG] repositories type={type(repositories)}, repositories={repositories}")
    print(f"[REPO BANNER DEBUG] repositories length={len(repositories) if repositories else 0}")
    
    if not repositories or len(repositories) == 0:
        raise HTTPException(status_code=404, detail="No repositories found for this card")
    
    if repo_index < 0 or repo_index >= len(repositories):
        raise HTTPException(status_code=404, detail=f"Repository index out of range. Available: 0-{len(repositories)-1}, requested: {repo_index}")
    
    repo = repositories[repo_index]
    print(f"[REPO BANNER DEBUG] Selected repo: {repo}, type: {type(repo)}")
    
    try:
        svg_banner = exporters.generate_svg_repository_banner(repo)
        print(f"[REPO BANNER DEBUG] SVG generated successfully, length: {len(svg_banner)}")
    except Exception as e:
        print(f"[REPO BANNER DEBUG] Error generating SVG: {str(e)}")
        import traceback
        print(f"[REPO BANNER DEBUG] Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Error generating repository banner: {str(e)}")
    
    return Response(
        content=svg_banner,
        media_type="image/svg+xml",
        headers={
            "Content-Disposition": f'inline; filename="repo-banner-{github_login}-{card_id}-{repo_index}.svg"',
            "Cache-Control": "public, max-age=86400",  # 24시간
        },
    )


@router.get("/public/{github_login}/cards/{card_id}/html")
async def get_profile_card_html(
    github_login: str,
    card_id: int,
    db: Session = Depends(get_db),
):
    """
    HTML 형식의 프로필 카드를 반환합니다.
    - 인라인 스타일을 사용하여 독립적으로 렌더링 가능
    - stackMeta.ts의 카테고리 구조를 따름 (언어, 프론트엔드, 백엔드, 모바일, 데이터베이스 등)
    - 각 스택의 key, label, color를 올바르게 사용
    """
    card = profile_crud.get_public_profile_card_by_github_login_and_card_id(
        db, github_login, card_id
    )

    if not card:
        raise HTTPException(status_code=404, detail="Profile card not found")

    html = exporters.generate_html(card, github_login)

    return Response(
        content=html,
        media_type="text/html",
        headers={
            "Content-Disposition": f'inline; filename="gitcard-{github_login}-{card_id}.html"',
            "Cache-Control": "public, max-age=86400",  # 24시간
        },
    )

