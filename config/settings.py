import os

DB_CONFIG = {
    "host": os.getenv("mysql.railway.internal"),
    "user": os.getenv("root"),
    "password": os.getenv("bRQXvdMKWBmfeaABLzmdOVaCqkmzonoL"),
    "database": os.getenv("railway"),
    "port": int(os.getenv("3306"))
}
# System Settings
FP_COOLDOWN_SECONDS = 3
FACE_THRESHOLD = 60
# Admin Configuration
ADMIN_PASSWORD = "1234"  # Change this
MAX_ADMIN_ATTEMPTS = 3
