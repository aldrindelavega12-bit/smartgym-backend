import requests

from db.connection import get_connection


API_URL = "https://smartgym-api-ia2e.onrender.com"


def sync_trainer_plans():

    response = requests.get(
        f"{API_URL}/api/trainer_plans"
    )

    response.raise_for_status()

    data = response.json()["data"]

    connection = get_connection()

    cursor = connection.cursor()

    inserted = 0
    updated = 0

    try:

        for row in data:

            cursor.execute(
                """
                SELECT id

                FROM trainer_plans

                WHERE id=%s
                """,
                (
                    row["id"],
                )
            )

            if cursor.fetchone():

                cursor.execute(
                    """
                    UPDATE trainer_plans

                    SET
                        trainer_id=%s,
                        plan_name=%s,
                        duration_days=%s,
                        price=%s,
                        active=%s

                    WHERE id=%s
                    """,
                    (
                        row["trainer_id"],
                        row["plan_name"],
                        row["duration_days"],
                        row["price"],
                        row["active"],
                        row["id"]
                    )
                )

                updated += 1

            else:

                cursor.execute(
                    """
                    INSERT INTO trainer_plans (
                        id,
                        trainer_id,
                        plan_name,
                        duration_days,
                        price,
                        active
                    )

                    VALUES (
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s
                    )
                    """,
                    (
                        row["id"],
                        row["trainer_id"],
                        row["plan_name"],
                        row["duration_days"],
                        row["price"],
                        row["active"]
                    )
                )

                inserted += 1

        connection.commit()

        print()
        print("===== TRAINER PLAN SYNC =====")
        print(f"Inserted : {inserted}")
        print(f"Updated  : {updated}")
        print("=============================")
        print()

    finally:

        cursor.close()
        connection.close()