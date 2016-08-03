#!/bin/sh
# clear, set-up

pkill firefox
pkill chrome
pkill -f gnome-terminal

# just in case the host changed keys
rm -rf ~/.ssh/known_hosts

rm -rf ${WORKSPACE}/records/*.flv
rm -rf ${WORKSPACE}/pytest.log

touch ${WORKSPACE}/pytest.log

# rm recrods older thank 7 days
find /var/www/html/records/* -mtime +7 -exec rm -Rf {} \;

echo "pwd:"
pwd

# stop vnc server
#pkill -f "vnc :$DISPLAY_PORT"
vncserver -kill ":$DISPLAY_PORT"

BROWSER_WIDTH=$(grep -o 'BROWSER_WIDTH =.*' conf/properties.properties | sed 's/BROWSER_WIDTH = //g')
BROWSER_HEIGHT=$(grep -o 'BROWSER_HEIGHT =.*' conf/properties.properties | sed 's/BROWSER_HEIGHT = //g')

# start vnc server
SCREEN_HEIGHT=$(expr $BROWSER_HEIGHT + $(expr $TERMINAL_HEIGHT \* 27))
echo "Total screen dimension: ${BROWSER_WIDTH}x${SCREEN_HEIGHT}"
vncserver -geometry "${BROWSER_WIDTH}x${SCREEN_HEIGHT}" ":$DISPLAY_PORT"

# open terminal
export DISPLAY=:$DISPLAY_PORT
gnome-terminal --geometry $(expr $BROWSER_WIDTH / 11)x${TERMINAL_HEIGHT}+5+${BROWSER_HEIGHT} -e "tailf ${WORKSPACE}/pytest.log"
