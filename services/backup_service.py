import os
import re
from datetime import datetime, date, time
from decimal import Decimal

import mysql.connector
from dotenv import load_dotenv
from supabase import create_client, Client


load_dotenv()


# =========================================================
# RAILWAY DATABASE CONFIGURATION
# =========================================================

RAILWAY_DB_CONFIG = {
    "host": os.getenv("RAILWAY_DB_HOST") or os.getenv("DB_HOST"),
    "port": int(
        os.getenv("RAILWAY_DB_PORT")
        or os.getenv("DB_PORT")
        or "3306"
    ),
    "user": os.getenv("RAILWAY_DB_USER") or os.getenv("DB_USER"),
    "password": (
        os.getenv("RAILWAY_DB_PASSWORD")
        or os.getenv("DB_PASSWORD")
    ),
    "database": os.getenv("RAILWAY_DB_NAME") or os.getenv("DB_NAME"),
}


# =========================================================
# SUPABASE CONFIGURATION
# =========================================================

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv(
    "SUPABASE_SERVICE_ROLE_KEY"
)
SUPABASE_BACKUP_BUCKET = os.getenv(
    "SUPABASE_BACKUP_BUCKET",
    "smart-gym-backups"
)


def get_supabase_client():
    if not SUPABASE_URL:
        raise RuntimeError(
            "SUPABASE_URL environment variable is not configured."
        )

    if not SUPABASE_SERVICE_ROLE_KEY:
        raise RuntimeError(
            "SUPABASE_SERVICE_ROLE_KEY environment variable is not configured."
        )

    return create_client(
        SUPABASE_URL,
        SUPABASE_SERVICE_ROLE_KEY
    )


# =========================================================
# BACKUP DIRECTORY
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

BACKUP_DIR = os.path.join(
    BASE_DIR,
    "backups"
)

os.makedirs(
    BACKUP_DIR,
    exist_ok=True
)


# =========================================================
# RAILWAY CONNECTION
# =========================================================

def get_railway_connection():
    return mysql.connector.connect(
        **RAILWAY_DB_CONFIG
    )


# =========================================================
# MYSQL IDENTIFIER ESCAPING
# =========================================================

def quote_identifier(name):
    return (
        "`"
        + str(name).replace("`", "``")
        + "`"
    )


# =========================================================
# SQL VALUE CONVERSION
# =========================================================

def sql_value(value):

    if value is None:
        return "NULL"

    if isinstance(value, bool):
        return "1" if value else "0"

    if isinstance(
        value,
        (int, float, Decimal)
    ):
        return str(value)

    if isinstance(
        value,
        (datetime, date, time)
    ):
        value = str(value)

    if isinstance(value, bytes):
        return "X'" + value.hex() + "'"

    value = str(value)

    value = value.replace(
        "\\",
        "\\\\"
    )

    value = value.replace(
        "'",
        "''"
    )

    value = value.replace(
        "\0",
        "\\0"
    )

    value = value.replace(
        "\n",
        "\\n"
    )

    value = value.replace(
        "\r",
        "\\r"
    )

    value = value.replace(
        "\x1a",
        "\\Z"
    )

    return "'" + value + "'"


# =========================================================
# SAFE FILENAME
# =========================================================

def safe_filename(name):
    return re.sub(
        r"[^a-zA-Z0-9_.-]",
        "_",
        name
    )


# =========================================================
# GET DATABASE OBJECTS
# =========================================================

def get_database_objects(cursor):

    cursor.execute(
        """
        SELECT
            TABLE_NAME,
            TABLE_TYPE
        FROM information_schema.TABLES
        WHERE TABLE_SCHEMA = %s
        ORDER BY
            CASE
                WHEN TABLE_TYPE = 'BASE TABLE'
                THEN 1
                ELSE 2
            END,
            TABLE_NAME
        """,
        (
            RAILWAY_DB_CONFIG["database"],
        )
    )

    return cursor.fetchall()


# =========================================================
# BACKUP TABLE
# =========================================================

def backup_table(
    cursor,
    file,
    table_name
):

    quoted_table = quote_identifier(
        table_name
    )

    # -----------------------------------------------------
    # CREATE TABLE
    # -----------------------------------------------------

    cursor.execute(
        f"SHOW CREATE TABLE {quoted_table}"
    )

    result = cursor.fetchone()

    create_statement = result[1]

    file.write(
        "\n-- --------------------------------------------------\n"
    )

    file.write(
        f"-- TABLE: {table_name}\n"
    )

    file.write(
        "-- --------------------------------------------------\n\n"
    )

    file.write(
        f"DROP TABLE IF EXISTS {quoted_table};\n"
    )

    file.write(
        create_statement + ";\n\n"
    )

    # -----------------------------------------------------
    # GET COLUMNS
    # -----------------------------------------------------

    cursor.execute(
        f"SHOW COLUMNS FROM {quoted_table}"
    )

    columns = cursor.fetchall()

    column_names = [
        column[0]
        for column in columns
    ]

    if not column_names:
        return 0

    quoted_columns = ", ".join(
        quote_identifier(column)
        for column in column_names
    )

    # -----------------------------------------------------
    # GET DATA
    # -----------------------------------------------------

    cursor.execute(
        f"SELECT * FROM {quoted_table}"
    )

    rows = cursor.fetchall()

    row_count = 0

    for row in rows:

        values = ", ".join(
            sql_value(value)
            for value in row
        )

        file.write(
            f"INSERT INTO {quoted_table} "
            f"({quoted_columns}) "
            f"VALUES ({values});\n"
        )

        row_count += 1

    file.write("\n")

    return row_count


# =========================================================
# BACKUP VIEW
# =========================================================

def backup_view(
    cursor,
    file,
    view_name
):

    quoted_view = quote_identifier(
        view_name
    )

    cursor.execute(
        f"SHOW CREATE VIEW {quoted_view}"
    )

    result = cursor.fetchone()

    create_statement = result[1]

    file.write(
        "\n-- --------------------------------------------------\n"
    )

    file.write(
        f"-- VIEW: {view_name}\n"
    )

    file.write(
        "-- --------------------------------------------------\n\n"
    )

    file.write(
        f"DROP VIEW IF EXISTS {quoted_view};\n"
    )

    file.write(
        create_statement + ";\n\n"
    )


# =========================================================
# UPLOAD BACKUP TO SUPABASE
# =========================================================

def upload_backup_to_supabase(
    filepath,
    filename
):

    supabase = get_supabase_client()

    # Organize files by year/month
    now = datetime.now()

    storage_path = (
        f"{now.strftime('%Y')}/"
        f"{now.strftime('%m')}/"
        f"{filename}"
    )

    with open(
        filepath,
        "rb"
    ) as file:

        file_data = file.read()

    # Upload backup
    supabase.storage \
        .from_(SUPABASE_BACKUP_BUCKET) \
        .upload(
            path=storage_path,
            file=file_data,
            file_options={
                "content-type": "application/sql",
                "upsert": "false"
            }
        )

    return storage_path


# =========================================================
# DELETE SUPABASE BACKUP
# =========================================================

def delete_supabase_backup(
    storage_path
):

    if not storage_path:
        return

    try:

        supabase = get_supabase_client()

        supabase.storage \
            .from_(SUPABASE_BACKUP_BUCKET) \
            .remove(
                [storage_path]
            )

    except Exception as e:

        print(
            "SUPABASE DELETE WARNING:",
            e
        )


# =========================================================
# DOWNLOAD BACKUP FROM SUPABASE
# =========================================================

def download_backup_from_supabase(
    storage_path
):

    supabase = get_supabase_client()

    response = (
        supabase.storage
        .from_(SUPABASE_BACKUP_BUCKET)
        .download(storage_path)
    )

    return response


# =========================================================
# CREATE DATABASE BACKUP
# =========================================================

def create_database_backup():

    connection = None
    cursor = None

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    filename = safe_filename(
        f"smart_gym_railway_backup_{timestamp}.sql"
    )

    filepath = os.path.join(
        BACKUP_DIR,
        filename
    )

    storage_path = None

    try:

        # =================================================
        # CONNECT TO RAILWAY
        # =================================================

        connection = get_railway_connection()

        cursor = connection.cursor()

        database_name = (
            RAILWAY_DB_CONFIG["database"]
        )

        # =================================================
        # CREATE SQL FILE
        # =================================================

        with open(
            filepath,
            "w",
            encoding="utf-8"
        ) as file:

            # -------------------------------------------------
            # HEADER
            # -------------------------------------------------

            file.write(
                "-- ==================================================\n"
            )

            file.write(
                "-- SMART GYM DATABASE BACKUP\n"
            )

            file.write(
                "-- ==================================================\n"
            )

            file.write(
                f"-- Database: {database_name}\n"
            )

            file.write(
                "-- Created: "
                + datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                + "\n"
            )

            file.write(
                "-- Source: Railway MySQL\n"
            )

            file.write(
                "-- ==================================================\n\n"
            )

            file.write(
                "SET FOREIGN_KEY_CHECKS=0;\n"
            )

            file.write(
                "SET SQL_MODE='NO_AUTO_VALUE_ON_ZERO';\n"
            )

            file.write(
                "SET NAMES utf8mb4;\n\n"
            )

            # -------------------------------------------------
            # DATABASE
            # -------------------------------------------------

            file.write(
                f"CREATE DATABASE IF NOT EXISTS "
                f"{quote_identifier(database_name)} "
                f"CHARACTER SET utf8mb4;\n\n"
            )

            file.write(
                f"USE {quote_identifier(database_name)};\n\n"
            )

            # -------------------------------------------------
            # GET TABLES / VIEWS
            # -------------------------------------------------

            objects = get_database_objects(
                cursor
            )

            table_count = 0
            view_count = 0
            row_count = 0

            # -------------------------------------------------
            # TABLES FIRST
            # -------------------------------------------------

            for obj in objects:

                object_name = obj[0]
                object_type = obj[1]

                if object_type == "BASE TABLE":

                    rows = backup_table(
                        cursor,
                        file,
                        object_name
                    )

                    table_count += 1
                    row_count += rows

            # -------------------------------------------------
            # VIEWS AFTER TABLES
            # -------------------------------------------------

            for obj in objects:

                object_name = obj[0]
                object_type = obj[1]

                if object_type == "VIEW":

                    backup_view(
                        cursor,
                        file,
                        object_name
                    )

                    view_count += 1

            # -------------------------------------------------
            # FOOTER
            # -------------------------------------------------

            file.write(
                "\nSET FOREIGN_KEY_CHECKS=1;\n"
            )

            file.write(
                "\n-- ==================================================\n"
            )

            file.write(
                "-- BACKUP COMPLETE\n"
            )

            file.write(
                f"-- Tables: {table_count}\n"
            )

            file.write(
                f"-- Views: {view_count}\n"
            )

            file.write(
                f"-- Rows: {row_count}\n"
            )

            file.write(
                "-- ==================================================\n"
            )

        # =================================================
        # FILE SIZE
        # =================================================

        file_size = os.path.getsize(
            filepath
        )

        # =================================================
        # UPLOAD TO SUPABASE
        # =================================================

        storage_path = upload_backup_to_supabase(
            filepath,
            filename
        )

        print(
            "SUPABASE BACKUP UPLOAD SUCCESS:",
            storage_path
        )

        # =================================================
        # RETURN
        # =================================================

        return {
            "success": True,

            "filename": filename,

            # IMPORTANT:
            # This is now the Supabase object path.
            "filepath": storage_path,

            "storage_path": storage_path,

            "file_size": file_size,

            "tables": table_count,

            "views": view_count,

            "rows": row_count,

            "database": database_name,

            "created_at":
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
        }

    except Exception as e:

        # -------------------------------------------------
        # DELETE LOCAL INCOMPLETE FILE
        # -------------------------------------------------

        if os.path.exists(filepath):

            try:
                os.remove(filepath)

            except Exception:
                pass

        # -------------------------------------------------
        # DELETE SUPABASE FILE IF UPLOAD SUCCEEDED
        # BUT LATER STEP FAILED
        # -------------------------------------------------

        if storage_path:

            delete_supabase_backup(
                storage_path
            )

        print(
            "BACKUP ERROR:",
            e
        )

        return {
            "success": False,
            "error": str(e)
        }

    finally:

        try:

            if cursor:
                cursor.close()

        except Exception:
            pass

        try:

            if connection:
                connection.close()

        except Exception:
            pass
