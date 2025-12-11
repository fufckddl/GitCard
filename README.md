# GitCard Backend API

FastAPI 기반 GitHub OAuth 인증 백엔드입니다.

## 설정 방법

1. GitHub OAuth App 생성:
   - GitHub → Settings → Developer settings → OAuth Apps
   - "New OAuth App" 클릭
   - Application name: 원하는 이름
   - Homepage URL: `http://localhost:5173` (프론트엔드 URL)
   - Authorization callback URL: `http://localhost:8000/auth/github/callback`
   - "Register application" 클릭
   - Client ID와 Client Secret 복사

2. 환경 변수 설정:
   ```bash
   cp .env.example .env
   ```
   `.env` 파일을 열어서 실제 값으로 수정:
   - `GITHUB_CLIENT_ID`: GitHub에서 복사한 Client ID
   - `GITHUB_CLIENT_SECRET`: GitHub에서 복사한 Client Secret
   - `JWT_SECRET`: 강력한 랜덤 문자열 (예: `openssl rand -hex 32`)

3. 의존성 설치:
   ```bash
   pip install -r requirements.txt
   ```

4. 서버 실행:
   ```bash
   uvicorn app.main:app --reload
   ```

서버는 `http://localhost:8000`에서 실행됩니다.

API 문서는 `http://localhost:8000/docs`에서 확인할 수 있습니다.

