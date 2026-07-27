from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

APP_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    env: str = "development"
    cors_origins: str = "http://localhost:3000"

    max_total_upload_mb: int = 50
    file_ttl_minutes: int = 60
    cleanup_interval_minutes: int = 10

    rate_limit_per_minute: int = 10

    log_level: str = "INFO"
    log_json: bool = True

    upload_dir: Path = APP_DIR / "storage" / "uploads"
    output_dir: Path = APP_DIR / "storage" / "outputs"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


settings = Settings()
