import base64 
import sys, os
import sqlite3
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from flask import send_file
import json

# Path fix para mahanap ang 'db' folder sa root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db.connection import execute_query
import mysql.connector
from flask_socketio import SocketIO
from datetime import datetime

app = Flask(__name__)

CORS(app)
    
socketio = SocketIO(
    app,
    cors_allowed_origins="*"
)

# --- MILESTONE 4: SECURITY KEY ---
API_KEY = "GYM_MASTER_2026"

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
from flask import request
from datetime import datetime

@app.route("/api/attendance", methods=["GET"])
def get_attendance():
    try:
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        # ===== GET DATE FROM FRONTEND =====
        date = request.args.get("date")

        # default = today
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")

        # ===== QUERY WITH DATE FILTER =====
        cursor.execute("""
            SELECT 
                COALESCE(m.full_name, w.full_name) AS name,
                CASE 
                    WHEN m.id IS NOT NULL THEN 'member'
                    ELSE 'walk-in'
                END AS type,
                a.user_id,
                a.time_in,
                a.time_out,
                a.status
            FROM attendance_sessions a
            LEFT JOIN members m 
                ON a.user_id = m.id
            LEFT JOIN walkins w
                ON a.user_id = w.id
            WHERE DATE(a.time_in) = %s   -- 🔥 FILTER HERE
            ORDER BY a.time_in DESC
        """, (date,))

        rows = cursor.fetchall()

        data = []

        for row in rows:

            # ===== FORMAT TIME (NO SECONDS) =====
            time_in = row["time_in"].strftime("%I:%M %p") if row["time_in"] else "-"
            time_out = row["time_out"].strftime("%I:%M %p") if row["time_out"] else "-"

            data.append({
                "name": row["name"] if row["name"] else row["user_id"],
                "type": row["type"],
                "time_in": time_in,
                "time_out": time_out,
                "locker": "-",
                "remarks": "Completed" if row["time_out"] else "Active"
            })

        return jsonify({"data": data})

    except Exception as e:
        return jsonify({"error": str(e)})

    finally:
        conn.close()
        
@app.route("/api/create_staff_account",
           methods=["POST"])
def create_staff_account():

    try:

        data = request.json

        print(data)

        fullname = data["fullname"]
        username = data["username"]
        password = data["password"]
        role = data["role"]

        conn = get_connection()
        cursor = conn.cursor()

        if role == "staff":
            prefix = "S"
        else:
            prefix = "T"

        cursor.execute("""
            SELECT COUNT(*) total
            FROM user_accounts
            WHERE role=%s
        """,(role,))

        row = cursor.fetchone()

        print("ROW =", row)

        total = row[0] + 1

        user_id = f"{prefix}{total:04d}"

        cursor.execute("""
            INSERT INTO user_accounts
            (
                user_id,
                fullname,
                username,
                password,
                role
            )
            VALUES(%s,%s,%s,%s,%s)
        """,(
            user_id,
            fullname,
            username,
            password,
            role
        ))

        conn.commit()

        return jsonify({
            "status":"success"
        })

    except Exception as e:

        print("ERROR:", e)

        return jsonify({
            "status":"error",
            "message":str(e)
        }),500
        
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

    try:

        conn = get_connection()

        cursor = conn.cursor(
            pymysql.cursors.DictCursor
        )

        cursor.execute("""

            SELECT

                l.locker_number,

                CASE

                    WHEN ls.status='overtime'
                    THEN 'OVERTIME'

                    WHEN ls.status='active'
                    THEN 'IN_USE'

                    WHEN l.status='RESERVED'
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
            AND ls.status IN ('active','overtime')

            LEFT JOIN members m
            ON ls.user_id = m.id

            LEFT JOIN walkins w
            ON ls.user_id = w.id

            ORDER BY l.locker_number ASC

        """)

        rows = cursor.fetchall()

        data = []

        for row in rows:

            # 🔥 NAME
            name = row["full_name"] if row["full_name"] else "-"

            # 🔥 TIME
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
        })

    except Exception as e:

        print("LOCKER API ERROR:", e)

        return jsonify({
            "error": str(e)
        })

    finally:

        conn.close()
        
@app.route("/api/locker_history")
def locker_history():

    date = request.args.get("date")

    conn = get_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if date:
        cursor.execute("""
            SELECT 
                ls.locker_number,
                ls.start_time,
                ls.end_time,
                ls.status,
                COALESCE(m.full_name, w.full_name) AS name
            FROM locker_sessions ls
            LEFT JOIN members m ON ls.user_id = m.id
            LEFT JOIN walkins w ON ls.user_id = w.id
            WHERE DATE(ls.start_time)=%s
            ORDER BY ls.start_time DESC
        """,(date,))
    else:
        cursor.execute("SELECT * FROM locker_sessions")

    rows = cursor.fetchall()

    data = []
    for r in rows:
        data.append({
            "name": r["name"],
            "locker": r["locker_number"],
            "start": str(r["start_time"]),
            "end": str(r["end_time"]) if r["end_time"] else None,
            "status": r["status"]
        })

    return jsonify({"data": data})

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

        # =========================
        # APPROVED
        # =========================
        if data["status"] == "APPROVED":

            print("INSERTING APPROVED MESSAGE")

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

                booking["user_id"],

                "BOOKING ACCEPTED",

                f"Your booking for Locker {booking['locker_number']} was accepted.",

                "-"

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
                    title,
                    message,
                    reason
                )

                VALUES (%s,%s,%s,%s)

            """, (

                booking["user_id"],

                "BOOKING REJECTED",

                f"Your booking for Locker {booking['locker_number']} was rejected.",

                data.get("reason") or "No reason provided"

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
    conn = None
    try:
        data = request.get_json()

        username = data.get("username")
        password = data.get("password")

        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        # ✅ PURE LOGIN (NO JOIN)
        cursor.execute("""
            SELECT user_id, username, role
            FROM user_accounts
            WHERE username=%s AND password=%s
        """, (username, password))

        user = cursor.fetchone()

        if not user:
            return jsonify({
                "status": "error",
                "message": "Invalid login"
            })

        # ✅ OPTIONAL: get full name if MEMBER
        full_name = user["username"]

        if user["role"] == "member":
            cursor.execute("SELECT full_name FROM members WHERE id=%s", (user["user_id"],))
            m = cursor.fetchone()
            if m:
                full_name = m["full_name"]

        return jsonify({
            "status": "success",
            "user": {
                "id": user["user_id"],
                "name": full_name,
                "role": user["role"]
            }
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        })

    finally:
        if conn:
            conn.close()
            
@app.route("/api/change_password", methods=["POST"])
def change_password():

    try:

        data = request.get_json()

        username = data.get("username")
        old_password = data.get("old_password")
        new_password = data.get("new_password")

        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        cursor.execute("""
            SELECT *
            FROM user_accounts
            WHERE username=%s
            AND password=%s
        """, (
            username,
            old_password
        ))

        user = cursor.fetchone()

        if not user:

            return jsonify({
                "status": "error",
                "message": "Wrong username or password"
            })

        cursor.execute("""
            UPDATE user_accounts
            SET password=%s
            WHERE username=%s
        """, (
            new_password,
            username
        ))

        conn.commit()

        return jsonify({
            "status": "success",
            "message": "Password updated"
        })

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        })
            
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

        execute_query(
            """
            INSERT INTO attendance_sessions
            (user_id, time_in, status)
            VALUES (%s, NOW(), 'ACTIVE')
            """,
            (user_id,)
        )

        socketio.emit("attendance_update")

        return jsonify({
            "success": True
        })

    except Exception as e:

        print("SYNC ERROR:", e)

        return jsonify({
            "success": False
        }), 500

@app.route("/api/sync_timeout", methods=["POST"])
def sync_timeout():

    try:

        data = request.get_json()

        user_id = data.get("user_id")

        execute_query(
            """
            UPDATE attendance_sessions
            SET time_out = NOW(),
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
            (user_id,)
        )

        socketio.emit("attendance_update")

        return jsonify({
            "success": True
        })

    except Exception as e:

        print("SYNC TIMEOUT ERROR:", e)

        return jsonify({
            "success": False
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
