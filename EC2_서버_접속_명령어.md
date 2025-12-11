# EC2 서버 접속 명령어

## 🖥️ 서버 정보
- **서버 IP**: `3.37.130.140`
- **사용자명**: `ec2-user` (Amazon Linux)
- **PEM 키 파일**: `gitcard.pem`

---

## 📋 Windows PowerShell에서 접속

### 1단계: PEM 키 파일 권한 설정 (최초 1회만)

**PowerShell을 관리자 권한으로 실행** 후:

```powershell
# 한 줄로 실행
icacls "C:\Users\dlckd\OneDrive\바탕 화면\gitcard.pem" /inheritance:r /grant "$($env:USERNAME):R"
```

**또는 두 단계로:**
```powershell
# 첫 번째: 상속된 권한 제거
icacls "C:\Users\dlckd\OneDrive\바탕 화면\gitcard.pem" /inheritance:r

# 두 번째: 현재 사용자에게 읽기 권한만 부여
icacls "C:\Users\dlckd\OneDrive\바탕 화면\gitcard.pem" /grant "$($env:USERNAME):R"
```

⚠️ **권한을 설정하지 않으면 "UNPROTECTED PRIVATE KEY FILE" 오류 발생!**

---

### 2단계: EC2 서버 접속

**PowerShell에서:**

```powershell
# 절대 경로 사용 (권장)
ssh -i "C:\Users\dlckd\OneDrive\바탕 화면\gitcard.pem" ec2-user@3.37.130.140
```

**또는 현재 위치가 바탕 화면일 때:**
```powershell
ssh -i "gitcard.pem" ec2-user@3.37.130.140
```

---

## 🐧 Mac/Linux에서 접속

### 1단계: PEM 키 파일 권한 설정 (최초 1회만)

```bash
chmod 400 ~/.ssh/gitcard.pem
```

### 2단계: EC2 서버 접속

```bash
ssh -i ~/.ssh/gitcard.pem ec2-user@3.37.130.140
```

---

## 📁 접속 후 프로젝트 디렉토리로 이동

```bash
cd /var/www/GitCard
```

---

## 🔧 가상환경 활성화

```bash
# 프로젝트 디렉토리로 이동
cd /var/www/GitCard

# 가상환경 활성화
source venv/bin/activate

# 확인: 프롬프트에 (venv)가 나타나야 함
```

---

## ✅ 접속 확인 명령어

접속 후 다음 명령어로 확인:

```bash
# 현재 위치 확인
pwd
# 출력: /home/ec2-user

# 프로젝트 디렉토리로 이동
cd /var/www/GitCard

# 가상환경 활성화
source venv/bin/activate

# Python 경로 확인
which python
# 출력: /var/www/GitCard/venv/bin/python

# 서버 상태 확인
curl http://localhost:8000/health
# 출력: {"status":"healthy"}
```

---

## 🚪 서버에서 나가기

```bash
# 가상환경 비활성화 (선택사항)
deactivate

# SSH 연결 종료
exit
```

---

## 🔍 문제 해결

### "Permission denied" 오류

1. PEM 키 파일 권한 확인:
   ```powershell
   # Windows
   icacls "C:\Users\dlckd\OneDrive\바탕 화면\gitcard.pem"
   ```

2. 서버의 authorized_keys 확인:
   ```bash
   # 서버에 접속한 후
   cat ~/.ssh/authorized_keys
   ```

### "UNPROTECTED PRIVATE KEY FILE" 오류

Windows에서 PEM 키 파일 권한을 설정해야 합니다:
```powershell
icacls "C:\Users\dlckd\OneDrive\바탕 화면\gitcard.pem" /inheritance:r /grant "$($env:USERNAME):R"
```

### "Host key verification failed" 오류

```bash
# known_hosts에서 해당 호스트 제거
ssh-keygen -R 3.37.130.140
```

---

## 💡 빠른 접속 (별칭 설정)

**Windows PowerShell 프로필에 추가:**

```powershell
# 프로필 파일 열기
notepad $PROFILE

# 다음 내용 추가
function Connect-EC2 {
    ssh -i "C:\Users\dlckd\OneDrive\바탕 화면\gitcard.pem" ec2-user@3.37.130.140
}

# 저장 후 PowerShell 재시작
```

**사용:**
```powershell
Connect-EC2
```

**Mac/Linux ~/.bashrc 또는 ~/.zshrc에 추가:**

```bash
alias ec2='ssh -i ~/.ssh/gitcard.pem ec2-user@3.37.130.140'
```

**사용:**
```bash
ec2
```
