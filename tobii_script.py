#!

import argparse
import subprocess
import time

import pyaudio
import pandas as pd
import pywinauto
import tobii_research as tr
import mss as mss
from pydub import AudioSegment
from pydub.playback import play
from pywinauto import application

from pathlib import Path

# Additional requirements:
# - PyAudio

required_debug = False


## Color for text
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# 1. Argparse
parser = argparse.ArgumentParser(
                    prog='EyeTracking',
                    description='Get eye tracking data',
                    epilog='2024 - PKL Team Mika, Lab T-EL, FILKOM Universtas Brawijaya')

parser.add_argument('--calibrate', action='store_true', help='whether to calibrate or not | kalibrasi  (disarankan kalibrasi untuk setiap subjek)')
parser.add_argument('--duration', '-d',  type=int, default=5,  help='duration in seconds | durasi dalam detik (default: 5)', required=required_debug)
parser.add_argument('--beep', action='store_true', help='play beep | mainkan suara')
parser.add_argument('--window-name', '-w',  default="Chrome",  help='pick window name to be focused | pilih nama window dari aplikasi (default: Chrome)')
parser.add_argument('--output-csv', '-o', default="data-temp.csv",  help='(default: data-temp.csv)', required=required_debug)
parser.add_argument('--save-screenshot', '-s', default="screen-temp.png",  help='(default: screen-temp.png)', required=required_debug)

args = parser.parse_args()

# 2. Calibrate Tobii Eye Tracker
if args.calibrate:
    my_file = Path.home().joinpath('AppData\Local\Programs\TobiiProEyeTrackerManager\TobiiProEyeTrackerManager.exe')
    try:
        if not my_file.is_file():
            raise FileNotFoundError
    except FileNotFoundError:
        exit(bcolors.FAIL + "FileNotFoundError: Tobii Pro doesn't exist | Tobii Pro belum diinstall\nExiting..." + bcolors.ENDC)
    # subprocess.run([r"$env:USERPROFILE\AppData\Local\Programs\TobiiProEyeTrackerManager\TobiiProEyeTrackerManager.exe",
    subprocess.run([my_file,
                    "--mode=usercalibration",
                    "--device-sn=TPNA1-030109959122",
                    "--screen=1"])

def gaze_data_callback(gaze_data):
    # Print gaze points of left and right eye
    print("Left eye: ({gaze_left_eye}) \t Right eye: ({gaze_right_eye})".format(
        gaze_left_eye=gaze_data['left_gaze_point_on_display_area'],
        gaze_right_eye=gaze_data['right_gaze_point_on_display_area']))
    # print(gaze_data)
    data.append(gaze_data)


def save_to_csv(data, name):
    df = pd.DataFrame(data=data)

    df[['left_X', 'left_y']] = df['left_gaze_point_on_display_area'].to_list()
    df[['right_X', 'right_y']] = df['right_gaze_point_on_display_area'].to_list()

    df.to_csv(f'Output/{name}', index=False)


# 3. Beep
if args.beep:
    song = AudioSegment.from_wav("Resources/beep.wav")
    play(song)
else:
    time.sleep(1)


# 4. Get application window, set focus, and maximize
app = application.Application()
window_name = args.window_name
handle = pywinauto.findwindows.find_windows(title_re=f".+{window_name}$")[0]
app.connect(handle=handle)
window = app.window(handle=handle)

window.maximize()
window.set_focus()
window.capture_as_image().save(f'Output/{args.save_screenshot}')



# 5. Collect data
data = []

eyetracker = tr.find_all_eyetrackers()[0]

eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)
time.sleep(args.duration)

# # Screenshot
# with mss() as sct:
#     sct.shot(output=f'Output/{args.save_screenshot}')

save_to_csv(data=data, name=args.output_csv)
eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, gaze_data_callback)

#n. Beep when finished
if args.beep:
    song = AudioSegment.from_wav("Resources/beep.wav")
    play(song)
else:
    time.sleep(1)

print(f"{args.output_csv} is saved in {bcolors.OKCYAN}Output/{args.output_csv}{bcolors.ENDC}")
print(f"Screenshot is saved in {bcolors.OKCYAN}Output/{args.save_screenshot}{bcolors.ENDC}")
