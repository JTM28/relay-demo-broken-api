from dataclasses import dataclass
from functools import lru_cache
import os


@dataclass(frozen=True, slots=True)
class Settings:
    app_name: str
    app_version: str
    environment: str
    seed_version: str


@lru_cache
def get_settings() -> Settings:
    return Settings(
        app_name=os.getenv("RELAY_APP_NAME", "Relay Coordination API"),
        app_version=os.getenv("RELAY_APP_VERSION", "0.3.0"),
        environment=os.getenv("RELAY_ENVIRONMENT", "local"),
        seed_version=os.getenv("RELAY_SEED_VERSION", "2026.03-demo"),
    )
