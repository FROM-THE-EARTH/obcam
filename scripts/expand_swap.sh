#!/bin/bash
if [ ! -d /var/local/obcam/ ]; then
    mkdir /var/local/obcam/
fi

if [ ! -f /var/local/obcam/swapsize ]; then
    touch /var/local/obcam/swapsize
fi

source /var/local/obcam/swapsize
if [ -z $SWAPSIZE_LAST ]; then
    SWAPSIZE_LAST=100
fi

if [ -z $SWAPSIZE ]; then
    SWAPSIZE=2048
fi

service dphys-swapfile stop
sed -i "s/CONF_SWAPSIZE=${SWAPSIZE_LAST}/CONF_SWAPSIZE=${SWAPSIZE}/g" /etc/dphys-swapfile
service dphys-swapfile start

echo "SWAPSIZE_LAST=${SWAPSIZE}" > /var/local/obcam/swapsize
