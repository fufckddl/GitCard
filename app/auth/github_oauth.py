"""
GitHub OAuth flow implementation.

Handles:
1. Building GitHub authorization URL
2. Exchanging authorization code for access token
3. Fetching user information from GitHub API

SECURITY NOTE:
- Client Secret is NEVER sent to the frontend
- All OAuth operations happen server-side
- We use httpx for secure HTTP requests
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
    Build GitHub OAuth authorization URL.
    
    Args:
        state: Random state value for CSRF protection
        
    Returns:
        Complete GitHub authorization URL
    """
    params = {
        "client_id": settings.github_client_id,
        "redirect_uri": settings.github_redirect_uri,
        "scope": "read:user user:email",  # Request read access to user profile and email
        "state": state,
    }
    
    # Build query string
    query_string = "&".join([f"{k}={v}" for k, v in params.items()])
    return f"{GITHUB_AUTHORIZE_URL}?{query_string}"


async def exchange_code_for_token(code: str) -> Optional[str]:
    """
    Exchange GitHub authorization code for access token.
    
    SECURITY: This happens server-side. Client Secret is never exposed to frontend.
    
    Args:
        code: Authorization code from GitHub callback
        
    Returns:
        Access token if successful, None otherwise
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
                "Accept": "application/json",  # Request JSON response instead of form data
            },
        )
        
        if response.status_code != 200:
            return None
        
        data = response.json()
        return data.get("access_token")


async def fetch_github_user(access_token: str) -> Optional[Dict[str, any]]:
    """
    Fetch user information from GitHub API.
    
    Args:
        access_token: GitHub OAuth access token
        
    Returns:
        User data dictionary if successful, None otherwise
    """
    async with httpx.AsyncClient() as client:
        # Fetch user profile
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
        
        # Optionally fetch user emails to get primary email
        email_response = await client.get(
            GITHUB_USER_EMAILS_API_URL,
            headers={
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/vnd.github.v3+json",
            },
        )
        
        if email_response.status_code == 200:
            emails = email_response.json()
            # Find primary email
            primary_email = next(
                (email["email"] for email in emails if email.get("primary")),
                None
            )
            if primary_email:
                user_data["email"] = primary_email
        
        return user_data

