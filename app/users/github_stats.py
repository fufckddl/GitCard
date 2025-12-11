"""
GitHub statistics fetching utilities.

Fetches GitHub statistics for a user using GitHub API.
Uses OAuth token when available for higher rate limits (5,000/hour vs 60/hour).
"""
import httpx
from typing import Dict, Optional


async def fetch_github_stats(
    github_login: str,
    access_token: Optional[str] = None
) -> Optional[Dict[str, any]]:
    """
    Fetch GitHub statistics for a user.
    
    With OAuth token: 5,000 requests/hour
    Without token: 60 requests/hour
    
    Args:
        github_login: GitHub username
        access_token: Optional GitHub OAuth access token for higher rate limits
        
    Returns:
        Dictionary with stats: repositories, stars, followers, following, contributions
    """
    headers = {
        "Accept": "application/vnd.github.v3+json",
    }
    
    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"
    
    async with httpx.AsyncClient() as client:
        try:
            # Fetch user info (includes public_repos, followers, following)
            user_response = await client.get(
                f"https://api.github.com/users/{github_login}",
                headers=headers,
                timeout=10.0,
            )
            
            if user_response.status_code != 200:
                return None
            
            user_data = user_response.json()
            
            # Fetch all repositories with pagination to count total stars
            total_stars = 0
            page = 1
            per_page = 100
            
            while True:
                repos_response = await client.get(
                    f"https://api.github.com/users/{github_login}/repos",
                    headers=headers,
                    params={
                        "per_page": per_page,
                        "page": page,
                        "sort": "updated",
                    },
                    timeout=10.0,
                )
                
                if repos_response.status_code != 200:
                    break
                
                repos = repos_response.json()
                if not repos:  # No more repos
                    break
                
                total_stars += sum(repo.get("stargazers_count", 0) for repo in repos)
                
                # Check if there are more pages
                if len(repos) < per_page:
                    break
                
                page += 1
            
            # Fetch contributions using GraphQL API (if access_token is available)
            contributions = None
            if access_token:
                contributions = await _fetch_contributions_graphql(access_token, github_login)
            
            return {
                "repositories": user_data.get("public_repos", 0),
                "stars": total_stars,
                "followers": user_data.get("followers", 0),
                "following": user_data.get("following", 0),
                "contributions": contributions,
            }
        except Exception as e:
            print(f"Error fetching GitHub stats: {e}")
            return None


async def _fetch_contributions_graphql(access_token: str, username: str) -> Optional[int]:
    """
    Fetch contribution count using GitHub GraphQL API.
    
    Args:
        access_token: GitHub OAuth access token
        username: GitHub username
        
    Returns:
        Total contributions count or None if failed
    """
    query = """
    query($username: String!) {
      user(login: $username) {
        contributionsCollection {
          totalCommitContributions
          totalIssueContributions
          totalPullRequestContributions
          totalPullRequestReviewContributions
        }
      }
    }
    """
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.github.com/graphql",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/json",
                },
                json={
                    "query": query,
                    "variables": {"username": username},
                },
                timeout=10.0,
            )
            
            if response.status_code != 200:
                return None
            
            data = response.json()
            if "errors" in data:
                return None
            
            contributions = data.get("data", {}).get("user", {}).get("contributionsCollection", {})
            if not contributions:
                return None
            
            total = (
                contributions.get("totalCommitContributions", 0) +
                contributions.get("totalIssueContributions", 0) +
                contributions.get("totalPullRequestContributions", 0) +
                contributions.get("totalPullRequestReviewContributions", 0)
            )
            
            return total
    except Exception as e:
        print(f"Error fetching contributions: {e}")
        return None

