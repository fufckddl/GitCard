"""
간단한 MySQL 비밀번호 확인 스크립트
"""
import sys
import os

# 가상환경 경로 확인
venv_path = os.path.join(os.getcwd(), 'venv', 'Scripts', 'python.exe')
if os.path.exists(venv_path):
    sys.executable = venv_path

try:
    import pymysql
    
    # config.py에서 비밀번호 추출
    password = "password"  # config.py 기본값
    
    print("=" * 50)
    print("MySQL root 비밀번호 확인")
    print("=" * 50)
    print(f"\n시도할 비밀번호: '{password}' (config.py 기본값)")
    print("\n연결 테스트 중...")
    
    try:
        connection = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password=password,
            database='mysql',
            connect_timeout=3
        )
        connection.close()
        print(f"\n✓ 성공! MySQL root 비밀번호는 '{password}'입니다.")
        print(f"\n현재 설정된 DATABASE_URL:")
        print(f"mysql+pymysql://root:{password}@localhost:3306/gitcard")
    except pymysql.Error as e:
        print(f"\n✗ '{password}'로 연결 실패: {e}")
        print("\n다른 비밀번호를 시도하거나 다음 방법을 사용하세요:")
        print("1. .env 파일에 DATABASE_URL 설정")
        print("2. MySQL Workbench로 직접 연결 시도")
        print("3. MySQL 서비스 관리자에서 확인")
        
except ImportError:
    print("pymysql이 설치되어 있지 않습니다.")
    print("\n현재 설정된 비밀번호 (config.py 기본값): 'password'")
    print("\n비밀번호를 확인하려면:")
    print("1. 가상환경 활성화: .\\venv\\Scripts\\Activate.ps1")
    print("2. pymysql 설치: pip install pymysql")
    print("3. 이 스크립트 다시 실행: python check_mysql_simple.py")
    print("\n또는 MySQL Workbench나 다른 도구로 직접 연결을 시도해보세요.")




