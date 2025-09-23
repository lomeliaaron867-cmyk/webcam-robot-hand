# Assembly Guide

This guide provides general advice for assembling and calibrating the webcam-controlled robotic hand.

Because 3D-printed hand assembly and servo layouts can vary, some dimensions, tendon lengths, **elastic tension**, and mounting details may need to be adjusted for your specific build.

## Before Assembly

Before attaching the servos to the hand:

* Upload the Arduino firmware.
* Connect the servos according to the wiring diagram.
* Test each servo using the manual servo controller.
* Confirm which direction each servo moves.
* Move each servo to its intended starting position.

Do not attach tight tendon strings before verifying servo direction.

## Finger Assembly and Elastic Return

Each finger uses a rubber band or another elastic material to hold the finger segments together and help return the finger to its resting position.

For each finger:

1. Cut a length of rubber band or elastic cord.
2. Feed one end through one of the two large openings in the finger segments.
3. Feed the other end through the second opening so that the finger segments are fully connected.
4. Pass both ends through the corresponding holes in the hand or knuckle.
5. Tie the ends securely while keeping enough tension to hold the finger together without restricting movement.

If the rubber band is difficult to push through the hole near the knuckle, repeatedly twist the rubber band while inserting it.

A standard rubber band works adequately for the prototype. However, a stronger elastic cord or similar material can provide more consistent tension and help keep fingers that are not currently being actuated in their resting position.


## Servo Placement

Mount each servo securely so that it cannot rotate or shift under load.

Try to keep:

* servo horns accessible
* tendon paths as straight as possible
* wires away from moving parts
* enough clearance for the full range of motion

Loose servo mounts can cause inconsistent finger movement.

## Tendon Routing

Use a strong, low-stretch string such as fishing line or braided thread.

Route each tendon from the servo horn to the corresponding finger.

Avoid:

* sharp bends
* rubbing against rough printed surfaces
* loose sections that can snag

The tendon should be tight enough to move the finger, but not so tight that it pulls against the servo at rest.

## Initial Servo Position

Before connecting the tendons, move each servo to its configured open-hand position.

The current Arduino sketch uses different starting positions for some fingers because the servos are mounted in different orientations.

Verify the starting position before tightening the servo horn.

## Adjusting Tendon Tension

Attach the tendon with the finger in its open position.

Start with light tension.

After attaching it:

1. Move the servo through a small range.
2. Check whether the finger opens and closes smoothly.
3. Increase or reduce tendon tension as needed.
4. Confirm that the servo does not stall at either endpoint.

Do not immediately test the full 20° to 160° range with tightly attached tendons.

## Calibrating Each Finger

Use the manual servo controller to test each finger independently.

Adjust one finger at a time.

Look for:

* reversed motion
* incomplete opening
* incomplete closing
* servo buzzing
* excessive tendon tension
* fingers reaching their mechanical limit too early

Servo direction and offsets can be changed in the Arduino firmware.

Example direction reversal:

```cpp
servo.write(180 - value);
```

Example offset:

```cpp
int adjustedAngle = constrain(value + 10, 0, 180);
```

## Safe Motion Limits

The software currently limits normal commands to:

```text
20° to 160°
```

Your build may require a smaller range.

Reduce the range if:

* the servo buzzes near an endpoint
* the tendon becomes overly tight
* the finger reaches its mechanical limit early
* the servo horn presses against another part

## Power and Wiring

Use a separate regulated 5 V supply for the servos.

Do not power all five servos from the Arduino 5 V pin.

The Arduino ground and servo power-supply ground must be connected together.

A 470 µF to 1000 µF capacitor across the servo power rails can help reduce voltage dips and jitter.

## Common Assembly Problems

### Finger does not fully close

Possible causes:

* tendon is too loose
* servo range is too small
* servo horn is mounted at the wrong angle
* tendon path has too much friction

### Finger does not fully open

Possible causes:

* tendon is too tight
* return mechanism is too weak
* servo starting position is incorrect
* finger joint is binding

### Servo buzzes continuously

Possible causes:

* servo is pushing against a mechanical stop
* tendon is too tight
* servo angle exceeds the safe range
* power supply voltage is unstable

### Finger movement is inconsistent

Possible causes:

* loose servo mount
* flexible or stretching tendon
* friction in the printed joints
* loose electrical connection
* inadequate power supply

## Final Checks

Before running the webcam controller:

* confirm every servo moves in the correct direction
* verify that no servo stalls at its endpoints
* check that the tendons do not cross
* confirm that wires cannot be pulled into moving parts
* verify the external power supply is connected correctly
* test each finger manually
* test all five fingers together at low speed

Once the hand moves reliably under manual control, start the webcam controller.
