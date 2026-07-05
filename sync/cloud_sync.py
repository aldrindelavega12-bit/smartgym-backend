import requests

from db.connection import get_connection


API_URL = "https://smartgym-api-ia2e.onrender.com"


def sync_pending_members():

    response = requests.get(

        f"{API_URL}/api/pending_members"

    )

    response.raise_for_status()

    data = response.json()["data"]

    connection = get_connection()

    cursor = connection.cursor()

    inserted = 0

    skipped = 0

    try:

        for row in data:

            cursor.execute(

                """
                SELECT id

                FROM pending_members

                WHERE account_id=%s
                """,

                (

                    row["account_id"],

                )

            )

            if cursor.fetchone():

                skipped += 1

                continue

            cursor.execute(

                """
                INSERT INTO pending_members(

                    account_id,
                    full_name,
                    phone_number,
                    status

                )

                VALUES(

                    %s,
                    %s,
                    %s,
                    'PENDING'

                )
                """,

                (

                    row["account_id"],
                    row["full_name"],
                    row["phone_number"]

                )

            )

            inserted += 1

        connection.commit()

        print()

        print("========== CLOUD SYNC ==========")

        print(f"Inserted : {inserted}")

        print(f"Skipped  : {skipped}")

        print("===============================")

        print()

    finally:

        cursor.close()

        connection.close()