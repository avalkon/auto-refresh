# ---Auto-Refresh v0.1.8 by avalkon---
# ---Imports----
import tkinter as tk
import time
import threading
from pynput.mouse import Button, Controller
from python_imagesearch.imagesearch import imagesearch
from playsound3 import playsound

status = 0 #0=stopped, 1=refreshing, 3=waiting, 4=submitting
status_lock = threading.Lock()
mouse = Controller()

# ---status management---

def set_status(new_status):
    global status
    with status_lock:
        status = new_status

def get_status():
    with status_lock:
        return status

# ---Thread Starters---

def start_refresh():
    if get_status() != 1:
        set_status(1)
        threading.Thread(target=auto_refresh, daemon=True).start()

def start_acquire():
    set_status(2)
    threading.Thread(target=auto_acquire, daemon=True).start()

def start_wait():
    set_status(3)
    threading.Thread(target=auto_wait, daemon=True).start()

def start_submit():
    set_status(4)
    threading.Thread(target=auto_submit, daemon=True).start()

def stop_all(*args):
    set_status(0)
    nta_label.config(text="Stopped")
    submit_label.config(text="Stopped")

# ---Functions---

def thread_count():
    threading.active_count()
    threads_label.config(text=threading.active_count())

def auto_refresh():
    while get_status() == 1:
        if get_status() != 1:
            break
        time.sleep(2)
        nta = imagesearch("/opt/apps/auto-refresh/images/nta.png")
        if get_status() != 1:
            break
        if nta[0] != -1:
            nta_label.config(text="NTA")
            submit_label.config(text="Waiting")
            time.sleep(2)
            mouse.position = (92, 65)
            mouse.click(Button.left)
        else:
            nta_label.config(text="Not NTA!")
            set_status(2)
            start_acquire()
            break

def auto_acquire():
    if get_status() == 2:
        time.sleep(0.4)
        acquire = imagesearch("/opt/apps/auto-refresh/images/acquire.png")
        if acquire[0] != -1:
            nta_label.config(text="Acquiring!")
            submit_label.config(text="Waiting")
            mouse.position = (115, 235)
            mouse.click(Button.left)
            playsound("/opt/apps/auto-refresh/sounds/sound1.mp3")
            set_status(3)
            start_wait()
        else:
            nta_label.config(text="Already acquired")
            submit_label.config(text="Waiting")
            set_status(3)
            start_wait()

def auto_wait():
    nta = imagesearch("/opt/apps/auto-refresh/images/nta.png")
    acquire = imagesearch("/opt/apps/auto-refresh/images/acquire.png")
    if nta[0] != -1:
        set_status(1)
        threading.Thread(target=auto_refresh, daemon=True).start()
    else:
        while get_status() == 3:
            nta = imagesearch("/opt/apps/auto-refresh/images/nta.png")
            acquire = imagesearch("/opt/apps/auto-refresh/images/acquire.png")
            if get_status() != 3:
                break
            elif acquire[0] != -1:
                set_status(2)
                if get_status() == 2:
                    threading.Thread(target=auto_acquire, daemon=True).start()
                    break
            elif nta[0] != -1:
                set_status(1)
                if get_status() == 1:
                    threading.Thread(target=auto_refresh, daemon=True).start()
                    break
            else:
                time.sleep(5)
                nta_label.config(text="Task")

def auto_submit():
    while True:
        if get_status() != 4:
            break
        submit = imagesearch("/opt/apps/auto-refresh/images/submit.png", .995)
        submit2 = imagesearch("/opt/apps/auto-refresh/images/submit2.png", .995)
        submit3 = imagesearch("/opt/apps/auto-refresh/images/submit3.png", .99)
        submit4 = imagesearch("/opt/apps/auto-refresh/images/submit4.png", .995)
        submit5 = imagesearch("/opt/apps/auto-refresh/images/submit5.png", .995)
        if submit[0] != -1 or submit2[0] != -1 or submit3[0] != -1 or submit4[0] != -1 or submit5[0] != -1:
            submit_label.config(text="Submitting!")
            mouse.position = (115, 1017)
#            mouse.click(Button.left)
            set_status(1)
            time.sleep(.4)
            playsound("/opt/apps/auto-refresh/sounds/sound1.mp3")
            if get_status() == 1:
                time.sleep(.4)
                threading.Thread(target=auto_refresh, daemon=True).start() 
            break
        else:
            if get_status() != 4:
                submit_label.config(text="Interrupted")
                break
            submit_label.config(text="Waiting to submit")
            time.sleep(2)
            submit_label.config(text="Checking...")

# ---GUI---

root = tk.Tk()
root.title("Auto-Refresh v0.1.8")
root.minsize(313, 140)
root.maxsize(500, 500)
root.geometry("313x170+990+540")
icon = tk.PhotoImage(file="/opt/apps/auto-refresh/images/ntaico.png")
root.iconphoto(True, icon)

# ---Buttons---

start_button = tk.Button(root, text="Start Auto-Refresh", width= 16, command=start_refresh,)
start_button.grid(row=0, column=0)

submit_button = tk.Button(root, text="Auto-Submit", width= 16, command=start_submit,)
submit_button.grid(row=0, column=1)

stop_button = tk.Button(root, text="Stop", width= 16,  command=stop_all,)
root.bind('<F12>', stop_all)
stop_button.grid(row=2, column=0, columnspan=2)

threads_button = tk.Button(root, text="Get Threadcount", width=16, command=thread_count)
threads_button.grid(row=5, column=0)

# ---Labels---

nta_label = tk.Label(root, text="Stopped", width= 16,)
nta_label.grid(row=1, column=0)

submit_label = tk.Label(root, text="Waiting", width= 16,)
submit_label.grid(row=1, column=1)

spacer = tk.Label(root, text="")
spacer.grid(row=3)

threads_label = tk.Label(root, text="Threadcount")
threads_label.grid(row=4, column=1)

credits_label = tk.Label(root, text="Auto-Refresh v0.1.8, by avalkon")
credits_label.grid(row=5, column=0, columnspan=2, sticky=tk.S)

root.mainloop()
