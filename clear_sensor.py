from pyfingerprint.pyfingerprint import PyFingerprint

try:

    f = PyFingerprint('/dev/ttyUSB0', 57600)

    if not f.verifyPassword():
        raise ValueError("Sensor password error")

    print("Templates before:", f.getTemplateCount())

    f.clearDatabase()

    print("Sensor database cleared")

    print("Templates after:", f.getTemplateCount())

except Exception as e:

    print("Error:", e)
