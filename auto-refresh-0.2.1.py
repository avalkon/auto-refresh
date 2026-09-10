# --- Auto-Refresh v0.2.0 by avalkon --- #
# ---Imports---#

import tkinter as tk
import threading
import time
import configparser
from pynput.mouse import Button, Controller
from python_imagesearch.imagesearch import imagesearch
from playsound3 import playsound
from pathlib import Path

# ---Configs--- #
#These can be changed via the config.ini without needing to make changes to this file.

config_file = Path(__file__).parent / "config.ini"

config = configparser.ConfigParser()
config.read(config_file)

def config_path(name):
    path = Path(config["files"][name])
    if path.is_absolute():
        return path
    return config_file.parent / path

nta = config_path("nta")
acqimg = config_path("acquire")
timers = [
    (config_path("submit1"), config.getfloat("confidence", "submit1")),
    (config_path("submit2"), config.getfloat("confidence", "submit2")),
    (config_path("submit3"), config.getfloat("confidence", "submit3")),
    (config_path("submit4"), config.getfloat("confidence", "submit4")),
    (config_path("submit5"), config.getfloat("confidence", "submit5")),
]
sound = config_path("sound")
icon = config_path("icon")

# ---Mouse positions--- #

def get_position(name):
    x, y = config["positions"][name].split(",")
    return int(x), int(y)

refpos = get_position("refresh")
acqpos = get_position("acquire")
subpos = get_position("submit")

# ---Timing--- #

refdel = config.getfloat("timing", "refresh")
acqdel = config.getfloat("timing", "acquire")
waitdel = config.getfloat("timing", "wait")
subdel = config.getfloat("timing", "submit")

# ---Status--- #

stopped = 0
refreshing = 1
acquiring = 2
waiting = 3
submitting = 4

mouse = Controller()
status = stopped
sound_on = True
auto_submit = False
worker_thread = None

# ---Definitions--- #

def set_status(value):
    global status
    status = value

def found(image, confidence=0.8):
    return imagesearch(image, confidence)[0] != -1

def submit_found():
    return any(found(image, confidence) for image, confidence in timers)

def sleep(seconds, state):
    end = time.monotonic() + seconds
    while time.monotonic() < end:
        if status != state:
            return False
        time.sleep(0.1)
    return True

def click(position):
    mouse.position = position
    mouse.click(Button.left)

def label(widget, text):
    root.after(0, lambda: widget.config(text=text))

def play_sound():
    if sound_on:
        playsound(sound)

# ---Jobs--- #

def worker():
    while status != stopped:
        if status == refreshing:
            refresh()
        elif status == acquiring:
            acquire()
        elif status == waiting:
            wait()
        elif status == submitting:
            submit()

def refresh():
    label(nta_label, "Checking...")
    label(submit_label, "Waiting")
    if not sleep(refdel, refreshing):
        return
    if found(nta):
        label(nta_label, "NTA")
        if not sleep(refdel, refreshing):
            return
        click(refpos)
    else:
        label(nta_label, "Not NTA!")
        set_status(acquiring)

def acquire():
    if not sleep(acqdel, acquiring):
        return
    if found(acqimg):
        label(nta_label, "Acquiring!")
        label(submit_label, "Waiting")
        click(acqpos)
        play_sound()
    else:
        label(nta_label, "Already acquired")
        label(submit_label, "Waiting")
    set_status(waiting)

def wait():
    label(submit_label, "Waiting")
    if found(nta):
        label(nta_label, "NTA")
        set_status(refreshing)
        return
    if found(acqimg):
        label(nta_label, "Acquiring")
        set_status(acquiring)
        return
    label(nta_label, "Task")
    sleep(waitdel, waiting)

def submit():
    if submit_found():
        label(submit_label, "Submitting!")
        if auto_submit:
            click(subpos)
        if not sleep(acqdel, submitting):
            return
        play_sound()
        set_status(refreshing)

    else:
        label(submit_label, "Waiting to submit")
        if not sleep(subdel, submitting):
            return
        label(submit_label, "Checking...")

# ---Job starters--- #

def start_worker():
    global worker_thread
    if worker_thread and worker_thread.is_alive():
        return
    worker_thread = threading.Thread(target=worker, daemon=True)
    worker_thread.start()

def start_refresh():
    set_status(refreshing)
    label(nta_label, "Starting...")
    label(submit_label, "Waiting")
    start_worker()

def start_submit():
    set_status(submitting)
    label(submit_label, "Checking...")
    start_worker()

def stop_all(event=None):
    set_status(stopped)
    nta_label.config(text="stopped")
    submit_label.config(text="stopped")
    checkthreads()

def checkthreads():
    threads_label.config(text=str(threading.active_count()))

# ---Settings--- #

def open_settings():
    global sound_on, auto_submit
    window = tk.Toplevel(root)
    window.title("Settings")
    window.geometry("190x160")
    settings_label = tk.Label(window, text="Settings")
    settings_label.grid(row=0, column=0, columnspan=2)

    sound_var = tk.StringVar(value="On" if sound_on else "Off")
    snd_label = tk.Label(window, text="Sound:")
    snd_label.grid(row=1, column=0)
    snd_menu = tk.OptionMenu(window, sound_var, "On", "Off")
    snd_menu.grid(row=1, column=1)

    submit_var = tk.StringVar(value="On" if auto_submit else "Off")
    sub_label = tk.Label(window, text="Auto-Submit Click:")
    sub_label.grid(row=2, column=0)
    sub_menu = tk.OptionMenu(window, submit_var, "On", "Off")
    sub_menu.grid(row=2, column=1)

    def save():
        global sound_on, auto_submit
        sound_on = sound_var.get() == "On"
        auto_submit = submit_var.get() == "On"
        window.destroy()

    save_button = tk.Button(window, text="Save", width=16, command=save)
    save_button.grid(row=3, column=0, columnspan=2)

# ---Main window--- #

root = tk.Tk()
root.title("Auto-Refresh v0.2.0")
root.geometry("313x185+990+540")
root.minsize(313, 185)
root.iconphoto(True, tk.PhotoImage(file=icon))

# ---Buttons--- #

refresh_button = tk.Button(root, text="Start Auto-Refresh", width=16, command=start_refresh)
refresh_button.grid(row=0, column=0)

submit_button = tk.Button(root, text="Auto-Submit", width=16, command=start_submit)
submit_button.grid(row=0, column=1)

stop_button = tk.Button(root, text="Stop", width=16, command=stop_all)
stop_button.grid(row=2, column=0, columnspan=2)
root.bind("<F12>", stop_all)

thread_button = tk.Button(root, text="Get Threadcount", width=16, command=checkthreads)
thread_button.grid(row=4, column=0)

settings_button = tk.Button(root, text="Settings", width=16, command=open_settings)
settings_button.grid(row=5, column=0, columnspan=2)

# ---Labels--- #

nta_label = tk.Label(root, text="stopped", width=16)
nta_label.grid(row=1, column=0)

submit_label = tk.Label(root, text="Waiting", width=16)
submit_label.grid(row=1, column=1)

threads_label = tk.Label(root, text="Threadcount")
threads_label.grid(row=4, column=1)

credit_label = tk.Label(root, text="Auto-Refresh v0.2.0, by avalkon")
credit_label.grid(row=6, column=0, columnspan=2)

# ---Exit strategy(Not that you need one in this job, they'll do it for you with zero warning!)--- #
def close_program():
    global status
    status = stopped
    root.destroy()
root.protocol("WM_DELETE_WINDOW", close_program)
root.mainloop()
