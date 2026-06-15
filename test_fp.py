from pyfingerprint.pyfingerprint import PyFingerprint

f = PyFingerprint(
    '/dev/ttyUSB0',
    57600,
    0xFFFFFFFF,
    0x00000000
)

if not f.verifyPassword():
    print("Sensor error")
    exit()

for slot in [0, 3, 5]:
    try:
        f.deleteTemplate(slot)
        print(f"Deleted FP ID {slot}")
    except Exception as e:
        print(f"Failed FP ID {slot}: {e}")

print("Done")
