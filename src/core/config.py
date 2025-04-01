import logging
from typing import Any, List, Optional

from dotenv import load_dotenv
from pydantic import AnyHttpUrl, Field, PostgresDsn, field_validator, ValidationInfo
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = "Coffee Shop API"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "api"

    # Environment
    ENV: str = "dev"

    # Database
    POSTGRES_USER: str = Field(default="postgres", env="POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field(default="root", env="POSTGRES_PASSWORD")
    POSTGRES_HOST: str = Field(default="localhost", env="POSTGRES_HOST")
    POSTGRES_PORT: str = Field(default="5432", env="POSTGRES_PORT")
    POSTGRES_DB: str = Field(default="network-of-coffee-db", env="POSTGRES_DB")
    DATABASE_URL: str = Field(default="", env="DATABASE_URL")

    # Security
    SECRET_KEY: str = Field(default="your-secret-key-here", env="SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # JWT
    JWT_SECRET: str = Field(default="your-jwt-secret", env="JWT_SECRET")
    JWT_ALGORITHM: str = "HS256"
    JWT_REFRESH_SECRET: str = Field(default="your-jwt-refresh-secret", env="JWT_REFRESH_SECRET")
    SALT: str = Field(default="your-salt", env="SALT")

    # SMTP
    SMTP_HOST: str = Field(default="smtp.gmail.com", env="SMTP_HOST")
    SMTP_PORT: int = Field(default=587, env="SMTP_PORT")
    SMTP_USER: str = Field(default="your-email@gmail.com", env="SMTP_USER")
    SMTP_PASSWORD: str = Field(default="your-password", env="SMTP_PASSWORD")

    # 60 minutes * 24 hours * 2 days = 2 days
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 15
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    API_URL: str = Field(default="", env="API_URL")
    API_TOKEN: str = Field(default="", env="API_TOKEN")
    LOG_LEVEL: int = Field(default=logging.INFO, env="LOG_LEVEL")

    DEBUG: bool = Field(default=True, env="DEBUG")

    DB_POOL_SIZE: int = Field(default=83, env="DB_POOL_SIZE")
    WEB_CONCURRENCY: int = Field(default=9, env="WEB_CONCURRENCY")
    MAX_OVERFLOW: int = Field(default=64, env="MAX_OVERFLOW")
    POOL_SIZE: Optional[int] = None

    @field_validator("DATABASE_URL", mode="before")
    def build_database_url(cls, v: Optional[str], values: ValidationInfo) -> str:
        if v:
            return v
        return f"postgresql://{values.data.get('POSTGRES_USER')}:{values.data.get('POSTGRES_PASSWORD')}@{values.data.get('POSTGRES_HOST')}:{values.data.get('POSTGRES_PORT')}/{values.data.get('POSTGRES_DB')}"

    @field_validator("POOL_SIZE", mode="before")
    def build_pool(cls, v: Optional[str], values: ValidationInfo) -> Any:
        if isinstance(v, int):
            return v
        return max(values.data.get("DB_POOL_SIZE") // values.data.get("WEB_CONCURRENCY"), 5)

    class Config:
        env_file = ".env"


# object to store settings
settings = Settings()
print('-' * 20)
print('project name:', settings.PROJECT_NAME)
print('database url:', settings.DATABASE_URL)
