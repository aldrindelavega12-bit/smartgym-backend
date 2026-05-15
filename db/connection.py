import mysql.connector
from mysql.connector import pooling
from config.settings import DB_CONFIG


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

        # 🔥 AUTO RECONNECT CHECK
        if not conn.is_connected():
            conn.reconnect(attempts=1, delay=0)

        return conn

    except Exception as e:

        print("DB CONNECTION ERROR:", e)

        return None


# =========================
# EXECUTE QUERY
# =========================
def execute_query(query, params=None, fetch=False):

    conn = None
    cursor = None

    try:

        conn = get_connection()

        if conn is None:
            return None

        cursor = conn.cursor(dictionary=True)

        cursor.execute(query, params)

        # =========================
        # FETCH DATA
        # =========================
        if fetch:

            result = cursor.fetchall()

            return result

        # =========================
        # SAVE / INSERT / UPDATE
        # =========================
        else:

            conn.commit()

            return True

    except Exception as e:

        print("DB ERROR:", e)

        return None

    finally:

        # close cursor only
        try:
            if cursor:
                cursor.close()
        except:
            pass

        # 🔥 RETURN CONNECTION TO POOL
        try:
            if conn and conn.is_connected():
                conn.close()
        except:
            pass