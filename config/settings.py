import os

DB_CONFIG = {
    "host": os.getenv("DB_HOST") or "127.0.0.1",
    "user": os.getenv("DB_USER") or "smartgym",
    "password": os.getenv("DB_PASSWORD") or "smartgym123",
    "database": os.getenv("DB_NAME") or "smart_gym_db",
    "port": int(os.getenv("DB_PORT") or 3306)
}

# System Settings
FP_COOLDOWN_SECONDS = 3
FACE_THRESHOLD = 60
# Admin Configuration
ADMIN_PASSWORD = "1234"  # Change this
MAX_ADMIN_ATTEMPTS = 3
