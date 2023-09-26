from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import EmailStr


class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True, env_file='.env', env_file_encoding='utf-8', extra="ignore")
    DATABASE_URL: str
    SECRET_KEY: str
    MAIL_USERNAME: Optional[str] = None
    MAIL_PASSWORD: Optional[str] = None
    MAIL_FROM: Optional[EmailStr] = None
    MAIL_PORT: Optional[int] = None
    MAIL_SERVER: Optional[str] = None
    SUPERUSER_EMAIL: str
    SUPERUSER_PASSWORD: str
    WEBAPP_HOST: str
    SUPPRESS_SEND: int = 0
    ALLOWED_HOSTS: str = '*'
    HOST_FOR_TESTS: str


env = Settings()
