# auto-refresh v0.2.67
Python tool to automatically refresh, acquire and submit in Raterhub. See demo.png and demo2.png to see what it looks like. 
Nothing is ever sent off your computer.

# Auto-Refresh and Acquire
Automatically refreshes on NTA, acquires on Acquire if available. The auto-acquire is not quite as fast as an extension can 
be, but it's probably faster than you can manually click. At least if you're me. Auto-acquire is not necessary for 
time tracking if you manually trigger the acquire time.

# Auto-Submit
The auto-submit function is a time-tracker, notification sound, and auto-click. The click is disabled by default, 
change it in the settings menu after testing that it works for you. Auto-Submit does not always recognize/trigger 
on short(like 2 minutes) tasks. Probably needs more reference images. Auto-submit is not necessary for time tracking, 
if you  manually trigger the submit time.

# Time Logging
The application Logs time spent on each task, along with running totals for session length and daily task time, 
logged in a file(new file for each calendar day) and displayed onscreen. In order to use the time logging, you have to 
either use the auto-acquire, or manually trigger the acquire time(button provided), and use auto-submit, or manually 
trigger the submit time(button provided). The time tracking function of the auto-submit works whether the auto-click 
itself is turned on or off. Submit Time is also triggered by the Stop All button.

There is a button to export each days most recent Today's Tasks time to a separate spreadsheet, for easy per-day tracking
(see demo2.png). Every new week generates a new spreadsheet, and spreadsheets are never duplicated, only updated.

As a bonus, the totals in the daily logs can double as depressants when you compare your session time to 
task time! Yay nta.

# Images
The included images and mouse positions are based on a maximized Chrome window at a screen resolution of 1920x1080; 
if you use a different resolution, you will need to edit your own images to match. Mouse positions, filenames, 
image sensitivity, delay times and such can be modified in the config.ini file in any text editor. You can, of 
course, add your own sounds, icon, etc. 

Auto refresh recognizes NTA and Acquire if available immediately from any state(except stopped), so if you want to 
submit and stop, you need to turn off the auto-refresh to not immediately grab another task.

# Settings Panel
In the settings panel, you can enable/disable the sound(enabled by default), enable/disable the auto-submit 
click(disabled by default), choose which door auto-acquire prefers, turn on/off the mouse movement during auto-submit 
waiting, and enable/disable the thread count button(disabled by default). If disabled, pressing the auto-submit button 
will still play a sound and log the task/total time when it sees the appropriate timer position, which is useful for 
both testing and just as a notification/reminder, if you don't actually want true auto-submit. Test first. You can 
also set times for all of the delays here. Any settings saved in the settings panel are persistent, so they are the same 
next time you open the program as well. All of them can be set manually in the config.ini as well, that is where the 
save button writes to.

You can change what sound is played by putting your own sound into the sounds folder and modifying the config.ini in 
any text editor, along with your own images if you need to change resolutions. You can also change the mouse positions 
and delay times in the same file, as well as modifying the sensitivity of the image recognition. Instructions/descriptions 
are provided in the file.

# Installation
# Linux
The linux installer creates a venv, installs the necessary pip and apt dependencies and creates a .desktop file to access 
the program from the menu. The uninstaller removes the pip installed dependencies, but not the apt installed dependencies.

To install on Ubuntu-based Linux:

cd ~/Downloads

git clone https://github.com/avalkon/auto-refresh.git auto-refresh

cd auto-refresh

sudo ./linux-install.sh

To uninstall:

cd ~/Downloads/auto-refresh

sudo ./linux-uninstall.sh

# Windows
I don't own a Windows machine, if someone would like to contribute, please do!

The .py itself should work fine on all platforms, you just have to set it up manually. The called filepaths are all 
relative, so the program will run no matter where you put the folder. Basically:

Install Python 

Create a venv

pip install the contents of the requirements.txt file

Copy the entire auto-refresh folder into the venv

Run the .py file from the venv

# Mac:
Same problem, I don't own a Mac either, but the install should be basically the same as Windows.

# Why not just use an extension?:
https://segin.strangled.net/are-they-tracking-us.html

# Credits:
Our employers for giving us so much NTA I had time to learn to code this tool.
