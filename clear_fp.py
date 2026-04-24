from biometrics.fingerprint.in_sensor import InFingerprint
from biometrics.fingerprint.out_sensor import OutFingerprint
import time

in_fp = InFingerprint()
time.sleep(2)
out_fp = OutFingerprint()
time.sleep(2)

in_fp.f.clearDatabase()
print("IN sensor cleared.")

out_fp.f.clearDatabase()
print("OUT sensor cleared.")