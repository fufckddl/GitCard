"""
MySQL root 비밀번호 찾기 스크립트
여러 일반적인 비밀번호를 시도합니다.
"""
import pymysql
import sys

# 시도할 비밀번호 목록
passwords_to_try = [
    "",  # 빈 비밀번호
    "password",
    "root",
    "1234",
    "admin",
    "mysql",
    "123456",
    "qwerty",
    "Password123",
    "root123",
]

def test_password(password):
    """비밀번호 테스트"""
    try:
        conn = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password=password,
            database='gitcard',
            connect_timeout=3
        )
        conn.close()
        return True
    except:
        return False

print("=" * 60)
print("MySQL root 비밀번호 찾기")
print("=" * 60)
print("\n일반적인 비밀번호들을 시도 중...\n")

for pwd in passwords_to_try:
    pwd_display = pwd if pwd else "(빈 비밀번호)"
    print(f"시도 중: {pwd_display}...", end=" ")
    
    if test_password(pwd):
        print("✓ 성공!")
        print("\n" + "=" * 60)
        print(f"✓ MySQL root 비밀번호는 '{pwd_display}'입니다!")
        print("=" * 60)
        print(f"\n.env 파일의 DATABASE_URL을 다음과 같이 수정하세요:")
        print(f"DATABASE_URL=mysql+pymysql://root:{pwd}@localhost:3306/gitcard")
        sys.exit(0)
    else:
        print("✗ 실패")

print("\n" + "=" * 60)
print("✗ 일반적인 비밀번호로 연결할 수 없습니다.")
print("=" * 60)
print("\n다음 방법을 시도해보세요:")
print("\n1. MySQL Workbench나 다른 도구로 직접 연결 시도")
print("2. MySQL 명령줄에서 확인:")
print("   mysql -u root -p")
print("3. 비밀번호를 재설정:")
print("   - MySQL 서비스 중지")
print("   - --skip-grant-tables 옵션으로 시작")
print("   - ALTER USER 'root'@'localhost' IDENTIFIED BY '새비밀번호';")
print("\n또는 .env 파일에 올바른 비밀번호를 직접 입력하세요.")




