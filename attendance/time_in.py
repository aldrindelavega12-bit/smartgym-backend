from db.connection import execute_query
from datetime import datetime
import requests
import threading


# ==========================
# BACKGROUND WEBSITE NOTIFY
# ==========================
def notify_website():
    try:
        requests.post(
            "https://smartgym-api-ia2e.onrender.com/api/notify/attendance",
            timeout=1
        )
    except:
        pass


# ==========================
# CHECK ONLY (FAST VERSION)
# ==========================
def check_time_in(user_id):

    now = datetime.now()

    # ==========================
    # MEMBER CHECK
    # ==========================
    member = execute_query(
        """
        SELECT membership_expires, monthly_expires
        FROM members
        WHERE id = %s
        """,
        (user_id,),
        fetch=True
    )

    if member:

        member = member[0]

        # already inside
        active = execute_query(
            """
            SELECT *
            FROM attendance_sessions
            WHERE user_id = %s
            AND time_out IS NULL
            LIMIT 1
            """,
            (user_id,),
            fetch=True
        )

        if active:
            return {
                "allowed": False,
                "reason": "ALREADY_INSIDE"
            }

        # yearly membership
        if (
            member["membership_expires"]
            and member["membership_expires"] > now
        ):
            return {
                "allowed": True,
                "reason": "VALID_MEMBER"
            }

        # monthly membership
        if (
            member["monthly_expires"]
            and member["monthly_expires"] > now
        ):
            return {
                "allowed": True,
                "reason": "VALID_MEMBER"
            }

        return {
            "allowed": False,
            "reason": "NO_VALID_PAYMENT"
        }

    # ==========================
    # WALKIN CHECK
    # ==========================
    print("1")
    walkin = execute_query(
        """
        SELECT *
        FROM walkins
        WHERE id = %s
        """,
        (user_id,),
        fetch=True
    )

    if walkin:

        print("2")
        payment = execute_query(
            """
            SELECT *
            FROM payments
            WHERE user_id = %s
            AND payment_type = 'WALKIN'
            AND DATE(paid_at) = CURDATE()
            LIMIT 1
            """,
            (user_id,),
            fetch=True
        )

        if not payment:
            return {
                "allowed": False,
                "reason": "WALKIN_EXPIRED"
            }

        print("3")
        active = execute_query(
            """
            SELECT *
            FROM attendance_sessions
            WHERE user_id = %s
            AND time_out IS NULL
            LIMIT 1
            """,
            (user_id,),
            fetch=True
        )

        if active:
            return {
                "allowed": False,
                "reason": "ALREADY_INSIDE"
            }

        return {
            "allowed": True,
            "reason": "VALID_WALKIN"
        }

    return {
        "allowed": False,
        "reason": "USER_NOT_FOUND"
    }


# ==========================
# SAVE ONLY (BACKGROUND SAFE)
# ==========================
def save_time_in(user_id):

    now = datetime.now()

    # attendance session
    execute_query(
        """
        INSERT INTO attendance_sessions
        (user_id, time_in, status)
        VALUES (%s, %s, %s)
        """,
        (user_id, now, "ACTIVE")
    )

    # access logs
    execute_query(
        """
        INSERT INTO access_logs
        (user_id, direction, result, reason)
        VALUES (%s,%s,%s,%s)
        """,
        (user_id, "IN", "ALLOW", "VALID")
    )

    # ==========================
    # WEBSITE UPDATE (BACKGROUND)
    # ==========================
    # CLOUD SYNC
    threading.Thread(
        target=sync_attendance_cloud,
        args=(user_id,),
        daemon=True
    ).start()
    
# ==========================
# CLOUD SYNC
# ==========================
def sync_attendance_cloud(user_id):

    try:

        requests.post(
            "https://smartgym-api-ia2e.onrender.com/api/sync_attendance",
            json={
                "user_id": user_id
            },
            timeout=1
        )

    except:
        pass