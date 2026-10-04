import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

config = {
    "host": os.getenv("RAILWAY_DB_HOST"),
    "port": int(os.getenv("RAILWAY_DB_PORT", "3306")),
    "user": os.getenv("RAILWAY_DB_USER"),
    "password": os.getenv("RAILWAY_DB_PASSWORD"),
    "database": os.getenv("RAILWAY_DB_NAME")
}

print("Connecting to Railway...")

try:
    conn = mysql.connector.connect(**config)

    cursor = conn.cursor()

    cursor.execute("SELECT DATABASE(), VERSION()")
    result = cursor.fetchone()

    print("✅ RAILWAY CONNECTION SUCCESSFUL")
    print("Database:", result[0])
    print("MySQL:", result[1])

    cursor.close()
    conn.close()

except Exception as e:
    print("❌ RAILWAY CONNECTION FAILED")
    print("Error:", e)
