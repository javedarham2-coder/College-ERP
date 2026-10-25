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

    # JWT key is supplied only through the environment or local .env file.
    jwt_secret_key: str = Field(default="", validation_alias="JWT_SECRET_KEY")
    jwt_access_token_expire_minutes: int = Field(default=30, ge=1, le=1440, validation_alias="JWT_ACCESS_TOKEN_EXPIRE_MINUTES")

    # Development-only admission review endpoints.
    # Keep disabled unless explicitly enabled in the local environment.
    enable_dev_review_endpoints: bool = False

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()