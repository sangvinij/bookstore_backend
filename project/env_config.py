from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import EmailStr


class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True, env_file='.env', env_file_encoding='utf-8')
    DATABASE_URL: str
    SECRET_KEY: str
    MAIL_USERNAME: Optional[str]
    MAIL_PASSWORD: Optional[str]
    MAIL_FROM: Optional[EmailStr]
    MAIL_PORT: Optional[int]
    MAIL_SERVER: Optional[str]
    WEBAPP_HOST: str
    SUPPRESS_SEND: int = 0


env = Settings()
