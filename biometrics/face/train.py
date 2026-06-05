import os
import cv2
import numpy as np
import json


def train_faces():

    dataset_path = "datasets/faces"
    model_path = "biometrics/face/lbph_model.yml"
    labels_path = "biometrics/face/labels.json"

    os.makedirs("biometrics/face", exist_ok=True)

    if not os.path.exists(dataset_path):
        print("[ERROR] Dataset folder not found:", dataset_path)
        return

    try:
        recognizer = cv2.face.LBPHFaceRecognizer_create()
    except AttributeError:
        print("[ERROR] OpenCV face module not found")
        print("👉 Install: pip install opencv-contrib-python")
        return

    faces = []
    labels = []

    label_map = {}
    current_label = 0

    print("===================================")
    print("🚀 TRAINING FACE MODEL")
    print("===================================")

    for member_id in sorted(os.listdir(dataset_path)):

        member_folder = os.path.join(dataset_path, member_id)

        if not os.path.isdir(member_folder):
            continue

        print(f"[INFO] Processing: {member_id}")

        label_map[current_label] = member_id

        for image_name in sorted(os.listdir(member_folder)):

            image_path = os.path.join(member_folder, image_name)

            img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

            if img is None:
                print(f"[WARNING] Invalid image: {image_path}")
                continue

            # Normalize lighting
            img = cv2.equalizeHist(img)

            # Standard size
            img = cv2.resize(img, (200, 200))

            faces.append(img)
            labels.append(current_label)

        current_label += 1

    if len(faces) == 0:
        print("\n[ERROR] No face data found.")
        return

    print(f"\n[INFO] Total images: {len(faces)}")
    print("[INFO] Training model...")

    recognizer.train(faces, np.array(labels))

    recognizer.save(model_path)

    with open(labels_path, "w") as f:
        json.dump(label_map, f)

    print("\n===================================")
    print("✅ TRAINING COMPLETE")
    print("===================================")
    print(f"📁 Model  : {model_path}")
    print(f"🏷 Labels : {labels_path}")
    print("===================================\n")


if __name__ == "__main__":
    train_faces()