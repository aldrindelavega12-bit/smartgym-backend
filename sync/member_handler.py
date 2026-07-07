from db.connection import get_connection
from sync.face_installer import remove_face_package
from sync.fp_delete import delete_fingerprint


def handle_member_created(payload):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:

        member_id = payload["member_id"]

        # Check duplicate
        cursor.execute(
            "SELECT id FROM members WHERE id=%s",
            (member_id,)
        )

        if cursor.fetchone():

            return {
                "success": True,
                "message": "Member already synchronized."
            }

        # INSERT MEMBER
        cursor.execute(
            """
            INSERT INTO members(

                id,
                full_name,
                fingerprint_template,
                phone_number

            )

            VALUES(%s,%s,%s,%s)
            """,
            (

                payload["member_id"],
                payload["full_name"],
                payload["fp_template"],
                payload["phone_number"]

            )
        )

        # INSERT FP TEMPLATE
        cursor.execute(
            """
            INSERT INTO fp_templates(

                user_id,
                fp_id,
                template

            )

            VALUES(%s,%s,%s)
            """,
            (

                payload["member_id"],
                payload["fp_id"],
                payload["fp_template"]

            )
        )

        connection.commit()

        return {
            "success": True,
            "message": "Member synchronized."
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


def handle_member_deleted(payload):

    connection = get_connection()
    cursor = connection.cursor()

    try:
    

        member_id = payload["member_id"]

        # ==========================
        # GET FP ID
        # ==========================
        cursor.execute(
            """
            SELECT fp_id
            FROM fp_templates
            WHERE user_id=%s
            """,
            (member_id,)
        )

        result = cursor.fetchone()

        if result:

            fp_id = result[0]

            delete_fingerprint(fp_id)

        # ==========================
        # DELETE DATABASE
        # ==========================
        cursor.execute(
            "DELETE FROM fp_templates WHERE user_id=%s",
            (member_id,)
        )

        cursor.execute(
            "DELETE FROM members WHERE id=%s",
            (member_id,)
        )

        # ==========================
        # DELETE FACE DATASET
        # ==========================
        remove_face_package(member_id)
        # ==========================
        # DELETE USER ACCOUNT
        # ==========================
        print("DELETE USER ACCOUNT:", member_id)
        cursor.execute(
            """
            DELETE FROM user_accounts
            WHERE user_id=%s
            """,
            (member_id,)
        )
        connection.commit()

        return {
            "success": True,
            "message": "Member deleted."
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