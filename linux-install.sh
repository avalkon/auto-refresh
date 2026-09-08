#!/usr/bin/bash

apt install -y python3 python3-xlib scrot python3-tk python3-dev python3-opencv python3-pip
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
echo "Script directory: $SCRIPT_DIR"

python3  -m venv /opt/apps/auto-refresh
source /opt/apps/auto-refresh/bin/activate
pip install -r $SCRIPT_DIR/requirements.txt
deactivate

mkdir /opt/apps/auto-refresh/images
mkdir /opt/apps/auto-refresh/sounds

cp $SCRIPT_DIR/auto-refresh.sh /opt/apps/auto-refresh/auto-refresh.sh
cp $SCRIPT_DIR/auto-refresh-0.1.7.py /opt/apps/auto-refresh/auto-refresh-0.1.7.py
cp $SCRIPT_DIR/images/ntaico.png /opt/apps/auto-refresh/images/ntaico.png
cp $SCRIPT_DIR/images/nta.ico /opt/apps/auto-refresh/images/nta.ico
cp $SCRIPT_DIR/images/nta.png /opt/apps/auto-refresh/images/nta.png
cp $SCRIPT_DIR/sounds/sound1.mp3 /opt/apps/auto-refresh/sounds/sound1.mp3
cp $SCRIPT_DIR/images/submit.png /opt/apps/auto-refresh/images/submit.png
cp $SCRIPT_DIR/images/submit2.png /opt/apps/auto-refresh/images/submit2.png
cp $SCRIPT_DIR/images/submit3.png /opt/apps/auto-refresh/images/submit3.png
cp $SCRIPT_DIR/images/submit4.png /opt/apps/auto-refresh/images/submit4.png
cp $SCRIPT_DIR/images/acquire.png /opt/apps/auto-refresh/images/acquire.png
chmod +x /opt/apps/auto-refresh/auto-refresh.sh

printf "[Desktop Entry]\n" > /usr/share/applications/auto-refresh.desktop
printf "Name=Auto-Refresh\n" >> /usr/share/applications/auto-refresh.desktop
printf "Comment=Refresh, Acquire, and Submit in Raterhub\n" >> /usr/share/applications/auto-refresh.desktop
printf "Exec=/opt/apps/auto-refresh/auto-refresh.sh\n" >> /usr/share/applications/auto-refresh.desktop
printf "Icon=/opt/apps/auto-refresh/images/ntaico.png\n" >> /usr/share/applications/auto-refresh.desktop
printf "Categories=Internet\n" >> /usr/share/applications/auto-refresh.desktop
printf "Terminal=false\n" >> /usr/share/applications/auto-refresh.desktop
printf "Type=Application\n" >> /usr/share/applications/auto-refresh.desktop

