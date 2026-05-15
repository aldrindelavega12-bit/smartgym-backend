import mysql.connector
from mysql.connector import pooling
from config.settings import DB_CONFIG
import platform


# =========================
# AUTO LOCAL DB FOR RPI
# =========================
if platform.system() == "Linux":

    DB_CONFIG = {
        "host": "127.0.0.1",
        "user": "smartgym",
        "password": "smartgym123",
        "database": "smart_gym_db",
        "port": 3306
    }


# =========================
# CONNECTION POOL
# =========================
db_pool = pooling.MySQLConnectionPool(
    pool_name="smartgym_pool",
    pool_size=10,
    pool_reset_session=False,
    **DB_CONFIG
)


# =========================
# GET CONNECTION
# =========================
def get_connection():

    try:

        conn = db_pool.get_connection()

        # AUTO RECONNECT
        if not conn.is_connected():

            conn.reconnect(
                attempts=1,
                delay=0
            )

        return conn

    except Exception as e:

        print("DB CONNECTION ERROR:", e)

        return None


# =========================
# EXECUTE QUERY
# =========================
def execute_query(
    query,
    params=None,
    fetch=False
):

    conn = None
    cursor = None

    try:

        conn = get_connection()

        if conn is None:
            return None

        cursor = conn.cursor(
            dictionary=True
        )

        cursor.execute(
            query,
            params
        )

        # =========================
        # FETCH DATA
        # =========================
        if fetch:

            result = cursor.fetchall()

            return result

        # =========================
        # SAVE / UPDATE
        # =========================
        else:

            conn.commit()

            return True

    except Exception as e:

        print("DB ERROR:", e)

        return None

    finally:

        try:
            if cursor:
                cursor.close()
        except:
            pass

        try:
            if conn and conn.is_connected():
                conn.close()
        except:
            pass
