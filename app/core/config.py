
from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings(BaseSettings):
    APP_NAME: str = os.getenv("APP_NAME", "Compliance Scan Portal")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    API_PREFIX: str = os.getenv("API_PREFIX", "/api/v1")
    MONGODB_URL: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017/compliance_db")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    TEMP_UPLOAD_DIR: str = os.getenv("TEMP_UPLOAD_DIR", "./uploads")
    MAX_UPLOAD_SIZE: int = int(os.getenv("MAX_UPLOAD_SIZE", "20971520"))  # 20MB default
    DB_NAME: str = "compliance_db"  # Extract from MongoDB URL or set explicitly

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
