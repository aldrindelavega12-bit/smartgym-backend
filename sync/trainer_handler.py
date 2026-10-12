from db.connection import get_connection


def handle_trainer_assignment_created(payload):
    connection = None
    cursor = None

    try:
        assignment_id = payload.get("assignment_id")
        trainer_id = payload["trainer_id"]
        member_id = str(payload["member_id"])
        program_id = payload.get("program_id")
        program_plan_id = payload.get("program_plan_id")
        plan_id = payload["plan_id"]
        start_date = payload["start_date"]
        end_date = payload["end_date"]
        status = payload.get("status", "active")
        request_type = payload.get("request_type", "standard")

        connection = get_connection()
        cursor = connection.cursor()

        # MEMBER ID ONLY: find the latest existing assignment
        cursor.execute("""
            SELECT id
            FROM trainer_trainees
            WHERE member_id = %s
            ORDER BY id DESC
            LIMIT 1
            FOR UPDATE
        """, (member_id,))

        existing = cursor.fetchone()

        if existing:
            local_assignment_id = existing[0]

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
                trainer_id,
                program_id,
                program_plan_id,
                plan_id,
                start_date,
                end_date,
                status,
                request_type,
                local_assignment_id
            ))

            connection.commit()

            print(
                f"[TRAINER SYNC] Updated existing assignment "
                f"id={local_assignment_id}, member_id={member_id}"
            )

            return {
                "success": True,
                "message": "Existing trainer assignment updated.",
                "assignment_id": local_assignment_id,
                "member_id": member_id
            }

        # INSERT only if this member_id does not exist
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
            trainer_id,
            member_id,
            program_id,
            program_plan_id,
            plan_id,
            start_date,
            end_date,
            status,
            request_type
        ))

        local_assignment_id = cursor.lastrowid
        connection.commit()

        print(
            f"[TRAINER SYNC] Inserted new assignment "
            f"id={local_assignment_id}, member_id={member_id}"
        )

        return {
            "success": True,
            "message": "New trainer assignment created.",
            "assignment_id": local_assignment_id,
            "member_id": member_id
        }

    except Exception:
        if connection:
            connection.rollback()
        raise

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
