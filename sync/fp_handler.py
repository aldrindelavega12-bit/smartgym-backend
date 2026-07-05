from sync.fp_installer import install_fingerprint


def handle_fp_sync(payload):

    user_id = payload["user_id"]

    fp_id = payload["fp_id"]

    fp_template = payload["fp_template"]

    print("\n========== FP INSTALL ==========")
    print("User ID :", user_id)
    print("FP ID   :", fp_id)

    install_fingerprint(
        fp_id,
        fp_template
    )

    return {

        "success": True,

        "message": "Fingerprint installed."

    }