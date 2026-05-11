import os
os.environ["LIBCAMERA_LOG_LEVELS"] = "*:ERROR"
os.environ["DISPLAY"] = ":0"

from biometrics.fingerprint.in_sensor import InFingerprint
from biometrics.fingerprint.out_sensor import OutFingerprint
from attendance.time_in import check_time_in, save_time_in
from attendance.time_out import check_time_out, save_time_out
from db.connection import execute_query
from admin.menu import admin_menu
from config.settings import ADMIN_PASSWORD, MAX_ADMIN_ATTEMPTS
from biometrics.face.recognize import FaceRecognizer

from admin.actions import release_locker
from hardware.arduino_serial import init_serial, send_to_arduino, ser
from picamera2 import Picamera2
from config import camera_manager
from ui_display import UIDisplay
from ir_handler import wait_for_entry, wait_for_exit, monitor_bypass, check_tailgating
import cv2
import getpass
import time
import sys
import select
import threading
import system_state
import requests
from datetime import datetime

from api.api_server import socketio
from sms_module.sms import send_sms
from datetime import date



# =========================
# GLOBAL STATES
# =========================
system_paused = False
system_running = True
pending_face_user = None
admin_requested = False
recognition_enabled = True
# =========================
# ADMIN PASSWORD VERIFICATION
# =========================
def verify_admin():
    attempts = 0
    while attempts < MAX_ADMIN_ATTEMPTS:
        password = getpass.getpass("Enter Admin Password: ")
        if password == ADMIN_PASSWORD:
            print("Admin access granted.")
            return True
        attempts += 1
        print("Incorrect password.")
    print("Too many failed attempts.")
    return False

# =========================
# DATABASE HELPER
# =========================
def get_user_info_by_fp(fp_id):
    return execute_query(
        """
        SELECT 
            COALESCE(m.full_name, w.full_name) AS full_name,
            COALESCE(m.phone_number, w.phone_number) AS phone,
            f.user_id
        FROM fp_templates f
        LEFT JOIN members m ON f.user_id = m.id
        LEFT JOIN walkins w ON f.user_id = w.id
        WHERE f.fp_id = %s
        """,
        (fp_id,),
        fetch=True
    )

import requests

API_URL = "http://192.168.1.19:5001"

def notify_attendance():
    try:
        print("📡 Sending attendance update...")

        res = requests.post(f"{API_URL}/api/notify/attendance")

        print("Response:", res.status_code)

    except Exception as e:
        print("Notify error:", e)
    
def notify_locker():
    try:
        requests.post(f"{API_URL}/api/notify/locker")
    except:
        pass
    
def check_membership_status(user_id, full_name, phone):

    from datetime import date
    from sms_module.sms import send_sms

    result = execute_query("""
        SELECT monthly_expires, membership_expires, last_sms_sent
        FROM members
        WHERE id = %s
    """, (user_id,), fetch=True)

    if not result:
        return False

    row = result[0]
    today = date.today()

    # =========================
    # FORMAT NUMBER
    # =========================
    if phone.startswith("09"):
        phone = "63" + phone[1:]

    # ==================================================
    # 🔴 YEARLY MEMBERSHIP CHECK
    # (REMINDER ONLY - NO BLOCK)
    # ==================================================
    if row["membership_expires"]:

        yearly_expiry = row["membership_expires"].date()
        yearly_days = (yearly_expiry - today).days

        # EXPIRED
        if yearly_days < 0:

            print("DEBUG: YEARLY MEMBERSHIP EXPIRED")

            # avoid spam
            if row.get("last_sms_sent") != today:

                send_sms(
                    phone,
                    f"Hello {full_name}, your annual membership has expired. Please renew. - SMARTGYM"
                )

                execute_query("""
                    UPDATE members
                    SET last_sms_sent = %s
                    WHERE id = %s
                """, (today, user_id))

    # ==================================================
    # 🔴 MONTHLY / DAILY ACCESS REQUIRED
    # ==================================================
    if not row["monthly_expires"]:

        print("DEBUG: NO MONTHLY ACCESS")

        return False

    monthly_expiry = row["monthly_expires"].date()
    monthly_days = (monthly_expiry - today).days

    # =========================
    # SEND REMINDERS
    # =========================
    if monthly_days <= 3:

        # avoid spam
        if row.get("last_sms_sent") != today:

            if monthly_days > 0:

                msg = (
                    f"Hello {full_name}, your access will expire in "
                    f"{monthly_days} day(s). - SMARTGYM"
                )

            elif monthly_days == 0:

                msg = (
                    f"Hello {full_name}, your access expires TODAY. "
                    f"Please renew to avoid interruption. - SMARTGYM"
                )

            else:

                msg = (
                    f"Hello {full_name}, your access has expired. "
                    f"Please renew immediately. - SMARTGYM"
                )

            send_sms(phone, msg)

            execute_query("""
                UPDATE members
                SET last_sms_sent = %s
                WHERE id = %s
            """, (today, user_id))

    # =========================
    # BLOCK IF ACCESS EXPIRED
    # =========================
    if monthly_days < 0:

        print("DEBUG: MONTHLY ACCESS EXPIRED")

        return False

    # =========================
    # VALID ACCESS
    # =========================
    return True

# =========================
# IN THREAD (Entry Lane)
# =========================
def in_lane_loop(in_fp, face_recognizer, ui):

    while system_state.system_running:

        if system_state.system_paused:
            time.sleep(0.2)
            continue

        # =========================
        # WAIT FOR FINGERPRINT
        # =========================
        ui.set_status("")
        ui.set_name("")

        fp_id = in_fp.verify()

        if fp_id is None:
            time.sleep(0.1)
            continue

        user = get_user_info_by_fp(fp_id)

        if not user:
            print("[IN] Fingerprint not linked.")
            ui.set_status("NOT REGISTERED")
            send_to_arduino("IN:DENY:NOT_LINKED")
            time.sleep(1)
            continue

        user_id = user[0]["user_id"]
        full_name = user[0]["full_name"]

        user_type = "Member" if user_id.upper().startswith("M") else "Walkin"

        # =========================
        # MEMBER FLOW
        # =========================
        if user_type == "Member":

            # =========================
            # FACE VERIFICATION (FIXED)
            # =========================

            print("[IN] Starting face verification...")

            ui.set_status("LOOK AT CAMERA")

            start = time.time()
            face_ok = False

            while True:

                # 🔥 OPTIONAL TIMEOUT (10 seconds)
                if time.time() - start > 10:
                    break

                if system_state.system_paused:
                    break

                # 🔥 GET FRAME FROM UI (SAFE)
                with ui.frame_lock:
                    frame = None if ui.frame is None else ui.frame.copy()

                if frame is None:
                    time.sleep(0.05)
                    continue

                # 🔥 RECOGNIZE (PASS FRAME)
                face_user = face_recognizer.recognize(frame)

                # -------------------------
                # NO FACE → CONTINUE
                # -------------------------
                if face_user is None:
                    ui.set_status("NO FACE DETECTED")
                    time.sleep(0.1)
                    continue

                # -------------------------
                # MATCH
                # -------------------------
                if face_user == user_id:
                    ui.set_status("FACE VERIFIED")
                    face_ok = True
                    break

                # -------------------------
                # WRONG FACE
                # -------------------------
                else:
                    ui.set_status("FACE NOT MATCH")
                    time.sleep(0.5)

            # =========================
            # RESULT
            # =========================

            if not face_ok:

                reason = "Face Mismatch"

                print_access(full_name, user_type, "ACCESS DENIED", reason)

                send_to_arduino("IN:DENY:FACE_MISMATCH")

                time.sleep(2)
                continue

            else:
                ui.set_status("FACE VERIFIED")

        # =========================
        # ACCESS LOGIC
        # =========================
        # 🔥 NEW CHECK FIRST
        # =========================
        # MEMBER MEMBERSHIP CHECK ONLY
        # =========================
        if user_type == "Member":

            membership_ok = check_membership_status(
                user_id,
                full_name,
                user[0]["phone"]
            )

            if not membership_ok:

                ui.set_status("ACCESS EXPIRED")

                print_access(
                    full_name,
                    user_type,
                    "ACCESS DENIED",
                    "ACCESS EXPIRED"
                )

                send_to_arduino("IN:DENY:EXPIRED")

                time.sleep(2)
                continue

        # THEN normal logic
        result = check_time_in(user_id)
        current_time = datetime.now().strftime("%I:%M %p")

        if result["allowed"]:

            ui.set_status("ACCESS GRANTED")
            

            print_access(full_name, user_type, "ACCESS GRANTED")

            send_to_arduino(f"IN:ALLOW:{full_name}:{current_time}")

            passed = wait_for_entry()

            if passed:
                print("✅ PASSED")

                send_to_arduino("IN:LOCK")

                save_time_in(user_id)
                
                            
                # =========================
                # DAILY = ONE ENTRY ONLY
                # =========================
                execute_query("""
                    UPDATE members
                    SET monthly_expires = NOW()
                    WHERE id = %s
                    AND LOWER(membership_type) LIKE '%daily%'
                """, (user_id,))
                
                notify_attendance()
                check_tailgating("IN")
                

            else:
                print("❌ TIMEOUT")

                send_to_arduino("IN:LOCK")
                send_to_arduino("IN:DENY:TIMEOUT")

        else:

            reason = result["reason"]

            ui.set_status("ACCESS DENIED")

            print_access(full_name, user_type, "ACCESS DENIED", reason)

            send_to_arduino(f"IN:DENY:{reason}")
            

        time.sleep(2)
        
def has_unpaid_overtime(user_id):
    try:
        result = execute_query("""
            SELECT status, overtime_paid
            FROM locker_sessions
            WHERE user_id = %s
            ORDER BY start_time DESC
            LIMIT 1
        """, (user_id,), fetch=True)

        if not result:
            return False

        # 👉 list yan, kunin first row
        row = result[0]

        status = row["status"]
        paid = int(row["overtime_paid"] or 0)

        print("DEBUG:", status, paid)  # optional

        return status == "overtime" and paid == 0

    except Exception as e:
        print("[OVERTIME CHECK ERROR]", e)
        return False
        
# =========================
# OUT THREAD (Exit Lane)
# =========================
def out_lane_loop(out_fp):

    while system_state.system_running:

        if system_state.system_paused:
            time.sleep(0.2)
            continue

        fp_id = out_fp.verify()

        if fp_id is None:
            time.sleep(0.1)
            continue

        user = get_user_info_by_fp(fp_id)

        if not user:
            print("[OUT] Fingerprint not linked.")
            send_to_arduino("OUT:DENY:NOT_LINKED")
            time.sleep(1)
            continue

        user_id = user[0]["user_id"]
        full_name = user[0]["full_name"]

        user_type = "Member" if user_id.upper().startswith("M") else "Walkin"
        current_time = datetime.now().strftime("%I:%M %p")

        # =========================
        # 🔥 CHECK ACTIVE LOCKER
        # =========================
        if has_active_locker(user_id):

            print_access(full_name, user_type, "EXIT DENIED", "ACTIVE LOCKER")

            send_to_arduino("OUT:DENY:ACTIVE_LOCKER")
            time.sleep(2)
            continue

        # =========================
        # 🔥 NEW: CHECK OVERTIME
        # =========================
        if has_unpaid_overtime(user_id):

            print_access(full_name, user_type, "EXIT DENIED", "OVERTIME UNPAID")

            send_to_arduino("OUT:DENY:OVERTIME")

            time.sleep(2)
            continue

        # =========================
        # PROCESS EXIT (UPDATED)
        # =========================
        result = check_time_out(user_id)

        if result["allowed"]:

            print_access(full_name, user_type, "EXIT GRANTED")
            
            send_to_arduino(f"OUT:ALLOW:{full_name}:{current_time}")

            passed = wait_for_exit()

            if passed:
                print("✅ EXIT PASSED")

                send_to_arduino("OUT:LOCK")

                save_time_out(user_id)

                try:
                    release_locker(user_id)
                except:
                    pass

                notify_attendance()
                notify_locker()
                check_tailgating("OUT")
                

            else:
                print("❌ EXIT TIMEOUT")

                send_to_arduino("OUT:LOCK")
                send_to_arduino("OUT:DENY:TIMEOUT")

        else:

            reason = result["reason"]

            print_access(full_name, user_type, "EXIT DENIED", reason)

            send_to_arduino(
                f"OUT:DENY:{reason}"
            )

        time.sleep(2)
        
def has_active_locker(user_id):
    try:
        r = requests.get(
            "http://192.168.1.19:5001/api/check_locker",
            params={"user_id": user_id},
            headers={"X-API-KEY": "GYM_MASTER_2026"}
        )

        if r.status_code != 200:
            print("[API ERROR]", r.text)
            return False

        data = r.json()
        return data.get("active", False)

    except Exception as e:
        print("[ERROR CHECK LOCKER]", e)
        return False
        
from datetime import datetime

def print_access(name, user_type, status, reason=None):

    current_time = datetime.now().strftime("%I:%M %p")

    print("\n===================================")
    print(f"Name   : {name}")
    print(f"Time   : {current_time}")
    print(f"Type   : {user_type}")
    print(f"Status : {status}")

    if reason:
        print(f"Reason : {reason}")

    print("===================================\n")
        
# =========================
# MAIN SYSTEM LOOP
# =========================

def main():

    print("\n" + "="*35)
    print(" SMART GYM TURNSTILE SYSTEM")
    print(" AUTO MODE ACTIVE")
    print(" Commands: admin | quit")
    print("="*35 + "\n")

    # -------------------------
    # Initialize Hardware
    # -------------------------
    in_fp = InFingerprint()
    out_fp = OutFingerprint()

    init_serial("/dev/ttyACM0", 115200)

    # -------------------------
    # Initialize Camera
    # -------------------------
    picam2 = Picamera2()

    config = picam2.create_preview_configuration(
        main={"size": (1280,720), "format":"RGB888"},
        controls={"ScalerCrop": (0, 0, 3280, 2464)}
    )

    picam2.configure(config)
    picam2.start()

    ui = UIDisplay(picam2)
    ui.start()

    camera_manager.shared_camera = picam2

    face_recognizer = FaceRecognizer()

    # -------------------------
    # Start Lane Threads
    # -------------------------
    threading.Thread(
        target=in_lane_loop,
        args=(in_fp, face_recognizer, ui),
        daemon=True
    ).start()

    threading.Thread(
        target=out_lane_loop,
        args=(out_fp,),
        daemon=True
    ).start()
        # 🔥 START BYPASS MONITOR
    threading.Thread(
        target=monitor_bypass,
        daemon=True
    ).start()

    # -------------------------
    # Main Loop
    # -------------------------
    while system_state.system_running:

        # ❌ REMOVED: read_arduino() (handled by thread)

        # -------------------------
        # Handle Admin Request
        # -------------------------
        if system_state.admin_requested:

            system_state.system_paused = True

            ui.set_mode("ADMIN")
            ui.set_status("ADMIN MODE")
            ui.set_name("SYSTEM CONTROL")

            if verify_admin():
                print("\n--- ADMIN MODE ---\n")
                admin_menu(in_fp, out_fp, ui)

            system_state.admin_requested = False

            system_state.system_paused = False

            ui.set_mode("NORMAL")
            ui.set_status("SCAN FINGERPRINT")
            ui.set_name("")

            print("Returning to Auto Mode...\n")

        # -------------------------
        # Keyboard Commands
        # -------------------------
        if select.select([sys.stdin], [], [], 0)[0]:

            cmd = sys.stdin.readline().strip().lower()

            if cmd == "admin":
                system_state.admin_requested = True

            elif cmd == "quit":

                print("Shutting down...")
                system_state.system_running = False

                try:
                    picam2.stop()
                except:
                    pass

                sys.exit()

        time.sleep(0.05)


if __name__ == "__main__":
    main()
