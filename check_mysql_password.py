"""
MySQL root 비밀번호 확인 스크립트

여러 일반적인 비밀번호를 시도하여 MySQL root 계정 비밀번호를 확인합니다.
"""
import pymysql
import sys

# 시도할 비밀번호 목록 (일반적인 비밀번호들)
common_passwords = [
    "",  # 빈 비밀번호
    "password",
    "root",
    "1234",
    "admin",
    "mysql",
    "123456",
    "qwerty",
]

def test_connection(password):
    """MySQL 연결 테스트"""
    try:
        connection = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password=password,
            database='mysql',  # 시스템 데이터베이스
            connect_timeout=3
        )
        connection.close()
        return True
    except pymysql.Error as e:
        return False

def main():
    print("MySQL root 비밀번호 확인 중...")
    print("=" * 50)
    
    # config.py에서 기본값 확인
    try:
        from app.config import settings
        if hasattr(settings, 'database_url'):
            db_url = settings.database_url
            if 'mysql+pymysql://' in db_url:
                # URL에서 비밀번호 추출
                parts = db_url.replace('mysql+pymysql://', '').split('@')[0]
                if ':' in parts:
                    _, password_from_config = parts.split(':', 1)
                    print(f"config.py에서 발견된 비밀번호: {password_from_config}")
                    if test_connection(password_from_config):
                        print(f"\n✓ 성공! 비밀번호는 '{password_from_config}'입니다.")
                        return
                    else:
                        print(f"✗ '{password_from_config}'는 올바르지 않습니다.")
    except Exception as e:
        print(f"config.py 읽기 실패: {e}")
    
    # 일반적인 비밀번호들 시도
    print("\n일반적인 비밀번호들을 시도 중...")
    for pwd in common_passwords:
        if test_connection(pwd):
            print(f"\n✓ 성공! 비밀번호는 '{pwd if pwd else '(빈 비밀번호)'}'입니다.")
            return
        else:
            print(f"✗ '{pwd if pwd else '(빈 비밀번호)'}' - 실패")
    
    print("\n✗ 일반적인 비밀번호로 연결할 수 없습니다.")
    print("\n다음 방법을 시도해보세요:")
    print("1. MySQL 서비스가 실행 중인지 확인")
    print("2. .env 파일에 DATABASE_URL 확인")
    print("3. MySQL Workbench나 다른 도구로 직접 연결 시도")
    print("4. 비밀번호를 재설정:")
    print("   - MySQL 서비스 중지")
    print("   - --skip-grant-tables 옵션으로 시작")
    print("   - ALTER USER 'root'@'localhost' IDENTIFIED BY '새비밀번호';")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n작업이 취소되었습니다.")
        sys.exit(0)
    except Exception as e:
        print(f"\n오류 발생: {e}")
        sys.exit(1)




