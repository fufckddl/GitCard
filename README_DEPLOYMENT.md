# 빠른 배포 가이드

## 🚀 CI/CD 자동 배포 설정 (5분 안에 완료)

### 1단계: GitHub Secrets 설정

GitHub 저장소 → Settings → Secrets and variables → Actions에서 다음을 추가:

```
SSH_PRIVATE_KEY: 서버 SSH 개인 키
SSH_USER: 서버 사용자명 (예: ubuntu)
SSH_HOST: 서버 IP 또는 도메인
```

### 2단계: SSH 키 생성 및 설정

**로컬에서:**
```bash
ssh-keygen -t rsa -b 4096 -f ~/.ssh/github_actions_deploy
```

**서버에서:**
```bash
# authorized_keys에 공개 키 추가
cat ~/.ssh/github_actions_deploy.pub >> ~/.ssh/authorized_keys
```

**GitHub에 개인 키 추가:**
```bash
cat ~/.ssh/github_actions_deploy
# 출력된 내용을 GitHub Secrets의 SSH_PRIVATE_KEY에 붙여넣기
```

### 3단계: 코드 푸시

```bash
git add .
git commit -m "Add CI/CD pipeline"
git push origin main
```

**완료!** 이제 `main` 브랜치에 푸시할 때마다 자동으로 배포됩니다.

---

## 📋 수동 배포 체크리스트

서버에서 한 번만 설정:

- [ ] 서버에 프로젝트 클론
- [ ] `.env` 파일 생성 및 환경 변수 설정
- [ ] Python 가상환경 생성 및 의존성 설치
- [ ] Node.js 의존성 설치
- [ ] MySQL 데이터베이스 생성
- [ ] `init_db.py` 실행
- [ ] systemd 서비스 설정
- [ ] Nginx 설정
- [ ] SSL 인증서 발급

자세한 내용은 `DEPLOYMENT.md`를 참고하세요.

---

## 🔄 배포 프로세스

1. **코드 수정** → 로컬에서 작업
2. **커밋 & 푸시** → `git push origin main`
3. **자동 배포** → GitHub Actions가 서버에 배포
4. **서비스 재시작** → 자동으로 재시작됨

---

## 🐛 문제 해결

### 배포 실패 시

1. GitHub Actions 로그 확인
2. 서버 로그 확인: `sudo journalctl -u gitcard-api -n 50`
3. 수동 배포: `./scripts/deploy.sh`

### 서비스가 시작되지 않을 때

```bash
# 로그 확인
sudo journalctl -u gitcard-api -f

# 수동 실행
cd /var/www/gitcard
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

