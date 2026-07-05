from db.connection import get_connection


from db.connection import get_connection
from datetime import date
from sync.fp_delete import delete_fingerprint


def handle_walkin_created(payload):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO walkins(

                id,
                full_name,
                fingerprint_template,
                phone_number,
                visit_date,
                fp_id

            )

            VALUES(%s,%s,%s,%s,%s,%s)
            """,

            (

                payload["walkin_id"],
                payload["full_name"],
                payload["fp_template"],
                payload["phone_number"],
                date.today(),
                payload["fp_id"]

            )

        )

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

                payload["walkin_id"],
                payload["fp_id"],
                payload["fp_template"]

            )

        )

        connection.commit()

        return {

            "success": True,

            "message": "Walkin synchronized."

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

from db.connection import get_connection


def handle_walkin_payment_updated(payload):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO payments(

                user_id,
                payment_type,
                amount

            )

            VALUES(%s,%s,%s)
            """,
            (

                payload["walkin_id"],
                payload["payment_type"],
                payload["amount"]

            )
        )

        connection.commit()

        return {

            "success": True,

            "message": "Walk-in payment synchronized."

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


def handle_walkin_deleted(payload):

    connection = get_connection()

    cursor = connection.cursor()

    try:

        walkin_id = payload["walkin_id"]

        # ==========================
        # GET FP ID
        # ==========================

        cursor.execute(
            """
            SELECT fp_id
            FROM fp_templates
            WHERE user_id=%s
            """,
            (walkin_id,)
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
            (walkin_id,)
        )

        cursor.execute(
            "DELETE FROM walkins WHERE id=%s",
            (walkin_id,)
        )

        connection.commit()

        return {

            "success": True,

            "message": "Walkin deleted."

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
        
from db.connection import get_connection


def handle_walkin_locker_assigned(payload):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        walkin_id = payload["walkin_id"]
        locker_number = payload["locker_number"]

        cursor.execute(
            """
            INSERT INTO locker_sessions(

                user_id,
                locker_number,
                status

            )

            VALUES(%s,%s,'ACTIVE')
            """,
            (
                walkin_id,
                locker_number
            )
        )

        connection.commit()

        return {

            "success": True,

            "message": "Locker assigned."

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