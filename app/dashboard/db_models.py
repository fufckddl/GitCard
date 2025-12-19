"""
SQLAlchemy models for visitor statistics.
"""
from sqlalchemy import Column, Integer, Date, DateTime, func
from sqlalchemy.sql import func
from app.database import Base


class VisitorStats(Base):
    """Visitor statistics model for database."""
    
    __tablename__ = "visitor_stats"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date = Column(Date, unique=True, index=True, nullable=False)
    visitors = Column(Integer, default=0, nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

