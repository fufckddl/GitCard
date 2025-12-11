#!/bin/bash

# 서버 초기 설정 스크립트
# Ubuntu/Debian 서버에서 한 번만 실행

set -e

echo "🖥️  GitCard 서버 초기 설정을 시작합니다..."

# 시스템 업데이트
echo "📦 시스템 패키지를 업데이트합니다..."
sudo apt update && sudo apt upgrade -y

# 필수 패키지 설치
echo "📥 필수 패키지를 설치합니다..."
sudo apt install -y python3 python3-pip python3-venv nodejs npm nginx mysql-server git

# 프로젝트 디렉토리 생성
echo "📁 프로젝트 디렉토리를 생성합니다..."
sudo mkdir -p /var/www
cd /var/www

# Git 저장소 클론 (GitHub URL로 변경 필요)
echo "📥 프로젝트를 클론합니다..."
# sudo git clone https://github.com/your-username/gitcard.git
# sudo chown -R $USER:$USER /var/www/gitcard
# cd gitcard

echo "✅ 서버 초기 설정이 완료되었습니다!"
echo ""
echo "다음 단계:"
echo "1. cd /var/www/gitcard"
echo "2. .env 파일을 생성하고 환경 변수를 설정하세요"
echo "3. python3 -m venv venv && source venv/bin/activate"
echo "4. pip install -r requirements.txt"
echo "5. npm install"
echo "6. MySQL 데이터베이스를 생성하세요"
echo "7. python init_db.py"
echo "8. sudo systemctl enable gitcard-api && sudo systemctl start gitcard-api"

