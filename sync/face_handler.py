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

    return {

        "success": True,

        "message": "Face package installed."

    }