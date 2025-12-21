"""
GitHub OAuth 흐름을 위한 인증 라우터.

엔드포인트:
- GET /auth/github/login: GitHub OAuth 흐름 시작
- GET /auth/github/callback: GitHub OAuth 콜백 처리
"""
from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.auth import github_oauth, jwt_utils, storage
from app.auth import crud as auth_crud
from app.database import get_db
from app.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/github/login")
async def github_login():
    """
    GitHub OAuth 로그인 흐름을 시작합니다.
    
    흐름:
    1. CSRF 보호를 위한 랜덤 state 값 생성
    2. state가 포함된 GitHub 인증 URL 빌드
    3. 사용자를 GitHub로 리다이렉트하여 인증
    
    Returns:
        GitHub 인증 페이지로의 302 리다이렉트
    """
    # CSRF 보호를 위한 state 생성
    state = storage.generate_state()
    
    # GitHub 인증 URL 빌드
    auth_url = github_oauth.build_github_authorize_url(state)
    
    # GitHub로 리다이렉트
    return RedirectResponse(url=auth_url, status_code=302)


@router.get("/github/callback")
async def github_callback(
    code: str = Query(..., description="GitHub에서 받은 인증 코드"),
    state: str = Query(..., description="CSRF 보호를 위한 State 매개변수"),
    db: Session = Depends(get_db),
):
    """
    GitHub OAuth 콜백을 처리합니다.
    
    흐름:
    1. state 매개변수 검증 (CSRF 보호)
    2. 인증 코드를 액세스 토큰으로 교환
    3. GitHub API에서 사용자 정보 가져오기
    4. 데이터베이스에 사용자 생성 또는 업데이트
    5. JWT 토큰 생성
    6. 토큰과 함께 프론트엔드로 리다이렉트
    
    Args:
        code: GitHub에서 받은 인증 코드
        state: 검증할 State 매개변수
        
    Returns:
        JWT 토큰이 포함된 프론트엔드 콜백 URL로의 302 리다이렉트
    """
    # state 검증 (CSRF 보호)
    if not storage.validate_state(state):
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired state parameter"
        )
    
    # 인증 코드를 액세스 토큰으로 교환
    access_token = await github_oauth.exchange_code_for_token(code)
    if not access_token:
        raise HTTPException(
            status_code=400,
            detail="Failed to exchange authorization code for access token"
        )
    
    # GitHub에서 사용자 정보 가져오기
    github_user = await github_oauth.fetch_github_user(access_token)
    if not github_user:
        raise HTTPException(
            status_code=400,
            detail="Failed to fetch user information from GitHub"
        )
    
    # 사용자 데이터 추출
    github_id = github_user["id"]
    github_login = github_user["login"]
    name = github_user.get("name")
    email = github_user.get("email")
    avatar_url = github_user.get("avatar_url")
    html_url = github_user.get("html_url")
    
    # 데이터베이스에 사용자 생성 또는 업데이트
    # 보안 참고: 프로덕션에서는 저장 전에 github_access_token을 암호화하세요
    user = auth_crud.create_or_update_user(
        db=db,
        github_id=github_id,
        github_login=github_login,
        name=name,
        email=email,
        avatar_url=avatar_url,
        html_url=html_url,
        github_access_token=access_token,  # API 호출을 위해 액세스 토큰 저장
    )
    
    # JWT 토큰 생성
    jwt_token = jwt_utils.create_jwt_token(
        user_id=user.id,
        github_id=user.github_id
    )
    
    # 토큰과 함께 프론트엔드로 리다이렉트
    frontend_callback_url = f"{settings.frontend_base_url}/auth/callback?token={jwt_token}"
    return RedirectResponse(url=frontend_callback_url, status_code=302)

