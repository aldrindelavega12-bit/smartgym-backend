import cv2
import os
import pickle
import face_recognition

class FaceRecognizer:

    def __init__(self):

        self.data = None

        if os.path.exists(
            "biometrics/face/encodings.pkl"
        ):

            with open(
                "biometrics/face/encodings.pkl",
                "rb"
            ) as f:

                self.data = pickle.load(f)

            print(
                "[FACE] Encodings loaded"
            )

        else:

            print(
                "[FACE WARNING] encodings.pkl missing"
            )

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

            best_index = distances.argmin()

            best_distance = distances[
                best_index
            ]

            print(
                f"[FACE DISTANCE] {best_distance:.4f}"
            )

            if best_distance < 0.50:

                return {
                    "user_id":
                    self.data["ids"][best_index],

                    "confidence":
                    round(
                        (1-best_distance)*100,
                        2
                    )
                }

        return None
