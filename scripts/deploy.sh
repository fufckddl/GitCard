#!/bin/bash

# GitCard 배포 스크립트
# 사용법: ./scripts/deploy.sh

set -e  # 에러 발생 시 중단

echo "🚀 GitCard 배포를 시작합니다..."

# 현재 디렉토리 확인
if [ ! -f "app/main.py" ]; then
    echo "❌ 오류: app/main.py를 찾을 수 없습니다. 프로젝트 루트에서 실행해주세요."
    exit 1
fi

# 최신 코드 가져오기
echo "📥 최신 코드를 가져옵니다..."
git pull origin main

# 백엔드 업데이트
echo "🔧 백엔드 의존성을 업데이트합니다..."
if [ ! -d "venv" ]; then
    echo "가상환경이 없습니다. 생성 중..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 프론트엔드 빌드
echo "📦 프론트엔드를 빌드합니다..."
npm ci
npm run build

# 데이터베이스 마이그레이션
echo "🗄️ 데이터베이스 마이그레이션을 실행합니다..."
python init_db.py

# 서비스 재시작
echo "🔄 서비스를 재시작합니다..."
sudo systemctl restart gitcard-api
sudo systemctl reload nginx

# 헬스 체크
echo "🏥 헬스 체크를 수행합니다..."
sleep 3
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ 배포가 성공적으로 완료되었습니다!"
    echo "🌐 API: http://localhost:8000"
else
    echo "⚠️  배포는 완료되었지만 헬스 체크에 실패했습니다."
    echo "서비스 로그를 확인해주세요: sudo journalctl -u gitcard-api -n 50"
    exit 1
fi

