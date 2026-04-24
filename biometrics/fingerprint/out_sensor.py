from pyfingerprint.pyfingerprint import PyFingerprint
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

    def verify(self, timeout=5):

        try:

            if not self._wait_for_finger(timeout):
                return None

            time.sleep(0.2)

            self.f.convertImage(0x01)

            result = self.f.searchTemplate()

            positionNumber = result[0]
            accuracyScore = result[1]

            self._wait_for_removal()

            if positionNumber == -1:
                return None

            # fingerprint range check
            if 50 <= accuracyScore <= 200:

                print("[OUT] Fingerprint recognized")
                print("Position:", positionNumber)
                print("Accuracy:", accuracyScore)

                return positionNumber

            else:

                print("[OUT] Fingerprint rejected")
                print("Accuracy:", accuracyScore)

                return None

        except Exception:

            time.sleep(0.3)

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