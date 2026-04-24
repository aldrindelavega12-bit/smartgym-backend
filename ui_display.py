import cv2
import time
import numpy as np
import threading

class UIDisplay:

    def __init__(self, camera):
        self.camera = camera

        self.status = "READY"
        self.name = ""

        self.running = False
        self.mode = "NORMAL"

        self.frame = None
        self.frozen_frame = None
        self.camera_active = True

        self.tick = 0
        
        self.frame_lock = threading.Lock()

    def set_status(self, text):
        self.status = text

    def set_name(self, name):
        self.name = name

    def set_mode(self, mode):
        self.mode = mode

        if mode == "ADMIN" and self.camera_active:
            frame = self.camera.capture_array()
            frame = cv2.flip(frame, 1)
            self.frozen_frame = frame.copy()

    def start(self):
        self.running = True
        threading.Thread(target=self.run, daemon=True).start()

    # 🔥 BIG CORNER BOX
    def draw_corner_box(self, frame, x1, y1, x2, y2, color):

        t = 6   # thickness
        l = 40  # length

        # TL
        cv2.line(frame, (x1,y1), (x1+l,y1), color, t)
        cv2.line(frame, (x1,y1), (x1,y1+l), color, t)

        # TR
        cv2.line(frame, (x2,y1), (x2-l,y1), color, t)
        cv2.line(frame, (x2,y1), (x2,y1+l), color, t)

        # BL
        cv2.line(frame, (x1,y2), (x1+l,y2), color, t)
        cv2.line(frame, (x1,y2), (x1,y2-l), color, t)

        # BR
        cv2.line(frame, (x2,y2), (x2-l,y2), color, t)
        cv2.line(frame, (x2,y2), (x2,y2-l), color, t)

    def run(self):

        cv2.namedWindow("Turnstile", cv2.WINDOW_NORMAL)
        cv2.moveWindow("Turnstile", 1920, 0)

        cv2.setWindowProperty(
            "Turnstile",
            cv2.WND_PROP_FULLSCREEN,
            cv2.WINDOW_FULLSCREEN
        )

        while self.running:

            self.tick += 1

            # =========================
            # FRAME SOURCE
            # =========================
            if not self.camera_active:

                frame = np.zeros((800, 480, 3), dtype=np.uint8)

                dots = "." * ((self.tick // 10) % 4)

                cv2.putText(frame, "FACE ENROLLMENT", (60, 350),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

                cv2.putText(frame, f"PROCESSING{dots}", (100, 450),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,255), 2)

            elif self.mode == "ADMIN":

                if self.frozen_frame is None:
                    frame = np.zeros((800, 480, 3), dtype=np.uint8)
                else:
                    frame = self.frozen_frame.copy()

            else:
                frame = self.camera.capture_array()

                # FIX COLOR (IMPORTANT)

                frame = cv2.flip(frame, 1)

                with self.frame_lock:
                    self.frame = frame.copy()

            # =========================
            # RESIZE (PORTRAIT)
            # =========================
            frame = cv2.resize(frame, (480, 800))

            # =========================
            # DARK OVERLAY
            # =========================
            overlay = frame.copy()
            cv2.rectangle(overlay, (0,0), (480,800), (0,0,0), -1)
            frame = cv2.addWeighted(overlay, 0.4, frame, 0.6, 0)

            # =========================
            # TITLE
            # =========================
            cv2.putText(frame, "SMART GYM",
                        (100, 60),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.1,
                        (255,255,255),
                        2)

            # =========================
            # BIG FACE GUIDE BOX
            # =========================
            x1, y1 = 60, 180
            x2, y2 = 420, 540

            self.draw_corner_box(frame, x1, y1, x2, y2, (0,255,150))

            # =========================
            # SCANNING TEXT
            # =========================
            dots = "." * ((self.tick // 10) % 4)

            cv2.putText(frame, f"SCANNING{dots}",
                        (150, 140),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (0,255,0),
                        2)

            # =========================
            # NAME DISPLAY (OPTIONAL)
            # =========================
            if self.name:
                cv2.putText(frame, self.name,
                            (90, 620),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.8,
                            (0,255,0),
                            2)

            # =========================
            # STATUS (BOTTOM CENTER)
            # =========================
            if "GRANTED" in self.status:
                color = (0,255,0)
            elif "DENIED" in self.status:
                color = (0,0,255)
            elif "VERIFYING" in self.status:
                color = (0,255,255)
            else:
                color = (255,255,255)

            cv2.putText(frame, self.status,
                        (80, 700),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.9,
                        color,
                        2)

            # =========================
            # FOOTER NOTE
            # =========================
            cv2.putText(frame,
                        "Note: Scan Fingerprint First (Members Only)",
                        (20, 770),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (200,200,200),
                        1)

            # =========================
            # DISPLAY
            # =========================
            cv2.imshow("Turnstile", frame)
            cv2.setWindowProperty("Turnstile", cv2.WND_PROP_TOPMOST, 1)
            cv2.waitKey(1)