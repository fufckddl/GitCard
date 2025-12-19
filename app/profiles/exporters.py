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

# Contact type to Simple Icons slug mapping (matching contactMeta.ts)
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

# Stack key to Simple Icons slug mapping (matching stackMeta.ts)
# This should be kept in sync with src/shared/stackMeta.ts
STACK_ICON_MAP: Dict[str, str] = {
    # Languages
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
    # Frontend
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
    # Backend
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
    # Database
    "mysql": "mysql",
    "postgresql": "postgresql",
    "sqlite": "sqlite",
    "mariadb": "mariadb",
    "mongodb": "mongodb",
    "redis": "redis",
    "elasticsearch": "elasticsearch",
    "dynamodb": "amazondynamodb",
    "firebase-firestore": "firebase",
    # Infra
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
    # Collaboration
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
    # Tools
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
    Determine if a hex color is light or dark.
    Returns True if light (should use black icon), False if dark (should use white icon).
    
    Uses relative luminance formula: https://www.w3.org/WAI/GL/wiki/Relative_luminance
    """
    # Remove # if present
    hex_color = hex_color.lstrip('#')
    
    # Convert 3-digit hex to 6-digit
    if len(hex_color) == 3:
        hex_color = ''.join([c * 2 for c in hex_color])
    
    # Convert to RGB
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    
    # Calculate relative luminance
    # Using the formula: 0.299*R + 0.587*G + 0.114*B
    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    
    # If luminance is greater than 0.5, it's a light color
    return luminance > 0.5


try:
    from playwright.async_api import async_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

def _check_playwright_browsers() -> bool:
    """Check if Playwright browsers are installed."""
    if not PLAYWRIGHT_AVAILABLE:
        return False
    try:
        import subprocess
        result = subprocess.run(
            ["python", "-m", "playwright", "install", "--dry-run", "chromium"],
            capture_output=True,
            timeout=5
        )
        # If dry-run succeeds, browsers are already installed
        return result.returncode == 0
    except Exception:
        # If check fails, assume browsers might not be installed
        # But still try to use Playwright (might work)
        return True


async def generate_image_url(card: ProfileCard, github_login: str) -> str:
    """
    Generate image URL for profile card.
    Uses the public profile card page URL which can be converted to image.
    
    Args:
        card: ProfileCard instance
        github_login: GitHub username
        
    Returns:
        URL to the profile card page (can be used with screenshot services)
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
    Generate PNG or WebP image from profile card page using Playwright.
    Renders the actual web card UI and clips to the card container only.
    
    Args:
        card: ProfileCard instance
        github_login: GitHub username
        format: Image format ("png" or "webp", default: "png")
        width: Viewport width in pixels (default: 1200)
        height: Viewport height in pixels (default: 700)
        
    Returns:
        Image bytes (PNG or WebP), or None if Playwright is not available
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
            # Very large viewport to ensure full card is visible, DPR 2 for sharpness
            # Use fixed large height instead of dynamic adjustment
            page = await browser.new_page(
                viewport={"width": width, "height": 4000},  # Fixed large height
                device_scale_factor=2
            )
            
            # Disable animations and transitions for deterministic rendering
            await page.add_style_tag(content="""
                * {
                    animation: none !important;
                    transition: none !important;
                }
            """)
            
            # Navigate to the card page
            await page.goto(url, wait_until="networkidle", timeout=30000)
            
            # Wait for the card container to be visible
            card_selector = '[data-testid="gitcard-root"]'
            try:
                await page.wait_for_selector(card_selector, timeout=10000, state="visible")
            except Exception:
                # Fallback to cardWrapper if testid not found
                card_selector = ".cardWrapper"
                await page.wait_for_selector(card_selector, timeout=10000, state="visible")
            
            # Wait for all resources to load completely
            await page.wait_for_load_state("networkidle", timeout=30000)
            
            # Wait for fonts to load
            await page.evaluate("document.fonts.ready")
            await page.wait_for_timeout(500)
            
            # Wait for all images to load completely
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
            
            # Wait for CSS and stylesheets to load
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
            
            # Wait for layout to stabilize (check if element size is stable)
            await page.wait_for_timeout(1000)
            
            # Scroll to top of page first
            await page.evaluate("window.scrollTo(0, 0)")
            await page.wait_for_timeout(500)
            
            # Get the card element
            card_element = await page.query_selector(card_selector)
            if not card_element:
                # Fallback: try to find the card wrapper
                card_element = await page.query_selector(".cardWrapper")
            
            if card_element:
                # Get element's actual dimensions using multiple methods for accuracy
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
                    # Calculate required viewport size
                    # Add extra padding to ensure nothing is cut off
                    padding = 50
                    required_height = element_info['pageY'] + element_info['height'] + padding
                    required_width = element_info['pageX'] + element_info['width'] + padding
                    
                    # Ensure minimum viewport size
                    min_viewport_height = max(required_height, 4000)
                    min_viewport_width = max(required_width, width)
                    
                    # Resize viewport to accommodate full element
                    await page.set_viewport_size({
                        'width': min_viewport_width,
                        'height': min_viewport_height
                    })
                    await page.wait_for_timeout(500)
                    
                    # Reload page to ensure proper rendering with new viewport
                    await page.reload(wait_until="networkidle", timeout=30000)
                    
                    # Wait for all resources to load completely after reload
                    await page.wait_for_load_state("networkidle", timeout=30000)
                    
                    # Wait for fonts to load
                    await page.evaluate("document.fonts.ready")
                    await page.wait_for_timeout(500)
                    
                    # Wait for all images to load completely
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
                    
                    # Wait for CSS and stylesheets
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
                    
                    # Wait for layout to stabilize
                    await page.wait_for_timeout(1500)
                    
                    # Re-query element to get updated position after reload
                    card_element = await page.query_selector(card_selector)
                    if not card_element:
                        card_element = await page.query_selector(".cardWrapper")
                    
                    if card_element:
                        # Get updated element position
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
                            # Scroll to element position
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
                    
                    # Final wait for scroll and layout stabilization
                    await page.wait_for_timeout(1000)
                    
                    # Verify element is fully loaded and stable
                    await page.evaluate("""
                        () => {
                            return new Promise(resolve => {
                                // Wait for any pending animations or transitions
                                requestAnimationFrame(() => {
                                    requestAnimationFrame(() => {
                                        setTimeout(resolve, 500);
                                    });
                                });
                            });
                        }
                    """)
                    
                    # Re-query element after viewport change
                    card_element = await page.query_selector(card_selector)
                    if not card_element:
                        card_element = await page.query_selector(".cardWrapper")
                    
                    if card_element:
                        # Take screenshot - element.screenshot() should capture full element now
                        screenshot = await card_element.screenshot(
                            type=format,
                            timeout=15000
                        )
                    else:
                        # Fallback: full page screenshot
                        screenshot = await page.screenshot(type=format, full_page=True)
                else:
                    # Fallback: try regular element screenshot
                    await card_element.scroll_into_view_if_needed()
                    await page.wait_for_timeout(1000)
                    screenshot = await card_element.screenshot(type=format, timeout=10000)
            else:
                # Fallback: full page screenshot
                screenshot = await page.screenshot(type=format, full_page=True)
            
            await browser.close()
            return screenshot
    except Exception as e:
        error_msg = str(e)
        print(f"Error generating screenshot: {error_msg}")
        import traceback
        traceback.print_exc()
        
        # Check for common Playwright browser installation errors
        if "Executable doesn't exist" in error_msg or "BrowserType.launch" in error_msg:
            print("\n⚠️  Playwright browsers are not installed!")
            print("   Install with: python -m playwright install chromium")
            print("   Or install all browsers: python -m playwright install")
        
        return None


def generate_html(card: ProfileCard, github_login: str) -> str:
    """
    Generate standalone HTML representation of a profile card.
    Uses inline styles matching the actual frontend design.
    
    Args:
        card: ProfileCard instance
        github_login: GitHub username
        
    Returns:
        Complete HTML string with inline styles matching the design
    """
    card_url = f"{settings.frontend_base_url}/dashboard/{github_login}/cards/{card.id}"
    gradient = card.gradient or f"linear-gradient(135deg, {card.primary_color or '#667eea'} 0%, rgb(102, 126, 234) 100%)"
    
    # Escape HTML entities
    name = html_escape.escape(card.name)
    title = html_escape.escape(card.title)
    tagline = html_escape.escape(card.tagline) if card.tagline else ""
    
    # Organize stacks by category (following stackMeta.ts structure)
    # Category order and labels matching stackMeta.ts
    category_order = [
        "language", "frontend", "mobile", "backend", "database",
        "infra", "collaboration", "ai-ml", "testing", "tool"
    ]
    # Category labels (Korean / English) for HTML export
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
            # Use category from stack data (should match stackMeta.ts categories)
            # Normalize category to lowercase to handle case variations
            category_raw = stack.get('category', 'tool')
            category = category_raw.lower() if isinstance(category_raw, str) else 'tool'
            
            # Ensure category is in category_order, otherwise default to 'tool'
            if category not in category_order:
                category = 'tool'
            
            if category not in stacks_by_category:
                stacks_by_category[category] = []
            stacks_by_category[category].append(stack)
    
    # Build HTML with exact styling from CSS
    html = f"""<div style="max-width: 900px; margin: 0 auto; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1); font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;">
  <!-- Banner Section -->
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
                    # Use label and color from stack data (should match stackMeta.ts)
                    stack_label = html_escape.escape(stack.get('label', stack.get('key', '')))
                    stack_color = stack.get('color', '#667eea')
                    stack_key = stack.get('key', '')
                    
                    # If key is empty, try to use label as key (normalize to lowercase, replace spaces with hyphens)
                    if not stack_key and stack_label:
                        # Try to find icon by normalizing label (e.g., "Node.js" -> "nodejs", "Java" -> "java")
                        normalized_label = stack_label.lower().replace(' ', '-').replace('.', '').replace('++', 'plusplus')
                        # Try exact match first
                        if normalized_label in STACK_ICON_MAP:
                            stack_key = normalized_label
                        else:
                            # Try variations (e.g., "node.js" -> "nodejs", "c++" -> "cpp")
                            variations = [
                                normalized_label.replace('-', ''),
                                normalized_label.replace('.', ''),
                                normalized_label.replace(' ', ''),
                            ]
                            for variant in variations:
                                if variant in STACK_ICON_MAP:
                                    stack_key = variant
                                    break
                    
                    # Special case: Java should display as "OpenJDK" in HTML
                    if stack_key == 'java':
                        stack_label = 'OpenJDK'
                    
                    icon_slug = STACK_ICON_MAP.get(stack_key) if stack_key else None
                    
                    # Debug: Print if icon not found
                    if not icon_slug and stack_key:
                        print(f"[HTML] Icon not found for stack_key: '{stack_key}', label: '{stack_label}'")
                    elif not icon_slug and stack_label:
                        print(f"[HTML] No stack_key for label: '{stack_label}'")
                    
                    # Determine icon color based on background color brightness
                    is_light = _is_light_color(stack_color)
                    icon_color = "black" if is_light else "white"
                    # Also adjust text color based on background
                    text_color = "black" if is_light else "white"
                    
                    # Build badge HTML with optional icon
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
    
    # Contact Section
    if card.show_contact and card.contacts:
        html += """  <!-- Contact Section -->
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
            
            # Build icon HTML
            icon_html = ""
            if icon_slug:
                icon_html = f'<img src="https://cdn.simpleicons.org/{icon_slug}/000000" alt="{label}" style="width: 32px; height: 32px; object-fit: contain;" />'
                print(f"[HTML] Generated icon HTML for contact_type: '{contact_type}' with icon_slug: '{icon_slug}'")
            elif contact_type:
                # If type is specified but icon not found, log warning
                print(f"[HTML] Warning: Contact type '{contact_type}' specified but icon not in CONTACT_ICON_MAP")
            
            # Display contact card with icon, label, and value
            # Always display if value exists (value is required, label is optional)
            if value:
                # Use label as uppercase type name, or fallback to contact_type
                display_label = label.upper() if label else (contact_type.upper() if contact_type else 'CONTACT')
                
                # Build attributes string conditionally to avoid empty attributes
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
    
    # Baekjoon Tier Section (Solved.ac badge) - placed below Contact
    baekjoon_id = getattr(card, "baekjoon_id", None)
    if getattr(card, "show_baekjoon", False) and baekjoon_id:
        safe_handle = html_escape.escape(baekjoon_id)
        badge_src = f"http://mazassumnida.wtf/api/v2/generate_badge?boj={safe_handle}"
        solved_profile_url = f"https://solved.ac/{safe_handle}/"
        html += f"""  <!-- Baekjoon Tier Section -->
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
        <div style="font-size: 14px; font-weight: 500; opacity: 0.9; text-transform: uppercase; letter-spacing: 0.5px;">Contributions</div>
      </div>
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
    
    html += "</div>"
    
    return html


def _extract_gradient_colors(card: ProfileCard) -> tuple[str, str]:
    """
    Extract gradient colors from card.gradient field in database.
    
    Supports formats:
    - linear-gradient(135deg, #667eea 0%, #764ba2 100%)  (hex + hex)
    - linear-gradient(135deg, rgb(102, 126, 234) 0%, rgb(118, 75, 162) 100%)  (rgb + rgb)
    - linear-gradient(135deg, #667eea 0%, rgb(106, 104, 240) 100%)  (hex + rgb) - MIXED FORMAT
    - linear-gradient(135deg, rgb(102, 126, 234) 0%, #764ba2 100%)  (rgb + hex) - MIXED FORMAT
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
        # No colors found, try fallback patterns
        # Pattern 1: Try hex only
        # IMPORTANT: {6} must come before {3} to match 6-digit hex before 3-digit hex
        hex_regex = r"#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})"
        hex_matches = re.findall(hex_regex, gradient_clean)
        print(f"[COLOR EXTRACT FALLBACK] Hex matches: {hex_matches}")
        if hex_matches:
            primary = normalize_hex(hex_matches[0])
            secondary = normalize_hex(hex_matches[1]) if len(hex_matches) >= 2 else default_secondary
            print(f"[COLOR EXTRACT FALLBACK] Using hex fallback - primary={primary}, secondary={secondary}")
            return primary, secondary
        
        # Pattern 2: Try RGB only
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
        
        # All parsing failed - use defaults
        return default_primary, default_secondary
    
    # Ensure primary and secondary are different
    if primary == secondary:
        secondary = default_secondary
    
    # Debug: Print extracted colors
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
    
    # Stacks를 카테고리별로 그룹화
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
    
    # Stacks 섹션 높이 계산
    stacks_height = 0
    if stacks_by_category:
        stacks_height += 28 + 24  # "Stacks" 헤더
        for category, stacks in stacks_by_category.items():
            stacks_height += 18 + 12  # 카테고리 라벨 + 간격
            # 뱃지 행 계산
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
    
    # Contact 섹션 높이 계산
    contact_height = 0
    if card.show_contact and card.contacts:
        contact_height += 28 + 24  # "Contact" 헤더
        # 그리드 레이아웃: 최소 2열, 각 카드 높이 80px
        num_contacts = min(len(card.contacts), 6)  # 최대 6개
        cols = min(2, num_contacts)
        rows = (num_contacts + cols - 1) // cols
        contact_height += rows * 80 + (rows - 1) * 16  # 카드 높이 + 간격
        contact_height += section_padding * 2
    
    # GitHub Stats 섹션 높이 계산
    stats_height = 0
    if card.show_github_stats:
        stats_height += 28 + 24  # "Github-stats" 헤더
        # 5개 박스: 3개 상단, 2개 하단
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
            
            # 뱃지 렌더링
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

    # Contact section - 카드 형태로 렌더링
    if card.show_contact and card.contacts:
        svg += f"""  <!-- Contact Section Background -->
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
            
            # Always display if value exists (value is required, label is optional)
            if value:
                # Use label as uppercase type name, or fallback to contact_type
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

    # GitHub stats section - 그라데이션 배경 카드로 렌더링
    if card.show_github_stats:
        svg += f"""  <!-- GitHub Stats Section -->
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
            contributions = stats.get("contributions") or 0
            
            # 5개 박스: 3개 상단, 2개 하단
            box_w = (width - 80 - 40) // 3  # 3열
            box_h = 100
            box_gap = 20
            
            stats_data = [
                ("CONTRIBUTIONS", contributions),
                ("REPOSITORIES", repos),
                ("STARS", stars),
                ("FOLLOWERS", followers),
                ("FOLLOWING", following),
            ]
            
            for i, (label, value) in enumerate(stats_data):
                if i < 3:
                    # 상단 행
                    x = 40 + i * (box_w + box_gap)
                    y = stats_start_y
                else:
                    # 하단 행 (중앙 정렬)
                    x = 40 + (i - 3) * (box_w + box_gap) + (box_w + box_gap) // 2
                    y = stats_start_y + box_h + box_gap
                
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
    Remove port number from URL (e.g., :8000) for production use.
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
    Generate markdown snippet that embeds the card image in GitHub README.
    Uses the new image endpoint (PNG/WebP) instead of SVG for better design matching.
    """
    # Use image endpoint instead of SVG for accurate design rendering
    image_url = f"{settings.api_base_url}/api/profiles/public/{github_login}/cards/{card.id}/image?format=png"
    card_url = f"{settings.frontend_base_url}/dashboard/{github_login}/cards/{card.id}"
    
    # Remove port from URLs for production (e.g., :8000)
    image_url = _remove_port_from_url(image_url)
    card_url = _remove_port_from_url(card_url)
    
    # 이미지를 클릭하면 공개 카드 페이지로 이동하도록 링크 감싸기
    return f"[![GitCard]({image_url})]({card_url})"


def _hex_to_url_color(hex_color: str) -> str:
    """
    Convert hex color to URL-encoded format for capsule-render.
    Example: #667eea -> %23667eea
    """
    if hex_color.startswith('#'):
        return f"%23{hex_color[1:]}"
    return hex_color.replace('#', '%23')


def _extract_primary_color_for_banner(card: ProfileCard) -> str:
    """
    Extract primary color from card for banner.
    Falls back to default purple gradient color.
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
    Generate SVG banner with gradient background using pure SVG elements.
    This ensures reliable rendering in GitHub README without foreignObject.
    
    Args:
        card: ProfileCard instance
        
    Returns:
        SVG string with gradient banner
    """
    # Extract gradient colors from database
    # card.gradient contains the gradient string from database (e.g., "linear-gradient(135deg, #667eea 0%, rgb(106, 104, 240) 100%)")
    # IMPORTANT: This must match the colors extracted by the frontend in PublicProfileCardPage.tsx
    primary, secondary = _extract_gradient_colors(card)
    
    # Debug: Ensure we have valid colors (fallback if extraction fails)
    if not primary or not primary.startswith('#'):
        primary = card.primary_color or "#667eea"
    if not secondary or not secondary.startswith('#'):
        secondary = "#764ba2"
    
    # Debug: Print to console for debugging
    print(f"[SVG BANNER] card_id={card.id}, gradient={card.gradient}, extracted primary={primary}, secondary={secondary}")
    
    # Escape HTML entities for SVG text
    name = html_escape.escape(card.name)
    title = html_escape.escape(card.title)
    tagline = html_escape.escape(card.tagline or "")
    
    # Banner dimensions
    width = 900
    height = 200
    
    # Calculate center x position
    center_x = width / 2
    
    # Build SVG with pure SVG elements (no foreignObject)
    # Use objectBoundingBox with percentage coordinates for GitHub README compatibility
    # GitHub README renders gradients better with objectBoundingBox and percentage values
    # For 135deg gradient: from top-left (0%,0%) to bottom-right (100%, 100%)
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
    Generate SVG contact section with contact cards in a grid layout.
    This ensures reliable rendering in GitHub README without CSS dependencies.
    
    Args:
        card: ProfileCard instance
        
    Returns:
        SVG string with contact cards
    """
    if not card.show_contact or not card.contacts:
        return ""
    
    # Filter contacts with values
    valid_contacts = [c for c in card.contacts[:6] if c.get('value')]
    
    if not valid_contacts:
        return ""
    
    # Contact card dimensions
    card_width = 280
    card_height = 100
    card_padding = 20
    card_gap = 16
    cards_per_row = 3
    
    # Calculate grid dimensions
    num_cards = len(valid_contacts)
    num_rows = (num_cards + cards_per_row - 1) // cards_per_row
    width = (card_width * cards_per_row) + (card_gap * (cards_per_row - 1)) + (card_padding * 2)
    height = (card_height * num_rows) + (card_gap * (num_rows - 1)) + (card_padding * 2)
    
    # Build SVG
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
    
    # Generate contact cards
    for i, contact in enumerate(valid_contacts):
        row = i // cards_per_row
        col = i % cards_per_row
        
        x = card_padding + (col * (card_width + card_gap))
        y = card_padding + (row * (card_height + card_gap))
        
        label = html_escape.escape(contact.get('label', ''))
        value = html_escape.escape(contact.get('value', ''))
        contact_type = contact.get('type', '')
        
        # Use label as uppercase type name, or fallback to contact_type
        display_label = label.upper() if label else (contact_type.upper() if contact_type else 'CONTACT')
        
        # Truncate value if too long
        display_value = value[:30] + '...' if len(value) > 30 else value
        
        # Get icon slug from contact type mapping
        icon_slug = CONTACT_ICON_MAP.get(contact_type) if contact_type else None
        
        # Contact card
        svg += f'''  <!-- Contact Card {i+1} -->
  <rect x="{x}" y="{y}" width="{card_width}" height="{card_height}" rx="12" ry="12" fill="#ffffff" filter="url(#contactShadow)"/>
'''
        
        # Icon using shields.io (GitHub README compatible)
        if icon_slug:
            # Use shields.io icon-only badge for reliable rendering in GitHub README
            # Format: https://img.shields.io/badge/-{icon_slug}-000000?logo={icon_slug}&logoColor=white&style=flat
            icon_badge_url = f"https://img.shields.io/badge/-{icon_slug}-000000?logo={icon_slug}&logoColor=white&style=flat"
            svg += f'''  <image x="{x + 20}" y="{y + 20}" width="32" height="32" href="{icon_badge_url}" preserveAspectRatio="xMidYMid meet"/>
'''
        else:
            # Fallback: simple circle icon
            svg += f'''  <circle cx="{x + 36}" cy="{y + 36}" r="16" fill="#e0e0e0"/>
'''
        
        # Label text
        svg += f'''  <text x="{x + 60}" y="{y + 35}" fill="#667eea" font-size="12" font-weight="600" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif" text-transform="uppercase" letter-spacing="0.5">
    {display_label}
  </text>
'''
        
        # Value text
        svg += f'''  <text x="{x + 20}" y="{y + 70}" fill="#333333" font-size="14" font-weight="400" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif">
    {display_value}
  </text>
'''
    
    svg += '</svg>'
    
    return svg


def generate_readme_template(
    card: ProfileCard,
    github_login: str,
    stats: Optional[Dict[str, Optional[int]]] = None,
) -> str:
    """
    Generate a GitHub README-safe markdown template.    
    
    Uses:
    - SVG banner as image URL (capsule-render 방식) - 안정적인 렌더링 보장
    - shields.io badges for stacks and contacts
    - github-readme-stats for GitHub statistics
    - GitCard image endpoint for the custom card
    
    This template is guaranteed to work in GitHub README as it uses
    image URLs for SVG (like capsule-render), markdown headings, minimal HTML (div align, img, a),
    and external image services that GitHub supports.
    
    Args:
        card: ProfileCard instance
        github_login: GitHub username
        stats: Optional GitHub stats dictionary
        
    Returns:
        Complete README markdown template
    """
    # URLs
    banner_url = f"{settings.api_base_url}/profiles/public/{github_login}/cards/{card.id}/banner"
    card_url = f"{settings.frontend_base_url}/dashboard/{github_login}/cards/{card.id}"
    
    # Remove port from URLs for production
    banner_url = _remove_port_from_url(banner_url)
    card_url = _remove_port_from_url(card_url)
    
    # Build README template with banner as image URL (capsule-render 방식)
    # 배너는 사용자가 선택한 그라데이션 색상을 사용
    readme = f'''<div align="center">
  <img src="{banner_url}" alt="GitCard Banner" />
</div>

'''
    
    # Stacks Section
    if card.show_stacks and card.stacks:
        readme += "## 🛠️ Tech Stacks\n\n"
        
        # Category order and labels matching stackMeta.ts
        category_order = [
            "language", "frontend", "mobile", "backend", "database",
            "infra", "collaboration", "ai-ml", "testing", "tool"
        ]
        # Category labels (Korean / English) for README export
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
        
        # Group stacks by category
        stacks_by_category = {}
        for stack in card.stacks:
            # Normalize category to lowercase to handle case variations
            category_raw = stack.get('category', 'tool')
            category = category_raw.lower() if isinstance(category_raw, str) else 'tool'
            
            # Ensure category is in category_order, otherwise default to 'tool'
            if category not in category_order:
                category = 'tool'
            
            if category not in stacks_by_category:
                stacks_by_category[category] = []
            label = stack.get('label') or stack.get('key', '')
            color = stack.get('color', '#667eea')
            stack_key = stack.get('key', '')  # Get key for icon lookup
            if label:
                stacks_by_category[category].append({'label': label, 'color': color, 'key': stack_key})
        
        # Render categories in order matching stackMeta.ts
        for category in category_order:
            if category in stacks_by_category and stacks_by_category[category]:
                stacks = stacks_by_category[category]
                category_label = category_labels.get(category, category.upper())
                
                # Add category heading
                readme += f"### {category_label}\n\n"
                # Get alignment from card
                alignment = card.stack_alignment or 'center'
                align_value = alignment  # 'left', 'center', or 'right'
                readme += f'<div align="{align_value}">\n\n'
                
                # Generate shields.io badges for each stack in this category
                for stack_info in stacks[:20]:  # Limit to 20 stacks per category
                    stack_label = stack_info.get('label') if isinstance(stack_info, dict) else stack_info
                    stack_color = stack_info.get('color', '#667eea') if isinstance(stack_info, dict) else '#667eea'
                    stack_key = stack_info.get('key', '') if isinstance(stack_info, dict) else ''
                    
                    # If key is empty, try to use label as key (normalize to lowercase, replace spaces with hyphens)
                    if not stack_key and stack_label:
                        # Try to find icon by normalizing label (e.g., "Node.js" -> "nodejs", "Java" -> "java")
                        normalized_label = stack_label.lower().replace(' ', '-').replace('.', '').replace('++', 'plusplus')
                        # Try exact match first
                        if normalized_label in STACK_ICON_MAP:
                            stack_key = normalized_label
                        else:
                            # Try variations (e.g., "node.js" -> "nodejs", "c++" -> "cpp")
                            variations = [
                                normalized_label.replace('-', ''),
                                normalized_label.replace('.', ''),
                                normalized_label.replace(' ', ''),
                            ]
                            for variant in variations:
                                if variant in STACK_ICON_MAP:
                                    stack_key = variant
                                    break
                    
                    # Get icon slug from mapping
                    icon_slug = STACK_ICON_MAP.get(stack_key) if stack_key else None
                    
                    # Debug: Print if icon not found (only in development)
                    if not icon_slug and stack_key:
                        print(f"[README] Icon not found for stack_key: '{stack_key}', label: '{stack_label}'")
                    elif not icon_slug:
                        print(f"[README] No stack_key for label: '{stack_label}'")
                    
                    # Remove # from color for URL
                    color_code = stack_color.replace('#', '')
                    # Escape special characters for URL (shields.io format)
                    # shields.io format: label-message-color
                    # For tech stack badges, we use label as both label and message
                    stack_label_escaped = stack_label.replace('-', '--').replace('_', '__').replace(' ', '%20')
                    
                    # Determine icon color based on background color brightness
                    is_light = _is_light_color(stack_color)
                    icon_color = "black" if is_light else "white"
                    
                    # Build shields.io badge URL with optional logo
                    # Format: https://img.shields.io/badge/{label}-{color}?logo={iconSlug}&logoColor={iconColor}&style=for-the-badge
                    # shields.io allows label-color format without message
                    if icon_slug:
                        # Use shields.io with Simple Icons logo parameter and dynamic icon color
                        badge_url = f"https://img.shields.io/badge/{stack_label_escaped}-{color_code}?logo={icon_slug}&logoColor={icon_color}&style=for-the-badge"
                        readme += f'  <img src="{badge_url}" alt="{stack_label}" />\n'
                    else: 
                        # Fallback to badge without logo
                        badge_url = f"https://img.shields.io/badge/{stack_label_escaped}-{color_code}?style=for-the-badge"
                        readme += f'  <img src="{badge_url}" alt="{stack_label}" />\n'
                 
                readme += "\n</div>\n\n"
    
    # Contact Section - Use shields.io badges for each contact
    if card.show_contact and card.contacts:
        readme += "## 📬 Contact\n\n"
        readme += '<div align="center">\n\n'
        
        for contact in card.contacts[:6]:  # Limit to 6 contacts
            label = contact.get('label', '')
            value = contact.get('value', '')
            contact_type = contact.get('type', '')
            
            # Always display if value exists (value is required, label is optional)
            if value:
                # Get icon from contact type mapping
                icon_slug = CONTACT_ICON_MAP.get(contact_type) if contact_type else None
                
                # Determine link URL and attributes
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
                
                # Use label as uppercase type name, or fallback to contact_type
                display_label = label.upper() if label else (contact_type.upper() if contact_type else 'CONTACT')
                
                # Build attributes string conditionally to avoid empty attributes
                attrs = f'href="{link}"'
                if target_attr:
                    attrs += f' {target_attr}'
                if rel_attr:
                    attrs += f' {rel_attr}'
                
                # Create shields.io badge for each contact
                # Use only label in badge (value is too complex with special characters)
                # Format: https://img.shields.io/badge/{label}-{color}?logo={icon_slug}&style=flat
                # shields.io requires special character escaping:
                # - Replace '-' with '--'
                # - Replace '_' with '__'
                # - Replace ' ' with '_' or '%20'
                def escape_shields_io(text: str) -> str:
                    """Escape text for shields.io badge URL"""
                    return text.replace('-', '--').replace('_', '__').replace(' ', '_')
                
                escaped_label = escape_shields_io(display_label)
                
                # Use a neutral color for contact badges
                badge_color = "0077B5"  # LinkedIn blue as default
                
                if icon_slug:
                    # Use shields.io badge with Simple Icons logo
                    badge_url = f"https://img.shields.io/badge/{escaped_label}-{badge_color}?logo={icon_slug}&logoColor=white&style=flat"
                else:
                    # Fallback: badge without logo
                    badge_url = f"https://img.shields.io/badge/{escaped_label}-{badge_color}?style=flat"
                
                # Create clickable badge link with value as tooltip
                readme += f'  <a {attrs} title="{value}">\n'
                readme += f'    <img src="{badge_url}" alt="{display_label}: {value}" />\n'
                readme += f'  </a>\n'
        
        readme += "\n</div>\n\n"
    
    # Baekjoon Tier Section (Solved.ac badge) - below Contact
    baekjoon_id = getattr(card, "baekjoon_id", None)
    if getattr(card, "show_baekjoon", False) and baekjoon_id:
        handle = baekjoon_id
        readme += "## 🧩 Baekjoon Tier\n\n"
        readme += '<div align="center">\n\n'
        readme += f'[![Solved.ac Profile](http://mazassumnida.wtf/api/v2/generate_badge?boj={handle})](https://solved.ac/{handle}/)\n\n'
        readme += "</div>\n\n"

    # GitHub Stats Section
    if card.show_github_stats:
        readme += "## 🏅 GitHub Stats\n\n"
        readme += '<div align="center">\n\n'
        
        # GitHub stats cards using github-readme-stats
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
