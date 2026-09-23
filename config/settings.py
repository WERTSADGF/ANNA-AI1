from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    app_name: str = "ANNA AI"
    environment: str = os.getenv("ANNA_ENV", "development")
    privacy_mode: str = os.getenv("ANNA_PRIVACY_MODE", "ONLINE")
    log_level: str = os.getenv("ANNA_LOG_LEVEL", "INFO")


def load_settings() -> Settings:
    return Settings()
