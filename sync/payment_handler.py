
from db.connection import get_connection


def handle_payment_updated(payload):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        payment_type = str(
            payload.get("payment_type") or ""
        ).strip().lower()

        member_id = payload.get("member_id")
        amount = payload.get("amount", 0)
        trainer_id = payload.get("trainer_id")
        paid_at = payload.get("paid_at")

        membership_type = payload.get("membership_type")
        membership_expires = payload.get("membership_expires")
        monthly_expires = payload.get("monthly_expires")

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

        try:
            amount = float(amount or 0)
        except (TypeError, ValueError):
            return {
                "success": False,
                "message": "Invalid payment amount."
            }

        if amount < 0:
            return {
                "success": False,
                "message": "Payment amount cannot be negative."
            }

        # ==========================================
        # SUPPORTED PAYMENT TYPES
        # ==========================================

        supported_types = {
            "membership",
            "membership_fee",
            "access_fee",
            "trainer_fee",
            "membership-only",
            "membership-monthly",
            "membership-daily",
            "daily",
            "monthly"
        }

        if payment_type not in supported_types:
            return {
                "success": False,
                "message": (
                    f"Unknown payment type: "
                    f"{payload.get('payment_type')}"
                )
            }

        # ==========================================
        # TRAINER VALIDATION
        # ==========================================

        if payment_type == "trainer_fee" and not trainer_id:
            return {
                "success": False,
                "message": (
                    "trainer_id is required for trainer_fee."
                )
            }

        # ==========================================
        # CHECK MEMBER
        # ==========================================

        cursor.execute(
            "SELECT id FROM members WHERE id = %s",
            (member_id,)
        )

        if not cursor.fetchone():
            return {
                "success": False,
                "message": f"Member not found: {member_id}"
            }

        # ==========================================
        # UPDATE MEMBER BASED ON PAYMENT TYPE
        # ==========================================

        if payment_type in {"monthly", "daily"}:
            # Access only:
            # Update membership_type and monthly_expires.
            # Preserve membership_expires.

            update_fields = ["membership_type = %s"]
            update_values = [payment_type]

            if monthly_expires is not None:
                update_fields.append("monthly_expires = %s")
                update_values.append(monthly_expires)

            update_values.append(member_id)

            cursor.execute(
                f"""
                UPDATE members
                SET {", ".join(update_fields)}
                WHERE id = %s
                """,
                tuple(update_values)
            )

        elif payment_type in {
            "membership",
            "membership-only",
            "membership_fee"
        }:
            # Membership only:
            # Update membership_type and membership_expires.
            # Preserve monthly_expires.

            update_fields = ["membership_type = %s"]
            update_values = [
                membership_type
                if membership_type is not None
                else "membership"
            ]

            if membership_expires is not None:
                update_fields.append("membership_expires = %s")
                update_values.append(membership_expires)

            update_values.append(member_id)

            cursor.execute(
                f"""
                UPDATE members
                SET {", ".join(update_fields)}
                WHERE id = %s
                """,
                tuple(update_values)
            )

        elif payment_type in {
            "membership-monthly",
            "membership-daily"
        }:
            # Membership + access:
            # Update membership and access expiration fields.

            update_fields = []
            update_values = []

            if membership_type is not None:
                update_fields.append("membership_type = %s")
                update_values.append(membership_type)

            if membership_expires is not None:
                update_fields.append("membership_expires = %s")
                update_values.append(membership_expires)

            if monthly_expires is not None:
                update_fields.append("monthly_expires = %s")
                update_values.append(monthly_expires)

            if update_fields:
                update_values.append(member_id)

                cursor.execute(
                    f"""
                    UPDATE members
                    SET {", ".join(update_fields)}
                    WHERE id = %s
                    """,
                    tuple(update_values)
                )

        # ==========================================
        # SAVE PAYMENT
        # ==========================================

        cursor.execute(
            """
            INSERT INTO payments (
                user_id,
                payment_type,
                amount,
                trainer_id,
                paid_at
            )
            VALUES (%s, %s, %s, %s, COALESCE(%s, NOW()))
            """,
            (
                member_id,
                payment_type,
                amount,
                trainer_id if payment_type == "trainer_fee" else None,
                paid_at
            )
        )

        payment_id = cursor.lastrowid

        # ==========================================
        # COMMIT
        # ==========================================

        connection.commit()

        return {
            "success": True,
            "message": "Payment and member details synchronized.",
            "payment_id": payment_id,
            "member_id": member_id,
            "payment_type": payment_type,
            "amount": amount,
            "membership_type": (
                membership_type
                if membership_type is not None
                else (
                    payment_type
                    if payment_type in {"daily", "monthly"}
                    else "membership"
                    if payment_type in {
                        "membership",
                        "membership-only",
                        "membership_fee"
                    }
                    else None
                )
            ),
            "membership_expires": (
                str(membership_expires)
                if membership_expires is not None
                else None
            ),
            "monthly_expires": (
                str(monthly_expires)
                if monthly_expires is not None
                else None
            ),
            "trainer_id": trainer_id
        }

    except Exception as e:
        connection.rollback()

        return {
            "success": False,
            "message": str(e)
        }

    finally:
        cursor.close()
        connection.close()
