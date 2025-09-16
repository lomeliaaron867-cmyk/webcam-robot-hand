import tkinter as tk
from tkinter import ttk, messagebox

from arduino_connector import connect_to_arduino


BAUD_RATE = 9600
MIN_ANGLE = 20
MAX_ANGLE = 160

OPEN_POSITION = [20, 20, 20, 20, 20]
CLOSED_POSITION = [160, 160, 160, 160, 160]

arduino = connect_to_arduino(baud_rate=BAUD_RATE)


def send_angles():
    """Read, validate, and send all five servo angles."""
    try:
        angles = [int(entry.get()) for entry in entries]

        if any(
            angle < MIN_ANGLE or angle > MAX_ANGLE
            for angle in angles
        ):
            raise ValueError

        message = ",".join(str(angle) for angle in angles) + "\n"
        arduino.write(message.encode())

        status_variable.set(
            "Sent: " + ", ".join(str(angle) for angle in angles)
        )

    except ValueError:
        messagebox.showerror(
            "Invalid value",
            f"Enter whole numbers from {MIN_ANGLE} to {MAX_ANGLE}."
        )


def set_entries(angles):
    """Replace all five entry values."""
    for entry, angle in zip(entries, angles):
        entry.delete(0, tk.END)
        entry.insert(0, str(angle))


def synchronize_entries(event):
    """Copy one edited value into every field when Change All is enabled."""
    if not change_all_enabled.get():
        return

    edited_entry = event.widget
    value = edited_entry.get()

    for entry in entries:
        if entry is not edited_entry:
            entry.delete(0, tk.END)
            entry.insert(0, value)


def open_hand():
    set_entries(OPEN_POSITION)
    send_angles()


def close_hand():
    set_entries(CLOSED_POSITION)
    send_angles()


def close_program():
    """Open the hand, close serial, and exit."""
    try:
        arduino.write(b"20,20,20,20,20\n")
    finally:
        if arduino.is_open:
            arduino.close()

        window.destroy()


window = tk.Tk()
window.title("Robotic Hand Controller")
window.resizable(False, False)

# Main window spacing
window.configure(padx=22, pady=20)

style = ttk.Style()

# Use a cleaner built-in theme when available
available_themes = style.theme_names()

if "vista" in available_themes:
    style.theme_use("vista")
elif "clam" in available_themes:
    style.theme_use("clam")

style.configure(
    "Title.TLabel",
    font=("Segoe UI", 15, "bold")
)

style.configure(
    "Subtitle.TLabel",
    font=("Segoe UI", 9)
)

style.configure(
    "Finger.TLabel",
    font=("Segoe UI", 10)
)

style.configure(
    "Status.TLabel",
    font=("Segoe UI", 9)
)

style.configure(
    "Primary.TButton",
    font=("Segoe UI", 10, "bold"),
    padding=(12, 8)
)

style.configure(
    "Secondary.TButton",
    font=("Segoe UI", 10),
    padding=(12, 7)
)


main_frame = ttk.Frame(window)
main_frame.grid(row=0, column=0)


title_label = ttk.Label(
    main_frame,
    text="Manual Servo Control",
    style="Title.TLabel"
)
title_label.grid(
    row=0,
    column=0,
    columnspan=2,
    pady=(0, 4)
)


subtitle_label = ttk.Label(
    main_frame,
    text=f"Enter an angle from {MIN_ANGLE}° to {MAX_ANGLE}°",
    style="Subtitle.TLabel"
)
subtitle_label.grid(
    row=1,
    column=0,
    columnspan=2,
    pady=(0, 18)
)


finger_frame = ttk.LabelFrame(
    main_frame,
    text="Finger angles",
    padding=(16, 12)
)
finger_frame.grid(
    row=2,
    column=0,
    columnspan=2,
    sticky="ew"
)


finger_names = [
    "Thumb",
    "Index",
    "Middle",
    "Ring",
    "Pinky"
]

entries = []

for row, finger_name in enumerate(finger_names):
    label = ttk.Label(
        finger_frame,
        text=finger_name,
        style="Finger.TLabel"
    )
    label.grid(
        row=row,
        column=0,
        padx=(0, 16),
        pady=6,
        sticky="e"
    )

    entry = ttk.Entry(
        finger_frame,
        width=9,
        justify="center",
        font=("Segoe UI", 10)
    )
    entry.insert(0, "20")
    entry.grid(
        row=row,
        column=1,
        pady=6
    )

    entry.bind("<KeyRelease>", synchronize_entries)

    entries.append(entry)


change_all_enabled = tk.BooleanVar(value=False)

change_all_checkbox = ttk.Checkbutton(
    main_frame,
    text="Change all fingers together",
    variable=change_all_enabled
)
change_all_checkbox.grid(
    row=3,
    column=0,
    columnspan=2,
    pady=(14, 16)
)


send_button = ttk.Button(
    main_frame,
    text="Send Values",
    command=send_angles,
    style="Primary.TButton"
)
send_button.grid(
    row=4,
    column=0,
    columnspan=2,
    sticky="ew",
    pady=(0, 8)
)


open_button = ttk.Button(
    main_frame,
    text="Open Hand",
    command=open_hand,
    style="Secondary.TButton"
)
open_button.grid(
    row=5,
    column=0,
    padx=(0, 4),
    sticky="ew"
)


close_button = ttk.Button(
    main_frame,
    text="Close Hand",
    command=close_hand,
    style="Secondary.TButton"
)
close_button.grid(
    row=5,
    column=1,
    padx=(4, 0),
    sticky="ew"
)


status_variable = tk.StringVar(
    value="Connected and ready"
)

status_label = ttk.Label(
    main_frame,
    textvariable=status_variable,
    style="Status.TLabel",
    anchor="center"
)
status_label.grid(
    row=6,
    column=0,
    columnspan=2,
    pady=(16, 0),
    sticky="ew"
)


window.protocol(
    "WM_DELETE_WINDOW",
    close_program
)

window.mainloop()