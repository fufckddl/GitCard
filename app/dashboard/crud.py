"""
방문자 통계에 대한 CRUD 작업.
"""
from datetime import date, datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.dashboard.db_models import VisitorStats


def increment_visitor_count(db: Session) -> VisitorStats:
    """
    오늘의 방문자 수를 증가시킵니다.
    오늘의 레코드가 없으면 카운트 1로 새 레코드를 생성합니다.
    레코드가 있으면 카운트를 증가시킵니다.
    
    Returns:
        VisitorStats: 업데이트되거나 생성된 방문자 통계 레코드
    """
    today = date.today()
    
    # 오늘의 레코드 가져오기 시도
    stats = db.query(VisitorStats).filter(VisitorStats.date == today).first()
    
    if stats:
        # 기존 카운트 증가
        stats.visitors += 1
        stats.updated_at = datetime.now()
    else:
        # 오늘을 위한 새 레코드 생성
        stats = VisitorStats(date=today, visitors=1)
        db.add(stats)
    
    db.commit()
    db.refresh(stats)
    return stats


def get_today_visitors(db: Session) -> int:
    """
    오늘의 방문자 수를 가져옵니다.
    
    Returns:
        int: 오늘의 방문자 수 (레코드가 없으면 0)
    """
    today = date.today()
    stats = db.query(VisitorStats).filter(VisitorStats.date == today).first()
    return stats.visitors if stats else 0


def get_total_visitors(db: Session) -> int:
    """
    모든 날짜에 걸친 총 방문자 수를 가져옵니다.
    
    Returns:
        int: 총 방문자 수
    """
    result = db.query(func.sum(VisitorStats.visitors)).scalar()
    return int(result) if result else 0


def get_visitor_stats(db: Session) -> dict:
    """
    오늘의 방문자 수와 총 방문자 수를 모두 가져옵니다.
    
    Returns:
        dict: {
            "today_visitors": int,
            "total_visitors": int
        }
    """
    return {
        "today_visitors": get_today_visitors(db),
        "total_visitors": get_total_visitors(db)
    }


