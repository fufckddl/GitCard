# AWS EC2 PEM 키를 GitHub Actions에서 사용하기

## ✅ 가능합니다!

AWS EC2에서 제공받은 PEM 키를 GitHub Actions의 SSH_PRIVATE_KEY로 사용할 수 있습니다.

## 📋 설정 방법

### 1. PEM 키 내용 확인

**Windows에서:**
```powershell
# PowerShell에서
Get-Content "C:\Users\dlckd\OneDrive\바탕 화면\your-key.pem"

# 또는 메모장으로 열기
notepad "C:\Users\dlckd\OneDrive\바탕 화면\your-key.pem"
```

**Mac/Linux에서:**
```bash
cat ~/.ssh/your-key.pem
```

**참고**: `your-key.pem`을 실제 PEM 키 파일 이름으로 변경하세요.

### 2. GitHub Secrets에 추가

1. PEM 키 파일을 열어서 **전체 내용** 복사
   - `-----BEGIN RSA PRIVATE KEY-----` 부터
   - `-----END RSA PRIVATE KEY-----` 까지
   - 줄바꿈 포함해서 모두 복사

2. GitHub → Settings → Secrets → Actions
3. "New repository secret" 클릭
4. Name: `SSH_PRIVATE_KEY`
5. Secret: 복사한 PEM 키 전체 내용 붙여넣기
6. "Add secret" 클릭

### 3. EC2 인스턴스 확인

EC2 인스턴스에 접속하여 authorized_keys 확인:

**Windows PowerShell에서:**
```powershell
# EC2 인스턴스 접속
ssh -i "C:\Users\dlckd\OneDrive\바탕 화면\your-key.pem" ubuntu@your-ec2-ip

# 접속 후 authorized_keys 확인
cat ~/.ssh/authorized_keys

# PEM 키의 공개 키가 없으면 추가
# (일반적으로 EC2는 자동으로 등록되어 있음)
```

**Mac/Linux에서:**
```bash
# EC2 인스턴스 접속
ssh -i ~/.ssh/your-key.pem ubuntu@your-ec2-ip

# authorized_keys 확인
cat ~/.ssh/authorized_keys
```

**참고**: 
- `your-key.pem`을 실제 PEM 키 파일 이름으로 변경
- `your-ec2-ip`를 EC2 인스턴스의 Public IP 또는 Public DNS로 변경
  - 예: `ec2-12-34-56-78.compute-1.amazonaws.com` 또는 `12.34.56.78`
- `ubuntu`는 인스턴스 OS에 따라 다를 수 있음

### 4. GitHub Secrets 나머지 설정

- **SSH_USER**: EC2 인스턴스 사용자명
  - Amazon Linux: `ec2-user`
  - Ubuntu: `ubuntu`
  - Debian: `admin`
  - CentOS: `centos`

- **SSH_HOST**: EC2 인스턴스의 Public IP 또는 Public DNS
  - 예: `ec2-12-34-56-78.compute-1.amazonaws.com`
  - 또는: `12.34.56.78`

## ⚠️ 주의사항

1. **보안**: PEM 키는 절대 공개하지 마세요

2. **권한 설정 (필수!)**: Windows에서 SSH 접속 전 반드시 설정해야 합니다
   
   **PowerShell을 관리자 권한으로 실행** 후:
   ```powershell
   # 첫 번째: 상속된 권한 제거
   icacls "C:\Users\dlckd\OneDrive\바탕 화면\gitcard.pem" /inheritance:r
   
   # 두 번째: 현재 사용자에게 읽기 권한만 부여
   icacls "C:\Users\dlckd\OneDrive\바탕 화면\gitcard.pem" /grant "$($env:USERNAME):R"
   ```
   
   **또는 한 줄로:**
   ```powershell
   icacls "C:\Users\dlckd\OneDrive\바탕 화면\gitcard.pem" /inheritance:r /grant "$($env:USERNAME):R"
   ```
   
   **Mac/Linux**: 
   ```bash
   chmod 400 ~/.ssh/your-key.pem
   ```
   
   ⚠️ **권한을 설정하지 않으면 "UNPROTECTED PRIVATE KEY FILE" 오류 발생!**

3. **백업**: PEM 키는 한 번만 다운로드 가능하므로 안전하게 보관하세요

## 🔍 문제 해결

### "Permission denied" 오류가 나는 경우

```bash
# EC2 인스턴스에서 authorized_keys 확인
cat ~/.ssh/authorized_keys

# 없다면 PEM 키의 공개 키를 추가
# (EC2 콘솔에서 키 페어로 인스턴스를 생성했다면 자동으로 등록됨)
```

### "Host key verification failed" 오류

GitHub Actions 워크플로우에서 `StrictHostKeyChecking=no` 옵션이 이미 설정되어 있어서 문제없습니다.

## ✅ 완료!

이제 `git push origin main` 하면 자동으로 EC2에 배포됩니다!

