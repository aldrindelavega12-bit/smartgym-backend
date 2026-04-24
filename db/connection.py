import mysql.connector
from config.settings import DB_CONFIG


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def execute_query(query, params=None, fetch=False):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(query, params)

        if fetch:
            result = cursor.fetchall()
            return result
        else:
            conn.commit()
            return True

    except Exception as e:
        print("DB ERROR:", e)
        return None

    finally:
        cursor.close()
        conn.close()