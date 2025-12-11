"""
Authentication router for GitHub OAuth flow.

Endpoints:
- GET /auth/github/login: Initiates GitHub OAuth flow
- GET /auth/github/callback: Handles GitHub OAuth callback
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
    Initiate GitHub OAuth login flow.
    
    Flow:
    1. Generate a random state value for CSRF protection
    2. Build GitHub authorization URL with state
    3. Redirect user to GitHub for authentication
    
    Returns:
        302 redirect to GitHub authorization page
    """
    # Generate state for CSRF protection
    state = storage.generate_state()
    
    # Build GitHub authorization URL
    auth_url = github_oauth.build_github_authorize_url(state)
    
    # Redirect to GitHub
    return RedirectResponse(url=auth_url, status_code=302)


@router.get("/github/callback")
async def github_callback(
    code: str = Query(..., description="Authorization code from GitHub"),
    state: str = Query(..., description="State parameter for CSRF protection"),
    db: Session = Depends(get_db),
):
    """
    Handle GitHub OAuth callback.
    
    Flow:
    1. Validate state parameter (CSRF protection)
    2. Exchange authorization code for access token
    3. Fetch user information from GitHub API
    4. Create or update user in our database
    5. Generate JWT token
    6. Redirect to frontend with token
    
    Args:
        code: Authorization code from GitHub
        state: State parameter to validate
        
    Returns:
        302 redirect to frontend callback URL with JWT token
    """
    # Validate state (CSRF protection)
    if not storage.validate_state(state):
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired state parameter"
        )
    
    # Exchange code for access token
    access_token = await github_oauth.exchange_code_for_token(code)
    if not access_token:
        raise HTTPException(
            status_code=400,
            detail="Failed to exchange authorization code for access token"
        )
    
    # Fetch user information from GitHub
    github_user = await github_oauth.fetch_github_user(access_token)
    if not github_user:
        raise HTTPException(
            status_code=400,
            detail="Failed to fetch user information from GitHub"
        )
    
    # Extract user data
    github_id = github_user["id"]
    github_login = github_user["login"]
    name = github_user.get("name")
    email = github_user.get("email")
    avatar_url = github_user.get("avatar_url")
    html_url = github_user.get("html_url")
    
    # Create or update user in database
    # SECURITY NOTE: In production, encrypt github_access_token before storing
    user = auth_crud.create_or_update_user(
        db=db,
        github_id=github_id,
        github_login=github_login,
        name=name,
        email=email,
        avatar_url=avatar_url,
        html_url=html_url,
        github_access_token=access_token,  # Store access token for API calls
    )
    
    # Generate JWT token
    jwt_token = jwt_utils.create_jwt_token(
        user_id=user.id,
        github_id=user.github_id
    )
    
    # Redirect to frontend with token
    frontend_callback_url = f"{settings.frontend_base_url}/auth/callback?token={jwt_token}"
    return RedirectResponse(url=frontend_callback_url, status_code=302)

