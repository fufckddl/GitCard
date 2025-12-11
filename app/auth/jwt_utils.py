"""
JWT token utilities for creating and verifying authentication tokens.

Uses PyJWT for token creation and verification.
"""
from datetime import datetime, timedelta
from typing import Dict, Optional
import jwt
from app.config import settings


def create_jwt_token(user_id: int, github_id: int) -> str:
    """
    Create a JWT token for authenticated user.
    
    SECURITY NOTE:
    - Token includes user_id and github_id for identification
    - Token has an expiration time (default: 24 hours)
    - Token is signed with JWT_SECRET (never expose this to frontend)
    - In production, use HTTPS to prevent token interception
    
    Args:
        user_id: Internal user ID
        github_id: GitHub user ID
        
    Returns:
        Encoded JWT token string
    """
    expiration = datetime.utcnow() + timedelta(hours=settings.jwt_expiration_hours)
    
    payload: Dict[str, any] = {
        "user_id": user_id,
        "github_id": github_id,
        "exp": expiration,
        "iat": datetime.utcnow(),  # Issued at
    }
    
    token = jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm
    )
    
    return token


def verify_jwt_token(token: str) -> Optional[Dict[str, any]]:
    """
    Verify and decode a JWT token.
    
    Args:
        token: JWT token string to verify
        
    Returns:
        Decoded payload if valid, None otherwise
    """
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm]
        )
        return payload
    except jwt.ExpiredSignatureError:
        # Token has expired
        return None
    except jwt.InvalidTokenError:
        # Token is invalid
        return None

