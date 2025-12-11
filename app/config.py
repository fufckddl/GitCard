"""
Application configuration using Pydantic Settings.

Loads environment variables from .env file for:
- GitHub OAuth credentials (Client ID, Client Secret, Redirect URI)
- JWT secret for token signing
- Frontend base URL for post-login redirect
"""
from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Optional


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    GitHub OAuth requires:
    - GITHUB_CLIENT_ID: Your OAuth App's Client ID from GitHub Developer Settings
    - GITHUB_CLIENT_SECRET: Your OAuth App's Client Secret (NEVER expose to frontend)
    - GITHUB_REDIRECT_URI: The callback URL registered in GitHub OAuth App settings
                          Must match exactly with what's configured in GitHub
    
    These values are obtained from:
    GitHub → Settings → Developer settings → OAuth Apps → Create/Edit OAuth App
    """
    
    # GitHub OAuth Configuration
    github_client_id: str
    github_client_secret: str
    github_redirect_uri: str
    
    # JWT Configuration
    jwt_secret: str  # Secret key for signing JWT tokens
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24  # Token expiration time in hours
    
    # Frontend Configuration
    frontend_base_url: str  # Base URL of the frontend app (e.g., http://localhost:5173)
    
    # Server Configuration
    api_base_url: str = "http://localhost:8000"
    
    # Database Configuration
    database_url: str = "mysql+pymysql://root:password@localhost:3306/gitcard"
    # Format: mysql+pymysql://username:password@host:port/database_name
    
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",  # Ignore extra environment variables (e.g., VITE_API_BASE_URL for frontend)
    )


# Global settings instance
settings = Settings()

