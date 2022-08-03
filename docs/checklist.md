# Checklist

## Advance Preparation

- [ ] Make more than 2 SD cards Raspberry Pi OS Lite (32bit), referencing [the section](./setup.md#setup-of-the-os).
- [ ] Connect a monitor and keyboard to the Raspberry Pi.
- [ ] Boot the Raspberry Pi.
- [ ] Configure the keyboard setting.
- [ ] Configure the system settings using `raspi-config`, referencing [the section](./setup.md#essential-system-setttings-in-raspi-config).
    - [ ] WiFi setting for network connection.
    - [ ] Enabling legacy camera support.
- [ ] Install `git`:
    ```bash
    sudo apt update
    sudo apt install -y git
    ```
- [ ] Clone the `obcam` repository:
    ```bash
    git clone https://github.com/FROM-THE-EARTH/obcam.git
    cd obcam
    ```
- [ ] Confirm `glm.py` in the repository and change the content if necessary.
    ```bash
    # Confirm the content
    less glm.py

    # Change the content
    vi glm.py
    ```
- [ ] Install `obcam` and activate the flight camera mode:
    ```bash
    sudo ./install.sh
    ```
- [ ] Reboot the system:
    ```bash
    sudo reboot
    ```
- [ ] Check the LED is blinking (which means the program waits for connection of a flight pin). If the LED is blinking, then all preparation is done. Otherwise, connect a monitor and keyboard to the Raspberry Pi and view log output from the program. For more log output, you can change value of the parameter `log_level` to `logging.DEBUG` in `/usr/local/src/obcam/glm.py`:
    ```bash
    sudo vi /usr/local/src/obcam/glm.py

    # in the file
    #
    # ...
        - log_level=logging.INFO,
        + log_level=logging.DEBUG,
    ```

## In a rocket range

- [ ] Connect a Raspberry Pi which is setup already, flight pin cable, and 9V battery to the board.
- [ ] Confirm the LED is blinking. If the flight pin is already connected, the LED doesn't blink but is turned off. If the LED is being turned off dispite the flight pin is disconnected, connect a monitor and keyboard to the Raspberry Pi and vie log output from the program. If the camera is not detected, try to enable legacy camera support referencing [the section](./setup.md#enabling-legacy-camera-support) and reconnect camera cable.
- [ ] If the program is executed successfully, put the board in to a plastic bag.
- [ ] Close up the zipper of the plastic bag using curing tape.
- [ ] Put the plastic bag in to another platic bag and close up the zipper again.
- [ ] Put some block of styrofoam in to the nose corn.
- [ ] Put the camera in to the nose cone and fix the camera using curing tape.
- [ ] Put the plastic bag in to the nose corn.
- [ ] Connect the flight pin cable to the cable for the main board.
- [ ] Connect the flight pin.
- [ ] If you need, activate certain [command](./flightcam.md#commands).

## After collecting the body

- [ ] Remove the SD card from the Raspberry Pi and clean the SD card.
- [ ] Insert the SD card to your PC.
- [ ] Extract the movie file and log file from the SD, referencing [the section](./flightcam.md#extract-data-from-sd-cards).
- [ ] Confirm the movie and log.
