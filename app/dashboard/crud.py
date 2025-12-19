"""
CRUD operations for visitor statistics.
"""
from datetime import date, datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.dashboard.db_models import VisitorStats


def increment_visitor_count(db: Session) -> VisitorStats:
    """
    Increment visitor count for today.
    If no record exists for today, create one with count 1.
    If record exists, increment the count.
    
    Returns:
        VisitorStats: The updated or created visitor stats record
    """
    today = date.today()
    
    # Try to get today's record
    stats = db.query(VisitorStats).filter(VisitorStats.date == today).first()
    
    if stats:
        # Increment existing count
        stats.visitors += 1
        stats.updated_at = datetime.now()
    else:
        # Create new record for today
        stats = VisitorStats(date=today, visitors=1)
        db.add(stats)
    
    db.commit()
    db.refresh(stats)
    return stats


def get_today_visitors(db: Session) -> int:
    """
    Get today's visitor count.
    
    Returns:
        int: Today's visitor count (0 if no record exists)
    """
    today = date.today()
    stats = db.query(VisitorStats).filter(VisitorStats.date == today).first()
    return stats.visitors if stats else 0


def get_total_visitors(db: Session) -> int:
    """
    Get total visitor count across all dates.
    
    Returns:
        int: Total visitor count
    """
    result = db.query(func.sum(VisitorStats.visitors)).scalar()
    return int(result) if result else 0


def get_visitor_stats(db: Session) -> dict:
    """
    Get both today's and total visitor counts.
    
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


