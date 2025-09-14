#include <Servo.h>

Servo thumbServo;
Servo indexServo;
Servo middleServo;
Servo ringServo;
Servo pinkyServo;

String inputString = "";

void setup() {
  Serial.begin(9600);

  thumbServo.attach(3);
  indexServo.attach(5);
  middleServo.attach(6);
  ringServo.attach(9);
  pinkyServo.attach(10);

  thumbServo.write(20);
  indexServo.write(20);
  middleServo.write(160);
  ringServo.write(30);
  pinkyServo.write(160);
}

void loop() {
  while (Serial.available() > 0) {
    char c = Serial.read();

    if (c == '\r') {
      continue;
    }

    if (c == '\n') {
      if (inputString == "IDENTIFY") {
        Serial.println("ROBOTIC_HAND_CONTROLLER");
      } else {
        processData(inputString);
      }

      inputString = "";
    } else {
      inputString += c;
    }
  }
}

void processData(String data) {
  int values[5];
  int valueIndex = 0;

  while (data.length() > 0 && valueIndex < 5) {
    int commaIndex = data.indexOf(',');

    if (commaIndex == -1) {
      values[valueIndex] = data.toInt();
      data = "";
    } else {
      values[valueIndex] =
          data.substring(0, commaIndex).toInt();

      data = data.substring(commaIndex + 1);
    }

    values[valueIndex] =
        constrain(values[valueIndex], 0, 180);

    valueIndex++;
  }

  if (valueIndex == 5) {
    int thumbAngle = values[0];
    int indexAngle = values[1];
    int middleAngle = 180 - values[2];
    int ringAngle = constrain(values[3] + 10, 0, 180);
    int pinkyAngle = 180 - values[4];

    thumbServo.write(thumbAngle);
    indexServo.write(indexAngle);
    middleServo.write(middleAngle);
    ringServo.write(ringAngle);
    pinkyServo.write(pinkyAngle);

    delay(10);
  }
}