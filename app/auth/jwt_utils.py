"""
인증 토큰 생성 및 검증을 위한 JWT 토큰 유틸리티.

토큰 생성 및 검증에 PyJWT를 사용합니다.
"""
from datetime import datetime, timedelta
from typing import Dict, Optional
import jwt
from app.config import settings


def create_jwt_token(user_id: int, github_id: int) -> str:
    """
    인증된 사용자를 위한 JWT 토큰을 생성합니다.
    
    보안 참고:
    - 토큰에는 식별을 위한 user_id와 github_id가 포함됩니다
    - 토큰에는 만료 시간이 있습니다 (기본값: 24시간)
    - 토큰은 JWT_SECRET으로 서명됩니다 (프론트엔드에 노출하지 마세요)
    - 프로덕션에서는 토큰 가로채기를 방지하기 위해 HTTPS를 사용하세요
    
    Args:
        user_id: 내부 사용자 ID
        github_id: GitHub 사용자 ID
        
    Returns:
        인코딩된 JWT 토큰 문자열
    """
    expiration = datetime.utcnow() + timedelta(hours=settings.jwt_expiration_hours)
    
    payload: Dict[str, any] = {
        "user_id": user_id,
        "github_id": github_id,
        "exp": expiration,
        "iat": datetime.utcnow(),  # 발급 시간
    }
    
    token = jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm
    )
    
    return token


def verify_jwt_token(token: str) -> Optional[Dict[str, any]]:
    """
    JWT 토큰을 검증하고 디코딩합니다.
    
    Args:
        token: 검증할 JWT 토큰 문자열
        
    Returns:
        유효하면 디코딩된 페이로드, 그렇지 않으면 None
    """
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm]
        )
        return payload
    except jwt.ExpiredSignatureError:
        # 토큰이 만료됨
        return None
    except jwt.InvalidTokenError:
        # 토큰이 유효하지 않음
        return None

