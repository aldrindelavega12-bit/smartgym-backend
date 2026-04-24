import serial
import time

# Gamitin natin ang nahanap mong port
port = "/dev/ttyUSB0"
ser = serial.Serial(port, baudrate=9600, timeout=1)

def send_at(command):
    print(f"Sending: {command}")
    ser.write((command + "\r\n").encode())
    time.sleep(1)
    response = ser.read_all().decode()
    print(f"Response:\n{response}")
    return response

print("--- GSM STATUS CHECK ---")
send_at("AT")          # Dapat mag-reply ng OK
send_at("AT+CPIN?")    # Dapat READY (ibig sabihin detected ang SIM)
send_at("AT+CSQ")      # Signal strength (Dapat 10-31 ang unang number)
send_at("AT+COPS?")    # Check kung anong network (Globe/Smart)

ser.close()
