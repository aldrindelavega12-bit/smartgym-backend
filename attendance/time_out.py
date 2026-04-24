from datetime import datetime, timedelta
from db.connection import execute_query
import math

LOCKER_ALLOWED_HOURS = 3


# ==========================
# CHECK ONLY (NO SAVE)
# ==========================
def check_time_out(user_id):

    # 1. Check active attendance
    session = execute_query(
        "SELECT session_id FROM attendance_sessions "
        "WHERE user_id=%s AND time_out IS NULL",
        (user_id,),
        fetch=True
    )

    if not session:
        return {"allowed": False, "reason": "NO_ACTIVE_SESSION"}

    # 2. Check locker
    locker = execute_query(
        "SELECT locker_number, start_time, overtime_paid "
        "FROM locker_sessions "
        "WHERE user_id=%s AND end_time IS NULL",
        (user_id,),
        fetch=True
    )

    if locker:

        start_time = locker[0]["start_time"]
        overtime_paid = int(locker[0]["overtime_paid"] or 0)

        allowed_time = start_time + timedelta(hours=LOCKER_ALLOWED_HOURS)

        if datetime.now() > allowed_time and overtime_paid == 0:

            overtime_minutes = int((datetime.now() - allowed_time).total_seconds() / 60)
            fee = math.ceil(overtime_minutes / 2)

            return {
                "allowed": False,
                "reason": f"OVERTIME_{fee}"
            }

    return {"allowed": True, "reason": "OK"}


# ==========================
# SAVE ONLY (AFTER VALIDATED)
# ==========================
def save_time_out(user_id):

    # 1. Handle locker release
    locker = execute_query(
        "SELECT locker_number FROM locker_sessions "
        "WHERE user_id=%s AND end_time IS NULL",
        (user_id,),
        fetch=True
    )

    if locker:
        locker_number = locker[0]["locker_number"]

        execute_query(
            "UPDATE locker_sessions SET end_time=NOW() "
            "WHERE user_id=%s AND end_time IS NULL",
            (user_id,)
        )

        execute_query(
            "UPDATE lockers SET status='AVAILABLE' "
            "WHERE locker_number=%s",
            (locker_number,)
        )

        print(f"[LOCKER RELEASED]: {locker_number}")

    # 2. Close attendance
    execute_query(
        "UPDATE attendance_sessions SET time_out=NOW() "
        "WHERE user_id=%s AND time_out IS NULL",
        (user_id,)
    )

    print("[SESSION CLOSED]:", user_id)