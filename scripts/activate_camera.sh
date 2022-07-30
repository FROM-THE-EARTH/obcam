#!/bin/bash
raspi-config nonint do_camera 0
sed -i "s/start_x=0/start_x=1/g" /boot/config.txt
