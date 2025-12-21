"""
GitHub OAuth 흐름 구현.

처리:
1. GitHub 인증 URL 빌드
2. 인증 코드를 액세스 토큰으로 교환
3. GitHub API에서 사용자 정보 가져오기

보안 참고:
- Client Secret은 절대 프론트엔드로 전송되지 않습니다
- 모든 OAuth 작업은 서버 측에서 수행됩니다
- 안전한 HTTP 요청을 위해 httpx를 사용합니다
"""
import httpx
from typing import Dict, Optional
from app.config import settings


GITHUB_AUTHORIZE_URL = "https://github.com/login/oauth/authorize"
GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
GITHUB_USER_API_URL = "https://api.github.com/user"
GITHUB_USER_EMAILS_API_URL = "https://api.github.com/user/emails"


def build_github_authorize_url(state: str) -> str:
    """
    GitHub OAuth 인증 URL을 빌드합니다.
    
    Args:
        state: CSRF 보호를 위한 랜덤 state 값
        
    Returns:
        완전한 GitHub 인증 URL
    """
    params = {
        "client_id": settings.github_client_id,
        "redirect_uri": settings.github_redirect_uri,
        "scope": "read:user user:email",  # 사용자 프로필 및 이메일에 대한 읽기 액세스 요청
        "state": state,
    }
    
    # 쿼리 문자열 빌드
    query_string = "&".join([f"{k}={v}" for k, v in params.items()])
    return f"{GITHUB_AUTHORIZE_URL}?{query_string}"


async def exchange_code_for_token(code: str) -> Optional[str]:
    """
    GitHub 인증 코드를 액세스 토큰으로 교환합니다.
    
    보안: 이것은 서버 측에서 발생합니다. Client Secret은 절대 프론트엔드에 노출되지 않습니다.
    
    Args:
        code: GitHub 콜백에서 받은 인증 코드
        
    Returns:
        성공하면 액세스 토큰, 그렇지 않으면 None
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            GITHUB_TOKEN_URL,
            json={
                "client_id": settings.github_client_id,
                "client_secret": settings.github_client_secret,
                "code": code,
                "redirect_uri": settings.github_redirect_uri,
            },
            headers={
                "Accept": "application/json",  # 폼 데이터 대신 JSON 응답 요청
            },
        )
        
        if response.status_code != 200:
            return None
        
        data = response.json()
        return data.get("access_token")


async def fetch_github_user(access_token: str) -> Optional[Dict[str, any]]:
    """
    GitHub API에서 사용자 정보를 가져옵니다.
    
    Args:
        access_token: GitHub OAuth 액세스 토큰
        
    Returns:
        성공하면 사용자 데이터 딕셔너리, 그렇지 않으면 None
    """
    async with httpx.AsyncClient() as client:
        # 사용자 프로필 가져오기
        response = await client.get(
            GITHUB_USER_API_URL,
            headers={
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/vnd.github.v3+json",
            },
        )
        
        if response.status_code != 200:
            return None
        
        user_data = response.json()
        
        # 선택적으로 사용자 이메일을 가져와서 기본 이메일 얻기
        email_response = await client.get(
            GITHUB_USER_EMAILS_API_URL,
            headers={
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/vnd.github.v3+json",
            },
        )
        
        if email_response.status_code == 200:
            emails = email_response.json()
            # 기본 이메일 찾기
            primary_email = next(
                (email["email"] for email in emails if email.get("primary")),
                None
            )
            if primary_email:
                user_data["email"] = primary_email
        
        return user_data

