"""
GitHub 통계 가져오기 유틸리티.

GitHub API를 사용하여 사용자의 GitHub 통계를 가져옵니다.
사용 가능한 경우 더 높은 속도 제한(시간당 5,000 vs 60)을 위해 OAuth 토큰을 사용합니다.
"""
import httpx
from typing import Dict, Optional


async def fetch_github_stats(
    github_login: str,
    access_token: Optional[str] = None
) -> Optional[Dict[str, any]]:
    """
    사용자의 GitHub 통계를 가져옵니다.
    
    OAuth 토큰 사용 시: 시간당 5,000 요청
    토큰 없이: 시간당 60 요청
    
    Args:
        github_login: GitHub 사용자명
        access_token: 더 높은 속도 제한을 위한 선택적 GitHub OAuth 액세스 토큰
        
    Returns:
        통계가 포함된 딕셔너리: repositories, stars, followers, following, contributions
    """
    headers = {
        "Accept": "application/vnd.github.v3+json",
    }
    
    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"
    
    async with httpx.AsyncClient() as client:
        try:
            # 사용자 정보 가져오기 (public_repos, followers, following 포함)
            user_response = await client.get(
                f"https://api.github.com/users/{github_login}",
                headers=headers,
                timeout=10.0,
            )
            
            if user_response.status_code != 200:
                return None
            
            user_data = user_response.json()
            
            # 총 스타 수를 계산하기 위해 페이지네이션으로 모든 저장소 가져오기
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
                if not repos:  # 더 이상 저장소 없음
                    break
                
                total_stars += sum(repo.get("stargazers_count", 0) for repo in repos)
                
                # 더 많은 페이지가 있는지 확인
                if len(repos) < per_page:
                    break
                
                page += 1
            
            # GraphQL API를 사용하여 기여도 가져오기 (access_token이 사용 가능한 경우)
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


async def fetch_github_repositories(
    github_login: str,
    access_token: Optional[str] = None
) -> list[Dict[str, any]]:
    """
    사용자의 모든 GitHub 레포지토리 목록을 가져옵니다.
    페이지네이션을 통해 모든 레포지토리를 가져옵니다.
    
    Args:
        github_login: GitHub 사용자명
        access_token: 더 높은 속도 제한을 위한 선택적 GitHub OAuth 액세스 토큰
        
    Returns:
        레포지토리 정보 리스트: 각 레포지토리는 name, description, html_url 등을 포함
    """
    headers = {
        "Accept": "application/vnd.github.v3+json",
    }
    
    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"
    
    repositories = []
    
    try:
        async with httpx.AsyncClient() as client:
            # 페이지네이션을 통해 모든 레포지토리 가져오기
            page = 1
            per_page = 100  # GitHub API 최대값
            
            while True:
                repos_response = await client.get(
                    f"https://api.github.com/users/{github_login}/repos",
                    headers=headers,
                    params={
                        "per_page": per_page,
                        "page": page,
                        "sort": "updated",
                        "direction": "desc",
                    },
                    timeout=10.0,
                )
                
                if repos_response.status_code != 200:
                    break
                
                repos = repos_response.json()
                if not repos:  # 더 이상 레포지토리 없음
                    break
                
                # 필요한 정보만 추출
                for repo in repos:
                    repositories.append({
                        "name": repo.get("name", ""),
                        "description": repo.get("description") or "",
                        "html_url": repo.get("html_url", ""),
                        "language": repo.get("language"),
                        "stargazers_count": repo.get("stargazers_count", 0),
                        "forks_count": repo.get("forks_count", 0),
                        "updated_at": repo.get("updated_at"),
                    })
                
                # 더 많은 페이지가 있는지 확인
                if len(repos) < per_page:
                    break
                
                page += 1
            
            return repositories
    except Exception as e:
        print(f"Error fetching GitHub repositories: {e}")
        return []


async def _fetch_contributions_graphql(access_token: str, username: str) -> Optional[int]:
    """
    GitHub GraphQL API를 사용하여 기여도 수를 가져옵니다.
    
    Args:
        access_token: GitHub OAuth 액세스 토큰
        username: GitHub 사용자명
        
    Returns:
        총 기여도 수 또는 실패 시 None
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

