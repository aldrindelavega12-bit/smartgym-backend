
import os
import re
import zipfile
import shutil
import tempfile
import urllib.request


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

# =========================================================
# GITHUB BACKUP SOURCES
# =========================================================

GITHUB_BACKEND_URL = (
    "https://github.com/"
    "aldrindelavega12-bit/"
    "smartgym-backend"
)

GITHUB_FRONTEND_URL = (
    "https://github.com/"
    "aldrindelavega12-bit/"
    "smartgym-frontend"
)

def download_github_repository(
    repository_url,
    destination_dir
):
    """
    Download a public GitHub repository
    and return the extracted repository directory.
    """

    # =========================================================
    # CREATE DESTINATION DIRECTORY
    # =========================================================

    os.makedirs(
        destination_dir,
        exist_ok=True
    )

    # =========================================================
    # GITHUB MAIN BRANCH ZIP
    # =========================================================

    archive_url = (
        repository_url.rstrip("/")
        + "/archive/refs/heads/main.zip"
    )

    archive_path = os.path.join(
        destination_dir,
        "repository.zip"
    )

    # =========================================================
    # DOWNLOAD REPOSITORY
    # =========================================================

    urllib.request.urlretrieve(
        archive_url,
        archive_path
    )

    # =========================================================
    # CHECK DOWNLOADED ZIP
    # =========================================================

    if not os.path.exists(
        archive_path
    ):
        raise RuntimeError(
            "GitHub repository ZIP download failed."
        )

    if os.path.getsize(
        archive_path
    ) == 0:
        raise RuntimeError(
            "Downloaded GitHub repository ZIP is empty."
        )

    # =========================================================
    # EXTRACT DIRECTORY
    # =========================================================

    extract_dir = os.path.join(
        destination_dir,
        "extracted"
    )

    os.makedirs(
        extract_dir,
        exist_ok=True
    )

    # =========================================================
    # EXTRACT ZIP
    # =========================================================

    with zipfile.ZipFile(
        archive_path,
        "r"
    ) as zip_file:

        zip_file.extractall(
            extract_dir
        )

    # =========================================================
    # FIND EXTRACTED REPOSITORY DIRECTORY
    # =========================================================

    extracted_items = [
        os.path.join(
            extract_dir,
            item
        )
        for item in os.listdir(
            extract_dir
        )
    ]

    directories = [
        item
        for item in extracted_items
        if os.path.isdir(item)
    ]

    # =========================================================
    # VALIDATE EXTRACTION
    # =========================================================

    if not directories:
        raise RuntimeError(
            "GitHub repository extraction failed."
        )

    # =========================================================
    # RETURN REPOSITORY DIRECTORY
    # =========================================================

    return directories[0]



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
# ZIP BACKUP HELPERS
# =========================================================
def zip_directory(source_dir, output_zip, excluded_dirs=None, excluded_files=None):
    """
    Create a ZIP backup of a directory while excluding
    sensitive/unnecessary files and folders.
    """

    excluded_dirs = excluded_dirs or set()
    excluded_files = excluded_files or set()

    source_dir = os.path.abspath(source_dir)
    output_zip = os.path.abspath(output_zip)

    with zipfile.ZipFile(
        output_zip,
        "w",
        zipfile.ZIP_DEFLATED
    ) as zipf:

        for root, dirs, files in os.walk(source_dir):

            # Remove excluded directories from traversal
            dirs[:] = [
                d for d in dirs
                if d not in excluded_dirs
            ]

            for file in files:

                # Explicit file exclusions
                if file in excluded_files:
                    continue

                # Extension exclusions
                if file.endswith((
                    ".pyc",
                    ".db",
                    ".log"
                )):
                    continue

                # Environment / secret files
                if file == ".env":
                    continue

                # ngrok files
                if file.startswith("ngrok"):
                    continue

                full_path = os.path.join(root, file)

                # Never include the ZIP being created
                if os.path.abspath(full_path) == output_zip:
                    continue

                arcname = os.path.relpath(
                    full_path,
                    source_dir
                )

                zipf.write(full_path, arcname)

    return output_zip

def upload_zip_backup_to_supabase(
    filepath,
    storage_path
):
    """
    Upload ZIP backup to Supabase Storage
    and return the actual Supabase storage path.
    """

    try:

        supabase = get_supabase_client()

        with open(
            filepath,
            "rb"
        ) as file:

            file_data = file.read()

        supabase.storage.from_(
            SUPABASE_BACKUP_BUCKET
        ).upload(
            storage_path,
            file_data,
            {
                "content-type": "application/zip",
                "upsert": "true"
            }
        )

        return storage_path

    except Exception as e:

        print(
            "SUPABASE ZIP UPLOAD ERROR:",
            e
        )

        return None

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

# =========================================================
# CREATE BACKEND BACKUP
# =========================================================

def create_backend_backup():

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    filename = safe_filename(
        f"smart_gym_backend_backup_{timestamp}.zip"
    )

    filepath = os.path.join(
        BACKUP_DIR,
        filename
    )

    storage_path = None

    try:

        # =================================================
        # DOWNLOAD BACKEND FROM GITHUB
        # =================================================

        with tempfile.TemporaryDirectory() as temp_dir:

            backend_dir = download_github_repository(
                GITHUB_BACKEND_URL,
                temp_dir
            )

            # =================================================
            # CREATE ZIP
            # =================================================

            zip_directory(
                backend_dir,
                filepath,

                excluded_dirs={
                    ".git",
                    "venv",
                    "__pycache__",
                    "backups"
                },

                excluded_files={
                    ".env"
                }
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

        storage_path = upload_zip_backup_to_supabase(
            filepath,
            filename
        )

        if not storage_path:

            raise RuntimeError(
                "Backend backup upload to Supabase failed."
            )

        print(
            "SUPABASE BACKEND BACKUP SUCCESS:",
            storage_path
        )

        return {
            "success": True,

            "filename": filename,

            "filepath": storage_path,

            "storage_path": storage_path,

            "file_size": file_size,

            "backup_type": "backend",

            "created_at":
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
        }

    except Exception as e:

        if os.path.exists(filepath):

            try:
                os.remove(filepath)
            except Exception:
                pass

        if storage_path:

            delete_supabase_backup(
                storage_path
            )

        print(
            "BACKEND BACKUP ERROR:",
            e
        )

        return {
            "success": False,
            "error": str(e)
        }

    
# =========================================================
# CREATE FRONTEND BACKUP
# =========================================================

def create_frontend_backup():

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    filename = safe_filename(
        f"smart_gym_frontend_backup_{timestamp}.zip"
    )

    filepath = os.path.join(
        BACKUP_DIR,
        filename
    )

    storage_path = None

    try:

        # =================================================
        # DOWNLOAD FRONTEND FROM GITHUB
        # =================================================

        with tempfile.TemporaryDirectory() as temp_dir:

            frontend_dir = download_github_repository(
                GITHUB_FRONTEND_URL,
                temp_dir
            )

            # =================================================
            # CREATE ZIP
            # =================================================

            zip_directory(
                frontend_dir,
                filepath,

                excluded_dirs={
                    ".git"
                },

                excluded_files={
                    ".env"
                }
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

        storage_path = upload_zip_backup_to_supabase(
            filepath,
            filename
        )

        if not storage_path:

            raise RuntimeError(
                "Frontend backup upload to Supabase failed."
            )

        print(
            "SUPABASE FRONTEND BACKUP SUCCESS:",
            storage_path
        )

        return {
            "success": True,

            "filename": filename,

            "filepath": storage_path,

            "storage_path": storage_path,

            "file_size": file_size,

            "backup_type": "frontend",

            "created_at":
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
        }

    except Exception as e:

        if os.path.exists(filepath):

            try:
                os.remove(filepath)
            except Exception:
                pass

        if storage_path:

            delete_supabase_backup(
                storage_path
            )

        print(
            "FRONTEND BACKUP ERROR:",
            e
        )

        return {
            "success": False,
            "error": str(e)
        }


# =========================================================
# =========================================================
# CREATE FULL SYSTEM BACKUP
# =========================================================

def create_full_system_backup():

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    filename = safe_filename(
        f"smart_gym_full_system_backup_{timestamp}.zip"
    )

    filepath = os.path.join(
        BACKUP_DIR,
        filename
    )

    storage_path = None
    database_result = None

    try:

        # =================================================
        # TEMPORARY GITHUB SOURCES
        # =================================================

        with tempfile.TemporaryDirectory() as temp_dir:

            # ---------------------------------------------
            # DOWNLOAD BACKEND
            # ---------------------------------------------

            backend_dir = download_github_repository(
                GITHUB_BACKEND_URL,
                os.path.join(
                    temp_dir,
                    "backend"
                )
            )

            # ---------------------------------------------
            # DOWNLOAD FRONTEND
            # ---------------------------------------------

            frontend_dir = download_github_repository(
                GITHUB_FRONTEND_URL,
                os.path.join(
                    temp_dir,
                    "frontend"
                )
            )

            # =================================================
            # CREATE DATABASE BACKUP
            # =================================================

            database_result = create_database_backup()

            if not database_result.get(
                "success"
            ):

                raise RuntimeError(
                    "Database backup failed: "
                    + str(
                        database_result.get(
                            "error"
                        )
                    )
                )

            database_sql_path = os.path.join(
                BACKUP_DIR,
                database_result["filename"]
            )

            if not os.path.exists(
                database_sql_path
            ):

                raise RuntimeError(
                    "Database SQL file was not found locally."
                )

            # =================================================
            # CREATE FULL SYSTEM ZIP
            # =================================================

            with zipfile.ZipFile(
                filepath,
                "w",
                compression=zipfile.ZIP_DEFLATED
            ) as zip_file:

                # ---------------------------------------------
                # DATABASE
                # ---------------------------------------------

                zip_file.write(
                    database_sql_path,
                    os.path.join(
                        "database",
                        database_result["filename"]
                    )
                )

                # ---------------------------------------------
                # BACKEND
                # ---------------------------------------------

                for root, dirs, files in os.walk(
                    backend_dir
                ):

                    dirs[:] = [
                        directory
                        for directory in dirs
                        if directory not in {
                            ".git",
                            "venv",
                            "__pycache__",
                            "backups"
                        }
                    ]

                    for file_name in files:

                        if file_name == ".env":
                            continue

                        if file_name.endswith(
                            (
                                ".pyc",
                                ".db",
                                ".log"
                            )
                        ):
                            continue

                        if file_name.startswith(
                            "ngrok"
                        ):
                            continue

                        source_path = os.path.join(
                            root,
                            file_name
                        )

                        relative_path = os.path.relpath(
                            source_path,
                            backend_dir
                        )

                        zip_file.write(
                            source_path,
                            os.path.join(
                                "backend",
                                relative_path
                            )
                        )

                # ---------------------------------------------
                # FRONTEND
                # ---------------------------------------------

                for root, dirs, files in os.walk(
                    frontend_dir
                ):

                    dirs[:] = [
                        directory
                        for directory in dirs
                        if directory != ".git"
                    ]

                    for file_name in files:

                        if file_name == ".env":
                            continue

                        source_path = os.path.join(
                            root,
                            file_name
                        )

                        relative_path = os.path.relpath(
                            source_path,
                            frontend_dir
                        )

                        zip_file.write(
                            source_path,
                            os.path.join(
                                "frontend",
                                relative_path
                            )
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

        storage_path = upload_zip_backup_to_supabase(
            filepath,
            filename
        )

        if not storage_path:

            raise RuntimeError(
                "Full System backup upload to Supabase failed."
            )

        print(
            "SUPABASE FULL SYSTEM BACKUP SUCCESS:",
            storage_path
        )

        return {
            "success": True,

            "filename": filename,

            "filepath": storage_path,

            "storage_path": storage_path,

            "file_size": file_size,

            "backup_type": "full_system",

            "database_backup":
                database_result["filename"],

            "created_at":
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
        }

    except Exception as e:

        if os.path.exists(filepath):

            try:
                os.remove(filepath)
            except Exception:
                pass

        if storage_path:

            delete_supabase_backup(
                storage_path
            )

        print(
            "FULL SYSTEM BACKUP ERROR:",
            e
        )

        return {
            "success": False,
            "error": str(e)
        }
