import cv2
import mediapipe as mp
import math

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.8,
    min_tracking_confidence=0.7
)

def joint_angle(a, b, c):
    """
    Finds the angle at point b using points a, b, and c.
    Example: for finger joints 5-6-7, it finds the angle at joint 6.
    """
    ab = (a.x - b.x, a.y - b.y)
    cb = (c.x - b.x, c.y - b.y)

    dot = ab[0] * cb[0] + ab[1] * cb[1]

    mag_ab = math.sqrt(ab[0] ** 2 + ab[1] ** 2)
    mag_cb = math.sqrt(cb[0] ** 2 + cb[1] ** 2)

    if mag_ab == 0 or mag_cb == 0:
        return 180

    cos_angle = dot / (mag_ab * mag_cb)
    cos_angle = max(-1, min(1, cos_angle))

    angle = math.degrees(math.acos(cos_angle))
    return angle

def finger_bend_from_joints(landmarks, mcp, pip, dip, tip):
    """
    Calculates a bend value from 0 to 180 for one finger.
    0 means mostly straight.
    180 means strongly bent.
    """
    pip_angle = joint_angle(landmarks[mcp], landmarks[pip], landmarks[dip])
    dip_angle = joint_angle(landmarks[pip], landmarks[dip], landmarks[tip])

    bend_amount = (180 - pip_angle) + (180 - dip_angle)

    # Tune this if values are too weak or too strong
    max_bend = 140

    bend = bend_amount / max_bend
    bend = max(0, min(1, bend))

    return int(bend * 180)

while True:
    success, frame = cap.read()

    if not success:
        print("Camera not found")
        break

    frame = cv2.flip(frame, 1)

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    finger_values = [0, 0, 0, 0, 0]
    status = "No hand detected"

    if result.multi_hand_landmarks:
        status = "Tracking hand"

        for hand_landmarks in result.multi_hand_landmarks:
            lm = hand_landmarks.landmark

            # Thumb is harder with a webcam, so this is a rough joint-angle estimate
            thumb = finger_bend_from_joints(lm, 1, 2, 3, 4)

            index = finger_bend_from_joints(lm, 5, 6, 7, 8)
            middle = finger_bend_from_joints(lm, 9, 10, 11, 12)
            ring = finger_bend_from_joints(lm, 13, 14, 15, 16)
            pinky = finger_bend_from_joints(lm, 17, 18, 19, 20)

            finger_values = [thumb, index, middle, ring, pinky]

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

    cv2.putText(
        frame,
        status,
        (10, 40),
        cv2.FONT_HERSHEY_DUPLEX,
        0.8,
        (255, 255, 255),
        2
    )

    finger_names = ["Thumb", "Index", "Middle", "Ring", "Pinky"]

    for i, name in enumerate(finger_names):
        cv2.putText(
            frame,
            f"{name}: {finger_values[i]}",
            (10, 80 + i * 30),
            cv2.FONT_HERSHEY_DUPLEX,
            0.7,
            (255, 255, 255),
            2
        )
    
    cv2.putText(
    frame,
    "Press Q to quit",
    (10, 455),
    cv2.FONT_HERSHEY_DUPLEX,
    0.6,
    (255, 255, 255),
    2
)

    cv2.imshow("Hand Tracking Test", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()