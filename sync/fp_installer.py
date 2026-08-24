def hex_to_characteristics(hex_string):

    return [
        int(hex_string[i:i + 2], 16)
        for i in range(0, len(hex_string), 2)
    ]


def install_fingerprint(fp_manager, fp_id, fp_template):

    characteristics = hex_to_characteristics(
        fp_template
    )

    print("[FP] Installing to IN")

    fp_manager.install_in(
        fp_id,
        characteristics
    )

    print("[FP] Installing to OUT")

    fp_manager.install_out(
        fp_id,
        characteristics
    )

    print("[FP] Fingerprint installed to IN and OUT")

    return True