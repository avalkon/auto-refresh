#!/usr/bin/bash

source /opt/apps/auto-refresh/bin/activate
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
echo "Script directory: $SCRIPT_DIR"
pip uninstall -r $SCRIPT_DIR/requirements.txt
deactivate
rm -r /opt/apps/auto-refresh
rm /usr/share/applications/auto-refresh.desktop
