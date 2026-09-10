# auto-refresh
Python tool to automatically refresh, acquire and submit in Raterhub

The installer creates a venv, installs the necessary pip and apt dependencies and creates a .desktop file to access the
program from the menu. The uninstaller removes the pip installed dependencies, but not the apt installed dependencies.

To install on Ubuntu-based Linux:

cd ~/Downloads

git clone https://github.com/avalkon/auto-refresh.git auto-refresh

cd auto-refresh

sudo ./linux-install.sh

I don't own a Windows or Mac machine, if someone would like to contribute, please do!

The .py itself should work fine on all platforms, you just have to set it up manually. The called filepaths are all 
relative now, so the program will run no matter where you put the folder.

# What it does:
Automatically refreshes on NTA, acquires on Acquire if available, and can submit based on timer position, without triggering 
a third-party extension ping. 

Logs time spent on each task, along with running totals for sessions length and cumulative task lengths, both logged 
in a file and displayed onscreen. Task time logging only works if you click the auto-submit button, but it works 
whether the auto-click is on or not. The totals double as depressants when you compare your session time to task time.
Yay nta. Example of hours log included.

It does not currently perform any additional mouse movements to keep the extension awake, so keep that in mind. 

The included images are based on a maximized Chrome window at a screen resolution of 1920x1080; if you use a different 
resolution, you will need to edit your own photos to match. 

The auto-submit needs some more tuning, it seems to work well on longer (7+ minutes) tasks, not as well yet on shorter ones. 
Probably needs additional reference photos. 

Auto refresh recognizes NTA and Acquire if available immediately from any state(except stopped), so if you want to 
submit and stop, you need to turn off the auto-refresh to not immediately grab another task.

There is a settings panel where you can turn off the sound, and enable or disable the auto-submit click. If disabled, 
pressing the auto-submit button will still play a sound when it sees the appropriate timer position, which is useful for 
both testing and just as a notification/reminder. It is disabled by default. Test first.

You can change what sound is played by putting your own sound into the sounds folder and modifying the config.ini in 
any text editor, along with your own images if you need to change resolutions. You can also change the mouse positions 
and delay times in the same file, as well as modifying the sensitivity of the image recognition. Instructions/descriptions 
are provided in the file.

# Why not just use an extension?:
https://segin.strangled.net/are-they-tracking-us.html

# Credits:
Our employers for giving us so much NTA I had time to learn to code this tool.
