from functools import lru_cache

from pydantic_settings import BaseSettings


@lru_cache()
def get_settings():
    return Settings()


class Settings(BaseSettings):
    app_name: str = "r2kook"

    kook_api_base_url: str = "https://www.kookapp.cn/api/v3"

    kook_token: str = ""

    github_webhook_secret: str = ""

    class Config:
        env_file = ".env"


settings = get_settings()
