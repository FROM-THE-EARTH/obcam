#!/bin/bash

# NOTE
# This script should be executed when the current directory is the parent
# directory of this script.

# Install `RPi.GPIO``.
# `RPi.GPIO` can be installed using `pip``, but the installation behavior is
# not stable. This method may be stabler.
apt-get update
apt-get install -y python3-rpi.gpio

# Install `obcam`.
python -m pip install .
