import serial
import time

class GSMManager:
    def __init__(self, port="/dev/ttyUSB0", baudrate=9600):
        self.port = port
        self.baudrate = baudrate
        self.ser = None
        self.initialize_gsm()

    def initialize_gsm(self):
        try:
            self.ser = serial.Serial(self.port, baudrate=self.baudrate, timeout=1)
            time.sleep(1)
            print(f"GSM Connected on {self.port}")
        except Exception as e:
            print(f"GSM Connection Error: {e}")

    def send_notification(self, phone_number, message):
        if not self.ser:
            print("GSM not initialized. Reconnecting...")
            self.initialize_gsm()
            if not self.ser: return

        try:
            # Set to Text Mode
            self.ser.write(b'AT+CMGF=1\r\n')
            time.sleep(0.5)
            # Set Recipient
            cmd = f'AT+CMGS="{phone_number}"\r\n'
            self.ser.write(cmd.encode())
            time.sleep(0.5)
            # Send Message + Ctrl+Z
            self.ser.write(f'{message}\x1a'.encode())
            time.sleep(2) 
            print(f"? SMS Alert sent to {phone_number}")
        except Exception as e:
            print(f"? Failed to send SMS: {e}")

    def close(self):
        if self.ser:
            self.ser.close()
