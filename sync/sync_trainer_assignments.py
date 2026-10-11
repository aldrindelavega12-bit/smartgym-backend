
import requests

from db.connection import get_connection


API_URL = "https://smartgym-api-ia2e.onrender.com"
API_ENDPOINT = f"{API_URL}/api/trainer_assignments"
TIMEOUT = 15


def sync_trainer_assignments():
    connection = None
    cursor = None

    try:
        # Get assignments from Railway first.
        response = requests.get(
            API_ENDPOINT,
            timeout=TIMEOUT
        )
        response.raise_for_status()

        result = response.json()

        # Do not modify local data if the response is invalid.
        if not isinstance(result, dict):
            raise ValueError("Invalid API response format.")

        if result.get("success") is not True:
            raise ValueError("Railway API returned an unsuccessful response.")

        data = result.get("data")

        if not isinstance(data, list):
            raise ValueError("API data must be a list.")

        inserted = 0
        updated = 0
        skipped = 0

        connection = get_connection()
        cursor = connection.cursor()

        for row in data:
            required_fields = [
                "id",
                "trainer_id",
                "member_id",
                "plan_id",
                "start_date",
                "end_date",
                "status",
                "request_type"
            ]

            missing = [
                field for field in required_fields
                if row.get(field) is None
            ]

            if missing:
                raise ValueError(
                    f"Assignment has missing fields: {missing}"
                )

            # Use the Railway assignment ID as the source identifier.
            # Local auto-increment IDs may be different, so match using
            # the assignment's identifying fields instead.
            cursor.execute(
                """
                SELECT id, program_id, program_plan_id, status,
                       request_type
                FROM trainer_trainees
                WHERE trainer_id = %s
                  AND member_id = %s
                  AND plan_id = %s
                  AND start_date = %s
                  AND end_date = %s
                LIMIT 1
                """,
                (
                    str(row["trainer_id"]),
                    str(row["member_id"]),
                    row["plan_id"],
                    row["start_date"],
                    row["end_date"]
                )
            )

            existing = cursor.fetchone()

            if existing:
                current_values = (
                    existing[1],
                    existing[2],
                    existing[3],
                    existing[4]
                )

                new_values = (
                    row.get("program_id"),
                    row.get("program_plan_id"),
                    row["status"],
                    row["request_type"]
                )

                if current_values != new_values:
                    cursor.execute(
                        """
                        UPDATE trainer_trainees
                        SET program_id = %s,
                            program_plan_id = %s,
                            status = %s,
                            request_type = %s
                        WHERE id = %s
                        """,
                        (
                            row.get("program_id"),
                            row.get("program_plan_id"),
                            row["status"],
                            row["request_type"],
                            existing[0]
                        )
                    )
                    updated += 1
                else:
                    skipped += 1

            else:
                cursor.execute(
                    """
                    INSERT INTO trainer_trainees (
                        trainer_id,
                        member_id,
                        program_id,
                        program_plan_id,
                        plan_id,
                        start_date,
                        end_date,
                        status,
                        request_type
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        str(row["trainer_id"]),
                        str(row["member_id"]),
                        row.get("program_id"),
                        row.get("program_plan_id"),
                        row["plan_id"],
                        row["start_date"],
                        row["end_date"],
                        row["status"],
                        row["request_type"]
                    )
                )
                inserted += 1

        connection.commit()

        print()
        print("===== TRAINER ASSIGNMENT SYNC =====")
        print(f"Received : {len(data)}")
        print(f"Inserted : {inserted}")
        print(f"Updated  : {updated}")
        print(f"Skipped  : {skipped}")
        print("===================================")
        print()

    except Exception as e:
        if connection:
            connection.rollback()

        print(f"[TRAINER ASSIGNMENT SYNC ERROR] {e}")
        raise

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()
