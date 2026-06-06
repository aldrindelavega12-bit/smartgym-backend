import os
import cv2
import pickle
import face_recognition

def train_faces():

    ENCODINGS_FILE = "biometrics/face/encodings.pkl"
    DATASET = "datasets/faces"

    known_encodings = []
    known_ids = []

    for member_id in sorted(os.listdir(DATASET)):

        folder = os.path.join(DATASET, member_id)

        if not os.path.isdir(folder):
            continue

        print("Processing", member_id)

        for img_name in os.listdir(folder):

            path = os.path.join(folder, img_name)

            image = cv2.imread(path)

            if image is None:
                continue

            rgb = cv2.cvtColor(
                image,
                cv2.COLOR_BGR2RGB
            )

            encodings = face_recognition.face_encodings(rgb)

            if len(encodings) == 0:
                print("SKIPPED:", path)
                continue

            print("ENCODED:", path)

            known_encodings.append(
                encodings[0]
            )

            known_ids.append(
                member_id
            )

    data = {
        "encodings": known_encodings,
        "ids": known_ids
    }

    with open(ENCODINGS_FILE, "wb") as f:
        pickle.dump(data, f)

    print("DONE")
    print("TOTAL:", len(known_ids))


if __name__ == "__main__":
    train_faces()