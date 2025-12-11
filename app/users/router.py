"""
User router for user-related endpoints.

Endpoints:
- GET /api/users/me: Get current user information
- GET /api/users/me/github-stats: Get GitHub statistics for current user
"""
from fastapi import APIRouter, Depends, HTTPException
from app.auth.dependencies import get_current_user
from app.auth.db_models import User
from app.users import github_stats

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/me")
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """
    Get current authenticated user's information.

    Returns:
        User information including GitHub profile data
    """
    # Convert datetime to ISO format strings for JSON serialization
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
    Get GitHub statistics for current authenticated user.
    
    Uses OAuth token if available for higher rate limits (5,000/hour vs 60/hour).
    
    Returns:
        GitHub statistics including repositories, stars, followers, following, contributions
    """
    if not current_user.github_login:
        raise HTTPException(
            status_code=404,
            detail="GitHub username not found"
        )
    
    # Use stored access token if available (increases rate limit from 60 to 5,000/hour)
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

