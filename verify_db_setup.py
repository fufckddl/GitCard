"""
데이터베이스 설정 확인 스크립트
"""
import sys
import os

# 환경 변수 로드
from dotenv import load_dotenv
load_dotenv()

try:
    from app.database import engine, init_db
    from sqlalchemy import text
    
    print("=" * 60)
    print("GitCard 데이터베이스 설정 확인")
    print("=" * 60)
    
    # 1. 연결 테스트
    print("\n[1] 데이터베이스 연결 테스트...")
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT DATABASE()"))
            db_name = result.scalar()
            print(f"   ✓ 연결 성공! 현재 데이터베이스: {db_name}")
    except Exception as e:
        print(f"   ✗ 연결 실패: {e}")
        print("\n   확인 사항:")
        print("   - MySQL 서비스가 실행 중인지 확인")
        print("   - .env 파일의 DATABASE_URL이 올바른지 확인")
        print("   - 데이터베이스 'gitcard'가 생성되었는지 확인")
        sys.exit(1)
    
    # 2. 기존 테이블 확인
    print("\n[2] 기존 테이블 확인...")
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SHOW TABLES"))
            existing_tables = [row[0] for row in result]
            
            if existing_tables:
                print(f"   ✓ 기존 테이블 발견 ({len(existing_tables)}개):")
                for table in existing_tables:
                    print(f"     - {table}")
            else:
                print("   ⚠ 테이블이 없습니다. 초기화가 필요합니다.")
    except Exception as e:
        print(f"   ✗ 오류: {e}")
    
    # 3. 테이블 초기화
    print("\n[3] 테이블 초기화...")
    try:
        init_db()
        print("   ✓ 초기화 완료!")
    except Exception as e:
        print(f"   ✗ 초기화 실패: {e}")
        sys.exit(1)
    
    # 4. 최종 테이블 확인
    print("\n[4] 생성된 테이블 확인...")
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SHOW TABLES"))
            tables = [row[0] for row in result]
            
            if tables:
                print(f"   ✓ 테이블 생성 완료 ({len(tables)}개):")
                for table in tables:
                    print(f"     - {table}")
                    
                    # 테이블 구조 확인
                    result2 = conn.execute(text(f"DESCRIBE {table}"))
                    columns = [row[0] for row in result2]
                    print(f"       컬럼: {', '.join(columns)}")
            else:
                print("   ⚠ 테이블이 생성되지 않았습니다.")
    except Exception as e:
        print(f"   ✗ 오류: {e}")
    
    print("\n" + "=" * 60)
    print("✓ 데이터베이스 설정이 완료되었습니다!")
    print("=" * 60)
    print("\n다음 단계:")
    print("1. FastAPI 서버 시작: uvicorn app.main:app --reload")
    print("2. 브라우저에서 http://localhost:8000/docs 접속하여 API 확인")
    
except ImportError as e:
    print(f"✗ 모듈 import 실패: {e}")
    print("\n필요한 패키지가 설치되었는지 확인하세요:")
    print("  pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"\n✗ 오류 발생: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)




