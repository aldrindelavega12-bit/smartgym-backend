import mysql.connector

conn = mysql.connector.connect(
    host="127.0.0.1",
    user="smartgym",
    password="smartgym123",
    database="smart_gym_db"
)

print("Database connected successfully!")

conn.close()
