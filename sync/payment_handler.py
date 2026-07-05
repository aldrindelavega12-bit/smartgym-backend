from db.connection import get_connection


def handle_payment_updated(payload):

    connection = get_connection()

    cursor = connection.cursor()

    try:

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

                payload["membership_type"],
                payload["membership_expires"],
                payload["monthly_expires"],
                payload["member_id"]

            )

        )

        connection.commit()

        return {

            "success": True,

            "message": "Payment synchronized."

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