import cv2
import os
import time

def capture_faces(picam2, member_id, samples=10):

    # 🔥 FIX: absolute + safe path
    dataset_path = os.path.abspath("datasets/faces")
    os.makedirs(dataset_path, exist_ok=True)

    save_path = os.path.join(dataset_path, member_id)
    os.makedirs(save_path, exist_ok=True)

    print("Saving dataset to:", save_path)

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    print("FACE CAPTURE MODE")
    print("Waiting for face...")

    count = 0

    cv2.namedWindow("Face Enrollment", cv2.WINDOW_AUTOSIZE)
    cv2.moveWindow("Face Enrollment", 50, 50)

    time.sleep(1)

    while count < samples:

        try:
            frame = picam2.capture_array("main")
        except Exception as e:
            print("Camera read error:", e)
            time.sleep(0.05)
            continue

        if frame is None:
            continue

        # FIX: remove alpha
        if len(frame.shape) == 3 and frame.shape[2] == 4:
            frame = frame[:, :, :3]

        display = frame.copy()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.05,
            minNeighbors=3,
            minSize=(30, 30)
        )

        # =========================
        # NO FACE → WAIT
        # =========================
        if len(faces) == 0:

            cv2.putText(display, "NO FACE DETECTED",
                        (120, 240),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (0,0,255),
                        2)

            cv2.imshow("Face Enrollment", display)
            cv2.waitKey(1)
            continue

        # =========================
        # FACE FOUND
        # =========================
        faces = sorted(faces, key=lambda x: x[2]*x[3], reverse=True)
        (x,y,w,h) = faces[0]

        # =========================
        # NON-BLOCKING COUNTDOWN
        # =========================
        countdown = 3
        start_time = time.time()

        while countdown > 0:

            try:
                frame = picam2.capture_array("main")
            except:
                continue

            if frame is None:
                continue

            if len(frame.shape) == 3 and frame.shape[2] == 4:
                frame = frame[:, :, :3]

            display = frame.copy()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(100, 100)
            )

            if len(faces) > 0:
                (x,y,w,h) = faces[0]
                cv2.rectangle(display, (x,y), (x+w,y+h), (0,255,0), 2)

                cv2.putText(display, str(countdown),
                            (x + w//2 - 10, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1.5,
                            (0,255,255),
                            3)

            cv2.imshow("Face Enrollment", display)
            cv2.waitKey(1)

            if time.time() - start_time >= 1:
                countdown -= 1
                start_time = time.time()

        # =========================
        # CAPTURE (SAFE SAVE)
        # =========================
        # =========================
        # CAPTURE (SAFE SAVE)
        # =========================

        # =========================
        # CAPTURE (FULL FACE)
        # =========================

        padding = int(w * 0.25)  # 25% padding

        x1 = max(0, x - padding)
        y1 = max(0, y - padding)
        x2 = min(gray.shape[1], x + w + padding)
        y2 = min(gray.shape[0], y + h + padding)

        face_img = gray[y1:y2, x1:x2]

        # normalize lighting
        face_img = cv2.equalizeHist(face_img)

        # mas mataas resolution
        face_img = cv2.resize(face_img, (200, 200))

        count += 1

        filename = os.path.join(save_path, f"{count}.jpg")

        success = cv2.imwrite(filename, face_img)

        if success:
            print(f"Captured {count}/{samples} → {filename}")
        else:
            print("❌ Failed to save image")

        # flash effect
        flash = display.copy()
        flash[:] = 255
        cv2.imshow("Face Enrollment", flash)
        cv2.waitKey(100)

    cv2.destroyWindow("Face Enrollment")

    print("✅ Face capture complete.")

    return count

