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
    updated = 0
    skipped = 0

    try:

        for row in data:

            cursor.execute(

                """
                SELECT

                    full_name,
                    phone_number

                FROM pending_members

                WHERE account_id=%s
                """,

                (

                    row["account_id"],

                )

            )

            existing = cursor.fetchone()

            # =========================
            # NEW RECORD
            # =========================

            if not existing:

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

            # =========================
            # EXISTING RECORD
            # =========================

            else:

                current_name = existing[0]
                current_phone = existing[1]

                if (

                    current_name != row["full_name"]

                    or

                    current_phone != row["phone_number"]

                ):

                    cursor.execute(

                        """
                        UPDATE pending_members

                        SET

                            full_name=%s,
                            phone_number=%s

                        WHERE account_id=%s
                        """,

                        (

                            row["full_name"],
                            row["phone_number"],
                            row["account_id"]

                        )

                    )

                    updated += 1

                else:

                    skipped += 1

        connection.commit()

        print()

        print("========== CLOUD SYNC ==========")

        print(f"Inserted : {inserted}")
        print(f"Updated  : {updated}")
        print(f"Skipped  : {skipped}")

        print("===============================")

        print()

    finally:

        cursor.close()

        connection.close()