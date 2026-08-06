from pathlib import Path

from sync.face_installer import install_face_package


UPLOAD_DIR = Path(__file__).resolve().parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)


def handle_face_sync(event):

    uploaded_file = event["file"]

    save_path = UPLOAD_DIR / uploaded_file.filename

    uploaded_file.save(save_path)

    # Install package
    install_face_package(save_path)
    from db.connection import get_connection

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    UPDATE sync_versions
    SET version = version + 1
    WHERE resource='face'
    """)

    connection.commit()

    cursor.close()
    connection.close()

    return {

        "success": True,

        "message": "Face package installed."

    }