"""
Profile card export utilities.

Functions to export profile cards as:
- SVG/Markdown format for GitHub README
- Image format (PNG/JPEG)
"""
from typing import Optional, Dict
from io import BytesIO
import html as html_escape
from app.profiles.db_models import ProfileCard
from app.config import settings

# 연락처 타입을 Simple Icons slug로 매핑 (contactMeta.ts와 일치)
CONTACT_ICON_MAP: Dict[str, str] = {
    "mail": "gmail",
    "instagram": "instagram",
    "linkedin": "inspire",
    "velog": "velog",
    "reddit": "reddit",
    "facebook": "facebook",
    "youtube": "youtube",
    "x": "x",
    "thread": "threads",
}

# 스택 키를 Simple Icons slug로 매핑 (stackMeta.ts와 일치)
# src/shared/stackMeta.ts와 동기화를 유지해야 함
STACK_ICON_MAP: Dict[str, str] = {
    # 언어
    "javascript": "javascript",
    "typescript": "typescript",
    "python": "python",
    "java": "openjdk",
    "kotlin": "kotlin",
    "swift": "swift",
    "dart": "dart",
    "c": "c",
    "cpp": "cplusplus",
    "csharp": "csharp",
    "go": "go",
    "rust": "rust",
    "php": "php",
    "ruby": "ruby",
    "scala": "scala",
    "r": "r",
    "shell": "gnubash",
    # 프론트엔드
    "react": "react",
    "nextjs": "nextdotjs",
    "vue": "vuedotjs",
    "nuxt": "nuxtdotjs",
    "svelte": "svelte",
    "angular": "angular",
    "jquery": "jquery",
    "html": "html5",
    "css": "css3",
    "sass": "sass",
    "tailwind": "tailwindcss",
    "bootstrap": "bootstrap",
    "styled-components": "styledcomponents",
    "vite": "vite",
    # Mobile
    "react-native": "react",
    "flutter": "flutter",
    "android": "android",
    "ios": "ios",
    "swiftui": "swift",
    # 백엔드
    "nodejs": "nodedotjs",
    "express": "express",
    "nest": "nestjs",
    "fastapi": "fastapi",
    "django": "django",
    "flask": "flask",
    "spring": "spring",
    "spring-boot": "springboot",
    "laravel": "laravel",
    "ruby-on-rails": "rubyonrails",
    "aspnet": "dotnet",
    "grpc": "grpc",
    # 데이터베이스
    "mysql": "mysql",
    "postgresql": "postgresql",
    "sqlite": "sqlite",
    "mariadb": "mariadb",
    "mongodb": "mongodb",
    "redis": "redis",
    "elasticsearch": "elasticsearch",
    "dynamodb": "amazondynamodb",
    "firebase-firestore": "firebase",
    # 인프라
    # "aws": "amazonaws",  # AWS 아이콘 제거
    "gcp": "googlecloud",
    "azure": "microsoftazure",
    "docker": "docker",
    "kubernetes": "kubernetes",
    "nginx": "nginx",
    "apache": "apache",
    "gitlab-ci": "gitlab",
    "github-actions": "githubactions",
    "jenkins": "jenkins",
    "vercel": "vercel",
    "netlify": "netlify",
    "cloudflare": "cloudflare",
    # 협업 도구
    "git": "git",
    "github": "github",
    "gitlab": "gitlab",
    "bitbucket": "bitbucket",
    "jira": "jira",
    "notion": "notion",
    "slack": "slack",
    "discord": "discord",
    "figma": "figma",
    # AI/ML
    "pandas": "pandas",
    "numpy": "numpy",
    "scikit-learn": "scikitlearn",
    "tensorflow": "tensorflow",
    "pytorch": "pytorch",
    "opencv": "opencv",
    "huggingface": "huggingface",
    # Testing
    "jest": "jest",
    "cypress": "cypress",
    "playwright": "playwright",
    "pytest": "pytest",
    "junit": "junit",
    # 도구
    "webpack": "webpack",
    "rollup": "rollupdotjs",
    "babel": "babel",
    "eslint": "eslint",
    "prettier": "prettier",
    "npm": "npm",
    "yarn": "yarn",
    "pnpm": "pnpm",
}

def _is_light_color(hex_color: str) -> bool:
    """
    hex 색상이 밝은지 어두운지 판단합니다.
    밝으면 True 반환 (검은색 아이콘 사용), 어두우면 False 반환 (흰색 아이콘 사용).
    
    상대 휘도 공식 사용: https://www.w3.org/WAI/GL/wiki/Relative_luminance
    """
    # # 제거 (있는 경우)
    hex_color = hex_color.lstrip('#')
    
    # 3자리 hex를 6자리로 변환
    if len(hex_color) == 3:
        hex_color = ''.join([c * 2 for c in hex_color])
    
    # RGB로 변환
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    
    # 상대 휘도 계산
    # 공식 사용: 0.299*R + 0.587*G + 0.114*B
    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    
    # 휘도가 0.5보다 크면 밝은 색상
    return luminance > 0.5


try:
    from playwright.async_api import async_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

def _check_playwright_browsers() -> bool:
    """Playwright 브라우저가 설치되어 있는지 확인합니다."""
    if not PLAYWRIGHT_AVAILABLE:
        return False
    try:
        import subprocess
        result = subprocess.run(
            ["python", "-m", "playwright", "install", "--dry-run", "chromium"],
            capture_output=True,
            timeout=5
        )
        # dry-run이 성공하면 브라우저가 이미 설치되어 있음
        return result.returncode == 0
    except Exception:
        # 확인이 실패하면 브라우저가 설치되지 않았을 수 있음
        # 하지만 여전히 Playwright를 사용해봄 (작동할 수 있음)
        return True


async def generate_image_url(card: ProfileCard, github_login: str) -> str:
    """
    프로필 카드의 이미지 URL을 생성합니다.
    이미지로 변환할 수 있는 공개 프로필 카드 페이지 URL을 사용합니다.
    
    Args:
        card: ProfileCard 인스턴스
        github_login: GitHub 사용자명
        
    Returns:
        프로필 카드 페이지 URL (스크린샷 서비스와 함께 사용 가능)
    """
    return f"{settings.frontend_base_url}/dashboard/{github_login}/cards/{card.id}"


async def generate_image_screenshot(
    card: ProfileCard, 
    github_login: str,
    format: str = "png",
    width: int = 1200,
    height: int = 700
) -> Optional[bytes]:
    """
    Playwright를 사용하여 프로필 카드 페이지에서 PNG 또는 WebP 이미지를 생성합니다.
    실제 웹 카드 UI를 렌더링하고 카드 컨테이너만 잘라냅니다.
    
    Args:
        card: ProfileCard 인스턴스
        github_login: GitHub 사용자명
        format: 이미지 형식 ("png" 또는 "webp", 기본값: "png")
        width: 뷰포트 너비 (픽셀, 기본값: 1200)
        height: 뷰포트 높이 (픽셀, 기본값: 700)
        
    Returns:
        이미지 바이트 (PNG 또는 WebP), Playwright를 사용할 수 없으면 None
    """
    if not PLAYWRIGHT_AVAILABLE:
        print("Playwright is not installed. Install with: pip install playwright && playwright install chromium")
        return None
    
    if format not in ("png", "webp"):
        format = "png"
    
    try:
        url = f"{settings.frontend_base_url}/dashboard/{github_login}/cards/{card.id}"
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            # 전체 카드가 보이도록 매우 큰 뷰포트 사용, 선명도를 위해 DPR 2
            # 동적 조정 대신 고정된 큰 높이 사용
            page = await browser.new_page(
                viewport={"width": width, "height": 4000},  # 고정된 큰 높이
                device_scale_factor=2
            )
            
            # 결정론적 렌더링을 위해 애니메이션과 전환 비활성화
            await page.add_style_tag(content="""
                * {
                    animation: none !important;
                    transition: none !important;
                }
            """)
            
            # 카드 페이지로 이동
            await page.goto(url, wait_until="networkidle", timeout=30000)
            
            # 카드 컨테이너가 보일 때까지 대기
            card_selector = '[data-testid="gitcard-root"]'
            try:
                await page.wait_for_selector(card_selector, timeout=10000, state="visible")
            except Exception:
                # testid를 찾을 수 없으면 cardWrapper로 대체
                card_selector = ".cardWrapper"
                await page.wait_for_selector(card_selector, timeout=10000, state="visible")
            
            # 모든 리소스가 완전히 로드될 때까지 대기
            await page.wait_for_load_state("networkidle", timeout=30000)
            
            # 폰트 로드 대기
            await page.evaluate("document.fonts.ready")
            await page.wait_for_timeout(500)
            
            # 모든 이미지가 완전히 로드될 때까지 대기
            await page.evaluate("""
                async () => {
                    const images = Array.from(document.images);
                    await Promise.all(
                        images.map(img => {
                            if (img.complete && img.naturalHeight !== 0) {
                                return Promise.resolve();
                            }
                            return new Promise((resolve) => {
                                const timeout = setTimeout(() => resolve(), 10000);
                                img.onload = () => {
                                    clearTimeout(timeout);
                                    resolve();
                                };
                                img.onerror = () => {
                                    clearTimeout(timeout);
                                    resolve(); // Continue even if image fails
                                };
                            });
                        })
                    );
                    // Additional wait to ensure images are fully rendered
                    await new Promise(resolve => setTimeout(resolve, 1000));
                }
            """)
            
            # CSS와 스타일시트 로드 대기
            await page.evaluate("""
                () => {
                    return Promise.all(
                        Array.from(document.styleSheets).map(sheet => {
                            try {
                                if (sheet.cssRules) return Promise.resolve();
                                return new Promise(resolve => {
                                    sheet.onload = resolve;
                                    sheet.onerror = resolve;
                                    setTimeout(resolve, 2000);
                                });
                            } catch (e) {
                                return Promise.resolve();
                            }
                        })
                    );
                }
            """)
            
            # 레이아웃 안정화 대기 (요소 크기가 안정적인지 확인)
            await page.wait_for_timeout(1000)
            
            # 먼저 페이지 상단으로 스크롤
            await page.evaluate("window.scrollTo(0, 0)")
            await page.wait_for_timeout(500)
            
            # 카드 요소 가져오기
            card_element = await page.query_selector(card_selector)
            if not card_element:
                # 대체: 카드 래퍼 찾기 시도
                card_element = await page.query_selector(".cardWrapper")
            
            if card_element:
                # 정확도를 위해 여러 방법을 사용하여 요소의 실제 크기 가져오기
                element_info = await page.evaluate("""
                    (selector) => {
                        const element = document.querySelector(selector);
                        if (!element) return null;
                        
                        // Get bounding rect (relative to viewport)
                        const rect = element.getBoundingClientRect();
                        
                        // Get scroll dimensions (actual content size)
                        const scrollHeight = element.scrollHeight;
                        const scrollWidth = element.scrollWidth;
                        
                        // Get client dimensions (visible area)
                        const clientHeight = element.clientHeight;
                        const clientWidth = element.clientWidth;
                        
                        // Get computed styles for padding/border
                        const styles = window.getComputedStyle(element);
                        const paddingTop = parseFloat(styles.paddingTop) || 0;
                        const paddingBottom = parseFloat(styles.paddingBottom) || 0;
                        const paddingLeft = parseFloat(styles.paddingLeft) || 0;
                        const paddingRight = parseFloat(styles.paddingRight) || 0;
                        const borderTop = parseFloat(styles.borderTopWidth) || 0;
                        const borderBottom = parseFloat(styles.borderBottomWidth) || 0;
                        const borderLeft = parseFloat(styles.borderLeftWidth) || 0;
                        const borderRight = parseFloat(styles.borderRightWidth) || 0;
                        
                        // Calculate total dimensions including padding and border
                        const totalHeight = scrollHeight + paddingTop + paddingBottom + borderTop + borderBottom;
                        const totalWidth = scrollWidth + paddingLeft + paddingRight + borderLeft + borderRight;
                        
                        // Use the maximum of all measurements to ensure we capture everything
                        const finalHeight = Math.max(
                            Math.round(rect.height),
                            Math.round(scrollHeight),
                            Math.round(clientHeight),
                            Math.round(totalHeight)
                        );
                        const finalWidth = Math.max(
                            Math.round(rect.width),
                            Math.round(scrollWidth),
                            Math.round(clientWidth),
                            Math.round(totalWidth)
                        );
                        
                        return {
                            x: Math.round(rect.x),
                            y: Math.round(rect.y),
                            width: finalWidth,
                            height: finalHeight,
                            scrollHeight: scrollHeight,
                            scrollWidth: scrollWidth,
                            pageY: Math.round(rect.y + window.scrollY),
                            pageX: Math.round(rect.x + window.scrollX)
                        };
                    }
                """, card_selector)
                
                if element_info:
                    # 필요한 뷰포트 크기 계산
                    # 잘리지 않도록 여유 공간 추가
                    padding = 50
                    required_height = element_info['pageY'] + element_info['height'] + padding
                    required_width = element_info['pageX'] + element_info['width'] + padding
                    
                    # 최소 뷰포트 크기 보장
                    min_viewport_height = max(required_height, 4000)
                    min_viewport_width = max(required_width, width)
                    
                    # 전체 요소를 수용하도록 뷰포트 크기 조정
                    await page.set_viewport_size({
                        'width': min_viewport_width,
                        'height': min_viewport_height
                    })
                    await page.wait_for_timeout(500)
                    
                    # 새 뷰포트로 올바른 렌더링을 위해 페이지 다시 로드
                    await page.reload(wait_until="networkidle", timeout=30000)
                    
                    # 다시 로드 후 모든 리소스가 완전히 로드될 때까지 대기
                    await page.wait_for_load_state("networkidle", timeout=30000)
                    
                    # 폰트 로드 대기
                    await page.evaluate("document.fonts.ready")
                    await page.wait_for_timeout(500)
                    
                    # 모든 이미지가 완전히 로드될 때까지 대기
                    await page.evaluate("""
                        async () => {
                            const images = Array.from(document.images);
                            await Promise.all(
                                images.map(img => {
                                    if (img.complete && img.naturalHeight !== 0) {
                                        return Promise.resolve();
                                    }
                                    return new Promise((resolve) => {
                                        const timeout = setTimeout(() => resolve(), 10000);
                                        img.onload = () => {
                                            clearTimeout(timeout);
                                            resolve();
                                        };
                                        img.onerror = () => {
                                            clearTimeout(timeout);
                                            resolve();
                                        };
                                    });
                                })
                            );
                            // Additional wait to ensure images are fully rendered
                            await new Promise(resolve => setTimeout(resolve, 1000));
                        }
                    """)
                    
                    # CSS와 스타일시트 대기
                    await page.evaluate("""
                        () => {
                            return Promise.all(
                                Array.from(document.styleSheets).map(sheet => {
                                    try {
                                        if (sheet.cssRules) return Promise.resolve();
                                        return new Promise(resolve => {
                                            sheet.onload = resolve;
                                            sheet.onerror = resolve;
                                            setTimeout(resolve, 2000);
                                        });
                                    } catch (e) {
                                        return Promise.resolve();
                                    }
                                })
                            );
                        }
                    """)
                    
                    # 레이아웃 안정화 대기
                    await page.wait_for_timeout(1500)
                    
                    # 다시 로드 후 업데이트된 위치를 얻기 위해 요소 다시 쿼리
                    card_element = await page.query_selector(card_selector)
                    if not card_element:
                        card_element = await page.query_selector(".cardWrapper")
                    
                    if card_element:
                        # 업데이트된 요소 위치 가져오기
                        updated_element_info = await page.evaluate("""
                            (selector) => {
                                const element = document.querySelector(selector);
                                if (!element) return null;
                                const rect = element.getBoundingClientRect();
                                return {
                                    pageY: Math.round(rect.y + window.scrollY),
                                    pageX: Math.round(rect.x + window.scrollX)
                                };
                            }
                        """, card_selector)
                        
                        if updated_element_info:
                            # 요소 위치로 스크롤
                            await page.evaluate(f"""
                                window.scrollTo(0, {updated_element_info['pageY'] - padding});
                            """)
                        else:
                            await page.evaluate(f"""
                                window.scrollTo(0, {element_info['pageY'] - padding});
                            """)
                    else:
                        await page.evaluate(f"""
                            window.scrollTo(0, {element_info['pageY'] - padding});
                        """)
                    
                    # 스크롤 및 레이아웃 안정화를 위한 최종 대기
                    await page.wait_for_timeout(1000)
                    
                    # 요소가 완전히 로드되고 안정적인지 확인
                    await page.evaluate("""
                        () => {
                            return new Promise(resolve => {
                                // 대기 중인 애니메이션 또는 전환 대기
                                requestAnimationFrame(() => {
                                    requestAnimationFrame(() => {
                                        setTimeout(resolve, 500);
                                    });
                                });
                            });
                        }
                    """)
                    
                    # 뷰포트 변경 후 요소 다시 쿼리
                    card_element = await page.query_selector(card_selector)
                    if not card_element:
                        card_element = await page.query_selector(".cardWrapper")
                    
                    if card_element:
                        # 스크린샷 촬영 - element.screenshot()이 이제 전체 요소를 캡처해야 함
                        screenshot = await card_element.screenshot(
                            type=format,
                            timeout=15000
                        )
                    else:
                        # 대체: 전체 페이지 스크린샷
                        screenshot = await page.screenshot(type=format, full_page=True)
                else:
                    # 대체: 일반 요소 스크린샷 시도
                    await card_element.scroll_into_view_if_needed()
                    await page.wait_for_timeout(1000)
                    screenshot = await card_element.screenshot(type=format, timeout=10000)
            else:
                # 대체: 전체 페이지 스크린샷
                screenshot = await page.screenshot(type=format, full_page=True)
            
            await browser.close()
            return screenshot
    except Exception as e:
        error_msg = str(e)
        print(f"Error generating screenshot: {error_msg}")
        import traceback
        traceback.print_exc()
        
        # 일반적인 Playwright 브라우저 설치 오류 확인
        if "Executable doesn't exist" in error_msg or "BrowserType.launch" in error_msg:
            print("\n⚠️  Playwright 브라우저가 설치되지 않았습니다!")
            print("   설치 방법: python -m playwright install chromium")
            print("   또는 모든 브라우저 설치: python -m playwright install")
        
        return None


def generate_html(card: ProfileCard, github_login: str) -> str:
    """
    프로필 카드의 독립적인 HTML 표현을 생성합니다.
    실제 프론트엔드 디자인과 일치하는 인라인 스타일을 사용합니다.
    
    Args:
        card: ProfileCard 인스턴스
        github_login: GitHub 사용자명
        
    Returns:
        디자인과 일치하는 인라인 스타일이 포함된 완전한 HTML 문자열
    """
    card_url = f"{settings.frontend_base_url}/dashboard/{github_login}/cards/{card.id}"
    gradient = card.gradient or f"linear-gradient(135deg, {card.primary_color or '#667eea'} 0%, rgb(102, 126, 234) 100%)"
    
    # HTML 엔티티 이스케이프
    name = html_escape.escape(card.name)
    title = html_escape.escape(card.title)
    tagline = html_escape.escape(card.tagline) if card.tagline else ""
    
    # 카테고리별로 스택 정리 (stackMeta.ts 구조 따름)
    # stackMeta.ts와 일치하는 카테고리 순서 및 라벨
    category_order = [
        "language", "frontend", "mobile", "backend", "database",
        "infra", "collaboration", "ai-ml", "testing", "tool"
    ]
    # HTML 내보내기용 카테고리 라벨 (한국어 / 영어)
    category_labels_ko = {
        "language": "언어",
        "frontend": "프론트엔드",
        "mobile": "모바일",
        "backend": "백엔드",
        "database": "데이터베이스",
        "infra": "인프라",
        "collaboration": "협업 도구",
        "ai-ml": "AI/ML",
        "testing": "테스팅",
        "tool": "도구",
    }
    category_labels_en = {
        "language": "Language",
        "frontend": "Frontend",
        "mobile": "Mobile",
        "backend": "Backend",
        "database": "Database",
        "infra": "Infra",
        "collaboration": "Collaboration",
        "ai-ml": "AI / ML",
        "testing": "Testing",
        "tool": "Tools",
    }
    # 카드 설정에 따라 라벨 언어 선택 ('ko' | 'en')
    stack_label_lang = getattr(card, "stack_label_lang", "en")
    # None이나 빈 문자열인 경우 영어로 기본값 설정
    if not stack_label_lang or stack_label_lang not in ("ko", "en"):
        stack_label_lang = "en"
    category_labels = category_labels_ko if stack_label_lang == "ko" else category_labels_en
    print(f"[HTML] Using stack_label_lang='{stack_label_lang}', category_labels keys: {list(category_labels.keys())[:3]}...")
    
    stacks_by_category = {}
    if card.show_stacks and card.stacks:
        for stack in card.stacks:
            # 스택 데이터에서 카테고리 사용 (stackMeta.ts 카테고리와 일치해야 함)
            # 대소문자 변형을 처리하기 위해 카테고리를 소문자로 정규화
            category_raw = stack.get('category', 'tool')
            category = category_raw.lower() if isinstance(category_raw, str) else 'tool'
            
            # 카테고리가 category_order에 있는지 확인, 없으면 'tool'로 기본값 설정
            if category not in category_order:
                category = 'tool'
            
            if category not in stacks_by_category:
                stacks_by_category[category] = []
            stacks_by_category[category].append(stack)
    
    # CSS와 정확히 일치하는 스타일로 HTML 빌드
    html = f"""<div style="max-width: 900px; margin: 0 auto; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1); font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;">
  <!-- 배너 섹션 -->
  <div style="background: {gradient}; padding: 60px 40px; text-align: center; color: white; border-radius: 12px 12px 0 0;">
    <div style="max-width: 800px; margin: 0 auto;">
      <h1 style="font-size: 42px; font-weight: 700; margin: 0 0 16px 0; line-height: 1.2;">Hello World 👋 I'm {name}!</h1>
      <p style="font-size: 24px; font-weight: 500; margin: 0 0 12px 0; opacity: 0.95;">{title}</p>
"""
    
    if card.tagline:
        html += f'      <p style="font-size: 18px; margin: 0; opacity: 0.85; font-weight: 400;">{tagline}</p>\n'
    
    html += """    </div>
  </div>
"""
    
    # Stacks Section - Render categories in order matching stackMeta.ts
    if card.show_stacks and stacks_by_category:
        html += """  <!-- Stacks Section -->
  <div style="padding: 32px 40px; background: white;">
    <h2 style="font-size: 28px; font-weight: 700; margin: 0 0 24px 0; color: #333;">Stacks</h2>
    <div style="display: flex; flex-direction: column; gap: 24px;">
"""
        # Render categories in the order defined in stackMeta.ts
        for category in category_order:
            if category in stacks_by_category and stacks_by_category[category]:
                stacks = stacks_by_category[category]
                category_label = category_labels.get(category, category.upper())
                category_escaped = html_escape.escape(category_label)
                # Get alignment from card
                alignment = card.stack_alignment or 'center'
                justify_content = 'flex-start' if alignment == 'left' else ('flex-end' if alignment == 'right' else 'center')
                
                html += f"""      <div style="display: flex; flex-direction: column; gap: 12px;">
        <h3 style="font-size: 18px; font-weight: 600; margin: 0; color: #666; text-transform: uppercase; letter-spacing: 0.5px;">{category_escaped}</h3>
        <div style="display: flex; flex-wrap: wrap; gap: 12px; justify-content: {justify_content};">
"""
                for stack in stacks:
                    # 스택 데이터에서 라벨과 색상 사용 (stackMeta.ts와 일치해야 함)
                    stack_label = html_escape.escape(stack.get('label', stack.get('key', '')))
                    stack_color = stack.get('color', '#667eea')
                    stack_key = stack.get('key', '')
                    
                    # 키가 비어 있으면 라벨을 키로 사용 시도 (소문자로 정규화, 공백을 하이픈으로 교체)
                    if not stack_key and stack_label:
                        # 라벨을 정규화하여 아이콘 찾기 시도 (예: "Node.js" -> "nodejs", "Java" -> "java")
                        normalized_label = stack_label.lower().replace(' ', '-').replace('.', '').replace('++', 'plusplus')
                        # 먼저 정확한 일치 시도
                        if normalized_label in STACK_ICON_MAP:
                            stack_key = normalized_label
                        else:
                            # 변형 시도 (예: "node.js" -> "nodejs", "c++" -> "cpp")
                            variations = [
                                normalized_label.replace('-', ''),
                                normalized_label.replace('.', ''),
                                normalized_label.replace(' ', ''),
                            ]
                            for variant in variations:
                                if variant in STACK_ICON_MAP:
                                    stack_key = variant
                                    break
                    
                    # 특수 케이스: Java는 HTML에서 "OpenJDK"로 표시
                    if stack_key == 'java':
                        stack_label = 'OpenJDK'
                    
                    icon_slug = STACK_ICON_MAP.get(stack_key) if stack_key else None
                    
                    # 디버그: 아이콘을 찾을 수 없으면 출력
                    if not icon_slug and stack_key:
                        print(f"[HTML] Icon not found for stack_key: '{stack_key}', label: '{stack_label}'")
                    elif not icon_slug and stack_label:
                        print(f"[HTML] No stack_key for label: '{stack_label}'")
                    
                    # 배경색 밝기에 따라 아이콘 색상 결정
                    is_light = _is_light_color(stack_color)
                    icon_color = "black" if is_light else "white"
                    # 배경에 따라 텍스트 색상도 조정
                    text_color = "black" if is_light else "white"
                    
                    # 선택적 아이콘이 포함된 배지 HTML 빌드
                    icon_html = ""
                    if icon_slug:
                        icon_html = f'<img src="https://cdn.simpleicons.org/{icon_slug}/{icon_color}" alt="" style="width: 16px; height: 16px; margin-right: 6px; vertical-align: middle; object-fit: contain;" />'
                    
                    html += f"""          <span style="display: inline-flex; align-items: center; gap: 6px; padding: 8px 16px; border-radius: 20px; font-size: 14px; font-weight: 600; color: {text_color}; background-color: {stack_color}; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);">{icon_html}{stack_label}</span>
"""
                html += """        </div>
      </div>
"""
        html += """    </div>
  </div>
"""
    
    # 연락처 섹션
    if card.show_contact and card.contacts:
        html += """  <!-- 연락처 섹션 -->
  <div style="padding: 32px 40px; background: #f8f9fa;">
    <h2 style="font-size: 28px; font-weight: 700; margin: 0 0 24px 0; color: #333;">Contact</h2>
    <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 16px;">
"""
        for contact in card.contacts:
            label = html_escape.escape(contact.get('label', ''))
            value = html_escape.escape(contact.get('value', ''))
            contact_type = contact.get('type', '')
            
            # Debug: Print contact info for troubleshooting
            print(f"[HTML] Processing contact - type: '{contact_type}', label: '{label}', value: '{value[:50]}...'")
            
            # Get icon from contact type mapping
            icon_slug = CONTACT_ICON_MAP.get(contact_type) if contact_type else None
            
            # Debug: Print contact info for troubleshooting
            if not icon_slug and contact_type:
                print(f"[HTML] Icon not found for contact_type: '{contact_type}', label: '{label}'. Available types: {list(CONTACT_ICON_MAP.keys())}")
            elif not contact_type:
                print(f"[HTML] No contact_type specified for label: '{label}'")
            
            is_email = '@' in value and not value.startswith('http')
            is_url = value.startswith('http://') or value.startswith('https://')
            
            if is_email:
                href = f"mailto:{value}"
                target_attr = ""
                rel_attr = ""
            elif is_url:
                href = value
                target_attr = 'target="_blank"'
                rel_attr = 'rel="noopener noreferrer"'
            else:
                href = f"https://{value}"
                target_attr = 'target="_blank"'
                rel_attr = 'rel="noopener noreferrer"'
            
            # 아이콘 HTML 빌드
            icon_html = ""
            if icon_slug:
                icon_html = f'<img src="https://cdn.simpleicons.org/{icon_slug}/000000" alt="{label}" style="width: 32px; height: 32px; object-fit: contain;" />'
                print(f"[HTML] Generated icon HTML for contact_type: '{contact_type}' with icon_slug: '{icon_slug}'")
            elif contact_type:
                # 타입이 지정되었지만 아이콘을 찾을 수 없으면 경고 로그
                print(f"[HTML] Warning: Contact type '{contact_type}' specified but icon not in CONTACT_ICON_MAP")
            
            # 아이콘, 라벨, 값이 포함된 연락처 카드 표시
            # 값이 있으면 항상 표시 (값은 필수, 라벨은 선택사항)
            if value:
                # 라벨을 대문자 타입 이름으로 사용하거나, contact_type으로 대체
                display_label = label.upper() if label else (contact_type.upper() if contact_type else 'CONTACT')
                
                # 빈 속성을 피하기 위해 조건부로 속성 문자열 빌드
                attrs = f'href="{href}"'
                if target_attr:
                    attrs += f' {target_attr}'
                if rel_attr:
                    attrs += f' {rel_attr}'
                
                html += f"""      <a {attrs} style="display: flex; flex-direction: column; padding: 20px; background: white; border-radius: 12px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); text-decoration: none; color: inherit; transition: transform 0.2s, box-shadow 0.2s;" onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 4px 12px rgba(0, 0, 0, 0.15)';" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 8px rgba(0, 0, 0, 0.1)';">
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
          {icon_html if icon_html else '<div style="width: 32px; height: 32px; background: #e0e0e0; border-radius: 4px;"></div>'}
          <span style="font-size: 14px; font-weight: 600; color: #667eea; text-transform: uppercase; letter-spacing: 0.5px;">{display_label}</span>
        </div>
        <span style="font-size: 16px; color: #333; word-break: break-word;">{value}</span>
      </a>
"""
        html += """    </div>
  </div>
"""
    
    # 백준 티어 섹션 (Solved.ac 배지) - 연락처 아래에 배치
    baekjoon_id = getattr(card, "baekjoon_id", None)
    if getattr(card, "show_baekjoon", False) and baekjoon_id:
        safe_handle = html_escape.escape(baekjoon_id)
        badge_src = f"http://mazassumnida.wtf/api/v2/generate_badge?boj={safe_handle}"
        solved_profile_url = f"https://solved.ac/{safe_handle}/"
        html += f"""  <!-- 백준 티어 섹션 -->
  <div style="padding: 32px 40px; background: white;">
    <h2 style="font-size: 28px; font-weight: 700; margin: 0 0 24px 0; color: #333;">Baekjoon</h2>
    <div style="text-align: center;">
      <a href="{solved_profile_url}" target="_blank" rel="noopener noreferrer">
        <img src="{badge_src}" alt="Solved.ac Profile" />
      </a>
    </div>
  </div>
"""
    
    # GitHub Stats Section (정적 데이터만 표시, API 호출 불가)
    # HTML에서는 실제 통계를 가져올 수 없으므로 링크만 제공
    if card.show_github_stats:
        html += f"""  <!-- GitHub Stats Section -->
  <div style="padding: 32px 40px; background: white;">
    <h2 style="font-size: 28px; font-weight: 700; margin: 0 0 24px 0; color: #333;">Github-stats</h2>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 20px;">
      <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 24px; background: {gradient}; border-radius: 12px; color: white; box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);">
        <div style="font-size: 36px; font-weight: 700; margin-bottom: 8px;">-</div>
        <div style="font-size: 14px; font-weight: 500; opacity: 0.9; text-transform: uppercase; letter-spacing: 0.5px;">Repositories</div>
      </div>
      <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 24px; background: {gradient}; border-radius: 12px; color: white; box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);">
        <div style="font-size: 36px; font-weight: 700; margin-bottom: 8px;">-</div>
        <div style="font-size: 14px; font-weight: 500; opacity: 0.9; text-transform: uppercase; letter-spacing: 0.5px;">Stars</div>
      </div>
      <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 24px; background: {gradient}; border-radius: 12px; color: white; box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);">
        <div style="font-size: 36px; font-weight: 700; margin-bottom: 8px;">-</div>
        <div style="font-size: 14px; font-weight: 500; opacity: 0.9; text-transform: uppercase; letter-spacing: 0.5px;">Followers</div>
      </div>
      <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 24px; background: {gradient}; border-radius: 12px; color: white; box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);">
        <div style="font-size: 36px; font-weight: 700; margin-bottom: 8px;">-</div>
        <div style="font-size: 14px; font-weight: 500; opacity: 0.9; text-transform: uppercase; letter-spacing: 0.5px;">Following</div>
      </div>
    </div>
    <p style="text-align: center; margin-top: 16px; color: #666; font-size: 14px;">※ GitHub 통계는 <a href="{card_url}" target="_blank" rel="noopener noreferrer" style="color: #667eea; text-decoration: none;">프로필 카드 페이지</a>에서 확인하세요.</p>
  </div>
"""
    
    # 레포지토리 섹션
    repositories = getattr(card, "repositories", [])
    if repositories and len(repositories) > 0:
        html += """  <!-- Repositories Section -->
  <div style="padding: 32px 40px; background: white;">
    <h2 style="font-size: 28px; font-weight: 700; margin: 0 0 24px 0; color: #333;">Repositories</h2>
    <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px;">
"""
        for repo in repositories:
            repo_name = html_escape.escape(repo.get("name", ""))
            repo_description = html_escape.escape(repo.get("description", "")) if repo.get("description") else ""
            repo_url = html_escape.escape(repo.get("html_url", ""))
            repo_language = html_escape.escape(repo.get("language", "")) if repo.get("language") else ""
            stargazers_count = repo.get("stargazers_count", 0)
            forks_count = repo.get("forks_count", 0)
            
            html += f"""      <a href="{repo_url}" target="_blank" rel="noopener noreferrer" style="display: flex; flex-direction: column; padding: 20px; background: #f8f9fa; border-radius: 12px; border: 1px solid #e5e7eb; text-decoration: none; color: inherit; transition: all 0.2s;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
          <h3 style="font-size: 18px; font-weight: 600; margin: 0; color: #667eea;">{repo_name}</h3>
"""
            if repo_language:
                html += f"""          <span style="font-size: 12px; padding: 4px 8px; background: #e5e7eb; border-radius: 12px; color: #6b7280; font-weight: 500;">{repo_language}</span>
"""
            html += """        </div>
"""
            if repo_description:
                html += f"""        <p style="font-size: 14px; color: #6b7280; margin: 0 0 12px 0; line-height: 1.5; flex: 1;">{repo_description}</p>
"""
            html += f"""        <div style="display: flex; gap: 16px; font-size: 14px; color: #9ca3af; margin-top: auto;">
          <span style="display: flex; align-items: center; gap: 4px;">⭐ {stargazers_count}</span>
          <span style="display: flex; align-items: center; gap: 4px;">🍴 {forks_count}</span>
        </div>
      </a>
"""
        html += """    </div>
  </div>
"""
    
    html += "</div>"
    
    return html


def _extract_gradient_colors(card: ProfileCard) -> tuple[str, str]:
    """
    데이터베이스의 card.gradient 필드에서 그라데이션 색상을 추출합니다.
    
    지원 형식:
    - linear-gradient(135deg, #667eea 0%, #764ba2 100%)  (hex + hex)
    - linear-gradient(135deg, rgb(102, 126, 234) 0%, rgb(118, 75, 162) 100%)  (rgb + rgb)
    - linear-gradient(135deg, #667eea 0%, rgb(106, 104, 240) 100%)  (hex + rgb) - 혼합 형식
    - linear-gradient(135deg, rgb(102, 126, 234) 0%, #764ba2 100%)  (rgb + hex) - 혼합 형식
    - #667eea, #764ba2
    - #667eea
    """
    import re
    
    # Default fallback colors
    default_primary = card.primary_color or "#667eea"
    default_secondary = "#764ba2"
    
    gradient = card.gradient or ""
    
    # If gradient is empty, use primary_color as fallback
    if not gradient or gradient.strip() == "":
        return default_primary, default_secondary
    
    # Normalize: remove whitespace for easier parsing
    gradient_clean = gradient.strip()
    
    # Helper functions
    def normalize_hex(hex_str: str) -> str:
        """Convert 3-digit hex to 6-digit hex."""
        if len(hex_str) == 3:
            return f"#{hex_str[0]}{hex_str[0]}{hex_str[1]}{hex_str[1]}{hex_str[2]}{hex_str[2]}"
        return f"#{hex_str}"
    
    def rgb_to_hex(r: int, g: int, b: int) -> str:
        """Convert RGB to hex."""
        return f"#{r:02x}{g:02x}{b:02x}"
    
    # Find all color values in order (both hex and RGB)
    # We need to find colors in the order they appear in the gradient string
    
    # Pattern to match color values: either hex (#...) or rgb(...)
    # This regex finds both hex and rgb patterns, preserving their order
    # IMPORTANT: {6} must come before {3} to match 6-digit hex before 3-digit hex
    color_pattern = r"(?:#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})|rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\))"
    
    colors = []
    for match in re.finditer(color_pattern, gradient_clean):
        groups = match.groups()
        # groups[0] is hex color (if found)
        # groups[1], groups[2], groups[3] are RGB values (if found)
        if groups[0] is not None:  # Hex color found
            hex_color = normalize_hex(groups[0])
            colors.append(hex_color)
            print(f"[COLOR EXTRACT] Found hex color: {groups[0]} -> {hex_color}")
        elif groups[1] is not None and groups[2] is not None and groups[3] is not None:  # RGB color found
            r, g, b = int(groups[1]), int(groups[2]), int(groups[3])
            rgb_hex = rgb_to_hex(r, g, b)
            colors.append(rgb_hex)
            print(f"[COLOR EXTRACT] Found RGB color: rgb({r}, {g}, {b}) -> {rgb_hex}")
    
    # Extract primary and secondary colors
    print(f"[COLOR EXTRACT] Total colors found: {len(colors)}, colors: {colors}")
    if len(colors) >= 2:
        primary = colors[0]
        secondary = colors[1]
        print(f"[COLOR EXTRACT] Using colors[0]={primary}, colors[1]={secondary}")
    elif len(colors) == 1:
        primary = colors[0]
        secondary = default_secondary
        print(f"[COLOR EXTRACT] Only one color found, using default secondary: {secondary}")
    else:
        # 색상을 찾을 수 없음, 대체 패턴 시도
        # 패턴 1: hex만 시도
        # 중요: 3자리 hex보다 6자리 hex를 먼저 매칭하려면 {6}이 {3}보다 앞에 와야 함
        hex_regex = r"#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})"
        hex_matches = re.findall(hex_regex, gradient_clean)
        print(f"[COLOR EXTRACT FALLBACK] Hex matches: {hex_matches}")
        if hex_matches:
            primary = normalize_hex(hex_matches[0])
            secondary = normalize_hex(hex_matches[1]) if len(hex_matches) >= 2 else default_secondary
            print(f"[COLOR EXTRACT FALLBACK] Using hex fallback - primary={primary}, secondary={secondary}")
            return primary, secondary
        
        # 패턴 2: RGB만 시도
        rgb_regex = r"rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)"
        rgb_matches = re.findall(rgb_regex, gradient_clean)
        if rgb_matches:
            r, g, b = map(int, rgb_matches[0])
            primary = rgb_to_hex(r, g, b)
            if len(rgb_matches) >= 2:
                r2, g2, b2 = map(int, rgb_matches[1])
                secondary = rgb_to_hex(r2, g2, b2)
            else:
                secondary = default_secondary
            return primary, secondary
        
        # 모든 파싱 실패 - 기본값 사용
        return default_primary, default_secondary
    
    # 주요 색상과 보조 색상이 다른지 확인
    if primary == secondary:
        secondary = default_secondary
    
    # 디버그: 추출된 색상 출력
    print(f"[COLOR EXTRACT] gradient={gradient_clean}, colors_found={colors}, primary={primary}, secondary={secondary}")
    
    return primary, secondary


def generate_svg(
    card: ProfileCard,
    github_login: str,
    stats: Optional[Dict[str, Optional[int]]] = None,
) -> str:
    """
    Generate an SVG representation of the profile card.
    This is optimized for GitHub README: SVG는 그대로 렌더링되며 CSS 없이도
    카드와 거의 동일한 디자인을 유지할 수 있습니다.
    """
    primary, secondary = _extract_gradient_colors(card)

    name = html_escape.escape(card.name)
    title = html_escape.escape(card.title)
    tagline = html_escape.escape(card.tagline or "")

    width = 900
    
    # 스택을 카테고리별로 그룹화
    stacks_by_category = {}
    if card.show_stacks and card.stacks:
        for stack in card.stacks:
            category = stack.get('category', 'Other')
            if category not in stacks_by_category:
                stacks_by_category[category] = []
            raw_label = stack.get("label") or stack.get("key") or ""
            label = html_escape.escape(raw_label)
            if label:
                color = stack.get("color") or primary
                stacks_by_category[category].append({"label": label, "color": color})
    
    # 높이 동적 계산
    banner_height = 180
    section_padding = 32
    section_gap = 0
    
    # 스택 섹션 높이 계산
    stacks_height = 0
    if stacks_by_category:
        stacks_height += 28 + 24  # "Stacks" 헤더
        for category, stacks in stacks_by_category.items():
            stacks_height += 18 + 12  # 카테고리 라벨 + 간격
            # 배지 행 계산
            badge_height = 28
            badge_gap = 8
            row_gap = 10
            max_width = width - 80 - 40  # 좌우 패딩 제외
            current_row_width = 0
            rows = 1
            for stack in stacks[:20]:
                text_len = len(stack["label"])
                badge_width = max(60, min(200, text_len * 8 + 24))
                if current_row_width + badge_width > max_width and current_row_width > 0:
                    rows += 1
                    current_row_width = badge_width + badge_gap
                else:
                    current_row_width += badge_width + badge_gap
            stacks_height += rows * badge_height + (rows - 1) * row_gap
            stacks_height += 24  # 카테고리 간 간격
        stacks_height += section_padding * 2
    
    # 연락처 섹션 높이 계산
    contact_height = 0
    if card.show_contact and card.contacts:
        contact_height += 28 + 24  # "Contact" 헤더
        # 그리드 레이아웃: 최소 2열, 각 카드 높이 80px
        num_contacts = min(len(card.contacts), 6)  # 최대 6개
        cols = min(2, num_contacts)
        rows = (num_contacts + cols - 1) // cols
        contact_height += rows * 80 + (rows - 1) * 16  # 카드 높이 + 간격
        contact_height += section_padding * 2
    
    # GitHub 통계 섹션 높이 계산
    stats_height = 0
    if card.show_github_stats:
        stats_height += 28 + 24  # "Github-stats" 헤더
        # 4개 박스: 2x2 그리드
        stats_height += 2 * 100 + 20  # 박스 높이 100px, 간격 20px
        stats_height += section_padding * 2
    
    # 전체 높이 계산
    total_height = banner_height + stacks_height + contact_height + stats_height
    height = max(600, total_height)  # 최소 높이 600px

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
  <defs>
    <linearGradient id="bannerGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{primary}" />
      <stop offset="100%" stop-color="{secondary}" />
    </linearGradient>
    <linearGradient id="statsGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{primary}" />
      <stop offset="100%" stop-color="{secondary}" />
    </linearGradient>
    <filter id="cardShadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="4" stdDeviation="8" flood-color="rgba(0,0,0,0.15)" />
    </filter>
    <filter id="smallShadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="2" stdDeviation="4" flood-color="rgba(0,0,0,0.1)" />
    </filter>
  </defs>
  <title id="title">GitCard - {name}</title>
  <desc id="desc">GitHub 프로필 카드</desc>

  <!-- Card background -->
  <rect x="0" y="0" width="{width}" height="{height}" rx="16" ry="16" fill="#ffffff" filter="url(#cardShadow)" />

  <!-- Banner -->
  <rect x="0" y="0" width="{width}" height="{banner_height}" rx="16" ry="16" fill="url(#bannerGradient)" />

  <!-- Name -->
  <text x="{width/2}" y="80" text-anchor="middle" fill="#ffffff" font-size="42" font-weight="700" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif">
    Hello World 👋 I'm {name}!
  </text>

  <!-- Title -->
  <text x="{width/2}" y="130" text-anchor="middle" fill="#ffffff" font-size="24" font-weight="500" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif" opacity="0.95">
    {title}
  </text>
"""

    if tagline:
        svg += f"""  <!-- Tagline -->
  <text x="{width/2}" y="160" text-anchor="middle" fill="#ffffff" font-size="18" font-weight="400" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif" opacity="0.85">
    {tagline}
  </text>
"""

    current_y = banner_height + section_padding

    # Stacks section - 카테고리별로 그룹화하여 렌더링
    if stacks_by_category:
        svg += f"""  <!-- Stacks Section -->
  <text x="40" y="{current_y}" fill="#333333" font-size="28" font-weight="700" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif">
    Stacks
  </text>
"""
        current_y += 28 + 24
        
        for category, stacks in stacks_by_category.items():
            category_escaped = html_escape.escape(category.upper())
            svg += f"""  <!-- Category: {category} -->
  <text x="40" y="{current_y}" fill="#666666" font-size="18" font-weight="600" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif" letter-spacing="0.5">
    {category_escaped}
  </text>
"""
            current_y += 18 + 12
            
            # 배지 렌더링
            badge_start_x = 40
            badge_x = badge_start_x
            badge_y = current_y
            badge_height = 28
            horizontal_gap = 12
            vertical_gap = 10
            max_width = width - 80
            
            for stack in stacks[:20]:
                label = stack["label"]
                color = stack["color"]
                text_len = len(label)
                badge_width = max(60, min(200, text_len * 8 + 24))
                
                # 줄바꿈 처리
                if badge_x + badge_width > max_width:
                    badge_x = badge_start_x
                    badge_y += badge_height + vertical_gap
                
                text_x = badge_x + badge_width / 2
                text_y = badge_y + badge_height / 2 + 4
                
                svg += f"""  <g>
    <rect x="{badge_x}" y="{badge_y}" rx="20" ry="20" width="{badge_width}" height="{badge_height}" fill="{color}" filter="url(#smallShadow)" />
    <text x="{text_x}" y="{text_y}" text-anchor="middle" fill="#ffffff" font-size="14" font-weight="600" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif">{label}</text>
  </g>
"""
                badge_x += badge_width + horizontal_gap
            
            current_y = badge_y + badge_height + 24
        
        current_y += section_padding - 24

    # 연락처 섹션 - 카드 형태로 렌더링
    if card.show_contact and card.contacts:
        svg += f"""  <!-- 연락처 섹션 배경 -->
  <rect x="0" y="{current_y}" width="{width}" height="{contact_height - section_padding * 2}" fill="#f8f9fa" />
  <text x="40" y="{current_y + section_padding}" fill="#333333" font-size="28" font-weight="700" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif">
    Contact
  </text>
"""
        contact_start_y = current_y + section_padding + 28 + 24
        contact_x = 40
        contact_y = contact_start_y
        contact_card_width = (width - 80 - 16) // 2  # 2열 그리드
        contact_card_height = 80
        contact_gap = 16
        
        for i, contact in enumerate(card.contacts[:6]):
            if i > 0 and i % 2 == 0:
                contact_x = 40
                contact_y += contact_card_height + contact_gap
            
            label = html_escape.escape(contact.get("label", ""))
            value = html_escape.escape(contact.get("value", ""))
            contact_type = contact.get("type", "")
            
            # 값이 있으면 항상 표시 (값은 필수, 라벨은 선택사항)
            if value:
                # 라벨을 대문자 타입 이름으로 사용하거나, contact_type으로 대체
                display_label = label.upper() if label else (contact_type.upper() if contact_type else 'CONTACT')
                
                svg += f"""  <!-- Contact Card -->
  <rect x="{contact_x}" y="{contact_y}" width="{contact_card_width}" height="{contact_card_height}" rx="12" ry="12" fill="#ffffff" filter="url(#smallShadow)" />
  <text x="{contact_x + 20}" y="{contact_y + 24}" fill="#667eea" font-size="14" font-weight="600" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif" letter-spacing="0.5">
    {display_label}
  </text>
  <text x="{contact_x + 20}" y="{contact_y + 48}" fill="#333333" font-size="16" font-weight="400" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif">
    {value[:40]}{'...' if len(value) > 40 else ''}
  </text>
"""
                contact_x += contact_card_width + contact_gap
        
        current_y += contact_height

    # GitHub 통계 섹션 - 그라데이션 배경 카드로 렌더링
    if card.show_github_stats:
        svg += f"""  <!-- GitHub 통계 섹션 -->
  <text x="40" y="{current_y + section_padding}" fill="#333333" font-size="28" font-weight="700" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif">
    Github-stats
  </text>
"""
        stats_start_y = current_y + section_padding + 28 + 24
        
        if stats:
            repos = stats.get("repositories") or 0
            stars = stats.get("stars") or 0
            followers = stats.get("followers") or 0
            following = stats.get("following") or 0
            
            # 4개 박스: 2x2 그리드
            box_w = (width - 80 - 20) // 2  # 2열
            box_h = 100
            box_gap = 20
            
            stats_data = [
                ("REPOSITORIES", repos),
                ("STARS", stars),
                ("FOLLOWERS", followers),
                ("FOLLOWING", following),
            ]
            
            for i, (label, value) in enumerate(stats_data):
                row = i // 2
                col = i % 2
                x = 40 + col * (box_w + box_gap)
                y = stats_start_y + row * (box_h + box_gap)
                
                svg += f"""  <!-- Stat Box: {label} -->
  <g>
    <rect x="{x}" y="{y}" width="{box_w}" height="{box_h}" rx="12" ry="12" fill="url(#statsGradient)" filter="url(#smallShadow)" />
    <text x="{x + box_w/2}" y="{y + 40}" text-anchor="middle" fill="#ffffff" font-size="36" font-weight="700" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif">{value}</text>
    <text x="{x + box_w/2}" y="{y + 70}" text-anchor="middle" fill="#ffffff" font-size="14" font-weight="500" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif" opacity="0.9" letter-spacing="0.5">
      {label}
    </text>
  </g>
"""

    svg += "\n</svg>"
    return svg


def _remove_port_from_url(url: str) -> str:
    """
    프로덕션 사용을 위해 URL에서 포트 번호 제거 (예: :8000).
    """
    from urllib.parse import urlparse, urlunparse
    parsed = urlparse(url)
    # Remove port if it exists
    netloc = parsed.netloc.split(':')[0] if ':' in parsed.netloc else parsed.netloc
    # Reconstruct URL without port
    new_parsed = parsed._replace(netloc=netloc)
    return urlunparse(new_parsed)


def generate_svg_markdown(card: ProfileCard, github_login: str) -> str:
    """
    GitHub README에 카드 이미지를 포함하는 마크다운 스니펫을 생성합니다.
    더 나은 디자인 일치를 위해 SVG 대신 새 이미지 엔드포인트(PNG/WebP)를 사용합니다.
    """
    # 정확한 디자인 렌더링을 위해 SVG 대신 이미지 엔드포인트 사용
    image_url = f"{settings.api_base_url}/api/profiles/public/{github_login}/cards/{card.id}/image?format=png"
    card_url = f"{settings.frontend_base_url}/dashboard/{github_login}/cards/{card.id}"
    
    # 프로덕션을 위해 URL에서 포트 제거 (예: :8000)
    image_url = _remove_port_from_url(image_url)
    card_url = _remove_port_from_url(card_url)
    
    # 이미지를 클릭하면 공개 카드 페이지로 이동하도록 링크 감싸기
    return f"[![GitCard]({image_url})]({card_url})"


def _hex_to_url_color(hex_color: str) -> str:
    """
    capsule-render를 위해 hex 색상을 URL 인코딩 형식으로 변환합니다.
    예: #667eea -> %23667eea
    """
    if hex_color.startswith('#'):
        return f"%23{hex_color[1:]}"
    return hex_color.replace('#', '%23')


def _extract_primary_color_for_banner(card: ProfileCard) -> str:
    """
    배너용 카드에서 주요 색상을 추출합니다.
    기본 보라색 그라데이션 색상으로 대체됩니다.
    """
    primary = card.primary_color or "#667eea"
    # Extract first color from gradient if available
    if card.gradient:
        import re
        hex_regex = r"#(?:[A-Fa-f0-9]{3}|[A-Fa-f0-9]{6})"
        matches = re.findall(hex_regex, card.gradient)
        if matches:
            primary = matches[0]
    return primary


def generate_svg_banner(card: ProfileCard) -> str:
    """
    순수 SVG 요소를 사용하여 그라데이션 배경이 있는 SVG 배너를 생성합니다.
    foreignObject 없이 GitHub README에서 안정적인 렌더링을 보장합니다.
    
    Args:
        card: ProfileCard 인스턴스
        
    Returns:
        그라데이션 배너가 있는 SVG 문자열
    """
    # 데이터베이스에서 그라데이션 색상 추출
    # card.gradient는 데이터베이스의 그라데이션 문자열을 포함합니다 (예: "linear-gradient(135deg, #667eea 0%, rgb(106, 104, 240) 100%)")
    # 중요: 프론트엔드의 PublicProfileCardPage.tsx에서 추출한 색상과 일치해야 함
    primary, secondary = _extract_gradient_colors(card)
    
    # 디버그: 유효한 색상인지 확인 (추출 실패 시 대체)
    if not primary or not primary.startswith('#'):
        primary = card.primary_color or "#667eea"
    if not secondary or not secondary.startswith('#'):
        secondary = "#764ba2"
    
    # 디버그: 디버깅을 위해 콘솔에 출력
    print(f"[SVG BANNER] card_id={card.id}, gradient={card.gradient}, extracted primary={primary}, secondary={secondary}")
    
    # SVG 텍스트용 HTML 엔티티 이스케이프
    name = html_escape.escape(card.name)
    title = html_escape.escape(card.title)
    tagline = html_escape.escape(card.tagline or "")
    
    # 배너 크기
    width = 900
    height = 200
    
    # 중심 x 위치 계산
    center_x = width / 2
    
    # 순수 SVG 요소로 SVG 빌드 (foreignObject 없음)
    # GitHub README 호환성을 위해 objectBoundingBox와 백분율 좌표 사용
    # GitHub README는 objectBoundingBox와 백분율 값을 사용하면 그라데이션을 더 잘 렌더링합니다
    # 135deg 그라데이션의 경우: 왼쪽 상단 (0%,0%)에서 오른쪽 하단 (100%, 100%)으로
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <defs>
    <linearGradient id="bannerGradient" x1="0%" y1="0%" x2="100%" y2="100%" gradientUnits="objectBoundingBox">
      <stop offset="0%" stop-color="{primary}" />
      <stop offset="100%" stop-color="{secondary}" />
    </linearGradient>
  </defs>
  
  <!-- Gradient background -->
  <rect x="0" y="0" width="{width}" height="{height}" fill="url(#bannerGradient)" />
  
  <!-- Name text -->
  <text x="{center_x}" y="80" text-anchor="middle" fill="#ffffff" font-size="42" font-weight="700" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif">
    🧩 Hello World 👋 I'm {name}!
  </text>
  
  <!-- Title text -->
  <text x="{center_x}" y="130" text-anchor="middle" fill="#ffffff" font-size="24" font-weight="500" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif" opacity="0.95">
    {title}
  </text>
'''
    
    if tagline:
        svg += f'''  <!-- Tagline text -->
  <text x="{center_x}" y="165" text-anchor="middle" fill="#ffffff" font-size="18" font-weight="400" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif" opacity="0.85">
    {tagline}
  </text>
'''
    
    svg += '</svg>'
    
    return svg


def generate_svg_contact(card: ProfileCard) -> str:
    """
    그리드 레이아웃의 연락처 카드가 있는 SVG 연락처 섹션을 생성합니다.
    CSS 의존성 없이 GitHub README에서 안정적인 렌더링을 보장합니다.
    
    Args:
        card: ProfileCard 인스턴스
        
    Returns:
        연락처 카드가 있는 SVG 문자열
    """
    if not card.show_contact or not card.contacts:
        return ""
    
    # Filter contacts with values
    valid_contacts = [c for c in card.contacts[:6] if c.get('value')]
    
    if not valid_contacts:
        return ""
    
    # 연락처 카드 크기
    card_width = 280
    card_height = 100
    card_padding = 20
    card_gap = 16
    cards_per_row = 3
    
    # 그리드 크기 계산
    num_cards = len(valid_contacts)
    num_rows = (num_cards + cards_per_row - 1) // cards_per_row
    width = (card_width * cards_per_row) + (card_gap * (cards_per_row - 1)) + (card_padding * 2)
    height = (card_height * num_rows) + (card_gap * (num_rows - 1)) + (card_padding * 2)
    
    # SVG 빌드
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <defs>
    <filter id="contactShadow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur in="SourceAlpha" stdDeviation="2"/>
      <feOffset dx="0" dy="2" result="offsetblur"/>
      <feComponentTransfer>
        <feFuncA type="linear" slope="0.3"/>
      </feComponentTransfer>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>
  
  <!-- Background -->
  <rect x="0" y="0" width="{width}" height="{height}" fill="#f8f9fa" rx="12" ry="12"/>
'''
    
    # 연락처 카드 생성
    for i, contact in enumerate(valid_contacts):
        row = i // cards_per_row
        col = i % cards_per_row
        
        x = card_padding + (col * (card_width + card_gap))
        y = card_padding + (row * (card_height + card_gap))
        
        label = html_escape.escape(contact.get('label', ''))
        value = html_escape.escape(contact.get('value', ''))
        contact_type = contact.get('type', '')
        
        # 라벨을 대문자 타입 이름으로 사용하거나, contact_type으로 대체
        display_label = label.upper() if label else (contact_type.upper() if contact_type else 'CONTACT')
        
        # 너무 길면 값 자르기
        display_value = value[:30] + '...' if len(value) > 30 else value
        
        # 연락처 타입 매핑에서 아이콘 slug 가져오기
        icon_slug = CONTACT_ICON_MAP.get(contact_type) if contact_type else None
        
        # 연락처 카드
        svg += f'''  <!-- 연락처 카드 {i+1} -->
  <rect x="{x}" y="{y}" width="{card_width}" height="{card_height}" rx="12" ry="12" fill="#ffffff" filter="url(#contactShadow)"/>
'''
        
        # shields.io를 사용한 아이콘 (GitHub README 호환)
        if icon_slug:
            # GitHub README에서 안정적인 렌더링을 위해 shields.io 아이콘 전용 배지 사용
            # 형식: https://img.shields.io/badge/-{icon_slug}-000000?logo={icon_slug}&logoColor=white&style=flat
            icon_badge_url = f"https://img.shields.io/badge/-{icon_slug}-000000?logo={icon_slug}&logoColor=white&style=flat"
            svg += f'''  <image x="{x + 20}" y="{y + 20}" width="32" height="32" href="{icon_badge_url}" preserveAspectRatio="xMidYMid meet"/>
'''
        else:
            # 대체: 간단한 원형 아이콘
            svg += f'''  <circle cx="{x + 36}" cy="{y + 36}" r="16" fill="#e0e0e0"/>
'''
        
        # 라벨 텍스트
        svg += f'''  <text x="{x + 60}" y="{y + 35}" fill="#667eea" font-size="12" font-weight="600" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif" text-transform="uppercase" letter-spacing="0.5">
    {display_label}
  </text>
'''
        
        # 값 텍스트
        svg += f'''  <text x="{x + 20}" y="{y + 70}" fill="#333333" font-size="14" font-weight="400" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif">
    {display_value}
  </text>
'''
    
    svg += '</svg>'
    
    return svg


def generate_svg_repository_banner(repo: Dict) -> str:
    """
    레포지토리 정보를 카드 형태의 SVG 배너로 생성합니다.
    이미지 설명에 맞는 레이아웃: 레포지토리 이름, 언어 배지, 설명, Stars/Forks 통계
    
    Args:
        repo: 레포지토리 정보 딕셔너리
            - name: 레포지토리 이름
            - description: 설명 (선택)
            - html_url: GitHub URL
            - language: 주요 언어 (선택)
            - stargazers_count: 스타 수
            - forks_count: 포크 수
    
    Returns:
        레포지토리 카드 SVG 문자열
    """
    repo_name = html_escape.escape(repo.get("name", ""))
    repo_description = html_escape.escape(repo.get("description", "")) if repo.get("description") else ""
    repo_language = html_escape.escape(repo.get("language", "")) if repo.get("language") else ""
    stargazers_count = repo.get("stargazers_count", 0)
    forks_count = repo.get("forks_count", 0)
    
    # 카드 크기
    card_width = 800
    card_height = 140
    card_padding = 24
    
    # SVG 빌드
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{card_width}" height="{card_height}" viewBox="0 0 {card_width} {card_height}">
  <defs>
    <filter id="repoShadow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur in="SourceAlpha" stdDeviation="2"/>
      <feOffset dx="0" dy="2" result="offsetblur"/>
      <feComponentTransfer>
        <feFuncA type="linear" slope="0.05"/>
      </feComponentTransfer>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>
  
  <!-- 카드 배경 -->
  <rect x="0" y="0" width="{card_width}" height="{card_height}" rx="12" ry="12" fill="#ffffff" stroke="#e0e7ff" stroke-width="1" filter="url(#repoShadow)"/>
  
  <!-- 레포지토리 이름 (좌측 상단) -->
  <text x="{card_padding}" y="40" fill="#667eea" font-size="18" font-weight="600" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif">
    {repo_name}
  </text>'''
    
    # 언어 배지 (우측 상단)
    if repo_language:
        # 언어 배지 크기 계산
        language_x = card_width - card_padding - 80  # 대략적인 배지 너비
        svg += f'''  <!-- 언어 배지 -->
  <rect x="{language_x}" y="20" width="80" height="24" rx="12" ry="12" fill="#f3f4f6"/>
  <text x="{language_x + 40}" y="37" text-anchor="middle" fill="#374151" font-size="12" font-weight="500" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif">
    {repo_language}
  </text>'''
    
    # 설명 텍스트 (중앙)
    if repo_description:
        # 긴 설명은 자르기 (최대 2줄)
        max_desc_length = 80
        if len(repo_description) > max_desc_length:
            repo_description = repo_description[:max_desc_length] + "..."
        svg += f'''  <!-- 설명 텍스트 -->
  <text x="{card_padding}" y="75" fill="#4b5563" font-size="14" font-weight="400" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif">
    {repo_description}
  </text>'''
    
    # 통계 정보 (하단)
    stats_y = card_height - 20
    svg += f'''  <!-- 통계 정보 -->
  <text x="{card_padding}" y="{stats_y}" fill="#4b5563" font-size="14" font-weight="400" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif">
    ⭐ {stargazers_count}  🍴 {forks_count}
  </text>
</svg>'''
    
    return svg


def generate_readme_template(
    card: ProfileCard,
    github_login: str,
    stats: Optional[Dict[str, Optional[int]]] = None,
) -> str:
    """
    GitHub README 안전 마크다운 템플릿을 생성합니다.    
    
    사용:
    - 이미지 URL로 SVG 배너 (capsule-render 방식) - 안정적인 렌더링 보장
    - 스택 및 연락처용 shields.io 배지
    - GitHub 통계용 github-readme-stats
    - 커스텀 카드용 GitCard 이미지 엔드포인트
    
    이 템플릿은 GitHub README에서 작동이 보장됩니다. SVG용 이미지 URL(capsule-render와 유사),
    마크다운 제목, 최소한의 HTML(div align, img, a), GitHub가 지원하는 외부 이미지 서비스를 사용합니다.
    
    Args:
        card: ProfileCard 인스턴스
        github_login: GitHub 사용자명
        stats: 선택적 GitHub 통계 딕셔너리
        
    Returns:
        완전한 README 마크다운 템플릿
    """
    # URL
    banner_url = f"{settings.api_base_url}/profiles/public/{github_login}/cards/{card.id}/banner"
    card_url = f"{settings.frontend_base_url}/dashboard/{github_login}/cards/{card.id}"
    
    # 프로덕션을 위해 URL에서 포트 제거
    banner_url = _remove_port_from_url(banner_url)
    card_url = _remove_port_from_url(card_url)
    
    # 이미지 URL로 배너가 있는 README 템플릿 빌드 (capsule-render 방식)
    # 배너는 사용자가 선택한 그라데이션 색상을 사용
    readme = f'''<div align="center">
  <img src="{banner_url}" alt="GitCard Banner" />
</div>

'''
    
    # 스택 섹션
    if card.show_stacks and card.stacks:
        readme += "## 🛠️ Tech Stacks\n\n"
        
        # stackMeta.ts와 일치하는 카테고리 순서 및 라벨
        category_order = [
            "language", "frontend", "mobile", "backend", "database",
            "infra", "collaboration", "ai-ml", "testing", "tool"
        ]
        # README 내보내기용 카테고리 라벨 (한국어 / 영어)
        category_labels_ko = {
            "language": "언어",
            "frontend": "프론트엔드",
            "mobile": "모바일",
            "backend": "백엔드",
            "database": "데이터베이스",
            "infra": "인프라",
            "collaboration": "협업 도구",
            "ai-ml": "AI/ML",
            "testing": "테스팅",
            "tool": "도구",
        }
        category_labels_en = {
            "language": "Language",
            "frontend": "Frontend",
            "mobile": "Mobile",
            "backend": "Backend",
            "database": "Database",
            "infra": "Infra",
            "collaboration": "Collaboration",
            "ai-ml": "AI / ML",
            "testing": "Testing",
            "tool": "Tools",
        }
        # 카드 설정에 따라 라벨 언어 선택 ('ko' | 'en')
        stack_label_lang = getattr(card, "stack_label_lang", "en")
        # None이나 빈 문자열인 경우 영어로 기본값 설정
        if not stack_label_lang or stack_label_lang not in ("ko", "en"):
            stack_label_lang = "en"
        category_labels = category_labels_ko if stack_label_lang == "ko" else category_labels_en
        print(f"[README] Using stack_label_lang='{stack_label_lang}', category_labels keys: {list(category_labels.keys())[:3]}...")
        
        # 카테고리별로 스택 그룹화
        stacks_by_category = {}
        for stack in card.stacks:
            # 대소문자 변형을 처리하기 위해 카테고리를 소문자로 정규화
            category_raw = stack.get('category', 'tool')
            category = category_raw.lower() if isinstance(category_raw, str) else 'tool'
            
            # 카테고리가 category_order에 있는지 확인, 없으면 'tool'로 기본값 설정
            if category not in category_order:
                category = 'tool'
            
            if category not in stacks_by_category:
                stacks_by_category[category] = []
            label = stack.get('label') or stack.get('key', '')
            color = stack.get('color', '#667eea')
            stack_key = stack.get('key', '')  # 아이콘 조회용 키 가져오기
            if label:
                stacks_by_category[category].append({'label': label, 'color': color, 'key': stack_key})
        
        # stackMeta.ts와 일치하는 순서로 카테고리 렌더링
        for category in category_order:
            if category in stacks_by_category and stacks_by_category[category]:
                stacks = stacks_by_category[category]
                category_label = category_labels.get(category, category.upper())
                
                # 카테고리 제목 추가
                readme += f"### {category_label}\n\n"
                # 카드에서 정렬 가져오기
                alignment = card.stack_alignment or 'center'
                align_value = alignment  # 'left', 'center', 또는 'right'
                readme += f'<div align="{align_value}">\n\n'
                
                # 이 카테고리의 각 스택에 대해 shields.io 배지 생성
                for stack_info in stacks[:20]:  # 카테고리당 최대 20개 스택 제한
                    stack_label = stack_info.get('label') if isinstance(stack_info, dict) else stack_info
                    stack_color = stack_info.get('color', '#667eea') if isinstance(stack_info, dict) else '#667eea'
                    stack_key = stack_info.get('key', '') if isinstance(stack_info, dict) else ''
                    
                    # 키가 비어 있으면 라벨을 키로 사용 시도 (소문자로 정규화, 공백을 하이픈으로 교체)
                    if not stack_key and stack_label:
                        # 라벨을 정규화하여 아이콘 찾기 시도 (예: "Node.js" -> "nodejs", "Java" -> "java")
                        normalized_label = stack_label.lower().replace(' ', '-').replace('.', '').replace('++', 'plusplus')
                        # 먼저 정확한 일치 시도
                        if normalized_label in STACK_ICON_MAP:
                            stack_key = normalized_label
                        else:
                            # 변형 시도 (예: "node.js" -> "nodejs", "c++" -> "cpp")
                            variations = [
                                normalized_label.replace('-', ''),
                                normalized_label.replace('.', ''),
                                normalized_label.replace(' ', ''),
                            ]
                            for variant in variations:
                                if variant in STACK_ICON_MAP:
                                    stack_key = variant
                                    break
                    
                    # 매핑에서 아이콘 slug 가져오기
                    icon_slug = STACK_ICON_MAP.get(stack_key) if stack_key else None
                    
                    # 디버그: 아이콘을 찾을 수 없으면 출력 (개발 환경에서만)
                    if not icon_slug and stack_key:
                        print(f"[README] Icon not found for stack_key: '{stack_key}', label: '{stack_label}'")
                    elif not icon_slug:
                        print(f"[README] No stack_key for label: '{stack_label}'")
                    
                    # URL용 색상에서 # 제거
                    color_code = stack_color.replace('#', '')
                    # URL용 특수 문자 이스케이프 (shields.io 형식)
                    # shields.io 형식: label-message-color
                    # 기술 스택 배지의 경우 라벨을 라벨과 메시지 모두로 사용
                    stack_label_escaped = stack_label.replace('-', '--').replace('_', '__').replace(' ', '%20')
                    
                    # 배경색 밝기에 따라 아이콘 색상 결정
                    is_light = _is_light_color(stack_color)
                    icon_color = "black" if is_light else "white"
                    
                    # 선택적 로고가 있는 shields.io 배지 URL 빌드
                    # 형식: https://img.shields.io/badge/{label}-{color}?logo={iconSlug}&logoColor={iconColor}&style=for-the-badge
                    # shields.io는 메시지 없이 label-color 형식을 허용합니다
                    if icon_slug:
                        # Simple Icons 로고 매개변수와 동적 아이콘 색상으로 shields.io 사용
                        badge_url = f"https://img.shields.io/badge/{stack_label_escaped}-{color_code}?logo={icon_slug}&logoColor={icon_color}&style=for-the-badge"
                        readme += f'  <img src="{badge_url}" alt="{stack_label}" />\n'
                    else: 
                        # 대체: 로고 없는 배지
                        badge_url = f"https://img.shields.io/badge/{stack_label_escaped}-{color_code}?style=for-the-badge"
                        readme += f'  <img src="{badge_url}" alt="{stack_label}" />\n'
                 
                readme += "\n</div>\n\n"
    
    # 연락처 섹션 - 각 연락처에 shields.io 배지 사용
    if card.show_contact and card.contacts:
        readme += "## 📬 Contact\n\n"
        readme += '<div align="center">\n\n'
        
        for contact in card.contacts[:6]:  # 최대 6개 연락처 제한
            label = contact.get('label', '')
            value = contact.get('value', '')
            contact_type = contact.get('type', '')
            
            # 값이 있으면 항상 표시 (값은 필수, 라벨은 선택사항)
            if value:
                # 연락처 타입 매핑에서 아이콘 가져오기
                icon_slug = CONTACT_ICON_MAP.get(contact_type) if contact_type else None
                
                # 링크 URL 및 속성 결정
                if value.startswith('http://') or value.startswith('https://'):
                    link = value
                    target_attr = 'target="_blank"'
                    rel_attr = 'rel="noopener noreferrer"'
                elif '@' in value and not value.startswith('http'):
                    link = f"mailto:{value}"
                    target_attr = ''
                    rel_attr = ''
                else:
                    link = f"https://{value}" if not value.startswith('http') else value
                    target_attr = 'target="_blank"'
                    rel_attr = 'rel="noopener noreferrer"'
                
                # 라벨을 대문자 타입 이름으로 사용하거나, contact_type으로 대체
                display_label = label.upper() if label else (contact_type.upper() if contact_type else 'CONTACT')
                
                # 빈 속성을 피하기 위해 조건부로 속성 문자열 빌드
                attrs = f'href="{link}"'
                if target_attr:
                    attrs += f' {target_attr}'
                if rel_attr:
                    attrs += f' {rel_attr}'
                
                # 각 연락처에 대한 shields.io 배지 생성
                # 배지에는 라벨만 사용 (값은 특수 문자가 너무 복잡함)
                # 형식: https://img.shields.io/badge/{label}-{color}?logo={icon_slug}&style=flat
                # shields.io는 특수 문자 이스케이프가 필요합니다:
                # - '-'를 '--'로 교체
                # - '_'를 '__'로 교체
                # - ' '를 '_' 또는 '%20'으로 교체
                def escape_shields_io(text: str) -> str:
                    """shields.io 배지 URL용 텍스트 이스케이프"""
                    return text.replace('-', '--').replace('_', '__').replace(' ', '_')
                
                escaped_label = escape_shields_io(display_label)
                
                # 연락처 배지에 중립 색상 사용
                badge_color = "0077B5"  # 기본값으로 LinkedIn 파란색
                
                if icon_slug:
                    # Simple Icons 로고가 있는 shields.io 배지 사용
                    badge_url = f"https://img.shields.io/badge/{escaped_label}-{badge_color}?logo={icon_slug}&logoColor=white&style=flat"
                else:
                    # 대체: 로고 없는 배지
                    badge_url = f"https://img.shields.io/badge/{escaped_label}-{badge_color}?style=flat"
                
                # 값이 툴팁인 클릭 가능한 배지 링크 생성
                readme += f'  <a {attrs} title="{value}">\n'
                readme += f'    <img src="{badge_url}" alt="{display_label}: {value}" />\n'
                readme += f'  </a>\n'
        
        readme += "\n</div>\n\n"
    
    # 백준 티어 섹션 (Solved.ac 배지) - 연락처 아래
    baekjoon_id = getattr(card, "baekjoon_id", None)
    if getattr(card, "show_baekjoon", False) and baekjoon_id:
        handle = baekjoon_id
        readme += "## 🧩 Baekjoon Tier\n\n"
        readme += '<div align="center">\n\n'
        readme += f'[![Solved.ac Profile](http://mazassumnida.wtf/api/v2/generate_badge?boj={handle})](https://solved.ac/{handle}/)\n\n'
        readme += "</div>\n\n"

    # 레포지토리 섹션 - 배너 이미지로 표시
    repositories = getattr(card, "repositories", [])
    if repositories and len(repositories) > 0:
        readme += "## 📂 Repositories\n\n"
        readme += '<div align="left">\n\n'
        
        for index, repo in enumerate(repositories):
            repo_url = html_escape.escape(repo.get("html_url", ""))
            repo_name = html_escape.escape(repo.get("name", ""))
            
            # 레포지토리 배너 이미지 URL 생성
            banner_url = f"{settings.api_base_url}/profiles/public/{github_login}/cards/{card.id}/repositories/{index}/banner"
            banner_url = _remove_port_from_url(banner_url)
            
            # 이미지 링크로 표시
            readme += f'<a href="{repo_url}" target="_blank" rel="noopener noreferrer">\n'
            readme += f'  <img src="{banner_url}" alt="{repo_name}" />\n'
            readme += f'</a>\n\n'
        
        readme += "</div>\n\n"

    # GitHub 통계 섹션
    if card.show_github_stats:
        readme += "## 🏅 GitHub Stats\n\n"
        readme += '<div align="center">\n\n'
        
        # github-readme-stats를 사용한 GitHub 통계 카드
        readme += f'  <img src="https://github-readme-stats.vercel.app/api?username={github_login}&show_icons=true&theme=default" alt="{github_login} stats" />\n'
        readme += f'  <img src="https://github-readme-stats.vercel.app/api/top-langs/?username={github_login}&layout=compact&theme=default" alt="Top Languages" />\n'
        
        readme += "\n</div>\n\n"
    
    # Footer
    readme += f"""---
<div align="center">
  <p>Made with ❤️ using <a href="https://www.gitcard.kr">GitCard</a></p>
</div>
"""
    
    return readme
