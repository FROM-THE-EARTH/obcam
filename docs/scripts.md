# Scripts

There are some executable shell scripts in the repository. You can run the scripts if downloading the repository to local. In many cases, you should execute the scripts as the root user.

## `install.sh`

This script installs `obcam` and activates the flight camera mode simultaneously. This script is executed using other scripts below, so you should not delete other scripts. This script requires network connection.

```bash
sudo ./install.sh
```

## `scripts/activate_camera.sh`

This script enables the Raspberry Pi Camera Board.

```bash
sudo scripts/activate_camera.sh
```

## `scripts/activate_flightcam.sh`

This script activates the flight camera mode.

```bash
sudo scripts/activate_flightcam.sh
```

## `scripts/deactivate_flightcam.sh`

This script deactivates the flight camera mode.

```bash
sudo scripts/deactivate_flightcam.sh
```

## `scripts/install_obcam.sh`

This script just installs `obcam` using `pip`, but doesn't activate the flight camera mode. This script requires network connection.

```bash
sudo scripts/install_obcam.sh
```

## `scripts/install_pip.sh`

This script installs `pip`. This script requires network connection.

```bash
sudo scripts/install_pip.sh
```

## `scripts/uninstall_obcam.sh`

This script uninstalls `obcam` using `pip`.

```bash
sudo scripts/uninstall_obcam.sh
```
