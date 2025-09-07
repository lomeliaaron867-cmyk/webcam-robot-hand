import cv2

WINDOW_NAME = "Camera Test"

cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read()

    if not success:
        print("Camera not found")
        break

    cv2.imshow(WINDOW_NAME, frame)

    # Exit when q is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

    # Exit when the window's X button is clicked
    if cv2.getWindowProperty(
        WINDOW_NAME,
        cv2.WND_PROP_VISIBLE
    ) < 1:
        break

cap.release()
cv2.destroyAllWindows()