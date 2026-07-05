from pyfingerprint.pyfingerprint import PyFingerprint

EXPECTED_FP_ID = 0

sensor = PyFingerprint(
    "/dev/fp_out",
    57600
)

if not sensor.verifyPassword():
    raise Exception("Fingerprint sensor password invalid.")

print("\n=== VERIFY TEST (OUT SENSOR) ===")

while True:

    print("\nPlace enrolled finger...")

    while not sensor.readImage():
        pass

    try:

        sensor.convertImage(0x01)

        fp_id, score = sensor.searchTemplate()

        print("\nReturned FP ID :", fp_id)
        print("Score          :", score)

        if fp_id == EXPECTED_FP_ID:

            print("\n✅ PASS")
            print("Fingerprint synchronization successful.")
            break

        else:

            print("\n❌ FAIL")
            print(f"Expected : {EXPECTED_FP_ID}")
            print(f"Detected : {fp_id}")

    except Exception as e:

        print("\nScan Error:", e)
        print("Try again...")