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

    deleted = 0

    trainer_plans_deleted = 0

    try:

        # =====================================================
        # INSERT / UPDATE
        # =====================================================

        for row in data:

            cursor.execute(

                """
                SELECT
                    id,
                    user_id,
                    role

                FROM user_accounts

                WHERE username=%s
                """,

                (

                    row["username"],

                )

            )

            existing = cursor.fetchone()

            if existing:

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


        # =====================================================
        # DELETE ACCOUNTS THAT NO LONGER EXIST IN RAILWAY
        #
        # ALL ROLES ARE INCLUDED:
        # Manager
        # Admin
        # Staff
        # Trainer
        # =====================================================

        railway_user_ids = [

            str(row["user_id"])

            for row in data

            if row.get("user_id") is not None

        ]


        # Get ALL local accounts first

        cursor.execute(

            """
            SELECT
                id,
                user_id,
                username,
                role

            FROM user_accounts
            """

        )

        local_accounts = cursor.fetchall()


        for local in local_accounts:

            local_user_id = local[1]

            local_username = local[2]

            local_role = local[3]


            # -------------------------------------------------
            # If local account is NOT in Railway anymore
            # -------------------------------------------------

            if (

                local_user_id is not None

                and str(local_user_id)
                not in railway_user_ids

            ):

                print(
                    f"DELETED FROM RAILWAY: "
                    f"{local_username} "
                    f"({local_role})"
                )


                # =============================================
                # IF TRAINER
                #
                # Delete trainer plans FIRST
                # =============================================

                if (

                    local_role

                    and str(local_role).lower()
                    == "trainer"

                ):

                    cursor.execute(

                        """
                        DELETE FROM trainer_plans

                        WHERE trainer_id=%s
                        """,

                        (

                            local_user_id,

                        )

                    )

                    trainer_plans_deleted += (
                        cursor.rowcount
                    )

                    print(
                        f"Trainer plans deleted: "
                        f"{cursor.rowcount}"
                    )


                # =============================================
                # DELETE USER ACCOUNT
                # =============================================

                cursor.execute(

                    """
                    DELETE FROM user_accounts

                    WHERE user_id=%s
                    """,

                    (

                        local_user_id,

                    )

                )

                deleted += cursor.rowcount


        # =====================================================
        # COMMIT EVERYTHING
        # =====================================================

        connection.commit()


        # =====================================================
        # LOG
        # =====================================================

        print()

        print("===== USER ACCOUNT SYNC =====")

        print(f"Inserted              : {inserted}")

        print(f"Updated               : {updated}")

        print(f"Deleted               : {deleted}")

        print(
            f"Trainer Plans Deleted : "
            f"{trainer_plans_deleted}"
        )

        print("=============================")

        print()


    except Exception:

        connection.rollback()

        raise


    finally:

        cursor.close()

        connection.close()
