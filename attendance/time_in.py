from db.connection import execute_query
from datetime import datetime


# ==========================
# CHECK ONLY (NO SAVE)
# ==========================
def check_time_in(user_id):
    now = datetime.now()

    # MEMBER
    member = execute_query(
        "SELECT * FROM members WHERE id = %s",
        (user_id,),
        fetch=True
    )

    if member:
        member = member[0]

        # already inside
        active = execute_query(
            "SELECT * FROM attendance_sessions WHERE user_id = %s AND time_out IS NULL",
            (user_id,),
            fetch=True
        )

        if active:
            return {"allowed": False, "reason": "ALREADY_INSIDE"}

        # valid membership
        if member["membership_expires"] and member["membership_expires"] > now:
            return {"allowed": True, "reason": "VALID_MEMBER"}

        if member["monthly_expires"] and member["monthly_expires"] > now:
            return {"allowed": True, "reason": "VALID_MEMBER"}

        return {"allowed": False, "reason": "NO_VALID_PAYMENT"}

    # WALKIN
    walkin = execute_query(
        "SELECT * FROM walkins WHERE id = %s",
        (user_id,),
        fetch=True
    )

    if walkin:
        payment = execute_query(
            """
            SELECT * FROM payments 
            WHERE user_id = %s 
            AND payment_type = 'WALKIN'
            AND DATE(paid_at) = CURDATE()
            LIMIT 1
            """,
            (user_id,),
            fetch=True
        )

        if not payment:
            return {"allowed": False, "reason": "WALKIN_EXPIRED"}

        active = execute_query(
            "SELECT * FROM attendance_sessions WHERE user_id = %s AND time_out IS NULL",
            (user_id,),
            fetch=True
        )

        if active:
            return {"allowed": False, "reason": "ALREADY_INSIDE"}

        return {"allowed": True, "reason": "VALID_WALKIN"}

    return {"allowed": False, "reason": "USER_NOT_FOUND"}


from db.connection import execute_query
from datetime import datetime
import requests


# ==========================
# SAVE ONLY (AFTER VALIDATION)
# ==========================
def save_time_in(user_id):
    now = datetime.now()

    execute_query(
        "INSERT INTO attendance_sessions (user_id, time_in, status) VALUES (%s, %s, %s)",
        (user_id, now, "ACTIVE")
    )

    execute_query(
        "INSERT INTO access_logs (user_id, direction, result, reason) VALUES (%s,%s,%s,%s)",
        (user_id, "IN", "ALLOW", "VALID")
    )

    # ===================================
    # 🔥 REALTIME WEBSITE UPDATE
    # ===================================
    try:
        notify = requests.post(
            "https://smartgym-api-ia2e.onrender.com/api/notify/attendance",
            timeout=5
        )

        print("🔥 WEBSITE NOTIFY:", notify.status_code)

    except Exception as e:
        print("❌ NOTIFY ERROR:", e)