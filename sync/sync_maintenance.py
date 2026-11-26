
import requests

from db.connection import get_connection


API_URL = "https://smartgym-api-ia2e.onrender.com"

# Use the existing API key from your cloud backend.
API_KEY = "GYM_MASTER_2026"

HEADERS = {
    "X-API-KEY": API_KEY
}


MAINTENANCE_CONFIG = {

    "gym-access-types": {
        "table": "gym_access_types",
        "fields": [
            "access_name",
            "price",
            "duration_days",
            "status"
        ]
    },

    "membership-types": {
        "table": "membership_types",
        "fields": [
            "membership_name",
            "fee",
            "validity_days",
            "status"
        ]
    },

    "trainer-plans": {
        "table": "trainer_plans",
        "fields": [
            "trainer_id",
            "plan_name",
            "duration_days",
            "price",
            "active"
        ]
    }

}


def sync_maintenance(resource):

    config = MAINTENANCE_CONFIG[resource]

    table = config["table"]
    fields = config["fields"]

    response = requests.get(
        f"{API_URL}/api/sync/maintenance/{resource}",
        headers=HEADERS,
        timeout=30
    )

    response.raise_for_status()

    result = response.json()

    if result.get("status") != "success":

        raise Exception(
            result.get("message", "Cloud sync failed")
        )

    data = result["data"]

    connection = get_connection()
    cursor = connection.cursor()

    inserted = 0
    updated = 0
    skipped = 0

    try:

        for row in data:

            record_id = row["id"]

            values = [
                row[field]
                for field in fields
            ]

            cursor.execute(
                f"""
                SELECT {", ".join(fields)}
                FROM {table}
                WHERE id = %s
                """,
                (record_id,)
            )

            existing = cursor.fetchone()

            # =========================
            # NEW RECORD
            # =========================

            if not existing:

                columns = ["id"] + fields

                placeholders = ", ".join(
                    ["%s"] * len(columns)
                )

                cursor.execute(
                    f"""
                    INSERT INTO {table}
                    ({", ".join(columns)})
                    VALUES ({placeholders})
                    """,
                    [record_id] + values
                )

                inserted += 1

            # =========================
            # EXISTING RECORD
            # =========================

            else:

                current_values = list(existing)

                if current_values != values:

                    update_fields = ", ".join(
                        f"{field} = %s"
                        for field in fields
                    )

                    cursor.execute(
                        f"""
                        UPDATE {table}
                        SET {update_fields}
                        WHERE id = %s
                        """,
                        values + [record_id]
                    )

                    updated += 1

                else:

                    skipped += 1

        connection.commit()

        print()
        print(f"========== {resource.upper()} SYNC ==========")
        print(f"Inserted : {inserted}")
        print(f"Updated  : {updated}")
        print(f"Skipped  : {skipped}")
        print("==========================================")
        print()

    except Exception:

        connection.rollback()
        raise

    finally:

        cursor.close()
        connection.close()


def sync_all_maintenance():

    for resource in MAINTENANCE_CONFIG:

        try:

            sync_maintenance(resource)

        except Exception as e:

            print(
                f"[MAINTENANCE SYNC ERROR] "
                f"{resource}: {e}"
            )


if __name__ == "__main__":

    sync_all_maintenance()
