import os

class Config:
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/projectDatabase")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt_secret_key")
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")