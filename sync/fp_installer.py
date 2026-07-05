from pyfingerprint.pyfingerprint import PyFingerprint


def hex_to_characteristics(hex_string):

    return [

        int(hex_string[i:i + 2], 16)

        for i in range(0, len(hex_string), 2)

    ]


def install_fingerprint(fp_id, fp_template):

    characteristics = hex_to_characteristics(
        fp_template
    )

    for port in [

        "/dev/fp_in",
        "/dev/fp_out"

    ]:

        print(f"[FP] Installing to {port}")

        sensor = PyFingerprint(
            port,
            57600
        )

        if not sensor.verifyPassword():

            raise Exception(
                f"{port}: Password invalid."
            )

        try:

            sensor.deleteTemplate(fp_id)

        except Exception:
            pass

        sensor.uploadCharacteristics(
            0x01,
            characteristics
        )

        sensor.storeTemplate(
            fp_id,
            0x01
        )

        print(f"[FP] Installed to {port}")

    return True