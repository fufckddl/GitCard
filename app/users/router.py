"""
사용자 관련 엔드포인트를 위한 사용자 라우터.

엔드포인트:
- GET /api/users/me: 현재 사용자 정보 가져오기
- GET /api/users/me/github-stats: 현재 사용자의 GitHub 통계 가져오기
"""
from fastapi import APIRouter, Depends, HTTPException
from app.auth.dependencies import get_current_user
from app.auth.db_models import User
from app.users import github_stats

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me")
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """
    현재 인증된 사용자의 정보를 가져옵니다.

    Returns:
        GitHub 프로필 데이터를 포함한 사용자 정보
    """
    # JSON 직렬화를 위해 datetime을 ISO 형식 문자열로 변환
    return {
        "id": current_user.id,
        "github_id": current_user.github_id,
        "github_login": current_user.github_login,
        "name": current_user.name,
        "email": current_user.email,
        "avatar_url": current_user.avatar_url,
        "html_url": current_user.html_url,
        "created_at": current_user.created_at.isoformat() if current_user.created_at else None,
        "last_login_at": current_user.last_login_at.isoformat() if current_user.last_login_at else None,
    }


@router.get("/me/github-stats")
async def get_github_stats(
    current_user: User = Depends(get_current_user)
):
    """
    현재 인증된 사용자의 GitHub 통계를 가져옵니다.
    
    사용 가능한 경우 더 높은 속도 제한(시간당 5,000 vs 60)을 위해 OAuth 토큰을 사용합니다.
    
    Returns:
        저장소, 스타, 팔로워, 팔로잉, 기여도를 포함한 GitHub 통계
    """
    if not current_user.github_login:
        raise HTTPException(
            status_code=404,
            detail="GitHub username not found"
        )
    
    # 사용 가능한 경우 저장된 액세스 토큰 사용 (속도 제한을 시간당 60에서 5,000으로 증가)
    stats = await github_stats.fetch_github_stats(
        current_user.github_login,
        access_token=current_user.github_access_token
    )
    
    if not stats:
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch GitHub statistics"
        )
    
    return stats


@router.get("/me/repositories")
async def get_github_repositories(
    current_user: User = Depends(get_current_user)
):
    """
    현재 인증된 사용자의 모든 GitHub 레포지토리 목록을 가져옵니다.
    페이지네이션을 통해 모든 레포지토리를 반환합니다.
    
    Returns:
        레포지토리 정보 리스트: 각 레포지토리는 name, description, html_url 등을 포함
    """
    if not current_user.github_login:
        raise HTTPException(
            status_code=404,
            detail="GitHub username not found"
        )
    
    # 사용 가능한 경우 저장된 액세스 토큰 사용
    repositories = await github_stats.fetch_github_repositories(
        current_user.github_login,
        access_token=current_user.github_access_token
    )
    
    return {
        "repositories": repositories,
        "count": len(repositories)
    }

