from db.connection import get_connection


def handle_trainer_assignment_created(payload):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        assignment_id = payload["assignment_id"]
        trainer_id = payload["trainer_id"]
        member_id = payload["member_id"]
        program_id = payload.get("program_id")
        program_plan_id = payload.get("program_plan_id")
        plan_id = payload["plan_id"]
        start_date = payload["start_date"]
        end_date = payload["end_date"]
        status = payload.get("status", "active")
        request_type = payload.get(
            "request_type",
            "standard"
        )

        # ==========================================
        # CHECK IF ASSIGNMENT ALREADY EXISTS
        # ==========================================

        cursor.execute(
            """
            SELECT id
            FROM trainer_trainees
            WHERE id=%s
            """,
            (assignment_id,)
        )

        existing = cursor.fetchone()

        if existing:

            # Update existing assignment
            cursor.execute(
                """
                UPDATE trainer_trainees
                SET
                    trainer_id=%s,
                    member_id=%s,
                    program_id=%s,
                    program_plan_id=%s,
                    plan_id=%s,
                    start_date=%s,
                    end_date=%s,
                    status=%s,
                    request_type=%s
                WHERE id=%s
                """,
                (
                    trainer_id,
                    member_id,
                    program_id,
                    program_plan_id,
                    plan_id,
                    start_date,
                    end_date,
                    status,
                    request_type,
                    assignment_id
                )
            )

            connection.commit()

            return {
                "success": True,
                "message":
                    "Trainer assignment updated."
            }

        # ==========================================
        # INSERT TRAINER ASSIGNMENT
        # ==========================================

        cursor.execute(
            """
            INSERT INTO trainer_trainees
            (
                id,
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
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )
            """,
            (
                assignment_id,
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
        )

        connection.commit()

        print(
            "[TRAINER SYNC] Trainer assignment "
            "synchronized."
        )

        print(
            f"[TRAINER SYNC] Assignment ID : "
            f"{assignment_id}"
        )

        print(
            f"[TRAINER SYNC] Trainer ID    : "
            f"{trainer_id}"
        )

        print(
            f"[TRAINER SYNC] Member ID     : "
            f"{member_id}"
        )

        print(
            f"[TRAINER SYNC] Plan ID       : "
            f"{plan_id}"
        )

        return {
            "success": True,
            "message":
                "Trainer assignment synchronized."
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