# Setting

## gileum file

gileum files are kinds of setting files of the application. In a gileum file, an object of the `OBCamGileum` should be created. The default gileum file is prepared [in the repository](https://github.com/FROM-THE-EARTH/obcam/blob/main/glm.py). If necessary, you can change the content of the gileum file and apply the setting when executing the flight camera application.

## `OBCamGileum`

This class is the setting class of the application. You should only instantiate the class giving the parameters below.

### `timeout`

Length of recording time.

### `pin_flight`

Pin number for a flight pin, defaults `22`.

### `pin_led`

Pin number for a status LED, defaults `12`.

### `file_mov`

Path to new video file, defaults `None`.

### `file_log`

Path to new log file, defualts `None`.

### `parent_dir`

Path to the parent directory of output files, defaults `None`. If a specfied directory doesn't exist, the program automatically create the repository.

### `resolution`

Resolution of the video to be recorded, defaults `(1920, 1080)`. You cannot make the value greater than the default value, because `(1920, 1080)` is about maximum value.


### `framerate`

Framerate of the video to be recorded, defaults `30`. You cannot make the value greater than the default value, because `30` fps is about maximum value.

### `interval`

Wating time for recording, `0.1`.

### `led_blink_freq`

Frequency of LED blinking, defaults `2.`.

### `log_level`

Log level used in the application, defaults `logging.INFO` (`20`).

### `check_waiting_time`

If making log outputs during waiting time for disconnection of the flight pin or not, defaults `False`.

## Examples

```python
import logging
from obcam import OBCamGileum

glm = OBCamGileum(
    # Make the timeout shorter for tests.
    timeout=10,

    # Change path to the movie file.
    file_mov="test.h254",

    # Change path to the log file.
    flie_log="test.log",

    # Set the parent directory of the output files.
    parent_dir="/obcam-out"

    # Make the frequency smaller.
    led_blink_freq=1.,

    # Make verbose log outputs for tests.
    log_level=logging.DEBUG,

    # Observe waiting time until the flight pin is disconnected.
    check_waiting_time=True,

    # Use the default settings.
    # To use defualt values, you don't have to give corresponding arguments.
    pin_flight=22,
    pin_led=12,
    resolution=(1920, 1080),
    framerate=30,
    interval=0.1,
)
```
