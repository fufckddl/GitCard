# Windows에서 PEM 키 파일 권한 설정

## ⚠️ 오류 메시지
```
WARNING: UNPROTECTED PRIVATE KEY FILE!
Permissions for '...' are too open.
```

이 오류는 PEM 키 파일의 권한이 너무 열려있어서 발생합니다.

## ✅ 해결 방법

### 방법 1: icacls 명령어 사용 (권장)

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

**설명:**
- `/inheritance:r`: 상속된 권한 제거
- `/grant "$($env:USERNAME):R"`: 현재 사용자에게 읽기 권한만 부여
  - PowerShell에서는 `$($env:USERNAME)` 형식을 사용해야 합니다

### 방법 2: 파일 속성에서 설정

1. 파일 탐색기에서 `gitcard.pem` 파일 찾기
2. 우클릭 → **속성** 클릭
3. **보안** 탭 클릭
4. **고급** 버튼 클릭
5. **상속 사용 안 함** 체크
6. **모든 사용자** 제거 (본인 계정만 남기기)
7. 본인 계정의 권한을 **읽기**만 허용

### 방법 3: 파일 탐색기에서 직접 권한 설정

1. `gitcard.pem` 파일 우클릭
2. **속성** → **보안** 탭
3. **편집** 클릭
4. 모든 사용자 제거 (본인 계정만 남기기)
5. 본인 계정의 권한을 **읽기**만 체크
6. **적용** → **확인**

## 🔍 권한 확인

설정 후 권한이 올바른지 확인:

```powershell
icacls "C:\Users\dlckd\OneDrive\바탕 화면\gitcard.pem"
```

출력 예시:
```
C:\Users\dlckd\OneDrive\바탕 화면\gitcard.pem YOUR-USERNAME:(R)
```

`(R)`만 보이면 성공입니다.

## ✅ 접속 테스트

권한 설정 후 다시 접속 시도:

```powershell
ssh -i "C:\Users\dlckd\OneDrive\바탕 화면\gitcard.pem" ec2-user@3.37.130.140
```

성공하면 EC2 인스턴스에 접속됩니다!

## 💡 추가 팁

- 권한 설정은 한 번만 하면 됩니다
- 파일을 다른 위치로 이동하면 다시 설정해야 할 수 있습니다
- OneDrive 동기화 폴더에 있으면 권한이 변경될 수 있으니 주의하세요

