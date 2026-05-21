import os
import cv2
import numpy as np
import json


def train_faces():

    dataset_path = "datasets/faces"
    model_path = "biometrics/face/lbph_model.yml"
    labels_path = "biometrics/face/labels.json"

    # 🔥 AUTO CREATE FOLDER
    os.makedirs("biometrics/face", exist_ok=True)

    # 🔥 CHECK DATASET
    if not os.path.exists(dataset_path):
        print("[ERROR] Dataset folder not found:", dataset_path)
        return

    # 🔥 INIT RECOGNIZER
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

            # 🔥 READ IMAGE (GRAY)
            img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

            if img is None:
                print(f"[WARNING] Skipped invalid image: {image_path}")
                continue
            
            img = cv2.resize(img, (100, 100))

            faces.append(img)
            labels.append(current_label)

        current_label += 1

    # ❌ NO DATA
    if len(faces) == 0:
        print("\n[ERROR] No face data found.")
        return

    print(f"\n[INFO] Total images: {len(faces)}")
    print("[INFO] Training model...")

    # 🔥 TRAIN
    recognizer.train(faces, np.array(labels))

    # 🔥 SAVE MODEL
    recognizer.save(model_path)

    # 🔥 SAVE LABELS
    with open(labels_path, "w") as f:
        json.dump(label_map, f)

    print("\n===================================")
    print("✅ TRAINING COMPLETE")
    print("===================================")
    print(f"📁 Model  : {model_path}")
    print(f"🏷 Labels : {labels_path}")
    print("===================================\n")


# 🔥 MAIN ENTRY (IMPORTANT)
if __name__ == "__main__":
    train_faces()