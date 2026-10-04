from db.connection import get_connection


def handle_payment_updated(payload):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        payment_type = payload.get("payment_type")
        member_id = payload.get("member_id")
        amount = payload.get("amount", 0)
        trainer_id = payload.get("trainer_id")

        # ==========================================
        # VALIDATION
        # ==========================================

        if not member_id:
            return {
                "success": False,
                "message": "member_id is required."
            }

        if not payment_type:
            return {
                "success": False,
                "message": "payment_type is required."
            }

        if amount is None:
            amount = 0

        # ==========================================
        # MEMBERSHIP PAYMENT
        # ==========================================

        if payment_type == "membership_fee":

            cursor.execute(
                """
                UPDATE members
                SET
                    membership_type=%s,
                    membership_expires=%s,
                    monthly_expires=%s
                WHERE id=%s
                """,
                (
                    payload.get("membership_type"),
                    payload.get("membership_expires"),
                    payload.get("monthly_expires"),
                    member_id
                )
            )

        # ==========================================
        # ACCESS PAYMENT
        # ==========================================

        elif payment_type == "access_fee":

            # Access payment does not need
            # membership fields.
            pass

        # ==========================================
        # TRAINER PAYMENT
        # ==========================================

        elif payment_type == "trainer_fee":

            if not trainer_id:

                return {
                    "success": False,
                    "message": "trainer_id is required for trainer_fee."
                }

        # ==========================================
        # UNKNOWN PAYMENT TYPE
        # ==========================================

        else:

            return {
                "success": False,
                "message": f"Unknown payment type: {payment_type}"
            }

        # ==========================================
        # PAYMENT RECORD
        # ==========================================

        cursor.execute(
            """
            INSERT INTO payments
            (
                user_id,
                payment_type,
                amount,
                trainer_id,
                paid_at
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s
            )
            """,
            (
                member_id,
                payment_type,
                amount,
                trainer_id,
                payload.get("paid_at")
            )
        )

        payment_id = cursor.lastrowid

        connection.commit()

        print(
            "\n========== PAYMENT HANDLER =========="
        )

        print(
            "Member ID:",
            member_id
        )

        print(
            "Payment Type:",
            payment_type
        )

        print(
            "Amount:",
            amount
        )

        print(
            "Trainer ID:",
            trainer_id
        )

        print(
            "Payment ID:",
            payment_id
        )

        print(
            "====================================\n"
        )

        return {

            "success": True,

            "message": "Payment synchronized.",

            "payment_id": payment_id,

            "member_id": member_id,

            "payment_type": payment_type,

            "amount": amount,

            "trainer_id": trainer_id

        }

    except Exception as e:

        connection.rollback()

        print(
            "[PAYMENT HANDLER ERROR]",
            str(e)
        )

        return {

            "success": False,

            "message": str(e)

        }

    finally:

        cursor.close()

        connection.close()
