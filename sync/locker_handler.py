from db.connection import get_connection


def handle_locker_overtime_paid(payload):
    print("=== NEW HANDLER ===")
    print(payload)

    connection = get_connection()
    cursor = connection.cursor()

    try:

        # End locker session
        cursor.execute(
            """
            UPDATE locker_sessions
            SET
                overtime_paid = 1,
                status = 'ended',
                end_time = NOW()
            WHERE
                user_id = %s
                AND locker_number = %s
                AND status = 'active'
            """,
            (
                payload["user_id"],
                payload["locker_number"]
            )
        )

        # Record payment
        cursor.execute(
            """
            INSERT INTO payments(

                user_id,
                payment_type,
                amount

            )

            VALUES(%s,%s,%s)
            """,
            (
                payload["user_id"],
                "LOCKER_OVERTIME",
                payload["overtime_fee"]
            )
        )

        connection.commit()

        return {
            "success": True,
            "message": "Locker overtime synchronized."
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