#!/bin/bash
if [ -f /etc/rc.local.original ]; then
    rm /etc/rc.local
    mv /etc/rc.local.original /etc/rc.local
    chmod 755 /etc/rc.local
    echo "Deactivated flight camera mode."
elif
    echo "Couldn't deactivate flight camera mode. Have you ever activated the mode?"
fi
