"""
Pydantic Settings를 사용한 애플리케이션 설정.

.env 파일에서 다음을 위한 환경 변수 로드:
- GitHub OAuth 자격 증명 (Client ID, Client Secret, Redirect URI)
- 토큰 서명용 JWT 시크릿
- 로그인 후 리다이렉트용 프론트엔드 기본 URL
"""
from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Optional


class Settings(BaseSettings):
    """
    환경 변수에서 로드된 애플리케이션 설정.
    
    GitHub OAuth에 필요:
    - GITHUB_CLIENT_ID: GitHub Developer Settings에서 가져온 OAuth App의 Client ID
    - GITHUB_CLIENT_SECRET: OAuth App의 Client Secret (프론트엔드에 노출하지 마세요)
    - GITHUB_REDIRECT_URI: GitHub OAuth App 설정에 등록된 콜백 URL
                          GitHub에 구성된 것과 정확히 일치해야 함
    
    이러한 값은 다음에서 얻을 수 있습니다:
    GitHub → Settings → Developer settings → OAuth Apps → Create/Edit OAuth App
    """
    
    # GitHub OAuth 설정
    github_client_id: str
    github_client_secret: str
    github_redirect_uri: str
    
    # JWT 설정
    jwt_secret: str  # JWT 토큰 서명용 시크릿 키
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24  # 토큰 만료 시간 (시간 단위)
    
    # 프론트엔드 설정
    frontend_base_url: str  # 프론트엔드 앱의 기본 URL (예: http://localhost:5173)
    
    # 서버 설정
    api_base_url: str = "http://localhost:8000"
    
    # 데이터베이스 설정
    database_url: str  # 환경 변수에서 로드 (예: mysql+pymysql://username:password@host:port/database_name)
    # 형식: mysql+pymysql://username:password@host:port/database_name
    
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",  # 추가 환경 변수 무시 (예: 프론트엔드용 VITE_API_BASE_URL)
    )


# 전역 설정 인스턴스
settings = Settings()

