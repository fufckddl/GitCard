# MySQL 데이터베이스 설정 가이드

## 1. MySQL 설치 및 데이터베이스 생성

```sql
-- MySQL에 접속하여 데이터베이스 생성
CREATE DATABASE IF NOT EXISTS gitcard CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## 2. 환경 변수 설정

`.env` 파일에 다음 변수를 추가하세요:

```env
# 기존 환경 변수들...
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/gitcard
```

예시:
```env
DATABASE_URL=mysql+pymysql://root:yourpassword@localhost:3306/gitcard
```

## 3. 패키지 설치

```bash
pip install -r requirements.txt
```

## 4. 데이터베이스 초기화

### 방법 1: Python 스크립트 사용
```bash
python init_db.py
```

### 방법 2: SQL 스크립트 직접 실행
```bash
mysql -u root -p gitcard < database_schema.sql
```

## 5. 애플리케이션 실행

```bash
uvicorn app.main:app --reload
```

애플리케이션이 시작될 때 자동으로 테이블이 생성됩니다 (이미 존재하는 경우 스킵).

## 데이터베이스 스키마

### users 테이블
- `id`: 자동 증가 기본 키
- `github_id`: GitHub 사용자 ID (고유)
- `github_login`: GitHub 사용자명
- `name`: 사용자 이름
- `email`: 이메일 주소
- `avatar_url`: 프로필 이미지 URL
- `html_url`: GitHub 프로필 URL
- `github_access_token`: GitHub OAuth 액세스 토큰 (보안: 프로덕션에서는 암호화 필요)
- `created_at`: 계정 생성 시간
- `last_login_at`: 마지막 로그인 시간

### profile_cards 테이블
- `id`: 자동 증가 기본 키
- `user_id`: 사용자 ID (외래 키, users.id 참조)
- `card_title`: 카드 목록에서 보이는 제목
- `name`: 프로필 이름
- `title`: 프로필 제목
- `tagline`: 태그라인
- `primary_color`: 주요 색상 (hex)
- `gradient`: 그라데이션 문자열
- `show_stacks`: 스택 섹션 표시 여부
- `show_contact`: 연락처 섹션 표시 여부
- `show_github_stats`: GitHub 통계 표시 여부
- `stacks`: 스택 정보 (JSON)
- `contacts`: 연락처 정보 (JSON)
- `created_at`: 생성 시간
- `updated_at`: 수정 시간

## 보안 주의사항

1. **github_access_token**: 프로덕션 환경에서는 반드시 암호화하여 저장해야 합니다.
2. **데이터베이스 비밀번호**: `.env` 파일을 `.gitignore`에 추가하여 버전 관리에서 제외하세요.
3. **연결 풀링**: SQLAlchemy의 연결 풀링이 자동으로 설정되어 있습니다.


