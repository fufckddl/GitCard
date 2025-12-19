"""
Dashboard router for visitor statistics.

Endpoints:
- GET /dashboard/stats: Get visitor statistics (today and total)
- POST /dashboard/visit: Record a visit (increment today's visitor count)
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.dashboard import crud

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/stats")
async def get_visitor_stats(db: Session = Depends(get_db)):
    """
    Get visitor statistics.
    
    Returns:
        dict: {
            "today_visitors": int,
            "total_visitors": int
        }
    """
    return crud.get_visitor_stats(db)


@router.post("/visit")
async def record_visit(db: Session = Depends(get_db)):
    """
    Record a visit (increment today's visitor count).
    
    Returns:
        dict: {
            "today_visitors": int,
            "total_visitors": int
        }
    """
    crud.increment_visitor_count(db)
    return crud.get_visitor_stats(db)


