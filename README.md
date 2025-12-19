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

<div style="max-width: 900px; margin: 0 auto; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1); font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;">
  <!-- Banner Section -->
  <div style="background: linear-gradient(135deg, #667eea 0%, rgb(106, 104, 240) 100%); padding: 60px 40px; text-align: center; color: white; border-radius: 12px 12px 0 0;">
    <div style="max-width: 800px; margin: 0 auto;">
      <h1 style="font-size: 42px; font-weight: 700; margin: 0 0 16px 0; line-height: 1.2;">Hello World 👋 I'm James!</h1>
      <p style="font-size: 24px; font-weight: 500; margin: 0 0 12px 0; opacity: 0.95;">AI & Full-stack Developer</p>
      <p style="font-size: 18px; margin: 0; opacity: 0.85; font-weight: 400;">Passionate about building amazing things</p>
    </div>
  </div>
  <!-- Stacks Section -->
  <div style="padding: 32px 40px; background: white;">
    <h2 style="font-size: 28px; font-weight: 700; margin: 0 0 24px 0; color: #333;">Stacks</h2>
    <div style="display: flex; flex-direction: column; gap: 24px;">
      <div style="display: flex; flex-direction: column; gap: 12px;">
        <h3 style="font-size: 18px; font-weight: 600; margin: 0; color: #666; text-transform: uppercase; letter-spacing: 0.5px;">frontend</h3>
        <div style="display: flex; flex-wrap: wrap; gap: 12px;">
          <span style="display: inline-block; padding: 8px 16px; border-radius: 20px; font-size: 14px; font-weight: 600; color: white; background-color: #61DAFB; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);">React</span>
          <span style="display: inline-block; padding: 8px 16px; border-radius: 20px; font-size: 14px; font-weight: 600; color: white; background-color: #3178C6; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);">TypeScript</span>
        </div>
      </div>
      <div style="display: flex; flex-direction: column; gap: 12px;">
        <h3 style="font-size: 18px; font-weight: 600; margin: 0; color: #666; text-transform: uppercase; letter-spacing: 0.5px;">backend</h3>
        <div style="display: flex; flex-wrap: wrap; gap: 12px;">
          <span style="display: inline-block; padding: 8px 16px; border-radius: 20px; font-size: 14px; font-weight: 600; color: white; background-color: #339933; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);">Node.js</span>
        </div>
      </div>
    </div>
  </div>
  <!-- Contact Section -->
  <div style="padding: 32px 40px; background: #f8f9fa;">
    <h2 style="font-size: 28px; font-weight: 700; margin: 0 0 24px 0; color: #333;">Contact</h2>
    <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 16px;">
      <a href="mailto:example@gmail.com" target="" rel="" style="display: flex; flex-direction: column; padding: 20px; background: white; border-radius: 12px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); text-decoration: none; color: inherit;">
        <span style="font-size: 14px; font-weight: 600; color: #667eea; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px;">Gmail</span>
        <span style="font-size: 16px; color: #333; word-break: break-word;">example@gmail.com</span>
      </a>
      <a href="mailto:https://velog.io/@username" target=""_blank"" rel="noopener noreferrer" style="display: flex; flex-direction: column; padding: 20px; background: white; border-radius: 12px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); text-decoration: none; color: inherit;">
        <span style="font-size: 14px; font-weight: 600; color: #667eea; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px;">Velog</span>
        <span style="font-size: 16px; color: #333; word-break: break-word;">https://velog.io/@username</span>
      </a>
    </div>
  </div>
  <!-- GitHub Stats Section -->
  <div style="padding: 32px 40px; background: white;">
    <h2 style="font-size: 28px; font-weight: 700; margin: 0 0 24px 0; color: #333;">Github-stats</h2>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 20px;">
      <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 24px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; color: white; box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);">
        <div style="font-size: 36px; font-weight: 700; margin-bottom: 8px;">-</div>
        <div style="font-size: 14px; font-weight: 500; opacity: 0.9; text-transform: uppercase; letter-spacing: 0.5px;">Contributions</div>
      </div>
      <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 24px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; color: white; box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);">
        <div style="font-size: 36px; font-weight: 700; margin-bottom: 8px;">-</div>
        <div style="font-size: 14px; font-weight: 500; opacity: 0.9; text-transform: uppercase; letter-spacing: 0.5px;">Repositories</div>
      </div>
      <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 24px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; color: white; box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);">
        <div style="font-size: 36px; font-weight: 700; margin-bottom: 8px;">-</div>
        <div style="font-size: 14px; font-weight: 500; opacity: 0.9; text-transform: uppercase; letter-spacing: 0.5px;">Stars</div>
      </div>
      <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 24px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; color: white; box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);">
        <div style="font-size: 36px; font-weight: 700; margin-bottom: 8px;">-</div>
        <div style="font-size: 14px; font-weight: 500; opacity: 0.9; text-transform: uppercase; letter-spacing: 0.5px;">Followers</div>
      </div>
      <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 24px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; color: white; box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);">
        <div style="font-size: 36px; font-weight: 700; margin-bottom: 8px;">-</div>
        <div style="font-size: 14px; font-weight: 500; opacity: 0.9; text-transform: uppercase; letter-spacing: 0.5px;">Following</div>
      </div>
    </div>
    <p style="text-align: center; margin-top: 16px; color: #666; font-size: 14px;">※ GitHub 통계는 <a href="https://gitcard.kr/dashboard/fufckddl/cards/2" target="_blank" rel="noopener noreferrer" style="color: #667eea;">프로필 카드 페이지</a>에서 확인하세요.</p>
  </div>
</div>
