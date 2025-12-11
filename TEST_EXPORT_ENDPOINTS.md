# 이미지 및 마크다운 엔드포인트 테스트 가이드

## 가상환경 중첩 문제 확인

프롬프트에 `(venv) (venv)`가 두 번 나타나는 것은 가상환경이 중첩 활성화된 것입니다.

### 확인 방법:
```bash
# 현재 가상환경 경로 확인
echo $VIRTUAL_ENV

# 가상환경 비활성화
deactivate

# 한 번 더 비활성화 (중첩된 경우)
deactivate

# 올바른 가상환경 활성화
cd /var/www/GitCard
source venv/bin/activate
```

### 올바른 상태:
프롬프트가 다음과 같이 나타나야 합니다:
```bash
(venv) [ec2-user@ip-172-31-41-253 GitCard]$
```

---

## 엔드포인트 테스트 방법

### 1. 마크다운 배지 가져오기
```bash
curl http://3.37.130.140/api/profiles/public/fufckddl/cards/1/markdown/badge
```

**예상 결과:**
```
[![GitCard](http://3.37.130.140/dashboard/fufckddl/cards/1)](http://3.37.130.140/dashboard/fufckddl/cards/1)
```

### 2. 전체 마크다운 가져오기
```bash
curl http://3.37.130.140/api/profiles/public/fufckddl/cards/1/markdown
```

**예상 결과:**
```markdown
# 사용자 이름

태그라인

## 제목

### 🛠️ Tech Stack

- 기술 스택 1
- 기술 스택 2

### 📧 Contact

- **이메일**: example@email.com
- **GitHub**: https://github.com/username

---

[![GitCard](http://3.37.130.140/dashboard/fufckddl/cards/1)](http://3.37.130.140/dashboard/fufckddl/cards/1)
```

### 3. 이미지 URL 및 마크다운 정보
```bash
curl http://3.37.130.140/api/profiles/public/fufckddl/cards/1/image-url
```

**예상 결과 (JSON):**
```json
{
  "image_url": "http://3.37.130.140/dashboard/fufckddl/cards/1",
  "markdown_badge": "[![GitCard](http://3.37.130.140/dashboard/fufckddl/cards/1)](http://3.37.130.140/dashboard/fufckddl/cards/1)",
  "html_img": "<img src=\"http://3.37.130.140/dashboard/fufckddl/cards/1\" alt=\"GitCard\" />",
  "markdown_link": "[내 GitCard 보기](http://3.37.130.140/dashboard/fufckddl/cards/1)"
}
```

### 4. 이미지 다운로드 (Playwright 필요)
```bash
# 이미지 다운로드
curl http://3.37.130.140/api/profiles/public/fufckddl/cards/1/image -o card.png

# 또는 크기 지정
curl "http://3.37.130.140/api/profiles/public/fufckddl/cards/1/image?width=1200&height=800" -o card-large.png
```

**주의:** Playwright가 설치되어 있지 않으면 503 에러가 발생합니다.

---

## 브라우저에서 테스트

### 1. 마크다운 배지
브라우저에서 다음 URL 접속:
```
http://3.37.130.140/api/profiles/public/fufckddl/cards/1/markdown/badge
```

### 2. 전체 마크다운
```
http://3.37.130.140/api/profiles/public/fufckddl/cards/1/markdown
```

### 3. 이미지 URL 정보
```
http://3.37.130.140/api/profiles/public/fufckddl/cards/1/image-url
```

### 4. 이미지 (PNG)
```
http://3.37.130.140/api/profiles/public/fufckddl/cards/1/image
```

---

## GitHub README에 사용하기

### 방법 1: 마크다운 배지 사용
1. 브라우저에서 `http://3.37.130.140/api/profiles/public/fufckddl/cards/1/markdown/badge` 접속
2. 표시된 마크다운 코드 복사
3. README.md에 붙여넣기

### 방법 2: 직접 작성
README.md에 다음 코드 추가:
```markdown
[![GitCard](http://3.37.130.140/dashboard/fufckddl/cards/1)](http://3.37.130.140/dashboard/fufckddl/cards/1)
```

---

## Playwright 설치 (이미지 생성용)

이미지 생성 기능을 사용하려면 Playwright를 설치해야 합니다:

```bash
# 가상환경 활성화
cd /var/www/GitCard
source venv/bin/activate

# Playwright 설치
pip install playwright

# Chromium 브라우저 설치
playwright install chromium
```

설치 후 백엔드 서비스를 재시작:
```bash
sudo systemctl restart gitcard-api
```

---

## 문제 해결

### 404 에러가 발생하는 경우
- 카드 ID가 올바른지 확인
- GitHub 로그인이 올바른지 확인
- 백엔드 서버가 실행 중인지 확인: `curl http://localhost:8000/health`

### 503 에러 (이미지 생성)
- Playwright가 설치되어 있는지 확인
- `playwright install chromium` 실행

### 가상환경 문제
- `deactivate` 명령어로 모든 가상환경 비활성화
- 올바른 경로에서 `source venv/bin/activate` 실행
