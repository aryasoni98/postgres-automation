from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "PostgreSQL Automation API"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    AWS_REGION: str
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    
    ENVIRONMENT: str
    SSH_KEY_PATH: str
    
    DEFAULT_POSTGRESQL_VERSION: str = "14"
    DEFAULT_MAX_CONNECTIONS: int = 100
    DEFAULT_SHARED_BUFFERS: str = "1GB"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()