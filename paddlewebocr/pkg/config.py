from typing import List

from pydantic import BaseSettings, AnyHttpUrl


class Settings(BaseSettings):
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "PaddleWebOCR"
    CORS_ORIGINS: List[AnyHttpUrl] = []
    DEBUG: bool = False
    LOG_FILE: str = "log/info.log"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
