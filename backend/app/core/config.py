from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "AI News Briefing MVP"
    api_prefix: str = "/api"
    secret_key: str = "dev-secret-change-me"
    access_token_expire_minutes: int = 10080
    database_url: str = "postgresql+psycopg://news:news@postgres:5432/news"
    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:3000"])
    briefing_focus_ratio: float = 0.7
    briefing_general_ratio: float = 0.3
    ranking_topic_weight: float = 0.34
    ranking_importance_weight: float = 0.28
    ranking_recency_weight: float = 0.16
    ranking_source_diversity_weight: float = 0.12
    ranking_novelty_weight: float = 0.10
    default_briefing_length_minutes: int = 6
    mock_news_mode: bool = True
    newsapi_key: str | None = None
    media_dir: str = str(BASE_DIR / "media")
    frontend_url: str = "http://localhost:3000"
    backend_public_url: str = "http://localhost:8000"
    admin_email: str = "admin@example.com"
    admin_password: str = "Admin123456!"
    admin_full_name: str = "Local Admin"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
