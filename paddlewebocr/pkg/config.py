from typing import List

from pydantic import BaseSettings, AnyHttpUrl


class Settings(BaseSettings):
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "PaddleWebOCR"
    CORS_ORIGINS: List[AnyHttpUrl] = []

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
