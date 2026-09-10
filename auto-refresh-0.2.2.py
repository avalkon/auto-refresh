# --- Auto-Refresh v0.2.2 by avalkon --- #
#I know, I have issues with remembering how I was even naming stuff at any given hour. 
#sucks, doesn't it? but at least it works. mostly.
# ---Imports--- #

import tkinter as tk
import threading
import time
import configparser
from pynput.mouse import Button, Controller
from python_imagesearch.imagesearch import imagesearch
from playsound3 import playsound
from pathlib import Path

config_file = Path(__file__).parent / "config.ini"
config = configparser.ConfigParser()
config.read(config_file)

# ---Files--- #

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
    (config_path("submit5"), config.getfloat("confidence", "submit5")),]
sound = config_path("sound")
icon = config_path("icon")

# ---Mouse positions--- #
#this is all so you could have a config file. it was all tidier when I hardcoded filepaths.

def get_position(name):
    x, y = config["positions"][name].split(",")
    return int(x), int(y)

refpos = get_position("refresh")
acqpos = get_position("acquire")
subpos = get_position("submit")

# ---Hours logging and other miscellanea--- #

refdel = config.getfloat("timing", "refresh")
acqdel = config.getfloat("timing", "acquire")
waitdel = config.getfloat("timing", "wait")
subdel = config.getfloat("timing", "submit")

log_file = Path(__file__).parent / "hours.log"
session_start_time = None
acquire_time = None
last_submit_time = None
total_acquire_submit_time = 0
submit_count = 0
session_running = False

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

def log_hours(message):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a") as f:
        f.write(f"{timestamp} - {message}\n")

def log_submit():
    global last_submit_time
    global total_acquire_submit_time
    global submit_count
    global acquire_time
    now = time.monotonic()
    if acquire_time is not None:
        acquire_elapsed = now - acquire_time
        total_acquire_submit_time += acquire_elapsed
        acquire_text = format_elapsed(acquire_elapsed)
    else:
        acquire_elapsed = None
        acquire_text = "--"
    if last_submit_time is not None:
        submit_elapsed = now - last_submit_time
        submit_text = format_elapsed(submit_elapsed)
    else:
        submit_elapsed = None
        submit_text = "--"
    if session_start_time is not None:
        session_elapsed = now - session_start_time
        session_text = format_elapsed(session_elapsed)
    else:
        session_text = "--"
    submit_count += 1
    log_hours(
        f"Task #{submit_count} | "
        f"Since Acquire: {acquire_text} | "
        f"Since submit: {submit_text} | "
        f"Session Total: {session_text}")
    last_submit_time = now

def format_elapsed(seconds):
    hours = int(seconds // 3600)
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def update_timers():
    now = time.monotonic()
    if session_running and session_start_time is not None:
        elapsed = now - session_start_time
        session_label.config(text=f"Session: {format_elapsed(elapsed)}")
    if acquire_time is not None:
        elapsed = now - acquire_time
        acquire_timer_label.config(text=f"Since Acquire: {format_elapsed(elapsed)}")
    else:
        acquire_timer_label.config(text="Since Acquire: --:--")
    if last_submit_time is not None:
        elapsed = now - last_submit_time
        submit_timer_label.config(text=f"Since Submit: {format_elapsed(elapsed)}")
    else:
        submit_timer_label.config(text="Since Submit: --:--")
    submit_count_label.config(text=f"Tasks: {submit_count}")
    root.after(1000, update_timers)

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
    global acquire_time
    global last_submit_time
    label(nta_label, "Checking...")
    label(submit_label, "Waiting")
    if not sleep(refdel, refreshing):
        return
    if found(nta):
        label(nta_label, "NTA")
        if not sleep(refdel, refreshing):
            return
        click(refpos)
        aquire_time = None
        last_submit_time = None
        #this doesn't seem to work and I don't know why. halp.
    else:
        label(nta_label, "Not NTA!")
        set_status(acquiring)

def acquire():
    global acquire_time
    if not sleep(acqdel, acquiring):
        return
    if found(acqimg):
        label(nta_label, "Acquiring!")
        label(submit_label, "Waiting")
        click(acqpos)
        acquire_time = time.monotonic()
        log_hours("Acquired")
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
    global last_submit_time
    global acquire_time
    if submit_found():
        label(submit_label, "Submitting!")
        log_submit()
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

def start_worker():
    global worker_thread
    if worker_thread and worker_thread.is_alive():
        return
    worker_thread = threading.Thread(target=worker, daemon=True)
    worker_thread.start()

def start_refresh():
    global session_start_time
    global acquire_time
    global last_submit_time
    global total_acquire_submit_time
    global submit_count
    global session_running
    session_start_time = time.monotonic()
    acquire_time = None
    last_submit_time = None
    total_acquire_submit_time = 0
    submit_count = 0
    session_running = True
    set_status(refreshing)
    label(nta_label, "Starting...")
    label(submit_label, "Waiting")
    start_worker()

def start_submit():
    set_status(submitting)
    label(submit_label, "Checking...")
    start_worker()

def stop_all(event=None):
    global session_running
    session_running = False
    set_status(stopped)
    nta_label.config(text="stopped")
    submit_label.config(text="stopped")
    checkthreads()

def checkthreads():
    threads_label.config(text=str(threading.active_count()))

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
        #you wouldn't belive how hard this was to figure out. maybe not for you, but for me.

    save_button = tk.Button(window, text="Save", width=16, command=save)
    save_button.grid(row=3, column=0, columnspan=2)

root = tk.Tk()
root.title("Auto-Refresh v0.2.2")
root.geometry("328x230+990+540")
root.minsize(328, 230)
root.iconphoto(True, tk.PhotoImage(file=icon))

root.after(1000, update_timers)
#apparently this goes here. why the fork can't it stay up there with the rest of it's friends?!

# ---Buttons n such--- #

refresh_button = tk.Button(root, text="Start Auto-Refresh", width=16, command=start_refresh)
refresh_button.grid(row=0, column=0)

submit_button = tk.Button(root, text="Auto-Submit", width=16, command=start_submit)
submit_button.grid(row=0, column=1)

nta_label = tk.Label(root, text="stopped", width=16)
nta_label.grid(row=1, column=0)

submit_label = tk.Label(root, text="Waiting", width=16)
submit_label.grid(row=1, column=1)

session_label = tk.Label(root, text="Session: 00:00", width=20)
session_label.grid(row=3, column=0)

acquire_timer_label = tk.Label(root, text="Since Acquire: 00:00", width=20)
acquire_timer_label.grid(row=3, column=1)

submit_timer_label = tk.Label(root, text="Since Submit: 00:00", width=20)
submit_timer_label.grid(row=4, column=0)

submit_count_label = tk.Label(root, text="Tasks: 0", width=20)
submit_count_label.grid(row=4, column=1)

stop_button = tk.Button(root, text="Stop", width=16, command=stop_all)
stop_button.grid(row=5, column=0, columnspan=2)
root.bind("<F12>", stop_all)
#I wish I could figure out how to make this keybind work when the window isn't in focus.

thread_button = tk.Button(root, text="Get Threadcount", width=16, command=checkthreads)
thread_button.grid(row=6, column=0)

threads_label = tk.Label(root, text="Threadcount")
threads_label.grid(row=6, column=1)

settings_button = tk.Button(root, text="Settings", width=16, command=open_settings)
settings_button.grid(row=7, column=0, columnspan=2)

credit_label = tk.Label(root, text="Auto-Refresh v0.2.2, by avalkon")
credit_label.grid(row=8, column=0, columnspan=2)

def close_program():
    global status
    status = stopped
    root.destroy()
root.protocol("WM_DELETE_WINDOW", close_program)
#it's more of an exit strategy than you'll ever need at this job...
root.mainloop()
