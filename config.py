"""Default configuration settings."""
from functools import lru_cache

# from pydantic import BaseSettings
#class Settings(BaseSettings):

class Settings():
    """Default BaseSettings."""

    env_name: str = "Local"
    base_url: str = "http://localhost:8000"
    db_url: str = "sqlite:///./Ezzy_Url_Shortener.db"

    # Postgreqsl specific
    db_name: str = "Ezzy_Url_Shortener" #Ezzy_Url_Shortener
    db_address: str = "localhost"
    db_port: str = "5432"
    db_user: str = "postgres"
    db_pw: str = "admin"

    # default to SQLite
    db_backend: str = "sqlite" #change to 'postgresql' for postgres database

    class Config:
        """Load env variables from .env file."""

        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    """Return the current settings."""
    settings = Settings()
    if settings.db_backend == "postgresql":
        settings.db_url: str = (
            f"postgresql://{settings.db_user}:{settings.db_pw}"
            f"@{settings.db_address}:{settings.db_port}/{settings.db_name}"
        )
    print(f"Loading settings for: {settings.env_name}")
    print(f"Database String: '{settings.db_url}'")
    return settings
