# GitHub Secrets 설정 방법

## 📍 정확한 경로

1. GitHub 저장소 페이지로 이동
2. 상단 메뉴에서 **Settings** 클릭
3. 왼쪽 사이드바에서 **Security** 섹션 찾기
4. **Secrets and variables** 클릭
5. **Actions** 탭 클릭 (기본으로 선택되어 있을 수 있음)
6. **New repository secret** 버튼 클릭

## 🔑 추가할 3개의 Secrets

각각 "New repository secret" 버튼을 눌러 추가:

### 1. SSH_PRIVATE_KEY
- **Name**: `SSH_PRIVATE_KEY`
- **Secret**: SSH 개인 키 전체 내용 (-----BEGIN RSA PRIVATE KEY----- 부터 -----END RSA PRIVATE KEY----- 까지)

### 2. SSH_USER
- **Name**: `SSH_USER`
- **Secret**: 서버 사용자명 (예: `ubuntu`, `root`)

### 3. SSH_HOST
- **Name**: `SSH_HOST`
- **Secret**: 서버 IP 주소 또는 도메인 (예: `123.45.67.89` 또는 `api.yourdomain.com`)

## 📸 스크린샷 가이드

```
GitHub 저장소
  └─ Settings (상단 메뉴)
      └─ Security (왼쪽 사이드바)
          └─ Secrets and variables
              └─ Actions 탭
                  └─ New repository secret 버튼
```

## ⚠️ 주의사항

- Secrets는 한 번 저장하면 다시 볼 수 없습니다
- 잘못 입력했다면 삭제 후 다시 추가하세요
- SSH_PRIVATE_KEY는 전체 내용을 복사해야 합니다 (줄바꿈 포함)

