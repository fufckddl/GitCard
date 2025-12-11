# 🚀 GitCard 빠른 배포 가이드

## CI/CD 자동 배포 설정 (5분 완성)

### 1️⃣ GitHub Secrets 설정

1. GitHub 저장소 → **Settings** → **Secrets and variables** → **Actions**
2. 다음 3개의 Secrets 추가:

| Secret 이름 | 설명 | 예시 |
|-----------|------|------|
| `SSH_PRIVATE_KEY` | 서버 SSH 개인 키 | `-----BEGIN RSA PRIVATE KEY-----...` |
| `SSH_USER` | 서버 사용자명 | `ubuntu` 또는 `root` |
| `SSH_HOST` | 서버 주소 | `123.45.67.89` 또는 `api.yourdomain.com` |

### 2️⃣ SSH 키 생성 및 설정

#### 로컬에서 SSH 키 생성

```bash
ssh-keygen -t rsa -b 4096 -f ~/.ssh/github_actions_deploy
# 비밀번호는 입력하지 않아도 됩니다 (엔터 두 번)
```

#### 서버에 공개 키 추가

```bash
# 서버에 접속
ssh user@your-server-ip

# authorized_keys에 공개 키 추가
mkdir -p ~/.ssh
chmod 700 ~/.ssh

# 로컬에서 공개 키 복사
cat ~/.ssh/github_actions_deploy.pub
# 출력된 내용을 복사

# 서버에서 붙여넣기
nano ~/.ssh/authorized_keys
# 복사한 공개 키를 붙여넣고 저장

chmod 600 ~/.ssh/authorized_keys
```

#### GitHub에 개인 키 추가

```bash
# 로컬에서 개인 키 내용 확인
cat ~/.ssh/github_actions_deploy

# 출력된 전체 내용을 복사 (-----BEGIN 부터 -----END 까지)
# GitHub Secrets의 SSH_PRIVATE_KEY에 붙여넣기
```

### 3️⃣ 서버 초기 설정 (한 번만)

```bash
# 서버에 접속
ssh user@your-server-ip

# 프로젝트 디렉토리 생성
sudo mkdir -p /var/www
cd /var/www

# 프로젝트 클론
sudo git clone https://github.com/your-username/gitcard.git
sudo chown -R $USER:$USER /var/www/GitCard
cd GitCard

# Python 가상환경 생성
python3 -m venv venv
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt
npm install

# 환경 변수 설정
cp env.example .env
nano .env  # 환경 변수 편집

# MySQL 데이터베이스 생성
sudo mysql -u root -p
```

MySQL에서:
```sql
CREATE DATABASE gitcard CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'gitcard_user'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON gitcard.* TO 'gitcard_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

```bash
# 데이터베이스 초기화
python init_db.py

# systemd 서비스 설정
sudo nano /etc/systemd/system/gitcard-api.service
```

서비스 파일 내용:
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
# 서비스 활성화
sudo systemctl daemon-reload
sudo systemctl enable gitcard-api
sudo systemctl start gitcard-api
```

### 4️⃣ Nginx 설정

```bash
sudo nano /etc/nginx/sites-available/gitcard
```

설정 내용:
```nginx
# API 서버
server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# 프론트엔드
server {
    listen 80;
    server_name yourdomain.com;
    root /var/www/gitcard/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

```bash
# Nginx 활성화
sudo ln -s /etc/nginx/sites-available/gitcard /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 5️⃣ SSL 인증서 (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d api.yourdomain.com
```

---

## ✅ 완료! 이제 자동 배포가 작동합니다

### 사용 방법

1. **코드 수정** → 로컬에서 작업
2. **커밋 & 푸시**:
   ```bash
   git add .
   git commit -m "Update feature"
   git push origin main
   ```
3. **자동 배포** → GitHub Actions가 자동으로:
   - 최신 코드 가져오기
   - 의존성 업데이트
   - 프론트엔드 빌드
   - 데이터베이스 마이그레이션
   - 서비스 재시작

### 배포 상태 확인

- **GitHub Actions**: 저장소 → Actions 탭에서 배포 진행 상황 확인
- **서버 로그**: `sudo journalctl -u gitcard-api -f`
- **헬스 체크**: `curl https://api.yourdomain.com/health`

---

## 🔧 문제 해결

### 배포가 실패하는 경우

1. **GitHub Actions 로그 확인**
   - 저장소 → Actions → 실패한 워크플로우 클릭
   - 에러 메시지 확인

2. **서버에서 수동 확인**
   ```bash
   ssh user@your-server-ip
   cd /var/www/gitcard
   sudo journalctl -u gitcard-api -n 50
   ```

3. **수동 배포 시도**
   ```bash
   cd /var/www/gitcard
   ./scripts/deploy.sh
   ```

### SSH 연결 오류

```bash
# SSH 키 권한 확인
chmod 600 ~/.ssh/github_actions_deploy
chmod 644 ~/.ssh/github_actions_deploy.pub

# 서버에서 authorized_keys 권한 확인
chmod 600 ~/.ssh/authorized_keys
```

### 서비스가 시작되지 않을 때

```bash
# 로그 확인
sudo journalctl -u gitcard-api -n 100

# 수동 실행하여 에러 확인
cd /var/www/gitcard
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

## 📚 추가 자료

- 상세 가이드: `DEPLOYMENT.md`
- 빠른 참조: `README_DEPLOYMENT.md`

