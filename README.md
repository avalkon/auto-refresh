# auto-refresh
Python tool to automatically refresh, acquire and submit in Raterhub

The installer installs all necessary dependencies. 

To install:

cd ~/Downloads

git clone https://github.com/avalkon/auto-refresh.git auto-refresh

cd auto-refresh

sudo ./install.sh

# What it does:
Automatically refreshes on NTA, acquires on Acquire if available, and can submit based on timer position, without triggering a third-party extension ping. It does not currently perform any additional mouse movements to keep the extension awake, so keep that in mind. The included images are based on a maximized Chrome window at a screen resolution of 1920x1080; if you use a different resolution, you will need to edit your own photos to match. The auto-submit definitely needs tuning, it seems to work ok on longer (9+ minutes) tasks, not so well yet on shorter ones. Probably needs additional reference photos. Auto-submit as-delivered has it's mouse click(line 110 in auto-refresh-0.1.7.py) commented out so it only moves the cursor and gives a notification sound. I recommend testing it before uncommenting the click.

# Credits:
Our employers for giving us so much NTA I had time to learn to code this tool.
