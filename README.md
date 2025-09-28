# Webcam Robot Hand

A robotic hand that copies your hand's movements using just a webcam, built with MediaPipe, Python, an Arduino Uno, and five servo motors.

---

The computer tracks your hand with MediaPipe, turns each finger's bend into a servo angle, and sends those angles to an Arduino Uno over USB. The Arduino then moves five servos connected to a 3D-printed hand.

## Features

* **Smooth Movement:** Each finger eases toward its new position instead of jumping there, so small wobbles in the tracking don't make the servos jitter. You can change how smooth it is with `SMOOTHING` in `python/hand_controller.py`.
* **Opens Back Up When Your Hand Leaves:** If the camera loses your hand for more than 1.5 seconds, the robot hand slowly opens instead of staying frozen. You can change the wait with `LOST_HAND_DELAY`.

* **Webcam Hand Tracking:** Tracks one hand in real time using MediaPipe and OpenCV.
* **Five-Finger Control:** Sends a separate value for the thumb, index, middle, ring, and pinky.
* **Automatic Arduino Detection:** Checks the connected serial ports and finds the right Arduino using a handshake.
* **Manual Servo Controller:** A window for testing and calibrating each finger on its own.
* **Diagnostic Programs:** Separate camera and hand-tracking tests.
* **Safe Servo Limits:** Keeps normal commands inside a set angle range.
* **Simple Windows Setup:** Scripts that create the Python environment and install everything for you.

For mechanical assembly, tendon routing, elastics, and servo calibration, see the [Assembly Guide](docs/assembly-guide.md).

## How It Works

```text
Webcam
   ↓
MediaPipe hand tracking
   ↓
Python finger calculations and smoothing
   ↓
USB serial communication
   ↓
Arduino Uno
   ↓
Five servo motors
   ↓
Robotic hand movement
```

## Getting Started

### 1. Gather the Parts

You will need:

* Arduino Uno (or Uno-compatible board)
* 5 × MG90S micro servos
* Computer with a webcam
* Breadboard
* Jumper wires
* Regulated 5 V, 3 A power supply
* USB cable
* 3D-printed robotic hand (`hardware/complete_hand.stl`)
* 5 rubber bands (or stronger elastic)
* String or fishing line
* Optional: 470 µF to 1000 µF capacitor (reduces servo jitter)

### 2. Wire the Electronics

| Finger | Arduino pin |
| ------ | ----------: |
| Thumb  |          D3 |
| Index  |          D5 |
| Middle |          D6 |
| Ring   |          D9 |
| Pinky  |         D10 |

The servos use an external regulated 5 V supply. See `hardware/hand_wiring_guide.png` for the diagram.

```text
External +5 V → servo red wires
External GND → servo brown or black wires
Arduino GND → external GND
Arduino digital pins → servo signal wires
```

**Do not power all five servos from the Arduino 5 V pin.**

The Arduino and the external servo supply must share a common ground.

### 3. Upload the Arduino Firmware

Open `arduino/robotic_hand_controller/robotic_hand_controller.ino` in the Arduino IDE, select the Arduino Uno, and upload the sketch.

The firmware:

* receives five comma-separated servo values
* controls the five servos
* reverses servos that are mounted the opposite way
* applies calibration offsets
* answers the Python identification handshake

Close the Arduino Serial Monitor before starting the Python controller.

### 4. Install the Python Software

This project uses Python 3.11.

Open the `python` folder and run:

```text
setup_windows.bat
```

The setup script creates a local virtual environment, updates pip, and installs OpenCV, MediaPipe, and PySerial.

### 5. Start the Hand Controller

Run:

```text
run_windows.bat
```

The program will:

1. Search for the Arduino.
2. Confirm that it's running the right firmware.
3. Open the webcam.
4. Track one hand.
5. Calculate and smooth five finger values.
6. Send those values to the Arduino.

Press `Q` or close the camera window to stop the program.

## Included Software

| File | What it does |
| ---- | ------------ |
| `python/hand_controller.py` | The main program. Tracks your hand and sends live finger values to the Arduino. |
| `python/manual_servo_control.py` | A window for testing and calibrating each finger, with change-all mode, open and close presets, and input checking. |
| `python/camera_test.py` | Checks whether OpenCV can open your webcam. |
| `python/hand_tracking_test.py` | Tests MediaPipe tracking and shows the finger values without needing the Arduino. |
| `python/arduino_connector.py` | Checks the serial ports and asks each device to identify itself. |

The connector sends `IDENTIFY`, and the right Arduino answers `ROBOTIC_HAND_CONTROLLER`.

## Tuning

These settings are at the top of `python/hand_controller.py`:

| Setting | Default | What it does |
| ------- | ------: | ------------ |
| `SMOOTHING` | `0.35` | How far each finger moves toward its new angle every frame. Lower is smoother but slower to react. `1` turns smoothing off. |
| `LOST_HAND_DELAY` | `1.5` | Seconds without a hand before the robot hand opens back up. |

## Calibration

Servo direction depends on how each servo is mounted.

A reversed servo can be fixed in the Arduino firmware:

```cpp
middleServo.write(180 - values[2]);
```

A mechanical offset can be added like this:

```cpp
int ringAngle = constrain(values[3] + 10, 0, 180);
```

Test every servo before tightening the tendon strings.

The default command range is 20° to 160°. Your build may need a smaller range.

## Repository Structure

```text
webcam-robot-hand/
│
├── arduino/
│   └── robotic_hand_controller/
│       └── robotic_hand_controller.ino
│
├── docs/
│   └── assembly-guide.md
│
├── hardware/
│   ├── complete_hand.stl
│   └── hand_wiring_guide.png
│
├── python/
│   ├── arduino_connector.py
│   ├── camera_test.py
│   ├── hand_controller.py
│   ├── hand_tracking_test.py
│   ├── manual_servo_control.py
│   ├── requirements.txt
│   ├── run_windows.bat
│   └── setup_windows.bat
│
├── .gitignore
├── LICENSE
└── README.md
```

## Current Limitations

* Thumb movement is more limited.
* Tracking gets less reliable when your hand turns sideways.
* Finger bend is measured in screen distance, so moving your hand closer to or farther from the camera changes the readings.
* MG90S servos don't give any force feedback.
* Servo calibration depends on how the hand is put together.
* There's no wrist movement.

## Ideas for Later

* Measure finger bend against palm size so camera distance doesn't matter
* A calibration step that fits the open and closed positions to your hand
* Wrist rotation
* Better thumb movement
* Force or current sensing

## Safety

* Don't power all five servos through the Arduino.
* Use a separate regulated 5 V servo supply.
* Connect the Arduino ground to the external supply ground.
* Unplug power before changing wiring.
* Don't force the servos or leave them stalled.
* Test servo direction before attaching tight tendons.

## License

This project is available under the MIT License. See `LICENSE`.
