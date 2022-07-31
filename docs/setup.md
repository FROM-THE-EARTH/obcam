# Setup

## Environment

- Raspberry Pi Zero
- Raspberry Pi Camera V2
- Raspberry Pi OS Lite

## Setup of the OS

[Raspberry Pi Imager](https://www.raspberrypi.com/software/) enables brief preparation for booting Raspberry Pi OS.

**Steps for writing an OS image to micro SD**

1. Install [Raspberry Pi Imager](https://www.raspberrypi.com/software/).
2. Open Raspberry Pi Imager.
3. Select Raspberry Pi OS Lite (32bit) as OS.
4. Select a SD card the OS is written in.
5. Click *WRITE*.

![raspi-imager](./res/raspi-imager.gif)

## Brief setup for the flight camera mode

Using this method, you can install `obcam` and activate the flight camera mode simultaneously. The brief setup gets unser way using the script `install.sh` [in the repository](https://github.com/FROM-THE-EARTH/obcam/blob/main/install.sh).

First you should download the repository using `git clone`:

```bash
git clone https://github.com/FROM-THE-EARTH/obcam.git
```

And then, you can execute the brief setup like below:

```bash
cd obcam
sudo ./install.sh
```

That's all setup of the flight camera mode of `obcam`. You can reboot the Raspberry Pi and run the flight camera program.

!!!info "Installation of `git`"
    If `git` is not installed in the system, you can run the commands below and install `git`:

    ```bash
    sudo apt update
    sudo apt install git
    ```

## Install only `obcam` module

`obcam` can be installed using `pip`.

```bash
pip install git+https://github.com/FROM-THE-EARTH/obcam.git
```

After the installation, you can use the `obcam` command to start the flight camera application.

!!!info "If `pip` is not installed in the system"
    Right after the first booting of Raspberry Pi, `pip` might be not installed yet. In the situation, you can install `pip` following the procedures below:

    1. Download the script to install `pip`. After the command below is executed, the script `get-pip.py` is to be downloaded in the current directory.
        ```bash
        wget https://bootstrap.pypa.io/get-pip.py
        ```
    2. Execute the script `get-pip.py`.
        ```bash
        python get-pip.py
        ```

## Activate the flight camera mode

### About the flight camera mode

To activate the flight camera mode, the procedures below is required:

1. Install `obcam`.
2. Enable the Raspberry Pi Camera Board.
3. Writing a gileum file for the flight camera.
4. Activate the flight camera mode.

In the flight camera mode, the application of the flight camera automatically starts when booting a Raspberry Pi.

### Enable the Raspberry Pi Camera Board

You can enable the Raspberry Pi Camera Board just executing the script `scripts/activate_camera.sh` as the root user. The `scripts/activate_camera.sh` is [in the repository](https://github.com/FROM-THE-EARTH/obcam/blob/main/scripts/activate_camera.sh).

```bash
sudo ./scripts/activate_camera.sh
```

!!!tip "Alternatives of the method"
    - Execute the command below:
        ```bash
        sudo raspi-config noint do_camera 0
        ```
    - Setting interactively using raspi-config
        ```bash
        sudo raspi-config
        # [3 Interfacing Options] >> [I1 Legacy Camera] >> [Yes]
        ```

### Writing a gileum file

Gileum files are kinds of setting files of the application. You should write a gileum file `glm.py` before activation of the flight camera mode. The gileum file `glm.py` is in the repository, so you can overwrite the file after downloding the repository. Details of the setting parameters are written in [the page](./setting.md). But please note that the settings are already done in the `glm.py` when downloading the repository, so **you doesn't have to change the settings if there are no certain reasons**.

### Activate the flight camera mode

Using the script `scripts/activate_flightcam.sh`, you can activate the flight camera mode. The `scripts/activate_flihgtcam.sh` is also [in the repository](https://github.com/FROM-THE-EARTH/obcam/blob/main/scripts/activate_flightcam.sh).

```bash
sudo ./scripts/activate_flightcam.sh
```

## Details of the activation

In this section, details of the activate process is described. The process is not complicated so much. The point is to update the `/etc/rc.local` file in the system. The file `/etc/rc.local` is a shell script to be executed at booting.

The script `scripts/activate_flightcam.sh` inserts the line to `/etc/rc.local`, in order to execute the `obcam` program like that:

```
# /etc/rc.local

# Some lines ...

/usr/bin/python -m obcam /usr/local/src/obcam/glm.py
exit 0
```

As you can see, the `obcam` program is executed giving the gileum file `/usr/local/src/obcam/glm.py`, which is copied when executing `scripts/activate_flightcam.sh`. Therefore, there is no effects in terms of the flight camera application if you change the content of the `glm.py` in the downloaded repository, because `obcam` refers `/usr/local/src/obcam/glm.py`. **If you want apply the change of the `glm.py` in the downloaded repository, just run `scripts/activate_flightcam.sh` again, or copy the `glm.py` to `/usr/local/src/obcam/glm.py`**.
