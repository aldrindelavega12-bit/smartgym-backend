import threading
from biometrics.fingerprint.in_sensor import InFingerprint
from biometrics.fingerprint.out_sensor import OutFingerprint


class FingerprintManager:

    def __init__(self):
        print("[FP MANAGER] Initializing fingerprint sensors...")

        self.in_fp = InFingerprint()
        self.out_fp = OutFingerprint()

        self.in_lock = threading.Lock()
        self.out_lock = threading.Lock()

        print("[FP MANAGER] Ready")

    # =========================
    # IN SENSOR
    # =========================

    def verify_in(self):
        with self.in_lock:
            return self.in_fp.verify()
    def install_in(self, fp_id, characteristics):

        with self.in_lock:

            print(f"[FP DEBUG] IN delete slot {fp_id}")

            try:
                self.in_fp.f.deleteTemplate(fp_id)
                print("[FP DEBUG] IN delete OK")

            except Exception as e:
                print("[FP DEBUG] IN delete failed:", e)

            print("[FP DEBUG] Uploading characteristics...")
            print("[FP DEBUG] Characteristics length:", len(characteristics))

            self.in_fp.f.uploadCharacteristics(
                0x01,
                characteristics
            )

            print("[FP DEBUG] Upload SUCCESS")

            result = self.in_fp.f.storeTemplate(
                fp_id,
                0x01
            )

            print("[FP DEBUG] STORE SUCCESS:", result)

            return result


    def delete_in(self, fp_id):

        with self.in_lock:

            print(f"[FP DEBUG] IN delete slot {fp_id}")

            result = self.in_fp.f.deleteTemplate(fp_id)

            print("[FP DEBUG] IN delete SUCCESS")

            return result
            
    
    def delete_in(self, fp_id):

        with self.in_lock:
            self.in_fp.f.deleteTemplate(fp_id)

    # =========================
    # OUT SENSOR
    # =========================

    def verify_out(self):
        with self.out_lock:
            return self.out_fp.verify()
    def install_out(self, fp_id, characteristics):

        with self.out_lock:

            print(f"[FP DEBUG] OUT delete slot {fp_id}")

            try:
                self.out_fp.f.deleteTemplate(fp_id)
                print("[FP DEBUG] OUT delete OK")

            except Exception as e:
                print("[FP DEBUG] OUT delete failed:", e)

            print("[FP DEBUG] OUT uploading characteristics...")
            print("[FP DEBUG] Characteristics length:", len(characteristics))

            self.out_fp.f.uploadCharacteristics(
                0x01,
                characteristics
            )

            print("[FP DEBUG] OUT upload SUCCESS")

            result = self.out_fp.f.storeTemplate(
                fp_id,
                0x01
            )

            print("[FP DEBUG] OUT STORE SUCCESS:", result)

            return result


    def delete_out(self, fp_id):

        with self.out_lock:

            print(f"[FP DEBUG] OUT delete slot {fp_id}")

            result = self.out_fp.f.deleteTemplate(fp_id)

            print("[FP DEBUG] OUT delete SUCCESS")

            return result
