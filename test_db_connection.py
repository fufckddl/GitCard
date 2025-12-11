"""
데이터베이스 연결 테스트 및 초기화 스크립트
"""
import sys
from app.database import engine, init_db
from sqlalchemy import text

def test_connection():
    """데이터베이스 연결 테스트"""
    try:
        print("=" * 50)
        print("데이터베이스 연결 테스트")
        print("=" * 50)
        
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✓ 데이터베이스 연결 성공!")
            
            # 데이터베이스 이름 확인
            result = connection.execute(text("SELECT DATABASE()"))
            db_name = result.scalar()
            print(f"✓ 현재 데이터베이스: {db_name}")
            
            # 테이블 목록 확인
            result = connection.execute(text("SHOW TABLES"))
            tables = [row[0] for row in result]
            
            if tables:
                print(f"\n✓ 기존 테이블 ({len(tables)}개):")
                for table in tables:
                    print(f"  - {table}")
            else:
                print("\n⚠ 테이블이 없습니다. 초기화가 필요합니다.")
            
            return True
    except Exception as e:
        print(f"\n✗ 데이터베이스 연결 실패: {e}")
        print("\n확인 사항:")
        print("1. MySQL 서비스가 실행 중인지 확인")
        print("2. .env 파일의 DATABASE_URL이 올바른지 확인")
        print("3. 데이터베이스 'gitcard'가 생성되었는지 확인")
        return False

def initialize_tables():
    """테이블 초기화"""
    try:
        print("\n" + "=" * 50)
        print("테이블 초기화 중...")
        print("=" * 50)
        
        init_db()
        print("✓ 테이블 초기화 완료!")
        
        # 초기화 후 테이블 확인
        with engine.connect() as connection:
            result = connection.execute(text("SHOW TABLES"))
            tables = [row[0] for row in result]
            
            if tables:
                print(f"\n✓ 생성된 테이블 ({len(tables)}개):")
                for table in tables:
                    print(f"  - {table}")
            
            # users 테이블 구조 확인
            if 'users' in tables:
                print("\n✓ users 테이블 구조:")
                result = connection.execute(text("DESCRIBE users"))
                for row in result:
                    print(f"  - {row[0]}: {row[1]}")
            
            # profile_cards 테이블 구조 확인
            if 'profile_cards' in tables:
                print("\n✓ profile_cards 테이블 구조:")
                result = connection.execute(text("DESCRIBE profile_cards"))
                for row in result:
                    print(f"  - {row[0]}: {row[1]}")
        
        return True
    except Exception as e:
        print(f"\n✗ 테이블 초기화 실패: {e}")
        return False

if __name__ == "__main__":
    try:
        # 연결 테스트
        if test_connection():
            # 테이블 초기화
            initialize_tables()
            print("\n" + "=" * 50)
            print("✓ 모든 작업이 완료되었습니다!")
            print("=" * 50)
        else:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n작업이 취소되었습니다.")
        sys.exit(0)
    except Exception as e:
        print(f"\n오류 발생: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)




