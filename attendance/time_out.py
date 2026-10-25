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
def sync_timeout_cloud(user_id, time_out):

    try:

        response = requests.post(
            "https://smartgym-api-ia2e.onrender.com/api/sync_timeout",
            json={
                "user_id": user_id,
                "time_out": time_out.strftime("%Y-%m-%d %H:%M:%S")
            },
            timeout=3
        )

        if response.status_code == 200:
            print(
                f"☁️ TIME-OUT SYNCED: "
                f"{user_id} | {time_out}"
            )
        else:
            print(
                f"☁️ TIME-OUT SYNC FAILED: "
                f"{response.status_code}"
            )

    except Exception as e:

        print(
            "SYNC OUT ERROR:",
            e
        )

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
    locker = execute_query("""
        SELECT locker_number, start_time, overtime_paid
        FROM locker_sessions
        WHERE user_id = %s
          AND end_time IS NULL
          AND status = 'ACTIVE'
          AND start_time IS NOT NULL
        ORDER BY start_time DESC
        LIMIT 1
    """, (user_id,), fetch=True)


    if locker:

        start_time = locker[0]["start_time"]
        overtime_paid = int(locker[0]["overtime_paid"] or 0)
        
        if start_time is None:
            print(
                f"[TIME OUT ERROR] Missing locker start_time "
                f"for user={user_id}"
            )
            return {
                "allowed": False,
                "reason": "LOCKER_START_TIME_MISSING"
            }

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
# SAVE ONLY AFTER EXIT PASSED
# ==========================
def save_time_out(user_id):

    now = datetime.now()

    # ==========================
    # CLOSE LATEST ATTENDANCE ONLY
    # DO NOT RELEASE LOCKER HERE
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
            ) AS temp
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
        VALUES (%s, %s, %s, %s)
        """,
        (user_id, "OUT", "ALLOW", "VALID")
    )

    # ==========================
    # BACKGROUND WEBSITE UPDATE
    # ==========================
    threading.Thread(
        target=sync_timeout_cloud,
        args=(user_id, now),
        daemon=True
    ).start()

# ==========================
# SAVE ONLY (AFTER VALIDATED)
# ==========================

   
