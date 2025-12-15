"""
Profile card export utilities.

Functions to export profile cards as:
- Markdown format (for GitHub README)
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


def generate_markdown(card: ProfileCard, github_login: str) -> str:
    """
    Generate markdown representation of a profile card.
    
    Args:
        card: ProfileCard instance
        github_login: GitHub username
        
    Returns:
        Markdown string
    """
    markdown = f"""# {card.name}

{card.tagline or ''}

## {card.title}

"""
    
    # Stacks section
    if card.show_stacks and card.stacks:
        markdown += "### 🛠️ Tech Stack\n\n"
        for stack in card.stacks:
            stack_label = stack.get('label', stack.get('key', ''))
            if stack_label:
                markdown += f"- {stack_label}\n"
        markdown += "\n"
    
    # Contact section
    if card.show_contact and card.contacts:
        markdown += "### 📧 Contact\n\n"
        for contact in card.contacts:
            label = contact.get('label', '')
            value = contact.get('value', '')
            if label and value:
                if 'http' in value.lower() or 'www' in value.lower():
                    markdown += f"- **{label}**: [{value}]({value})\n"
                else:
                    markdown += f"- **{label}**: {value}\n"
        markdown += "\n"
    
    # Card link
    card_url = f"{settings.frontend_base_url}/dashboard/{github_login}/cards/{card.id}"
    markdown += f"---\n\n[![GitCard]({card_url})]({card_url})\n"
    
    return markdown


def generate_simple_markdown_badge(card: ProfileCard, github_login: str) -> str:
    """
    Generate a simple markdown badge/link for GitHub README.
    
    Args:
        card: ProfileCard instance
        github_login: GitHub username
        
    Returns:
        Simple markdown badge string
    """
    card_url = f"{settings.frontend_base_url}/dashboard/{github_login}/cards/{card.id}"
    return f"[![GitCard]({card_url})]({card_url})"


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
    width: int = 800,
    height: int = 600
) -> Optional[bytes]:
    """
    Generate PNG image from profile card page using Playwright.
    
    Args:
        card: ProfileCard instance
        github_login: GitHub username
        width: Screenshot width in pixels
        height: Screenshot height in pixels
        
    Returns:
        PNG image bytes, or None if Playwright is not available
    """
    if not PLAYWRIGHT_AVAILABLE:
        return None
    
    try:
        url = f"{settings.frontend_base_url}/dashboard/{github_login}/cards/{card.id}"
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page(viewport={"width": width, "height": height})
            await page.goto(url, wait_until="networkidle", timeout=10000)
            
            # Wait for content to load
            await page.wait_for_timeout(2000)
            
            # Take screenshot
            screenshot = await page.screenshot(type="png", full_page=True)
            
            await browser.close()
            return screenshot
    except Exception as e:
        print(f"Error generating screenshot: {e}")
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
    height = 420

    # Stacks text (간단히 한 줄로 이어붙임)
    stacks_text = ""
    if card.show_stacks and card.stacks:
        labels = [
            html_escape.escape(s.get("label") or s.get("key") or "")
            for s in card.stacks
            if (s.get("label") or s.get("key"))
        ]
        if labels:
            stacks_text = " | ".join(labels)

    # Contacts text (간단 텍스트 형태로)
    contacts_text = ""
    if card.show_contact and card.contacts:
        pairs = []
        for c in card.contacts:
            label = html_escape.escape(c.get("label") or "")
            value = html_escape.escape(c.get("value") or "")
            if label and value:
                pairs.append(f"{label}: {value}")
        if pairs:
            contacts_text = " • ".join(pairs)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
  <defs>
    <linearGradient id="bannerGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{primary}" />
      <stop offset="100%" stop-color="{secondary}" />
    </linearGradient>
    <filter id="cardShadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="4" stdDeviation="8" flood-color="rgba(0,0,0,0.15)" />
    </filter>
  </defs>
  <title id="title">GitCard - {name}</title>
  <desc id="desc">GitHub 프로필 카드</desc>

  <!-- Card background -->
  <rect x="0" y="0" width="{width}" height="{height}" rx="16" ry="16" fill="#ffffff" filter="url(#cardShadow)" />

  <!-- Banner -->
  <rect x="0" y="0" width="{width}" height="180" rx="16" ry="16" fill="url(#bannerGradient)" />

  <!-- Name -->
  <text x="{width/2}" y="80" text-anchor="middle" fill="#ffffff" font-size="32" font-weight="700" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif">
    Hello World 👋 I'm {name}!
  </text>

  <!-- Title -->
  <text x="{width/2}" y="120" text-anchor="middle" fill="#ffffff" font-size="20" font-weight="500" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif">
    {title}
  </text>
"""

    if tagline:
        svg += f"""  <!-- Tagline -->
  <text x="{width/2}" y="150" text-anchor="middle" fill="#f8f9fa" font-size="16" font-weight="400" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif">
    {tagline}
  </text>
"""

    current_y = 210

    # Stacks section (optional)
    if stacks_text:
        svg += f"""  <!-- Stacks Section -->
  <text x="40" y="{current_y}" fill="#333333" font-size="18" font-weight="700" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif">
    🛠 Tech Stack
  </text>
  <text x="40" y="{current_y + 30}" fill="#495057" font-size="14" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif">
    {stacks_text}
  </text>
"""
        current_y += 70

    # Contact section (optional)
    if contacts_text:
        svg += f"""  <!-- Contact Section -->
  <text x="40" y="{current_y}" fill="#333333" font-size="18" font-weight="700" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif">
    📧 Contact
  </text>
  <text x="40" y="{current_y + 30}" fill="#495057" font-size="14" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif">
    {contacts_text}
  </text>
"""
        current_y += 70

    # GitHub stats section (optional, uses cached stats if available)
    if stats:
        repos = stats.get("repositories") or 0
        stars = stats.get("stars") or 0
        followers = stats.get("followers") or 0
        following = stats.get("following") or 0
        contributions = stats.get("contributions") or 0

        stats_y = current_y + 10
        box_w = (width - 80) / 5
        box_h = 80

        def stat_box(x_index: int, label: str, value: int) -> str:
            x = 40 + x_index * (box_w + 4)
            return f"""
  <g>
    <rect x="{x}" y="{stats_y}" width="{box_w}" height="{box_h}" rx="10" ry="10" fill="{primary}" opacity="0.9" />
    <text x="{x + box_w/2}" y="{stats_y + 32}" text-anchor="middle" fill="#ffffff" font-size="22" font-weight="700" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif">{value}</text>
    <text x="{x + box_w/2}" y="{stats_y + 56}" text-anchor="middle" fill="#f1f3f5" font-size="12" font-weight="500" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif">{label}</text>
  </g>"""

        svg += "  <!-- GitHub Stats Section -->\n"
        svg += stat_box(0, "Repos", repos)
        svg += stat_box(1, "Stars", stars)
        svg += stat_box(2, "Followers", followers)
        svg += stat_box(3, "Following", following)
        svg += stat_box(4, "Contribs", contributions)

    svg += "\n</svg>"
    return svg


def generate_svg_markdown(card: ProfileCard, github_login: str) -> str:
    """
    Generate markdown snippet that embeds the SVG card in GitHub README.
    """
    svg_url = f"{settings.api_base_url}/api/profiles/public/{github_login}/cards/{card.id}/svg"
    card_url = f"{settings.frontend_base_url}/dashboard/{github_login}/cards/{card.id}"
    # 이미지(SVG)를 클릭하면 공개 카드 페이지로 이동하도록 링크 감싸기
    return f"[![GitCard]({svg_url})]({card_url})"
