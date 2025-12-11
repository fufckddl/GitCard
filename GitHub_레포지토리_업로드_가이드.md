# GitHub 레포지토리에 프로젝트 업로드하기

## 📋 사전 준비

1. GitHub 계정이 있어야 합니다
2. GitHub에 새 레포지토리를 생성해야 합니다

## 🚀 단계별 가이드

### 1. GitHub에서 새 레포지토리 생성

1. GitHub 웹사이트 접속: https://github.com
2. 우측 상단 **+** 버튼 클릭 → **New repository**
3. 레포지토리 정보 입력:
   - **Repository name**: `GitCard` (또는 원하는 이름)
   - **Description**: (선택사항) 프로젝트 설명
   - **Public** 또는 **Private** 선택
   - ⚠️ **README, .gitignore, license 추가하지 않기** (이미 있으므로)
4. **Create repository** 클릭

### 2. 로컬 프로젝트를 Git 저장소로 초기화

**프로젝트 폴더에서 PowerShell 또는 Git Bash 실행:**

```powershell
# 현재 디렉토리 확인 (프로젝트 루트여야 함)
cd "C:\Users\dlckd\OneDrive\바탕 화면\명함"

# Git 초기화 (이미 되어있으면 생략)
git init

# 현재 상태 확인
git status
```

### 3. 파일 추가 및 커밋

```powershell
# 모든 파일 추가
git add .

# 첫 커밋
git commit -m "Initial commit: GitCard project"
```

### 4. GitHub 레포지토리와 연결

**GitHub에서 생성한 레포지토리 페이지로 이동하면 보이는 명령어 사용:**

```powershell
# 원격 저장소 추가 (your-username을 실제 사용자명으로 변경)
git remote add origin https://github.com/fufckddl/GitCard.git

# 원격 저장소 확인
git remote -v
```

### 5. GitHub에 푸시

```powershell
# main 브랜치로 푸시
git branch -M main
git push -u origin main
```

**인증 요청 시:**
- GitHub Personal Access Token 사용 (비밀번호 대신)
- 또는 GitHub Desktop 사용

## 🔑 GitHub Personal Access Token 생성

### 방법 1: Personal Access Token 사용

1. GitHub → 우측 상단 프로필 → **Settings**
2. 왼쪽 사이드바 → **Developer settings**
3. **Personal access tokens** → **Tokens (classic)**
4. **Generate new token** → **Generate new token (classic)**
5. 설정:
   - **Note**: `GitCard Local Push`
   - **Expiration**: 원하는 기간 선택
   - **Select scopes**: `repo` 체크
6. **Generate token** 클릭
7. **토큰 복사** (한 번만 보이므로 저장!)

### 푸시 시 토큰 사용

```powershell
git push -u origin main
# Username: fufckddl (또는 GitHub 사용자명)
# Password: [복사한 Personal Access Token 붙여넣기]
```

## ✅ 완료 확인

GitHub 레포지토리 페이지를 새로고침하면 모든 파일이 업로드된 것을 확인할 수 있습니다!

## 🔄 이후 업데이트

코드를 수정한 후:

```powershell
git add .
git commit -m "업데이트 내용 설명"
git push origin main
```

## ⚠️ 주의사항

1. **.env 파일은 업로드하지 않음** (이미 .gitignore에 포함됨)
2. **venv 폴더는 업로드하지 않음** (이미 .gitignore에 포함됨)
3. **node_modules는 업로드하지 않음** (이미 .gitignore에 포함됨)

## 🐛 문제 해결

### "remote origin already exists" 오류

```powershell
# 기존 원격 저장소 제거
git remote remove origin

# 다시 추가
git remote add origin https://github.com/fufckddl/GitCard.git
```

### 인증 오류

- Personal Access Token을 사용하세요 (비밀번호는 더 이상 사용 불가)
- 또는 SSH 키를 사용하세요

### 대용량 파일 오류

```powershell
# .gitignore 확인
cat .gitignore

# 큰 파일이 있다면 .gitignore에 추가
```

