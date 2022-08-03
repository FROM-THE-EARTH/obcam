# Trouble Shooting

## When SD cards are broken

1. Insert a broken SD card to your PC.
2. If possible, clean up and rewrite the OS image referencing [the section](./setup.md#setup-of-the-os). If the trial fails, you should use new SD card and write in the OS image to the SD card.

## When camera is not detected

1. Confirm if legacy camera support is enabled or not, referencing [the section](./setup.md#enabling-legacy-camera-support).
2. Confirm if camera cable is connected properly or not.
3. If the trouble is not solved in spite of the operations above, change camera or Raspberry Pi.

## When `obcam` doesn't work regardless of activation of the flight camera mode

1. Connect a monitor and keyboard to the Raspberry Pi and check log output from `obcam`.
2. Execute `obcam` in the terminal and check the response.
    ```bash
    sudo obcam /usr/local/src/obcam/glm.py
    ```
3. If `obcam` is not installed, install `obcam` and activate the flight camera mode, referencing [the section](./setup.md#brief-setup-for-the-flight-camera-mode).
4. If `obcam` successfully run in this way, it is possible that the flight camera mode is deactivated. Thus, activate the flight camera mode:
    ```bash
    sudo /usr/local/src/obcam/scripts/activate_flightcam.sh
    ```
5. If the shell tells you that `/usr/local/src/obcam/glm.py` doesn't exist, it is possible that the flight camera mode have never been activated. Thus, activate the flight camera mode:
    ```bash
    sudo /usr/local/src/obcam/scripts/activate_flightcam.sh
    ```
