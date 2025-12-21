# 🎴 GitCard

**GitHub 프로필을 아름다운 카드로 만들어주는 서비스**

[![Live Demo](https://img.shields.io/badge/Live%20Demo-www.gitcard.kr-667eea?style=for-the-badge)](https://www.gitcard.kr)
[![License](https://img.shields.io/badge/license-MIT-blue.svg?style=for-the-badge)](LICENSE)

GitCard는 GitHub 프로필을 시각적으로 아름답고 전문적인 프로필 카드로 변환해주는 서비스입니다. README에 삽입하거나 포트폴리오에 활용할 수 있는 다양한 형식의 프로필 카드를 생성할 수 있습니다.

## ✨ 주요 기능

- 🎨 **커스터마이징 가능한 디자인**: 색상, 그라데이션, 레이아웃을 자유롭게 설정
- 📊 **실시간 GitHub 통계**: 기여도, 저장소, 스타, 팔로워 등 자동 업데이트
- 🏷️ **기술 스택 배지**: 다양한 프로그래밍 언어와 프레임워크를 카테고리별로 정리
- 📱 **다양한 형식 지원**: SVG, HTML, 이미지, Markdown 등 다양한 형식으로 내보내기
- 🔗 **연락처 정보**: 이메일, 블로그, SNS 등 다양한 연락처 추가 가능
- 🎯 **백준 온라인 저지 연동**: 백준 프로필과 연동하여 알고리즘 문제 해결 통계 표시
- 🌐 **공개 프로필 페이지**: 독립적인 URL로 프로필 카드 공유 가능

## 🚀 빠른 시작

### 온라인 사용

1. [GitCard 웹사이트](https://www.gitcard.kr)에 접속
2. GitHub 계정으로 로그인
3. 프로필 카드 생성 및 커스터마이징
4. 생성된 카드를 README나 포트폴리오에 삽입

### README에 삽입하기

생성된 프로필 카드를 GitHub README에 삽입하려면:

```markdown
[![GitCard](https://www.gitcard.kr/api/profiles/{username}/{card_id}/image)](https://www.gitcard.kr/{username}/{card_id})
```

또는 SVG 형식으로:

```markdown
![GitCard](https://www.gitcard.kr/api/profiles/{username}/{card_id}/svg)
```

## 📸 예시

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

## 🛠️ 기술 스택

### Frontend
- **React** - 사용자 인터페이스 구축
- **TypeScript** - 타입 안정성
- **Vite** - 빠른 개발 환경
- **Tailwind CSS** - 스타일링

### Backend
- **FastAPI** - 고성능 Python 웹 프레임워크
- **SQLAlchemy** - ORM 및 데이터베이스 관리
- **Pydantic** - 데이터 검증 및 설정 관리
- **JWT** - 인증 및 보안

### 기타
- **GitHub OAuth** - 소셜 로그인
- **Playwright** - 이미지 생성
- **SVG** - 벡터 그래픽 렌더링

## 📖 사용 방법

### 1. 프로필 카드 생성

1. [GitCard](https://www.gitcard.kr)에 접속하여 GitHub로 로그인
2. 대시보드에서 "새 프로필 카드 만들기" 클릭
3. 원하는 정보 입력:
   - 이름 및 태그라인
   - 기술 스택 선택
   - 연락처 정보
   - 색상 및 디자인 설정

### 2. 커스터마이징

- **색상**: 주 색상과 보조 색상을 선택하여 그라데이션 배너 생성
- **기술 스택**: 카테고리별로 기술 스택을 추가하고 정렬 방식 선택
- **레이아웃**: 스택 레이블 언어, 배치 방식 등 세부 설정

### 3. 공유 및 삽입

- **공개 URL**: 독립적인 프로필 페이지 URL 생성
- **README 삽입**: Markdown 코드 복사하여 GitHub README에 삽입
- **이미지**: PNG/JPEG 형식으로 다운로드 가능

## 🤝 기여하기

GitCard는 오픈소스 프로젝트입니다. 기여를 환영합니다!

1. 이 저장소를 포크합니다
2. 새로운 기능 브랜치를 생성합니다 (`git checkout -b feature/AmazingFeature`)
3. 변경사항을 커밋합니다 (`git commit -m 'Add some AmazingFeature'`)
4. 브랜치에 푸시합니다 (`git push origin feature/AmazingFeature`)
5. Pull Request를 생성합니다

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 🔗 링크

- **웹사이트**: [www.gitcard.kr](https://www.gitcard.kr)
- **GitHub 저장소**: [GitHub](https://github.com/fufckddl/GitCard)

---

**GitCard로 당신의 GitHub 프로필을 더욱 돋보이게 만들어보세요!** ✨
