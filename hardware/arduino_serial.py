import serial
import time

ser = None

def init_serial(port="/dev/ttyACM0", baudrate=115200):
    global ser
    try:
        print("Opening serial:", port)

        ser = serial.Serial(port, baudrate, timeout=1)

        # 🔥 TURN OFF DTR (IMPORTANT)
        ser.setDTR(False)
        time.sleep(1)

        ser.reset_input_buffer()

        print("✅ Serial READY (no reset)")

    except Exception as e:
        print("Serial error:", e)

def send_to_arduino(message):
    global ser

    if ser is None:
        print("Serial NONE")
        return

    try:
        print("[SEND]:", message)
        ser.write((message + "\n").encode())
        ser.flush()
    except Exception as e:
        print("Serial write error:", e)

def read_from_arduino():
    global ser

    if ser is None:
        return None

    try:
        if ser.in_waiting:
            line = ser.readline().decode(errors='ignore').strip()

            if line:
                print("🔥 SERIAL:", line)
                return line

    except Exception as e:
        print("Serial read error:", e)

    return None