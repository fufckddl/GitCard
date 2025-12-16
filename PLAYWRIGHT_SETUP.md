# Playwright 설치 가이드

## 문제
이미지 생성 엔드포인트에서 다음 에러가 발생하는 경우:
```
{"detail":"Image generation is not available. Playwright may not be installed."}
```

## 원인
Playwright Python 패키지는 설치되었지만, **브라우저 바이너리가 설치되지 않았습니다**.

## 해결 방법

### 1. 로컬 개발 환경

```bash
# 가상환경 활성화
source venv/bin/activate  # Linux/Mac
# 또는
venv\Scripts\activate  # Windows

# Playwright 브라우저 설치
python -m playwright install chromium

# 또는 모든 브라우저 설치
python -m playwright install
```

### 2. 서버 환경 (Amazon Linux / EC2)

```bash
# SSH로 서버 접속
ssh ec2-user@your-server-ip

# 프로젝트 디렉토리로 이동
cd /var/www/GitCard

# 가상환경 활성화
source venv/bin/activate

# Playwright 브라우저 설치
python -m playwright install chromium

# 시스템 의존성 설치 (Amazon Linux의 경우)
# 참고: 이전에 시도했던 yum install 명령어들이 필요할 수 있습니다
```

### 3. CI/CD 파이프라인에 추가

`.github/workflows/ci.yml`의 deploy 섹션에 추가:

```yaml
- name: Install Playwright browsers
  run: |
    source venv/bin/activate
    python -m playwright install chromium
```

### 4. 설치 확인

```bash
# 브라우저가 설치되었는지 확인
python -m playwright install --dry-run chromium

# 또는 Python에서 직접 확인
python -c "from playwright.sync_api import sync_playwright; p = sync_playwright().start(); p.stop()"
```

## 주의사항

1. **브라우저 바이너리는 대용량입니다** (~300MB)
2. **서버 디스크 공간을 확인**하세요
3. **설치 시간**이 몇 분 걸릴 수 있습니다

## 대안

Playwright 설치가 어려운 경우:
- SVG 엔드포인트 사용 (이미 구현됨)
- 외부 스크린샷 서비스 사용 (예: htmlcsstoimage.com API)
