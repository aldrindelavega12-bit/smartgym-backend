import RPi.GPIO as GPIO
import time
import requests

IR_IN = 17
IR_OUT = 27

GPIO.setmode(GPIO.BCM)

GPIO.setup(IR_IN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(IR_OUT, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# ================= CONFIG =================
TAILGATE_TIME = 3
DEBOUNCE = 0.3

API_URL = "http://192.168.1.19:5001"

# ================= STATE =================
scan_active_in = False
scan_active_out = False

tailgate_active_in = False
tailgate_active_out = False


# ================= ALERT =================
def send_alert(event, lane):
    try:
        data = {
            "event": event,
            "lane": lane,
            "time": time.strftime("%Y-%m-%d %H:%M:%S")
        }

        print("📡 Sending alert...", data)

        res = requests.post(
            f"{API_URL}/api/notify/security",
            json=data,
            timeout=3
        )

        print("📡 RESPONSE:", res.status_code, res.text)

    except Exception as e:
        print("❌ ALERT ERROR:", e)

# ================= FILTER =================
def stable_detect(pin):
    count = 0
    for _ in range(6):
        if GPIO.input(pin) == 0:
            count += 1
        time.sleep(0.005)
    return count >= 4


# ================= ENTRY =================
def wait_for_entry(timeout=10):

    global scan_active_in

    print("⏳ Waiting for ENTRY...")
    start = time.time()

    scan_active_in = True

    while time.time() - start < timeout:

        if stable_detect(IR_IN):

            print("✅ ENTRY DETECTED")

            while GPIO.input(IR_IN) == 0:
                time.sleep(0.01)

            time.sleep(DEBOUNCE)

            scan_active_in = False
            return True

    print("❌ ENTRY TIMEOUT")
    scan_active_in = False
    return False


# ================= EXIT =================
def wait_for_exit(timeout=10):

    global scan_active_out

    print("⏳ Waiting for EXIT...")
    start = time.time()

    scan_active_out = True

    while time.time() - start < timeout:

        if stable_detect(IR_OUT):

            print("✅ EXIT DETECTED")

            while GPIO.input(IR_OUT) == 0:
                time.sleep(0.01)

            time.sleep(DEBOUNCE)

            scan_active_out = False
            return True

    print("❌ EXIT TIMEOUT")
    scan_active_out = False
    return False


# ================= TAILGATING (FIXED) =================
def check_tailgating(lane):

    global tailgate_active_in, tailgate_active_out

    pin = IR_IN if lane == "IN" else IR_OUT

    print(f"⏱ 3s monitoring for {lane}...")

    if lane == "IN":
        tailgate_active_in = True
    else:
        tailgate_active_out = True

    start = time.time()
    last_state = 1  # HIGH

    while time.time() - start < TAILGATE_TIME:

        current = GPIO.input(pin)

        # 🔥 EDGE DETECTION (NEW PERSON)
        if last_state == 1 and current == 0:

            if stable_detect(pin):

                print(f"🚨 TAILGATING DETECTED ({lane})")
                send_alert("TAILGATING", lane)

                while GPIO.input(pin) == 0:
                    time.sleep(0.01)

                break

        last_state = current
        time.sleep(0.01)

    print(f"✅ {lane} WINDOW END")

    if lane == "IN":
        tailgate_active_in = False
    else:
        tailgate_active_out = False


# ================= BYPASS (FIXED EDGE) =================
def monitor_bypass():

    print("🚀 BYPASS MONITOR STARTED")

    last_in = 1
    last_out = 1

    while True:

        cur_in = GPIO.input(IR_IN)
        cur_out = GPIO.input(IR_OUT)

        # IN
        if not scan_active_in and not tailgate_active_in:
            if last_in == 1 and cur_in == 0:
                if stable_detect(IR_IN):
                    print("🚨 BYPASS DETECTED (IN)")
                    send_alert("BYPASS", "IN")

                    while GPIO.input(IR_IN) == 0:
                        time.sleep(0.01)

        # OUT
        if not scan_active_out and not tailgate_active_out:
            if last_out == 1 and cur_out == 0:
                if stable_detect(IR_OUT):
                    print("🚨 BYPASS DETECTED (OUT)")
                    send_alert("BYPASS", "OUT")

                    while GPIO.input(IR_OUT) == 0:
                        time.sleep(0.01)

        last_in = cur_in
        last_out = cur_out

        time.sleep(0.05)