from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    database_url: str
    session_secret: str
    upload_dir: str


def get_settings() -> Settings:
    return Settings(
        database_url=os.environ.get("API_DATABASE_URL", "sqlite:///./dev.db"),
        session_secret=os.environ.get("API_SESSION_SECRET", "dev-secret-change-me"),
        upload_dir=os.environ.get("API_UPLOAD_DIR", "./uploads"),
    )

