from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    DATABASE_URL: str = Field(default=f"sqlite:///{BASE_DIR / 'cantina_api.db'}", env="DATABASE_URL")
    SECRET_KEY: str = Field(default="SUA_CHAVE_SECRETA_SUPER_SEGURA_AQUI", env="SECRET_KEY")
    ALGORITHM: str = Field(default="HS256", env="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    API_TITLE: str = Field(default="Cantina Interativa API", env="API_TITLE")
    API_DESCRIPTION: str = Field(default="API REST simples e modular para gerenciar clientes e produtos de cantina.", env="API_DESCRIPTION")
    API_VERSION: str = Field(default="0.1.0", env="API_VERSION")
    ALLOWED_ORIGINS: str = Field(default="http://localhost", env="ALLOWED_ORIGINS")
    ENVIRONMENT: str = Field(default="development", env="ENVIRONMENT")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
