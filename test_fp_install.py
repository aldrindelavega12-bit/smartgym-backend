from pyfingerprint.pyfingerprint import PyFingerprint


def hex_to_characteristics(hex_string):

    return [

        int(hex_string[i:i+2], 16)

        for i in range(0, len(hex_string), 2)

    ]


# =====================================
# PASTE FP_SYNC PAYLOAD HERE
# =====================================

USER_ID = "W0001"

FP_ID = 1

FP_TEMPLATE = "03035d2700012001740000000000000000000000000000000000000000000000000000000000000000000000000000001200000085000c3300033fffffffffffbbfbfbaaaaaaaaa99996659559555555565401100000040101010101010101010101010101010101010101010101010101010101010101010101010101010101730b505e410dc01e4716805e2020459e1929dc7e4a2f005e3bb8035e553b6bde548b259f75928fbf551b2b5f121e5cdf35a783df4b2b191f3b2d5b3f23ad85ff31adc41f6cb293bf23b4057f2c345c7f323c447f3c1f839c61a8e9bc562f163c5b31aa1c4d13299d5316ea3d36a21b7d2a0adcfa268cc5fa6c1c26ba57a2eafa6a1e52fb158a46980c8bc5d85aa616785727ea58118a5cf94e8696560000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003035c2c0001200174000000000000000000000000000000000000000000000000000000000000000000000000000000130001007b000c0f30ccf3ffffffffbffbeeaaaa9aa6a9a99959595555555510540000004000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"


# =====================================
# Convert HEX -> Characteristics
# =====================================

characteristics = hex_to_characteristics(
    FP_TEMPLATE
)

print("HEX Length :", len(FP_TEMPLATE))
print("BYTE Length:", len(characteristics))


# =====================================
# Connect IN Sensor
# =====================================

fp_in = PyFingerprint(
    "/dev/fp_in",
    57600
)

if not fp_in.verifyPassword():

    raise Exception(
        "IN sensor password failed."
    )


# =====================================
# Connect OUT Sensor
# =====================================

fp_out = PyFingerprint(
    "/dev/fp_out",
    57600
)

if not fp_out.verifyPassword():

    raise Exception(
        "OUT sensor password failed."
    )


# =====================================
# INSTALL TO IN
# =====================================

print("\nInstalling to IN...")

fp_in.uploadCharacteristics(
    0x01,
    characteristics
)

fp_in.storeTemplate(
    FP_ID,
    0x01
)

print("IN Installed ✔")


# =====================================
# INSTALL TO OUT
# =====================================

print("\nInstalling to OUT...")

fp_out.uploadCharacteristics(
    0x01,
    characteristics
)

fp_out.storeTemplate(
    FP_ID,
    0x01
)

print("OUT Installed ✔")


print("\nDONE")