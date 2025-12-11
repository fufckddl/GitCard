"""
Profile card export utilities.

Functions to export profile cards as:
- Markdown format (for GitHub README)
- Image format (PNG/JPEG)
"""
from typing import Optional
from io import BytesIO
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
