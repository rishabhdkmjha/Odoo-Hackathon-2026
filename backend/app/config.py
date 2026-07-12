"""
Central application configuration.
Reads from environment variables with sane defaults for hackathon/dev use.
"""
import os
from datetime import timedelta


class Settings:
    PROJECT_NAME: str = "AssetFlow API"
    API_V1_PREFIX: str = ""  # frontend expects endpoints WITHOUT /api/v1 prefix

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./assetflow.db")

    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "CHANGE_THIS_SECRET_IN_PRODUCTION_9f8a7d6c5b4e3f2a1")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "480"))  # 8h for hackathon demo

    # CORS - frontend dev servers
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", "*").split(",")

    @property
    def access_token_expire_delta(self) -> timedelta:
        return timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)


settings = Settings()
