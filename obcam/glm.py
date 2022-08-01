import typing as t

import gileum


class OBCamGileum(gileum.BaseGileum):
    """Setting giluem for the obcam application.

    An object of this class should be created in a gileum file, a setting file
    of the application, when you execute the obcam application. The gileum
    file can be given to the first argument of the obcam CLI application and
    the application will search the object of this class, and finally start
    recording using the parameters defined in the object. In this sense,
    an object of this class is a setting object of the application.

    Note that the `__init__` method of this class has a essential argument,
    `timeout`. The argument `timeout` means length of recording time as
    seconds. The other arguments could be given if necessary.
    """

    timeout: float
    """Length of recording time."""

    pin_flight: int = 22
    """Pin number for a flight pin."""

    pin_led: int = 12
    """Pin number for a status LED."""

    file_mov: t.Optional[str] = None
    """Path to new video file."""

    file_log: t.Optional[str] = None
    """Path to new log file."""

    resolution: t.Tuple[int, int] = (1920, 1080)
    """Resolution of the video to be recorded."""

    framerate: int = 30
    """Framerate of the video to be recorded."""

    interval: float = 0.1
    """Wating time for recording."""

    led_blink_freq: float = 2.
    """Frequency of LED blinking."""
