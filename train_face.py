import cv2
import os
import json
import numpy as np

# ================= PATHS =================
DATASET_PATH = "datasets/faces"
MODEL_PATH = "biometrics/face/lbph_model.yml"
LABELS_PATH = "biometrics/face/labels.json"

# ================= INIT =================
recognizer = cv2.face.LBPHFaceRecognizer_create()

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)

# ================= STORAGE =================
x_train = []
y_labels = []

labels = {}
current_id = 0

# ================= USERS =================
users = sorted(os.listdir(DATASET_PATH))

print("\n=== TRAINING STARTED ===\n")

for user_id in users:

    user_path = os.path.join(
        DATASET_PATH,
        user_id
    )

    if not os.path.isdir(user_path):
        continue

    print(f"[TRAINING] {user_id}")

    labels[current_id] = user_id

    for img_name in os.listdir(user_path):

        img_path = os.path.join(
            user_path,
            img_name
        )

        # ================= READ =================
        image = cv2.imread(img_path)

        if image is None:
            continue

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        # ================= DETECT =================
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(80, 80)
        )

        for (x, y, w, h) in faces:

            roi = gray[y:y+h, x:x+w]

            roi = cv2.resize(
                roi,
                (100, 100)
            )

            x_train.append(roi)
            y_labels.append(current_id)

    current_id += 1

# ================= TRAIN =================
if len(x_train) == 0:

    print("[ERROR] No faces found")
    exit()

recognizer.train(
    x_train,
    np.array(y_labels)
)

# ================= SAVE MODEL =================
os.makedirs(
    "biometrics/face",
    exist_ok=True
)

recognizer.save(MODEL_PATH)

# ================= SAVE LABELS =================
with open(LABELS_PATH, "w") as f:
    json.dump(labels, f)

print("\n=== TRAINING COMPLETE ===")
print("LABELS:", labels)
print("TOTAL FACES:", len(x_train))
print("MODEL SAVED ✔")
