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

### `resolution`

Resolution of the video to be recorded, defaults `(640, 480)`.

### `interval`

Wating time for recording, `1.`.

### `led_blink_freq`

Frequency of LED blinking, defaults `2.`.

## Examples

```python
from obcam import OBCamGileum


glm = OBCamGileum(
    # Make the timeout shorter for tests.
    timeout=10,

    # Change path to the movie file.
    file_mov="test.h254",

    # Change path to the log file.
    flie_log="test.log",

    # Make the frequency smaller.
    led_blink_freq=1.,

    # Use the default settings.
    pin_flight=22,
    pin_led=12,
    resolution=(640, 480),
    interval=1.,
)
```