import base64 
import sys, os
import sqlite3
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from flask import send_file
import json
import random
import hashlib
from datetime import datetime, timedelta
from sms_module.sms import send_sms
# Path fix para mahanap ang 'db' folder sa root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db.connection import execute_query
import mysql.connector
from flask_socketio import SocketIO
from datetime import datetime
import requests

app = Flask(__name__)

CORS(app)
    
socketio = SocketIO(
    app,
    cors_allowed_origins="*"
)

# --- MILESTONE 4: SECURITY KEY ---
API_KEY = "GYM_MASTER_2026"
RENDER_API = "https://smartgym-api-ia2e.onrender.com"
@app.route("/api/activate_account", methods=["POST"])

@app.route("/api/member/attendance/<user_id>", methods=["GET"])
def get_member_attendance(user_id):

    conn = None

    try:

        conn = get_connection()

        cursor = conn.cursor(
            pymysql.cursors.DictCursor
        )

        # =========================
        # GET ALL ATTENDANCE DATES
        # =========================

        cursor.execute("""
            SELECT DISTINCT
                DATE(time_in) AS attendance_date
            FROM attendance_sessions
            WHERE user_id = %s
            AND time_in IS NOT NULL
            ORDER BY attendance_date ASC
        """, (user_id,))

        rows = cursor.fetchall()


        # =========================
        # FORMAT DATES
        # =========================

        dates = []

        for row in rows:

            attendance_date = row["attendance_date"]

            if attendance_date:

                dates.append(
                    attendance_date.strftime(
                        "%Y-%m-%d"
                    )
                )


        # =========================
        # TOTAL USES
        # =========================

        total = len(dates)


        return jsonify({

            "success": True,

            "dates": dates,

            "total": total

        })


    except Exception as e:

        print(
            "MEMBER ATTENDANCE ERROR:",
            e
        )

        return jsonify({

            "success": False,

            "dates": [],

            "total": 0,

            "message": str(e)

        }), 500


    finally:

        if conn:

            conn.close()

@app.route("/api/staff_member_messages")
def staff_member_messages():

    try:

        conn = get_connection()

        cursor = conn.cursor(
            pymysql.cursors.DictCursor
        )

        cursor.execute("""
            SELECT
                m.id,

                SUBSTRING_INDEX(
                    m.message,
                    ' ',
                    1
                ) AS user_id,

                mem.full_name AS member_name,

                m.title,
                m.message,
                m.reason,
                m.is_read,

                DATE_FORMAT(
                    CONVERT_TZ(
                        m.created_at,
                        '+00:00',
                        '+08:00'
                    ),
                    '%M %d, %Y %h:%i %p'
                ) AS created_at

            FROM messages m

            LEFT JOIN members mem
                ON mem.id = SUBSTRING_INDEX(
                    m.message,
                    ' ',
                    1
                )

            WHERE m.user_id = 'ADMIN'

            AND m.id = (
                SELECT MAX(m2.id)

                FROM messages m2

                WHERE m2.user_id = 'ADMIN'

                AND SUBSTRING_INDEX(
                    m2.message,
                    ' ',
                    1
                ) = SUBSTRING_INDEX(
                    m.message,
                    ' ',
                    1
                )
            )

            ORDER BY m.id DESC

        """)

        rows = cursor.fetchall()

        conn.close()

        return jsonify(rows)

    except Exception as e:

        print(
            "STAFF MEMBER MESSAGES ERROR:",
            e
        )

        return jsonify({
            "error": str(e)
        }), 500
    
@app.route("/api/member/profile", methods=["PUT"])
def update_member_profile():

    data = request.get_json() or {}

    account_id = data.get("id")
    username = data.get("username", "").strip()
    phone_number = data.get("phone_number", "").strip()

    current_password = data.get("current_password", "")
    new_password = data.get("new_password", "")
    confirm_password = data.get("confirm_password", "")

    # =========================
    # BASIC VALIDATION
    # =========================

    if not account_id:
        return jsonify({
            "success": False,
            "message": "Account ID is required."
        }), 400

    if not username:
        return jsonify({
            "success": False,
            "message": "Username is required."
        }), 400

    if not phone_number:
        return jsonify({
            "success": False,
            "message": "Phone number is required."
        }), 400

    conn = get_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    try:

        # =========================
        # GET ACCOUNT
        # =========================

        cursor.execute("""
            SELECT
                ua.id,
                ua.user_id,
                ua.username,
                ua.password,
                ua.role
            FROM user_accounts ua
            WHERE ua.id=%s
            LIMIT 1
        """, (account_id,))

        account = cursor.fetchone()

        if not account:
            return jsonify({
                "success": False,
                "message": "Account not found."
            }), 404

        # =========================
        # MUST BE MEMBER
        # =========================

        if account["role"] != "member":
            return jsonify({
                "success": False,
                "message": "Member account required."
            }), 403

        member_id = account["user_id"]

        # =========================
        # CHECK MEMBER EXISTS
        # =========================

        cursor.execute("""
            SELECT id
            FROM members
            WHERE id=%s
            LIMIT 1
        """, (member_id,))

        member = cursor.fetchone()

        if not member:
            return jsonify({
                "success": False,
                "message": "Member record not found."
            }), 404

        # =========================
        # CHECK USERNAME DUPLICATE
        # =========================

        cursor.execute("""
            SELECT id
            FROM user_accounts
            WHERE username=%s
            AND id<>%s
            LIMIT 1
        """, (
            username,
            account_id
        ))

        existing_username = cursor.fetchone()

        if existing_username:
            return jsonify({
                "success": False,
                "message": "Username already exists."
            }), 409

        # =========================
        # PASSWORD CHANGE?
        # =========================

        changing_password = bool(
            current_password or
            new_password or
            confirm_password
        )

        if changing_password:

            if not current_password:
                return jsonify({
                    "success": False,
                    "message": "Current password is required."
                }), 400

            if not new_password:
                return jsonify({
                    "success": False,
                    "message": "New password is required."
                }), 400

            if not confirm_password:
                return jsonify({
                    "success": False,
                    "message": "Please confirm your new password."
                }), 400

            # CURRENT PASSWORD
            if account["password"] != current_password:
                return jsonify({
                    "success": False,
                    "message": "Current password is incorrect."
                }), 400

            # CONFIRM PASSWORD
            if new_password != confirm_password:
                return jsonify({
                    "success": False,
                    "message": "New passwords do not match."
                }), 400

            # MINIMUM LENGTH
            if len(new_password) < 8:
                return jsonify({
                    "success": False,
                    "message": "Password must be at least 8 characters."
                }), 400

        # =========================
        # UPDATE USERNAME
        # =========================

        if changing_password:

            cursor.execute("""
                UPDATE user_accounts
                SET
                    username=%s,
                    password=%s
                WHERE id=%s
            """, (
                username,
                new_password,
                account_id
            ))

        else:

            cursor.execute("""
                UPDATE user_accounts
                SET username=%s
                WHERE id=%s
            """, (
                username,
                account_id
            ))

        # =========================
        # UPDATE PHONE
        # =========================

        cursor.execute("""
            UPDATE members
            SET phone_number=%s
            WHERE id=%s
        """, (
            phone_number,
            member_id
        ))

        # =========================
        # COMMIT
        # =========================

        conn.commit()

        # =========================
        # SUCCESS
        # =========================

        return jsonify({
            "success": True,
            "message": "Profile updated successfully.",
            "user": {
                "id": account_id,
                "user_id": member_id,
                "username": username,
                "phone_number": phone_number
            }
        }), 200

    except Exception as e:

        conn.rollback()

        print("MEMBER PROFILE UPDATE ERROR:", e)

        return jsonify({
            "success": False,
            "message": "Failed to update profile."
        }), 500

    finally:

        cursor.close()
        conn.close()

def generate_otp():
    return f"{random.randint(0, 999999):06d}"


def hash_otp(otp):
    return hashlib.sha256(
        otp.encode("utf-8")
    ).hexdigest()

@app.route("/api/forgot-password/reset", methods=["POST"])
def reset_password():

    data = request.get_json() or {}

    username = data.get("username", "").strip()
    otp = data.get("otp", "").strip()
    new_password = data.get("new_password", "")
    confirm_password = data.get("confirm_password", "")

    # =========================
    # BASIC VALIDATION
    # =========================

    if not username:
        return jsonify({
            "success": False,
            "message": "Username is required."
        }), 400

    if not otp:
        return jsonify({
            "success": False,
            "message": "Verification code is required."
        }), 400

    if not new_password:
        return jsonify({
            "success": False,
            "message": "New password is required."
        }), 400

    if new_password != confirm_password:
        return jsonify({
            "success": False,
            "message": "Passwords do not match."
        }), 400

    if len(new_password) < 8:
        return jsonify({
            "success": False,
            "message": "Password must be at least 8 characters."
        }), 400


    conn = get_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    try:

        # =========================
        # FIND ACCOUNT
        # =========================

        cursor.execute("""
            SELECT
                user_id,
                username
            FROM user_accounts
            WHERE username = %s
            LIMIT 1
        """, (username,))

        user = cursor.fetchone()

        if not user:
            return jsonify({
                "success": False,
                "message": "Account not found."
            }), 404


        # =========================
        # GET LATEST OTP
        # =========================

        cursor.execute("""
            SELECT
                id,
                otp_hash,
                expires_at,
                attempts,
                used
            FROM password_reset_otps
            WHERE user_id = %s
            ORDER BY id DESC
            LIMIT 1
        """, (user["user_id"],))

        reset = cursor.fetchone()

        if not reset:
            return jsonify({
                "success": False,
                "message": "No verification code found."
            }), 400


        # =========================
        # CHECK USED
        # =========================

        if reset["used"]:
            return jsonify({
                "success": False,
                "message": "Verification code has already been used."
            }), 400


        # =========================
        # CHECK EXPIRATION
        # =========================

        if datetime.now() > reset["expires_at"]:

            cursor.execute("""
                UPDATE password_reset_otps
                SET used = 1
                WHERE id = %s
            """, (reset["id"],))

            conn.commit()

            return jsonify({
                "success": False,
                "message": "Verification code has expired."
            }), 400


        # =========================
        # CHECK ATTEMPTS
        # =========================

        if reset["attempts"] >= 5:

            cursor.execute("""
                UPDATE password_reset_otps
                SET used = 1
                WHERE id = %s
            """, (reset["id"],))

            conn.commit()

            return jsonify({
                "success": False,
                "message": "Too many attempts. Please request a new code."
            }), 400


        # =========================
        # VERIFY OTP
        # =========================

        if hash_otp(otp) != reset["otp_hash"]:

            cursor.execute("""
                UPDATE password_reset_otps
                SET attempts = attempts + 1
                WHERE id = %s
            """, (reset["id"],))

            conn.commit()

            return jsonify({
                "success": False,
                "message": "Invalid verification code."
            }), 400


        # =========================
        # UPDATE PASSWORD
        # =========================

        cursor.execute("""
            UPDATE user_accounts
            SET password = %s
            WHERE user_id = %s
        """, (
            new_password,
            user["user_id"]
        ))


        # =========================
        # MARK OTP USED
        # =========================

        cursor.execute("""
            UPDATE password_reset_otps
            SET used = 1
            WHERE id = %s
        """, (reset["id"],))


        conn.commit()


        return jsonify({
            "success": True,
            "message": "Password reset successfully."
        })


    except Exception as e:

        conn.rollback()

        print(
            "RESET PASSWORD ERROR:",
            e
        )

        return jsonify({
            "success": False,
            "message": "Server error."
        }), 500


    finally:

        cursor.close()
        conn.close()

@app.route("/api/forgot-password/send-otp", methods=["POST"])
def send_password_reset_otp():

    data = request.get_json() or {}

    username = data.get("username", "").strip()
    mobile = data.get("mobile", "").strip()

    if not username or not mobile:
        return jsonify({
            "success": False,
            "message": "Username and mobile number are required."
        }), 400

    conn = get_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    try:

        # =========================
        # FIND ACCOUNT
        # =========================

        cursor.execute("""
            SELECT
                ua.id,
                ua.user_id,
                ua.username,
                m.phone_number AS member_phone,
                pm.phone_number AS pending_phone
            FROM user_accounts ua
            
            LEFT JOIN members m
                ON m.id COLLATE utf8mb4_general_ci
                = ua.user_id COLLATE utf8mb4_general_ci

            LEFT JOIN pending_members pm
                ON pm.account_id = ua.id

            WHERE ua.username = %s

            LIMIT 1
        """, (username,))

        user = cursor.fetchone()

        if not user:
            return jsonify({
                "success": False,
                "message": "Account not found."
            }), 404


        # =========================
        # GET REGISTERED MOBILE
        # =========================

        registered_mobile = (
            user["member_phone"]
            or user["pending_phone"]
            or ""
        ).strip()

        if not registered_mobile:
            return jsonify({
                "success": False,
                "message": "No registered mobile number found."
            }), 400


        # =========================
        # NORMALIZE NUMBERS
        # =========================

        entered_mobile = (
            mobile
            .replace(" ", "")
            .replace("-", "")
        )

        registered_mobile = (
            registered_mobile
            .replace(" ", "")
            .replace("-", "")
        )

        if entered_mobile.startswith("09"):
            entered_mobile = "+63" + entered_mobile[1:]

        if registered_mobile.startswith("09"):
            registered_mobile = "+63" + registered_mobile[1:]


        # =========================
        # CHECK MOBILE
        # =========================

        if entered_mobile != registered_mobile:

            return jsonify({
                "success": False,
                "message": "Mobile number does not match our records."
            }), 400


        # =========================
        # GENERATE OTP
        # =========================

        otp = generate_otp()

        otp_hash = hash_otp(otp)

        expires_at = (
            datetime.now()
            + timedelta(minutes=5)
        )


        # =========================
        # INVALIDATE OLD OTP
        # =========================

        cursor.execute("""
            UPDATE password_reset_otps

            SET used = 1

            WHERE user_id = %s
              AND used = 0
        """, (
            user["user_id"],
        ))


        # =========================
        # SAVE NEW OTP
        # =========================

        cursor.execute("""
            INSERT INTO password_reset_otps
            (
                user_id,
                otp_hash,
                expires_at
            )

            VALUES
            (
                %s,
                %s,
                %s
            )
        """, (
            user["user_id"],
            otp_hash,
            expires_at
        ))


        # =========================
        # SEND SMS
        # =========================

        message = (
            f"SMART GYM: Your password reset "
            f"verification code is {otp}. "
            f"This code expires in 5 minutes."
        )

        sms_sent = send_sms(
            registered_mobile,
            message
        )


        if not sms_sent:

            conn.rollback()

            return jsonify({
                "success": False,
                "message": "Failed to send verification code."
            }), 500


        # =========================
        # LOG SMS
        # =========================

        cursor.execute("""
            INSERT INTO sms_logs
            (
                user_id,
                sms_type
            )

            VALUES
            (
                %s,
                %s
            )
        """, (
            user["user_id"],
            "PASSWORD_RESET"
        ))


        conn.commit()


        return jsonify({
            "success": True,
            "message": "Verification code sent successfully."
        })


    except Exception as e:

        conn.rollback()

        print(
            "FORGOT PASSWORD OTP ERROR:",
            e
        )

        return jsonify({
            "success": False,
            "message": "Server error."
        }), 500


    finally:

        cursor.close()
        conn.close()

def activate_account():

    data = request.get_json()

    token = data.get("token")
    username = data.get("username")
    password = data.get("password")

    if not token or not username or not password:
        return jsonify({
            "success": False,
            "message": "Missing required fields."
        })

    conn = get_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    try:

        # CHECK TOKEN
        cursor.execute("""
            SELECT
                a.member_id,
                m.full_name
            FROM member_activation a
            JOIN members m
                ON a.member_id = m.id
            WHERE a.activation_token=%s
            AND a.status='PENDING'
            LIMIT 1
        """, (token,))

        activation = cursor.fetchone()

        if not activation:
            return jsonify({
                "success": False,
                "message": "Invalid activation link."
            })

        member_id = activation["member_id"]
        fullname = activation["full_name"]

        # CHECK DUPLICATE USERNAME
        cursor.execute("""
            SELECT id
            FROM user_accounts
            WHERE username=%s
        """, (username,))

        if cursor.fetchone():
            return jsonify({
                "success": False,
                "message": "Username already exists."
            })

        # INSERT ACCOUNT
        cursor.execute("""
            INSERT INTO user_accounts
            (
                user_id,
                fullname,
                username,
                password,
                role
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                'member'
            )
        """, (
            member_id,
            fullname,
            username,
            password
        ))

        # MARK TOKEN USED
        cursor.execute("""
            UPDATE member_activation
            SET status='USED'
            WHERE activation_token=%s
        """, (token,))

        conn.commit()

        return jsonify({
            "success": True,
            "message": "Account activated successfully."
        })

    except Exception as e:

        conn.rollback()

        return jsonify({
            "success": False,
            "message": str(e)
        })

    finally:

        cursor.close()
        conn.close()

@app.route("/api/activation_created", methods=["POST"])
def activation_created():

    data = request.get_json()

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            INSERT INTO member_activation
            (
                member_id,
                activation_token,
                status
            )
            VALUES (%s,%s,%s)

            ON DUPLICATE KEY UPDATE

                activation_token=VALUES(activation_token),
                status=VALUES(status)
        """, (

            data["member_id"],
            data["activation_token"],
            data.get("status", "PENDING")

        ))

        conn.commit()

        return jsonify({

            "success": True,
            "message": "Activation synchronized."

        })

    except Exception as e:

        conn.rollback()

        return jsonify({

            "success": False,
            "error": str(e)

        }), 500

    finally:

        cursor.close()
        conn.close()
@app.route("/api/activation/<token>", methods=["GET"])
def check_activation(token):

    conn = get_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    try:

        cursor.execute("""
            SELECT

                a.member_id,
                a.status,
                m.full_name

            FROM member_activation a

            JOIN members m
                ON a.member_id = m.id

            WHERE a.activation_token = %s

            LIMIT 1
        """, (token,))

        activation = cursor.fetchone()

        # Token not found
        if not activation:

            return jsonify({

                "success": False,
                "message": "Invalid activation link."

            }), 404

        # Already used
        if activation["status"] == "USED":

            return jsonify({

                "success": False,
                "message": "This activation link has already been used."

            })

        # Valid
        return jsonify({

            "success": True,

            "member_id": activation["member_id"],

            "full_name": activation["full_name"]

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)

        }), 500

    finally:

        cursor.close()
        conn.close()

# ============================================
# 📊 REPORTS - ATTENDANCE API
# ============================================

@app.route("/api/reports/attendance", methods=["GET"])
def reports_attendance():

    conn = None

    try:

        # ========================================
        # GET DATE RANGE
        # ========================================

        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")

        # If no dates supplied → today
        if not start_date:
            start_date = datetime.now().strftime("%Y-%m-%d")

        if not end_date:
            end_date = start_date


        # ========================================
        # VALIDATE DATE RANGE
        # ========================================

        try:

            start = datetime.strptime(
                start_date,
                "%Y-%m-%d"
            ).date()

            end = datetime.strptime(
                end_date,
                "%Y-%m-%d"
            ).date()

        except ValueError:

            return jsonify({
                "success": False,
                "message": "Invalid date format. Use YYYY-MM-DD.",
                "data": []
            }), 400


        if start > end:

            return jsonify({
                "success": False,
                "message": "Start date cannot be later than end date.",
                "data": []
            }), 400


        # ========================================
        # DATABASE
        # ========================================

        conn = get_connection()

        cursor = conn.cursor(
            pymysql.cursors.DictCursor
        )


        # ========================================
        # ATTENDANCE QUERY
        # ========================================

        cursor.execute("""
            SELECT

                a.user_id,

                COALESCE(
                    m.full_name,
                    w.full_name,
                    a.user_id
                ) AS name,

                CASE

                    WHEN m.id IS NOT NULL
                        THEN 'Member'

                    WHEN w.id IS NOT NULL
                        THEN 'Walk-in'

                    ELSE '-'

                END AS type,

                a.time_in,

                a.time_out,

                a.status

            FROM attendance_sessions a

            LEFT JOIN members m

                ON CONVERT(a.user_id USING utf8mb4)
                COLLATE utf8mb4_general_ci

                =

                CONVERT(m.id USING utf8mb4)
                COLLATE utf8mb4_general_ci


            LEFT JOIN walkins w

                ON CONVERT(a.user_id USING utf8mb4)
                COLLATE utf8mb4_general_ci

                =

                CONVERT(w.id USING utf8mb4)
                COLLATE utf8mb4_general_ci


            WHERE DATE(a.time_in)
                BETWEEN %s AND %s


            ORDER BY
                a.time_in DESC

        """, (
            start_date,
            end_date
        ))


        rows = cursor.fetchall()


        # ========================================
        # FORMAT DATA
        # ========================================

        data = []


        for row in rows:

            # ------------------------------------
            # ID
            # ------------------------------------

            user_id = (
                row["user_id"]
                if row["user_id"]
                else "-"
            )


            # ------------------------------------
            # TIME IN
            # ------------------------------------

            time_in = "-"

            if row["time_in"]:

                time_in = row["time_in"].strftime(
                    "%I:%M %p"
                )


            # ------------------------------------
            # TIME OUT
            # ------------------------------------

            time_out = "-"

            if row["time_out"]:

                time_out = row["time_out"].strftime(
                    "%I:%M %p"
                )


            # ------------------------------------
            # DURATION
            # ------------------------------------

            duration = "-"

            if row["time_in"] and row["time_out"]:

                seconds = (
                    row["time_out"]
                    - row["time_in"]
                ).total_seconds()


                minutes = int(
                    seconds // 60
                )


                hours = minutes // 60

                remaining_minutes = (
                    minutes % 60
                )


                if hours > 0:

                    duration = (
                        f"{hours}h "
                        f"{remaining_minutes}m"
                    )

                else:

                    duration = (
                        f"{remaining_minutes}m"
                    )


            # ------------------------------------
            # REMARKS
            # ------------------------------------

            if row["time_out"]:

                remarks = "Completed"

            else:

                remarks = "Active"


            # ------------------------------------
            # VISIT DATE
            # ------------------------------------

            visit_date = "-"

            if row["time_in"]:

                visit_date = (
                    row["time_in"]
                    .strftime("%Y-%m-%d")
                )


            # ------------------------------------
            # APPEND
            # ------------------------------------

            data.append({

                "id":
                    user_id,

                "name":
                    row["name"]
                    if row["name"]
                    else "-",

                "type":
                    row["type"]
                    if row["type"]
                    else "-",

                "time_in":
                    time_in,

                "time_out":
                    time_out,

                "duration":
                    duration,

                "visit_date":
                    visit_date,

                "remarks":
                    remarks

            })


        # ========================================
        # RESPONSE
        # ========================================

        return jsonify({

            "success": True,

            "start_date":
                start_date,

            "end_date":
                end_date,

            "total":
                len(data),

            "data":
                data

        })


    except Exception as e:

        print(
            "❌ REPORTS ATTENDANCE API ERROR:",
            e
        )


        return jsonify({

            "success": False,

            "message":
                str(e),

            "data":
                []

        }), 500


    finally:

        if conn:

            conn.close()

# ============================================
# 📊 REPORTS - LOCKER API
# ============================================

@app.route("/api/reports/locker", methods=["GET"])
def reports_locker():

    conn = None

    try:

        # ========================================
        # DATE RANGE
        # ========================================

        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")


        if not start_date:
            start_date = datetime.now().strftime("%Y-%m-%d")


        if not end_date:
            end_date = start_date


        # ========================================
        # VALIDATE DATES
        # ========================================

        try:

            start = datetime.strptime(
                start_date,
                "%Y-%m-%d"
            ).date()

            end = datetime.strptime(
                end_date,
                "%Y-%m-%d"
            ).date()

        except ValueError:

            return jsonify({
                "success": False,
                "message": "Invalid date format. Use YYYY-MM-DD.",
                "data": []
            }), 400


        if start > end:

            return jsonify({
                "success": False,
                "message": "Start date cannot be later than end date.",
                "data": []
            }), 400


        # ========================================
        # DATABASE
        # ========================================

        conn = get_connection()

        cursor = conn.cursor(
            pymysql.cursors.DictCursor
        )


        # ========================================
        # LOCKER SESSIONS
        # ========================================

        cursor.execute("""

            SELECT

                l.id,

                l.user_id,

                l.locker_number,

                l.start_time,

                l.end_time,


                COALESCE(
                    m.full_name,
                    w.full_name,
                    l.user_id
                ) AS name,


                CASE

                    WHEN m.id IS NOT NULL
                        THEN 'Member'

                    WHEN w.id IS NOT NULL
                        THEN 'Walk-in'

                    ELSE '-'

                END AS type


            FROM locker_sessions l


            LEFT JOIN members m

                ON CONVERT(l.user_id USING utf8mb4)
                COLLATE utf8mb4_general_ci

                =

                CONVERT(m.id USING utf8mb4)
                COLLATE utf8mb4_general_ci


            LEFT JOIN walkins w

                ON CONVERT(l.user_id USING utf8mb4)
                COLLATE utf8mb4_general_ci

                =

                CONVERT(w.id USING utf8mb4)
                COLLATE utf8mb4_general_ci


            WHERE DATE(l.start_time)
                BETWEEN %s AND %s


            ORDER BY
                l.start_time DESC

        """, (
            start_date,
            end_date
        ))


        rows = cursor.fetchall()


        # ========================================
        # FORMAT DATA
        # ========================================

        data = []


        for row in rows:

            # ------------------------------------
            # START TIME
            # ------------------------------------

            start_time = "-"

            if row["start_time"]:

                start_time = row["start_time"].strftime(
                    "%I:%M %p"
                )


            # ------------------------------------
            # END TIME
            # ------------------------------------

            end_time = "-"

            if row["end_time"]:

                end_time = row["end_time"].strftime(
                    "%I:%M %p"
                )


            # ------------------------------------
            # DURATION
            # ------------------------------------

            duration = "-"


            if (
                row["start_time"]
                and row["end_time"]
            ):

                total_minutes = int(
                    (
                        row["end_time"]
                        - row["start_time"]
                    ).total_seconds()
                    // 60
                )


                hours = total_minutes // 60

                minutes = total_minutes % 60


                if hours > 0:

                    duration = (
                        f"{hours}h "
                        f"{minutes:02d}m"
                    )

                else:

                    duration = (
                        f"{minutes}m"
                    )


            # ------------------------------------
            # STATUS
            # ------------------------------------

            if not row["end_time"]:

                status = "Active"

            else:

                status = "Completed"


            # ------------------------------------
            # VISIT DATE
            # ------------------------------------

            visit_date = "-"


            if row["start_time"]:

                visit_date = row["start_time"].strftime(
                    "%Y-%m-%d"
                )


            # ------------------------------------
            # DATA
            # ------------------------------------

            data.append({

                "id":
                    row["id"],

                "locker_number":
                    row["locker_number"],

                "user_id":
                    row["user_id"],

                "name":
                    row["name"]
                    if row["name"]
                    else "-",

                "type":
                    row["type"]
                    if row["type"]
                    else "-",

                "start_time":
                    start_time,

                "end_time":
                    end_time,

                "duration":
                    duration,

                "status":
                    status,

                "visit_date":
                    visit_date

            })


        # ========================================
        # SUMMARY
        # ========================================

        total_usage = len(data)


        total_members = sum(
            1
            for row in data
            if str(row["type"]).lower() == "member"
        )


        total_walkins = sum(
            1
            for row in data
            if str(row["type"]).lower() in ["walk-in", "walkin"]
        )

        # ========================================
        # RESPONSE
        # ========================================

        return jsonify({

            "success": True,

            "start_date":
                start_date,

            "end_date":
                end_date,

            "total":
                total_usage,

            "members":
                total_members,

            "walkins":
                total_walkins,

            "data":
                data

        })


    except Exception as e:

        print(
            "❌ LOCKER REPORT API ERROR:",
            e
        )


        return jsonify({

            "success": False,

            "message":
                str(e),

            "total": 0,

            "members": 0,

            "walkins": 0,

            "data": []

        }), 500


    finally:

        if conn:
            conn.close()
# ==============================
# 📊 DAILY ATTENDANCE SUMMARY
# ==============================

@app.route("/api/attendance_summary", methods=["GET"])
def get_attendance_summary():

    conn = None

    try:

        conn = get_connection()

        cursor = conn.cursor(
            pymysql.cursors.DictCursor
        )

        cursor.execute("""
            SELECT
                SUM(
                    DATE(time_in) = CURDATE()
                ) AS today,

                SUM(
                    DATE(time_in) = CURDATE() - INTERVAL 1 DAY
                ) AS yesterday

            FROM attendance_sessions

            WHERE DATE(time_in)
                IN (
                    CURDATE(),
                    CURDATE() - INTERVAL 1 DAY
                )
        """)

        row = cursor.fetchone()

        today = row["today"] or 0
        yesterday = row["yesterday"] or 0


        # ==============================
        # PERCENTAGE CHANGE
        # ==============================

        if yesterday > 0:

            percentage = (
                (today - yesterday)
                / yesterday
            ) * 100

        else:

            percentage = 100 if today > 0 else 0


        return jsonify({

            "today": today,

            "yesterday": yesterday,

            "difference": today - yesterday,

            "percentage": round(
                percentage,
                1
            )

        })


    except Exception as e:

        print(
            "ATTENDANCE SUMMARY ERROR:",
            e
        )

        return jsonify({

            "today": 0,

            "yesterday": 0,

            "difference": 0,

            "percentage": 0,

            "error": str(e)

        }), 500


    finally:

        if conn:
            conn.close()

@app.route("/api/walkins_summary", methods=["GET"])
def walkins_summary():

    conn = get_connection()
    cursor = conn.cursor(
        pymysql.cursors.DictCursor
    )

    try:

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM walkins
            WHERE visit_date = CURDATE()
        """)

        row = cursor.fetchone()

        return jsonify({
            "today": row["total"]
        })

    except Exception as e:

        print("WALKIN SUMMARY ERROR:", e)

        return jsonify({
            "today": 0,
            "error": str(e)
        }), 500

    finally:

        cursor.close()
        conn.close()
        
@app.route("/api/trainer_plans", methods=["GET"])
def trainer_plans():

    conn = None
    cursor = None

    try:

        conn = get_connection()

        cursor = conn.cursor(
            pymysql.cursors.DictCursor
        )

        cursor.execute("""
            SELECT
                tp.id,
                tp.trainer_id,
                ua.fullname,
                ua.username,
                tp.plan_name,
                tp.duration_days,
                tp.price,
                tp.active
            FROM trainer_plans tp
            INNER JOIN user_accounts ua
                ON tp.trainer_id = ua.user_id
            WHERE ua.role = 'trainer'
            ORDER BY tp.trainer_id, tp.duration_days
        """)

        rows = cursor.fetchall()

        return jsonify(rows), 200

    except Exception as e:

        print("GET TRAINER PLANS ERROR:", e)

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


# =========================================================
# TRAINER MESSAGES
# GET MESSAGES RECEIVED BY TRAINER
# =========================================================

@app.route(
    "/api/trainer_messages",
    methods=["GET"]
)
def trainer_messages():

    conn = None
    cursor = None

    try:

        # =====================================================
        # GET TRAINER ID
        # =====================================================

        trainer_id = str(
            request.args.get(
                "trainer_id",
                ""
            )
        ).strip()


        # =====================================================
        # VALIDATION
        # =====================================================

        if not trainer_id:

            return jsonify({
                "success": False,
                "message": "Trainer ID is required."
            }), 400


        # =====================================================
        # DATABASE
        # =====================================================

        conn = get_connection()

        cursor = conn.cursor(
            pymysql.cursors.DictCursor
        )


        # =====================================================
        # GET TRAINER MESSAGES
        # =====================================================
        
        cursor.execute("""
            SELECT
                m.id,
                m.user_id,
                m.sender_id,
                m.sender_name AS member_name,
                m.sender_role,
                m.title,
                m.message,
                m.reason,
                m.is_read,

                DATE_FORMAT(
                    CONVERT_TZ(
                        m.created_at,
                        '+00:00',
                        '+08:00'
                    ),
                    '%%M %%d, %%Y %%h:%%i %%p'
                ) AS created_at

            FROM messages m

            WHERE m.user_id = %s
            AND m.receiver_role = 'trainer'

            ORDER BY m.id DESC

        """, (
            trainer_id,
        ))



        rows = cursor.fetchall()


        # =====================================================
        # RESPONSE
        # =====================================================

        return jsonify(
            rows
        ), 200


    except Exception as e:

        print(
            "TRAINER MESSAGES ERROR:",
            e
        )


        return jsonify({

            "success":
                False,

            "message":
                str(e)

        }), 500


    finally:

        if cursor:

            cursor.close()

        if conn:

            conn.close()
# =========================================================
# TRAINER REQUEST
# MEMBER -> TRAINER
# =========================================================
@app.route(
    "/api/trainer/request",
    methods=["POST"]
)
def create_trainer_request():

    conn = None
    cursor = None

    try:

        data = request.get_json() or {}

        member_id = str(
            data.get("member_id", "")
        ).strip()

        trainer_id = str(
            data.get("trainer_id", "")
        ).strip()

        program_id = data.get(
            "program_id"
        )

        program_plan_id = data.get(
            "program_plan_id"
        )

        plan_id = data.get(
            "plan_id"
        )

        start_date = str(
            data.get("start_date", "")
        ).strip()


        # =================================================
        # VALIDATION
        # =================================================

        if not member_id:

            return jsonify({
                "status": "error",
                "message": "Member ID is required."
            }), 400


        if not trainer_id:

            return jsonify({
                "status": "error",
                "message": "Trainer ID is required."
            }), 400


        if not program_id:

            return jsonify({
                "status": "error",
                "message": "Program ID is required."
            }), 400


        if not program_plan_id:

            return jsonify({
                "status": "error",
                "message": "Program Plan ID is required."
            }), 400


        if not plan_id:

            return jsonify({
                "status": "error",
                "message": "Trainer Rate Plan ID is required."
            }), 400


        if not start_date:

            return jsonify({
                "status": "error",
                "message": "Training start date is required."
            }), 400


        # =================================================
        # START DATE
        # =================================================

        try:

            start_date_obj = datetime.strptime(
                start_date,
                "%Y-%m-%d"
            ).date()

        except ValueError:

            return jsonify({
                "status": "error",
                "message": "Invalid training start date."
            }), 400


        today = datetime.now().date()


        if start_date_obj < today:

            return jsonify({
                "status": "error",
                "message": "Training start date cannot be in the past."
            }), 400


        # =================================================
        # DATABASE CONNECTION
        # =================================================

        conn = get_connection()

        cursor = conn.cursor(
            pymysql.cursors.DictCursor
        )


        # =================================================
        # GET MEMBER
        # =================================================

        cursor.execute("""
            SELECT
                id,
                full_name
            FROM members
            WHERE id = %s
            LIMIT 1
        """, (
            member_id,
        ))

        member = cursor.fetchone()


        if not member:

            return jsonify({
                "status": "error",
                "message": "Member not found."
            }), 404


        # =================================================
        # GET TRAINER
        # =================================================

        cursor.execute("""
            SELECT
                user_id,
                fullname
            FROM user_accounts
            WHERE user_id = %s
            AND role = 'trainer'
            LIMIT 1
        """, (
            trainer_id,
        ))

        trainer = cursor.fetchone()


        if not trainer:

            return jsonify({
                "status": "error",
                "message": "Trainer not found."
            }), 404


        # =================================================
        # GET PROGRAM
        # =================================================

        cursor.execute("""
            SELECT
                id,
                program_name,
                description,
                duration_days,
                active
            FROM programs
            WHERE id = %s
            AND active = 1
            LIMIT 1
        """, (
            program_id,
        ))

        program = cursor.fetchone()


        if not program:

            return jsonify({
                "status": "error",
                "message": "Program not found."
            }), 404


        # =================================================
        # GET PROGRAM PLAN / SPLIT
        # =================================================

        cursor.execute("""
            SELECT
                id,
                program_id,
                plan_name,
                description,
                active
            FROM program_plans
            WHERE id = %s
            AND program_id = %s
            AND active = 1
            LIMIT 1
        """, (
            program_plan_id,
            program_id
        ))

        program_plan = cursor.fetchone()


        if not program_plan:

            return jsonify({
                "status": "error",
                "message":
                    "Program plan not found for this program."
            }), 404


        # =================================================
        # GET TRAINER RATE PLAN
        # =================================================

        cursor.execute("""
            SELECT
                id,
                trainer_id,
                plan_name,
                duration_days,
                price,
                active
            FROM trainer_plans
            WHERE id = %s
            AND trainer_id = %s
            LIMIT 1
        """, (
            plan_id,
            trainer_id
        ))

        plan = cursor.fetchone()


        if not plan:

            return jsonify({
                "status": "error",
                "message": "Trainer plan not found."
            }), 404


        if int(plan["active"]) != 1:

            return jsonify({
                "status": "error",
                "message":
                    "This trainer plan is not available."
            }), 400


        # =================================================
        # PROGRAM DURATION
        #
        # IMPORTANT:
        # PROGRAM duration is independent from
        # TRAINER RATE duration.
        #
        # Example:
        # General Fitness = 30 days
        # Daily Rate      = 1 day
        #
        # End date follows PROGRAM duration.
        # =================================================

        program_duration_days = int(
            program["duration_days"]
        )


        if program_duration_days <= 0:

            return jsonify({
                "status": "error",
                "message": "Invalid program duration."
            }), 400


        end_date_obj = (
            start_date_obj +
            timedelta(
                days=program_duration_days - 1
            )
        )


        # =================================================
        # CHECK EXISTING MEMBER TRAINER RECORD
        # =================================================

        cursor.execute("""
            SELECT
                tt.id,
                tt.trainer_id,
                ua.fullname AS trainer_name,
                tt.member_id,

                tt.program_id,
                tt.program_plan_id,
                tt.plan_id,

                tt.start_date,
                tt.end_date,
                tt.status

            FROM trainer_trainees tt

            INNER JOIN user_accounts ua
                ON tt.trainer_id = ua.user_id

            WHERE tt.member_id = %s

            LIMIT 1
        """, (
            member_id,
        ))

        existing = cursor.fetchone()


        # =================================================
        # CHECK DATE OVERLAP
        # =================================================

        if existing:

            if existing["status"] in (
                "pending",
                "active"
            ):

                existing_start = (
                    existing["start_date"]
                )

                existing_end = (
                    existing["end_date"]
                )


                overlap = (
                    existing_start <= end_date_obj
                    and
                    existing_end >= start_date_obj
                )


                if overlap:

                    return jsonify({
                        "status": "error",
                        "message":
                            "You already have a trainer during the selected dates.",

                        "existing_trainer":
                            existing["trainer_name"],

                        "existing_start_date":
                            existing_start.strftime(
                                "%Y-%m-%d"
                            ),

                        "existing_end_date":
                            existing_end.strftime(
                                "%Y-%m-%d"
                            ),

                        "existing_status":
                            existing["status"]
                    }), 409


        # =================================================
        # DETERMINE ACTION
        # =================================================

        request_status = "pending"

        action = "created"


        if existing:

            if existing["status"] == "cancelled":

                request_status = "pending"

                action = "created"


            elif (
                existing["status"] == "completed"
                and
                existing["trainer_id"] == trainer_id
            ):

                request_status = "active"

                action = "renewed"


            else:

                request_status = "pending"

                action = "changed_trainer"


        # =================================================
        # UPDATE EXISTING RECORD
        # =================================================

        if existing:

            cursor.execute("""
                UPDATE trainer_trainees

                SET

                    trainer_id = %s,

                    program_id = %s,

                    program_plan_id = %s,

                    plan_id = %s,

                    start_date = %s,

                    end_date = %s,

                    status = %s,

                    created_at = CONVERT_TZ(
                        NOW(),
                        '+00:00',
                        '+08:00'
                    )

                WHERE id = %s

            """, (
                trainer_id,

                program_id,

                program_plan_id,

                plan_id,

                start_date_obj,

                end_date_obj,

                request_status,

                existing["id"]
            ))


            request_id = existing["id"]


        # =================================================
        # INSERT NEW RECORD
        # =================================================

        else:

            cursor.execute("""
                INSERT INTO trainer_trainees
                (
                    trainer_id,
                    member_id,
                    program_id,
                    program_plan_id,
                    plan_id,
                    start_date,
                    end_date,
                    status
                )

                VALUES
                (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )

            """, (
                trainer_id,

                member_id,

                program_id,

                program_plan_id,

                plan_id,

                start_date_obj,

                end_date_obj,

                "pending"
            ))


            request_id = cursor.lastrowid

            request_status = "pending"

            action = "created"


        # =================================================
        # CREATE TRAINER MESSAGE
        # =================================================

        print(
            "CREATING TRAINER MESSAGE..."
        )


        cursor.execute("""
            INSERT INTO messages
            (
                user_id,
                sender_id,
                sender_name,
                sender_role,
                title,
                message,
                reason,
                receiver_role,
                is_read
            )

            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                0
            )

        """, (

            trainer["user_id"],

            member_id,

            member["full_name"],

            "member",

            (
                "TRAINER RENEWAL"
                if action == "renewed"
                else
                "NEW TRAINER REQUEST"
            ),

            (
                f"{member['full_name']} renewed training with you."
                if action == "renewed"
                else
                f"{member['full_name']} sent you a trainer request."
            ),

            "-",

            "trainer"

        ))


        trainer_message_id = cursor.lastrowid


        print(
            "TRAINER MESSAGE CREATED:",
            trainer_message_id
        )


        # =================================================
        # COMMIT
        # =================================================

        conn.commit()


        # =================================================
        # RESPONSE MESSAGE
        # =================================================

        if action == "renewed":

            message = (
                "Training renewed successfully."
            )

        elif action == "changed_trainer":

            message = (
                "Trainer request submitted successfully."
            )

        else:

            message = (
                "Trainer request submitted successfully."
            )


        # =================================================
        # RESPONSE
        # =================================================

        return jsonify({

            "status":
                "success",

            "message":
                message,

            "action":
                action,

            "request_id":
                request_id,


            # =================================================
            # MEMBER
            # =================================================

            "member_id":
                member_id,

            "member_name":
                member["full_name"],


            # =================================================
            # TRAINER
            # =================================================

            "trainer_id":
                trainer_id,

            "trainer_name":
                trainer["fullname"],


            # =================================================
            # PROGRAM
            # =================================================

            "program_id":
                program["id"],

            "program_name":
                program["program_name"],

            "program_duration_days":
                program["duration_days"],


            # =================================================
            # PROGRAM PLAN / SPLIT
            # =================================================

            "program_plan_id":
                program_plan["id"],

            "program_plan_name":
                program_plan["plan_name"],


            # =================================================
            # TRAINER RATE
            # =================================================

            "plan_id":
                plan["id"],

            "plan_name":
                plan["plan_name"],

            "trainer_rate_duration_days":
                plan["duration_days"],

            "price":
                str(plan["price"]),


            # =================================================
            # DATES
            # =================================================

            "start_date":
                start_date_obj.strftime(
                    "%Y-%m-%d"
                ),

            "end_date":
                end_date_obj.strftime(
                    "%Y-%m-%d"
                ),


            # =================================================
            # STATUS
            # =================================================

            "status":
                request_status

        }), 201


    except Exception as e:

        if conn:

            conn.rollback()


        print(
            "CREATE TRAINER REQUEST ERROR:",
            e
        )


        return jsonify({
            "status":
                "error",

            "message":
                str(e)
        }), 500


    finally:

        if cursor:

            cursor.close()


        if conn:

            conn.close()
            
@app.route(
    "/api/trainer/trainees/<trainer_id>",
    methods=["GET"]
)
def get_trainer_trainees(trainer_id):

    conn = None
    cursor = None

    try:

        trainer_id = str(
            trainer_id
        ).strip()


        # =====================================================
        # VALIDATION
        # =====================================================

        if not trainer_id:

            return jsonify({
                "status": "error",
                "message": "Trainer ID is required."
            }), 400


        # =====================================================
        # DATABASE CONNECTION
        # =====================================================

        conn = get_connection()

        cursor = conn.cursor(
            pymysql.cursors.DictCursor
        )


        # =====================================================
        # AUTO-COMPLETE EXPIRED ACTIVE TRAINING
        # =====================================================

        cursor.execute("""
            UPDATE trainer_trainees
            SET status = 'completed'
            WHERE trainer_id = %s
            AND status = 'active'
            AND end_date < CURDATE()
        """, (
            trainer_id,
        ))


        conn.commit()


        # =====================================================
        # GET ACTIVE + COMPLETED TRAINEES
        # =====================================================

        cursor.execute("""
            SELECT
                tt.id,
                tt.trainer_id,
                tt.member_id,

                m.full_name,

                tt.plan_id,

                tp.plan_name,
                tp.duration_days,

                tt.start_date,
                tt.end_date,

                tt.status,

                tt.created_at

            FROM trainer_trainees tt

            INNER JOIN members m
                ON tt.member_id = m.id

            INNER JOIN trainer_plans tp
                ON tt.plan_id = tp.id

            WHERE tt.trainer_id = %s

            AND tt.status IN (
                'active',
                'completed'
            )

            ORDER BY
                CASE
                    WHEN tt.status = 'active'
                    THEN 0
                    ELSE 1
                END,

                tt.end_date DESC,

                tt.created_at DESC
        """, (
            trainer_id,
        ))


        rows = cursor.fetchall()


        # =====================================================
        # FORMAT DATES
        # =====================================================

        for row in rows:

            if row["start_date"] is not None:

                row["start_date"] = \
                    row["start_date"].strftime(
                        "%Y-%m-%d"
                    )


            if row["end_date"] is not None:

                row["end_date"] = \
                    row["end_date"].strftime(
                        "%Y-%m-%d"
                    )


            if row["created_at"] is not None:

                row["created_at"] = \
                    row["created_at"].strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )


        # =====================================================
        # RESPONSE
        # =====================================================

        return jsonify(
            rows
        ), 200


    except Exception as e:

        if conn:

            conn.rollback()


        print(
            "GET TRAINER TRAINEES ERROR:",
            e
        )


        return jsonify({

            "status":
                "error",

            "message":
                str(e)

        }), 500


    finally:

        if cursor:

            cursor.close()

        if conn:

            conn.close()
# =========================================================
# GET TRAINER CLIENT REQUESTS
# =========================================================

# =========================================================
# GET TRAINER CLIENT REQUESTS
# =========================================================

@app.route(
    "/api/trainer/requests/<trainer_id>",
    methods=["GET"]
)
def get_trainer_requests(trainer_id):

    conn = None
    cursor = None

    try:

        trainer_id = str(
            trainer_id
        ).strip()

        if not trainer_id:

            return jsonify({
                "status": "error",
                "message": "Trainer ID is required."
            }), 400


        conn = get_connection()

        cursor = conn.cursor(
            pymysql.cursors.DictCursor
        )


        # =================================================
        # GET PENDING TRAINER REQUESTS
        # =================================================

        cursor.execute("""
            SELECT

                /* =========================
                   REQUEST
                   ========================= */

                tt.id,

                tt.trainer_id,

                tt.member_id,


                /* =========================
                   MEMBER
                   ========================= */

                m.full_name,


                /* =========================
                   PROGRAM
                   ========================= */

                tt.program_id,

                p.program_name,


                /* =========================
                   PROGRAM PLAN / SPLIT
                   ========================= */

                tt.program_plan_id,

                pp.plan_name AS program_plan_name,


                /* =========================
                   TRAINER RATE
                   ========================= */

                tt.plan_id,

                tp.plan_name,

                tp.duration_days,

                tp.price,


                /* =========================
                   DATES
                   ========================= */

                tt.start_date,

                tt.end_date,


                /* =========================
                   STATUS
                   ========================= */

                tt.status,

                tt.created_at


            FROM trainer_trainees tt


            /* =========================
               MEMBER
               ========================= */

            INNER JOIN members m

                ON tt.member_id = m.id


            /* =========================
               PROGRAM
               ========================= */

            LEFT JOIN programs p

                ON tt.program_id = p.id


            /* =========================
               PROGRAM PLAN / SPLIT
               ========================= */

            LEFT JOIN program_plans pp

                ON tt.program_plan_id = pp.id


            /* =========================
               TRAINER RATE
               ========================= */

            INNER JOIN trainer_plans tp

                ON tt.plan_id = tp.id


            /* =========================
               FILTER
               ========================= */

            WHERE tt.trainer_id = %s

            AND tt.status = 'pending'


            /* =========================
               LATEST REQUEST FIRST
               ========================= */

            ORDER BY
                tt.created_at DESC

        """, (
            trainer_id,
        ))


        rows = cursor.fetchall()


        # =================================================
        # FORMAT DATA
        # =================================================

        for row in rows:


            # =========================
            # START DATE
            # =========================

            if row["start_date"] is not None:

                row["start_date"] = (
                    row["start_date"]
                    .strftime("%Y-%m-%d")
                )


            # =========================
            # END DATE
            # =========================

            if row["end_date"] is not None:

                row["end_date"] = (
                    row["end_date"]
                    .strftime("%Y-%m-%d")
                )


            # =========================
            # CREATED AT
            # =========================

            if row["created_at"] is not None:

                row["created_at"] = (
                    row["created_at"]
                    .strftime("%Y-%m-%d %H:%M:%S")
                )


            # =========================
            # PRICE
            # =========================

            if row["price"] is not None:

                row["price"] = float(
                    row["price"]
                )


        # =================================================
        # RESPONSE
        # =================================================

        return jsonify(rows), 200


    except Exception as e:

        print(
            "GET TRAINER REQUESTS ERROR:",
            e
        )


        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


    finally:

        if cursor:
            cursor.close()


        if conn:
            conn.close()
 
 
# =========================================================
# ACCEPT TRAINER REQUEST
# =========================================================

@app.route(
    "/api/trainer/request/<int:request_id>/accept",
    methods=["POST"]
)
def accept_trainer_request(request_id):

    conn = None
    cursor = None

    try:

        data = request.get_json() or {}

        trainer_id = str(
            data.get("trainer_id", "")
        ).strip()


        if not trainer_id:

            return jsonify({
                "status": "error",
                "message": "Trainer ID is required."
            }), 400


        conn = get_connection()

        cursor = conn.cursor(
            pymysql.cursors.DictCursor
        )


        # =================================================
        # CHECK REQUEST
        # =================================================

        cursor.execute("""
            SELECT
                id,
                trainer_id,
                member_id,
                plan_id,
                status
            FROM trainer_trainees
            WHERE id = %s
            AND trainer_id = %s
            LIMIT 1
        """, (
            request_id,
            trainer_id
        ))


        request_row = cursor.fetchone()


        if not request_row:

            return jsonify({
                "status": "error",
                "message": "Trainer request not found."
            }), 404


        if request_row["status"] != "pending":

            return jsonify({
                "status": "error",
                "message": "This request is no longer pending."
            }), 409


        # =================================================
        # ACCEPT
        # =================================================

        cursor.execute("""
            UPDATE trainer_trainees
            SET status = 'active'
            WHERE id = %s
            AND trainer_id = %s
            AND status = 'pending'
        """, (
            request_id,
            trainer_id
        ))


        conn.commit()


        return jsonify({

            "status": "success",

            "message":
                "Trainer request accepted successfully.",

            "request_id":
                request_id,

            "member_id":
                request_row["member_id"],

            "trainer_id":
                trainer_id,

            "plan_id":
                request_row["plan_id"],

            "new_status":
                "active"

        }), 200


    except Exception as e:

        if conn:
            conn.rollback()


        print(
            "ACCEPT TRAINER REQUEST ERROR:",
            e
        )


        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close() 
 
# =========================================================
# REJECT TRAINER REQUEST
# =========================================================

@app.route(
    "/api/trainer/request/<int:request_id>/reject",
    methods=["POST"]
)
def reject_trainer_request(request_id):

    conn = None
    cursor = None

    try:

        data = request.get_json() or {}

        trainer_id = str(
            data.get("trainer_id", "")
        ).strip()


        if not trainer_id:

            return jsonify({
                "status": "error",
                "message": "Trainer ID is required."
            }), 400


        conn = get_connection()

        cursor = conn.cursor(
            pymysql.cursors.DictCursor
        )


        # =================================================
        # CHECK REQUEST
        # =================================================

        cursor.execute("""
            SELECT
                id,
                trainer_id,
                member_id,
                plan_id,
                status
            FROM trainer_trainees
            WHERE id = %s
            AND trainer_id = %s
            LIMIT 1
        """, (
            request_id,
            trainer_id
        ))


        request_row = cursor.fetchone()


        if not request_row:

            return jsonify({
                "status": "error",
                "message": "Trainer request not found."
            }), 404


        if request_row["status"] != "pending":

            return jsonify({
                "status": "error",
                "message": "This request is no longer pending."
            }), 409


        # =================================================
        # REJECT
        # =================================================

        cursor.execute("""
            UPDATE trainer_trainees
            SET status = 'cancelled'
            WHERE id = %s
            AND trainer_id = %s
            AND status = 'pending'
        """, (
            request_id,
            trainer_id
        ))


        conn.commit()


        return jsonify({

            "status": "success",

            "message":
                "Trainer request rejected successfully.",

            "request_id":
                request_id,

            "member_id":
                request_row["member_id"],

            "trainer_id":
                trainer_id,

            "plan_id":
                request_row["plan_id"],

            "new_status":
                "cancelled"

        }), 200


    except Exception as e:

        if conn:
            conn.rollback()


        print(
            "REJECT TRAINER REQUEST ERROR:",
            e
        )


        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()

@app.route("/api/trainer/workout", methods=["POST"])
def create_trainer_workout():

    conn = None
    cursor = None

    try:

        data = request.json

        member_id = str(
            data.get("member_id", "")
        ).strip()

        trainer_id = str(
            data.get("trainer_id", "")
        ).strip()

        workout_date = data.get(
            "workout_date"
        )

        workout_name = str(
            data.get("workout_name", "")
        ).strip()


        # =========================
        # VALIDATION
        # =========================

        if not member_id:
            return jsonify({
                "status": "error",
                "message": "Member ID is required."
            }), 400


        if not trainer_id:
            return jsonify({
                "status": "error",
                "message": "Trainer ID is required."
            }), 400


        if not workout_date:
            return jsonify({
                "status": "error",
                "message": "Workout date is required."
            }), 400


        if not workout_name:
            return jsonify({
                "status": "error",
                "message": "Workout name is required."
            }), 400


        # =========================
        # DATABASE
        # =========================

        conn = get_connection()

        cursor = conn.cursor(
            pymysql.cursors.DictCursor
        )


        cursor.execute("""
            INSERT INTO trainer_workout_schedule
            (
                member_id,
                trainer_id,
                workout_date,
                workout_name,
                status
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                'scheduled'
            )
        """, (
            member_id,
            trainer_id,
            workout_date,
            workout_name
        ))


        conn.commit()


        return jsonify({
            "status": "success",
            "message": "Workout scheduled successfully.",
            "workout_id": cursor.lastrowid
        }), 201


    except Exception as e:

        if conn:
            conn.rollback()

        print(
            "CREATE TRAINER WORKOUT ERROR:",
            e
        )

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()

@app.route(
    "/api/member/workout-schedule/<member_id>",
    methods=["GET"]
)
def get_member_workout_schedule(member_id):

    conn = None
    cursor = None

    try:

        member_id = str(
            member_id
        ).strip()


        if not member_id:

            return jsonify({
                "status": "error",
                "message": "Member ID is required."
            }), 400


        conn = get_connection()

        cursor = conn.cursor(
            pymysql.cursors.DictCursor
        )


        cursor.execute("""
            SELECT

                id,
                member_id,
                trainer_id,
                workout_date,
                workout_name,
                status

            FROM trainer_workout_schedule

            WHERE member_id = %s

            ORDER BY workout_date ASC

        """, (
            member_id,
        ))


        rows = cursor.fetchall()


        for row in rows:

            if row["workout_date"] is not None:

                row["workout_date"] = row[
                    "workout_date"
                ].strftime(
                    "%Y-%m-%d"
                )


        return jsonify({

            "status": "success",

            "member_id": member_id,

            "workouts": rows

        }), 200


    except Exception as e:

        print(
            "GET MEMBER WORKOUT SCHEDULE ERROR:",
            e
        )


        return jsonify({

            "status": "error",

            "message": str(e)

        }), 500


    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()
 
@app.route(
    "/api/member/trainer-status/<member_id>",
    methods=["GET"]
)
def get_member_trainer_status(member_id):

    conn = None
    cursor = None

    try:

        member_id = str(member_id).strip()

        if not member_id:
            return jsonify({
                "status": "error",
                "message": "Member ID is required."
            }), 400

        conn = get_connection()

        cursor = conn.cursor(
            pymysql.cursors.DictCursor
        )

        cursor.execute("""
            SELECT
                tt.id,

                tt.trainer_id,
                ua.fullname AS trainer_name,

                tt.member_id,

                tt.program_id,
                p.program_name,
                p.description AS program_description,
                p.duration_days AS program_duration_days,

                tt.plan_id,
                tp.plan_name,
                tp.duration_days,
                tp.price,

                tt.start_date,
                tt.end_date,
                tt.status

            FROM trainer_trainees tt

            INNER JOIN user_accounts ua
                ON tt.trainer_id = ua.user_id

            LEFT JOIN programs p
                ON tt.program_id = p.id

            INNER JOIN trainer_plans tp
                ON tt.plan_id = tp.id

            WHERE tt.member_id = %s

            AND tt.status IN ('pending', 'active')

            AND tt.start_date <= CURDATE()
            AND tt.end_date >= CURDATE()

            ORDER BY tt.created_at DESC

            LIMIT 1

        """, (member_id,))

        row = cursor.fetchone()

        if not row:

            return jsonify({
                "has_trainer": False
            }), 200

        if row["start_date"] is not None:

            row["start_date"] = row[
                "start_date"
            ].strftime("%Y-%m-%d")

        if row["end_date"] is not None:

            row["end_date"] = row[
                "end_date"
            ].strftime("%Y-%m-%d")

        if row["price"] is not None:

            row["price"] = float(
                row["price"]
            )

        return jsonify({

            "has_trainer": True,

            "trainer": row

        }), 200

    except Exception as e:

        print(
            "GET MEMBER TRAINER STATUS ERROR:",
            e
        )

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()
     
@app.route("/api/website_walkins", methods=["GET"])
def website_walkins():

    conn = None
    cursor = None

    try:

        conn = get_connection()

        cursor = conn.cursor(
            pymysql.cursors.DictCursor
        )

        cursor.execute("""
            SELECT
                w.id,
                w.full_name,
                w.phone_number,
                w.visit_date,

                COUNT(a.session_id) AS total_visit

            FROM walkins w

            LEFT JOIN attendance_sessions a
                ON a.user_id = w.id

            GROUP BY
                w.id,
                w.full_name,
                w.phone_number,
                w.visit_date

            ORDER BY
                w.visit_date DESC,
                w.id ASC
        """)

        rows = cursor.fetchall()

        data = []

        for row in rows:

            data.append({

                "id": row["id"],

                "name": row["full_name"],

                "phone": row["phone_number"],

                "visit_date": (
                    row["visit_date"].strftime("%Y-%m-%d")
                    if row["visit_date"]
                    else "-"
                ),

                "total_visit":
                    row["total_visit"] or 0
            })

        return jsonify({

            "success": True,

            "data": data

        })

    except Exception as e:

        print(
            "WEBSITE WALKINS API ERROR:",
            e
        )

        return jsonify({

            "success": False,

            "data": [],

            "error": str(e)

        }), 500

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()        



# ----------------ENROLLMENT-------------

@app.route("/api/walkin_created", methods=["POST"])
def walkin_created():

    data = request.get_json()

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            INSERT INTO walkins(
                id,
                full_name,
                fingerprint_template,
                phone_number,
                visit_date,
                fp_id
            )
            VALUES(
                %s,
                %s,
                %s,
                %s,
                CURDATE(),
                %s
            )

            ON DUPLICATE KEY UPDATE

                full_name=VALUES(full_name),
                fingerprint_template=VALUES(fingerprint_template),
                phone_number=VALUES(phone_number),
                fp_id=VALUES(fp_id)

        """, (
            data["walkin_id"],
            data["full_name"],
            data["fp_template"],
            data["phone_number"],
            data["fp_id"]
        ))

        conn.commit()

        return jsonify({
            "success": True,
            "message": "Walkin synchronized."
        })

    except Exception as e:

        conn.rollback()

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

    finally:

        cursor.close()
        conn.close()
        
        
@app.route("/api/walkin_payment_updated", methods=["POST"])
def walkin_payment_updated():

    data = request.get_json()

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            INSERT INTO payments(
                user_id,
                payment_type,
                amount
            )
            VALUES(
                %s,
                %s,
                %s
            )
        """, (
            data["walkin_id"],
            data["payment_type"],
            data["amount"]
        ))

        conn.commit()

        return jsonify({
            "success": True,
            "message": "Walk-in payment synchronized."
        })

    except Exception as e:

        conn.rollback()

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

    finally:

        cursor.close()
        conn.close()
        
@app.route("/api/walkin_deleted", methods=["POST"])
def walkin_deleted():

    data = request.get_json()

    conn = get_connection()
    cursor = conn.cursor()

    try:

        walkin_id = data["walkin_id"]

        # Delete fingerprint template record
        cursor.execute("""
            DELETE FROM fp_templates
            WHERE user_id=%s
        """, (walkin_id,))

        # Delete walk-in
        cursor.execute("""
            DELETE FROM walkins
            WHERE id=%s
        """, (walkin_id,))

        # Delete related payments
        cursor.execute("""
            DELETE FROM payments
            WHERE user_id=%s
        """, (walkin_id,))

        conn.commit()

        return jsonify({
            "success": True,
            "message": "Walk-in deleted."
        })

    except Exception as e:

        conn.rollback()

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

    finally:

        cursor.close()
        conn.close()


@app.route("/api/walkins", methods=["GET"])
def get_walkins():

    try:

        walkins = execute_query(
            """
            SELECT *
            FROM walkins
            """,
            fetch=True
        )

        return jsonify({

            "walkins": walkins

        })

    except Exception as e:

        return jsonify({

            "error": str(e)

        }), 500

@app.route("/api/locker_member_version")
def locker_member_version():

    return jsonify({

        "version": get_sync_version("members")

    })


@app.route("/api/locker_walkin_version")
def locker_walkin_version():

    return jsonify({

        "version": get_sync_version("walkins")

    })


@app.route("/api/locker_fingerprint_version")
def locker_fingerprint_version():

    return jsonify({

        "version": get_sync_version("fingerprints")

    })


@app.route("/api/locker_face_version")
def locker_face_version():

    return jsonify({

        "version": get_sync_version("face")

    })

def get_sync_version(resource):

    row = execute_query(
        """
        SELECT version
        FROM sync_versions
        WHERE resource=%s
        """,
        (resource,),
        fetch=True
    )

    if not row:
        return 0

    return row[0]["version"]

@app.route(
    "/api/sync_account",
    methods=["POST"]
)
def sync_account():

    try:

        data = request.get_json()

        execute_query(
            """
            INSERT INTO user_accounts
            (
                user_id,
                username,
                password,
                role,
                fullname
            )

            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s
            )

            ON DUPLICATE KEY UPDATE

                username = VALUES(username),

                password = VALUES(password),

                role = VALUES(role),

                fullname = VALUES(fullname)
            """,

            (

                data["user_id"],

                data["username"],

                data["password"],

                data["role"],

                data["fullname"]

            )

        )

        return jsonify({

            "success": True

        })

    except Exception as e:

        print(e)

        return jsonify({

            "success": False,

            "error": str(e)

        }),500


@app.route(
    "/api/create-member-account",
    methods=["POST"]
)
def create_member_account():

    data = request.json

    username = data["username"].strip()
    password = data["password"]
    user_id = data["user_id"]
    fullname = data["fullname"]

    # ==========================
    # CHECK DUPLICATE USERNAME
    # ==========================
    existing = execute_query(
        """
        SELECT id
        FROM user_accounts
        WHERE username=%s
        """,
        (username,),
        fetch=True
    )

    if existing:

        return jsonify({

            "success": False,

            "message": "Username already exists."

        })

    # ==========================
    # SAVE TO TURNSTILE DATABASE
    # ==========================
    execute_query(
        """
        INSERT INTO user_accounts
        (
            user_id,
            username,
            password,
            role,
            fullname
        )
        VALUES
        (
            %s,
            %s,
            %s,
            %s,
            %s
        )
        """,
        (
            user_id,
            username,
            password,
            "member",
            fullname
        )
    )

    # ==========================
    # SYNC TO RENDER / RAILWAY
    # ==========================
    try:

        response = requests.post(

            f"{RENDER_API}/api/sync_account",

            json={

                "user_id": user_id,
                "username": username,
                "password": password,
                "role": "member",
                "fullname": fullname

            },

            timeout=15

        )

        print("========== RENDER ==========")
        print("STATUS :", response.status_code)
        print("TEXT   :", response.text)
        print("============================")

    except Exception as e:

        print("[RENDER ERROR]", str(e))

    # ==========================
    # SUCCESS
    # ==========================
    return jsonify({

        "success": True,

        "message": "Member account created successfully."

    })

@app.route(
    "/api/members/without-account",
    methods=["GET"]
)
def members_without_account():

    query = """
        SELECT
            m.id,
            m.full_name,
            m.phone_number
        FROM members m
        LEFT JOIN user_accounts ua
            ON ua.user_id = m.id
        WHERE ua.user_id IS NULL
        ORDER BY m.full_name
    """

    members = execute_query(
        query,
        fetch=True
    )

    return jsonify({
        "success": True,
        "data": members
    })

@app.route("/api/locker_overtime/<user_id>", methods=["GET"])
def api_get_locker_overtime(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute("""
            SELECT

                ls.user_id,

                COALESCE(
                    m.full_name,
                    w.full_name
                ) AS full_name,

                ls.locker_number,

                ls.start_time,

                ls.overtime_paid,

                ls.status,

                GREATEST(

                    TIMESTAMPDIFF(

                        MINUTE,

                        DATE_ADD(ls.start_time, INTERVAL 3 HOUR),

                        NOW()

                    ),

                    0

                ) AS overtime_minutes

            FROM locker_sessions ls

            LEFT JOIN members m
                ON ls.user_id = m.id

            LEFT JOIN walkins w
                ON ls.user_id = w.id

            WHERE

                ls.user_id=%s

                AND ls.status='active'

                AND ls.overtime_paid=0

            LIMIT 1

        """, (user_id,))

        row = cursor.fetchone()

        if not row:

            return jsonify({

                "success": False

            })

        import math

        overtime_fee = math.ceil(row[6] / 2)   # PHP 1 per minute

        locker = {

            "user_id": row[0],

            "full_name": row[1],

            "locker_number": row[2],

            "start_time": str(row[3]),

            "overtime_paid": row[4],

            "status": row[5],

            "overtime_minutes": row[6],

            "overtime_fee": overtime_fee

        }

        return jsonify({

            "success": True,

            "locker": locker

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)

        })

    finally:

        cursor.close()
        connection.close()

@app.route("/api/payment_updated", methods=["POST"])
def payment_updated():

    data = request.get_json()

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""

            UPDATE members

            SET

                membership_type=%s,
                membership_expires=%s,
                monthly_expires=%s

            WHERE id=%s

        """, (

            data["membership_type"],
            data["membership_expires"],
            data["monthly_expires"],
            data["member_id"]

        ))

        conn.commit()

        return jsonify({

            "success": True,
            "message": "Payment synchronized."

        })

    except Exception as e:

        conn.rollback()

        return jsonify({

            "success": False,
            "error": str(e)

        }), 500

    finally:

        cursor.close()
        conn.close()
        
@app.route("/api/member_created", methods=["POST"])
def member_created():

    data = request.get_json()

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            INSERT INTO members(

                id,
                full_name,
                fingerprint_template,
                phone_number,
                membership_type,
                membership_expires,
                monthly_expires

            )

            VALUES(

                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s

            )

            ON DUPLICATE KEY UPDATE

                full_name=VALUES(full_name),
                fingerprint_template=VALUES(fingerprint_template),
                phone_number=VALUES(phone_number),
                membership_type=VALUES(membership_type),
                membership_expires=VALUES(membership_expires),
                monthly_expires=VALUES(monthly_expires)

        """, (

            data["member_id"],
            data["full_name"],
            data["fp_template"],
            data["phone_number"],
            data.get("membership_type"),
            data.get("membership_expires"),
            data.get("monthly_expires")

        ))

        conn.commit()

        return jsonify({

            "success": True,
            "message": "Member synchronized."

        })

    except Exception as e:

        conn.rollback()

        return jsonify({

            "success": False,
            "error": str(e)

        }), 500

    finally:

        cursor.close()
        conn.close()

#--------NEW------
@app.route("/api/delete_member", methods=["POST"])
def delete_member():

    print("DELETE MEMBER API CALLED")

    data = request.get_json()
    print(data)

    member_id = data["member_id"]

    conn = get_connection()
    cursor = conn.cursor()

    try:

        print("Deleting user_account...")

        cursor.execute("""
            DELETE FROM user_accounts
            WHERE user_id=%s
        """, (member_id,))

        print("Rows:", cursor.rowcount)

        print("Deleting member...")

        cursor.execute("""
            DELETE FROM members
            WHERE id=%s
        """, (member_id,))

        print("Rows:", cursor.rowcount)

        conn.commit()

        print("COMMIT DONE")

        return jsonify({
            "success": True,
            "message": "Member deleted."
        })

    except Exception as e:

        print("ERROR:", e)

        conn.rollback()

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

    finally:

        cursor.close()
        conn.close()
#from sync.sync_sender import send_event
@app.route("/api/register", methods=["POST"])
def register():

    conn = None

    try:

        data = request.get_json()

        fullname = data.get("fullname")
        phone_number = data.get("phone_number")
        username = data.get("username")
        password = data.get("password")

        # ===========================
        # BASIC VALIDATION
        # ===========================
        if not all([
            fullname,
            phone_number,
            username,
            password
        ]):

            return jsonify({
                "status": "error",
                "message": "Please complete all fields."
            })

        conn = get_connection()
        cursor = conn.cursor()

        # ===========================
        # CHECK DUPLICATE USERNAME
        # ===========================
        cursor.execute(
            """
            SELECT id
            FROM user_accounts
            WHERE username=%s
            """,
            (username,)
        )

        if cursor.fetchone():

            return jsonify({
                "status": "error",
                "message": "Username already exists."
            })

        # ===========================
        # INSERT ACCOUNT
        # ===========================
        cursor.execute(
            """
            INSERT INTO user_accounts(

                user_id,
                fullname,
                username,
                password,
                role

            )

            VALUES(

                NULL,
                %s,
                %s,
                %s,
                'pre_member'

            )
            """,
            (
                fullname,
                username,
                password
            )
        )

        account_id = cursor.lastrowid

        # ===========================
        # INSERT PENDING MEMBER
        # ===========================
        cursor.execute(
            """
            INSERT INTO pending_members(

                account_id,
                full_name,
                phone_number

            )

            VALUES(%s,%s,%s)
            """,
            (
                account_id,
                fullname,
                phone_number
            )
        )

        conn.commit()
#         send_event(

#             "PENDING_MEMBER_CREATED",

#             {

#                 "account_id": account_id,

#                 "full_name": fullname,

#                 "phone_number": phone_number

#             }

#         )

        return jsonify({

            "status": "success",

            "message": "Registration submitted."

        })

    except Exception as e:

        if conn:
            conn.rollback()

        return jsonify({

            "status": "error",

            "message": str(e)

        })

    finally:

        if conn:
            conn.close()
            

@app.route("/api/pending_members", methods=["GET"])
def pending_members():

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            SELECT
                account_id,
                full_name,
                phone_number,
                created_at
            FROM pending_members
            WHERE status='PENDING'
            ORDER BY created_at ASC
        """)

        rows = cursor.fetchall()

        data = []

        for row in rows:

            data.append({

                "account_id": row[0],
                "full_name": row[1],
                "phone_number": row[2],
                "created_at": row[3]

            })

        return jsonify({

            "status": "success",
            "data": data

        })

    except Exception as e:

        return jsonify({

            "status": "error",
            "message": str(e)

        }), 500

    finally:

        cursor.close()
        conn.close()
        
# =========================================================
# GET TRAINER WORKOUT SCHEDULES
# =========================================================

@app.route(
    "/api/trainer/workouts/<trainer_id>",
    methods=["GET"]
)
def get_trainer_workouts(trainer_id):

    conn = None
    cursor = None

    try:

        trainer_id = str(
            trainer_id
        ).strip()


        # =========================
        # VALIDATION
        # =========================

        if not trainer_id:

            return jsonify({
                "status": "error",
                "message": "Trainer ID is required."
            }), 400


        # =========================
        # DATABASE
        # =========================

        conn = get_connection()

        cursor = conn.cursor(
            pymysql.cursors.DictCursor
        )


        cursor.execute("""
            SELECT

                tws.id,

                tws.member_id,

                m.full_name AS member_name,

                tws.trainer_id,

                tws.workout_date,

                tws.workout_name,

                tws.status

            FROM trainer_workout_schedule tws

            INNER JOIN members m
                ON tws.member_id = m.id

            WHERE tws.trainer_id = %s

            ORDER BY
                tws.workout_date ASC,
                tws.id ASC

        """, (
            trainer_id,
        ))


        rows = cursor.fetchall()


        # =========================
        # FORMAT DATE
        # =========================

        for row in rows:

            if row["workout_date"] is not None:

                row["workout_date"] = row[
                    "workout_date"
                ].strftime(
                    "%Y-%m-%d"
                )


        # =========================
        # RESPONSE
        # =========================

        return jsonify({

            "status": "success",

            "trainer_id": trainer_id,

            "workouts": rows

        }), 200


    except Exception as e:

        print(
            "GET TRAINER WORKOUTS ERROR:",
            e
        )


        return jsonify({

            "status": "error",

            "message": str(e)

        }), 500


    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()
# =========================================================
# MARK TRAINER WORKOUT AS COMPLETED
# =========================================================

@app.route(
    "/api/trainer/workout/<int:workout_id>/complete",
    methods=["POST"]
)
def complete_trainer_workout(workout_id):

    conn = None
    cursor = None

    try:

        # =========================
        # DATABASE
        # =========================

        conn = get_connection()

        cursor = conn.cursor(
            pymysql.cursors.DictCursor
        )


        # =========================
        # CHECK WORKOUT
        # =========================

        cursor.execute("""
            SELECT
                id,
                member_id,
                trainer_id,
                workout_date,
                workout_name,
                status

            FROM trainer_workout_schedule

            WHERE id = %s

        """, (
            workout_id,
        ))


        workout = cursor.fetchone()


        if not workout:

            return jsonify({
                "status": "error",
                "message": "Workout not found."
            }), 404


        # =========================
        # UPDATE STATUS
        # =========================

        cursor.execute("""
            UPDATE trainer_workout_schedule

            SET status = 'completed'

            WHERE id = %s

        """, (
            workout_id,
        ))


        conn.commit()


        # =========================
        # RESPONSE
        # =========================

        return jsonify({

            "status": "success",

            "message": "Workout marked as completed.",

            "workout": {
                "id": workout["id"],
                "member_id": workout["member_id"],
                "trainer_id": workout["trainer_id"],
                "workout_date":
                    workout["workout_date"].strftime("%Y-%m-%d")
                    if workout["workout_date"]
                    else None,
                "workout_name": workout["workout_name"],
                "status": "completed"
            }

        }), 200


    except Exception as e:

        if conn:
            conn.rollback()

        print(
            "COMPLETE TRAINER WORKOUT ERROR:",
            e
        )

        return jsonify({

            "status": "error",

            "message": str(e)

        }), 500


    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()

# =========================================================
# MARK TRAINER WORKOUT AS MISSED
# =========================================================

@app.route(
    "/api/trainer/workout/<int:workout_id>/missed",
    methods=["POST"]
)
def missed_trainer_workout(workout_id):

    conn = None
    cursor = None

    try:

        # =========================
        # DATABASE
        # =========================

        conn = get_connection()

        cursor = conn.cursor(
            pymysql.cursors.DictCursor
        )


        # =========================
        # CHECK WORKOUT
        # =========================

        cursor.execute("""
            SELECT
                id,
                member_id,
                trainer_id,
                workout_date,
                workout_name,
                status

            FROM trainer_workout_schedule

            WHERE id = %s

        """, (
            workout_id,
        ))


        workout = cursor.fetchone()


        if not workout:

            return jsonify({
                "status": "error",
                "message": "Workout not found."
            }), 404


        # =========================
        # UPDATE STATUS
        # =========================

        cursor.execute("""
            UPDATE trainer_workout_schedule

            SET status = 'missed'

            WHERE id = %s

        """, (
            workout_id,
        ))


        conn.commit()


        # =========================
        # RESPONSE
        # =========================

        return jsonify({

            "status": "success",

            "message": "Workout marked as missed.",

            "workout": {

                "id": workout["id"],

                "member_id":
                    workout["member_id"],

                "trainer_id":
                    workout["trainer_id"],

                "workout_date":
                    workout["workout_date"].strftime("%Y-%m-%d")
                    if workout["workout_date"]
                    else None,

                "workout_name":
                    workout["workout_name"],

                "status": "missed"

            }

        }), 200


    except Exception as e:

        if conn:
            conn.rollback()


        print(
            "MISSED TRAINER WORKOUT ERROR:",
            e
        )


        return jsonify({

            "status": "error",

            "message": str(e)

        }), 500


    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()

# =========================================================
# RESCHEDULE MISSED WORKOUT TO NEXT DAY
# =========================================================

@app.route(
    "/api/trainer/workout/<int:workout_id>/reschedule",
    methods=["POST"]
)
def reschedule_trainer_workout(workout_id):

    conn = None
    cursor = None

    try:

        # =========================
        # DATABASE
        # =========================

        conn = get_connection()

        cursor = conn.cursor(
            pymysql.cursors.DictCursor
        )


        # =========================
        # GET WORKOUT
        # =========================

        cursor.execute("""
            SELECT
                id,
                member_id,
                trainer_id,
                workout_date,
                workout_name,
                status

            FROM trainer_workout_schedule

            WHERE id = %s

        """, (
            workout_id,
        ))


        workout = cursor.fetchone()


        if not workout:

            return jsonify({
                "status": "error",
                "message": "Workout not found."
            }), 404


        # =========================
        # ONLY MISSED WORKOUT
        # =========================

        if workout["status"] != "missed":

            return jsonify({
                "status": "error",
                "message":
                    "Only missed workouts can be rescheduled."
            }), 400


        # =========================
        # CALCULATE NEXT DAY
        # =========================

        current_date = workout["workout_date"]


        if isinstance(current_date, str):

            current_date = datetime.strptime(
                current_date,
                "%Y-%m-%d"
            ).date()


        next_date = current_date + timedelta(
            days=1
        )


        # =========================
        # CHECK EXISTING WORKOUT
        # =========================

        cursor.execute("""
            SELECT
                id

            FROM trainer_workout_schedule

            WHERE member_id = %s
            AND workout_date = %s

            LIMIT 1

        """, (
            workout["member_id"],
            next_date
        ))


        existing = cursor.fetchone()


        if existing:

            return jsonify({

                "status": "error",

                "message":
                    "Member already has a workout scheduled for the next day."

            }), 409


        # =========================
        # UPDATE WORKOUT
        # =========================

        cursor.execute("""
            UPDATE trainer_workout_schedule

            SET
                workout_date = %s,
                status = 'scheduled'

            WHERE id = %s

        """, (
            next_date,
            workout_id
        ))


        conn.commit()


        # =========================
        # RESPONSE
        # =========================

        return jsonify({

            "status": "success",

            "message":
                "Workout rescheduled to the next day.",

            "workout": {

                "id":
                    workout["id"],

                "member_id":
                    workout["member_id"],

                "trainer_id":
                    workout["trainer_id"],

                "workout_date":
                    str(next_date),

                "workout_name":
                    workout["workout_name"],

                "status":
                    "scheduled"

            }

        }), 200


    except Exception as e:

        if conn:
            conn.rollback()


        print(
            "RESCHEDULE TRAINER WORKOUT ERROR:",
            e
        )


        return jsonify({

            "status": "error",

            "message": str(e)

        }), 500


    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()

@app.route("/api/user_accounts", methods=["GET"])
def get_user_accounts():

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            SELECT
                id,
                user_id,
                fullname,
                username,
                password,
                role,
                created_at
            FROM user_accounts
            ORDER BY id ASC
        """)

        rows = cursor.fetchall()

        data = []

        for row in rows:

            data.append({

                "id": row[0],
                "user_id": row[1],
                "fullname": row[2],
                "username": row[3],
                "password": row[4],
                "role": row[5],
                "created_at": row[6]

            })

        return jsonify({
            "status": "success",
            "data": data
        })

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

    finally:

        cursor.close()
        conn.close()
        
@app.route("/api/pre_member/profile", methods=["PUT"])
def update_pre_member_profile():

    try:

        data = request.get_json()

        account_id = data["id"]
        fullname = data["fullname"]
        username = data["username"]
        phone = data["phone_number"]

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""

            UPDATE user_accounts

            SET

                fullname=%s,

                username=%s

            WHERE id=%s

        """,(

            fullname,

            username,

            account_id

        ))
        
        cursor.execute("""

            UPDATE pending_members

            SET

                full_name=%s,
                phone_number=%s

            WHERE account_id=%s

        """,(

            fullname,
            phone,
            account_id

        ))

        conn.commit()

        return jsonify({

            "status":"success",

            "message":"Profile updated."

        })

    except Exception as e:

        return jsonify({

            "status":"error",

            "message":str(e)

        })

    finally:

        cursor.close()
        conn.close()
@app.route("/api/check_account/<int:account_id>")
def check_account(account_id):

    conn = get_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    try:

        cursor.execute("""
            SELECT
                ua.id,
                ua.user_id,
                ua.fullname,
                ua.username,
                ua.role,
                pm.phone_number

            FROM user_accounts ua

            LEFT JOIN pending_members pm
                ON ua.id = pm.account_id

            WHERE ua.id=%s
        """, (account_id,))

        user = cursor.fetchone()

        if not user:

            return jsonify({
                "status": "error"
            }), 404

        return jsonify({

            "status": "success",

            "role": user["role"],

            "user": {

                "id": user["id"],

                "user_id": user["user_id"],

                "name": user["fullname"],

                "username": user["username"],

                "phone_number": user["phone_number"],

                "role": user["role"]

            }

        })

    except Exception as e:

        print("CHECK ACCOUNT ERROR:", e)

        return jsonify({

            "status": "error",

            "message": str(e)

        }), 500

    finally:

        cursor.close()
        conn.close()       

@app.route("/api/local/pending_members", methods=["GET"])
def local_pending_members():

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""

            SELECT

                account_id,
                full_name,
                phone_number,
                status

            FROM pending_members

            WHERE status='PENDING'

            ORDER BY full_name ASC

        """)

        rows = cursor.fetchall()

        return jsonify({

            "status": "success",
            "data": rows

        })

    except Exception as e:

        return jsonify({

            "status": "error",
            "message": str(e)

        }), 500

    finally:

        cursor.close()
        conn.close()
        
@app.route("/api/local/pending_completed", methods=["POST"])
def pending_completed():

    data = request.get_json()

    account_id = data["account_id"]

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        UPDATE pending_members

        SET status='COMPLETED'

        WHERE account_id=%s

    """, (account_id,))

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        "success": True
    })

@app.route("/api/local/activate_member", methods=["POST"])
def activate_member():

    data = request.get_json()

    account_id = data["account_id"]
    member_id = data["member_id"]

    print("\n========== ACTIVATE MEMBER ==========")
    print("ACCOUNT_ID:", account_id)
    print("MEMBER_ID :", member_id)

    conn = get_connection()
    cursor = conn.cursor()

    # Database information
    cursor.execute("""
        SELECT
            @@hostname,
            @@port,
            DATABASE(),
            @@socket
    """)
    print("CONNECTED TO:", cursor.fetchone())

    # Before update
    cursor.execute("""
        SELECT
            id,
            user_id,
            role
        FROM user_accounts
        WHERE id=%s
    """, (account_id,))
    print("BEFORE UPDATE:", cursor.fetchone())

    # Update
    cursor.execute("""
        UPDATE user_accounts
        SET
            user_id=%s,
            role='member'
        WHERE id=%s
    """, (member_id, account_id))

    print("ROWS UPDATED:", cursor.rowcount)

    conn.commit()

    # After update
    cursor.execute("""
        SELECT
            id,
            user_id,
            role
        FROM user_accounts
        WHERE id=%s
    """, (account_id,))
    print("AFTER UPDATE:", cursor.fetchone())

    cursor.close()
    conn.close()

    return jsonify({
        "success": True
    })
@app.route("/api/activate_member", methods=["POST"])
def activate_member_cloud():
    data = request.get_json()

    account_id = data["account_id"]
    member_id = data["member_id"]

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            UPDATE user_accounts
            SET
                user_id=%s,
                role='member'
            WHERE id=%s
        """, (member_id, account_id))

        conn.commit()

        return jsonify({
            "success": True,
            "message": "Account activated."
        })

    except Exception as e:

        conn.rollback()

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

    finally:

        cursor.close()
        conn.close()
        
@app.route("/api/pending_completed", methods=["POST"])
def pending_completed_cloud():

    data = request.get_json()

    account_id = data["account_id"]

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""

            UPDATE pending_members

            SET status='COMPLETED'

            WHERE account_id=%s

        """,(account_id,))

        conn.commit()

        return jsonify({
            "success": True
        })

    except Exception as e:

        conn.rollback()

        return jsonify({
            "success": False,
            "error": str(e)
        }),500

    finally:

        cursor.close()
        conn.close()
#--------OLD-----------
        
from config.settings import DB_CONFIG
import pymysql

def get_connection():
    return pymysql.connect(**DB_CONFIG)

@app.route("/test-db")
def test_db():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM attendance_sessions")
        result = cursor.fetchone()
        return {"count": result[0]}
    except Exception as e:
        return {"error": str(e)}

@app.route("/")
def home():
    return "Smart Gym System API is running"

def require_api_key(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.headers.get('X-API-KEY') == API_KEY:
            return f(*args, **kwargs)
        return jsonify({"error": "Unauthorized Access"}), 401
    return decorated

# --- MILESTONE 1: TEST ENDPOINT ---
@app.route('/api/ping', methods=['GET'])
def ping():
    return jsonify({"status": "online", "message": "Gym Master Server is Active"}), 200

# --- MILESTONE 2: LOCKER & MEMBER ENDPOINTS ---

@app.route('/api/verify_member', methods=['POST'])
@require_api_key
def verify_member():
    data = request.json
    user_id = data.get('user_id')
    # Check kung active ang session sa Turnstile (Phase 1 Milestone 5)
    query = "SELECT id FROM attendance_sessions WHERE user_id = %s AND time_out IS NULL"
    session = execute_query(query, (user_id,), fetch=True)
    if session:
        return jsonify({"allowed": True, "user_id": user_id}), 200
    return jsonify({"allowed": False, "reason": "NOT_IN_GYM"}), 403


@app.route('/api/get_templates', methods=['GET'])
@require_api_key
def get_templates():
    try:
        query = "SELECT user_id, template FROM fp_templates"
        rows = execute_query(query, fetch=True)
        
        results = []
        for row in rows:
            template_val = row['template']
            # Kung ang template ay bytes, i-convert sa string
            if isinstance(template_val, bytes):
                template_val = base64.b64encode(template_val).decode('utf-8')
            
            results.append({
                "user_id": row['user_id'],
                "template": template_val
            })
            
        return jsonify(results), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

from flask import send_file, jsonify
import os

@app.route('/api/get_face_model', methods=['GET'])
def get_face_model():
    try:
        model_path = os.path.join(os.getcwd(), "biometrics/face/lbph_model.yml")

        print("[DEBUG] FACE MODEL PATH:", model_path)

        # check if file exists
        if not os.path.exists(model_path):
            return jsonify({"error": "Face model not found"}), 404

        # send file (BINARY)
        return send_file(
            model_path,
            mimetype='application/octet-stream',
            as_attachment=False
        )

    except Exception as e:
        print("[ERROR FACE MODEL]", e)
        return jsonify({"error": str(e)}), 500
    
from flask import send_file, request
import os

API_KEY = "GYM_MASTER_2026"

def check_api_key(req):
    return req.headers.get("X-API-KEY") == API_KEY

@app.route('/api/get_face_labels', methods=['GET'])
def get_face_labels():
    try:
        labels_path = "/home/thesis_group6/smart_gym_turnstile/biometrics/face/labels.json"

        print("\n[DEBUG] USING PATH:", labels_path)

        if not os.path.exists(labels_path):
            print("[ERROR] FILE NOT FOUND")
            return jsonify({})

        with open(labels_path, "r") as f:
            data = json.load(f)

        print("[DEBUG] LABELS:", data)

        return jsonify(data)

    except Exception as e:
        print("[ERROR LABELS]", e)
        return jsonify({})
    
@app.route("/api/face_version")
def face_version():
    try:
        model_path = "/home/thesis_group6/smart_gym_turnstile/biometrics/face/lbph_model.yml"
        labels_path = "/home/thesis_group6/smart_gym_turnstile/biometrics/face/labels.json"

        model_time = os.path.getmtime(model_path) if os.path.exists(model_path) else 0
        labels_time = os.path.getmtime(labels_path) if os.path.exists(labels_path) else 0

        version = int(max(model_time, labels_time))

        return jsonify({
            "version": version
        })

    except Exception as e:
        return jsonify({
            "version": 0,
            "error": str(e)
        }), 500
    
from flask import send_file, jsonify
import os
import zipfile
import tempfile

@app.route("/api/get_face_images")
def get_face_images():
    try:
        FACE_DATASET_DIR = "/home/thesis_group6/smart_gym_turnstile/datasets/faces"

        if not os.path.exists(FACE_DATASET_DIR):
            return jsonify({"success": False, "message": "Face dataset not found"}), 404

        temp_zip = tempfile.NamedTemporaryFile(delete=False, suffix=".zip")
        temp_zip.close()

        with zipfile.ZipFile(temp_zip.name, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(FACE_DATASET_DIR):
                for file in files:
                    if file.lower().endswith((".jpg", ".jpeg", ".png")):
                        full_path = os.path.join(root, file)
                        rel_path = os.path.relpath(full_path, FACE_DATASET_DIR)
                        zipf.write(full_path, rel_path)

        return send_file(
            temp_zip.name,
            as_attachment=True,
            download_name="face_images.zip",
            mimetype="application/zip"
        )

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/start_locker', methods=['POST'])
def start_locker():
    try:
        data = request.get_json(force=True)

        user_id = data.get('user_id')
        locker_id = data.get('locker_id')

        if not user_id or not locker_id:
            return jsonify({
                "status": "error",
                "message": "Missing user_id or locker_id"
            }), 400

        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        # ================= CHECK ACTIVE SESSION =================
        cursor.execute("""
            SELECT * FROM locker_sessions
            WHERE user_id = %s AND status = 'active'
            LIMIT 1
        """, (user_id,))

        existing = cursor.fetchone()

        if existing:
            print(f"⚠️ {user_id} already has active session")

            return jsonify({
                "status": "exists",
                "locker": existing["locker_number"]
            }), 200

        # ================= CHECK LOCKER AVAILABILITY =================
        cursor.execute("""
            SELECT status FROM lockers
            WHERE locker_number = %s
        """, (locker_id,))

        locker = cursor.fetchone()

        if not locker:
            return jsonify({
                "status": "error",
                "message": "Locker not found"
            }), 404

        if locker["status"] == "OCCUPIED":
            print(f"❌ Locker {locker_id} already occupied")

            return jsonify({
                "status": "error",
                "message": "Locker already occupied"
            }), 400

        # ================= INSERT SESSION =================
        cursor.execute("""
            INSERT INTO locker_sessions 
            (user_id, locker_number, start_time, end_time, overtime_paid, status)
            VALUES (%s, %s, NOW(), NULL, 0, 'active')
        """, (user_id, locker_id))

        # ================= UPDATE LOCKER =================
        cursor.execute("""
            UPDATE lockers
            SET status = 'OCCUPIED'
            WHERE locker_number = %s
        """, (locker_id,))

        conn.commit()

        print(f"✅ START: {user_id} → Locker {locker_id}")

        cursor.close()
        conn.close()

        return jsonify({
            "status": "success",
            "locker": locker_id
        }), 201

    except Exception as e:
        print("🔥 START LOCKER ERROR:", e)

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
    
    
@app.route('/api/check_locker', methods=['GET'])
@require_api_key
def check_locker():
    try:
        user_id = request.args.get("user_id")

        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT * FROM locker_sessions
        WHERE user_id = %s AND status = 'active'
        LIMIT 1
        """

        cursor.execute(query, (user_id,))
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        if result:
            return jsonify({"active": True})
        else:
            return jsonify({"active": False})

    except Exception as e:
        print("[CHECK LOCKER ERROR]", e)
        return jsonify({"error": str(e)}), 500

@app.route("/api/locker_status", methods=["GET"])
def locker_status():

    if not require_api_key(request):
        return jsonify({"error": "Unauthorized"}), 401

    sessions = execute_query("""
        SELECT user_id, locker_number, start_time, overtime_paid
        FROM locker_sessions
        WHERE status = 'active'
    """, fetch=True)

    return jsonify({
        "success": True,
        "active_lockers": sessions
    })

@app.route("/api/end_locker", methods=["POST"])
def end_locker():
    try:
        if not require_api_key(request):
            return jsonify({"error": "Unauthorized"}), 401

        data = request.get_json()
        user_id = data.get("user_id")

        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # 🔥 GET ACTIVE LOCKER
        cursor.execute("""
            SELECT locker_number FROM locker_sessions
            WHERE user_id=%s AND status='active'
        """, (user_id,))

        result = cursor.fetchone()

        if not result:
            return jsonify({
                "success": False,
                "message": "No active session"
            }), 200

        locker_number = result[0]

        # 🔥 END SESSION
        cursor.execute("""
            UPDATE locker_sessions
            SET end_time = NOW(),
                status = 'ended'
            WHERE user_id = %s AND status = 'active'
        """, (user_id,))

        # 🔥 🔥 CRITICAL FIX (ETO KULANG MO)
        cursor.execute("""
            UPDATE lockers
            SET status = 'AVAILABLE'
            WHERE locker_number = %s
        """, (locker_number,))

        conn.commit()

        print(f"✅ RELEASED LOCKER {locker_number}")

        return jsonify({
            "success": True,
            "locker_released": locker_number
        }), 200

    except Exception as e:
        print("🔥 ERROR END:", e)
        return jsonify({"error": str(e)}), 500


@app.route('/api/overtime', methods=['POST'])
@require_api_key
def overtime():

    data = request.json
    locker_id = data.get("locker_id")

    execute_query("""
        UPDATE locker_sessions
        SET status = 'overtime'
        WHERE locker_number = %s
        AND status = 'active'
    """, (locker_id,))

    execute_query("""
        UPDATE lockers
        SET status = 'OVERTIME'
        WHERE locker_number = %s
    """, (locker_id,))

    socketio.emit("locker_update")

    print("⚠️ LOCAL OVERTIME:", locker_id)

    return jsonify({"success": True})

@app.route('/api/get_active_sessions', methods=['GET'])
def get_active_sessions():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        # Siguraduhin na 'user_id' at 'locker_number' ang columns
        query = "SELECT user_id, locker_number FROM locker_sessions WHERE end_time IS NULL"
        
        cursor.execute(query)
        rows = cursor.fetchall()
        
        conn.close()
        return jsonify({"sessions": rows}), 200

    except Exception as e:
        print(f"❌ DATABASE ERROR: {e}")
        return jsonify({"error": str(e)}), 500
    
@app.route("/api/members", methods=["GET"])
def get_members():
    try:
        members = execute_query("SELECT * FROM members", fetch=True)
        walkins = execute_query("SELECT * FROM walkins", fetch=True)
        fps = execute_query("SELECT * FROM fp_templates", fetch=True)

        # 🔥 MAP user_id → fp_id
        fp_map = {f["user_id"]: f["fp_id"] for f in fps}

        all_users = []

        # MEMBERS
        for m in members:
            all_users.append({
                "id": m["id"],
                "name": m["full_name"],
                "type": "member",
                "fp_id": fp_map.get(m["id"])
            })

        # WALKINS
        for w in walkins:
            all_users.append({
                "id": w["id"],
                "name": w["full_name"],
                "type": "walkin",
                "fp_id": fp_map.get(w["id"])
            })

        return jsonify(all_users)

    except Exception as e:
        return {"error": str(e)}, 500
    
@app.route('/api/get_locker/<user_id>', methods=['GET'])
def get_locker(user_id):

    result = execute_query("""
        SELECT locker_number
        FROM locker_sessions
        WHERE user_id=%s
        AND status IN ('reserved','active','overtime')
        AND end_time IS NULL
        LIMIT 1
    """, (user_id,), fetch=True)

    if result:
        locker_no = result[0]["locker_number"]

        # 🔥 IMPORTANT FIX
        execute_query("""
            UPDATE lockers
            SET status = 'RESERVED'
            WHERE locker_number = %s
        """, (locker_no,))

        return jsonify({
            "success": True,
            "locker_number": locker_no
        })

    return jsonify({
        "success": False
    })

@app.route("/api/verify_fingerprint", methods=["POST"])
def verify_fingerprint():

    data = request.json
    template = data.get("template")

    if not template:
        return jsonify({"success": False})

    rows = execute_query(
        "SELECT user_id, template FROM fp_templates",
        fetch=True
    )

    for r in rows:

        if r["template"] == template:

            return jsonify({
                "success": True,
                "user_id": r["user_id"]
            })

    return jsonify({
        "success": False
    })

@app.route("/api/get_fp_templates", methods=["GET"])
def get_fp_templates():
    try:
        data = execute_query(
            "SELECT fp_id, template FROM fp_templates",
            fetch=True
        )

        result = []

        for row in data:

            template = row["template"]

            # 🔥 FIX: DO NOT .hex() AGAIN
            if isinstance(template, bytes):
                template = template.decode()  # or .hex() only if raw bytes

            result.append({
                "fp_id": row["fp_id"],
                "template": template
            })

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

import mysql.connector


@app.route('/api/get_available_locker', methods=['GET'])
def get_available_locker():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT locker_number
            FROM lockers
            WHERE locker_number NOT IN (
                SELECT locker_number
                FROM locker_sessions
                WHERE status = 'active'
            )
            ORDER BY locker_number ASC
            LIMIT 1
        """)

        row = cursor.fetchone()

        if row:
            return jsonify({
                "success": True,
                "locker_number": row[0]
            })

        return jsonify({"success": False})

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })
    
def sync_lockers():
    execute_query("""
        UPDATE lockers l
        LEFT JOIN locker_sessions s 
        ON l.locker_number = s.locker_number 
        AND s.status = 'active'
        SET l.status = 
            CASE 
                WHEN s.locker_number IS NULL THEN 'AVAILABLE'
                ELSE 'OCCUPIED'
            END
    """)
    
@app.route('/api/get_active_locker', methods=['GET'])
def get_active_locker():
    user_id = request.args.get("user_id")

    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT locker_number 
        FROM locker_sessions
        WHERE user_id=%s 
        AND status IN ('active', 'overtime')
        ORDER BY start_time DESC
        LIMIT 1
    """, (user_id,))

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result:
        return jsonify({
            "locker_number": result["locker_number"]
        }), 200

    return jsonify({
        "locker_number": None
    }), 200

@app.route("/api/check_overtime/<user_id>", methods=["GET"])
def check_overtime(user_id):

    result = execute_query("""
        SELECT status, overtime_paid
        FROM locker_sessions
        WHERE user_id = %s
        ORDER BY start_time DESC
        LIMIT 1
    """, (user_id,), fetch_one=True)

    if not result:
        return jsonify({"overtime": False})

    status, paid = result

    if status == "overtime" and paid == 0:
        return jsonify({"overtime": True})

    return jsonify({"overtime": False})

from flask import Flask, jsonify
from flask_cors import CORS
import pymysql


# ===== DB CONFIG =====


# ===== DB CONNECTION FUNCTION =====
def get_connection():
    return pymysql.connect(**DB_CONFIG)


# ==============================
# 📊 ATTENDANCE API (FIXED 🔥)
# ==============================
# ==============================
# 📊 ATTENDANCE API
# ==============================
from flask import request, jsonify
from datetime import datetime
import pymysql


@app.route("/api/attendance", methods=["GET"])
def get_attendance():

    conn = None

    try:

        conn = get_connection()

        cursor = conn.cursor(
            pymysql.cursors.DictCursor
        )

        # ==============================
        # GET DATE
        # ==============================

        date = request.args.get("date")

        if not date:
            date = datetime.now().strftime("%Y-%m-%d")


        # ==============================
        # ATTENDANCE QUERY
        # ==============================

        cursor.execute("""
            SELECT

                COALESCE(
                    m.full_name,
                    w.full_name
                ) AS name,

                CASE
                    WHEN m.id IS NOT NULL
                        THEN 'Member'

                    WHEN w.id IS NOT NULL
                        THEN 'Walk-in'

                    ELSE '-'
                END AS type,

                a.user_id,
                a.time_in,
                a.time_out,
                a.status

            FROM attendance_sessions a

            LEFT JOIN members m
                ON CONVERT(a.user_id USING utf8mb4)
                COLLATE utf8mb4_general_ci
                =
                CONVERT(m.id USING utf8mb4)
                COLLATE utf8mb4_general_ci

            LEFT JOIN walkins w
                ON CONVERT(a.user_id USING utf8mb4)
                COLLATE utf8mb4_general_ci
                =
                CONVERT(w.id USING utf8mb4)
                COLLATE utf8mb4_general_ci

            WHERE DATE(a.time_in) = %s

            ORDER BY a.time_in DESC

        """, (date,))


        rows = cursor.fetchall()


        # ==============================
        # FORMAT DATA
        # ==============================

        data = []

        for row in rows:

            # TIME IN
            if row["time_in"]:

                time_in = row["time_in"].strftime(
                    "%I:%M %p"
                )

            else:

                time_in = "-"


            # TIME OUT
            if row["time_out"]:

                time_out = row["time_out"].strftime(
                    "%I:%M %p"
                )

            else:

                time_out = "-"


            # REMARKS
            if row["time_out"]:

                remarks = "Completed"

            else:

                remarks = "Active"


            data.append({

                "name":
                    row["name"]
                    if row["name"]
                    else row["user_id"],

                "type":
                    row["type"],

                "time_in":
                    time_in,

                "time_out":
                    time_out,

                "locker":
                    "-",

                "remarks":
                    remarks

            })


        # ==============================
        # RESPONSE
        # ==============================

        return jsonify({
            "data": data
        })


    except Exception as e:

        print(
            "❌ ATTENDANCE API ERROR:",
            e
        )

        return jsonify({
            "error": str(e),
            "data": []
        }), 500


    finally:

        if conn:

            conn.close()
        
@app.route("/api/create_staff_account",
           methods=["POST"])
def create_staff_account():

    conn = None
    cursor = None

    try:

        data = request.get_json() or {}

        print("CREATE STAFF DATA:", data)

        fullname = data.get("fullname", "").strip()
        username = data.get("username", "").strip()
        password = data.get("password", "")
        role = data.get("role", "").strip().lower()

        price_day = data.get("price_day")
        price_week = data.get("price_week")
        price_month = data.get("price_month")

        # Trainer programs
        programs = data.get("programs", [])


        # =========================
        # BASIC VALIDATION
        # =========================

        if not fullname or not username or not password or not role:

            return jsonify({
                "status": "error",
                "message": "Please complete all required fields."
            }), 400


        if role not in ["staff", "trainer"]:

            return jsonify({
                "status": "error",
                "message": "Invalid role."
            }), 400


        # =========================
        # TRAINER VALIDATION
        # =========================

        if role == "trainer":

            # At least one program
            if not programs:

                return jsonify({
                    "status": "error",
                    "message": "Please select at least one program."
                }), 400


            # =========================
            # TRAINER PRICE VALIDATION
            # =========================

            if (
                price_day is None or
                price_week is None or
                price_month is None
            ):

                return jsonify({
                    "status": "error",
                    "message": "All trainer prices are required."
                }), 400


            try:

                price_day = float(price_day)
                price_week = float(price_week)
                price_month = float(price_month)

            except (ValueError, TypeError):

                return jsonify({
                    "status": "error",
                    "message": "Invalid trainer price."
                }), 400


            if (
                price_day < 0 or
                price_week < 0 or
                price_month < 0
            ):

                return jsonify({
                    "status": "error",
                    "message": "Trainer prices cannot be negative."
                }), 400


            # =========================
            # PROGRAM ID VALIDATION
            # =========================

            try:

                programs = [
                    int(program_id)
                    for program_id in programs
                ]

            except (ValueError, TypeError):

                return jsonify({
                    "status": "error",
                    "message": "Invalid program selection."
                }), 400


            # Remove duplicate programs

            programs = list(
                dict.fromkeys(programs)
            )


        # =========================
        # DATABASE
        # =========================

        conn = get_connection()

        cursor = conn.cursor(
            pymysql.cursors.DictCursor
        )


        # =========================
        # CHECK USERNAME
        # =========================

        cursor.execute("""
            SELECT id
            FROM user_accounts
            WHERE username=%s
            LIMIT 1
        """, (
            username,
        ))

        existing = cursor.fetchone()

        if existing:

            return jsonify({
                "status": "error",
                "message": "Username already exists."
            }), 409


        # =========================
        # VALIDATE PROGRAMS
        # =========================

        if role == "trainer":

            placeholders = ",".join(
                ["%s"] * len(programs)
            )

            cursor.execute(
                f"""
                SELECT id
                FROM programs
                WHERE id IN ({placeholders})
                AND active = 1
                """,
                tuple(programs)
            )

            valid_programs = cursor.fetchall()

            valid_ids = {
                int(row["id"])
                for row in valid_programs
            }


            # Check if every selected
            # program actually exists

            for program_id in programs:

                if program_id not in valid_ids:

                    return jsonify({
                        "status": "error",
                        "message": "One or more selected programs are invalid."
                    }), 400


        # =========================
        # GENERATE USER ID
        # =========================

        if role == "staff":

            prefix = "S"

        else:

            prefix = "T"


        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM user_accounts
            WHERE role=%s
        """, (
            role,
        ))

        row = cursor.fetchone()

        total = int(row["total"]) + 1

        user_id = f"{prefix}{total:04d}"


        # =========================
        # CREATE ACCOUNT
        # =========================

        cursor.execute("""
            INSERT INTO user_accounts
            (
                user_id,
                fullname,
                username,
                password,
                role
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s
            )
        """, (
            user_id,
            fullname,
            username,
            password,
            role
        ))


        # =========================
        # SAVE TRAINER PRICES
        # ONE SET ONLY
        # =========================

        if role == "trainer":

            cursor.execute("""
                INSERT INTO trainer_plans
                (
                    trainer_id,
                    plan_name,
                    duration_days,
                    price,
                    active
                )
                VALUES
                    (%s, '1 Day', 1, %s, 1),
                    (%s, '1 Week', 7, %s, 1),
                    (%s, '1 Month', 30, %s, 1)
            """, (
                user_id,
                price_day,

                user_id,
                price_week,

                user_id,
                price_month
            ))


        # =========================
        # SAVE TRAINER PROGRAMS
        # NO PRICES HERE
        # =========================

        if role == "trainer":

            for program_id in programs:

                cursor.execute("""
                    INSERT INTO trainer_programs
                    (
                        trainer_id,
                        program_id,
                        active
                    )
                    VALUES
                    (
                        %s,
                        %s,
                        1
                    )
                """, (
                    user_id,
                    program_id
                ))


        # =========================
        # COMMIT
        # =========================

        conn.commit()


        # =========================
        # LOG
        # =========================

        print("================================")
        print("ACCOUNT CREATED")
        print("USER ID :", user_id)
        print("ROLE    :", role)

        if role == "trainer":

            print("PROGRAMS :", programs)
            print("1 DAY    :", price_day)
            print("1 WEEK   :", price_week)
            print("1 MONTH  :", price_month)

        print("================================")


        # =========================
        # RESPONSE
        # =========================

        return jsonify({

            "status": "success",

            "message":
                "Trainer account, pricing, and programs created successfully."
                if role == "trainer"
                else
                "Staff account created successfully.",

            "user_id": user_id

        }), 201


    # =========================
    # ERROR
    # =========================

    except Exception as e:

        if conn:

            conn.rollback()


        print(
            "CREATE STAFF ERROR:",
            e
        )


        return jsonify({

            "status": "error",

            "message": str(e)

        }), 500


    # =========================
    # CLOSE CONNECTION
    # =========================

    finally:

        if cursor:

            cursor.close()

        if conn:

            conn.close()

@app.route("/api/programs", methods=["GET"])
def get_programs():

    conn = None
    cursor = None

    try:

        conn = get_connection()

        cursor = conn.cursor(
            pymysql.cursors.DictCursor
        )

        cursor.execute("""
            SELECT
                id,
                program_name,
                description,
                duration_days,
                active
            FROM programs
            WHERE active = 1
            ORDER BY program_name
        """)

        programs = cursor.fetchall()

        return jsonify(programs), 200

    except Exception as e:

        print("PROGRAM LOAD ERROR:", e)

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()

@app.route(
    "/api/programs/<int:program_id>/plans",
    methods=["GET"]
)
def get_program_plans(program_id):

    conn = None
    cursor = None

    try:

        # =========================
        # DATABASE
        # =========================

        conn = get_connection()

        cursor = conn.cursor(
            pymysql.cursors.DictCursor
        )


        # =========================
        # CHECK PROGRAM
        # =========================

        cursor.execute("""
            SELECT
                id,
                program_name,
                description,
                duration_days,
                active
            FROM programs
            WHERE id = %s
            AND active = 1
            LIMIT 1
        """, (
            program_id,
        ))

        program = cursor.fetchone()


        if not program:

            return jsonify({
                "status": "error",
                "message": "Program not found."
            }), 404


        # =========================
        # GET PLANS / SPLITS
        # =========================

        cursor.execute("""
            SELECT
                id,
                program_id,
                plan_name,
                description,
                active,
                created_at
            FROM program_plans
            WHERE program_id = %s
            AND active = 1
            ORDER BY id ASC
        """, (
            program_id,
        ))

        plans = cursor.fetchall()


        # =========================
        # FORMAT DATE
        # =========================

        for plan in plans:

            if plan["created_at"] is not None:

                plan["created_at"] = (
                    plan["created_at"]
                    .strftime("%Y-%m-%d %H:%M:%S")
                )


        # =========================
        # RESPONSE
        # =========================

        return jsonify({

            "status": "success",

            "program": {
                "id": program["id"],
                "program_name":
                    program["program_name"],
                "description":
                    program["description"],
                "duration_days":
                    program["duration_days"]
            },

            "plans": plans

        }), 200


    # =========================
    # ERROR
    # =========================

    except Exception as e:

        print(
            "PROGRAM PLANS LOAD ERROR:",
            e
        )

        return jsonify({

            "status": "error",
            "message": str(e)

        }), 500


    # =========================
    # CLOSE
    # =========================

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()

@app.route("/api/program_trainers", methods=["GET"])
def get_program_trainers():

    conn = None
    cursor = None

    try:

        conn = get_connection()

        cursor = conn.cursor(
            pymysql.cursors.DictCursor
        )

        cursor.execute("""
            SELECT
                p.id AS program_id,
                p.program_name,
                p.description,
                p.duration_days,

                u.user_id AS trainer_id,
                u.fullname AS trainer_name,

                /* =========================
                   TRAINER RATE PLAN IDs
                   ========================= */

                MAX(
                    CASE
                        WHEN tp.plan_name = '1 Day'
                        THEN tp.id
                    END
                ) AS plan_id_day,

                MAX(
                    CASE
                        WHEN tp.plan_name = '1 Week'
                        THEN tp.id
                    END
                ) AS plan_id_week,

                MAX(
                    CASE
                        WHEN tp.plan_name = '1 Month'
                        THEN tp.id
                    END
                ) AS plan_id_month,

                /* =========================
                   TRAINER RATE PRICES
                   ========================= */

                MAX(
                    CASE
                        WHEN tp.plan_name = '1 Day'
                        THEN tp.price
                    END
                ) AS price_day,

                MAX(
                    CASE
                        WHEN tp.plan_name = '1 Week'
                        THEN tp.price
                    END
                ) AS price_week,

                MAX(
                    CASE
                        WHEN tp.plan_name = '1 Month'
                        THEN tp.price
                    END
                ) AS price_month

            FROM programs p

            INNER JOIN trainer_programs trp
                ON trp.program_id = p.id
                AND trp.active = 1

            INNER JOIN user_accounts u
                ON u.user_id COLLATE utf8mb4_general_ci
                   =
                   trp.trainer_id COLLATE utf8mb4_general_ci

                AND u.role = 'trainer'

            LEFT JOIN trainer_plans tp
                ON tp.trainer_id COLLATE utf8mb4_general_ci
                   =
                   u.user_id COLLATE utf8mb4_general_ci

                AND tp.active = 1

            WHERE p.active = 1

            GROUP BY
                p.id,
                p.program_name,
                p.description,
                p.duration_days,
                u.user_id,
                u.fullname

            ORDER BY
                p.id,
                u.fullname
        """)

        data = cursor.fetchall()

        return jsonify(data), 200


    except Exception as e:

        print(
            "PROGRAM TRAINERS ERROR:",
            e
        )

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()

@app.route("/api/staff_accounts")
def staff_accounts():

    conn = get_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    cursor.execute("""
        SELECT
            user_id,
            fullname,
            username,
            role
        FROM user_accounts
        WHERE role IN ('staff','trainer')
    """)

    rows = cursor.fetchall()

    conn.close()

    return jsonify(rows)

@app.route("/api/delete_staff/<user_id>",
           methods=["DELETE"])
def delete_staff(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM user_accounts
        WHERE user_id=%s
    """,(user_id,))

    conn.commit()
    conn.close()

    return jsonify({
        "status":"success"
    })

@app.route("/api/attendance_summary", methods=["GET"])
def attendance_summary():
    try:
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        # 🔥 TODAY COUNT
        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM attendance_sessions
            WHERE DATE(time_in) = CURDATE()
        """)
        today = cursor.fetchone()["total"]

        # 🔥 TODAY USERS (NAME LIST)
        cursor.execute("""
            SELECT COALESCE(m.full_name, w.full_name) AS name
            FROM attendance_sessions a
            LEFT JOIN members m ON a.user_id = m.id
            LEFT JOIN walkins w ON a.user_id = w.id
            WHERE DATE(a.time_in) = CURDATE()
        """)
        users = [row["name"] for row in cursor.fetchall()]

        return jsonify({
            "today": today,
            "users": users
        })

    except Exception as e:
        return jsonify({"error": str(e)})

    finally:
        conn.close()

# ==============================
# 🔐 LOCKERS API (NEW 🔥)
# ==============================
from datetime import datetime
from datetime import timedelta

@app.route("/api/lockers", methods=["GET"])
def get_lockers():

    conn = None

    try:

        conn = get_connection()

        cursor = conn.cursor(
            pymysql.cursors.DictCursor
        )

        cursor.execute("""
            SELECT

                l.locker_number,

                CASE
                    WHEN ls.status = 'overtime'
                        THEN 'OVERTIME'

                    WHEN ls.status = 'active'
                        THEN 'IN_USE'

                    WHEN l.status = 'RESERVED'
                        THEN 'RESERVED'

                    ELSE 'AVAILABLE'
                END AS status,

                ls.user_id,
                ls.start_time,

                COALESCE(
                    m.full_name,
                    w.full_name,
                    ls.user_id
                ) AS full_name

            FROM lockers l

            LEFT JOIN locker_sessions ls
                ON l.locker_number = ls.locker_number
                AND ls.status IN ('active', 'overtime')

            LEFT JOIN members m
                ON CONVERT(ls.user_id USING utf8mb4)
                   COLLATE utf8mb4_general_ci
                   =
                   CONVERT(m.id USING utf8mb4)
                   COLLATE utf8mb4_general_ci

            LEFT JOIN walkins w
                ON CONVERT(ls.user_id USING utf8mb4)
                   COLLATE utf8mb4_general_ci
                   =
                   CONVERT(w.id USING utf8mb4)
                   COLLATE utf8mb4_general_ci

            ORDER BY l.locker_number ASC
        """)

        rows = cursor.fetchall()

        data = []

        for row in rows:

            # =========================
            # NAME
            # =========================
            name = row["full_name"] or "-"

            # =========================
            # TIME
            # =========================
            time_start = "-"

            if row["start_time"]:
                time_start = row["start_time"].strftime("%I:%M %p")

            data.append({
                "locker": row["locker_number"],
                "name": name,
                "time_start": time_start,
                "status": row["status"]
            })

        return jsonify({
            "data": data
        }), 200

    except Exception as e:

        print("LOCKER API ERROR:", repr(e))

        return jsonify({
            "error": str(e),
            "data": []
        }), 500

    finally:

        if conn:
            conn.close()
@app.route("/api/locker_history", methods=["GET"])
def locker_history():

    conn = None

    try:

        date = request.args.get("date")

        conn = get_connection()

        cursor = conn.cursor(
            pymysql.cursors.DictCursor
        )

        if date:

            cursor.execute("""
                SELECT
                    ls.locker_number,

                    ls.start_time,

                    ls.end_time,

                    ls.status,

                    COALESCE(
                        m.full_name,
                        w.full_name,
                        ls.user_id
                    ) AS name

                FROM locker_sessions ls

                LEFT JOIN members m
                    ON CONVERT(ls.user_id USING utf8mb4)
                    COLLATE utf8mb4_unicode_ci
                    =
                    CONVERT(m.id USING utf8mb4)
                    COLLATE utf8mb4_unicode_ci

                LEFT JOIN walkins w
                    ON CONVERT(ls.user_id USING utf8mb4)
                    COLLATE utf8mb4_unicode_ci
                    =
                    CONVERT(w.id USING utf8mb4)
                    COLLATE utf8mb4_unicode_ci

                WHERE DATE(ls.start_time) = %s

                ORDER BY ls.start_time DESC

            """, (date,))

        else:

            cursor.execute("""
                SELECT
                    ls.locker_number,

                    ls.start_time,

                    ls.end_time,

                    ls.status,

                    COALESCE(
                        m.full_name,
                        w.full_name,
                        ls.user_id
                    ) AS name

                FROM locker_sessions ls

                LEFT JOIN members m
                    ON CONVERT(ls.user_id USING utf8mb4)
                    COLLATE utf8mb4_unicode_ci
                    =
                    CONVERT(m.id USING utf8mb4)
                    COLLATE utf8mb4_unicode_ci

                LEFT JOIN walkins w
                    ON CONVERT(ls.user_id USING utf8mb4)
                    COLLATE utf8mb4_unicode_ci
                    =
                    CONVERT(w.id USING utf8mb4)
                    COLLATE utf8mb4_unicode_ci

                ORDER BY ls.start_time DESC

            """)

        rows = cursor.fetchall()

        data = []

        for row in rows:

            start = "-"
            end = "-"

            if row["start_time"]:
                start = row["start_time"].strftime("%I:%M %p")

            if row["end_time"]:
                end = row["end_time"].strftime("%I:%M %p")

            data.append({
                "name": row["name"] if row["name"] else "-",
                "locker": row["locker_number"],
                "start": start,
                "end": end,
                "status": row["status"]
            })

        return jsonify({
            "data": data
        })

    except Exception as e:

        print("================================")
        print("LOCKER HISTORY API ERROR:")
        print(e)
        print("================================")

        return jsonify({
            "error": str(e)
        }), 500

    finally:

        if conn:
            conn.close()
@app.route("/api/notify/attendance", methods=["POST"])
def notify_attendance_api():
    socketio.emit("attendance_update")
    print("🔥 ATTENDANCE EMITTED")
    return jsonify({"status": "ok"})
        
@app.route("/api/notify/locker", methods=["POST"])
def notify_locker():
    print("[NOTIFY] Locker update received")
    socketio.emit("locker_update")
    return {"status": "ok"}

# ==============================
# 📊 DASHBOARD API
# ==============================
@app.route("/api/dashboard", methods=["GET"])
def get_dashboard():
    conn = None

    total_attendance = 0
    active_users = 0
    active_lockers = 0

    try:
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        # 🔥 TOTAL ATTENDANCE (TODAY)
        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM attendance_sessions
            WHERE DATE(time_in) = CURDATE()
        """)
        total_attendance = cursor.fetchone()["total"]

        # 🔥 ACTIVE USERS (TODAY ONLY)
        cursor.execute("""
            SELECT COUNT(*) AS active
            FROM attendance_sessions
            WHERE time_out IS NULL
            AND DATE(time_in) = CURDATE()
        """)
        active_users = cursor.fetchone()["active"]

        # 🔥 ACTIVE LOCKERS (TODAY ONLY)
        cursor.execute("""
            SELECT COUNT(*) AS lockers
            FROM locker_sessions
            WHERE status = 'active'
            AND DATE(start_time) = CURDATE()
        """)
        active_lockers = cursor.fetchone()["lockers"]

    except Exception as e:
        print("DASHBOARD ERROR:", e)

    finally:
        if conn:
            conn.close()

    return jsonify({
        "total_attendance": total_attendance,
        "active_users": active_users,
        "active_lockers": active_lockers
    })

@app.route("/api/alerts", methods=["GET"])
def get_alerts():
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        alerts = []

        from datetime import datetime, timedelta

        # GET ACTIVE LOCKERS
        cursor.execute("""
            SELECT locker_number, start_time
            FROM locker_sessions
            WHERE status = 'active'
        """)

        rows = cursor.fetchall()

        for row in rows:
            locker = row["locker_number"]
            start = row["start_time"]

            # 🔥 3 HOURS LIMIT
            end_time = start + timedelta(hours=3)

            if datetime.now() > end_time:
                alerts.append({
                    "type": "OVERTIME",
                    "message": f"Locker {locker} exceeded 3 hours"
                })

        return jsonify({
            "alerts": alerts,
            "has_alert": len(alerts) > 0
        })

    except Exception as e:
        print("ALERT ERROR:", e)
        return jsonify({"alerts": [], "has_alert": False})

    finally:
        if conn:
            conn.close()
            
@app.route("/api/notify/security", methods=["POST"])
def notify_security():
    
    print("🔥 SECURITY ROUTE HIT")

    try:
        data = request.get_json()

        event = data.get("event")     # BYPASS / TAILGATING
        lane = data.get("lane")       # IN / OUT
        time_val = data.get("time")

        print(f"🚨 SECURITY ALERT: {event} | {lane}")

        # 🔥 REALTIME SEND TO WEBSITE
        socketio.emit("security_alert", {
            "event": event,
            "lane": lane,
            "time": time_val
        })

        return jsonify({"status": "ok"})

    except Exception as e:
        print("SECURITY ERROR:", e)
        return jsonify({"error": str(e)}), 500
            
@app.route("/api/notify/overtime", methods=["POST"])
def notify_overtime():
    try:
        data = request.get_json()
        locker = data.get("locker")

        print(f"⚠️ OVERTIME RECEIVED: Locker {locker}")

        # 🔥 REALTIME EMIT
        socketio.emit("overtime_alert", {
            "message": f"Locker {locker} is overtime"
        })

        return jsonify({"status": "ok"})

    except Exception as e:
        print("OVERTIME ERROR:", e)
        return jsonify({"error": str(e)}), 500

from datetime import datetime

@app.route("/api/members_list", methods=["GET"])
def get_members_list():

    conn = get_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    cursor.execute("""
        SELECT 
            id,
            full_name,
            membership_type,
            membership_expires,
            monthly_expires
        FROM members
    """)

    rows = cursor.fetchall()

    result = []

    now = datetime.now()

    for r in rows:

        # =========================
        # FORMAT DATE ONLY
        # =========================
        def format_date(dt):

            if not dt:
                return None

            return dt.strftime("%Y-%m-%d")

        membership_exp = format_date(
            r["membership_expires"]
        )

        monthly_exp = format_date(
            r["monthly_expires"]
        )

        # =========================
        # MEMBERSHIP STATUS
        # =========================
        membership_status = "EXPIRED"

        if r["membership_expires"]:

            membership_status = (
                "ACTIVE"
                if r["membership_expires"] > now
                else "EXPIRED"
            )

        # =========================
        # MONTHLY STATUS
        # =========================
        monthly_status = "EXPIRED"

        if r["monthly_expires"]:

            monthly_status = (
                "ACTIVE"
                if r["monthly_expires"] > now
                else "EXPIRED"
            )

        # =========================
        # DAILY = NO MONTHLY
        # =========================
        membership_type = (
            r["membership_type"] or ""
        ).lower()

        if "daily" in membership_type:

            monthly_status = "-"
            monthly_exp = "-"

        result.append({

            "id": r["id"],

            "name": r["full_name"],

            "type": r["membership_type"],

            "membership_expires": membership_exp,

            "membership_status": membership_status,

            "monthly_expires": monthly_exp,

            "monthly_status": monthly_status

        })

    conn.close()

    return jsonify(result)

@app.route("/api/book_locker", methods=["POST"])
def book_locker():

    try:
        data = request.get_json()

        print("BOOK DATA:", data)

        user_id = data.get("user_id")
        locker = data.get("locker")
        date = data.get("date")

        # 🔥 NEW FORMAT
        start_time = data.get("start_time")
        end_time = data.get("end_time")
        
        

        # =========================
        # VALIDATE
        # =========================
        if not start_time or not end_time:

            return jsonify({
                "status": "error",
                "message": "Missing time"
            })

        conn = get_connection()
        cursor = conn.cursor()

        # =========================
        # CHECK OVERLAP
        # =========================
        cursor.execute("""
            SELECT *
            FROM locker_bookings
            WHERE locker_number=%s
            AND date=%s
            AND status IN ('PENDING','APPROVED')
            AND (
                (%s < end_time AND %s > start_time)
            )
        """, (
            locker,
            date,
            start_time,
            end_time
        ))

        existing = cursor.fetchone()

        if existing:

            return jsonify({
                "status": "error",
                "message": "Time overlaps with existing booking"
            })

        # =========================
        # INSERT
        # =========================
        cursor.execute("""
            INSERT INTO locker_bookings
            (
                user_id,
                locker_number,
                date,
                start_time,
                end_time,
                status
            )
            VALUES (%s,%s,%s,%s,%s,'PENDING')
        """, (
            user_id,
            locker,
            date,
            start_time,
            end_time
        ))

        conn.commit()
        
        # =========================
        # ADMIN MESSAGE
        # =========================
        cursor.execute("""

            INSERT INTO messages
            (
                user_id,
                title,
                message,
                reason
            )

            VALUES (%s,%s,%s,%s)

        """, (

            "ADMIN",

            "NEW BOOKING",

            f"{user_id} booked Locker {locker} ({format_time(start_time)} - {format_time(end_time)})",

            "-"

        ))
        conn.commit()
        
        socketio.emit(
            "new_booking",
            {
                "message": "New booking received"
            }
        )

        return jsonify({
            "status": "success",
            "message": "Booking submitted"
        })

    except Exception as e:

        print("BOOK ERROR:", e)

        return jsonify({
            "status": "error",
            "message": str(e)
        })
    
@app.route("/api/admin_messages")
def admin_messages():

    conn = get_connection()

    cursor = conn.cursor(
        pymysql.cursors.DictCursor
    )

    cursor.execute("""

        SELECT

            id,
            title,
            message,
            reason,
            is_read,

            DATE_FORMAT(
                CONVERT_TZ(created_at, '+00:00', '+08:00'),
                '%M %d, %Y %h:%i %p'
            ) AS created_at

        FROM messages

        WHERE user_id='ADMIN'

        ORDER BY id DESC

    """)

    rows = cursor.fetchall()

    conn.close()

    return jsonify(rows)

from datetime import timedelta

@app.route("/api/bookings")
def get_bookings():

    try:

        conn = get_connection()

        cursor = conn.cursor(pymysql.cursors.DictCursor)

        cursor.execute("""
            SELECT *
            FROM locker_bookings
            ORDER BY id DESC
        """)

        bookings = cursor.fetchall()

        for b in bookings:

            # =========================
            # FIX DATE
            # =========================
            if b.get("start_time"):

                b["start_time"] = str(b["start_time"])

            if b.get("end_time"):

                b["end_time"] = str(b["end_time"])

            # =========================
            # FIX TIMEDELTA
            # =========================
            if b.get("start_time"):

                b["start_time"] = str(b["start_time"])

            if b.get("end_time"):

                b["end_time"] = str(b["end_time"])

            if b.get("time"):

                b["time"] = str(b["time"])

            # =========================
            # SLOT FORMAT
            # =========================
            if b.get("start_time") and b.get("end_time"):

                b["slot"] = (
                    f'{b["start_time"]} - {b["end_time"]}'
                )

            elif b.get("time"):

                b["slot"] = b["time"]

            else:

                b["slot"] = "-"

        return jsonify({
            "data": bookings
        })

    except Exception as e:

        print("ERROR:", e)

        return jsonify({
            "error": str(e)
        })

    finally:

        conn.close()
        
# ==============================
# FORMAT TIME
# ==============================
def format_time(t):

    return datetime.strptime(
        t,
        "%H:%M"
    ).strftime("%I:%M %p")

@app.route("/api/booked_slots")
def booked_slots():

    try:

        locker = request.args.get("locker")
        date = request.args.get("date")

        print("LOCKER RECEIVED:", locker)
        print("DATE RECEIVED:", date)

        conn = get_connection()

        cursor = conn.cursor(
            pymysql.cursors.DictCursor
        )

        cursor.execute("""
            SELECT start_time, end_time
            FROM locker_bookings
            WHERE locker_number=%s
            AND date=%s
            AND status IN ('PENDING','APPROVED')
        """, (
            locker,
            date
        ))

        rows = cursor.fetchall()
        
        print("DB ROWS:", rows)

        slots = []

        slots = []

        for r in rows:

            start = r["start_time"]
            end = r["end_time"]

            # 🔥 IF STRING
            if isinstance(start, str):
                start = datetime.strptime(start, "%H:%M")

            if isinstance(end, str):
                end = datetime.strptime(end, "%H:%M")

            # 🔥 FORMAT TO 12 HOURS
            start_fmt = start.strftime("%I:%M %p").lstrip("0")
            end_fmt = end.strftime("%I:%M %p").lstrip("0")

            slots.append(f"{start_fmt} - {end_fmt}")

        print("BOOKED:", slots)

        return jsonify({
            "slots": slots
        })

    except Exception as e:

        print("BOOKED SLOT ERROR:", e)

        return jsonify({
            "error": str(e)
        })

    finally:

        conn.close()

@app.route("/api/fully_booked_dates")
def fully_booked_dates():

    try:

        conn = get_connection()

        cursor = conn.cursor(pymysql.cursors.DictCursor)

        cursor.execute("""
            SELECT DISTINCT date
            FROM locker_bookings
            WHERE status='APPROVED'
        """)

        rows = cursor.fetchall()

        dates = []

        for r in rows:

            dates.append(str(r["date"]))

        return jsonify({
            "dates": dates
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        })

    finally:

        conn.close()
        
@app.route("/api/current_lockers")
def current_lockers():

    try:

        conn = get_connection()

        cursor = conn.cursor(
            pymysql.cursors.DictCursor
        )

        cursor.execute("""
            SELECT locker_number,
                   status
            FROM lockers
        """)

        rows = cursor.fetchall()

        conn.close()

        lockers = {}

        for r in rows:

            locker = str(r["locker_number"])

            status = r["status"]

            print(locker, status)

            if status == "OCCUPIED":

                lockers[locker] = "IN_USE"

            elif status == "RESERVED":

                lockers[locker] = "RESERVED"

            elif status == "OVERTIME":

                lockers[locker] = "OVERTIME"

            else:

                lockers[locker] = "AVAILABLE"

        return jsonify(lockers)

    except Exception as e:

        print("CURRENT LOCKER ERROR:", e)

        return jsonify({
            "error": str(e)
        }), 500

@app.route("/api/update_booking", methods=["POST"])
def update_booking():

    try:

        data = request.json

        print("UPDATE DATA:", data)

        conn = get_connection()

        cursor = conn.cursor(
            pymysql.cursors.DictCursor
        )

        # =========================
        # GET SENDER / FRONT DESK
        # =========================
        sender_id = data.get("sender_id")

        if not sender_id:
            return jsonify({
                "error": "Sender ID is required."
            }), 400

        cursor.execute("""
            SELECT
                user_id,
                fullname,
                role
            FROM user_accounts
            WHERE user_id=%s
            LIMIT 1
        """, (sender_id,))

        sender = cursor.fetchone()

        if not sender:
            return jsonify({
                "error": "Sender account not found."
            }), 404

        # Only Front Desk can approve/reject locker bookings
        if sender["role"] != "staff":
            return jsonify({
                "error": "Only Front Desk can update locker bookings."
            }), 403

        print("SENDER:", sender)

        # =========================
        # UPDATE BOOKING
        # =========================
        cursor.execute("""

            UPDATE locker_bookings

            SET status=%s,
                reason=%s

            WHERE id=%s

        """, (

            data["status"],
            data.get("reason"),
            data["id"]

        ))

        # =========================
        # GET BOOKING INFO
        # =========================
        cursor.execute("""

            SELECT
                user_id,
                locker_number

            FROM locker_bookings

            WHERE id=%s

        """, (data["id"],))

        booking = cursor.fetchone()

        print("BOOKING:", booking)

        if not booking:
            conn.rollback()
            return jsonify({
                "error": "Booking not found."
            }), 404

        # =========================
        # APPROVED
        # =========================
        if data["status"] == "APPROVED":

            print("INSERTING APPROVED MESSAGE")

            cursor.execute("""

                INSERT INTO messages
                (
                    user_id,
                    sender_id,
                    sender_name,
                    sender_role,
                    title,
                    message,
                    reason,
                    receiver_role
                )

                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)

            """, (

                booking["user_id"],

                sender["user_id"],

                sender["fullname"],

                sender["role"],

                "BOOKING ACCEPTED",

                f"Your booking for Locker {booking['locker_number']} was accepted.",

                "-",

                "member"

            ))

            print("APPROVED MESSAGE INSERTED")

        # =========================
        # REJECTED / DECLINED
        # =========================
        elif data["status"] in ["REJECTED", "DECLINED"]:

            print("INSERTING REJECTED MESSAGE")

            cursor.execute("""

                INSERT INTO messages
                (
                    user_id,
                    sender_id,
                    sender_name,
                    sender_role,
                    title,
                    message,
                    reason,
                    receiver_role
                )

                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)

            """, (

                booking["user_id"],

                sender["user_id"],

                sender["fullname"],

                sender["role"],

                "BOOKING REJECTED",

                f"Your booking for Locker {booking['locker_number']} was rejected.",

                data.get("reason") or "No reason provided",

                "member"

            ))

            print("REJECTED MESSAGE INSERTED")

        # =========================
        # COMMIT
        # =========================
        conn.commit()

        print("DATABASE COMMIT SUCCESS")

        conn.close()

        return jsonify({
            "message": "updated"
        })

    except Exception as e:

        print("UPDATE BOOKING ERROR:", e)

        if conn:
            conn.rollback()

        if conn:
            conn.close()

        return jsonify({
            "error": str(e)
        }), 500
        
from datetime import timedelta

@app.route("/api/approved_bookings", methods=["GET"])
def get_approved_bookings():
    try:
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        cursor.execute("""
            SELECT * FROM locker_bookings
            WHERE status='APPROVED'
        """)

        data = cursor.fetchall()

        # 🔥 FORCE CONVERT ALL VALUES TO STRING (SAFE)
        for row in data:
            for key in row:
                if isinstance(row[key], (timedelta,)):
                    row[key] = str(row[key])

        return jsonify({
            "data": data
        })

    except Exception as e:
        print("ERROR:", e)
        return jsonify({
            "error": str(e)
        })

    finally:
        conn.close()

@app.route("/api/cancel_booking", methods=["POST"])
def cancel_booking():
    data = request.json

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE locker_bookings
        SET status='CANCELLED'
        WHERE id=%s
    """, (data["id"],))

    conn.commit()
    conn.close()

    return jsonify({"message": "cancelled"})

@app.route("/api/notify/no_show", methods=["POST"])
def notify_no_show():
    data = request.json

    socketio.emit("new_alert", {
        "type": "NO_SHOW",
        "locker": data["locker"],
        "user": data["user"]
    })

    return jsonify({"status": "sent"})

@app.route("/api/create_account", methods=["POST"])
def create_account():
    try:
        data = request.get_json()

        user_id = data.get("user_id")
        username = data.get("username")
        password = data.get("password")

        conn = get_connection()
        cursor = conn.cursor()

        # 🔥 CHECK 1: member exists
        cursor.execute("SELECT id FROM members WHERE id=%s", (user_id,))
        if not cursor.fetchone():
            return jsonify({"status":"error","message":"Member not found"})

        # 🔥 CHECK 2: one account per member
        cursor.execute("SELECT * FROM user_accounts WHERE user_id=%s", (user_id,))
        if cursor.fetchone():
            return jsonify({"status":"error","message":"❌ Member already has an account"})

        # 🔥 CHECK 3: unique username (ADD THIS)
        cursor.execute("SELECT * FROM user_accounts WHERE username=%s", (username,))
        if cursor.fetchone():
            return jsonify({"status":"error","message":"❌ Username already taken"})

        # 🔥 INSERT
        cursor.execute("""
            INSERT INTO user_accounts (user_id, username, password, role)
            VALUES (%s,%s,%s,'member')
        """, (user_id, username, password))

        conn.commit()

        return jsonify({"status":"success","message":"Account created"})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"status":"error","message":str(e)})

    finally:
        conn.close()
        
@app.route("/api/account_status", methods=["GET"])
def account_status():

    try:

        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        cursor.execute("""
            SELECT
                m.id,
                m.full_name,
                ua.username

            FROM members m

            LEFT JOIN user_accounts ua
            ON m.id = ua.user_id

            ORDER BY m.id ASC
        """)

        rows = cursor.fetchall()

        result = []

        for r in rows:

            result.append({

                "id": r["id"],

                "name": r["full_name"],

                "username": r["username"],

                "status":
                    "HAS ACCOUNT"
                    if r["username"]
                    else "NO ACCOUNT"

            })

        return jsonify(result)

    except Exception as e:

        print("ERROR:", e)

        return jsonify([])

    finally:

        conn.close()
@app.route("/api/login", methods=["POST"])
def login():

    data = request.get_json()

    username = data.get("username", "").strip()
    password = data.get("password", "").strip()

    conn = get_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    try:

        cursor.execute("""
			SELECT
				ua.id,
				ua.user_id,
				COALESCE(m.full_name, ua.fullname) AS fullname,
				ua.username,
				ua.password,
				ua.role,
				pm.phone_number
			FROM user_accounts ua
			LEFT JOIN members m
				ON m.id COLLATE utf8mb4_general_ci
				= ua.user_id COLLATE utf8mb4_general_ci
			LEFT JOIN pending_members pm
				ON ua.id = pm.account_id
			WHERE ua.username=%s
		""", (username,))

        user = cursor.fetchone()

        if not user:

            return jsonify({
                "status": "error",
                "message": "Invalid username or password"
            })

        # Plain text password comparison
        if user["password"] != password:

            return jsonify({
                "status": "error",
                "message": "Invalid username or password"
            })

        return jsonify({

            "status": "success",

            "user": {

                # IMPORTANT:
                # user_accounts.id
                # This is the account_id used by pre_member
                "id": user["id"],

                # This can be NULL while still pre_member
                "user_id": user["user_id"],

                "fullname": user["fullname"],

                "username": user["username"],

                "phone_number": user["phone_number"],

                "role": user["role"]

            }

        })

    except Exception as e:

        print("LOGIN ERROR:", e)

        return jsonify({

            "status": "error",
            "message": str(e)

        }), 500

    finally:

        cursor.close()
        conn.close()       

@app.route("/api/change_password", methods=["POST"])
def change_password():

    data = request.get_json()

    username = data.get("username", "").strip()
    current_password = data.get("current_password", "")
    new_password = data.get("new_password", "")

    conn = get_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    try:

        cursor.execute("""
            SELECT id, password
            FROM user_accounts
            WHERE username=%s
        """, (username,))

        user = cursor.fetchone()

        if not user:

            return jsonify({
                "success": False,
                "message": "User not found."
            })

        # CHECK OLD PASSWORD
        if user["password"] != current_password:

            return jsonify({
                "success": False,
                "message": "Old password is incorrect."
            })

        # UPDATE PASSWORD
        cursor.execute("""
            UPDATE user_accounts
            SET password=%s
            WHERE id=%s
        """, (
            new_password,
            user["id"]
        ))

        conn.commit()

        return jsonify({
            "success": True,
            "message": "Password changed successfully."
        })

    except Exception as e:

        conn.rollback()

        print("CHANGE PASSWORD ERROR:", e)

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

    finally:

        cursor.close()
        conn.close()
@app.route("/api/membership/<user_id>")
def get_membership(user_id):

    try:

        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        cursor.execute("""
            SELECT 
                full_name,

                CASE 
                    WHEN NOW() <= membership_expires THEN 'ACTIVE'
                    ELSE 'EXPIRED'
                END AS membership_status,

                DATE_FORMAT(
                    membership_expires,
                    '%%Y-%%m-%%d'
                ) AS membership_validity,

                membership_type,

                CASE 
                    WHEN NOW() <= monthly_expires THEN 'PAID'
                    ELSE 'UNPAID'
                END AS monthly_status,

                DATE_FORMAT(
                    monthly_expires,
                    '%%Y-%%m-%%d'
                ) AS monthly_validity

            FROM members
            WHERE id = %s
        """, (user_id,))

        data = cursor.fetchone()

        # =====================================
        # DAILY MEMBERSHIP = NO MONTHLY
        # =====================================
        if data:

            membership_type = (
                data["membership_type"] or ""
            ).lower()

            if "daily" in membership_type:

                data["monthly_status"] = "-"
                data["monthly_validity"] = "-"

        return jsonify({
            "data": data
        })

    except Exception as e:

        print("ERROR:", e)

        return jsonify({
            "error": str(e)
        })

    finally:

        conn.close()
        
from flask_socketio import SocketIO

@app.route("/api/notify/priority", methods=["POST"])
def notify_priority():
    try:
        data = request.json

        locker = data.get("locker")
        message = data.get("message")
        time_str = data.get("time")

        execute_query(
            """
            INSERT INTO messages
            (user_id, title, message, reason)
            VALUES (%s,%s,%s,%s)
            """,
            (
                "ADMIN",
                "PRIORITY LANE ALERT",
                message,
                f"Reserved time: {time_str}"
            )
        )

        socketio.emit("new_message")
        socketio.emit("priority_alert", {
            "locker": locker,
            "time": time_str,
            "message": message
        })

        print("[PRIORITY SAVED TO MESSAGES]")

        return jsonify({"success": True})

    except Exception as e:
        print("PRIORITY ERROR:", e)
        return jsonify({"success": False, "error": str(e)}), 500
@app.route("/api/sync_attendance", methods=["POST"])
def sync_attendance():

    try:

        data = request.get_json()

        user_id = data.get("user_id")
        time_in = data.get("time_in")
        status = data.get("status", "ACTIVE")

        if not user_id:
            return jsonify({
                "success": False,
                "message": "user_id is required"
            }), 400

        execute_query(
            """
            INSERT INTO attendance_sessions
            (
                user_id,
                time_in,
                status
            )
            VALUES
            (
                %s,
                %s,
                %s
            )
            """,
            (
                user_id,
                time_in if time_in else datetime.now(),
                status
            )
        )

        socketio.emit("attendance_update")

        print(
            f"☁️ ATTENDANCE SYNCED: "
            f"{user_id} | {time_in}"
        )

        return jsonify({
            "success": True,
            "message": "Attendance synchronized."
        })

    except Exception as e:

        print(
            "SYNC ATTENDANCE ERROR:",
            e
        )

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500        
@app.route("/api/sync_timeout", methods=["POST"])
def sync_timeout():

    try:

        data = request.get_json()

        user_id = data.get("user_id")
        time_out = data.get("time_out")

        if not user_id:
            return jsonify({
                "success": False,
                "message": "user_id is required"
            }), 400

        execute_query(
            """
            UPDATE attendance_sessions
            SET
                time_out=%s,
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
            (
                time_out if time_out else datetime.now(),
                user_id
            )
        )

        socketio.emit("attendance_update")

        print(
            f"☁️ TIME-OUT SYNCED: "
            f"{user_id} | {time_out}"
        )

        return jsonify({
            "success": True
        })

    except Exception as e:

        print(
            "SYNC TIMEOUT ERROR:",
            e
        )

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


@app.route("/api/sync_locker_start", methods=["POST"])
def sync_locker_start():

    try:

        data = request.get_json()

        user_id = data.get("user_id")
        locker_id = data.get("locker_id")

        # CLOSE OLD
        execute_query(
            """
            UPDATE locker_sessions
            SET end_time = NOW(),
                status='ended'
            WHERE user_id=%s
            AND end_time IS NULL
            """,
            (user_id,)
        )

        # INSERT NEW
        execute_query(
            """
            INSERT INTO locker_sessions
            (
                user_id,
                locker_number,
                start_time,
                status
            )
            VALUES (%s,%s,NOW(),'active')
            """,
            (user_id, locker_id)
        )

        # 🔥 IMPORTANT
        execute_query(
            """
            UPDATE lockers
            SET status='OCCUPIED'
            WHERE locker_number=%s
            """,
            (locker_id,)
        )

        socketio.emit("locker_update")

        return jsonify({
            "success": True
        })

    except Exception as e:

        print("SYNC LOCKER ERROR:", e)

        return jsonify({
            "success": False
        }), 500
    
@app.route("/api/sync_locker_end", methods=["POST"])
def sync_locker_end():

    try:

        data = request.get_json()

        user_id = data.get("user_id")

        # GET LOCKER FIRST
        result = execute_query(
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

        locker_no = None

        if result:
            locker_no = result[0]["locker_number"]

        # END SESSION
        execute_query(
            """
            UPDATE locker_sessions
            SET end_time = NOW(),
                status='ended'
            WHERE user_id=%s
            AND end_time IS NULL
            """,
            (user_id,)
        )

        # 🔥 RELEASE LOCKER
        if locker_no:

            execute_query(
                """
                UPDATE lockers
                SET status='AVAILABLE'
                WHERE locker_number=%s
                """,
                (locker_no,)
            )

        socketio.emit("locker_update")

        return jsonify({
            "success": True
        })

    except Exception as e:

        print("SYNC LOCKER END ERROR:", e)

        return jsonify({
            "success": False
        }), 500
    
@app.route("/api/sync_locker_overtime", methods=["POST"])
def sync_locker_overtime():

    try:
        data = request.get_json()

        locker_id = data.get("locker_id")

        execute_query(
            """
            UPDATE locker_sessions
            SET status='overtime'
            WHERE locker_number=%s
            AND end_time IS NULL
            """,
            (locker_id,)
        )

        # 🔥 KULANG MO ITO
        execute_query(
            """
            UPDATE lockers
            SET status='OVERTIME'
            WHERE locker_number=%s
            """,
            (locker_id,)
        )

        socketio.emit("locker_update")

        print("☁️ CLOUD OVERTIME:", locker_id)

        return jsonify({
            "success": True
        })

    except Exception as e:

        print("SYNC LOCKER OVERTIME ERROR:", e)

        return jsonify({
            "success": False
        }), 500
    
@app.route("/api/sync_member", methods=["POST"])
def sync_member():

    try:

        data = request.get_json()
        print("SYNC DATA:", data)

        execute_query(
            """
            INSERT INTO members
            (
                id,
                full_name,
                phone_number,
                fingerprint_template,
                membership_type,
                membership_expires,
                monthly_expires
            )
            
            VALUES (%s,%s,%s,%s,%s,%s,%s)
            ON DUPLICATE KEY UPDATE
                full_name=VALUES(full_name),
                phone_number=VALUES(phone_number),
                fingerprint_template=VALUES(fingerprint_template),
                membership_type=VALUES(membership_type),
                membership_expires=VALUES(membership_expires),
                monthly_expires=VALUES(monthly_expires)
            """,
            (
                data["id"],
                data["full_name"],
                data["phone_number"],
                data.get("fingerprint_template"),
                data.get("membership_type"),
                data.get("membership_expires"),
                data.get("monthly_expires")
            )
        )

        socketio.emit("member_update")

        return jsonify({
            "success": True
        })

    except Exception as e:

        print("SYNC MEMBER ERROR:", e)

        return jsonify({
            "success": False
        }), 500
    
@app.route("/api/delete_member", methods=["POST"])
def delete_member_cloud_api():

    try:

        data = request.get_json()
        
        execute_query(
            "DELETE FROM user_accounts WHERE user_id=%s",
            (data["user_id"],)
        )

        execute_query(
            "DELETE FROM members WHERE id=%s",
            (data["user_id"],)
        )

        socketio.emit("member_update")

        return jsonify({
            "success": True
        })

    except Exception as e:

        print("DELETE MEMBER ERROR:", e)

        return jsonify({
            "success": False
        }), 500
    
@app.route("/api/sync_walkin", methods=["POST"])
def sync_walkin():

    try:

        data = request.get_json()

        execute_query(
            """
            INSERT INTO walkins
            (
                id,
                full_name,
                phone_number,
                fingerprint_template,
                fp_id,
                visit_date
            )
            VALUES (%s,%s,%s,%s,%s,CURDATE())
            ON DUPLICATE KEY UPDATE
                full_name=VALUES(full_name),
                phone_number=VALUES(phone_number),
                fingerprint_template=VALUES(fingerprint_template),
                fp_id=VALUES(fp_id)
            """,
            (
                data["id"],
                data["full_name"],
                data["phone_number"],
                data["fingerprint_template"],
                data["fp_id"]
            )
        )

        socketio.emit("walkin_update")

        return jsonify({"success": True})

    except Exception as e:

        print("SYNC WALKIN ERROR:", e)

        return jsonify({"success": False}), 500
    
@app.route("/api/delete_walkin", methods=["POST"])
def delete_walkin_cloud_api():

    try:

        data = request.get_json()

        execute_query(
            "DELETE FROM walkins WHERE id=%s",
            (data["user_id"],)
        )

        execute_query(
            "DELETE FROM fp_templates WHERE user_id=%s",
            (data["user_id"],)
        )

        socketio.emit("walkin_update")

        return jsonify({
            "success": True
        })

    except Exception as e:

        print("DELETE WALKIN ERROR:", e)

        return jsonify({
            "success": False
        }), 500
    
@app.route("/api/sync_payment", methods=["POST"])
def sync_payment():

    try:

        data = request.get_json()

        execute_query(
            """
            INSERT INTO payments
            (user_id, payment_type, amount, paid_at)
            VALUES (%s,%s,%s,NOW())
            """,
            (
                data["user_id"],
                data["payment_type"],
                data["amount"]
            )
        )

        socketio.emit("payment_update")

        return jsonify({"success": True})

    except Exception as e:

        print("SYNC PAYMENT ERROR:", e)

        return jsonify({"success": False}), 500
        
@app.route(
    "/api/update_locker_status",
    methods=["POST"]
)
def update_locker_status():

    try:

        data = request.json

        locker_number = data.get(
            "locker_number"
        )

        status = data.get(
            "status"
        )

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
            UPDATE lockers
            SET status=%s
            WHERE locker_number=%s
        """, (
            status,
            locker_number
        ))

        conn.commit()
        conn.close()

        print(
            f"☁️ LOCKER {locker_number} → {status}"
        )

        socketio.emit(
            "locker_update"
        )

        return jsonify({
            "success": True
        })

    except Exception as e:

        print(
            "UPDATE LOCKER STATUS ERROR:",
            e
        )

        return jsonify({
            "success": False
        }), 500
    
@app.route("/api/messages/<user_id>")
def get_messages(user_id):

    conn = get_connection()
    cursor = conn.cursor(
        pymysql.cursors.DictCursor
    )

    cursor.execute("""
        SELECT
            id,
            user_id,
            sender_id,
            sender_name,

            CASE
                WHEN sender_role = 'staff'
                    THEN 'Front Desk'
                WHEN sender_role = 'trainer'
                    THEN 'Trainer'
                ELSE sender_role
            END AS sender_role,

            title,
            message,
            reason,
            is_read,

            DATE_FORMAT(
                CONVERT_TZ(
                    created_at,
                    '+00:00',
                    '+08:00'
                ),
                '%%a, %%d %%b %%Y %%h:%%i %%p'
            ) AS created_at

        FROM messages

        WHERE user_id = %s

        ORDER BY id DESC

    """, (user_id,))

    rows = cursor.fetchall()

    conn.close()

    return jsonify(rows)

@app.route("/api/send_message", methods=["POST"])
def send_message():

    conn = None
    cursor = None

    try:

        data = request.get_json() or {}

        sender_id = str(
            data.get("sender_id", "")
        ).strip()

        receiver_id = str(
            data.get("receiver_id", "")
        ).strip()

        title = str(
            data.get("title", "")
        ).strip()

        message = str(
            data.get("message", "")
        ).strip()

        reason = data.get("reason", "-")

        # =========================
        # VALIDATION
        # =========================

        if not sender_id:
            return jsonify({
                "success": False,
                "message": "Sender ID is required."
            }), 400

        if not receiver_id:
            return jsonify({
                "success": False,
                "message": "Receiver ID is required."
            }), 400

        if not message:
            return jsonify({
                "success": False,
                "message": "Message is required."
            }), 400

        conn = get_connection()

        cursor = conn.cursor(
            pymysql.cursors.DictCursor
        )

        # =========================
        # GET SENDER
        # =========================

        cursor.execute("""
            SELECT
                user_id,
                fullname,
                role
            FROM user_accounts
            WHERE user_id = %s
            AND role IN ('staff', 'trainer')
            LIMIT 1
        """, (
            sender_id,
        ))

        sender = cursor.fetchone()

        if not sender:

            return jsonify({
                "success": False,
                "message": "Sender account not found."
            }), 404

        # =========================
        # GET RECEIVER
        # =========================

        cursor.execute("""
            SELECT
                user_id,
                fullname,
                role
            FROM user_accounts
            WHERE user_id = %s
            LIMIT 1
        """, (
            receiver_id,
        ))

        receiver = cursor.fetchone()

        if not receiver:

            return jsonify({
                "success": False,
                "message": "Receiver account not found."
            }), 404

        # =========================
        # SENDER ROLE
        # =========================

        sender_role = sender["role"]

        if sender_role == "staff":
            sender_role = "staff"

        elif sender_role == "trainer":
            sender_role = "trainer"

        else:
            return jsonify({
                "success": False,
                "message": "Only Front Desk and Trainer can send messages."
            }), 403

        # =========================
        # INSERT MESSAGE
        # =========================

        cursor.execute("""
            INSERT INTO messages
            (
                user_id,
                sender_id,
                sender_name,
                sender_role,
                title,
                message,
                reason,
                receiver_role,
                is_read
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                0
            )
        """, (
            receiver["user_id"],
            sender["user_id"],
            sender["fullname"],
            sender_role,
            title,
            message,
            reason,
            receiver["role"]
        ))

        message_id = cursor.lastrowid

        conn.commit()

        # =========================
        # REALTIME NOTIFICATION
        # =========================

        socketio.emit(
            "new_message",
            {
                "message_id": message_id,
                "receiver_id": receiver["user_id"]
            }
        )

        return jsonify({

            "success": True,

            "message": "Message sent successfully.",

            "data": {
                "id": message_id,
                "receiver_id": receiver["user_id"],
                "sender_id": sender["user_id"],
                "sender_name": sender["fullname"],
                "sender_role": sender_role,
                "title": title,
                "message": message,
                "reason": reason
            }

        }), 201

    except Exception as e:

        if conn:
            conn.rollback()

        print(
            "SEND MESSAGE ERROR:",
            e
        )

        return jsonify({

            "success": False,
            "message": str(e)

        }), 500

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()

@app.route("/api/member_active_locker/<user_id>", methods=["GET"])
def member_active_locker(user_id):
    try:
        row = execute_query(
            """
            SELECT locker_number
            FROM locker_sessions
            WHERE user_id=%s
            AND end_time IS NULL
            ORDER BY start_time DESC
            LIMIT 1
            """,
            (user_id,),
            fetchone=True
        )

        if row:
            return jsonify({
                "success": True,
                "locker": row["locker_number"]
            })

        return jsonify({
            "success": True,
            "locker": None
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
    
@app.route("/api/messages_count/<user_id>")
def messages_count(user_id):

    conn = get_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    cursor.execute("""
        SELECT COUNT(*) AS count
        FROM messages
        WHERE user_id=%s
        AND is_read=0
    """, (user_id,))

    row = cursor.fetchone()

    conn.close()

    return jsonify(row)


@app.route("/api/messages_read/<user_id>", methods=["POST"])
def messages_read(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE messages
        SET is_read = 1
        WHERE user_id = %s
    """, (user_id,))

    conn.commit()
    conn.close()

    return jsonify({"status":"success"})
    
@app.route("/api/messages_read_single/<int:msg_id>", methods=["POST"])
def messages_read_single(msg_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE messages
        SET is_read = 1
        WHERE id = %s
    """, (msg_id,))

    conn.commit()
    conn.close()

    return jsonify({"status": "success"})


@app.route("/api/messages_unread_single/<int:msg_id>", methods=["POST"])
def messages_unread_single(msg_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE messages
        SET is_read = 0
        WHERE id = %s
    """, (msg_id,))

    conn.commit()
    conn.close()

    return jsonify({"status": "success"})


@app.route("/api/messages_delete/<int:msg_id>", methods=["DELETE"])
def messages_delete(msg_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM messages
        WHERE id = %s
    """, (msg_id,))

    conn.commit()
    conn.close()

    return jsonify({"status": "success"})

import os

@app.route("/api/get_face_encodings", methods=["GET"])
def get_face_encodings():

    api_key = request.headers.get("X-API-KEY")

    if api_key != API_KEY:
        return jsonify({"error":"Unauthorized"}), 401

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    path = os.path.join(
        base_dir,
        "biometrics",
        "face",
        "encodings.pkl"
    )

    print("[ENCODINGS PATH]", path)

    if not os.path.exists(path):
        return jsonify({"error":"encodings not found"}), 404

    return send_file(
        path,
        as_attachment=True
    )
@app.route("/api/message_read/<int:id>", methods=["POST"])
def message_read(id):

    execute_query("""
        UPDATE messages
        SET is_read = 1
        WHERE id = %s
    """, (id,))

    return jsonify({
        "success": True
    })
    
@app.route("/api/message_unread/<int:id>", methods=["POST"])
def message_unread(id):

    execute_query("""
        UPDATE messages
        SET is_read = 0
        WHERE id = %s
    """, (id,))

    return jsonify({
        "success": True
    })
    
@app.route("/api/delete_message/<int:id>", methods=["DELETE"])
def delete_message(id):

    execute_query("""
        DELETE FROM messages
        WHERE id = %s
    """, (id,))

    return jsonify({
        "success": True
    })
    
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001, debug=True)
