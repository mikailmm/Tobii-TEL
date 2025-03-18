import tkinter as tk
from tkinter import messagebox
import argparse
import subprocess
import time

import pyaudio
import pandas as pd
import pywinauto
import tobii_research as tr
from mss import mss
from pydub import AudioSegment
from pydub.playback import play
from pywinauto import application


# Function to perform the CLI logic (with the GUI inputs)
def run_eye_tracking():
    # Get values from GUI
    calibrate = calibrate_var.get()
    duration = int(duration_var.get())
    beep = beep_var.get()
    window_name = window_name_var.get()
    output_csv = output_csv_var.get()
    save_screenshot = save_screenshot_var.get()

    try:
        # 1. Calibrate Tobii Eye Tracker
        if calibrate:
            subprocess.run([r"C:\Users\PC 7\AppData\Local\Programs\TobiiProEyeTrackerManager\TobiiProEyeTrackerManager.exe",
                            "--mode=usercalibration",
                            "--device-sn=TPNA1-030109959122"])

        def gaze_data_callback(gaze_data):
            print(f"Left eye: ({gaze_data['left_gaze_point_on_display_area']}) \t Right eye: ({gaze_data['right_gaze_point_on_display_area']})")
            data.append(gaze_data)

        def save_to_csv(data, name):
            df = pd.DataFrame(data=data)
            df[['left_X', 'left_y']] = df['left_gaze_point_on_display_area'].to_list()
            df[['right_X', 'right_y']] = df['right_gaze_point_on_display_area'].to_list()
            df.to_csv(f'Output/{name}.csv', index=False)

        # 2. Beep if necessary
        if beep:
            song = AudioSegment.from_wav("Resources/beep.wav")
            play(song)
        else:
            time.sleep(1)

        # 3. Get application window, set focus, and maximize
        app = application.Application()
        handle = pywinauto.findwindows.find_windows(title_re=f".+{window_name}$")[0]
        app.connect(handle=handle)
        window = app.window(handle=handle)
        window.maximize()
        window.set_focus()

        # 4. Collect data
        data = []
        eyetracker = tr.find_all_eyetrackers()[0]
        eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)
        time.sleep(duration)

        # Screenshot
        with mss() as sct:
            sct.shot(output=f'Output/{save_screenshot}')

        save_to_csv(data=data, name=output_csv)
        eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, gaze_data_callback)

        # Show success message
        messagebox.showinfo("Success", f"Data saved to Output/{output_csv}.csv\nScreenshot saved to Output/{save_screenshot}")
    
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


# Create the main window
root = tk.Tk()
root.title("Eye Tracking GUI")

# Create variables to hold values from GUI
calibrate_var = tk.BooleanVar()
beep_var = tk.BooleanVar()
window_name_var = tk.StringVar()
output_csv_var = tk.StringVar()
save_screenshot_var = tk.StringVar()
duration_var = tk.StringVar(value="5")

# Create UI elements
calibrate_check = tk.Checkbutton(root, text="Calibrate", variable=calibrate_var)
calibrate_check.grid(row=0, column=0, sticky="w")

beep_check = tk.Checkbutton(root, text="Play Beep", variable=beep_var)
beep_check.grid(row=1, column=0, sticky="w")

window_name_label = tk.Label(root, text="Window Name:")
window_name_label.grid(row=2, column=0, sticky="w")
window_name_entry = tk.Entry(root, textvariable=window_name_var)
window_name_entry.grid(row=2, column=1, sticky="w")
window_name_var.set("Chrome")  # default value

output_csv_label = tk.Label(root, text="Output CSV Name:")
output_csv_label.grid(row=3, column=0, sticky="w")
output_csv_entry = tk.Entry(root, textvariable=output_csv_var)
output_csv_entry.grid(row=3, column=1, sticky="w")

save_screenshot_label = tk.Label(root, text="Screenshot Name:")
save_screenshot_label.grid(row=4, column=0, sticky="w")
save_screenshot_entry = tk.Entry(root, textvariable=save_screenshot_var)
save_screenshot_entry.grid(row=4, column=1, sticky="w")

duration_label = tk.Label(root, text="Duration (seconds):")
duration_label.grid(row=5, column=0, sticky="w")
duration_entry = tk.Entry(root, textvariable=duration_var)
duration_entry.grid(row=5, column=1, sticky="w")

# Button to run the eye tracking process
run_button = tk.Button(root, text="Start Eye Tracking", command=run_eye_tracking)
run_button.grid(row=6, column=0, columnspan=2)

# Run the Tkinter main loop
root.mainloop()
