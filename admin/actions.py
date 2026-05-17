from db.connection import execute_query
from biometrics.fingerprint.in_sensor import InFingerprint
from biometrics.fingerprint.template_sync import TemplateSync
from biometrics.face.capture import capture_faces
from config import camera_manager
from datetime import datetime, time as dt_time
from biometrics.face.train import train_faces

import os
import cv2
import shutil
import system_state
import time

import requests
import threading

CLOUD_API = "https://smartgym-api-ia2e.onrender.com"

# ==============================
# ADD MEMBER
# ==============================
import cv2
import time

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)

# ==============================
# CLOUD SYNC
# ==============================
def sync_member_cloud(member_data):

    try:

        requests.post(
            f"{CLOUD_API}/api/sync_member",
            json=member_data,
            timeout=3
        )

        print("☁️ MEMBER SYNCED")

    except Exception as e:

        print("SYNC MEMBER ERROR:", e)


def delete_member_cloud(user_id):

    try:

        requests.post(
            f"{CLOUD_API}/api/delete_member",
            json={
                "user_id": user_id
            },
            timeout=3
        )

        print("☁️ MEMBER DELETED CLOUD")

    except Exception as e:

        print("DELETE CLOUD ERROR:", e)
        
def sync_walkin_cloud(walkin_data):

    try:

        requests.post(
            f"{CLOUD_API}/api/sync_walkin",
            json=walkin_data,
            timeout=3
        )

        print("☁️ WALKIN SYNCED")

    except Exception as e:

        print("SYNC WALKIN ERROR:", e)


def sync_payment_cloud(payment_data):

    try:

        requests.post(
            f"{CLOUD_API}/api/sync_payment",
            json=payment_data,
            timeout=3
        )

        print("☁️ PAYMENT SYNCED")

    except Exception as e:

        print("SYNC PAYMENT ERROR:", e)
        
def add_member(in_fp, out_fp, ui):

    import os
    import time
    import cv2
    import system_state
    from biometrics.fingerprint.template_sync import TemplateSync

    system_state.system_paused = True

    # =========================
    # MEMBER INFO
    # =========================
    ui.set_mode("ADMIN")
    ui.set_status("ENTER MEMBER INFO")
    ui.set_name("")

    full_name = input("Enter Full Name: ")
    phone_number = input("Enter Phone Number: ")

    # =========================
    # FINGERPRINT
    # =========================
    print("\nStarting fingerprint enrollment...")
    ui.set_status("SCAN FINGERPRINT")

    fp_id, hex_template = in_fp.enroll()

    if fp_id is None:
        print("❌ Enrollment failed.")
        system_state.system_paused = False
        return

    print(f"Fingerprint enrolled at position: {fp_id}")

    try:
        sync = TemplateSync(in_fp.f, out_fp.f)
        sync.sync_template(fp_id)
        print("✅ Synced to OUT sensor.")
    except Exception as e:
        print("❌ Sync failed:", e)
        system_state.system_paused = False
        return

    # =========================
    # GENERATE ID
    # =========================
    last = execute_query(
        "SELECT id FROM members ORDER BY id DESC LIMIT 1",
        fetch=True
    )

    new_id = f"M{int(last[0]['id'][1:]) + 1:04d}" if last else "M0001"

    print("DEBUG MEMBER ID:", new_id)

    # =========================
    # PREPARE DATASET
    # =========================
    dataset_path = os.path.abspath("datasets/faces")
    os.makedirs(dataset_path, exist_ok=True)

    save_path = os.path.join(dataset_path, new_id)
    os.makedirs(save_path, exist_ok=True)

    print("Saving dataset to:", save_path)

    # =========================
    # FACE ENROLLMENT
    # =========================
    print("\nStarting face enrollment...")

    ui.set_mode("ENROLL")
    ui.set_name(full_name)
    ui.camera_active = True   # 🔥 ensure camera ON

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    captured = 0

    while captured < 5:

        # ---------------------
        # WAIT FOR FRAME
        # ---------------------
        with ui.frame_lock:
            frame = None if ui.frame is None else ui.frame.copy()

        if frame is None:
            time.sleep(0.05)
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(
            gray, 1.3, 5, minSize=(60,60)
        )

        if len(faces) == 0:
            ui.set_status("NO FACE DETECTED")
            time.sleep(0.3)
            continue

        # ---------------------
        # COUNTDOWN
        # ---------------------
        for i in [3, 2, 1]:
            ui.set_status(f"CAPTURE {captured+1}/5 IN {i}")
            start = time.time()

            while time.time() - start < 1:
                time.sleep(0.01)

        # ---------------------
        # FINAL FRAME (SAFE)
        # ---------------------
        with ui.frame_lock:
            frame = None if ui.frame is None else ui.frame.copy()

        if frame is None:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(
            gray, 1.3, 5, minSize=(60,60)
        )

        if len(faces) == 0:
            ui.set_status("FACE LOST")
            time.sleep(0.3)
            continue

        # largest face
        faces = sorted(faces, key=lambda x: x[2]*x[3], reverse=True)
        (x,y,w,h) = faces[0]

        face_img = gray[y:y+h, x:x+w]
        face_img = cv2.resize(face_img, (100,100))

        filename = os.path.join(save_path, f"{captured+1}.jpg")
        cv2.imwrite(filename, face_img)

        captured += 1

        ui.set_status(f"CAPTURED {captured}/5")
        print(f"Captured {captured}/5 → {filename}")

        time.sleep(0.5)

    print("✅ Face capture complete.")
    train_faces()

    # =========================
    # SAVE MEMBER
    # =========================
    execute_query(
        """
        INSERT INTO members (id, full_name, phone_number, fingerprint_template)
        VALUES (%s,%s,%s,%s)
        """,
        (new_id, full_name, phone_number, hex_template)
    )

    
    execute_query(
    "INSERT INTO fp_templates (user_id, fp_id, template) VALUES (%s,%s,%s)",
    (new_id, fp_id, hex_template)
)

    print(f"✅ Member {new_id} registered.")
    
    threading.Thread(
        target=sync_member_cloud,
        args=({
            "id": new_id,
            "full_name": full_name,
            "phone_number": phone_number,
            "fingerprint_template": hex_template
        },),
        daemon=True
    ).start()

    # =========================
    # SUCCESS UI
    # =========================
    ui.set_status("ENROLL SUCCESS")
    time.sleep(2)

    ui.set_mode("ADMIN")

    system_state.system_paused = False

# ==============================
# ADD WALKIN
# ==============================
def add_walkin(in_fp, out_fp, ui):

    import system_state

    # 🔥 PAUSE SYSTEM (IMPORTANT)
    system_state.system_paused = True

    full_name = input("Enter Full Name: ")
    phone_number = input("Enter Phone Number: ")

    print("Start fingerprint enrollment...")

    fp_id, hex_template = in_fp.enroll()

    if fp_id is None:
        print("Enrollment failed")
        system_state.system_paused = False   # 🔥 RESUME
        return

    print("Fingerprint enrolled at position:", fp_id)

    # -------------------------
    # SYNC TEMPLATE TO OUT SENSOR
    # -------------------------
    try:
        from biometrics.fingerprint.template_sync import TemplateSync

        sync = TemplateSync(in_fp.f, out_fp.f)
        sync.sync_template(fp_id)

        print("Template synced to OUT sensor.")

    except Exception as e:
        print("OUT sensor sync failed:", e)

    # -------------------------
    # Generate walkin ID
    # -------------------------
    last = execute_query(
        "SELECT id FROM walkins ORDER BY id DESC LIMIT 1",
        fetch=True
    )

    if last:
        number = int(last[0]["id"][1:]) + 1
    else:
        number = 1

    walkin_id = f"W{number:04d}"

    # -------------------------
    # Save walkin
    # -------------------------
    execute_query(
        """
        INSERT INTO walkins 
        (id, full_name, phone_number, visit_date, fingerprint_template, fp_id)
        VALUES (%s,%s,%s,CURDATE(),%s,%s)
        """,
        (walkin_id, full_name, phone_number, hex_template, fp_id)
    )

    # -------------------------
    # AUTO LINK fingerprint
    # -------------------------
    execute_query(
        """
        INSERT INTO fp_templates (user_id, fp_id, template)
        VALUES (%s,%s,%s)
        """,
        (walkin_id, fp_id, hex_template)
    )

    print("Fingerprint linked automatically.")
    print("Walkin created:", walkin_id)
    threading.Thread(
        target=sync_walkin_cloud,
        args=({
            "id": walkin_id,
            "full_name": full_name,
            "phone_number": phone_number,
            "fingerprint_template": hex_template,
            "fp_id": fp_id
        },),
        daemon=True
    ).start()

    # 🔥 RESUME SYSTEM
    system_state.system_paused = False
# ==============================
# PAYMENT
# ==============================
def process_payment():

    print("\n[PAYMENT]")
    print("1. Member")
    print("2. Walkin")
    print("3. Cancel")

    choice = input("Select option: ")

    from datetime import datetime, timedelta
    now = datetime.now()

    # MEMBER
    # MEMBER
    if choice == "1":

        print("1. Membership + Monthly")
        print("2. Membership + Daily")
        print("3. Membership Only")
        print("4. Monthly Only")
        print("5. Daily Only")

        pay_type = input("Select option: ")
        user_id = input("Enter Member ID: ").upper()

        # =========================
        # GET MEMBER
        # =========================
        member = execute_query(
            """
            SELECT membership_expires, monthly_expires
            FROM members
            WHERE id=%s
            """,
            (user_id,),
            fetch=True
        )

        if not member:
            print("❌ Member not found.")
            return

        member = member[0]

        current_membership = member["membership_expires"]
        current_monthly = member["monthly_expires"]

        # =========================
        # DEFAULT VALUES
        # =========================
        membership_expiry = current_membership
        monthly_expiry = current_monthly
        membership_type = ""

        # =========================
        # MEMBERSHIP + MONTHLY
        # =========================
        if pay_type == "1":

            # membership
            if not current_membership or current_membership < now:
                membership_expiry = now + timedelta(days=365)
            else:
                membership_expiry = current_membership + timedelta(days=365)

            # monthly
            if not current_monthly or current_monthly < now:
                monthly_expiry = now + timedelta(days=30)
            else:
                monthly_expiry = current_monthly + timedelta(days=30)

            membership_type = "membership-monthly"

        # =========================
        # MEMBERSHIP + DAILY
        # =========================
        elif pay_type == "2":

            # membership
            if not current_membership or current_membership < now:
                membership_expiry = now + timedelta(days=365)
            else:
                membership_expiry = current_membership + timedelta(days=365)

            # daily
            if not current_monthly or current_monthly < now:
                monthly_expiry = datetime.combine(
                    now.date(),
                    dt_time(23, 59, 59)
                )
            else:
                monthly_expiry = current_monthly + timedelta(days=1)

            membership_type = "membership-daily"

        # =========================
        # MEMBERSHIP ONLY
        # =========================
        elif pay_type == "3":

            if not current_membership or current_membership < now:
                membership_expiry = now + timedelta(days=365)
            else:
                membership_expiry = current_membership + timedelta(days=365)

            membership_type = "membership"

        # =========================
        # MONTHLY ONLY
        # =========================
        elif pay_type == "4":

            # must have active membership
            if not current_membership or current_membership < now:
                print("❌ No active membership.")
                return

            if not current_monthly or current_monthly < now:
                monthly_expiry = now + timedelta(days=30)
            else:
                monthly_expiry = current_monthly + timedelta(days=30)

            membership_type = "monthly"

        # =========================
        # DAILY ONLY
        # =========================
        elif pay_type == "5":

            # must have active membership
            if not current_membership or current_membership < now:
                print("❌ No active membership.")
                return

            if not current_monthly or current_monthly < now:
                monthly_expiry = datetime.combine(
                    now.date(),
                    dt_time(23, 59, 59)
                )
            else:
                monthly_expiry = current_monthly + timedelta(days=1)

            membership_type = "daily"

        else:
            print("Invalid option.")
            return

        # =========================
        # UPDATE DATABASE
        # =========================
        execute_query(
            """
            UPDATE members 
            SET membership_expires=%s,
                monthly_expires=%s,
                membership_type=%s
            WHERE id=%s
            """,
            (
                membership_expiry,
                monthly_expiry,
                membership_type,
                user_id
            )
        )

        # =========================
        # SAVE PAYMENT
        # =========================
        execute_query(
            """
            INSERT INTO payments 
            (user_id, payment_type, amount)
            VALUES (%s,%s,%s)
            """,
            (
                user_id,
                membership_type.upper(),
                0
            )
        )

        # =========================
        # DISPLAY RESULT
        # =========================
        print("\n✅ PAYMENT RECORDED")
        
        # ==============================
        # SYNC UPDATED MEMBER TO CLOUD
        # ==============================
        member = execute_query(
            """
            SELECT *
            FROM members
            WHERE id=%s
            """,
            (user_id,),
            fetch=True
        )

        if member:

            member = member[0]

            threading.Thread(
                target=sync_member_cloud,
                args=({
                    "id": member["id"],
                    "full_name": member["full_name"],
                    "phone_number": member["phone_number"],
                    "fingerprint_template": member["fingerprint_template"],
                    "membership_type": member["membership_type"],
                    "membership_expires": str(member["membership_expires"]) if member["membership_expires"] else None,
                    "monthly_expires": str(member["monthly_expires"]) if member["monthly_expires"] else None
                },),
                daemon=True
            ).start()
        
        threading.Thread(
            target=sync_payment_cloud,
            args=({
                "user_id": user_id,
                "payment_type": membership_type.upper(),
                "amount": 0
            },),
            daemon=True
        ).start()

        print(f"Member ID: {user_id}")
        print(f"Type: {membership_type}")

        if membership_expiry:
            print("\n--- MEMBERSHIP ---")
            print(
                f"Valid Until: "
                f"{membership_expiry.strftime('%Y-%m-%d %H:%M:%S')}"
            )

        if monthly_expiry:
            print("\n--- ACCESS ---")
            print(
                f"Valid Until: "
                f"{monthly_expiry.strftime('%Y-%m-%d %H:%M:%S')}"
            )

    # WALKIN
    elif choice == "2":

        user_id = input("Enter Walkin ID: ").upper()

        end_of_day = datetime.combine(datetime.today(), dt_time(23, 59, 59))

        execute_query(
            "INSERT INTO payments (user_id, payment_type, amount, paid_at) VALUES (%s,%s,%s,NOW())",
            (user_id, "WALKIN", 0)
        )
        

        print("Walkin marked as paid.")
        
        threading.Thread(
            target=sync_payment_cloud,
            args=({
                "user_id": user_id,
                "payment_type": "WALKIN",
                "amount": 0
            },),
            daemon=True
        ).start()

        locker = input("Will use locker? (yes/no): ")

        if locker.lower() == "yes":

            # Get available lockers
            available = execute_query(
                "SELECT locker_number FROM lockers WHERE status='AVAILABLE'",
                fetch=True
            )

            if not available:
                print("No lockers available.")
                return

            print("\nAvailable Lockers:")
            for l in available:
                print(f"Locker {l['locker_number']}")

            selected = int(input("Select locker number: "))

            # Check if selected locker is available
            # =========================
            # CHECK EXISTING LOCKER
            # =========================
            existing = execute_query(
                "SELECT * FROM locker_sessions WHERE user_id=%s AND status='active'",
                (user_id,),
                fetch=True
            )

            if existing:
                print(f"⚠ User already has locker {existing[0]['locker_number']}")
                return

            # Assign locker
            execute_query(
                "UPDATE lockers SET status='OCCUPIED' WHERE locker_number=%s",
                (selected,)
            )

            execute_query(
                """
                INSERT INTO locker_sessions (user_id, locker_number, start_time, status)
                VALUES (%s,%s,NOW(),'reserved')
                """,
                (user_id, selected)
            )        

            print(f"Locker {selected} assigned successfully.")
    
    else:
        print("Cancelled.")
        
def release_locker(user_id):

    result = execute_query(
        "SELECT locker_number FROM locker_sessions WHERE user_id=%s AND end_time IS NULL",
        (user_id,),
        fetch=True
    )

    if not result:
        return

    locker = result[0]["locker_number"]

    # close locker session
    execute_query(
        "UPDATE locker_sessions SET end_time=NOW() WHERE user_id=%s AND end_time IS NULL",
        (user_id,)
    )

    # make locker available again
    execute_query(
        "UPDATE lockers SET status='AVAILABLE' WHERE locker_number=%s",
        (locker,)
    )

    print(f"Locker {locker} released.")

def pay_locker_overtime():

    from datetime import datetime, timedelta
    import math

    LOCKER_ALLOWED_HOURS = 3

    user_id = input("Enter User ID (Member or Walkin): ").upper()

    locker = execute_query(
        """
        SELECT locker_number, start_time, overtime_paid 
        FROM locker_sessions
        WHERE user_id=%s 
        AND status='overtime'
        AND overtime_paid=0
        ORDER BY start_time DESC
        LIMIT 1
        """,
        (user_id,),
        fetch=True
    )

    if not locker:
        print("No unpaid overtime found.")
        return

    locker = locker[0]

    locker_number = locker["locker_number"]
    start_time = locker["start_time"]
    overtime_paid = int(locker["overtime_paid"] or 0)

    allowed_time = start_time + timedelta(hours=LOCKER_ALLOWED_HOURS)

    overtime_duration = datetime.now() - allowed_time
    overtime_minutes = int(overtime_duration.total_seconds() / 60)

    overtime_fee = math.ceil(overtime_minutes / 2)

    print("\n--- LOCKER OVERTIME DETAILS ---")
    print(f"Locker Number : {locker_number}")
    print(f"Overtime      : {overtime_minutes} minutes")
    print(f"Overtime Fee  : PHP {overtime_fee}")
    print("--------------------------------")

    confirm = input("Pay locker overtime? (yes/no): ")

    if confirm.lower() != "yes":
        print("Payment cancelled.")
        return

    execute_query(
        "UPDATE locker_sessions SET overtime_paid=1 WHERE user_id=%s AND status='overtime'",
        (user_id,)
    )

    execute_query(
        "INSERT INTO payments (user_id, payment_type, amount) VALUES (%s,%s,%s)",
        (user_id, "LOCKER_OVERTIME", overtime_fee)
    )

    print("Locker overtime payment recorded successfully.")
    
# ==============================
# VIEW MEMBERS
# ==============================
def view_members():

    members = execute_query("SELECT * FROM members", fetch=True)

    for m in members:
        print(m)


# ==============================
# VIEW WALKINS
# ==============================
def view_walkins():

    walkins = execute_query("SELECT * FROM walkins", fetch=True)

    for w in walkins:
        print(w)


# ==============================
# DELETE MEMBER
# ==============================
def delete_member(in_fp, out_fp):

    member_id = input("Enter Member ID: ").strip().upper()

    data = execute_query(
        "SELECT * FROM members WHERE id=%s",
        (member_id,),
        fetch=True
    )

    if not data:
        print("❌ Member not found.")
        return

    confirm = input(f"Delete member {member_id}? (y/n): ").lower()

    if confirm != "y":
        print("Cancelled.")
        return

    # fingerprint delete
    fp = execute_query(
        "SELECT fp_id FROM fp_templates WHERE user_id=%s",
        (member_id,),
        fetch=True
    )

    if fp:

        fp_id = fp[0]["fp_id"]

        try:
            in_fp.f.deleteTemplate(fp_id)
            out_fp.f.deleteTemplate(fp_id)
        except:
            pass

        execute_query(
            "DELETE FROM fp_templates WHERE user_id=%s",
            (member_id,)
        )

    # face dataset delete
    import shutil, os

    face_path = f"datasets/faces/{member_id}"

    if os.path.exists(face_path):
        shutil.rmtree(face_path)

    execute_query(
        "DELETE FROM members WHERE id=%s",
        (member_id,)
    )

    print(f"✅ Member {member_id} deleted.")
    
    threading.Thread(
        target=delete_member_cloud,
        args=(member_id,),
        daemon=True
    ).start()
# ==============================
# DELETE WALKIN
# ==============================
def delete_walkin(in_fp, out_fp):

    walkin_id = input("Enter Walkin ID: ").strip().upper()

    data = execute_query(
        "SELECT * FROM walkins WHERE id=%s",
        (walkin_id,),
        fetch=True
    )

    if not data:
        print("❌ Walkin not found.")
        return

    confirm = input(f"Delete walkin {walkin_id}? (y/n): ").lower()

    if confirm != "y":
        print("Cancelled.")
        return

    fp = execute_query(
        "SELECT fp_id FROM fp_templates WHERE user_id=%s",
        (walkin_id,),
        fetch=True
    )

    if fp:

        fp_id = fp[0]["fp_id"]

        try:
            in_fp.f.deleteTemplate(fp_id)
            out_fp.f.deleteTemplate(fp_id)
        except:
            pass

        execute_query(
            "DELETE FROM fp_templates WHERE user_id=%s",
            (walkin_id,)
        )

    execute_query(
        "DELETE FROM walkins WHERE id=%s",
        (walkin_id,)
    )

    print(f"✅ Walkin {walkin_id} deleted.")
    
    threading.Thread(
        target=delete_walkin_cloud,
        args=(walkin_id,),
        daemon=True
    ).start()
# ==============================
# CLEAR FINGERPRINT
# ==============================
def clear_fingerprint(in_fp, out_fp):

    user_id = input("Enter Member/Walkin ID: ").strip().upper()

    data = execute_query(
        "SELECT fp_id FROM fp_templates WHERE user_id=%s",
        (user_id,),
        fetch=True
    )

    if not data:
        print("❌ No fingerprint enrolled for this user.")
        return

    fp_id = data[0]["fp_id"]

    confirm = input(f"Clear fingerprint for {user_id}? (y/n): ").lower()

    if confirm != "y":
        print("Cancelled.")
        return

    try:

        in_fp.f.deleteTemplate(fp_id)
        out_fp.f.deleteTemplate(fp_id)

        execute_query(
            "DELETE FROM fp_templates WHERE user_id=%s",
            (user_id,)
        )

        print(f"✅ Fingerprint cleared for {user_id}")

    except Exception as e:

        print("Error clearing fingerprint:", e)
        
