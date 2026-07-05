import requests

from db.connection import get_connection


API_URL = "https://smartgym-api-ia2e.onrender.com"


def sync_user_accounts():

    response = requests.get(

        f"{API_URL}/api/user_accounts"

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

                FROM user_accounts

                WHERE username=%s
                """,

                (

                    row["username"],

                )

            )

            if cursor.fetchone():

                cursor.execute(

                    """
                    UPDATE user_accounts

                    SET

                        user_id=%s,
                        fullname=%s,
                        password=%s,
                        role=%s

                    WHERE username=%s
                    """,

                    (

                        row["user_id"],
                        row["fullname"],
                        row["password"],
                        row["role"],
                        row["username"]

                    )

                )

                updated += 1

            else:

                cursor.execute(

                    """
                    INSERT INTO user_accounts(

                        id,
                        user_id,
                        username,
                        password,
                        role,
                        fullname

                    )

                    VALUES(

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
                        row["user_id"],
                        row["username"],
                        row["password"],
                        row["role"],
                        row["fullname"]

                    )

                )

                inserted += 1

        connection.commit()

        print()

        print("===== USER ACCOUNT SYNC =====")

        print(f"Inserted : {inserted}")

        print(f"Updated  : {updated}")

        print("=============================")

        print()

    finally:

        cursor.close()

        connection.close()