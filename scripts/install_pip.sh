#!/bin/bash

# Install `distutils`.
# This module is required when `pip` is installed.
apt-get update
apt-get install -y python3-distutils

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
