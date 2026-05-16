from datetime import datetime, timedelta
from db.connection import execute_query
import math
import requests
import threading

LOCKER_ALLOWED_HOURS = 3


# ==========================
# WEBSITE UPDATE
# ==========================
def notify_website():

    try:

        # attendance refresh
        requests.post(
            "https://smartgym-api-ia2e.onrender.com/api/notify/attendance",
            timeout=1
        )

        # locker refresh
        requests.post(
            "https://smartgym-api-ia2e.onrender.com/api/notify/locker",
            timeout=1
        )

    except:
        pass

def sync_timeout_cloud(user_id):

    try:

        response = requests.post(
            "https://smartgym-api-ia2e.onrender.com/api/sync_timeout",
            json={
                "user_id": user_id
            },
            timeout=3
        )

        print("☁️ TIMEOUT CLOUD:", response.status_code)

    except Exception as e:

        print("SYNC OUT ERROR:", e)
# ==========================
# CHECK ONLY (NO SAVE)
# ==========================
def check_time_out(user_id):

    # 1. Check active attendance
    session = execute_query(
        """
        SELECT session_id
        FROM attendance_sessions
        WHERE user_id=%s
        AND time_out IS NULL
        LIMIT 1
        """,
        (user_id,),
        fetch=True
    )

    if not session:

        return {
            "allowed": False,
            "reason": "NO_ACTIVE_SESSION"
        }

    # 2. Check locker
    locker = execute_query(
        """
        SELECT locker_number, start_time, overtime_paid
        FROM locker_sessions
        WHERE user_id=%s
        AND end_time IS NULL
        LIMIT 1
        """,
        (user_id,),
        fetch=True
    )

    if locker:

        start_time = locker[0]["start_time"]
        overtime_paid = int(locker[0]["overtime_paid"] or 0)

        allowed_time = start_time + timedelta(
            hours=LOCKER_ALLOWED_HOURS
        )

        if datetime.now() > allowed_time and overtime_paid == 0:

            overtime_minutes = int(
                (datetime.now() - allowed_time).total_seconds() / 60
            )

            fee = math.ceil(overtime_minutes / 2)

            return {
                "allowed": False,
                "reason": f"OVERTIME_{fee}"
            }

    return {
        "allowed": True,
        "reason": "OK"
    }


# ==========================
# SAVE ONLY (AFTER VALIDATED)
# ==========================
def save_time_out(user_id):

    now = datetime.now()

    # ==========================
    # HANDLE LOCKER RELEASE
    # ==========================
    locker = execute_query(
        """
        SELECT locker_number
        FROM locker_sessions
        WHERE user_id=%s
        AND end_time IS NULL
        LIMIT 1
        """,
        (user_id,),
        fetch=True
    )

    if locker:

        locker_number = locker[0]["locker_number"]

        # close locker session
        execute_query(
            """
            UPDATE locker_sessions
            SET end_time=%s
            WHERE user_id=%s
            AND end_time IS NULL
            """,
            (now, user_id)
        )

        # make locker available
        execute_query(
            """
            UPDATE lockers
            SET status='AVAILABLE'
            WHERE locker_number=%s
            """,
            (locker_number,)
        )

        print(f"[LOCKER RELEASED]: {locker_number}")

    # ==========================
    # CLOSE ATTENDANCE
    # ==========================
    # ==========================
    # CLOSE LATEST ATTENDANCE ONLY
    # ==========================
    execute_query(
        """
        UPDATE attendance_sessions
        SET time_out=%s,
            status='COMPLETED'
        WHERE session_id = (

            SELECT session_id
            FROM (

                SELECT session_id
                FROM attendance_sessions
                WHERE user_id=%s
                AND time_out IS NULL
                ORDER BY session_id DESC
                LIMIT 1

            ) temp
        )
        """,
        (now, user_id)
    )

    print("[SESSION CLOSED]:", user_id)

    # ==========================
    # ACCESS LOG
    # ==========================
    execute_query(
        """
        INSERT INTO access_logs
        (user_id, direction, result, reason)
        VALUES (%s,%s,%s,%s)
        """,
        (user_id, "OUT", "ALLOW", "VALID")
    )

    # ==========================
    # BACKGROUND WEBSITE UPDATE
    # ==========================
    threading.Thread(
        target=sync_timeout_cloud,
        args=(user_id,),
        daemon=True
    ).start()
