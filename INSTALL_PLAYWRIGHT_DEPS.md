# Playwright 시스템 의존성 설치 가이드

## EC2 서버에서 실행

### Amazon Linux 2023에서 설치

```bash
# 1. 프로젝트 디렉토리로 이동
cd /var/www/GitCard

# 2. 가상환경 활성화
source venv/bin/activate

# 3. Playwright 시스템 의존성 설치 (권장)
sudo playwright install-deps

# 4. Chromium 브라우저 설치 (이미 설치되어 있다면 생략)
playwright install chromium
```

### 수동 설치 (playwright install-deps가 작동하지 않는 경우)

Amazon Linux 2023에서는 다음 명령어를 사용:

```bash
# Amazon Linux 2023용 패키지 설치
sudo yum install -y \
  atk \
  cups-libs \
  gtk3 \
  libXScrnSaver \
  alsa-lib \
  libdrm \
  libxkbcommon \
  libxshmfence \
  mesa-libgbm \
  pango \
  cairo \
  libXcomposite \
  libXdamage \
  libXext \
  libXfixes \
  libXrandr \
  libXrender \
  libXtst
```

### 설치 확인

```bash
# Playwright가 제대로 작동하는지 테스트
cd /var/www/GitCard
source venv/bin/activate
python -c "from playwright.sync_api import sync_playwright; p = sync_playwright().start(); browser = p.chromium.launch(); print('Playwright 작동 확인!'); browser.close()"
```

### 서비스 재시작

의존성 설치 후 백엔드 서비스를 재시작:

```bash
sudo systemctl restart gitcard-api
```

### 문제 해결

만약 여전히 에러가 발생한다면:

1. **Playwright 재설치:**
```bash
cd /var/www/GitCard
source venv/bin/activate
pip uninstall playwright -y
pip install playwright
playwright install chromium
playwright install-deps
```

2. **권한 확인:**
```bash
# Playwright 브라우저 경로 확인
ls -la ~/.cache/ms-playwright/
```

3. **로그 확인:**
```bash
sudo journalctl -u gitcard-api -n 50 --no-pager | grep -i playwright
```

