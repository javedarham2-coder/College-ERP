from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    postgres_host: str = "127.0.0.1"
    postgres_port: int = 5432
    postgres_db: str = "college_erp"
    postgres_user: str = "erp_user"
    postgres_password: str = Field(validation_alias="POSTGRES_PASSWORD")

    # Development-only admission review endpoints.
    # Keep disabled unless explicitly enabled in the local environment.
    enable_dev_review_endpoints: bool = False

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()