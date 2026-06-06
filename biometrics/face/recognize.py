import cv2
import pickle
import numpy as np
import face_recognition
import os


class FaceRecognizer:

    def __init__(self):

        self.data = None

        encoding_file = "biometrics/face/encodings.pkl"

        if os.path.exists(encoding_file):

            with open(encoding_file, "rb") as f:
                self.data = pickle.load(f)

            print("[FACE] DLIB encodings loaded.")

        else:

            print("[FACE WARNING] encodings.pkl not found")

    def recognize(self, frame):

        if self.data is None:
            return None

        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        locations = face_recognition.face_locations(
            rgb,
            model="hog"
        )

        if len(locations) == 0:
            return None

        encodings = face_recognition.face_encodings(
            rgb,
            locations
        )

        for encoding in encodings:

            distances = face_recognition.face_distance(
                self.data["encodings"],
                encoding
            )

            best_index = np.argmin(distances)

            best_distance = distances[best_index]

            matched_id = self.data["ids"][best_index]

            print(
                f"[FACE MATCH] {matched_id} "
                f"distance={best_distance:.4f}"
            )

            if best_distance < 0.55:

                confidence = (
                    1.0 - best_distance
                ) * 100

                return {
                    "user_id": matched_id,
                    "confidence": round(
                        confidence,
                        2
                    )
                }

        return None