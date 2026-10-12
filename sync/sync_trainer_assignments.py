import requests
from db.connection import get_connection


API_URL = "https://smartgym-api-ia2e.onrender.com"
API_ENDPOINT = f"{API_URL}/api/trainer_assignments"
TIMEOUT = 15


def sync_trainer_assignments():
    connection = None
    cursor = None

    try:
        # Get assignments from Railway
        response = requests.get(
            API_ENDPOINT,
            timeout=TIMEOUT
        )
        response.raise_for_status()

        result = response.json()

        if not isinstance(result, dict):
            raise ValueError("Invalid API response format.")

        if result.get("success") is not True:
            raise ValueError(
                "Railway API returned an unsuccessful response."
            )

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

            member_id = str(row["member_id"])

            # MEMBER ID ONLY: Find the latest existing record
            cursor.execute("""
                SELECT
                    id,
                    program_id,
                    program_plan_id,
                    plan_id,
                    start_date,
                    end_date,
                    status,
                    request_type
                FROM trainer_trainees
                WHERE member_id = %s
                ORDER BY id DESC
                LIMIT 1
            """, (member_id,))

            existing = cursor.fetchone()

            new_values = (
                row.get("program_id"),
                row.get("program_plan_id"),
                row["plan_id"],
                row["start_date"],
                row["end_date"],
                row["status"],
                row["request_type"]
            )

            if existing:
                current_values = (
                    existing[1],
                    existing[2],
                    existing[3],
                    (
                        existing[4].strftime("%Y-%m-%d")
                        if existing[4] else None
                    ),
                    (
                        existing[5].strftime("%Y-%m-%d")
                        if existing[5] else None
                    ),
                    existing[6],
                    existing[7]
                )

                normalized_new_values = (
                    row.get("program_id"),
                    row.get("program_plan_id"),
                    row["plan_id"],
                    row["start_date"],
                    row["end_date"],
                    row["status"],
                    row["request_type"]
                )

                if current_values != normalized_new_values:
                    # Update the existing member record only
                    cursor.execute("""
                        UPDATE trainer_trainees
                        SET
                            trainer_id = %s,
                            program_id = %s,
                            program_plan_id = %s,
                            plan_id = %s,
                            start_date = %s,
                            end_date = %s,
                            status = %s,
                            request_type = %s
                        WHERE id = %s
                    """, (
                        row["trainer_id"],
                        row.get("program_id"),
                        row.get("program_plan_id"),
                        row["plan_id"],
                        row["start_date"],
                        row["end_date"],
                        row["status"],
                        row["request_type"],
                        existing[0]
                    ))

                    updated += 1
                else:
                    skipped += 1

            else:
                # Insert only if this member_id does not exist
                cursor.execute("""
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
                """, (
                    row["trainer_id"],
                    member_id,
                    row.get("program_id"),
                    row.get("program_plan_id"),
                    row["plan_id"],
                    row["start_date"],
                    row["end_date"],
                    row["status"],
                    row["request_type"]
                ))

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
