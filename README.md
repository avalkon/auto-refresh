# auto-refresh v0.2.53
Python tool to automatically refresh, acquire and submit in Raterhub. See demo.png to see what it looks like.

Automatically refreshes on NTA, acquires on Acquire if available, and can submit based on timer position, without triggering 
a third-party extension ping. The auto-acquire is not quite as fast as a plugin can be, but it's probably faster than you can 
manually click. At least if you're me. Auto-submit's click is disabled by default, change it in the settings menu 
after testing that it works for you. The setting is not persistent, since I'm not using an external settings file.

Logs time spent on each task, along with running totals for session length and daily task time, both logged 
in a file and displayed onscreen. Task time logging only works if you click the auto-submit button or the Trigger 
Submission Time button, but it works whether the auto-click itself is turned on or off. 

As a bonus, the totals can double as alcohol replacements when you compare your session time to task time! Yay nta. 
Example of hours log included.

It does not currently perform any additional mouse movements to keep the extension awake, so keep that in mind. 
I'll work on that soon.

The included images and mouse positions are based on a maximized Chrome window at a screen resolution of 1920x1080; 
if you use a different resolution, you will need to edit your own images to match. Mouse positions, filenames, 
image sensitivity, delay times and such can be modified in the config.ini file in any text editor. You can, of 
course, add your own sounds, icon, etc.

The auto-submit needs more tuning, it seems to work best on longer (6+ minutes) tasks, not quite as well yet on 
shorter ones. Needs additional reference images. 

Auto refresh recognizes NTA and Acquire if available immediately from any state(except stopped), so if you want to 
submit and stop, you need to turn off the auto-refresh to not immediately grab another task.

There is a settings panel where you can enable/disable the sound(enabled by default), enable/disable the auto-submit 
click(disabled by default), and enable/disable the thread count button(disabled by default). If disabled, 
pressing the auto-submit button will still play a sound and log the task/total time when it sees the appropriate timer 
position, which is useful for both testing and just as a notification/reminder, if you don't actually want true 
auto-submit. Test first.

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

# Windows
I don't own a Windows machine, if someone would like to contribute, please do!

The .py itself should work fine on all platforms, you just have to set it up manually. The called filepaths are all 
relative now, so the program will run no matter where you put the folder. Basically:

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
