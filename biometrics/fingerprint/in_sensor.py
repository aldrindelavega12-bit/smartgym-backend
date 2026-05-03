from pyfingerprint.pyfingerprint import PyFingerprint
from hardware.arduino_serial import init_serial, send_to_arduino, ser
import time


class InFingerprint:


    def __init__(self, port='/dev/fp_in', baudrate=57600):

        while True:
            try:

                self.f = PyFingerprint(port, baudrate)

                if not self.f.verifyPassword():
                    raise ValueError("Fingerprint sensor password incorrect")

                print("✅ IN Fingerprint Sensor Initialized")

                break

            except Exception as e:

                print("IN sensor init error:", e)
                print("Retrying IN sensor in 2 seconds...")
                time.sleep(2)


    # =========================
    # ENROLL FINGERPRINT
    # =========================
    def enroll(self):

        try:

            print("\n--- FINGERPRINT ENROLLMENT ---")

            input("Press ENTER to scan first fingerprint...")
            print("Place finger...")

            if not self._wait_for_finger(10):
                print("Timeout waiting for finger.")
                return None, None

            self.f.convertImage(0x01)

            # =========================
            # DUPLICATE CHECK
            # =========================
            result = self.f.searchTemplate()
            positionNumber = result[0]

            if positionNumber >= 0:
                print(f"⚠ Finger already registered at position {positionNumber}")
                self._wait_for_removal()
                return None, None

            print("Remove finger...")
            self._wait_for_removal()

            input("Press ENTER to scan same finger again...")
            print("Place same finger...")

            if not self._wait_for_finger(10):
                print("Timeout waiting for finger.")
                return None, None

            self.f.convertImage(0x02)

            if self.f.compareCharacteristics() == 0:
                print("Finger mismatch. Enrollment failed.")
                return None, None

            self.f.createTemplate()

            # =========================
            # STORE TEMPLATE
            # =========================
            positionNumber = self.f.storeTemplate()

            # =========================
            # 🔥 GET CHARACTERISTICS (FIXED LOCATION)
            # =========================
            characteristics = self.f.downloadCharacteristics(0x01)

            # 🔥 FIX: get only first 512 bytes
            characteristics = characteristics[:512]

            hex_template = ''.join(format(x, '02x') for x in characteristics)

            print("LEN RAW:", len(characteristics))   # 512
            print("LEN HEX:", len(hex_template))      # 1024    # dapat 1024

            print(f"✅ Fingerprint enrolled at position: {positionNumber}")

            self._wait_for_removal()

            return positionNumber, hex_template

        except Exception as e:

            print("Enrollment error:", e)

            return None, None


    # =========================
    # VERIFY FINGERPRINT
    # =========================
    def verify(self, timeout=2):   # 🔥 from 5 → 2 seconds

        try:

            start = time.time()
            

            # =========================
            # WAIT FOR FINGER (FAST)
            # =========================
            while not self.f.readImage():

                if time.time() - start > timeout:
                    return None

                time.sleep(0.02)   # 🔥 faster polling

            print("📌 Finger detected")

            # =========================
            # CONVERT + SEARCH (NO DELAY)
            # =========================
            self.f.convertImage(0x01)

            positionNumber, accuracyScore = self.f.searchTemplate()

            self._wait_for_removal()

            # =========================
            # RESULT (FAST DECISION)
            # =========================
            if positionNumber == -1:
                print("❌ ACCESS DENIED (no match)")

                send_to_arduino(f"IN:DENY:NOT_LINKED")
                

                return None

            if accuracyScore >= 70:   # 🔥 simplified condition

                print("✅ ACCESS GRANTED")
                print("ID:", positionNumber)
                print("Score:", accuracyScore)

                # 👉 send to Arduino (GRANTED)
                # serial.write(b'GRANTED\n')

                return positionNumber

            else:
                print("❌ LOW CONFIDENCE")

                send_to_arduino("OUT:DENY:NOT_LINKED")

                return None

        except Exception as e:
            print("Verify error:", e)
            return None



    def _wait_for_removal(self, timeout=3):

        start = time.time()

        while True:

            try:

                if not self.f.readImage():
                    return

            except:
                return

            if time.time() - start > timeout:
                return

            time.sleep(0.05)