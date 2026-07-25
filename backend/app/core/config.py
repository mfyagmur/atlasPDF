from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

APP_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    env: str = "development"
    frontend_origin: str = "http://localhost:3000"

    max_total_upload_mb: int = 50
    file_ttl_minutes: int = 60

    upload_dir: Path = APP_DIR / "storage" / "uploads"
    output_dir: Path = APP_DIR / "storage" / "outputs"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
