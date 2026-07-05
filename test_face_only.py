import cv2
import pickle
import numpy as np
import face_recognition

from picamera2 import Picamera2
from biometrics.face.camera_stream import CameraStream

ENCODINGS_FILE = "biometrics/face/encodings.pkl"

print("Loading encodings...")

with open(ENCODINGS_FILE, "rb") as f:
    data = pickle.load(f)

print(f"Loaded {len(data['ids'])} face encodings.")

# ===========================
# Initialize Pi Camera
# ===========================

picam2 = Picamera2()

config = picam2.create_preview_configuration(
    main={"size": (640, 480)}
)

picam2.configure(config)
picam2.start()

camera = CameraStream(picam2)

print("Camera Started.")
print("Press Q to quit.\n")

while True:

    frame = camera.read()

    if frame is None:
        continue

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    locations = face_recognition.face_locations(
        rgb,
        model="hog"
    )

    encodings = face_recognition.face_encodings(
        rgb,
        locations
    )

    for (top, right, bottom, left), encoding in zip(locations, encodings):

        label = "UNKNOWN"
        color = (0, 0, 255)

        if len(data["encodings"]) > 0:

            distances = face_recognition.face_distance(
                data["encodings"],
                encoding
            )

            best_index = np.argmin(distances)
            best_distance = distances[best_index]

            if best_distance < 0.55:

                member_id = data["ids"][best_index]
                confidence = (1 - best_distance) * 100

                label = f"{member_id} ({confidence:.1f}%)"
                color = (0, 255, 0)

                print(
                    f"[MATCH] {member_id} "
                    f"distance={best_distance:.4f}"
                )

        cv2.rectangle(
            frame,
            (left, top),
            (right, bottom),
            color,
            2
        )

        cv2.putText(
            frame,
            label,
            (left, top - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            color,
            2
        )

    cv2.imshow("Standalone Face Test", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

picam2.stop()
cv2.destroyAllWindows()