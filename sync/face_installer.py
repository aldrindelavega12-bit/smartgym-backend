from pathlib import Path
import shutil
import zipfile


PROJECT_ROOT = Path(__file__).resolve().parent.parent

UPLOAD_DIR = PROJECT_ROOT / "sync" / "uploads"

FACE_DATASET = PROJECT_ROOT / "datasets" / "faces"

ENCODINGS_FILE = PROJECT_ROOT / "biometrics" / "face" / "encodings.pkl"


def install_face_package(zip_path):

    zip_path = Path(zip_path)

    extract_dir = UPLOAD_DIR / zip_path.stem

    if extract_dir.exists():

        shutil.rmtree(extract_dir)

    extract_dir.mkdir()

    # Extract ZIP
    with zipfile.ZipFile(zip_path, "r") as zip_ref:

        zip_ref.extractall(extract_dir)

    # Replace encodings first
    encodings = extract_dir / "encodings.pkl"

    if not encodings.exists():

        raise Exception("encodings.pkl not found.")

    shutil.copy2(

        encodings,

        ENCODINGS_FILE

    )

    # Optional member folder (FULL package only)
    member_dirs = [

        d for d in extract_dir.iterdir()

        if d.is_dir()

    ]

    if len(member_dirs) == 1:

        member_dir = member_dirs[0]

        destination = FACE_DATASET / member_dir.name

        if destination.exists():

            shutil.rmtree(destination)

        shutil.copytree(

            member_dir,

            destination

        )

    elif len(member_dirs) > 1:

        raise Exception("Invalid face package.")
        # Cleanup
    if extract_dir.exists():

        shutil.rmtree(extract_dir)

    if zip_path.exists():

        zip_path.unlink()

    return True
    
def remove_face_package(member_id):

    member_dir = FACE_DATASET / member_id

    if member_dir.exists():

        shutil.rmtree(member_dir)

    return True