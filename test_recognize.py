from biometrics.face.recognize import FaceRecognizer

recognizer = FaceRecognizer()
result = recognizer.recognize()

print("Recognized:", result)
