import os
from typing import List

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

from .enums import Environment

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))


class Settings(BaseSettings):
    DATABASE_USERNAME: str = os.getenv("DATABASE_USERNAME", "postgres")
    DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD", "postgres")
    DATABASE_HOST: str = os.getenv("DATABASE_HOST", "localhost")
    DATABASE_PORT: str = os.getenv("DATABASE_PORT", "5432")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "runescape")
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        f"postgresql+asyncpg://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}",
    )

    ENVIRONMENT: Environment = os.getenv("ENVIRONMENT", Environment.DEVELOPMENT)

    CORS_ORIGINS: List[str] = ["*"]
    CORS_ORIGINS_REGEX: str | None = None
    CORS_HEADERS: List[str] = ["*"]

    APP_VERSION: str = "1.0"


settings = Settings()
