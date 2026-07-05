from pyfingerprint.pyfingerprint import PyFingerprint


def delete_fingerprint(fp_id):

    for port in [

        "/dev/fp_in",
        "/dev/fp_out"

    ]:

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

            print(
                f"[FP] Deleted slot {fp_id} from {port}"
            )

        except Exception as e:

            print(
                f"[FP] {port}:",
                e
            )

    return True