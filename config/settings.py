import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "port": int(os.getenv("DB_PORT"))
}

# System Settings
FP_COOLDOWN_SECONDS = 3
FACE_THRESHOLD = 60

# Admin Configuration
ADMIN_PASSWORD = "1234"
MAX_ADMIN_ATTEMPTS = 3