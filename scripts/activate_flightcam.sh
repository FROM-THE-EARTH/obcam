#!/bin/bash

# Copy the source code.
if [ -d /usr/local/src/obcam ]; then
    rm -r /usr/local/src/obcam
fi
cp -r $(pwd) /usr/local/src

# Setting for execution of the program at booting.
if [ ! -f /etc/rc.local.original ]; then
    cp /etc/rc.local /etc/rc.local.original
fi
rm /etc/rc.local
sed -e '$d' /etc/rc.local.original >> /etc/rc.local
echo "/usr/bin/python -m obcam /usr/local/src/obcam/glm.py" >> /etc/rc.local
echo "exit 0" >> /etc/rc.local
chmod 766 /etc/rc.local
echo "Setup of the obcam was all done. Reboot to start the obcam program."
