#!/bin/bash

# Setting for Raspberry Pi Camera
sed -i "s/start_x=0/start_x=1/g" /boot/config.txt

# Install `RPi.GPIO``.
# `RPi.GPIO` can be installed using `pip``, but the installation behavior is
# not stable. This method may be stabler.
apt-get update
apt-get install -y python3-rpi.gpio

# Install `pip`` if absent.
if !(type "pip" > /dev/null 2>&1); then
    echo "No command named pip."
    if [ ! -f ./get-pip.py ]; then
        echo "Downloding get-pip.py to install pip."
        wget https://bootstrap.pypa.io/get-pip.py
    fi

    python get-pip.py
    echo "Installed pip."
fi

# Install `obcam`.
python -m pip install .
echo "Installed obcam."

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
