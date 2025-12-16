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

try:
    from playwright.async_api import async_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False


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
        return None
    
    if format not in ("png", "webp"):
        format = "png"
    
    try:
        url = f"{settings.frontend_base_url}/dashboard/{github_login}/cards/{card.id}"
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            # Large viewport to ensure full card is visible, DPR 2 for sharpness
            page = await browser.new_page(
                viewport={"width": width, "height": 2000},  # Increased height to accommodate full card
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
            
            # Wait for fonts to load
            await page.evaluate("document.fonts.ready")
            
            # Wait for the card container to be visible
            card_selector = '[data-testid="gitcard-root"]'
            try:
                await page.wait_for_selector(card_selector, timeout=10000, state="visible")
            except Exception:
                # Fallback to cardWrapper if testid not found
                card_selector = ".cardWrapper"
                await page.wait_for_selector(card_selector, timeout=10000, state="visible")
            
            # Wait for all images to load
            await page.evaluate("""
                Promise.all(
                    Array.from(document.images).map(img => {
                        if (img.complete) return Promise.resolve();
                        return new Promise((resolve, reject) => {
                            img.onload = resolve;
                            img.onerror = resolve; // Continue even if image fails
                            setTimeout(resolve, 5000); // Timeout after 5s
                        });
                    })
                )
            """)
            
            # Additional wait for layout stability
            await page.wait_for_timeout(1000)
            
            # Get the card element
            card_element = await page.query_selector(card_selector)
            if not card_element:
                # Fallback: try to find the card wrapper
                card_element = await page.query_selector(".cardWrapper")
            
            if card_element:
                # Scroll element into view to ensure it's fully rendered
                await card_element.scroll_into_view_if_needed()
                
                # Wait a bit more for any lazy-loaded content
                await page.wait_for_timeout(500)
                
                # Get bounding box to verify element is fully loaded
                box = await card_element.bounding_box()
                if box and box["height"] > 0:
                    # Screenshot the entire card element (element.screenshot automatically captures full bounding box)
                    screenshot = await card_element.screenshot(type=format)
                else:
                    # If bounding box is invalid, wait more and retry
                    await page.wait_for_timeout(1000)
                    screenshot = await card_element.screenshot(type=format)
            else:
                # Fallback: full page screenshot
                screenshot = await page.screenshot(type=format, full_page=True)
            
            await browser.close()
            return screenshot
    except Exception as e:
        print(f"Error generating screenshot: {e}")
        import traceback
        traceback.print_exc()
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
    
    # Organize stacks by category
    stacks_by_category = {}
    if card.show_stacks and card.stacks:
        for stack in card.stacks:
            category = stack.get('category', 'Other')
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
    
    # Stacks Section
    if card.show_stacks and stacks_by_category:
        html += """  <!-- Stacks Section -->
  <div style="padding: 32px 40px; background: white;">
    <h2 style="font-size: 28px; font-weight: 700; margin: 0 0 24px 0; color: #333;">Stacks</h2>
    <div style="display: flex; flex-direction: column; gap: 24px;">
"""
        for category, stacks in stacks_by_category.items():
            category_escaped = html_escape.escape(category)
            html += f"""      <div style="display: flex; flex-direction: column; gap: 12px;">
        <h3 style="font-size: 18px; font-weight: 600; margin: 0; color: #666; text-transform: uppercase; letter-spacing: 0.5px;">{category_escaped}</h3>
        <div style="display: flex; flex-wrap: wrap; gap: 12px;">
"""
            for stack in stacks:
                stack_label = html_escape.escape(stack.get('label', stack.get('key', '')))
                stack_color = stack.get('color', '#667eea')
                html += f"""          <span style="display: inline-block; padding: 8px 16px; border-radius: 20px; font-size: 14px; font-weight: 600; color: white; background-color: {stack_color}; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);">{stack_label}</span>
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
            is_email = '@' in value
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
            
            html += f"""      <a href="{href}" {target_attr} {rel_attr} style="display: flex; flex-direction: column; padding: 20px; background: white; border-radius: 12px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); text-decoration: none; color: inherit;">
        <span style="font-size: 14px; font-weight: 600; color: #667eea; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px;">{label}</span>
        <span style="font-size: 16px; color: #333; word-break: break-word;">{value}</span>
      </a>
"""
        html += """    </div>
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
    Helper to get two colors for gradients based on card data.
    Falls back to sensible defaults when gradient string is not parsable.
    """
    primary = card.primary_color or "#667eea"
    secondary = "#764ba2"
    gradient = card.gradient or ""
    # Try to extract hex colors from existing gradient
    hex_regex = r"#(?:[A-Fa-f0-9]{3}|[A-Fa-f0-9]{6})"
    import re

    matches = re.findall(hex_regex, gradient)
    if matches:
        primary = matches[0]
        if len(matches) >= 2:
            secondary = matches[1]
        elif matches[0].lower() != primary.lower():
            secondary = matches[0]
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
            
            if label and value:
                svg += f"""  <!-- Contact Card -->
  <rect x="{contact_x}" y="{contact_y}" width="{contact_card_width}" height="{contact_card_height}" rx="12" ry="12" fill="#ffffff" filter="url(#smallShadow)" />
  <text x="{contact_x + 20}" y="{contact_y + 24}" fill="#667eea" font-size="14" font-weight="600" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif" letter-spacing="0.5">
    {label.upper()}
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
