import os
from pydantic import BaseModel

class Settings(BaseModel):
    APP_NAME: str = "ZeroWasteByte Foundation API"
    MONGODB_URL: str = os.getenv("MONGODB_URL", "mongodb://127.0.0.1:27017")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "zerowaste_db")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "zerowaste-super-secure-secret-key-2025")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 7 days
    UPLOAD_DIR: str = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "uploads")

settings = Settings()
