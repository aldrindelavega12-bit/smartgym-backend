import mysql.connector
from mysql.connector import pooling
from config.settings import DB_CONFIG


# =========================
# CONNECTION POOL
# =========================
db_pool = pooling.MySQLConnectionPool(
    pool_name="smartgym_pool",
    pool_size=5,
    pool_reset_session=True,
    **DB_CONFIG
)


# =========================
# GET CONNECTION
# =========================
def get_connection():

    conn = db_pool.get_connection()

    # =========================
    # PH TIMEZONE
    # =========================
    cursor = conn.cursor()

    cursor.execute("SET time_zone = '+08:00'")

    cursor.close()

    return conn

# =========================
# EXECUTE QUERY
# =========================
def execute_query(query, params=None, fetch=False):

    conn = None
    cursor = None

    try:

        conn = get_connection()

        cursor = conn.cursor(dictionary=True)

        cursor.execute(query, params)

        # =========================
        # FETCH DATA
        # =========================
        if fetch:
            result = cursor.fetchall()
            return result

        # =========================
        # SAVE CHANGES
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
            if conn:
                conn.close()
        except:
            pass
