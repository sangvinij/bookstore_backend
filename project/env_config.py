from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True, env_file='.env', env_file_encoding='utf-8')
    DATABASE_URL: str


def get_variable(variable):
    settings = Settings()
    return getattr(settings, variable, None)
