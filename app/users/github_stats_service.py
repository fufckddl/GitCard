"""
Background sync service for GitHub statistics.

주기적으로 GitHub API를 호출하여 각 사용자의 통계를 DB에 저장합니다.
SVG 카드 생성 시에는 이 캐시된 값을 사용합니다.
"""
from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.auth.db_models import User
from app.users.github_stats_db_models import GitHubStats
from app.users import github_stats as github_stats_client


async def sync_user_github_stats(db: Session, user: User) -> Optional[GitHubStats]:
    """단일 사용자에 대한 GitHub 통계를 동기화합니다."""
    stats = await github_stats_client.fetch_github_stats(
        github_login=user.github_login,
        access_token=user.github_access_token,
    )

    if not stats:
        return None

    record = (
        db.query(GitHubStats)
        .filter(GitHubStats.user_id == user.id)
        .one_or_none()
    )

    if record is None:
        record = GitHubStats(user_id=user.id)
        db.add(record)

    record.repositories = stats.get("repositories")
    record.stars = stats.get("stars")
    record.followers = stats.get("followers")
    record.following = stats.get("following")
    record.contributions = stats.get("contributions")
    record.last_synced_at = datetime.utcnow()

    return record


async def sync_all_github_stats_once() -> None:
    """
    모든 사용자에 대해 한 번 GitHub 통계를 동기화합니다.
    - 백그라운드 스케줄러나 수동 호출에서 사용.
    """
    db = SessionLocal()
    try:
        users = db.query(User).all()
        for user in users:
            try:
                await sync_user_github_stats(db, user)
                db.commit()
            except Exception as e:  # 개별 유저 실패는 전체 루프를 막지 않도록
                db.rollback()
                print(f"[GitHubStats] Failed to sync user {user.github_login}: {e}")
    finally:
        db.close()


async def github_stats_background_loop(interval_seconds: int = 3600) -> None:
    """
    백그라운드에서 주기적으로 GitHub 통계를 동기화하는 루프입니다.
    - 앱 시작 시 한 번 태스크로 띄워두고, 꺼지지 않도록 유지합니다.
    """
    import asyncio

    # 서버 기동 직후 잠시 대기 (DB 준비 등)
    await asyncio.sleep(10)

    while True:
        print("[GitHubStats] Starting periodic sync...")
        await sync_all_github_stats_once()
        print("[GitHubStats] Sync completed. Sleeping...")
        await asyncio.sleep(interval_seconds)

