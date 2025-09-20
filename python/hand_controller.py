import cv2
import mediapipe as mp
import time
import math

from arduino_connector import connect_to_arduino


BAUD_RATE = 9600
DEFAULT_ANGLES = [20, 20, 20, 20, 20]

# How far each finger moves toward its new angle every frame (0 to 1).
# Lower is smoother but slower to react. 1 turns smoothing off.
SMOOTHING = 0.35

# Seconds without seeing a hand before the robot hand opens back up.
LOST_HAND_DELAY = 1.5

arduino = connect_to_arduino(baud_rate=BAUD_RATE)

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)

if not cap.isOpened():
    arduino.close()
    raise RuntimeError(
        "The camera could not be opened. Check camera permissions "
        "or try changing VideoCapture(0) to VideoCapture(1)."
    )

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)


def distance(point_a, point_b):
    return math.sqrt(
        (point_a.x - point_b.x) ** 2
        + (point_a.y - point_b.y) ** 2
    )


def bend_from_distance(
    landmarks,
    tip_id,
    base_id,
    open_distance,
    closed_distance
):
    measured_distance = distance(
        landmarks[tip_id],
        landmarks[base_id]
    )

    bend = (
        (open_distance - measured_distance)
        / (open_distance - closed_distance)
    )

    bend = max(0, min(1, bend))

    return int(bend * 180)


target_angles = DEFAULT_ANGLES.copy()
smoothed_angles = [float(angle) for angle in DEFAULT_ANGLES]
angles = DEFAULT_ANGLES.copy()
last_seen_hand = time.time()
finger_names = ["Thumb", "Index", "Middle", "Ring", "Pinky"]
window_name = "Hand Controller"
while True:
    success, frame = cap.read()

    if not success:
        print("Camera stopped providing frames.")
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        hand_landmarks = result.multi_hand_landmarks[0]
        lm = hand_landmarks.landmark

        thumb = bend_from_distance(lm, 4, 9, 0.22, 0.10)
        index = bend_from_distance(lm, 8, 5, 0.18, 0.07)
        middle = bend_from_distance(lm, 12, 9, 0.18, 0.07)
        ring = bend_from_distance(lm, 16, 13, 0.17, 0.06)
        pinky = bend_from_distance(lm, 20, 17, 0.15, 0.05)

        target_angles = [
            max(20, min(160, angle))
            for angle in [thumb, index, middle, ring, pinky]
        ]
        last_seen_hand = time.time()

        mp_draw.draw_landmarks(
            frame,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS
        )

    hand_lost = (
        not result.multi_hand_landmarks
        and time.time() - last_seen_hand > LOST_HAND_DELAY
    )

    if hand_lost:
        target_angles = DEFAULT_ANGLES.copy()

    # Ease each finger toward its target instead of jumping straight there.
    smoothed_angles = [
        current + SMOOTHING * (target - current)
        for current, target in zip(smoothed_angles, target_angles)
    ]
    angles = [round(angle) for angle in smoothed_angles]

    data = ",".join(str(angle) for angle in angles) + "\n"
    arduino.write(data.encode())

    if result.multi_hand_landmarks:
        status = "Tracking hand"
    elif hand_lost:
        status = "No hand detected - opening hand"
    else:
        status = "No hand detected - holding position"

    cv2.putText(
        frame,
        status,
        (10, 40),
        cv2.FONT_HERSHEY_DUPLEX,
        0.8,
        (255, 255, 255),
        2
    )

    for i, name in enumerate(finger_names):
        cv2.putText(
            frame,
            f"{name}: {angles[i]} deg",
            (10, 80 + i * 30),
            cv2.FONT_HERSHEY_DUPLEX,
            0.65,
            (255, 255, 255),
            2
        )

    frame_height, frame_width = frame.shape[:2]

    cv2.putText(
        frame,
        "Press Q to quit",
        (10, frame_height - 20),
        cv2.FONT_HERSHEY_DUPLEX,
        0.6,
        (255, 255, 255),
        2
    )

    cv2.imshow(window_name, frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        arduino.write(b"20,20,20,20,20\n")
        break

    if cv2.getWindowProperty(
        window_name,
        cv2.WND_PROP_VISIBLE
    ) < 1:
        arduino.write(b"20,20,20,20,20\n")
        break

    time.sleep(0.03)

hands.close()
cap.release()
cv2.destroyAllWindows()
arduino.close()