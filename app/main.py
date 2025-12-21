"""
FastAPI 애플리케이션 진입점.

CORS 설정, 라우터 및 백그라운드 작업이 포함된 메인 애플리케이션 설정.
"""
import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.auth.router import router as auth_router
from app.users.router import router as users_router
from app.profiles.router import router as profiles_router
from app.dashboard.router import router as dashboard_router
from app.config import settings
from app.database import init_db
# Base에 등록되도록 모델 가져오기
from app.auth import db_models  # noqa: F401
from app.profiles import db_models  # noqa: F401
from app.users import github_stats_db_models  # noqa: F401
from app.dashboard import db_models  # noqa: F401
from app.users.github_stats_service import github_stats_background_loop

app = FastAPI(
    title="GitCard API",
    description="Backend API for GitCard application with GitHub OAuth",
    version="1.0.0",
)


@app.on_event("startup")
async def startup_event():
    """시작 시 데이터베이스를 초기화하고 백그라운드 작업을 시작합니다."""
    init_db()
    # GitHub 통계 주기적 동기화 백그라운드 태스크 시작 (기본 1시간 간격)
    asyncio.create_task(github_stats_background_loop())

# CORS 설정
# 프로덕션에서는 프론트엔드 도메인으로 origin을 제한하세요
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.frontend_base_url,
        "http://localhost:5173",  # Vite 기본 개발 서버
        "http://localhost:3000",   # 일반적인 React 개발 서버
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# /api 접두사로 라우터 포함
# 참고: Nginx가 /api 접두사를 제거하는 경우, 라우터는 접두사 없이 등록해야 합니다
# Nginx가 접두사를 제거하지 않는 경우, 여기서 prefix="/api"를 사용하세요
app.include_router(auth_router, prefix="/api")
app.include_router(users_router, prefix="/api")
app.include_router(profiles_router, prefix="/api")
app.include_router(dashboard_router, prefix="/api")


@app.get("/")
async def root():
    """루트 엔드포인트."""
    return {
        "message": "GitCard API",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health")
async def health():
    """헬스 체크 엔드포인트."""
    return {"status": "healthy"}

