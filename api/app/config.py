import os
from typing import List, Optional

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

from .enums import Environment

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))


class DatabaseSettings(BaseSettings):
    DATABASE_USERNAME: str = "postgres"
    DATABASE_PASSWORD: str = "postgres"
    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: str = "5432"
    DATABASE_NAME: str = "runescape"

    model_config = SettingsConfigDict(env_prefix="")

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DATABASE_USERNAME}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"


class AppSettings(BaseSettings):
    ENVIRONMENT: Environment = Environment.DEVELOPMENT

    CORS_ORIGINS: List[str] = ["*"]
    CORS_ORIGINS_REGEX: Optional[str] = None
    CORS_HEADERS: List[str] = ["*"]

    APP_VERSION: str = "1.0"

    model_config = SettingsConfigDict(env_prefix="")


class RuinscapeURLSettings(BaseSettings):
    RUINSCAPE_BASE_URL: str = "https://prices.runescape.wiki/api/v1/osrs"
    RUINSCAPE_ITEM_MAPPING_URL: str = None
    RUINSCAPE_ITEM_PRICES_URL: str = None

    model_config = SettingsConfigDict(env_prefix="")

    def __init__(self, **data):
        super().__init__(**data)
        # Set dependent URLs if not provided
        if self.RUINSCAPE_ITEM_MAPPING_URL is None:
            self.RUINSCAPE_ITEM_MAPPING_URL = f"{self.RUINSCAPE_BASE_URL}/mapping"
        if self.RUINSCAPE_ITEM_PRICES_URL is None:
            self.RUINSCAPE_ITEM_PRICES_URL = f"{self.RUINSCAPE_BASE_URL}/latest"


class Settings(DatabaseSettings, AppSettings, RuinscapeURLSettings):
    pass


settings = Settings()
