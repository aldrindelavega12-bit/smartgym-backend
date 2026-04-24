import cv2

# Initialize Camera
cap = cv2.VideoCapture(0)

# Create Window and Force Fullscreen
cv2.namedWindow("SmartGym_Mirror", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("SmartGym_Mirror", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

print("--- Smart Gym System: ACTIVE ---")
print("Press 'q' in this terminal to exit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 1. Rotate 90 degrees clockwise (Para sa portrait monitor)
    # 2. Flip horizontally (Para maging parang salamin)
    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    frame = cv2.flip(frame, 1)

    # Ipakita ang frame sa window
    cv2.imshow("SmartGym_Mirror", frame)

    # Exit mechanism
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
