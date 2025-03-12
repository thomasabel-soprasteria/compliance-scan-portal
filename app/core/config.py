
from pydantic import BaseSettings, PostgresDsn
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings(BaseSettings):
    APP_NAME: str = os.getenv("APP_NAME", "Compliance Scan Portal")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    API_PREFIX: str = os.getenv("API_PREFIX", "/api/v1")
    DATABASE_URL: PostgresDsn = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/compliance_db")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    TEMP_UPLOAD_DIR: str = os.getenv("TEMP_UPLOAD_DIR", "./uploads")
    MAX_UPLOAD_SIZE: int = int(os.getenv("MAX_UPLOAD_SIZE", "20971520"))  # 20MB default

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
