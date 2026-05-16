from pyfingerprint.pyfingerprint import PyFingerprint
from hardware.arduino_serial import send_to_arduino
import time


class OutFingerprint:

    def __init__(self, port='/dev/fp_out', baudrate=57600):

        while True:
            try:
                self.f = PyFingerprint(port, baudrate)

                if not self.f.verifyPassword():
                    raise ValueError("Fingerprint sensor password incorrect")

            
                break

            except Exception as e:
                print("OUT sensor init error:", e)
                print("Retrying OUT sensor in 2 seconds...")
                time.sleep(2)

    def verify(self, timeout=2):

        try:

            start = time.time()

            # =========================
            # WAIT FOR FINGER
            # =========================
            while not self.f.readImage():

                if time.time() - start > timeout:
                    return None

                time.sleep(0.02)

            print("📌 Finger detected")

            # =========================
            # CONVERT + SEARCH
            # =========================
            self.f.convertImage(0x01)

            positionNumber, accuracyScore = self.f.searchTemplate()

            self._wait_for_removal()

            # =========================
            # NO MATCH
            # =========================
            if positionNumber == -1:

                print("❌ ACCESS DENIED (no match)")

                send_to_arduino("OUT:DENY:NOT_LINKED")

                return None

            # =========================
            # VALID MATCH
            # =========================
            if accuracyScore >= 70:

                print("✅ ACCESS GRANTED")
                print("ID:", positionNumber)
                print("Score:", accuracyScore)

                return positionNumber

            # =========================
            # LOW CONFIDENCE
            # =========================
            else:

                print("❌ LOW CONFIDENCE")

                send_to_arduino("OUT:DENY:NOT_LINKED")

                return None

        except Exception as e:

            

            return None

    def _wait_for_finger(self, timeout=5):

        start = time.time()

        while True:
            try:
                if self.f.readImage():
                    return True
            except:
                return False

            if time.time() - start > timeout:
                return False

            time.sleep(0.05)

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