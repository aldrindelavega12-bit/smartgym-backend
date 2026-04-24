import cv2

class CameraStream:

    def __init__(self, picam2):
        self.picam2 = picam2

    def read(self):

        try:

            frame = self.picam2.capture_array("main")

            # remove alpha channel
            if frame.shape[2] == 4:
                frame = frame[:, :, :3]

            return frame

        except Exception as e:
            print("Camera error:", e)
            return None