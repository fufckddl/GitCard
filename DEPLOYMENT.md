# GitCard 서버 배포 가이드

이 문서는 GitCard 프로젝트를 프로덕션 서버에 배포하고 CI/CD를 설정하는 방법을 설명합니다.

## 목차
1. [서버 환경 준비](#서버-환경-준비)
2. [수동 배포 방법](#수동-배포-방법)
3. [CI/CD 자동 배포 설정](#cicd-자동-배포-설정)
4. [환경 변수 설정](#환경-변수-설정)
5. [데이터베이스 마이그레이션](#데이터베이스-마이그레이션)
6. [모니터링 및 로그](#모니터링-및-로그)

---

## 서버 환경 준비

### 필수 요구사항
- **운영체제**: Ubuntu 20.04+ / CentOS 7+ / Debian 10+
- **Python**: 3.10 이상
- **Node.js**: 18.x 이상
- **MySQL**: 8.0 이상
- **Nginx**: 웹 서버 및 리버스 프록시
- **Git**: 버전 관리

### 서버 초기 설정

```bash
# 시스템 업데이트
sudo apt update && sudo apt upgrade -y

# 필수 패키지 설치
sudo apt install -y python3 python3-pip python3-venv nodejs npm nginx mysql-server git

# MySQL 설치 확인
sudo mysql_secure_installation
```

---

## 수동 배포 방법

### 1. 프로젝트 클론

```bash
# 서버에 프로젝트 디렉토리 생성
cd /var/www
sudo git clone https://github.com/your-username/gitcard.git
sudo chown -R $USER:$USER /var/www/gitcard
cd gitcard
```

### 2. 백엔드 설정

```bash
# Python 가상환경 생성 및 활성화
python3 -m venv venv
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정 (.env 파일 생성)
cp .env.example .env
nano .env  # 환경 변수 편집
```

### 3. 프론트엔드 빌드

```bash
# Node.js 의존성 설치
npm install

# 프로덕션 빌드
npm run build

# 빌드된 파일은 dist/ 디렉토리에 생성됩니다
```

### 4. 데이터베이스 설정

```bash
# MySQL 데이터베이스 생성
sudo mysql -u root -p
```

```sql
CREATE DATABASE gitcard CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'gitcard_user'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON gitcard.* TO 'gitcard_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

```bash
# 데이터베이스 테이블 초기화
python init_db.py
```

### 5. 백엔드 서비스 설정 (systemd)

```bash
# systemd 서비스 파일 생성
sudo nano /etc/systemd/system/gitcard-api.service
```

```ini
[Unit]
Description=GitCard API Service
After=network.target mysql.service

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/gitcard
Environment="PATH=/var/www/gitcard/venv/bin"
ExecStart=/var/www/gitcard/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# 서비스 활성화 및 시작
sudo systemctl daemon-reload
sudo systemctl enable gitcard-api
sudo systemctl start gitcard-api
sudo systemctl status gitcard-api
```

### 6. Nginx 설정

```bash
# Nginx 설정 파일 생성
sudo nano /etc/nginx/sites-available/gitcard
```

```nginx
# API 서버 (백엔드)
server {
    listen 80;
    server_name api.yourdomain.com;  # 또는 IP 주소

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# 프론트엔드 서버
server {
    listen 80;
    server_name yourdomain.com;  # 또는 IP 주소
    root /var/www/gitcard/dist;
    index index.html;

    # SPA 라우팅 지원
    location / {
        try_files $uri $uri/ /index.html;
    }

    # 정적 파일 캐싱
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

```bash
# 심볼릭 링크 생성 및 Nginx 재시작
sudo ln -s /etc/nginx/sites-available/gitcard /etc/nginx/sites-enabled/
sudo nginx -t  # 설정 테스트
sudo systemctl restart nginx
```

### 7. SSL 인증서 설정 (Let's Encrypt)

```bash
# Certbot 설치
sudo apt install certbot python3-certbot-nginx

# SSL 인증서 발급
sudo certbot --nginx -d yourdomain.com -d api.yourdomain.com

# 자동 갱신 설정
sudo certbot renew --dry-run
```

---

## CI/CD 자동 배포 설정

GitHub Actions를 사용하여 코드 푸시 시 자동으로 서버에 배포되도록 설정합니다.

### 1. GitHub Actions 워크플로우 생성

`.github/workflows/deploy.yml` 파일을 생성합니다:

```yaml
name: Deploy to Production

on:
  push:
    branches:
      - main  # main 브랜치에 푸시할 때 자동 배포
  workflow_dispatch:  # 수동 실행도 가능

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Setup SSH
        uses: webfactory/ssh-agent@v0.7.0
        with:
          ssh-private-key: ${{ secrets.SSH_PRIVATE_KEY }}

      - name: Deploy to server
        run: |
          ssh -o StrictHostKeyChecking=no ${{ secrets.SSH_USER }}@${{ secrets.SSH_HOST }} << 'ENDSSH'
            cd /var/www/gitcard
            
            # 최신 코드 가져오기
            git pull origin main
            
            # 백엔드 업데이트
            source venv/bin/activate
            pip install -r requirements.txt
            
            # 프론트엔드 빌드
            npm install
            npm run build
            
            # 데이터베이스 마이그레이션 (필요시)
            python init_db.py
            
            # 백엔드 서비스 재시작
            sudo systemctl restart gitcard-api
            
            # Nginx 재시작 (필요시)
            sudo systemctl reload nginx
            
            echo "Deployment completed successfully!"
          ENDSSH
```

### 2. GitHub Secrets 설정

GitHub 저장소의 Settings → Secrets and variables → Actions에서 다음 secrets를 추가합니다:

- `SSH_PRIVATE_KEY`: 서버 접속용 SSH 개인 키
- `SSH_USER`: 서버 사용자명 (예: `ubuntu`, `root`)
- `SSH_HOST`: 서버 IP 주소 또는 도메인

### 3. SSH 키 생성 및 설정

**로컬에서 SSH 키 생성:**

```bash
ssh-keygen -t rsa -b 4096 -C "github-actions"
# 파일명: github_actions_deploy (기본값 사용 가능)
```

**서버에 공개 키 추가:**

```bash
# 서버에 접속
ssh user@your-server-ip

# authorized_keys에 공개 키 추가
mkdir -p ~/.ssh
echo "YOUR_PUBLIC_KEY_CONTENT" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
chmod 700 ~/.ssh
```

**GitHub Secrets에 개인 키 추가:**

```bash
# 로컬에서 개인 키 내용 복사
cat ~/.ssh/github_actions_deploy
# 또는
cat ~/.ssh/id_rsa
```

복사한 내용을 GitHub Secrets의 `SSH_PRIVATE_KEY`에 추가합니다.

### 4. 고급 CI/CD 설정 (테스트 포함)

더 안전한 배포를 위해 테스트를 포함한 워크플로우:

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      mysql:
        image: mysql:8.0
        env:
          MYSQL_ROOT_PASSWORD: test_password
          MYSQL_DATABASE: gitcard_test
        ports:
          - 3306:3306
        options: --health-cmd="mysqladmin ping" --health-interval=10s --health-timeout=5s --health-retries=3

    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      
      - name: Run tests
        env:
          DATABASE_URL: mysql+pymysql://root:test_password@localhost:3306/gitcard_test
        run: |
          # 테스트 실행 (pytest 등)
          # pytest tests/
          echo "Tests would run here"
      
      - name: Lint with ESLint
        run: |
          npm install
          npm run lint

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Setup SSH
        uses: webfactory/ssh-agent@v0.7.0
        with:
          ssh-private-key: ${{ secrets.SSH_PRIVATE_KEY }}

      - name: Deploy to server
        run: |
          ssh -o StrictHostKeyChecking=no ${{ secrets.SSH_USER }}@${{ secrets.SSH_HOST }} << 'ENDSSH'
            set -e  # 에러 발생 시 중단
            
            cd /var/www/gitcard
            
            echo "Pulling latest code..."
            git pull origin main
            
            echo "Updating backend..."
            source venv/bin/activate
            pip install -r requirements.txt
            
            echo "Building frontend..."
            npm ci  # package-lock.json 기반 설치
            npm run build
            
            echo "Running database migrations..."
            python init_db.py
            
            echo "Restarting services..."
            sudo systemctl restart gitcard-api
            sudo systemctl reload nginx
            
            echo "✅ Deployment completed successfully!"
          ENDSSH
```

---

## 환경 변수 설정

### 서버의 .env 파일

```bash
# GitHub OAuth
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret
GITHUB_REDIRECT_URI=https://api.yourdomain.com/auth/github/callback

# JWT
JWT_SECRET=your_very_secure_random_secret_key_here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# Frontend
FRONTEND_BASE_URL=https://yourdomain.com

# API
API_BASE_URL=https://api.yourdomain.com

# Database
DATABASE_URL=mysql+pymysql://gitcard_user:your_secure_password@localhost:3306/gitcard
```

### 프론트엔드 환경 변수

프로덕션 빌드 시 환경 변수를 설정하려면 `.env.production` 파일을 생성하거나 빌드 시 지정:

```bash
# .env.production 파일 생성
echo "VITE_API_BASE_URL=https://api.yourdomain.com" > .env.production

# 또는 빌드 시 직접 지정
VITE_API_BASE_URL=https://api.yourdomain.com npm run build
```

---

## 데이터베이스 마이그레이션

### 자동 마이그레이션

`init_db.py`는 기존 테이블이 있으면 건너뛰므로 안전하게 실행 가능합니다:

```bash
python init_db.py
```

### 수동 마이그레이션 (필요시)

```bash
# MySQL 접속
mysql -u gitcard_user -p gitcard

# 스키마 확인
SHOW TABLES;
DESCRIBE users;
DESCRIBE profile_cards;
```

---

## 모니터링 및 로그

### 백엔드 로그 확인

```bash
# 실시간 로그 확인
sudo journalctl -u gitcard-api -f

# 최근 로그 확인
sudo journalctl -u gitcard-api -n 100

# 에러 로그만 확인
sudo journalctl -u gitcard-api -p err
```

### Nginx 로그 확인

```bash
# 액세스 로그
sudo tail -f /var/log/nginx/access.log

# 에러 로그
sudo tail -f /var/log/nginx/error.log
```

### 서비스 상태 확인

```bash
# 백엔드 서비스 상태
sudo systemctl status gitcard-api

# Nginx 상태
sudo systemctl status nginx

# MySQL 상태
sudo systemctl status mysql
```

### 헬스 체크

```bash
# API 헬스 체크
curl http://localhost:8000/health

# 또는 외부에서
curl https://api.yourdomain.com/health
```

---

## 배포 체크리스트

배포 전 확인사항:

- [ ] 서버에 필요한 모든 패키지 설치 완료
- [ ] GitHub OAuth 앱 설정 (프로덕션 URL로 업데이트)
- [ ] 환경 변수 모두 설정 완료
- [ ] 데이터베이스 생성 및 사용자 권한 설정
- [ ] SSL 인증서 발급 및 설정
- [ ] 방화벽 설정 (포트 80, 443, 22 열기)
- [ ] 백엔드 서비스가 정상 실행 중
- [ ] 프론트엔드 빌드 성공
- [ ] Nginx 설정 테스트 통과
- [ ] CI/CD 워크플로우 설정 완료
- [ ] GitHub Secrets 설정 완료

---

## 트러블슈팅

### 백엔드 서비스가 시작되지 않는 경우

```bash
# 로그 확인
sudo journalctl -u gitcard-api -n 50

# 수동 실행하여 에러 확인
cd /var/www/gitcard
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 데이터베이스 연결 오류

```bash
# MySQL 접속 테스트
mysql -u gitcard_user -p -h localhost gitcard

# 연결 문자열 확인
echo $DATABASE_URL
```

### 프론트엔드 빌드 실패

```bash
# Node.js 버전 확인
node --version
npm --version

# 캐시 클리어 후 재설치
rm -rf node_modules package-lock.json
npm install
npm run build
```

---

## 추가 보안 권장사항

1. **방화벽 설정**: UFW 사용
   ```bash
   sudo ufw allow 22/tcp
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   sudo ufw enable
   ```

2. **SSH 보안 강화**: 비밀번호 인증 비활성화, 포트 변경
3. **정기 백업**: 데이터베이스 자동 백업 스크립트 설정
4. **모니터링 도구**: PM2, Supervisor, 또는 systemd 사용
5. **로깅**: 구조화된 로깅 시스템 구축

---

## 참고 자료

- [FastAPI 배포 가이드](https://fastapi.tiangolo.com/deployment/)
- [Nginx 설정 가이드](https://nginx.org/en/docs/)
- [GitHub Actions 문서](https://docs.github.com/en/actions)
- [Let's Encrypt 문서](https://letsencrypt.org/docs/)

