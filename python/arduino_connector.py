import time

import serial
from serial.tools import list_ports


EXPECTED_RESPONSE = "ROBOTIC_HAND_CONTROLLER"


def try_port(port_name, baud_rate=9600, startup_delay=2.0):
    connection = None

    try:
        connection = serial.Serial(
            port=port_name,
            baudrate=baud_rate,
            timeout=1
        )

        time.sleep(startup_delay)

        connection.reset_input_buffer()
        connection.write(b"IDENTIFY\n")
        connection.flush()

        response = connection.readline().decode(
            errors="ignore"
        ).strip()

        if response == EXPECTED_RESPONSE:
            return connection

    except serial.SerialException:
        pass

    if connection is not None and connection.is_open:
        connection.close()

    return None


def connect_to_arduino(baud_rate=9600):
    ports = list(list_ports.comports())

    if not ports:
        raise RuntimeError(
            "No serial devices were found. Connect the Arduino and try again."
        )

    print("Searching for the robotic hand controller...")

    for port in ports:
        print(f"Testing {port.device}: {port.description}")

        connection = try_port(
            port_name=port.device,
            baud_rate=baud_rate
        )

        if connection is not None:
            print(f"Robotic hand controller found on {port.device}.")
            return connection

    raise RuntimeError(
        "The robotic hand controller was not found. "
        "Make sure the correct Arduino sketch is uploaded "
        "and that Serial Monitor is closed."
    )