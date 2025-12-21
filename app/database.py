"""
데이터베이스 연결 및 세션 관리.

SQLAlchemy 엔진, 세션 팩토리 및 데이터베이스 초기화를 처리합니다.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from app.config import settings

# SQLAlchemy 엔진 생성
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,  # 사용 전 연결 확인
    pool_recycle=3600,   # 1시간 후 연결 재활용
    echo=False,          # SQL 쿼리 로깅을 위해 True로 설정
)

# 세션 팩토리 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 모델용 기본 클래스
Base = declarative_base()


def get_db() -> Session:
    """
    데이터베이스 세션을 가져오는 의존성 함수.
    
    FastAPI에서 사용:
        @router.get("/items")
        def get_items(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """데이터베이스 테이블을 초기화합니다."""
    Base.metadata.create_all(bind=engine)





