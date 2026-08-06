from db.connection import execute_query


def handle_activation_created(payload):

    try:

        execute_query(
            """
            INSERT INTO member_activation
            (
                member_id,
                activation_token,
                status
            )
            VALUES (%s,%s,%s)
            ON DUPLICATE KEY UPDATE
                activation_token = VALUES(activation_token),
                status = VALUES(status)
            """,
            (
                payload["member_id"],
                payload["activation_token"],
                payload.get("status", "PENDING")
            )
        )

        return {
            "success": True
        }

    except Exception as e:

        print("ACTIVATION HANDLER:", e)

        return {
            "success": False,
            "message": str(e)
        }