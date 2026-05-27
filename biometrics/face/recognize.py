import cv2
import json
import time
import os

class FaceRecognizer:

    def __init__(self):
        self.model = cv2.face.LBPHFaceRecognizer_create()
        self.model_ready = False

        model_path = "biometrics/face/lbph_model.yml"
        labels_path = "biometrics/face/labels.json"

        if os.path.exists(model_path):
            try:
                self.model.read(model_path)
                self.model_ready = True
                print("[FACE] Model loaded successfully.")
            except Exception as e:
                print("[FACE WARNING] Failed to load model:", e)
        else:
            print("[FACE WARNING] No lbph_model.yml found. Face recognition disabled.")

        if os.path.exists(labels_path):
            try:
                with open(labels_path, "r") as f:
                    self.labels = json.load(f)
            except Exception as e:
                print("[FACE WARNING] Failed to load labels:", e)
                self.labels = {}
        else:
            self.labels = {}
            print("[FACE WARNING] No labels.json found. Face recognition disabled.")

        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

        self.start_detect_time = None
        self.scan_printed = False

        print("FACE ENGINE READY")

    def reset_scan(self):
        self.start_detect_time = None
        self.scan_printed = False

    def is_real_human(self, face_img_gray):
        """
        ANTI-SPOOFING CHECK:
        Sinusukat ang texture at sharpness ng mukha gamit ang Laplacian Variance.
        Ang mga printed na papel o cellphone screens ay may mababang variance (< 60-80).
        Ang totoong mukha ng tao ay may natural na detalye at anino (> 100+).
        """
        variance = cv2.Laplacian(face_img_gray, cv2.CV_64F).var()
        
        # 📌 I-print sa terminal para makita niyo ang actual score habang nagte-test!
        print(f"[LIVENESS DEBUG] Texture Variance Score: {variance:.2f}")
        
        # THRESHOLD: Kung mas mababa sa 70, automatic LITRATO ito.
        # (Maaari niyo itong taasan sa 80 o babaan sa 60 depende sa ilaw ng gym niyo)
        if variance < 250.0:
            return False
        return True

    def recognize(self, frame):
        if frame is None:
            return None

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=5,
            minSize=(90, 90)
        )

        if len(faces) == 0:
            self.reset_scan()
            return None

        faces = sorted(faces, key=lambda f: f[2] * f[3], reverse=True)
        x, y, w, h = faces[0]

        ratio = w / h
        if ratio < 0.75 or ratio > 1.35:
            self.reset_scan()
            return None

        if self.start_detect_time is None:
            self.start_detect_time = time.time()

        elapsed = time.time() - self.start_detect_time

        # Bigyan ng 1.5 seconds para mag-stabilize ang frame bago mag-desisyon
        if elapsed < 1.5:
            if not self.scan_printed:
                print("[FACE SCANNING] Face detected, verifying...")
                self.scan_printed = True
            return None

        # Kunin ang mismong rehiyon ng mukha
        face_img = gray[y:y+h, x:x+w]
        face_img_resized = cv2.resize(face_img, (100, 100))

        # =====================================
        # 🔥 CRITICAL ANTI-SPOOFING STEP
        # =====================================
        if not self.is_real_human(face_img_resized):
            print("🚨 [SPOOF DETECTED] This is a printed picture or screen!")
            self.reset_scan()
            return "SPOOF" # Ibabalik ang "SPOOF" string para basahin ng main.py
        
        if not self.model_ready or not self.labels:
            print("[FACE WARNING] No face model/labels available.")
            self.reset_scan()
            return None

        try:
            label, confidence = self.model.predict(face_img_resized)
        except Exception as e:
            print("[FACE ERROR]", e)
            self.reset_scan()
            return None

        user_id = self.labels.get(str(label))
        print(f"[FACE CHECK] label={label} user_id={user_id} confidence={confidence:.2f}")

        self.reset_scan()

        if user_id:
            return {
                "user_id": user_id,
                "confidence": confidence
            }

        return None