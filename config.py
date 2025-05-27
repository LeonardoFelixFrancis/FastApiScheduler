import os
from dotenv import load_dotenv

load_dotenv()

# DATABASE CONFIGURATIONS
DB_USER = os.getenv("DATABASE_USER")
DB_PASSWORD = os.getenv("DATABASE_PASSWORD")
DB_NAME = os.getenv("DATABASE_NAME")
DB_HOST = os.getenv("DATABASE_HOST")

# SECRETS
SECRET_KEY: str = os.getenv("SECRET_KEY", "")

if not SECRET_KEY:
    raise ValueError("SECRET_KEY must be set in environment variables!")

# JWT CONFIG
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120
REFRESH_TOKEN_EXPIRE_DAYS = 30

