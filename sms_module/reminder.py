import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import mysql.connector
from datetime import date
from sms_module.sms import send_sms

DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "smartgym",
    "password": "smartgym123",
    "database": "smart_gym_db"
}

db = mysql.connector.connect(**DB_CONFIG)
cursor = db.cursor(dictionary=True)

today = date.today()

cursor.execute("SELECT * FROM members")
members = cursor.fetchall()

for m in members:
    phone = m['phone_number']
    name = m['full_name']
    last_sent = m.get('last_sms_sent')

    if not phone:
        continue

    # ❌ anti-spam (once per day)
    if last_sent == today:
        continue

    sent = False

    # 🔵 MONTHLY
    if m['monthly_expires']:
        expiry = m['monthly_expires'].date()
        days_left = (expiry - today).days

        if days_left <= 1:
            message = f"Hello {name}, your monthly gym membership is about to expire. - SMARTGYM"
            if send_sms(phone, message):
                sent = True

    # 🟣 YEARLY
    elif m['membership_expires']:
        expiry = m['membership_expires'].date()
        days_left = (expiry - today).days

        if days_left <= 1:
            message = f"Hello {name}, your annual gym membership is about to expire. - SMARTGYM"
            if send_sms(phone, message):
                sent = True

    # ✅ UPDATE DB
    if sent:
        cursor.execute(
            "UPDATE members SET last_sms_sent=%s WHERE id=%s",
            (today, m['id'])
        )
        db.commit()

print("✅ Reminder check complete")