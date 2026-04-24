import cv2
import json


class FaceRecognizer:

    def __init__(self):

        self.model = cv2.face.LBPHFaceRecognizer_create()
        self.model.read("biometrics/face/lbph_model.yml")

        with open("biometrics/face/labels.json", "r") as f:
            self.labels = json.load(f)

        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades +
            "haarcascade_frontalface_default.xml"
        )

        print("FACE ENGINE READY")

    def recognize(self, frame):

        if frame is None:
            return None

        # 🔥 DO NOT TOUCH COLOR (already BGR from UI)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=4,
            minSize=(80, 80)
        )

        best_match = None
        best_conf = 999

        for (x, y, w, h) in faces:

            face_img = gray[y:y+h, x:x+w]
            face_img = cv2.resize(face_img, (100, 100))

            label, confidence = self.model.predict(face_img)

            # lower = better
            if confidence < best_conf:
                best_conf = confidence
                best_match = label

        # 🔥 tighter threshold (better accuracy)
        if best_match is not None and 60 <= best_conf <= 200:

            user_id = self.labels.get(str(best_match))

            if user_id:
                return user_id

        return None
